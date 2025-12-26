"""
КЛИЕНТ ПРИЛОЖЕНИЯ
=================

Клиент для подключения к серверу и выполнения задач.
Каждый клиент запускается в своем потоке.
"""

import socket
import threading
import time
import json
import uuid
from datetime import datetime
from typing import Optional, Callable, Any
from queue import Queue

from shared.protocols import (
    Message, MessageType, TaskRequest, TaskResponse,
    TaskType, ClientServerProtocol
)
from client.client_logger import ClientLogger


class Client:
    """Клиент приложения."""

    def __init__(self, server_host: str = 'localhost', server_port: int = 8888,
                 client_name: str = None):
        """
        Инициализация клиента.

        Args:
            server_host: Хост сервера
            server_port: Порт сервера
            client_name: Имя клиента (если None - генерируется)
        """
        self.server_host = server_host
        self.server_port = server_port
        self.client_name = client_name or f"Client_{uuid.uuid4().hex[:8]}"
        self.client_id = str(uuid.uuid4())

        self.socket = None
        self.connected = False
        self.running = False

        # Очереди для сообщений
        self.response_queue = Queue()
        self.message_queue = Queue()

        # Callback для обработки ответов
        self.response_callbacks = {}

        # Инициализация логгера
        self.logger = ClientLogger(self.client_name)

        self.logger.info(f"Клиент инициализирован: {self.client_name} (ID: {self.client_id})")

    def connect(self, timeout: int = 10) -> bool:
        """
        Подключение к серверу.

        Args:
            timeout: Таймаут подключения в секундах

        Returns:
            True если подключение успешно
        """
        try:
            self.logger.info(f"Подключение к серверу {self.server_host}:{self.server_port}")

            # Создание сокета
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(timeout)

            # Подключение
            self.socket.connect((self.server_host, self.server_port))

            # Отправка сообщения подключения
            connect_message = ClientServerProtocol.create_connect_message(
                self.client_id, self.client_name
            )
            self._send_message(connect_message)

            # Получение ответа
            response = self._receive_message(timeout=5)

            if response and response.message_type == MessageType.STATUS:
                self.connected = True
                self.running = True

                # Запуск потоков
                self._start_threads()

                self.logger.info(f"Успешно подключен к серверу")
                self.logger.client_message(f"подключен к серверу")

                return True
            else:
                self.logger.error("Не получили подтверждение подключения от сервера")
                return False

        except socket.timeout:
            self.logger.error("Таймаут подключения к серверу")
            return False
        except ConnectionRefusedError:
            self.logger.error(f"Сервер {self.server_host}:{self.server_port} недоступен")
            return False
        except Exception as e:
            self.logger.error(f"Ошибка подключения: {e}")
            return False

    def disconnect(self):
        """Отключение от сервера."""
        if not self.connected:
            return

        self.logger.info("Отключение от сервера...")
        self.running = False

        # Отправка сообщения отключения
        try:
            disconnect_message = ClientServerProtocol.create_disconnect_message(self.client_id)
            self._send_message(disconnect_message)
        except:
            pass

        # Остановка потоков
        self._stop_threads()

        # Закрытие сокета
        if self.socket:
            try:
                self.socket.close()
            except:
                pass

        self.connected = False
        self.logger.info("Отключен от сервера")
        self.logger.client_message(f"отключен от сервера")

    def execute_task(self, task_type: TaskType, parameters: Dict[str, Any],
                     callback: Optional[Callable] = None) -> Optional[TaskResponse]:
        """
        Выполнение задачи на сервере.

        Args:
            task_type: Тип задачи
            parameters: Параметры задачи
            callback: Функция обратного вызова для асинхронного ответа

        Returns:
            Ответ сервера или None если используется callback
        """
        if not self.connected:
            self.logger.error("Не подключен к серверу")
            return None

        try:
            # Создание запроса
            task_request = TaskRequest(task_type=task_type, parameters=parameters)

            # Логируем отправку запроса
            task_description = self._get_task_description(task_type, parameters)
            self.logger.client_message(f"отправлен запрос на {task_description}")

            # Если есть callback - используем асинхронный режим
            if callback:
                message_id = str(uuid.uuid4())
                self.response_callbacks[message_id] = callback

                # Создаем сообщение с нашим ID
                message = Message.create(
                    message_type=MessageType.TASK_REQUEST,
                    client_id=self.client_id,
                    data=task_request.to_dict()
                )
                message.message_id = message_id

                self._send_message(message)
                return None

            # Синхронный режим - отправляем и ждем ответ
            else:
                message = ClientServerProtocol.create_task_request(
                    self.client_id, task_request
                )

                # Отправляем запрос
                self._send_message(message)

                # Ждем ответ
                start_time = time.time()
                timeout = 30  # Таймаут ожидания ответа

                while time.time() - start_time < timeout:
                    if not self.response_queue.empty():
                        response_message = self.response_queue.get()

                        if response_message.message_type == MessageType.TASK_RESPONSE:
                            task_response = TaskResponse.from_dict(response_message.data)

                            # Логируем результат
                            if task_response.success:
                                self.logger.client_message(
                                    f"выполнена {task_description} "
                                    f"(время: {task_response.execution_time:.2f}с)"
                                )
                            else:
                                self.logger.client_message(
                                    f"ошибка при выполнении {task_description}: "
                                    f"{task_response.error_message}"
                                )

                            return task_response

                    time.sleep(0.1)

                self.logger.error(f"Таймаут ожидания ответа на задачу {task_type.value}")
                return None

        except Exception as e:
            self.logger.error(f"Ошибка выполнения задачи: {e}")
            return None

    def send_heartbeat(self):
        """Отправка heartbeat сообщения."""
        if self.connected:
            try:
                heartbeat_message = ClientServerProtocol.create_heartbeat_message(self.client_id)
                self._send_message(heartbeat_message)
            except:
                pass

    def _start_threads(self):
        """Запуск рабочих потоков."""
        # Поток для приема сообщений
        self.receive_thread = threading.Thread(target=self._receive_loop, daemon=True)
        self.receive_thread.start()

        # Поток для обработки сообщений
        self.process_thread = threading.Thread(target=self._process_messages, daemon=True)
        self.process_thread.start()

        # Поток для heartbeat
        self.heartbeat_thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
        self.heartbeat_thread.start()

    def _stop_threads(self):
        """Остановка рабочих потоков."""
        self.running = False

        # Ждем завершения потоков
        if hasattr(self, 'receive_thread'):
            self.receive_thread.join(timeout=1)

        if hasattr(self, 'process_thread'):
            self.process_thread.join(timeout=1)

        if hasattr(self, 'heartbeat_thread'):
            self.heartbeat_thread.join(timeout=1)

    def _receive_loop(self):
        """Цикл приема сообщений от сервера."""
        while self.running and self.connected:
            try:
                message = self._receive_message(timeout=1)
                if message:
                    self.message_queue.put(message)
            except socket.timeout:
                continue
            except Exception as e:
                self.logger.error(f"Ошибка приема сообщений: {e}")
                if self.connected:
                    self.disconnect()
                break

    def _process_messages(self):
        """Обработка полученных сообщений."""
        while self.running:
            try:
                if not self.message_queue.empty():
                    message = self.message_queue.get()

                    if message.message_type == MessageType.TASK_RESPONSE:
                        # Обрабатываем ответ на задачу
                        self._handle_task_response(message)

                    elif message.message_type == MessageType.STATUS:
                        # Статусные сообщения
                        self.logger.info(f"Статус от сервера: {message.data.get('status')}")

                    elif message.message_type == MessageType.ERROR:
                        # Сообщения об ошибках
                        self.logger.error(f"Ошибка от сервера: {message.data.get('error')}")

                    elif message.message_type == MessageType.HEARTBEAT:
                        # Heartbeat - игнорируем
                        pass

                else:
                    time.sleep(0.1)

            except Exception as e:
                self.logger.error(f"Ошибка обработки сообщений: {e}")

    def _handle_task_response(self, message: Message):
        """Обработка ответа на задачу."""
        try:
            task_response = TaskResponse.from_dict(message.data)

            # Проверяем, есть ли callback для этого сообщения
            if message.message_id in self.response_callbacks:
                callback = self.response_callbacks.pop(message.message_id)
                callback(task_response)

            # Иначе помещаем в очередь для синхронных запросов
            else:
                self.response_queue.put(message)

        except Exception as e:
            self.logger.error(f"Ошибка обработки ответа задачи: {e}")

    def _heartbeat_loop(self):
        """Цикл отправки heartbeat сообщений."""
        while self.running and self.connected:
            try:
                self.send_heartbeat()
                time.sleep(10)  # Отправляем каждые 10 секунд
            except Exception as e:
                self.logger.error(f"Ошибка heartbeat: {e}")

    def _send_message(self, message: Message):
        """Отправка сообщения на сервер."""
        try:
            data = message.to_json().encode('utf-8')
            message_length = len(data)

            # Отправляем длину сообщения
            self.socket.sendall(message_length.to_bytes(4, 'big'))

            # Отправляем само сообщение
            self.socket.sendall(data)

        except Exception as e:
            self.logger.error(f"Ошибка отправки сообщения: {e}")
            raise

    def _receive_message(self, timeout: int = 5) -> Optional[Message]:
        """Получение сообщения от сервера."""
        try:
            # Устанавливаем таймаут
            self.socket.settimeout(timeout)

            # Получаем длину сообщения
            length_bytes = self.socket.recv(4)
            if not length_bytes:
                return None

            message_length = int.from_bytes(length_bytes, 'big')

            # Получаем само сообщение
            data = b''
            while len(data) < message_length:
                chunk = self.socket.recv(min(4096, message_length - len(data)))
                if not chunk:
                    return None
                data += chunk

            # Декодируем сообщение
            message = Message.from_json(data.decode('utf-8'))
            return message

        except socket.timeout:
            return None
        except Exception as e:
            self.logger.debug(f"Ошибка приема сообщения: {e}")
            return None

    def _get_task_description(self, task_type: TaskType, parameters: Dict[str, Any]) -> str:
        """Получение описания задачи для логов."""
        descriptions = {
            TaskType.TASK1_SUM_ARRAYS: "сумму массивов",
            TaskType.TASK3_ROTATE_MATRIX: "поворот матрицы",
            TaskType.TASK8_COMMON_NUMBERS: "поиск общих чисел",
            TaskType.GENERATE_ARRAY: "генерацию массива",
            TaskType.GENERATE_MATRIX: "генерацию матрицы",
            TaskType.VALIDATE_DATA: "валидацию данных"
        }

        desc = descriptions.get(task_type, task_type.value)

        # Добавляем детали
        if task_type == TaskType.TASK1_SUM_ARRAYS:
            size1 = len(parameters.get('array1', []))
            size2 = len(parameters.get('array2', []))
            desc += f" ({size1}/{size2} элементов)"

        elif task_type == TaskType.TASK3_ROTATE_MATRIX:
            matrix = parameters.get('matrix', [])
            rows = len(matrix)
            cols = len(matrix[0]) if rows > 0 else 0
            direction = parameters.get('direction', 'clockwise')
            desc += f" ({rows}x{cols}, {direction})"

        elif task_type == TaskType.TASK8_COMMON_NUMBERS:
            size1 = len(parameters.get('array1', []))
            size2 = len(parameters.get('array2', []))
            desc += f" ({size1}/{size2} элементов)"

        elif task_type == TaskType.GENERATE_ARRAY:
            size = parameters.get('size', 0)
            desc += f" ({size} элементов)"

        elif task_type == TaskType.GENERATE_MATRIX:
            rows = parameters.get('rows', 0)
            cols = parameters.get('cols', 0)
            desc += f" ({rows}x{cols})"

        return desc

    def is_connected(self) -> bool:
        """Проверка подключения к серверу."""
        return self.connected

    def get_client_info(self) -> Dict[str, Any]:
        """Получение информации о клиенте."""
        return {
            'id': self.client_id,
            'name': self.client_name,
            'server': f"{self.server_host}:{self.server_port}",
            'connected': self.connected,
            'connection_time': datetime.now().strftime('%H:%M:%S') if self.connected else None
        }
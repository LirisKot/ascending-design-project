"""
СЕРВЕР ПРИЛОЖЕНИЯ
=================

Однопоточный сервер для выполнения расчетов.
Эмулирует длительные вычисления с помощью случайных пауз.
"""

import socket
import threading
import time
import json
import random
from datetime import datetime
from typing import Dict, Optional
from queue import Queue

from protocols import (
    Message, MessageType, TaskRequest, TaskResponse,
    ClientServerProtocol
)
from logger_serv import ServerLogger
from serv_task_proc import TaskProcessor



class Server:
    """Основной сервер приложения."""

    def __init__(self, host: str = 'localhost', port: int = 8888):
        """
        Инициализация сервера.

        Args:
            host: Хост сервера
            port: Порт сервера
        """
        self.host = host
        self.port = port
        self.server_socket = None
        self.running = False
        self.clients: Dict[str, Dict] = {}
        self.message_queue = Queue()

        # Инициализация компонентов
        self.logger = ServerLogger()
        self.task_processor = TaskProcessor(self.logger)

        # Блокировки для потокобезопасности
        self.clients_lock = threading.Lock()

        self.logger.info(f"Сервер инициализирован: {host}:{port}")

    def start(self):
        """Запуск сервера."""
        try:
            # Создание сокета
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.server_socket.settimeout(1)  # Таймаут для проверки running

            self.running = True

            self.logger.info(f"Сервер запущен на {self.host}:{self.port}")
            self.logger.info("Ожидание подключений...")

            # Запуск обработки сообщений
            message_thread = threading.Thread(target=self._process_messages, daemon=True)
            message_thread.start()

            # Основной цикл принятия подключений
            while self.running:
                try:
                    client_socket, client_address = self.server_socket.accept()

                    # Создание потока для клиента
                    client_thread = threading.Thread(
                        target=self._handle_client,
                        args=(client_socket, client_address),
                        daemon=True
                    )
                    client_thread.start()

                    self.logger.info(f"Принято подключение от {client_address}")

                except socket.timeout:
                    continue  # Таймаут для проверки running
                except Exception as e:
                    if self.running:  # Логируем только если сервер запущен
                        self.logger.error(f"Ошибка при принятии подключения: {e}")

        except Exception as e:
            self.logger.error(f"Ошибка запуска сервера: {e}")
            raise

    def stop(self):
        """Остановка сервера."""
        self.logger.info("Остановка сервера...")
        self.running = False

        # Закрытие всех клиентских соединений
        with self.clients_lock:
            for client_id, client_info in self.clients.items():
                try:
                    client_info['socket'].close()
                    self.logger.info(f"Закрыто соединение с клиентом {client_id}")
                except:
                    pass

            self.clients.clear()

        # Закрытие серверного сокета
        if self.server_socket:
            self.server_socket.close()

        self.logger.info("Сервер остановлен")

    def _handle_client(self, client_socket: socket.socket, client_address: tuple):
        """
        Обработка клиентского подключения.

        Args:
            client_socket: Сокет клиента
            client_address: Адрес клиента
        """
        client_id = None

        try:
            # Получение первого сообщения (подключение)
            data = self._receive_data(client_socket)
            if not data:
                return

            try:
                message = Message.from_json(data)

                if message.message_type != MessageType.CONNECT:
                    self.logger.warning(f"Первое сообщение не CONNECT от {client_address}")
                    return

                client_id = message.client_id
                client_name = message.data.get('client_name', 'Unknown')

                # Регистрация клиента
                with self.clients_lock:
                    self.clients[client_id] = {
                        'socket': client_socket,
                        'address': client_address,
                        'name': client_name,
                        'connected_at': datetime.now()
                    }

                self.logger.info(f"Клиент подключен: {client_name} ({client_id})")

                # Отправка подтверждения
                response = ClientServerProtocol.create_status_message(
                    client_id,
                    f"Подключение установлено. Добро пожаловать, {client_name}!"
                )
                self._send_message(client_socket, response)

                # Основной цикл обработки сообщений от клиента
                while self.running:
                    data = self._receive_data(client_socket)
                    if not data:
                        break

                    try:
                        message = Message.from_json(data)

                        # Обработка сообщения
                        if message.message_type == MessageType.DISCONNECT:
                            self.logger.info(f"Клиент {client_name} отключился")
                            break

                        elif message.message_type == MessageType.TASK_REQUEST:
                            # Помещаем задачу в очередь для обработки
                            task_request = TaskRequest.from_dict(message.data)
                            self.message_queue.put((client_id, message, task_request))

                        elif message.message_type == MessageType.HEARTBEAT:
                            # Heartbeat - просто обновляем время последней активности
                            pass

                        else:
                            self.logger.warning(f"Неизвестный тип сообщения от {client_id}: {message.message_type}")

                    except json.JSONDecodeError as e:
                        self.logger.error(f"Ошибка декодирования JSON от {client_id}: {e}")
                    except Exception as e:
                        self.logger.error(f"Ошибка обработки сообщения от {client_id}: {e}")

            except json.JSONDecodeError as e:
                self.logger.error(f"Ошибка декодирования JSON при подключении: {e}")
            except Exception as e:
                self.logger.error(f"Ошибка обработки подключения: {e}")

        except Exception as e:
            self.logger.error(f"Ошибка в обработчике клиента {client_address}: {e}")

        finally:
            # Удаление клиента
            if client_id:
                with self.clients_lock:
                    if client_id in self.clients:
                        del self.clients[client_id]

            # Закрытие сокета
            try:
                client_socket.close()
            except:
                pass

            if client_id:
                self.logger.info(f"Соединение с клиентом {client_id} закрыто")

    def _process_messages(self):
        """Обработка сообщений из очереди."""
        while self.running:
            try:
                if not self.message_queue.empty():
                    client_id, original_message, task_request = self.message_queue.get()

                    # Логируем начало обработки
                    self.logger.info(f"Начало обработки задачи от клиента {client_id}: {task_request.task_type.value}")

                    # Выполнение задачи
                    try:
                        # Эмуляция задержки перед началом обработки
                        delay = random.uniform(0.1, 0.5)
                        time.sleep(delay)

                        # Выполнение задачи
                        task_response = self.task_processor.process_task(task_request)

                        # Отправка ответа клиенту
                        with self.clients_lock:
                            if client_id in self.clients:
                                client_socket = self.clients[client_id]['socket']
                                response_message = ClientServerProtocol.create_task_response(
                                    client_id, task_response
                                )
                                self._send_message(client_socket, response_message)

                                # Логируем завершение
                                if task_response.success:
                                    self.logger.info(
                                        f"Задача от клиента {client_id} выполнена успешно "
                                        f"(время: {task_response.execution_time:.2f}с)"
                                    )
                                else:
                                    self.logger.warning(
                                        f"Задача от клиента {client_id} завершилась с ошибкой: "
                                        f"{task_response.error_message}"
                                    )

                    except Exception as e:
                        self.logger.error(f"Ошибка обработки задачи от {client_id}: {e}")

                        # Отправка ошибки клиенту
                        with self.clients_lock:
                            if client_id in self.clients:
                                client_socket = self.clients[client_id]['socket']
                                error_response = TaskResponse(
                                    success=False,
                                    result=None,
                                    error_message=str(e),
                                    execution_time=0
                                )
                                response_message = ClientServerProtocol.create_task_response(
                                    client_id, error_response
                                )
                                self._send_message(client_socket, response_message)

                else:
                    time.sleep(0.1)  # Небольшая пауза чтобы не грузить CPU

            except Exception as e:
                self.logger.error(f"Ошибка в обработчике сообщений: {e}")
                time.sleep(1)

    def _receive_data(self, sock: socket.socket, buffer_size: int = 4096) -> Optional[str]:
        """
        Получение данных из сокета.

        Args:
            sock: Сокет для чтения
            buffer_size: Размер буфера

        Returns:
            Полученные данные или None
        """
        try:
            # Получаем длину сообщения (первые 4 байта)
            length_bytes = sock.recv(4)
            if not length_bytes:
                return None

            message_length = int.from_bytes(length_bytes, 'big')

            # Получаем само сообщение
            data = b''
            while len(data) < message_length:
                chunk = sock.recv(min(buffer_size, message_length - len(data)))
                if not chunk:
                    return None
                data += chunk

            return data.decode('utf-8')

        except Exception as e:
            self.logger.debug(f"Ошибка при получении данных: {e}")
            return None

    def _send_message(self, sock: socket.socket, message: Message):
        """
        Отправка сообщения через сокет.

        Args:
            sock: Сокет для отправки
            message: Сообщение для отправки
        """
        try:
            data = message.to_json().encode('utf-8')
            message_length = len(data)

            # Отправляем длину сообщения (4 байта)
            sock.sendall(message_length.to_bytes(4, 'big'))

            # Отправляем само сообщение
            sock.sendall(data)

        except Exception as e:
            self.logger.error(f"Ошибка отправки сообщения: {e}")
            raise

    def get_clients_count(self) -> int:
        """Получение количества подключенных клиентов."""
        with self.clients_lock:
            return len(self.clients)

    def get_clients_info(self) -> list:
        """Получение информации о подключенных клиентах."""
        with self.clients_lock:
            return [
                {
                    'id': client_id,
                    'name': info['name'],
                    'address': info['address'],
                    'connected_at': info['connected_at'].strftime('%H:%M:%S')
                }
                for client_id, info in self.clients.items()
            ]

    def get_threads_info(self):
        """Получение информации о потоках сервера."""
        import threading

        threads = []
        for thread in threading.enumerate():
            threads.append({
                'name': thread.name,
                'ident': thread.ident,
                'daemon': thread.daemon,
                'alive': thread.is_alive()
            })

        return threads


def start_server():
    """Запуск сервера из командной строки."""
    import argparse

    parser = argparse.ArgumentParser(description='Запуск сервера приложения')
    parser.add_argument('--host', default='localhost', help='Хост сервера')
    parser.add_argument('--port', type=int, default=8888, help='Порт сервера')
    parser.add_argument('--log-file', default='server.log', help='Файл для логов')

    args = parser.parse_args()

    server = Server(host=args.host, port=args.port)

    try:
        server.start()
    except KeyboardInterrupt:
        print("\nОстановка сервера...")
        server.stop()
    except Exception as e:
        print(f"Ошибка: {e}")
        server.stop()


if __name__ == "__main__":
    start_server()
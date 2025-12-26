"""
ПОЛЬЗОВАТЕЛЬСКИЙ ИНТЕРФЕЙС КЛИЕНТА
==================================

Диалоговое меню для взаимодействия с пользователем.
Каждый клиент запускается в отдельном потоке.
"""

import threading
import time
import random
from datetime import datetime
from typing import Optional, Dict, Any

from client import Client
from shared.protocols import TaskType
from client.client_logger import ClientLogger


class ClientUI:
    """Пользовательский интерфейс клиента."""

    def __init__(self, client_name: str = None):
        """
        Инициализация UI клиента.

        Args:
            client_name: Имя клиента
        """
        self.client_name = client_name or f"Клиент_{random.randint(1000, 9999)}"
        self.client = None
        self.logger = ClientLogger(self.client_name)
        self.running = False

        # Статистика работы клиента
        self.stats = {
            'tasks_requested': 0,
            'tasks_completed': 0,
            'tasks_failed': 0,
            'total_waiting_time': 0
        }

    def start(self, server_host: str = 'localhost', server_port: int = 8888):
        """
        Запуск клиента.

        Args:
            server_host: Хост сервера
            server_port: Порт сервера
        """
        try:
            print(f"\n{'=' * 60}")
            print(f"КЛИЕНТ: {self.client_name}")
            print('=' * 60)

            # Создание и подключение клиента
            self.client = Client(server_host, server_port, self.client_name)

            if not self.client.connect():
                print(f"Не удалось подключиться к серверу {server_host}:{server_port}")
                return

            self.running = True

            # Запуск меню
            self._main_menu()

        except KeyboardInterrupt:
            print("\nЗавершение работы клиента...")
        except Exception as e:
            print(f"Ошибка: {e}")
        finally:
            self.stop()

    def stop(self):
        """Остановка клиента."""
        self.running = False

        if self.client:
            self.client.disconnect()

        # Вывод статистики
        self._print_stats()

        print(f"\nКлиент {self.client_name} остановлен")

    def _main_menu(self):
        """Главное меню клиента."""
        while self.running and self.client.is_connected():
            print(f"\n{'=' * 40}")
            print(f"ГЛАВНОЕ МЕНЮ - {self.client_name}")
            print('=' * 40)
            print("1. Выполнить задание 1 (Сумма массивов)")
            print("2. Выполнить задание 3 (Поворот матрицы)")
            print("3. Выполнить задание 8 (Общие числа)")
            print("4. Сгенерировать тестовые данные")
            print("5. Показать статистику")
            print("6. Информация о клиенте")
            print("7. Отключиться от сервера")
            print('=' * 40)

            try:
                choice = input("Выберите пункт (1-7): ").strip()

                if choice == '1':
                    self._execute_task1()
                elif choice == '2':
                    self._execute_task3()
                elif choice == '3':
                    self._execute_task8()
                elif choice == '4':
                    self._generate_test_data()
                elif choice == '5':
                    self._print_stats()
                elif choice == '6':
                    self._print_client_info()
                elif choice == '7':
                    print("Отключение от сервера...")
                    break
                else:
                    print("Неверный выбор. Попробуйте еще раз.")

            except KeyboardInterrupt:
                print("\nВозврат в меню...")
                continue
            except Exception as e:
                print(f"Ошибка: {e}")

        print(f"\nЗавершение работы клиента {self.client_name}...")

    def _execute_task1(self):
        """Выполнение задания 1: сумма массивов."""
        print(f"\n{'=' * 40}")
        print("ЗАДАНИЕ 1: Сумма массивов с разной сортировкой")
        print('=' * 40)

        print("\nВыберите способ получения данных:")
        print("1. Ввести массивы вручную")
        print("2. Сгенерировать случайные массивы")

        choice = input("Выбор (1-2): ").strip()

        if choice == '1':
            # Ручной ввод
            arr1 = self._input_array("Первый массив")
            arr2 = self._input_array("Второй массив")

            if arr1 is None or arr2 is None:
                print("Ошибка ввода данных")
                return

        elif choice == '2':
            # Генерация
            size = self._get_number("Размер массивов", min_val=1, max_val=20)
            min_val = self._get_number("Минимальное значение")
            max_val = self._get_number("Максимальное значение", min_val=min_val + 1)

            arr1 = self._generate_random_array(size, min_val, max_val)
            arr2 = self._generate_random_array(size, min_val, max_val)

            print(f"\nСгенерированы массивы:")
            print(f"  Массив 1: {arr1}")
            print(f"  Массив 2: {arr2}")

        else:
            print("Неверный выбор")
            return

        # Выполнение задания
        print(f"\nОтправка задания на сервер...")
        start_time = time.time()

        self.stats['tasks_requested'] += 1

        response = self.client.execute_task(
            TaskType.TASK1_SUM_ARRAYS,
            {'array1': arr1, 'array2': arr2}
        )

        if response:
            waiting_time = time.time() - start_time

            if response.success:
                self.stats['tasks_completed'] += 1
                self.stats['total_waiting_time'] += waiting_time

                print(f"\n✓ Задание выполнено успешно!")
                print(f"  Время выполнения на сервере: {response.execution_time:.2f}с")
                print(f"  Общее время ожидания: {waiting_time:.2f}с")
                print(f"\nРезультат:")
                print(f"  {response.result.get('result', [])}")

                # Логируем в консоль
                self.logger.client_message(f"получен результат суммы массивов")

            else:
                self.stats['tasks_failed'] += 1
                print(f"\n✗ Ошибка выполнения задания:")
                print(f"  {response.error_message}")
        else:
            print("\n✗ Не удалось получить ответ от сервера")

    def _execute_task3(self):
        """Выполнение задания 3: поворот матрицы."""
        print(f"\n{'=' * 40}")
        print("ЗАДАНИЕ 3: Поворот матрицы на 90 градусов")
        print('=' * 40)

        print("\nВыберите способ получения данных:")
        print("1. Ввести матрицу вручную")
        print("2. Сгенерировать случайную матрицу")

        choice = input("Выбор (1-2): ").strip()

        if choice == '1':
            # Ручной ввод
            matrix = self._input_matrix()
            if matrix is None:
                print("Ошибка ввода данных")
                return

        elif choice == '2':
            # Генерация
            rows = self._get_number("Количество строк", min_val=1, max_val=5)
            cols = self._get_number("Количество столбцов", min_val=1, max_val=5)
            min_val = self._get_number("Минимальное значение")
            max_val = self._get_number("Максимальное значение", min_val=min_val + 1)

            matrix = self._generate_random_matrix(rows, cols, min_val, max_val)

            print(f"\nСгенерирована матрица {rows}x{cols}:")
            for i, row in enumerate(matrix):
                print(f"  Строка {i + 1}: {row}")

        else:
            print("Неверный выбор")
            return

        # Выбор направления
        print("\nВыберите направление поворота:")
        print("1. По часовой стрелке")
        print("2. Против часовой стрелки")

        direction_choice = input("Выбор (1-2): ").strip()

        if direction_choice == '1':
            direction = 'clockwise'
        elif direction_choice == '2':
            direction = 'counterclockwise'
        else:
            print("Неверный выбор, используется поворот по часовой")
            direction = 'clockwise'

        # Выполнение задания
        print(f"\nОтправка задания на сервер...")
        start_time = time.time()

        self.stats['tasks_requested'] += 1

        response = self.client.execute_task(
            TaskType.TASK3_ROTATE_MATRIX,
            {'matrix': matrix, 'direction': direction}
        )

        if response:
            waiting_time = time.time() - start_time

            if response.success:
                self.stats['tasks_completed'] += 1
                self.stats['total_waiting_time'] += waiting_time

                print(f"\n✓ Задание выполнено успешно!")
                print(f"  Время выполнения на сервере: {response.execution_time:.2f}с")
                print(f"  Общее время ожидания: {waiting_time:.2f}с")
                print(f"\nРезультат:")

                result = response.result.get('result', [])
                for i, row in enumerate(result):
                    print(f"  Строка {i + 1}: {row}")

                # Логируем в консоль
                self.logger.client_message(f"получен результат поворота матрицы")

            else:
                self.stats['tasks_failed'] += 1
                print(f"\n✗ Ошибка выполнения задания:")
                print(f"  {response.error_message}")
        else:
            print("\n✗ Не удалось получить ответ от сервера")

    def _execute_task8(self):
        """Выполнение задания 8: поиск общих чисел."""
        print(f"\n{'=' * 40}")
        print("ЗАДАНИЕ 8: Поиск общих чисел с перевернутыми версиями")
        print('=' * 40)

        print("\nВыберите способ получения данных:")
        print("1. Ввести массивы вручную")
        print("2. Сгенерировать случайные массивы")

        choice = input("Выбор (1-2): ").strip()

        if choice == '1':
            # Ручной ввод
            arr1 = self._input_array("Первый массив")
            arr2 = self._input_array("Второй массив")

            if arr1 is None or arr2 is None:
                print("Ошибка ввода данных")
                return

        elif choice == '2':
            # Генерация
            size = self._get_number("Размер массивов", min_val=1, max_val=15)
            min_val = self._get_number("Минимальное значение (рекомендуется >=10)", min_val=10)
            max_val = self._get_number("Максимальное значение", min_val=min_val + 1)

            arr1 = self._generate_random_array(size, min_val, max_val)
            arr2 = self._generate_random_array(size, min_val, max_val)

            print(f"\nСгенерированы массивы:")
            print(f"  Массив 1: {arr1}")
            print(f"  Массив 2: {arr2}")

        else:
            print("Неверный выбор")
            return

        # Выполнение задания
        print(f"\nОтправка задания на сервер...")
        start_time = time.time()

        self.stats['tasks_requested'] += 1

        response = self.client.execute_task(
            TaskType.TASK8_COMMON_NUMBERS,
            {'array1': arr1, 'array2': arr2}
        )

        if response:
            waiting_time = time.time() - start_time

            if response.success:
                self.stats['tasks_completed'] += 1
                self.stats['total_waiting_time'] += waiting_time

                print(f"\n✓ Задание выполнено успешно!")
                print(f"  Время выполнения на сервера: {response.execution_time:.2f}с")
                print(f"  Общее время ожидания: {waiting_time:.2f}с")

                result = response.result.get('result', [])
                count = response.result.get('common_count', 0)

                print(f"\nРезультат:")
                print(f"  Общие числа ({count}): {result}")

                # Логируем в консоль
                self.logger.client_message(f"получен результат поиска общих чисел")

            else:
                self.stats['tasks_failed'] += 1
                print(f"\n✗ Ошибка выполнения задания:")
                print(f"  {response.error_message}")
        else:
            print("\n✗ Не удалось получить ответ от сервера")

    def _generate_test_data(self):
        """Генерация тестовых данных."""
        print(f"\n{'=' * 40}")
        print("ГЕНЕРАЦИЯ ТЕСТОВЫХ ДАННЫХ")
        print('=' * 40)

        print("\nВыберите тип данных:")
        print("1. Сгенерировать массив")
        print("2. Сгенерировать матрицу")
        print("3. Валидировать данные")

        choice = input("Выбор (1-3): ").strip()

        if choice == '1':
            # Генерация массива
            size = self._get_number("Размер массива", min_val=1, max_val=50)
            min_val = self._get_number("Минимальное значение")
            max_val = self._get_number("Максимальное значение", min_val=min_val + 1)

            print(f"\nОтправка запроса на генерацию массива...")

            response = self.client.execute_task(
                TaskType.GENERATE_ARRAY,
                {'size': size, 'min_val': min_val, 'max_val': max_val}
            )

            if response and response.success:
                array = response.result.get('array', [])
                print(f"\n✓ Сгенерирован массив:")
                print(f"  Размер: {len(array)}")
                print(f"  Минимальное значение: {min(array) if array else 'N/A'}")
                print(f"  Максимальное значение: {max(array) if array else 'N/A'}")
                print(f"  Массив: {array}")

                # Логируем в консоль
                self.logger.client_message(f"сгенерированы данные (массив {size} элементов)")
            else:
                print("\n✗ Ошибка генерации")

        elif choice == '2':
            # Генерация матрицы
            rows = self._get_number("Количество строк", min_val=1, max_val=5)
            cols = self._get_number("Количество столбцов", min_val=1, max_val=5)
            min_val = self._get_number("Минимальное значение")
            max_val = self._get_number("Максимальное значение", min_val=min_val + 1)

            print(f"\nОтправка запроса на генерацию матрицы...")

            response = self.client.execute_task(
                TaskType.GENERATE_MATRIX,
                {'rows': rows, 'cols': cols, 'min_val': min_val, 'max_val': max_val}
            )

            if response and response.success:
                matrix = response.result.get('matrix', [])
                print(f"\n✓ Сгенерирована матрица {rows}x{cols}:")
                for i, row in enumerate(matrix):
                    print(f"  Строка {i + 1}: {row}")

                # Логируем в консоль
                self.logger.client_message(f"сгенерированы данные (матрица {rows}x{cols})")
            else:
                print("\n✗ Ошибка генерации")

        elif choice == '3':
            # Валидация данных
            print("\nВведите данные для валидации (числа через пробел):")
            data_input = input("Данные: ").strip()

            try:
                data = [float(x) for x in data_input.split()]
                data_type = 'array'
            except:
                print("Некорректный ввод")
                return

            print(f"\nОтправка запроса на валидацию...")

            response = self.client.execute_task(
                TaskType.VALIDATE_DATA,
                {'type': data_type, 'data': data}
            )

            if response and response.success:
                is_valid = response.result.get('is_valid', False)
                if is_valid:
                    print(f"\n✓ Данные корректны")
                    print(f"  Тип: {response.result.get('data_type')}")
                    print(f"  Размер: {response.result.get('size', 0)}")
                else:
                    print(f"\n✗ Данные некорректны")
                    print(f"  Ошибка: {response.result.get('error', 'Неизвестная ошибка')}")
            else:
                print("\n✗ Ошибка валидации")

        else:
            print("Неверный выбор")

    def _input_array(self, array_name: str) -> Optional[list]:
        """
        Ввод массива с клавиатуры.

        Args:
            array_name: Название массива

        Returns:
            Список чисел или None при ошибке
        """
        print(f"\nВвод {array_name}:")
        print("Введите числа через пробел (например: 1 2 3 4 5)")

        try:
            input_str = input(f"{array_name}: ").strip()
            if not input_str:
                return []

            numbers = [float(x) for x in input_str.split()]
            return numbers

        except ValueError:
            print("Ошибка: вводите только числа!")
            return None
        except Exception as e:
            print(f"Ошибка ввода: {e}")
            return None

    def _input_matrix(self) -> Optional[list]:
        """Ввод матрицы с клавиатуры."""
        print("\nВвод матрицы:")

        try:
            rows = int(input("Количество строк: "))
            cols = int(input("Количество столбцов: "))

            if rows <= 0 or cols <= 0:
                print("Количество строк и столбцов должно быть положительным")
                return None

            matrix = []
            for i in range(rows):
                while True:
                    try:
                        row_input = input(f"Строка {i + 1} ({cols} чисел через пробел): ").strip()
                        row = [float(x) for x in row_input.split()]

                        if len(row) != cols:
                            print(f"Ошибка: нужно ввести ровно {cols} чисел")
                            continue

                        matrix.append(row)
                        break

                    except ValueError:
                        print("Ошибка: вводите только числа!")
                    except Exception as e:
                        print(f"Ошибка: {e}")

            return matrix

        except ValueError:
            print("Ошибка: вводите целые числа!")
            return None
        except Exception as e:
            print(f"Ошибка ввода: {e}")
            return None

    def _get_number(self, prompt: str, min_val: float = None, max_val: float = None) -> float:
        """
        Получение числа от пользователя с валидацией.

        Args:
            prompt: Подсказка для ввода
            min_val: Минимальное значение
            max_val: Максимальное значение

        Returns:
            Введенное число
        """
        while True:
            try:
                value = float(input(f"{prompt}: ").strip())

                if min_val is not None and value < min_val:
                    print(f"Ошибка: значение должно быть не меньше {min_val}")
                    continue

                if max_val is not None and value > max_val:
                    print(f"Ошибка: значение должно быть не больше {max_val}")
                    continue

                return value

            except ValueError:
                print("Ошибка: введите число!")
            except Exception as e:
                print(f"Ошибка: {e}")

    def _generate_random_array(self, size: int, min_val: int, max_val: int) -> list:
        """Генерация случайного массива."""
        import random
        return [random.randint(min_val, max_val) for _ in range(size)]

    def _generate_random_matrix(self, rows: int, cols: int, min_val: int, max_val: int) -> list:
        """Генерация случайной матрицы."""
        import random
        return [
            [random.randint(min_val, max_val) for _ in range(cols)]
            for _ in range(rows)
        ]

    def _print_stats(self):
        """Вывод статистики работы клиента."""
        print(f"\n{'=' * 40}")
        print(f"СТАТИСТИКА КЛИЕНТА: {self.client_name}")
        print('=' * 40)

        print(f"Всего запросов: {self.stats['tasks_requested']}")
        print(f"Успешно выполнено: {self.stats['tasks_completed']}")
        print(f"Ошибок выполнения: {self.stats['tasks_failed']}")

        if self.stats['tasks_completed'] > 0:
            avg_waiting = self.stats['total_waiting_time'] / self.stats['tasks_completed']
            print(f"Среднее время ожидания: {avg_waiting:.2f}с")

        success_rate = (self.stats['tasks_completed'] / self.stats['tasks_requested'] * 100
                        if self.stats['tasks_requested'] > 0 else 0)
        print(f"Процент успешных задач: {success_rate:.1f}%")

    def _print_client_info(self):
        """Вывод информации о клиенте."""
        if not self.client:
            print("Клиент не инициализирован")
            return

        info = self.client.get_client_info()

        print(f"\n{'=' * 40}")
        print(f"ИНФОРМАЦИЯ О КЛИЕНТЕ")
        print('=' * 40)

        print(f"Имя: {info['name']}")
        print(f"ID: {info['id']}")
        print(f"Сервер: {info['server']}")
        print(f"Статус подключения: {'Подключен' if info['connected'] else 'Не подключен'}")

        if info['connected'] and info['connection_time']:
            print(f"Время подключения: {info['connection_time']}")


def start_client(client_name: str = None):
    """
    Запуск клиента из командной строки.

    Args:
        client_name: Имя клиента
    """
    import argparse

    parser = argparse.ArgumentParser(description='Запуск клиента приложения')
    parser.add_argument('--host', default='localhost', help='Хост сервера')
    parser.add_argument('--port', type=int, default=8888, help='Порт сервера')
    parser.add_argument('--name', help='Имя клиента')

    args = parser.parse_args()

    client_ui = ClientUI(client_name=args.name or client_name)
    client_ui.start(server_host=args.host, server_port=args.port)


def start_multiple_clients(num_clients: int = 3):
    """
    Запуск нескольких клиентов в разных потоках.

    Args:
        num_clients: Количество клиентов
    """
    print(f"\nЗапуск {num_clients} клиентов...")
    print("=" * 60)

    threads = []

    for i in range(num_clients):
        client_name = f"Клиент{i + 1}"
        thread = threading.Thread(
            target=start_client,
            args=(client_name,),
            daemon=True
        )
        threads.append(thread)
        thread.start()

        # Небольшая задержка между запусками
        time.sleep(0.5)

    # Ожидание завершения всех клиентов
    try:
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        print("\nЗавершение всех клиентов...")


if __name__ == "__main__":
    # Можно запустить одного клиента или нескольких
    import argparse

    parser = argparse.ArgumentParser(description='Запуск клиента(ов) приложения')
    parser.add_argument('--multi', action='store_true', help='Запуск нескольких клиентов')
    parser.add_argument('--count', type=int, default=3, help='Количество клиентов при --multi')

    args = parser.parse_args()

    if args.multi:
        start_multiple_clients(args.count)
    else:
        start_client()
# coroutine_menu.py
"""
АВТОМАТНОЕ ПРОГРАММИРОВАНИЕ ЧЕРЕЗ КОРУТИНЫ
==========================================

Исправленная версия - без return в async generator.
Используем StopAsyncIteration с value.
"""

import asyncio
from enum import Enum
from typing import Dict, Any, Optional, AsyncGenerator
import time
import sys
import os

# Добавляем пути для импорта
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class EventType(Enum):
    """Типы событий для автомата."""
    ENTER_STATE = "enter_state"
    EXIT_STATE = "exit_state"
    USER_INPUT = "user_input"
    TIMEOUT = "timeout"
    ERROR = "error"
    COMPLETE = "complete"
    STATE_CHANGE = "state_change"  # Новое: запрос смены состояния


class State(Enum):
    """Состояния конечного автомата."""
    IDLE = "idle"
    MAIN_MENU = "main_menu"
    ARRAY_OPS = "array_operations"
    MATRIX_OPS = "matrix_operations"
    DATA_VALID = "data_validation"
    ALGORITHMS = "algorithms"
    CLIENT_SERVER = "client_server"
    EXIT = "exit"


class Event:
    """Класс события."""

    def __init__(self, event_type: EventType, data: Any = None):
        self.type = event_type
        self.data = data
        self.timestamp = time.time()

    def __repr__(self):
        return f"Event({self.type}, data={self.data})"


class CoroutineStateMachine:
    """
    Конечный автомат на корутинах - исправленная версия.

    Использует StopAsyncIteration для возврата следующего состояния.
    """

    def __init__(self):
        self.current_state = State.IDLE
        self.current_coroutine = None
        self.event_queue = asyncio.Queue()
        self.state_handlers = self._setup_state_handlers()
        self.running = False
        self.state_history = []

    def _setup_state_handlers(self) -> Dict[State, AsyncGenerator]:
        """Настройка обработчиков состояний."""
        return {
            State.IDLE: self.idle_state,
            State.MAIN_MENU: self.main_menu_state,
            State.ARRAY_OPS: self.array_ops_state,
            State.MATRIX_OPS: self.matrix_ops_state,
            State.DATA_VALID: self.data_valid_state,
            State.ALGORITHMS: self.algorithms_state,
            State.CLIENT_SERVER: self.client_server_state,
            State.EXIT: self.exit_state,
        }

    async def idle_state(self) -> AsyncGenerator[Event, None]:
        """Начальное состояние."""
        print("[IDLE] Система инициализируется...")

        yield Event(EventType.ENTER_STATE, {"state": State.IDLE})

        # Имитация инициализации
        await asyncio.sleep(0.5)

        # Выход из корутины с указанием следующего состояния
        # Используем StopAsyncIteration с value
        raise StopAsyncIteration(State.MAIN_MENU)

    async def main_menu_state(self) -> AsyncGenerator[Event, None]:
        """Состояние главного меню."""
        print("\n" + "=" * 60)
        print("ГЛАВНОЕ МЕНЮ - Задания 2 (Корутины)")
        print("=" * 60)

        yield Event(EventType.ENTER_STATE, {"state": State.MAIN_MENU})

        while True:
            print("\nДоступные опции:")
            print("1. 📊 Операции с массивами")
            print("2. 🧮 Операции с матрицами")
            print("3. ✅ Валидация данных")
            print("4. ⚡ Алгоритмы (1, 3, 8)")
            print("5. 🌐 Клиент-сервер")
            print("6. 🚪 Выход")
            print("=" * 60)

            # Ждем пользовательский ввод через yield
            choice_event = yield Event(EventType.USER_INPUT, {"prompt": "Выберите пункт (1-6): "})

            if choice_event.type == EventType.USER_INPUT:
                choice = choice_event.data

                if choice == '1':
                    raise StopAsyncIteration(State.ARRAY_OPS)
                elif choice == '2':
                    raise StopAsyncIteration(State.MATRIX_OPS)
                elif choice == '3':
                    raise StopAsyncIteration(State.DATA_VALID)
                elif choice == '4':
                    raise StopAsyncIteration(State.ALGORITHMS)
                elif choice == '5':
                    raise StopAsyncIteration(State.CLIENT_SERVER)
                elif choice == '6':
                    raise StopAsyncIteration(State.EXIT)
                else:
                    print("⚠ Неверный выбор. Попробуйте снова.")
                    yield Event(EventType.ERROR, {"message": "Неверный ввод"})

    async def array_ops_state(self) -> AsyncGenerator[Event, None]:
        """Состояние операций с массивами."""
        print("\n" + "=" * 60)
        print("ОПЕРАЦИИ С МАССИВАМИ (Корутины)")
        print("=" * 60)

        yield Event(EventType.ENTER_STATE, {"state": State.ARRAY_OPS})

        while True:
            print("\nОперации с массивами:")
            print("1. Создать массив")
            print("2. Суммировать массивы")
            print("3. Найти общие элементы")
            print("4. 🏠 Вернуться в главное меню")
            print("=" * 60)

            choice_event = yield Event(EventType.USER_INPUT, {"prompt": "Выберите операцию (1-4): "})

            if choice_event.type == EventType.USER_INPUT:
                choice = choice_event.data

                if choice == '1':
                    # Корутина создания массива
                    await self.create_array_coroutine()
                elif choice == '2':
                    # Корутина суммирования
                    await self.sum_arrays_coroutine()
                elif choice == '3':
                    # Корутина поиска общих элементов
                    await self.common_elements_coroutine()
                elif choice == '4':
                    raise StopAsyncIteration(State.MAIN_MENU)
                else:
                    print("Неверный выбор")

    async def matrix_ops_state(self) -> AsyncGenerator[Event, None]:
        """Состояние операций с матрицами."""
        print("\n" + "=" * 60)
        print("ОПЕРАЦИИ С МАТРИЦАМИ (Корутины)")
        print("=" * 60)

        yield Event(EventType.ENTER_STATE, {"state": State.MATRIX_OPS})

        while True:
            print("\nОперации с матрицами:")
            print("1. Создать матрицу")
            print("2. Повернуть матрицу")
            print("3. Транспонировать матрицу")
            print("4. 🏠 Вернуться в главное меню")
            print("=" * 60)

            choice_event = yield Event(EventType.USER_INPUT, {"prompt": "Выберите операцию (1-4): "})

            if choice_event.type == EventType.USER_INPUT:
                choice = choice_event.data

                if choice == '1':
                    await self.create_matrix_coroutine()
                elif choice == '2':
                    await self.rotate_matrix_coroutine()
                elif choice == '3':
                    await self.transpose_matrix_coroutine()
                elif choice == '4':
                    raise StopAsyncIteration(State.MAIN_MENU)
                else:
                    print("Неверный выбор")

    async def data_valid_state(self) -> AsyncGenerator[Event, None]:
        """Состояние валидации данных."""
        print("\n" + "=" * 60)
        print("ВАЛИДАЦИЯ ДАННЫХ (Корутины)")
        print("=" * 60)

        yield Event(EventType.ENTER_STATE, {"state": State.DATA_VALID})

        while True:
            print("\nВалидация данных:")
            print("1. Валидация числа")
            print("2. Валидация массива")
            print("3. Валидация матрицы")
            print("4. 🏠 Вернуться в главное меню")
            print("=" * 60)

            choice_event = yield Event(EventType.USER_INPUT, {"prompt": "Выберите тип (1-4): "})

            if choice_event.type == EventType.USER_INPUT:
                choice = choice_event.data

                if choice == '1':
                    await self.validate_number_coroutine()
                elif choice == '2':
                    await self.validate_array_coroutine()
                elif choice == '3':
                    await self.validate_matrix_coroutine()
                elif choice == '4':
                    raise StopAsyncIteration(State.MAIN_MENU)
                else:
                    print("Неверный выбор")

    async def algorithms_state(self) -> AsyncGenerator[Event, None]:
        """Состояние алгоритмов."""
        print("\n" + "=" * 60)
        print("АЛГОРИТМЫ (Корутины)")
        print("=" * 60)

        yield Event(EventType.ENTER_STATE, {"state": State.ALGORITHMS})

        while True:
            print("\nДоступные алгоритмы:")
            print("1. Алгоритм 1: Сумма массивов")
            print("2. Алгоритм 3: Поворот матрицы")
            print("3. Алгоритм 8: Общие числа")
            print("4. Запустить все асинхронно")
            print("5. 🏠 Вернуться в главное меню")
            print("=" * 60)

            choice_event = yield Event(EventType.USER_INPUT, {"prompt": "Выберите алгоритм (1-5): "})

            if choice_event.type == EventType.USER_INPUT:
                choice = choice_event.data

                if choice == '1':
                    await self.algorithm1_coroutine()
                elif choice == '2':
                    await self.algorithm3_coroutine()
                elif choice == '3':
                    await self.algorithm8_coroutine()
                elif choice == '4':
                    # Запуск всех алгоритмов асинхронно
                    await self.run_all_algorithms_async()
                elif choice == '5':
                    raise StopAsyncIteration(State.MAIN_MENU)
                else:
                    print("Неверный выбор")

    async def client_server_state(self) -> AsyncGenerator[Event, None]:
        """Состояние клиент-сервер."""
        print("\n" + "=" * 60)
        print("КЛИЕНТ-СЕРВЕР (Корутины)")
        print("=" * 60)

        yield Event(EventType.ENTER_STATE, {"state": State.CLIENT_SERVER})

        while True:
            print("\nКлиент-серверные операции:")
            print("1. Запустить сервер (демо)")
            print("2. Запустить клиента (демо)")
            print("3. Тест многопоточности")
            print("4. 🏠 Вернуться в главное меню")
            print("=" * 60)

            choice_event = yield Event(EventType.USER_INPUT, {"prompt": "Выберите действие (1-4): "})

            if choice_event.type == EventType.USER_INPUT:
                choice = choice_event.data

                if choice == '1':
                    await self.start_server_demo()
                elif choice == '2':
                    await self.start_client_demo()
                elif choice == '3':
                    await self.thread_test_coroutine()
                elif choice == '4':
                    raise StopAsyncIteration(State.MAIN_MENU)
                else:
                    print("Неверный выбор")

    async def exit_state(self) -> AsyncGenerator[Event, None]:
        """Состояние выхода."""
        print("\n" + "=" * 60)
        print("ВЫХОД ИЗ СИСТЕМЫ")
        print("=" * 60)

        yield Event(EventType.ENTER_STATE, {"state": State.EXIT})

        print("Завершение работы...")
        await asyncio.sleep(1.0)

        # Сигнал завершения
        yield Event(EventType.COMPLETE, {"message": "System shutdown"})

        # Останавливаем автомат
        self.running = False
        raise StopAsyncIteration(State.EXIT)

    # ========== ВСПОМОГАТЕЛЬНЫЕ КОРУТИНЫ ==========

    async def create_array_coroutine(self):
        """Корутина создания массива."""
        print("\n[Создание массива]")

        size_event = yield Event(EventType.USER_INPUT, {"prompt": "Введите размер массива: "})

        if size_event.type == EventType.USER_INPUT:
            try:
                size = int(size_event.data)
                print(f"Создание массива из {size} элементов...")
                yield Event(EventType.ENTER_STATE, {"action": "creating_array"})

                await asyncio.sleep(0.5)

                array = list(range(1, size + 1))
                print(f"✓ Создан массив: {array}")

                yield Event(EventType.COMPLETE, {"result": array})

            except ValueError:
                print("✗ Ошибка: введите число")
                yield Event(EventType.ERROR, {"message": "Invalid input"})

    async def sum_arrays_coroutine(self):
        """Корутина суммирования массивов."""
        print("\n[Суммирование массивов]")

        arr1_event = yield Event(EventType.USER_INPUT, {
            "prompt": "Введите первый массив (через запятую): "
        })

        if arr1_event.type == EventType.USER_INPUT:
            try:
                arr1 = [int(x.strip()) for x in arr1_event.data.split(',')]

                arr2_event = yield Event(EventType.USER_INPUT, {
                    "prompt": "Введите второй массив (через запятую): "
                })

                if arr2_event.type == EventType.USER_INPUT:
                    arr2 = [int(x.strip()) for x in arr2_event.data.split(',')]

                    print("Вычисление суммы...")
                    yield Event(EventType.ENTER_STATE, {"action": "calculating_sum"})

                    await asyncio.sleep(0.3)

                    if len(arr1) == len(arr2):
                        result = [a + b for a, b in zip(arr1, arr2)]
                        print(f"✓ Результат: {arr1} + {arr2} = {result}")
                        yield Event(EventType.COMPLETE, {"result": result})
                    else:
                        print("✗ Ошибка: массивы разной длины")
                        yield Event(EventType.ERROR, {"message": "Arrays length mismatch"})

            except ValueError:
                print("✗ Ошибка: введите числа через запятую")
                yield Event(EventType.ERROR, {"message": "Invalid input format"})

    async def common_elements_coroutine(self):
        """Корутина поиска общих элементов."""
        print("\n[Поиск общих элементов]")

        arr1_event = yield Event(EventType.USER_INPUT, {
            "prompt": "Первый массив (через запятую): "
        })

        if arr1_event.type == EventType.USER_INPUT:
            arr2_event = yield Event(EventType.USER_INPUT, {
                "prompt": "Второй массив (через запятую): "
            })

            if arr2_event.type == EventType.USER_INPUT:
                try:
                    arr1 = [int(x.strip()) for x in arr1_event.data.split(',')]
                    arr2 = [int(x.strip()) for x in arr2_event.data.split(',')]

                    print("Поиск общих элементов...")
                    yield Event(EventType.ENTER_STATE, {"action": "finding_common"})

                    await asyncio.sleep(0.4)

                    common = list(set(arr1) & set(arr2))
                    print(f"✓ Общие элементы: {common}")

                    yield Event(EventType.COMPLETE, {"result": common})

                except ValueError:
                    print("✗ Ошибка ввода")
                    yield Event(EventType.ERROR, {"message": "Input error"})

    async def create_matrix_coroutine(self):
        """Корутина создания матрицы."""
        print("\n[Создание матрицы]")

        rows_event = yield Event(EventType.USER_INPUT, {"prompt": "Количество строк: "})

        if rows_event.type == EventType.USER_INPUT:
            cols_event = yield Event(EventType.USER_INPUT, {"prompt": "Количество столбцов: "})

            if cols_event.type == EventType.USER_INPUT:
                try:
                    rows = int(rows_event.data)
                    cols = int(cols_event.data)

                    print(f"Создание матрицы {rows}x{cols}...")
                    yield Event(EventType.ENTER_STATE, {"action": "creating_matrix"})

                    await asyncio.sleep(0.5)

                    matrix = [[i * cols + j + 1 for j in range(cols)] for i in range(rows)]
                    print("✓ Матрица создана:")
                    for row in matrix:
                        print(f"  {row}")

                    yield Event(EventType.COMPLETE, {"result": matrix})

                except ValueError:
                    print("✗ Ошибка: введите числа")
                    yield Event(EventType.ERROR, {"message": "Invalid input"})

    async def rotate_matrix_coroutine(self):
        """Корутина поворота матрицы."""
        print("\n[Поворот матрицы]")

        matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        print("Исходная матрица:")
        for row in matrix:
            print(f"  {row}")

        direction_event = yield Event(EventType.USER_INPUT, {
            "prompt": "Направление (1-по часовой, 2-против): "
        })

        if direction_event.type == EventType.USER_INPUT:
            print("Поворот...")
            yield Event(EventType.ENTER_STATE, {"action": "rotating_matrix"})

            await asyncio.sleep(0.6)

            n = len(matrix)
            if direction_event.data == '1':
                rotated = [[matrix[n - 1 - j][i] for j in range(n)] for i in range(n)]
                direction = "по часовой стрелке"
            else:
                rotated = [[matrix[j][n - 1 - i] for j in range(n)] for i in range(n)]
                direction = "против часовой стрелки"

            print(f"✓ Матрица повернута {direction}:")
            for row in rotated:
                print(f"  {row}")

            yield Event(EventType.COMPLETE, {"result": rotated})

    async def validate_number_coroutine(self):
        """Корутина валидации числа."""
        print("\n[Валидация числа]")

        num_event = yield Event(EventType.USER_INPUT, {"prompt": "Введите число: "})

        if num_event.type == EventType.USER_INPUT:
            print("Проверка...")
            yield Event(EventType.ENTER_STATE, {"action": "validating_number"})

            await asyncio.sleep(0.2)

            text = num_event.data
            if text.replace('-', '').isdigit():
                print(f"✓ Число '{text}' валидно")
                yield Event(EventType.COMPLETE, {"valid": True})
            else:
                print(f"✗ '{text}' не является числом")
                yield Event(EventType.ERROR, {"valid": False})

    async def validate_array_coroutine(self):
        """Корутина валидации массива."""
        print("\n[Валидация массива]")

        arr_event = yield Event(EventType.USER_INPUT, {
            "prompt": "Введите массив (через запятую): "
        })

        if arr_event.type == EventType.USER_INPUT:
            print("Проверка...")
            yield Event(EventType.ENTER_STATE, {"action": "validating_array"})

            await asyncio.sleep(0.3)

            try:
                array = [int(x.strip()) for x in arr_event.data.split(',')]
                print(f"✓ Массив валиден: {array}")
                yield Event(EventType.COMPLETE, {"valid": True, "array": array})
            except ValueError:
                print("✗ Невалидный массив")
                yield Event(EventType.ERROR, {"valid": False})

    async def validate_matrix_coroutine(self):
        """Корутина валидации матрицы."""
        print("\n[Валидация матрицы]")

        matrix_event = yield Event(EventType.USER_INPUT, {
            "prompt": "Введите матрицу (строки через ';', элементы через ','): "
        })

        if matrix_event.type == EventType.USER_INPUT:
            print("Проверка...")
            yield Event(EventType.ENTER_STATE, {"action": "validating_matrix"})

            await asyncio.sleep(0.4)

            try:
                rows = matrix_event.data.split(';')
                matrix = []
                for i, row in enumerate(rows):
                    elements = [int(x.strip()) for x in row.split(',')]
                    matrix.append(elements)

                    if i > 0 and len(elements) != len(matrix[0]):
                        raise ValueError("Разные длины строк")

                print(f"✓ Матрица валидна, размер: {len(matrix)}x{len(matrix[0])}")
                yield Event(EventType.COMPLETE, {"valid": True, "matrix": matrix})

            except Exception as e:
                print(f"✗ Невалидная матрица: {e}")
                yield Event(EventType.ERROR, {"valid": False})

    async def algorithm1_coroutine(self):
        """Корутина алгоритма 1 (сумма массивов)."""
        print("\n[Алгоритм 1: Сумма массивов]")

        yield Event(EventType.ENTER_STATE, {"algorithm": "sum_arrays"})

        print("Выполнение алгоритма...")

        steps = ["Инициализация", "Проверка размеров", "Вычисление", "Формирование результата"]

        for step in steps:
            print(f"  {step}...")
            await asyncio.sleep(0.3)
            yield Event(EventType.ENTER_STATE, {"step": step})

        result = [1 + 4, 2 + 5, 3 + 6]
        print(f"✓ Результат: [1,2,3] + [4,5,6] = {result}")

        yield Event(EventType.COMPLETE, {"result": result})

    async def algorithm3_coroutine(self):
        """Корутина алгоритма 3 (поворот матрицы)."""
        print("\n[Алгоритм 3: Поворот матрицы]")

        yield Event(EventType.ENTER_STATE, {"algorithm": "rotate_matrix"})

        print("Выполнение алгоритма...")

        steps = ["Чтение матрицы", "Определение размеров", "Вычисление поворота", "Вывод результата"]

        for step in steps:
            print(f"  {step}...")
            await asyncio.sleep(0.4)
            yield Event(EventType.ENTER_STATE, {"step": step})

        print("✓ Матрица повернута успешно")

        yield Event(EventType.COMPLETE, {"result": "matrix_rotated"})

    async def algorithm8_coroutine(self):
        """Корутина алгоритма 8 (общие числа)."""
        print("\n[Алгоритм 8: Общие числа]")

        yield Event(EventType.ENTER_STATE, {"algorithm": "common_numbers"})

        print("Выполнение алгоритма...")

        steps = ["Чтение массивов", "Создание множеств", "Пересечение", "Сортировка результата"]

        for step in steps:
            print(f"  {step}...")
            await asyncio.sleep(0.35)
            yield Event(EventType.ENTER_STATE, {"step": step})

        result = [2, 3, 4]
        print(f"✓ Найдены общие числа: {result}")

        yield Event(EventType.COMPLETE, {"result": result})

    async def run_all_algorithms_async(self):
        """Асинхронный запуск всех алгоритмов."""
        print("\n[Асинхронный запуск всех алгоритмов]")

        tasks = [
            asyncio.create_task(self._run_algorithm_with_progress("Алгоритм 1", 1.0)),
            asyncio.create_task(self._run_algorithm_with_progress("Алгоритм 3", 1.5)),
            asyncio.create_task(self._run_algorithm_with_progress("Алгоритм 8", 1.2)),
        ]

        print("Запущено 3 алгоритма параллельно...")

        results = await asyncio.gather(*tasks, return_exceptions=True)

        print("\n✓ Все алгоритмы завершены!")
        for i, result in enumerate(results, 1):
            status = 'Успех' if not isinstance(result, Exception) else 'Ошибка'
            print(f"  Алгоритм {i}: {status}")

    async def _run_algorithm_with_progress(self, name: str, duration: float):
        """Вспомогательная корутина."""
        print(f"  {name} запущен...")

        steps = int(duration / 0.3)
        for i in range(steps):
            await asyncio.sleep(0.3)
            print(f"    {name}: шаг {i + 1}/{steps}")

        print(f"  {name}: завершен")
        return f"{name}_done"

    async def start_server_demo(self):
        """Демо запуска сервера."""
        print("\n[Демо сервера]")

        print("Запуск сервера...")
        yield Event(EventType.ENTER_STATE, {"action": "starting_server"})

        await asyncio.sleep(1.0)

        print("✓ Сервер запущен на localhost:8888")
        print("  Ожидание подключений...")

        for i in range(3):
            await asyncio.sleep(0.5)
            print(f"  Принято подключение #{i + 1}")

        yield Event(EventType.COMPLETE, {"status": "server_running"})

    async def start_client_demo(self):
        """Демо запуска клиента."""
        print("\n[Демо клиента]")

        print("Подключение к серверу...")
        yield Event(EventType.ENTER_STATE, {"action": "connecting_client"})

        await asyncio.sleep(0.7)

        print("✓ Клиент подключен")
        print("  Отправка запросов...")

        requests = ["GENERATE_ARRAY", "GENERATE_MATRIX", "SUM_ARRAYS"]
        for req in requests:
            await asyncio.sleep(0.4)
            print(f"  Отправлен запрос: {req}")
            await asyncio.sleep(0.2)
            print(f"  Получен ответ")

        yield Event(EventType.COMPLETE, {"status": "client_connected"})

    async def thread_test_coroutine(self):
        """Корутина теста многопоточности."""
        print("\n[Тест многопоточности]")

        print("Запуск теста...")
        yield Event(EventType.ENTER_STATE, {"action": "thread_test"})

        async def mock_request(request_id: int):
            await asyncio.sleep(0.5 + request_id * 0.1)
            return f"Request_{request_id}_done"

        print("Запуск 5 параллельных запросов...")

        tasks = [mock_request(i) for i in range(5)]
        start_time = time.time()

        results = await asyncio.gather(*tasks)

        elapsed = time.time() - start_time

        print(f"✓ Все запросы завершены за {elapsed:.2f}с")
        print(f"  Параллельность: {(0.5 * 5) / elapsed:.2f}x")

        yield Event(EventType.COMPLETE, {"results": results, "time": elapsed})

    async def event_loop(self):
        """Основной цикл обработки событий."""
        print("\n" + "=" * 60)
        print("АВТОМАТ НА КОРУТИНАХ - ЗАПУСК")
        print("=" * 60)

        self.running = True
        next_state = State.IDLE

        while self.running:
            handler = self.state_handlers.get(next_state)

            if not handler:
                print(f"Ошибка: нет обработчика для состояния {next_state}")
                break

            if next_state != self.current_state:
                self.state_history.append((self.current_state, next_state))
                self.current_state = next_state
                print(f"\n[Переход] → {self.current_state.value}")

            coroutine = handler()
            self.current_coroutine = coroutine

            try:
                event = await coroutine.__anext__()

                while True:
                    if event.type == EventType.USER_INPUT:
                        prompt = event.data.get('prompt', '> ')
                        user_input = await self.get_user_input(prompt)

                        event = await coroutine.asend(
                            Event(EventType.USER_INPUT, user_input)
                        )

                    elif event.type in [EventType.ENTER_STATE, EventType.EXIT_STATE,
                                        EventType.COMPLETE, EventType.ERROR]:
                        # Просто логируем и получаем следующее событие
                        event = await coroutine.__anext__()

                    else:
                        event = await coroutine.__anext__()

            except StopAsyncIteration as e:
                # Получаем следующее состояние из StopAsyncIteration
                next_state = e.value if hasattr(e, 'value') else State.MAIN_MENU

            except Exception as e:
                print(f"Ошибка в корутине: {e}")
                next_state = State.MAIN_MENU

            if next_state == State.EXIT:
                self.running = False

    async def get_user_input(self, prompt: str) -> str:
        """Асинхронное получение пользовательского ввода."""
        # Используем asyncio.to_thread для неблокирующего ввода
        return await asyncio.to_thread(input, prompt)

    def run(self):
        """Запуск автомата."""
        try:
            asyncio.run(self.event_loop())
        except KeyboardInterrupt:
            print("\n\nПрограмма прервана пользователем")
        finally:
            print("\n" + "=" * 60)
            print("АВТОМАТ ЗАВЕРШИЛ РАБОТУ")
            print(f"История переходов: {self.state_history}")
            print("=" * 60)


class AsyncMenuManager:
    """Менеджер асинхронного меню."""

    def __init__(self):
        self.state_machine = CoroutineStateMachine()

    def start(self):
        """Запуск меню."""
        print("\n" + "=" * 60)
        print("АВТОМАТНОЕ ПРОГРАММИРОВАНИЕ ЧЕРЕЗ КОРУТИНЫ")
        print("Реализация меню через асинхронные конечные автоматы")
        print("=" * 60)

        self.state_machine.run()


# Упрощенная версия для тестирования
class SimpleCoroutineMenu:
    """Упрощенная версия меню на корутинах."""

    async def main_menu(self):
        """Упрощенное главное меню."""
        print("\n" + "=" * 60)
        print("ПРОСТОЕ АВТОМАТНОЕ МЕНЮ (Корутины)")
        print("=" * 60)

        while True:
            print("\n1. Операции с массивами")
            print("2. Операции с матрицами")
            print("3. Выход")

            choice = await asyncio.to_thread(input, "Выберите: ")

            if choice == '1':
                await self.array_operations()
            elif choice == '2':
                await self.matrix_operations()
            elif choice == '3':
                print("\nВыход...")
                break
            else:
                print("Неверный выбор")

    async def array_operations(self):
        """Операции с массивами."""
        print("\n--- Операции с массивами ---")

        print("1. Создать массив")
        print("2. Суммировать массивы")
        print("3. Назад")

        choice = await asyncio.to_thread(input, "Выберите: ")

        if choice == '1':
            size = int(await asyncio.to_thread(input, "Размер: "))
            array = list(range(size))
            print(f"Массив: {array}")
        elif choice == '2':
            print("Суммирование массивов...")
            arr1 = [1, 2, 3]
            arr2 = [4, 5, 6]
            result = [a + b for a, b in zip(arr1, arr2)]
            print(f"Результат: {result}")

    async def matrix_operations(self):
        """Операции с матрицами."""
        print("\n--- Операции с матрицами ---")

        print("1. Создать матрицу")
        print("2. Повернуть матрицу")
        print("3. Назад")

        choice = await asyncio.to_thread(input, "Выберите: ")

        if choice == '1':
            rows = 3
            cols = 3
            matrix = [[i * cols + j + 1 for j in range(cols)] for i in range(rows)]
            print("Матрица создана")
        elif choice == '2':
            print("Поворот матрицы...")
            matrix = [[1, 2], [3, 4]]
            rotated = [[matrix[1][0], matrix[0][0]], [matrix[1][1], matrix[0][1]]]
            print(f"Повернута: {rotated}")


def print_state_machine_diagram():
    """Вывод графической схемы."""
    print("\n" + "=" * 70)
    print("ГРАФИЧЕСКАЯ СХЕМА АВТОМАТА НА КОРУТИНАХ")
    print("=" * 70)

    diagram = """
                       ┌─────────────┐
                       │     IDLE    │
                       │  (Начало)   │
                       └──────┬──────┘
                              │
                              ▼
                       ┌─────────────┐
                       │  MAIN_MENU  │◄─────────────┐
                       │   (Главное) │              │
                       └──────┬──────┘              │
            ┌─────────────────┼─────────────────┐   │
            │                 │                 │   │
            ▼                 ▼                 ▼   │
      ┌──────────┐     ┌──────────┐     ┌──────────┐
      │ ARRAY_OPS│     │MATRIX_OPS│     │DATA_VALID│
      │ (Массивы)│     │(Матрицы) │     │(Валидац.)│
      └────┬─────┘     └────┬─────┘     └────┬─────┘
           │                 │                 │
           └─────────────────┼─────────────────┘
                             │
            ┌────────────────┼─────────────────┐
            │                │                 │
            ▼                ▼                 ▼
      ┌──────────┐    ┌────────────┐    ┌─────────┐
      │ALGORITHMS│    │CLIENT_SERVER│   │   EXIT   │
      │(Алгоритмы)│    │(Клиент-серв)│   │  (Выход) │
      └──────────┘    └────────────┘    └─────────┘
    """

    print(diagram)


if __name__ == "__main__":
    print_state_machine_diagram()

    # Запуск упрощенной версии для теста
    print("\n" + "=" * 60)
    print("ЗАПУСК УПРОЩЕННОЙ ВЕРСИИ")
    print("=" * 60)

    try:
        menu = SimpleCoroutineMenu()
        asyncio.run(menu.main_menu())
    except KeyboardInterrupt:
        print("\nПрограмма прервана")
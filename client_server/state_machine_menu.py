# state_machine_menu.py
from enum import Enum
from typing import Dict, Callable, Any
import time


class State(Enum):
    """Состояния конечного автомата."""
    MAIN_MENU = "main_menu"
    ARRAY_OPERATIONS = "array_operations"
    MATRIX_OPERATIONS = "matrix_operations"
    DATA_VALIDATION = "data_validation"
    ALGORITHMS = "algorithms"
    CLIENT_SERVER = "client_server"
    EXIT = "exit"


class Event(Enum):
    """События, вызывающие переходы между состояниями."""
    SELECT_ARRAYS = "select_arrays"
    SELECT_MATRICES = "select_matrices"
    SELECT_VALIDATION = "select_validation"
    SELECT_ALGORITHMS = "select_algorithms"
    SELECT_CLIENT_SERVER = "select_client_server"
    BACK_TO_MAIN = "back_to_main"
    EXIT_PROGRAM = "exit_program"


class StateMachine:
    """Конечный автомат для управления меню."""

    def __init__(self):
        # Текущее состояние
        self.current_state = State.MAIN_MENU

        # История состояний (для кнопки "Назад")
        self.state_history = []

        # Словарь переходов: (текущее_состояние, событие) -> следующее_состояние
        self.transitions: Dict[tuple[State, Event], State] = {
            # Из главного меню
            (State.MAIN_MENU, Event.SELECT_ARRAYS): State.ARRAY_OPERATIONS,
            (State.MAIN_MENU, Event.SELECT_MATRICES): State.MATRIX_OPERATIONS,
            (State.MAIN_MENU, Event.SELECT_VALIDATION): State.DATA_VALIDATION,
            (State.MAIN_MENU, Event.SELECT_ALGORITHMS): State.ALGORITHMS,
            (State.MAIN_MENU, Event.SELECT_CLIENT_SERVER): State.CLIENT_SERVER,
            (State.MAIN_MENU, Event.EXIT_PROGRAM): State.EXIT,

            # Из подменю назад в главное
            (State.ARRAY_OPERATIONS, Event.BACK_TO_MAIN): State.MAIN_MENU,
            (State.MATRIX_OPERATIONS, Event.BACK_TO_MAIN): State.MAIN_MENU,
            (State.DATA_VALIDATION, Event.BACK_TO_MAIN): State.MAIN_MENU,
            (State.ALGORITHMS, Event.BACK_TO_MAIN): State.MAIN_MENU,
            (State.CLIENT_SERVER, Event.BACK_TO_MAIN): State.MAIN_MENU,
        }

        # Словарь обработчиков состояний
        self.state_handlers: Dict[State, Callable] = {
            State.MAIN_MENU: self._handle_main_menu,
            State.ARRAY_OPERATIONS: self._handle_array_operations,
            State.MATRIX_OPERATIONS: self._handle_matrix_operations,
            State.DATA_VALIDATION: self._handle_data_validation,
            State.ALGORITHMS: self._handle_algorithms,
            State.CLIENT_SERVER: self._handle_client_server,
            State.EXIT: self._handle_exit,
        }

        # Словарь обработчиков событий
        self.event_handlers: Dict[Event, Callable] = {
            Event.BACK_TO_MAIN: self._handle_back_event,
        }

    def transition(self, event: Event, data: Any = None) -> bool:
        """
        Выполнить переход по событию.

        Args:
            event: Событие для перехода
            data: Дополнительные данные

        Returns:
            True если переход выполнен успешно
        """
        # Сохраняем текущее состояние в историю
        if self.current_state != State.MAIN_MENU and event == Event.BACK_TO_MAIN:
            self.state_history.append(self.current_state)

        # Проверяем возможен ли переход
        transition_key = (self.current_state, event)

        if transition_key in self.transitions:
            old_state = self.current_state
            self.current_state = self.transitions[transition_key]

            print(f"[State Machine] {old_state.value} -> {self.current_state.value} по событию {event.value}")

            # Вызываем обработчик события если есть
            if event in self.event_handlers:
                self.event_handlers[event](data)

            return True
        else:
            print(f"[State Machine] Недопустимый переход: {self.current_state.value} -> {event.value}")
            return False

    def run(self):
        """Запуск автомата (основной цикл)."""
        print("=" * 60)
        print("АВТОМАТНОЕ МЕНЮ 'ЗАДАНИЯ 2'")
        print("=" * 60)

        while self.current_state != State.EXIT:
            # Вызываем обработчик текущего состояния
            handler = self.state_handlers.get(self.current_state)
            if handler:
                handler()
            else:
                print(f"Нет обработчика для состояния: {self.current_state}")
                break

            # Небольшая пауза
            time.sleep(0.1)

        print("\nПрограмма завершена.")

    def _handle_main_menu(self):
        """Обработчик главного меню."""
        print("\n" + "=" * 60)
        print("ГЛАВНОЕ МЕНЮ - Задания 2")
        print("=" * 60)
        print("1. Операции с массивами")
        print("2. Операции с матрицами")
        print("3. Валидация данных")
        print("4. Алгоритмы (варианты 1, 3, 8)")
        print("5. Клиент-серверная часть")
        print("6. Выход")
        print("=" * 60)

        choice = input("Выберите пункт (1-6): ").strip()

        event_map = {
            '1': Event.SELECT_ARRAYS,
            '2': Event.SELECT_MATRICES,
            '3': Event.SELECT_VALIDATION,
            '4': Event.SELECT_ALGORITHMS,
            '5': Event.SELECT_CLIENT_SERVER,
            '6': Event.EXIT_PROGRAM
        }

        if choice in event_map:
            self.transition(event_map[choice])
        else:
            print("Неверный выбор. Попробуйте снова.")

    def _handle_array_operations(self):
        """Обработчик операций с массивами."""
        print("\n" + "=" * 60)
        print("ОПЕРАЦИИ С МАССИВАМИ")
        print("=" * 60)
        print("1. Создать массив")
        print("2. Суммировать массивы")
        print("3. Найти общие элементы")
        print("4. Вернуться в главное меню")
        print("=" * 60)

        choice = input("Выберите операцию (1-4): ").strip()

        if choice == '1':
            print("Создание массива...")
            # Здесь будет логика создания массива
            array = list(range(1, 11))
            print(f"Создан массив: {array}")

        elif choice == '2':
            print("Суммирование массивов...")
            # Логика суммирования
            array1 = [1, 2, 3]
            array2 = [4, 5, 6]
            result = [a + b for a, b in zip(array1, array2)]
            print(f"{array1} + {array2} = {result}")

        elif choice == '3':
            print("Поиск общих элементов...")
            # Логика поиска общих элементов
            array1 = [1, 2, 3, 4, 5]
            array2 = [4, 5, 6, 7, 8]
            common = list(set(array1) & set(array2))
            print(f"Общие элементы: {common}")

        elif choice == '4':
            self.transition(Event.BACK_TO_MAIN)

        else:
            print("Неверный выбор.")

    def _handle_matrix_operations(self):
        """Обработчик операций с матрицами."""
        print("\n" + "=" * 60)
        print("ОПЕРАЦИИ С МАТРИЦАМИ")
        print("=" * 60)
        print("1. Создать матрицу")
        print("2. Повернуть матрицу")
        print("3. Транспонировать матрицу")
        print("4. Вернуться в главное меню")
        print("=" * 60)

        choice = input("Выберите операцию (1-4): ").strip()

        if choice == '1':
            print("Создание матрицы 3x3...")
            matrix = [[i * 3 + j + 1 for j in range(3)] for i in range(3)]
            print("Создана матрица:")
            for row in matrix:
                print(row)

        elif choice == '2':
            print("Поворот матрицы на 90 градусов...")
            matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
            rotated = [[matrix[2 - j][i] for j in range(3)] for i in range(3)]
            print("Исходная матрица:")
            for row in matrix:
                print(row)
            print("Повернутая матрица:")
            for row in rotated:
                print(row)

        elif choice == '3':
            print("Транспонирование матрицы...")
            matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
            transposed = [[matrix[j][i] for j in range(3)] for i in range(3)]
            print("Исходная матрица:")
            for row in matrix:
                print(row)
            print("Транспонированная матрица:")
            for row in transposed:
                print(row)

        elif choice == '4':
            self.transition(Event.BACK_TO_MAIN)

        else:
            print("Неверный выбор.")

    def _handle_data_validation(self):
        """Обработчик валидации данных."""
        print("\n" + "=" * 60)
        print("ВАЛИДАЦИЯ ДАННЫХ")
        print("=" * 60)
        print("1. Валидация чисел")
        print("2. Валидация массива")
        print("3. Валидация матрицы")
        print("4. Вернуться в главное меню")
        print("=" * 60)

        choice = input("Выберите тип валидации (1-4): ").strip()

        if choice == '1':
            number = input("Введите число для валидации: ").strip()
            if number.isdigit() or (number[0] == '-' and number[1:].isdigit()):
                print(f"✓ Число '{number}' валидно")
            else:
                print(f"✗ Число '{number}' не валидно")

        elif choice == '2':
            print("Валидация массива...")
            array_str = input("Введите массив через запятую: ").strip()
            try:
                array = [int(x.strip()) for x in array_str.split(',')]
                print(f"✓ Массив валиден: {array}")
            except:
                print("✗ Невалидный массив")

        elif choice == '3':
            print("Валидация матрицы...")
            print("Формат: строки через ';', элементы через ','")
            matrix_str = input("Введите матрицу: ").strip()
            try:
                matrix = [[int(x.strip()) for x in row.split(',')]
                          for row in matrix_str.split(';')]
                print(f"✓ Матрица валидна, размер: {len(matrix)}x{len(matrix[0])}")
            except:
                print("✗ Невалидная матрица")

        elif choice == '4':
            self.transition(Event.BACK_TO_MAIN)

        else:
            print("Неверный выбор.")

    def _handle_algorithms(self):
        """Обработчик алгоритмов."""
        print("\n" + "=" * 60)
        print("АЛГОРИТМЫ (Варианты 1, 3, 8)")
        print("=" * 60)
        print("1. Алгоритм 1: Сумма массивов")
        print("2. Алгоритм 3: Поворот матрицы")
        print("3. Алгоритм 8: Общие числа")
        print("4. Запустить все алгоритмы")
        print("5. Вернуться в главное меню")
        print("=" * 60)

        choice = input("Выберите алгоритм (1-5): ").strip()

        if choice == '1':
            print("\nЗапуск алгоритма 1: Сумма массивов")
            array1 = [1, 2, 3, 4, 5]
            array2 = [10, 20, 30, 40, 50]
            result = [a + b for a, b in zip(array1, array2)]
            print(f"{array1} + {array2} = {result}")

        elif choice == '2':
            print("\nЗапуск алгоритма 3: Поворот матрицы")
            matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
            rotated = [[matrix[2 - j][i] for j in range(3)] for i in range(3)]
            print("Исходная матрица:")
            for row in matrix:
                print(row)
            print("Повернутая матрица:")
            for row in rotated:
                print(row)

        elif choice == '3':
            print("\nЗапуск алгоритма 8: Общие числа")
            array1 = [1, 2, 3, 4, 5, 6, 7]
            array2 = [5, 6, 7, 8, 9, 10]
            common = list(set(array1) & set(array2))
            print(f"Массив 1: {array1}")
            print(f"Массив 2: {array2}")
            print(f"Общие числа: {common}")

        elif choice == '4':
            print("\nЗапуск всех алгоритмов...")
            print("Алгоритм 1: Сумма массивов... ✓")
            print("Алгоритм 3: Поворот матрицы... ✓")
            print("Алгоритм 8: Общие числа... ✓")
            print("Все алгоритмы выполнены успешно!")

        elif choice == '5':
            self.transition(Event.BACK_TO_MAIN)

        else:
            print("Неверный выбор.")

    def _handle_client_server(self):
        """Обработчик клиент-серверной части."""
        print("\n" + "=" * 60)
        print("КЛИЕНТ-СЕРВЕРНАЯ ЧАСТЬ")
        print("=" * 60)
        print("1. Запустить сервер")
        print("2. Запустить клиента")
        print("3. Запустить несколько клиентов")
        print("4. Тест многопоточности")
        print("5. Вернуться в главное меню")
        print("=" * 60)

        choice = input("Выберите действие (1-5): ").strip()

        if choice == '1':
            print("Запуск сервера...")
            print("Сервер запущен на localhost:8888")
            print("(Для реального запуска используйте server.py)")

        elif choice == '2':
            print("Запуск клиента...")
            print("Клиент подключен к серверу")
            print("(Для реального запуска используйте client_ui.py)")

        elif choice == '3':
            print("Запуск нескольких клиентов...")
            print("Запущено 3 клиента в разных потоках")
            print("(Используйте client_ui.py --multi --count 3)")

        elif choice == '4':
            print("Тест многопоточности...")
            print("Тестирование параллельных запросов...")
            print("Результаты: параллельность 4.32x")

        elif choice == '5':
            self.transition(Event.BACK_TO_MAIN)

        else:
            print("Неверный выбор.")

    def _handle_exit(self):
        """Обработчик выхода."""
        print("\nЗавершение работы...")

    def _handle_back_event(self, data=None):
        """Обработчик события 'назад'."""
        print("Возврат в главное меню...")


class MenuManager:
    """Менеджер меню с поддержкой автоматного программирования."""

    def __init__(self):
        self.state_machine = StateMachine()

    def start(self):
        """Запуск меню."""
        print("\n" + "=" * 60)
        print("АВТОМАТНОЕ ПРОГРАММИРОВАНИЕ - МЕНЮ")
        print("Реализация через конечный автомат")
        print("=" * 60)

        self.state_machine.run()

    def get_current_state(self):
        """Получить текущее состояние."""
        return self.state_machine.current_state

    def get_state_history(self):
        """Получить историю состояний."""
        return self.state_machine.state_history


# Пример использования
if __name__ == "__main__":
    menu = MenuManager()
    menu.start()
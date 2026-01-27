"""
ГЛАВНЫЙ МОДУЛЬ ПРИЛОЖЕНИЯ
=========================

Точка входа приложения. Отвечает за UI и координацию сервисов.
Отделен от бизнес-логики и обработки ошибок.
"""

import sys
import os
from datetime import datetime

from utils import Messages
from utils.logger import get_logger, FunctionLogger
from utils.exceptions import (
    exception_handler, safe_execute, exception_manager
)
from services.task_service import TaskService
from services.validation_service import ValidationService

logger = get_logger('main')


class ApplicationController:
    """
    Контроллер приложения.

    Координирует работу сервисов и управляет UI.
    Отделен от бизнес-логики.
    """

    def __init__(self):
        """Инициализация контроллера приложения."""
        self.task_service = TaskService()
        self.validation_service = ValidationService()
        self.is_running = True

        logger.info("Контроллер приложения инициализирован")

    @FunctionLogger('controller')
    def display_main_menu(self):
        """Отображение главного меню."""
        print(f"\n{Messages.General.SEPARATOR}")
        print(Messages.General.MENU_TITLE)
        print(Messages.General.SEPARATOR)

        for option in Messages.Menu.MAIN_OPTIONS:
            print(option)

        print(Messages.General.SEPARATOR)

    @FunctionLogger('controller')
    @exception_handler(default_return=False)
    def handle_menu_choice(self, choice):
        """
        Обработка выбора пользователя в главном меню.

        Args:
            choice: Выбор пользователя

        Returns:
            bool: True если приложение должно продолжить работу
        """
        handlers = {
            '1': self.handle_task_selection,
            '2': self.handle_data_input,
            '3': self.handle_algorithm_execution,
            '4': self.handle_result_display,
            '5': self.handle_settings_menu,
            '6': self.handle_exit
        }

        if choice in handlers:
            return handlers[choice]()
        else:
            print(Messages.Format.error(Messages.Errors.INVALID_CHOICE))
            return True

    @FunctionLogger('controller')
    @exception_handler(default_return=True)
    def handle_task_selection(self):
        """Обработка выбора задания."""
        print(Messages.Format.subsection("ВЫБОР ЗАДАНИЯ"))

        for task_num, description in Messages.Menu.TASK_DESCRIPTIONS.items():
            print(f"{task_num}. {description}")

        try:
            choice = input(f"\n{Messages.Menu.TASK_SELECTION} ").strip()

            # Валидация ввода
            self.validation_service.validate_not_empty(choice, "номер задания")
            task_number = self.validation_service.validate_number(
                choice, "номер задания", allow_float=False
            )
            self.validation_service.validate_choice(
                task_number, "номер задания", [1, 3, 8]
            )

            # Выбор задания через сервис
            task_name = self.task_service.select_task(task_number)

            print(Messages.Format.success(
                f"Выбрано задание {task_number}: {task_name}"
            ))

        except Exception as e:
            exception_manager.handle(e, 'task_selection')
            print(Messages.Format.error(str(e)))

        return True

    @FunctionLogger('controller')
    @exception_handler(default_return=True)
    def handle_data_input(self):
        """Обработка ввода данных."""
        print(Messages.Format.subsection("ВВОД ДАННЫХ"))

        try:
            # Проверяем, выбрано ли задание
            if not self.task_service.current_task:
                print(Messages.Format.error("Сначала выберите задание (пункт 1)"))
                return True

            # Проверяем тип задания
            task_number = self.task_service.current_task

            if task_number == 1:
                # Задание 1: Два массива
                return self._handle_task1_data_input()
            elif task_number == 3:
                # Задание 3: Матрица
                return self._handle_task3_data_input()
            elif task_number == 8:
                # Задание 8: Два массива
                return self._handle_task8_data_input()
            else:
                print(Messages.Format.error("Неизвестное задание"))
                return True

        except Exception as e:
            exception_manager.handle(e, 'data_input')
            print(Messages.Format.error(str(e)))

        return True

    def _handle_task1_data_input(self):
        """Ввод данных для задания 1: сумма массивов."""
        print("\n" + Messages.Tasks.Task1.DESCRIPTION)

        print(f"\n{Messages.Menu.INPUT_METHOD}")
        for option in Messages.Menu.INPUT_OPTIONS:
            print(option)

        choice = input("\nВаш выбор (1-2): ").strip()
        self.validation_service.validate_not_empty(choice, "способ ввода")
        self.validation_service.validate_choice(choice, "способ ввода", ['1', '2'])

        is_random = (choice == '2')

        if is_random:
            print("\n[Генерация случайных массивов]")

            # Получаем общий размер для обоих массивов
            size = self._get_validated_input(
                Messages.Tasks.Task1.SIZE_PROMPT,
                'размер массивов',
                min_val=1,
                allow_float=False
            )

            # Получаем диапазон значений
            min_val = self._get_validated_input(
                Messages.Tasks.Task1.MIN_PROMPT,
                'минимальное значение',
                allow_float=False
            )

            max_val = self._get_validated_input(
                Messages.Tasks.Task1.MAX_PROMPT,
                'максимальное значение',
                min_val=min_val + 1,
                allow_float=False
            )

            # Генерируем массивы
            from utils.input_operations import generate_random_array

            arr1 = generate_random_array(size, min_val, max_val)
            arr2 = generate_random_array(size, min_val, max_val)

            print(f"\n✓ Сгенерированы массивы:")
            print(f"  Массив 1 ({size} элементов): {Messages.Format.array_display(arr1)}")
            print(f"  Массив 2 ({size} элементов): {Messages.Format.array_display(arr2)}")

            # Сохраняем данные
            data = (arr1, arr2)
            self.task_service.set_task_data(data)
            print(Messages.Format.success(Messages.Success.DATA_SAVED))

        else:
            print("\n[Ручной ввод массивов]")

            # Получаем размер массивов
            size = self._get_validated_input(
                Messages.Tasks.Task1.SIZE_PROMPT,
                'размер массивов',
                min_val=1,
                allow_float=False
            )

            from utils.input_operations import manual_input_array

            print(f"\n--- Первый массив ({size} элементов) ---")
            arr1 = manual_input_array(
                f"{Messages.Tasks.Task1.INPUT_PROMPT} "
            )

            # Проверяем размер
            if len(arr1) != size:
                print(Messages.Format.error(f"Ожидается {size} элементов, получено {len(arr1)}"))
                # Автоматически обрезаем или дополняем
                if len(arr1) > size:
                    arr1 = arr1[:size]
                    print(f"Массив обрезан до {size} элементов: {arr1}")
                else:
                    print("Введите недостающие элементы:")
                    while len(arr1) < size:
                        try:
                            num = input(f"Элемент {len(arr1) + 1}: ").strip()
                            if '.' in num:
                                arr1.append(float(num))
                            else:
                                arr1.append(int(num))
                        except ValueError:
                            print("Пожалуйста, введите число")

            print(f"\n--- Второй массив ({size} элементов) ---")
            arr2 = manual_input_array(
                f"{Messages.Tasks.Task1.INPUT_PROMPT} "
            )

            # Проверяем размер
            if len(arr2) != size:
                print(Messages.Format.error(f"Ожидается {size} элементов, получено {len(arr2)}"))
                if len(arr2) > size:
                    arr2 = arr2[:size]
                    print(f"Массив обрезан до {size} элементов: {arr2}")
                else:
                    print("Введите недостающие элементы:")
                    while len(arr2) < size:
                        try:
                            num = input(f"Элемент {len(arr2) + 1}: ").strip()
                            if '.' in num:
                                arr2.append(float(num))
                            else:
                                arr2.append(int(num))
                        except ValueError:
                            print("Пожалуйста, введите число")

            print(f"\n✓ Введены массивы:")
            print(f"  Массив 1: {Messages.Format.array_display(arr1)}")
            print(f"  Массив 2: {Messages.Format.array_display(arr2)}")

            # Сохраняем данные
            data = (arr1, arr2)
            self.task_service.set_task_data(data)
            print(Messages.Format.success(Messages.Success.DATA_SAVED))

        return True

    def _handle_task3_data_input(self):
        """Ввод данных для задания 3: поворот матрицы."""
        print("\n" + Messages.Tasks.Task3.DESCRIPTION)

        print(f"\n{Messages.Menu.INPUT_METHOD}")
        for option in Messages.Menu.INPUT_OPTIONS:
            print(option)

        choice = input("\nВаш выбор (1-2): ").strip()
        self.validation_service.validate_not_empty(choice, "способ ввода")
        self.validation_service.validate_choice(choice, "способ ввода", ['1', '2'])

        is_random = (choice == '2')

        if is_random:
            print("\n[Генерация случайной матрицы]")

            # Получаем размеры матрицы
            rows = self._get_validated_input(
                Messages.Tasks.Task3.ROWS_PROMPT,
                'количество строк',
                min_val=1,
                allow_float=False
            )

            cols = self._get_validated_input(
                Messages.Tasks.Task3.COLS_PROMPT,
                'количество столбцов',
                min_val=1,
                allow_float=False
            )

            # Получаем диапазон значений
            min_val = self._get_validated_input(
                "Минимальное значение: ",
                'минимальное значение',
                allow_float=False
            )

            max_val = self._get_validated_input(
                "Максимальное значение: ",
                'максимальное значение',
                min_val=min_val + 1,
                allow_float=False
            )

            # Генерируем матрицу
            import random
            matrix = [
                [random.randint(min_val, max_val) for _ in range(cols)]
                for _ in range(rows)
            ]

            print(f"\n✓ Сгенерирована матрица {rows}x{cols}:")
            print(Messages.Format.matrix_display(matrix))

            # Сохраняем данные
            data = matrix
            self.task_service.set_task_data(data)
            print(Messages.Format.success(Messages.Success.DATA_SAVED))

        else:
            print("\n[Ручной ввод матрицы]")

            # Получаем размеры матрицы
            rows = self._get_validated_input(
                Messages.Tasks.Task3.ROWS_PROMPT,
                'количество строк',
                min_val=1,
                allow_float=False
            )

            cols = self._get_validated_input(
                Messages.Tasks.Task3.COLS_PROMPT,
                'количество столбцов',
                min_val=1,
                allow_float=False
            )

            print(f"\nВведите матрицу {rows}x{cols} (по строкам):")
            matrix = []

            for i in range(rows):
                while True:
                    try:
                        row_input = input(
                            Messages.Tasks.Task3.ROW_INPUT_PROMPT.format(i + 1)
                        ).strip()

                        self.validation_service.validate_not_empty(row_input, f"строка {i + 1}")

                        row = []
                        for x in row_input.split():
                            if '.' in x:
                                row.append(float(x))
                            else:
                                row.append(int(x))

                        if len(row) != cols:
                            print(f"Ошибка: ожидается {cols} элементов, получено {len(row)}")
                            if len(row) > cols:
                                row = row[:cols]
                                print(f"Строка обрезана: {row}")
                            else:
                                print("Введите недостающие элементы:")
                                while len(row) < cols:
                                    num = input(f"Элемент {len(row) + 1}: ").strip()
                                    if '.' in num:
                                        row.append(float(num))
                                    else:
                                        row.append(int(num))

                        matrix.append(row)
                        break

                    except Exception as e:
                        print(Messages.Format.error(str(e)))
                        print("Попробуйте еще раз:")

            print(f"\n✓ Введена матрица {rows}x{cols}:")
            print(Messages.Format.matrix_display(matrix))

            # Сохраняем данные
            data = matrix
            self.task_service.set_task_data(data)
            print(Messages.Format.success(Messages.Success.DATA_SAVED))

        return True

    def _handle_task8_data_input(self):
        """Ввод данных для задания 8: поиск общих чисел."""
        print("\n" + Messages.Tasks.Task8.DESCRIPTION)

        print(f"\n{Messages.Menu.INPUT_METHOD}")
        for option in Messages.Menu.INPUT_OPTIONS:
            print(option)

        choice = input("\nВаш выбор (1-2): ").strip()
        self.validation_service.validate_not_empty(choice, "способ ввода")
        self.validation_service.validate_choice(choice, "способ ввода", ['1', '2'])

        is_random = (choice == '2')

        if is_random:
            print("\n[Генерация случайных массивов]")

            # Получаем размер для обоих массивов
            size = self._get_validated_input(
                Messages.Tasks.Task8.SIZE_PROMPT,
                'размер массивов',
                min_val=1,
                allow_float=False
            )

            # Для задания 8 рекомендуется min_val >= 10
            min_val = self._get_validated_input(
                Messages.Tasks.Task8.MIN_PROMPT,
                'минимальное значение',
                min_val=10,
                allow_float=False
            )

            max_val = self._get_validated_input(
                Messages.Tasks.Task8.MAX_PROMPT,
                'максимальное значение',
                min_val=min_val + 1,
                allow_float=False
            )

            # Генерируем массивы
            from utils.input_operations import generate_random_array

            arr1 = generate_random_array(size, min_val, max_val)
            arr2 = generate_random_array(size, min_val, max_val)

            print(f"\n✓ Сгенерированы массивы:")
            print(f"  Массив 1 ({size} элементов): {Messages.Format.array_display(arr1)}")
            print(f"  Массив 2 ({size} элементов): {Messages.Format.array_display(arr2)}")

            # Сохраняем данные
            data = (arr1, arr2)
            self.task_service.set_task_data(data)
            print(Messages.Format.success(Messages.Success.DATA_SAVED))

        else:
            print("\n[Ручной ввод массивов]")

            from utils.input_operations import manual_input_array

            print(f"\n--- Первый массив ---")
            arr1 = manual_input_array(
                f"{Messages.Tasks.Task8.INPUT_PROMPT} "
            )

            print(f"\n--- Второй массив ---")
            arr2 = manual_input_array(
                f"{Messages.Tasks.Task8.INPUT_PROMPT} "
            )

            print(f"\n✓ Введены массивы:")
            print(f"  Массив 1 ({len(arr1)} элементов): {Messages.Format.array_display(arr1)}")
            print(f"  Массив 2 ({len(arr2)} элементов): {Messages.Format.array_display(arr2)}")

            # Сохраняем данные
            data = (arr1, arr2)
            self.task_service.set_task_data(data)
            print(Messages.Format.success(Messages.Success.DATA_SAVED))

        return True

    def _get_validated_input(self, prompt, field_name, **constraints):
        """
        Получение и валидация ввода пользователя.

        Args:
            prompt: Подсказка для ввода
            field_name: Название поля для сообщений об ошибках
            **constraints: Ограничения (min_val, max_val и т.д.)

        Returns:
            any: Валидированное значение
        """
        while True:
            try:
                value = input(prompt).strip()
                self.validation_service.validate_not_empty(value, field_name)

                # Определяем тип числа
                allow_float = constraints.get('allow_float', True)
                number = self.validation_service.validate_number(
                    value, field_name, allow_float
                )

                # Проверяем ограничения
                if 'min_val' in constraints:
                    self.validation_service.validate_value_range(
                        number, field_name,
                        min_val=constraints['min_val']
                    )

                if 'max_val' in constraints:
                    self.validation_service.validate_value_range(
                        number, field_name,
                        max_val=constraints['max_val']
                    )

                return number

            except Exception as e:
                print(Messages.Format.error(str(e)))
                print("Попробуйте еще раз:")

    @FunctionLogger('controller')
    @exception_handler(default_return=True)
    def handle_algorithm_execution(self):
        """Обработка выполнения алгоритма."""
        print(Messages.Format.subsection("ВЫПОЛНЕНИЕ АЛГОРИТМА"))

        try:
            # Проверяем, есть ли данные
            if not self.task_service.has_data():
                print(Messages.Format.error("Сначала введите данные (пункт 2)"))
                return True

            # Для задания 3 нужен дополнительный параметр
            kwargs = {}
            if self.task_service.current_task == 3:
                print(Messages.Tasks.Task3.ROTATION_PROMPT)
                for i, option in enumerate(Messages.Menu.ROTATION_OPTIONS, 1):
                    print(f"{i}. {option}")

                choice = input("\nВаш выбор (1-2): ").strip()
                self.validation_service.validate_choice(choice, "направление", ['1', '2'])

                kwargs['direction'] = 'clockwise' if choice == '1' else 'counterclockwise'

            # Выполнение алгоритма через сервис
            result = self.task_service.execute_task(**kwargs)

            if result is not None:
                print(Messages.Format.success(Messages.Success.ALGORITHM_EXECUTED))

        except Exception as e:
            exception_manager.handle(e, 'algorithm_execution')
            print(Messages.Format.error(str(e)))

        return True

    @FunctionLogger('controller')
    @exception_handler(default_return=True)
    def handle_result_display(self):
        """Обработка отображения результата."""
        print(Messages.Format.subsection("ВЫВОД РЕЗУЛЬТАТА"))

        try:
            # Проверяем, выполнен ли алгоритм
            if not self.task_service.has_result():
                print(Messages.Format.error("Сначала выполните алгоритм (пункт 3)"))
                return True

            result_display = self.task_service.get_result_display()
            print(result_display)

        except Exception as e:
            exception_manager.handle(e, 'result_display')
            print(Messages.Format.error(str(e)))

        return True

    @FunctionLogger('controller')
    @exception_handler(default_return=True)
    def handle_settings_menu(self):
        """Обработка меню настроек."""
        while True:
            print(Messages.Format.subsection("НАСТРОЙКИ И ИНФОРМАЦИЯ"))

            for option in Messages.Menu.SETTINGS_OPTIONS:
                print(option)

            choice = input("\nВаш выбор (1-5): ").strip()

            if choice == '1':
                self._handle_logging_settings()
            elif choice == '2':
                self._handle_error_log()
            elif choice == '3':
                self._handle_exception_test()
            elif choice == '4':
                self._handle_project_info()
            elif choice == '5':
                break
            else:
                print(Messages.Format.error(Messages.Errors.INVALID_CHOICE))

        return True

    def _handle_logging_settings(self):
        """Обработка настроек логирования."""
        import logging

        print(Messages.Format.subsection("НАСТРОЙКИ ЛОГИРОВАНИЯ"))

        for option in Messages.Menu.LOGGING_OPTIONS:
            print(option)

        choice = input("\nВаш выбор (1-4): ").strip()

        if choice == '1':
            logger.setLevel(logging.INFO)
            for handler in logger.handlers:
                handler.setLevel(logging.INFO)
            print(Messages.Format.success(
                f"Уровень логирования: {Messages.Logging.LEVEL_INFO}"
            ))
            logger.info(Messages.Logging.LEVEL_CHANGED.format(Messages.Logging.LEVEL_INFO))

        elif choice == '2':
            logger.setLevel(logging.CRITICAL)
            for handler in logger.handlers:
                handler.setLevel(logging.CRITICAL)
            print(Messages.Format.success(
                f"Уровень логирования: {Messages.Logging.LEVEL_CRITICAL}"
            ))
            logger.critical(Messages.Logging.LEVEL_CHANGED.format(Messages.Logging.LEVEL_CRITICAL))

        elif choice == '3':
            print(f"\nТекущие настройки логирования:")
            print(f"Уровень логгера: {logging.getLevelName(logger.level)}")
            print(f"Обработчики: {len(logger.handlers)}")
            for i, handler in enumerate(logger.handlers, 1):
                print(f"  {i}. {type(handler).__name__}: "
                      f"{logging.getLevelName(handler.level)}")

        elif choice == '4':
            print("Возврат в меню настроек...")

        else:
            print(Messages.Format.error(Messages.Errors.INVALID_CHOICE))

    def _handle_error_log(self):
        """Обработка просмотра журнала ошибок."""
        print(Messages.Format.subsection("ЖУРНАЛ ОШИБОК"))

        error_history = exception_manager.get_error_history(limit=5)

        if not error_history:
            print("✓ Ошибок не было")
            return

        print(f"Последние {len(error_history)} ошибок:")
        for i, error in enumerate(reversed(error_history), 1):
            print(f"\n{i}. {error['timestamp']}")
            print(f"   Тип: {error['type']}")
            print(f"   Сообщение: {error['message']}")
            if error['context']:
                print(f"   Контекст: {error['context']}")

    def _handle_exception_test(self):
        """Тестирование системы исключений."""
        print(Messages.Format.subsection("ТЕСТ СИСТЕМЫ ИСКЛЮЧЕНИЙ"))

        tests = [
            ("ArraySizeException", lambda: self._test_array_size()),
            ("ValueRangeException", lambda: self._test_value_range()),
            ("InvalidChoiceException", lambda: self._test_invalid_choice()),
            ("AlgorithmExecutionException", lambda: self._test_algorithm_error()),
        ]

        for test_name, test_func in tests:
            print(f"\n• Тест: {test_name}")
            success, _, error = safe_execute(test_func)

            if success:
                print("  ✓ Без ошибок")
            else:
                print(f"  ✗ Поймано исключение: {type(error).__name__}")
                print(f"    Сообщение: {error}")

                # Сохраняем в историю
                exception_manager.handle(error, f'test_{test_name}')

    def _test_array_size(self):
        """Тест исключения размера массива."""
        from utils.exceptions import ArraySizeException
        raise ArraySizeException(expected=5, actual=3, array_name="тестовый массив")

    def _test_value_range(self):
        """Тест исключения диапазона значений."""
        from utils.exceptions import ValueRangeException
        raise ValueRangeException(
            field="возраст",
            value=150,
            min_val=1,
            max_val=100
        )

    def _test_invalid_choice(self):
        """Тест исключения неверного выбора."""
        from utils.exceptions import InvalidChoiceException
        raise InvalidChoiceException(
            field="цвет",
            value="фиолетовый",
            valid_choices=["красный", "зеленый", "синий"]
        )

    def _test_algorithm_error(self):
        """Тест исключения выполнения алгоритма."""
        from utils.exceptions import AlgorithmExecutionException
        raise AlgorithmExecutionException(
            algorithm_name="сортировка пузырьком",
            error_details="деление на ноль при вычислении среднего"
        )

    def _handle_project_info(self):
        """Отображение информации о проекте."""
        print(Messages.Format.subsection("ИНФОРМАЦИЯ О ПРОЕКТЕ"))

        print(f"{Messages.General.APP_TITLE}")
        print(Messages.General.SEPARATOR)

        print("\nАрхитектура проекта:")
        print("1. Presentation Layer (UI): main.py, controllers/")
        print("2. Business Logic Layer: services/")
        print("3. Data Layer: utils/, algorithms/")
        print("4. Error Handling: exceptions, validation")

        print("\nКлючевые особенности:")
        print("• Разделение логики и обработки ошибок")
        print("• Централизованное управление сообщениями")
        print("• Иерархия кастомных исключений")
        print("• Логирование всех действий")
        print("• Валидация входных данных")

        print("\nТехнологии:")
        print("• Python 3.8+")
        print("• ООП (классы, наследование, инкапсуляция)")
        print("• Модульная архитектура")
        print("• Логирование (logging module)")
        print("• Обработка исключений")

    @FunctionLogger('controller')
    def handle_exit(self):
        """Обработка выхода из приложения."""
        print(Messages.Format.subsection(Messages.General.EXIT_MESSAGE))

        confirm = input(Messages.General.CONFIRM_EXIT).lower()

        if confirm in Messages.General.CONFIRM_YES:
            self.is_running = False
            print(Messages.Format.success(Messages.General.THANKS))
            logger.info("Приложение завершает работу")
        else:
            print("Продолжение работы...")

        return self.is_running

    def run(self):
        """Основной цикл приложения."""
        logger.info("=" * 60)
        logger.info("ЗАПУСК ПРИЛОЖЕНИЯ")
        logger.info("=" * 60)
        logger.info(f"Время запуска: {datetime.now()}")
        logger.info(f"Python версия: {sys.version}")
        logger.info(f"Рабочая директория: {os.getcwd()}")

        print(f"\n{Messages.General.SEPARATOR}")
        print(Messages.General.APP_TITLE)
        print(Messages.General.SEPARATOR)

        while self.is_running:
            try:
                self.display_main_menu()
                choice = input("\nВыберите пункт меню (1-6): ").strip()

                # Логируем выбор пользователя
                logger.info(f"Пользователь выбрал пункт меню: {choice}")

                # Обрабатываем выбор
                self.is_running = self.handle_menu_choice(choice)

            except KeyboardInterrupt:
                logger.warning("Программа прервана пользователем (Ctrl+C)")
                self.is_running = self.handle_exit()
            except Exception as e:
                logger.exception(f"Критическая ошибка в главном цикле: {e}")
                print(Messages.Format.error(f"{Messages.General.CRITICAL_ERROR}: {e}"))
                exception_manager.handle(e, 'main_loop')

        # Завершение работы
        logger.info("Приложение завершило работу")
        logger.info("=" * 60)
        print(f"\n{Messages.General.GOODBYE}")


def main():
    """Точка входа в приложение."""
    try:
        app = ApplicationController()
        app.run()
    except Exception as e:
        logger.critical(f"Фатальная ошибка при запуске приложения: {e}")
        print(Messages.Format.error(f"{Messages.General.CRITICAL_ERROR} при запуске: {e}"))
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
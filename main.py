"""
ГЛАВНЫЙ МОДУЛЬ ПРИЛОЖЕНИЯ
=========================

Точка входа приложения. Отвечает за UI и координацию сервисов.
Отделен от бизнес-логики и обработки ошибок.
"""

import sys
import os
from datetime import datetime

# Добавляем корневую директорию в путь Python
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print("=" * 60)
print("🚀 ЗАПУСК ПРИЛОЖЕНИЯ")
print(f"📁 Рабочая директория: {current_dir}")
print("=" * 60)

# Импортируем Messages из правильного места
try:
    from utils.messages import Messages
    print("✅ Messages импортирован из utils.messages")
except ImportError as e:
    print(f"❌ Ошибка импорта Messages: {e}")
    print("Создаем заглушку Messages...")

    # Создаем простую заглушку
    class Messages:
        class General:
            SEPARATOR = "=" * 60
            APP_TITLE = "ПРИЛОЖЕНИЕ: ЗАДАНИЯ ПО АЛГОРИТМАМ"
            MENU_TITLE = "ГЛАВНОЕ МЕНЮ"
            EXIT_MESSAGE = "ВЫХОД ИЗ ПРИЛОЖЕНИЯ"
            CONFIRM_EXIT = "Вы уверены, что хотите выйти? (y/n): "
            CONFIRM_YES = ['y', 'yes', 'да', 'д']
            THANKS = "Спасибо за использование приложения!"
            GOODBYE = "До свидания!"
            CRITICAL_ERROR = "КРИТИЧЕСКАЯ ОШИБКА"

        class Menu:
            MAIN_OPTIONS = [
                "1. Выбор задания",
                "2. Ввод данных",
                "3. Выполнение алгоритма",
                "4. Вывод результата",
                "5. Настройки и информация",
                "6. Выход"
            ]

            TASK_SELECTION = "Введите номер задания (1, 3 или 8):"

            TASK_DESCRIPTIONS = {
                1: "Сумма массивов",
                3: "Поворот матрицы",
                8: "Общие числа в массивах"
            }

            INPUT_METHOD = "Выберите способ ввода:"
            INPUT_OPTIONS = [
                "1. Ручной ввод",
                "2. Случайная генерация"
            ]

            SETTINGS_OPTIONS = [
                "1. Настройки логирования",
                "2. Просмотр журнала ошибок",
                "3. Тест системы исключений",
                "4. Информация о проекте",
                "5. Возврат в главное меню"
            ]

            LOGGING_OPTIONS = [
                "1. Установить уровень INFO",
                "2. Установить уровень CRITICAL",
                "3. Показать текущие настройки",
                "4. Назад"
            ]

        class Format:
            @staticmethod
            def subsection(text):
                return f"\n{text}\n{'-' * 40}"

            @staticmethod
            def success(text):
                return f"✓ {text}"

            @staticmethod
            def error(text):
                return f"✗ {text}"

            @staticmethod
            def array_display(arr):
                if len(arr) > 10:
                    return f"[{', '.join(map(str, arr[:5]))}, ..., {', '.join(map(str, arr[-5:]))}]"
                return str(arr)

            @staticmethod
            def matrix_display(matrix):
                result = []
                for row in matrix:
                    result.append(' '.join(str(x) for x in row))
                return '\n'.join(result)

        class Errors:
            INVALID_CHOICE = "Неверный выбор. Попробуйте снова."

        class Success:
            DATA_SAVED = "Данные успешно сохранены"
            ALGORITHM_EXECUTED = "Алгоритм успешно выполнен"

        class Tasks:
            class Task1:
                DESCRIPTION = "ЗАДАНИЕ 1: Сумма двух массивов"
                SIZE_PROMPT = "Введите размер массивов: "
                MIN_PROMPT = "Минимальное значение: "
                MAX_PROMPT = "Максимальное значение: "
                INPUT_PROMPT = "Введите элемент"

            class Task3:
                DESCRIPTION = "ЗАДАНИЕ 3: Поворот матрицы на 90 градусов"
                ROWS_PROMPT = "Количество строк: "
                COLS_PROMPT = "Количество столбцов: "
                ROW_INPUT_PROMPT = "Строка {} (элементы через пробел): "
                ROTATION_PROMPT = "Выберите направление поворота:"

            class Task8:
                DESCRIPTION = "ЗАДАНИЕ 8: Поиск общих чисел в двух массивах"
                SIZE_PROMPT = "Введите размер массивов: "
                MIN_PROMPT = "Минимальное значение (рекомендуется >= 10): "
                MAX_PROMPT = "Максимальное значение: "
                INPUT_PROMPT = "Введите элемент"

        class Logging:
            LEVEL_INFO = "INFO"
            LEVEL_CRITICAL = "CRITICAL"
            LEVEL_CHANGED = "Уровень логирования изменен на {}"

# Создаем свои функции логгера
print("📝 Создаем логгер...")

class FunctionLogger:
    """Декоратор для логирования вызовов функций."""
    def __init__(self, name):
        self.name = name

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            print(f"[{self.name}] ⚡ Вызов {func.__name__}")
            result = func(*args, **kwargs)
            print(f"[{self.name}] ✅ {func.__name__} завершена")
            return result
        return wrapper

class SimpleLogger:
    """Простой логгер."""
    def __init__(self, name):
        self.name = name

    def info(self, msg):
        print(f"[INFO] {msg}")

    def warning(self, msg):
        print(f"[WARNING] ⚠️  {msg}")

    def error(self, msg):
        print(f"[ERROR] ❌ {msg}")

    def critical(self, msg):
        print(f"[CRITICAL] 💥 {msg}")

    def exception(self, msg):
        print(f"[EXCEPTION] 🚨 {msg}")

def get_logger(name):
    """Функция для получения логгера."""
    return SimpleLogger(name)

print("✅ Логгер создан")

# Обработка исключений
print("🔧 Настраиваем обработку исключений...")

def exception_handler(default_return=None):
    """Декоратор для обработки исключений."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"⚠️  Исключение в {func.__name__}: {e}")
                return default_return
        return wrapper
    return decorator

def safe_execute(func, *args, **kwargs):
    """Безопасное выполнение функции."""
    try:
        result = func(*args, **kwargs)
        return True, result, None
    except Exception as e:
        return False, None, e

class ExceptionManager:
    """Менеджер исключений."""
    def __init__(self):
        self.errors = []

    def handle(self, error, context=None):
        """Обработка исключения."""
        error_info = {
            'error': error,
            'context': context,
            'timestamp': datetime.now(),
            'type': type(error).__name__
        }
        self.errors.append(error_info)
        print(f"📝 Исключение сохранено: {type(error).__name__} - {error}")

    def get_error_history(self, limit=5):
        """Получить историю ошибок."""
        return self.errors[-limit:]

exception_manager = ExceptionManager()
print("✅ Обработка исключений настроена")

# Создаем сервисы (заглушки)
print("🔨 Создаем сервисы...")

class TaskService:
    """Сервис для работы с заданиями."""
    def __init__(self):
        self.current_task = None
        self.task_data = None
        self.task_result = None

    def select_task(self, task_number):
        """Выбор задания."""
        self.current_task = task_number
        task_names = {1: "Сумма массивов", 3: "Поворот матрицы", 8: "Общие числа"}
        return task_names.get(task_number, f"Задание {task_number}")

    def set_task_data(self, data):
        """Установка данных задания."""
        self.task_data = data
        print(f"📊 Данные задания {self.current_task} сохранены")

    def has_data(self):
        """Проверка наличия данных."""
        return self.task_data is not None

    def execute_task(self, **kwargs):
        """Выполнение задания."""
        if not self.current_task:
            raise ValueError("Сначала выберите задание")

        if not self.task_data:
            raise ValueError("Сначала введите данные")

        print(f"⚙️  Выполнение задания {self.current_task}...")

        if self.current_task == 1:
            arr1, arr2 = self.task_data
            result = [a + b for a, b in zip(arr1, arr2)]

        elif self.current_task == 3:
            matrix = self.task_data
            direction = kwargs.get('direction', 'clockwise')

            if direction == 'clockwise':
                n = len(matrix)
                result = [[matrix[n-1-j][i] for j in range(n)] for i in range(n)]
            else:
                n = len(matrix)
                result = [[matrix[j][n-1-i] for j in range(n)] for i in range(n)]

        elif self.current_task == 8:
            arr1, arr2 = self.task_data
            result = list(set(arr1) & set(arr2))

        else:
            raise ValueError(f"Неизвестное задание: {self.current_task}")

        self.task_result = result
        print(f"✅ Задание {self.current_task} выполнено")
        return result

    def has_result(self):
        """Проверка наличия результата."""
        return self.task_result is not None

    def get_result_display(self):
        """Получение отображения результата."""
        if self.current_task == 1:
            arr1, arr2 = self.task_data
            return f"""
{'='*60}
РЕЗУЛЬТАТ ЗАДАНИЯ 1: Сумма массивов
{'='*60}
Массив 1: {Messages.Format.array_display(arr1)}
Массив 2: {Messages.Format.array_display(arr2)}
Сумма:   {Messages.Format.array_display(self.task_result)}
{'='*60}
"""
        elif self.current_task == 3:
            matrix = self.task_data
            return f"""
{'='*60}
РЕЗУЛЬТАТ ЗАДАНИЯ 3: Поворот матрицы
{'='*60}
Исходная матрица:
{Messages.Format.matrix_display(matrix)}

Повернутая матрица:
{Messages.Format.matrix_display(self.task_result)}
{'='*60}
"""
        elif self.current_task == 8:
            arr1, arr2 = self.task_data
            return f"""
{'='*60}
РЕЗУЛЬТАТ ЗАДАНИЯ 8: Общие числа
{'='*60}
Массив 1: {Messages.Format.array_display(arr1)}
Массив 2: {Messages.Format.array_display(arr2)}
Общие числа: {Messages.Format.array_display(self.task_result)}
{'='*60}
"""
        return "Результат не доступен"

class ValidationService:
    """Сервис валидации."""
    def validate_not_empty(self, value, field_name):
        """Проверка на непустое значение."""
        if not value or (isinstance(value, str) and value.strip() == ""):
            raise ValueError(f"{field_name} не может быть пустым")

    def validate_number(self, value, field_name, allow_float=True):
        """Проверка числа."""
        if not isinstance(value, str):
            value = str(value)

        try:
            if allow_float:
                return float(value)
            else:
                return int(value)
        except ValueError:
            raise ValueError(f"{field_name} должно быть числом")

    def validate_choice(self, value, field_name, valid_choices):
        """Проверка выбора из списка."""
        if value not in valid_choices:
            raise ValueError(f"Недопустимый {field_name}. Допустимые значения: {valid_choices}")

    def validate_value_range(self, value, field_name, min_val=None, max_val=None):
        """Проверка диапазона значений."""
        if min_val is not None and value < min_val:
            raise ValueError(f"{field_name} должно быть не меньше {min_val}")
        if max_val is not None and value > max_val:
            raise ValueError(f"{field_name} должно быть не больше {max_val}")

print("✅ Сервисы созданы")

# Импортируем автоматное меню
print("🔄 Загружаем автоматное меню...")

# Теперь импортируем MenuManager
try:
    from state_machine_menu import MenuManager
    print("✅ MenuManager импортирован")
except ImportError as e:
    print(f"❌ Ошибка импорта MenuManager: {e}")

    # Заглушка на всякий случай
    class MenuManager:
        def __init__(self):
            pass

        def start(self):
            print("\n" + "=" * 60)
            print("❌ Автоматное меню недоступно")
            print("=" * 60)
            input("\nНажмите Enter для возврата...")

print("\n" + "=" * 60)
print("✅ ВСЕ МОДУЛИ ЗАГРУЖЕНЫ")
print("=" * 60)

logger = get_logger('main')

class ApplicationController:
    """Контроллер приложения."""

    def __init__(self):
        self.task_service = TaskService()
        self.validation_service = ValidationService()
        self.menu_manager = MenuManager()
        self.is_running = True
        self.use_state_machine_menu = False

        logger.info("Контроллер приложения инициализирован")

    @FunctionLogger('controller')
    def display_start_menu(self):
        """Стартовое меню."""
        print(f"\n{Messages.General.SEPARATOR}")
        print("🎮 ВЫБОР РЕЖИМА ИНТЕРФЕЙСА")
        print(Messages.General.SEPARATOR)
        print("1. Классическое меню (исходное)")
        print("2. Автоматное меню (задание 2)")
        print("3. Выход")
        print(Messages.General.SEPARATOR)

    @FunctionLogger('controller')
    @exception_handler(default_return=True)
    def handle_start_choice(self, choice):
        """Обработка выбора интерфейса."""
        if choice == '1':
            self.use_state_machine_menu = False
            logger.info("Выбран классический режим меню")
            return True
        elif choice == '2':
            self.use_state_machine_menu = True
            logger.info("Выбран автоматный режим меню")
            return True
        elif choice == '3':
            self.handle_exit()
            return False
        else:
            print(Messages.Format.error(Messages.Errors.INVALID_CHOICE))
            return True

    @FunctionLogger('controller')
    def display_main_menu(self):
        """Главное меню."""
        print(f"\n{Messages.General.SEPARATOR}")
        print(Messages.General.MENU_TITLE)
        print(Messages.General.SEPARATOR)

        for option in Messages.Menu.MAIN_OPTIONS:
            print(option)

        print(Messages.General.SEPARATOR)

    @FunctionLogger('controller')
    @exception_handler(default_return=False)
    def handle_menu_choice(self, choice):
        """Обработка выбора в меню."""
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
        """Выбор задания."""
        print(Messages.Format.subsection("ВЫБОР ЗАДАНИЯ"))

        for task_num, description in Messages.Menu.TASK_DESCRIPTIONS.items():
            print(f"{task_num}. {description}")

        try:
            choice = input(f"\n{Messages.Menu.TASK_SELECTION} ").strip()
            task_number = int(choice)

            if task_number not in [1, 3, 8]:
                raise ValueError("Допустимые задания: 1, 3, 8")

            task_name = self.task_service.select_task(task_number)
            print(Messages.Format.success(f"Выбрано задание {task_number}: {task_name}"))

        except Exception as e:
            print(Messages.Format.error(str(e)))

        return True

    @FunctionLogger('controller')
    @exception_handler(default_return=True)
    def handle_data_input(self):
        """Ввод данных."""
        print(Messages.Format.subsection("ВВОД ДАННЫХ"))

        try:
            if not self.task_service.current_task:
                print(Messages.Format.error("Сначала выберите задание (пункт 1)"))
                return True

            task_number = self.task_service.current_task

            if task_number == 1:
                return self._handle_task1_data_input()
            elif task_number == 3:
                return self._handle_task3_data_input()
            elif task_number == 8:
                return self._handle_task8_data_input()
            else:
                print(Messages.Format.error("Неизвестное задание"))
                return True

        except Exception as e:
            exception_manager.handle(e, 'data_input')
            print(Messages.Format.error(str(e)))

        return True

    def _handle_task1_data_input(self):
        """Ввод данных для задания 1."""
        print("\n" + Messages.Tasks.Task1.DESCRIPTION)

        print(f"\n{Messages.Menu.INPUT_METHOD}")
        for option in Messages.Menu.INPUT_OPTIONS:
            print(option)

        choice = input("\nВаш выбор (1-2): ").strip()
        self.validation_service.validate_choice(choice, "способ ввода", ['1', '2'])

        is_random = (choice == '2')

        if is_random:
            print("\n[Генерация случайных массивов]")

            size = self._get_validated_input(
                Messages.Tasks.Task1.SIZE_PROMPT,
                'размер массивов',
                min_val=1,
                allow_float=False
            )

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

            import random
            arr1 = [random.randint(min_val, max_val) for _ in range(size)]
            arr2 = [random.randint(min_val, max_val) for _ in range(size)]

            print(f"\n✓ Сгенерированы массивы:")
            print(f"  Массив 1 ({size} элементов): {Messages.Format.array_display(arr1)}")
            print(f"  Массив 2 ({size} элементов): {Messages.Format.array_display(arr2)}")

            data = (arr1, arr2)
            self.task_service.set_task_data(data)
            print(Messages.Format.success(Messages.Success.DATA_SAVED))

        else:
            print("\n[Ручной ввод массивов]")

            size = self._get_validated_input(
                Messages.Tasks.Task1.SIZE_PROMPT,
                'размер массивов',
                min_val=1,
                allow_float=False
            )

            print(f"\n--- Первый массив ({size} элементов) ---")
            arr1 = []
            for i in range(size):
                while True:
                    try:
                        val = input(f"Элемент {i+1}: ").strip()
                        if '.' in val:
                            num = float(val)
                        else:
                            num = int(val)
                        arr1.append(num)
                        break
                    except Exception as e:
                        print(f"Ошибка: {e}. Попробуйте снова.")

            print(f"\n--- Второй массив ({size} элементов) ---")
            arr2 = []
            for i in range(size):
                while True:
                    try:
                        val = input(f"Элемент {i+1}: ").strip()
                        if '.' in val:
                            num = float(val)
                        else:
                            num = int(val)
                        arr2.append(num)
                        break
                    except Exception as e:
                        print(f"Ошибка: {e}. Попробуйте снова.")

            print(f"\n✓ Введены массивы:")
            print(f"  Массив 1: {Messages.Format.array_display(arr1)}")
            print(f"  Массив 2: {Messages.Format.array_display(arr2)}")

            data = (arr1, arr2)
            self.task_service.set_task_data(data)
            print(Messages.Format.success(Messages.Success.DATA_SAVED))

        return True

    def _handle_task3_data_input(self):
        """Ввод данных для задания 3."""
        print("\n" + Messages.Tasks.Task3.DESCRIPTION)

        print(f"\n{Messages.Menu.INPUT_METHOD}")
        for option in Messages.Menu.INPUT_OPTIONS:
            print(option)

        choice = input("\nВаш выбор (1-2): ").strip()
        self.validation_service.validate_choice(choice, "способ ввода", ['1', '2'])

        is_random = (choice == '2')

        if is_random:
            print("\n[Генерация случайной матрицы]")

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

            import random
            matrix = [
                [random.randint(min_val, max_val) for _ in range(cols)]
                for _ in range(rows)
            ]

            print(f"\n✓ Сгенерирована матрица {rows}x{cols}:")
            print(Messages.Format.matrix_display(matrix))

            data = matrix
            self.task_service.set_task_data(data)
            print(Messages.Format.success(Messages.Success.DATA_SAVED))

        else:
            print("\n[Ручной ввод матрицы]")

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

            data = matrix
            self.task_service.set_task_data(data)
            print(Messages.Format.success(Messages.Success.DATA_SAVED))

        return True

    def _handle_task8_data_input(self):
        """Ввод данных для задания 8."""
        print("\n" + Messages.Tasks.Task8.DESCRIPTION)

        print(f"\n{Messages.Menu.INPUT_METHOD}")
        for option in Messages.Menu.INPUT_OPTIONS:
            print(option)

        choice = input("\nВаш выбор (1-2): ").strip()
        self.validation_service.validate_choice(choice, "способ ввода", ['1', '2'])

        is_random = (choice == '2')

        if is_random:
            print("\n[Генерация случайных массивов]")

            size = self._get_validated_input(
                Messages.Tasks.Task8.SIZE_PROMPT,
                'размер массивов',
                min_val=1,
                allow_float=False
            )

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

            import random
            arr1 = [random.randint(min_val, max_val) for _ in range(size)]
            arr2 = [random.randint(min_val, max_val) for _ in range(size)]

            print(f"\n✓ Сгенерированы массивы:")
            print(f"  Массив 1 ({size} элементов): {Messages.Format.array_display(arr1)}")
            print(f"  Массив 2 ({size} элементов): {Messages.Format.array_display(arr2)}")

            data = (arr1, arr2)
            self.task_service.set_task_data(data)
            print(Messages.Format.success(Messages.Success.DATA_SAVED))

        else:
            print("\n[Ручной ввод массивов]")

            print(f"\n--- Первый массив ---")
            arr1 = []
            print("Введите элементы первого массива (пустая строка для завершения):")
            while True:
                val = input("Элемент: ").strip()
                if val == "":
                    if len(arr1) == 0:
                        print("Массив не может быть пустым")
                        continue
                    break
                try:
                    if '.' in val:
                        num = float(val)
                    else:
                        num = int(val)
                    arr1.append(num)
                except Exception as e:
                    print(f"Ошибка: {e}. Попробуйте снова.")

            print(f"\n--- Второй массив ---")
            arr2 = []
            print("Введите элементы второго массива (пустая строка для завершения):")
            while True:
                val = input("Элемент: ").strip()
                if val == "":
                    if len(arr2) == 0:
                        print("Массив не может быть пустым")
                        continue
                    break
                try:
                    if '.' in val:
                        num = float(val)
                    else:
                        num = int(val)
                    arr2.append(num)
                except Exception as e:
                    print(f"Ошибка: {e}. Попробуйте снова.")

            print(f"\n✓ Введены массивы:")
            print(f"  Массив 1 ({len(arr1)} элементов): {Messages.Format.array_display(arr1)}")
            print(f"  Массив 2 ({len(arr2)} элементов): {Messages.Format.array_display(arr2)}")

            data = (arr1, arr2)
            self.task_service.set_task_data(data)
            print(Messages.Format.success(Messages.Success.DATA_SAVED))

        return True

    def _get_validated_input(self, prompt, field_name, **constraints):
        """
        Получение и валидация ввода пользователя.
        """
        while True:
            try:
                value = input(prompt).strip()
                self.validation_service.validate_not_empty(value, field_name)

                allow_float = constraints.get('allow_float', True)
                number = self.validation_service.validate_number(
                    value, field_name, allow_float
                )

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
        """Выполнение алгоритма."""
        print(Messages.Format.subsection("ВЫПОЛНЕНИЕ АЛГОРИТМА"))

        try:
            if not self.task_service.has_data():
                print(Messages.Format.error("Сначала введите данные (пункт 2)"))
                return True

            kwargs = {}
            if self.task_service.current_task == 3:
                print(Messages.Tasks.Task3.ROTATION_PROMPT)
                print("1. По часовой стрелке")
                print("2. Против часовой стрелки")

                choice = input("\nВаш выбор (1-2): ").strip()
                self.validation_service.validate_choice(choice, "направление", ['1', '2'])

                kwargs['direction'] = 'clockwise' if choice == '1' else 'counterclockwise'

            result = self.task_service.execute_task(**kwargs)

            if result is not None:
                self.task_service.task_result = result
                print(Messages.Format.success(Messages.Success.ALGORITHM_EXECUTED))

        except Exception as e:
            exception_manager.handle(e, 'algorithm_execution')
            print(Messages.Format.error(str(e)))

        return True

    @FunctionLogger('controller')
    @exception_handler(default_return=True)
    def handle_result_display(self):
        """Отображение результата."""
        print(Messages.Format.subsection("ВЫВОД РЕЗУЛЬТАТА"))

        try:
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
    def handle_exit(self):
        """Выход из приложения."""
        print(Messages.Format.subsection(Messages.General.EXIT_MESSAGE))

        confirm = input(Messages.General.CONFIRM_EXIT).lower()

        if confirm in Messages.General.CONFIRM_YES:
            self.is_running = False
            print(Messages.Format.success(Messages.General.THANKS))
            logger.info("Приложение завершает работу")
        else:
            print("Продолжение работы...")

        return self.is_running

    def run_classic_menu(self):
        """Классическое меню."""
        logger.info("Запущен классический режим меню")

        while self.is_running:
            try:
                self.display_main_menu()
                choice = input("\nВыберите пункт меню (1-6): ").strip()
                logger.info(f"Пользователь выбрал: {choice}")
                self.is_running = self.handle_menu_choice(choice)

            except KeyboardInterrupt:
                logger.warning("Программа прервана пользователем")
                self.is_running = self.handle_exit()
            except Exception as e:
                logger.exception(f"Критическая ошибка: {e}")
                print(Messages.Format.error(f"{Messages.General.CRITICAL_ERROR}: {e}"))
                exception_manager.handle(e, 'main_loop')

    def run_state_machine_menu(self):
        """Автоматное меню."""
        logger.info("Запущен автоматный режим меню")
        self.menu_manager.start()

        print("\n" + "=" * 60)
        print("↩️  ВОЗВРАТ В СТАРТОВОЕ МЕНЮ")
        print("=" * 60)

    def run(self):
        """Основной цикл."""
        logger.info("=" * 60)
        logger.info("ЗАПУСК ПРИЛОЖЕНИЯ")
        logger.info("=" * 60)

        print(f"\n{Messages.General.SEPARATOR}")
        print(Messages.General.APP_TITLE)
        print("Версия с поддержкой автоматного программирования")
        print(Messages.General.SEPARATOR)

        while self.is_running:
            try:
                self.display_start_menu()
                choice = input("\n👉 Выберите режим (1-3): ").strip()
                logger.info(f"Пользователь выбрал режим: {choice}")

                should_continue = self.handle_start_choice(choice)

                if not should_continue:
                    break

                if self.use_state_machine_menu:
                    self.run_state_machine_menu()
                else:
                    self.run_classic_menu()

            except KeyboardInterrupt:
                logger.warning("Программа прервана пользователем")
                self.is_running = self.handle_exit()
            except Exception as e:
                logger.exception(f"Критическая ошибка: {e}")
                print(Messages.Format.error(f"{Messages.General.CRITICAL_ERROR}: {e}"))
                exception_manager.handle(e, 'main_loop')

        logger.info("Приложение завершило работу")
        print(f"\n{Messages.General.GOODBYE}")

def main():
    """Точка входа."""
    try:
        app = ApplicationController()
        app.run()
    except Exception as e:
        print(f"💥 Фатальная ошибка: {e}")
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
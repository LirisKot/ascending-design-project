"""
МОДУЛЬ ИСКЛЮЧЕНИЙ И ОШИБОК
==========================

Кастомные исключения для различных сценариев приложения.
Обеспечивают точную диагностику ошибок и корректную обработку.
"""

from utils.logger import get_logger

logger = get_logger('exceptions')


class AppBaseException(Exception):
    """Базовое исключение приложения с логированием."""

    def __init__(self, message, user_message=None, log_level='error'):
        """
        Инициализация исключения.

        Параметры:
        ----------
        message : str
            Техническое сообщение для логирования
        user_message : str or None
            Сообщение для пользователя (если None, используется message)
        log_level : str
            Уровень логирования ('debug', 'info', 'warning', 'error', 'critical')
        """
        self.message = message
        self.user_message = user_message or message
        self.log_level = log_level.lower()

        # Логируем исключение при создании
        self._log_exception()

        super().__init__(self.message)

    def _log_exception(self):
        """Логирование исключения при его создании."""
        log_method = getattr(logger, self.log_level, logger.error)
        log_method(f"СОЗДАНО ИСКЛЮЧЕНИЕ {self.__class__.__name__}: {self.message}")


# ============================================================================
# ИСКЛЮЧЕНИЯ ВАЛИДАЦИИ
# ============================================================================

class ValidationError(AppBaseException):
    """Базовое исключение для ошибок валидации."""

    def __init__(self, message, field=None, value=None, user_message=None):
        """
        Инициализация ошибки валидации.

        Параметры:
        ----------
        message : str
            Техническое сообщение об ошибке
        field : str or None
            Поле, в котором произошла ошибка
        value : any or None
            Значение, вызвавшее ошибку
        user_message : str or None
            Сообщение для пользователя
        """
        self.field = field
        self.value = value

        # Формируем детальное сообщение
        detailed_message = message
        if field:
            detailed_message += f" (поле: {field})"
        if value is not None:
            detailed_message += f" (значение: {value})"

        super().__init__(detailed_message, user_message, 'warning')


class ArraySizeError(ValidationError):
    """Ошибка размера массива."""

    def __init__(self, expected_size, actual_size, array_name="массив"):
        message = f"Неверный размер {array_name}: ожидалось {expected_size}, получено {actual_size}"
        user_message = f"{array_name.capitalize()} должен содержать {expected_size} элементов"
        super().__init__(message, 'size', actual_size, user_message)


class NumberRangeError(ValidationError):
    """Ошибка диапазона чисел."""

    def __init__(self, value, min_val, max_val, field_name="значение"):
        message = f"{field_name} {value} вне диапазона [{min_val}, {max_val}]"
        user_message = f"Введите {field_name} от {min_val} до {max_val}"
        super().__init__(message, field_name, value, user_message)


class MatrixDimensionError(ValidationError):
    """Ошибка размерности матрицы."""

    def __init__(self, expected_rows, expected_cols, actual_rows, actual_cols):
        message = f"Неверные размеры матрицы: ожидалось {expected_rows}x{expected_cols}, получено {actual_rows}x{actual_cols}"
        user_message = f"Матрица должна быть размером {expected_rows}x{expected_cols}"
        super().__init__(message, 'dimensions', f"{actual_rows}x{actual_cols}", user_message)


class DataTypeError(ValidationError):
    """Ошибка типа данных."""

    def __init__(self, expected_type, actual_type, field_name="данные"):
        message = f"Неверный тип {field_name}: ожидался {expected_type}, получен {actual_type}"
        user_message = f"Введите {field_name} правильного типа ({expected_type})"
        super().__init__(message, 'type', actual_type, user_message)


# ============================================================================
# ИСКЛЮЧЕНИЯ АЛГОРИТМОВ
# ============================================================================

class AlgorithmError(AppBaseException):
    """Базовое исключение для ошибок выполнения алгоритмов."""

    def __init__(self, algorithm_name, message, user_message=None):
        """
        Инициализация ошибки алгоритма.

        Параметры:
        ----------
        algorithm_name : str
            Название алгоритма
        message : str
            Техническое сообщение об ошибке
        user_message : str or None
            Сообщение для пользователя
        """
        self.algorithm_name = algorithm_name
        full_message = f"Алгоритм '{algorithm_name}': {message}"
        user_message = user_message or f"Ошибка выполнения алгоритма '{algorithm_name}'"
        super().__init__(full_message, user_message, 'error')


class AlgorithmExecutionError(AlgorithmError):
    """Ошибка выполнения алгоритма."""

    def __init__(self, algorithm_name, step=None, details=None):
        message = f"Ошибка на шаге выполнения"
        if step:
            message += f" (шаг: {step})"
        if details:
            message += f": {details}"
        user_message = f"Ошибка при выполнении алгоритма"
        super().__init__(algorithm_name, message, user_message)


class AlgorithmDataError(AlgorithmError):
    """Ошибка данных для алгоритма."""

    def __init__(self, algorithm_name, data_description, issue):
        message = f"Некорректные данные: {data_description} - {issue}"
        user_message = f"Некорректные данные для алгоритма"
        super().__init__(algorithm_name, message, user_message)


# ============================================================================
# ИСКЛЮЧЕНИЯ ПОЛЬЗОВАТЕЛЬСКОГО ВВОДА
# ============================================================================

class InputError(AppBaseException):
    """Базовое исключение для ошибок ввода."""

    def __init__(self, input_type, message, user_message=None):
        """
        Инициализация ошибки ввода.

        Параметры:
        ----------
        input_type : str
            Тип ввода ('manual', 'file', 'generated')
        message : str
            Техническое сообщение об ошибке
        user_message : str or None
            Сообщение для пользователя
        """
        self.input_type = input_type
        full_message = f"Ошибка ввода ({input_type}): {message}"
        user_message = user_message or "Ошибка при вводе данных"
        super().__init__(full_message, user_message, 'warning')


class UserInputError(InputError):
    """Ошибка ручного ввода пользователя."""

    def __init__(self, field_name, value, expected_format):
        message = f"Некорректный ввод для поля '{field_name}': '{value}'"
        user_message = f"Введите '{field_name}' в формате: {expected_format}"
        super().__init__('manual', message, user_message)


class FileInputError(InputError):
    """Ошибка чтения файла."""

    def __init__(self, filename, issue):
        message = f"Ошибка чтения файла '{filename}': {issue}"
        user_message = f"Ошибка при чтении файла {filename}"
        super().__init__('file', message, user_message)


# ============================================================================
# ИСКЛЮЧЕНИЯ СОСТОЯНИЯ ПРИЛОЖЕНИЯ
# ============================================================================

class StateError(AppBaseException):
    """Ошибка состояния приложения."""

    def __init__(self, current_state, required_state, operation):
        message = f"Невозможно выполнить '{operation}' в состоянии '{current_state}'"
        user_message = f"Сначала выполните: {required_state}"
        super().__init__(message, user_message, 'warning')


class NoTaskSelectedError(StateError):
    """Ошибка: задание не выбрано."""

    def __init__(self, operation):
        super().__init__("задание не выбрано", "выбор задания", operation)


class NoDataEnteredError(StateError):
    """Ошибка: данные не введены."""

    def __init__(self, operation):
        super().__init__("данные не введены", "ввод данных", operation)


class AlgorithmNotExecutedError(StateError):
    """Ошибка: алгоритм не выполнен."""

    def __init__(self, operation):
        super().__init__("алгоритм не выполнен", "выполнение алгоритма", operation)


# ============================================================================
# ДЕКОРАТОРЫ ДЛЯ ОБРАБОТКИ ИСКЛЮЧЕНИЙ
# ============================================================================

def handle_app_exceptions(default_return=None, log_level='error'):
    """
    Декоратор для обработки исключений приложения.

    Параметры:
    ----------
    default_return : any
        Значение, возвращаемое при возникновении исключения
    log_level : str
        Уровень логирования исключения

    Возвращает:
    -----------
    decorator
        Декоратор функции
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except AppBaseException as e:
                # Исключения приложения логируются при создании
                # Возвращаем значение по умолчанию
                return default_return
            except Exception as e:
                # Логируем неожиданные исключения
                logger_method = getattr(logger, log_level, logger.error)
                logger_method(
                    f"НЕОЖИДАННОЕ ИСКЛЮЧЕНИЕ в {func.__name__}: "
                    f"{type(e).__name__}: {str(e)}"
                )
                return default_return

        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        return wrapper

    return decorator


def safe_execute(func, *args, **kwargs):
    """
    Безопасное выполнение функции с обработкой исключений.

    Параметры:
    ----------
    func : callable
        Функция для выполнения
    *args, **kwargs
        Аргументы функции

    Возвращает:
    -----------
    tuple
        (success: bool, result: any or None, error: Exception or None)
    """
    try:
        result = func(*args, **kwargs)
        return True, result, None
    except AppBaseException as e:
        # Исключения приложения уже залогированы
        return False, None, e
    except Exception as e:
        logger.error(f"Неожиданная ошибка в {func.__name__}: {e}")
        return False, None, e
"""
СИСТЕМА ИСКЛЮЧЕНИЙ ПРИЛОЖЕНИЯ
==============================

Иерархия кастомных исключений с централизованным управлением сообщениями.
Разделение по категориям для точной диагностики ошибок.
"""

from utils.messages import Messages
from utils.logger import get_logger

logger = get_logger('exceptions')


# ============================================================================
# БАЗОВЫЕ КЛАССЫ ИСКЛЮЧЕНИЙ
# ============================================================================

class AppException(Exception):
    """
    Базовое исключение приложения.

    Содержит техническое сообщение для логирования и
    пользовательское сообщение для отображения.
    """

    def __init__(self, tech_message, user_message=None, log_level='error',
                 context=None, details=None):
        """
        Инициализация исключения.

        Args:
            tech_message: Техническое сообщение для логирования
            user_message: Сообщение для пользователя
            log_level: Уровень логирования
            context: Контекст возникновения ошибки
            details: Детали ошибки
        """
        self.tech_message = tech_message
        self.user_message = user_message or tech_message
        self.log_level = log_level.lower()
        self.context = context
        self.details = details

        # Формируем полное сообщение
        full_message = tech_message
        if context:
            full_message = f"[{context}] {full_message}"
        if details:
            full_message += f" (детали: {details})"

        super().__init__(full_message)

        # Автоматическое логирование
        self._log_exception()

    def _log_exception(self):
        """Логирование исключения при создании."""
        log_method = getattr(logger, self.log_level, logger.error)
        log_method(f"ИСКЛЮЧЕНИЕ {self.__class__.__name__}: {self.tech_message}")

    def __str__(self):
        """Строковое представление для пользователя."""
        return self.user_message

    def to_dict(self):
        """Представление исключения в виде словаря для логирования."""
        return {
            'type': self.__class__.__name__,
            'tech_message': self.tech_message,
            'user_message': self.user_message,
            'context': self.context,
            'details': self.details,
            'log_level': self.log_level
        }


# ============================================================================
# ИСКЛЮЧЕНИЯ ВАЛИДАЦИИ
# ============================================================================

class ValidationException(AppException):
    """Базовое исключение для ошибок валидации."""

    def __init__(self, field=None, value=None, expected=None, **kwargs):
        self.field = field
        self.value = value
        self.expected = expected

        # Формируем сообщение
        if 'tech_message' not in kwargs:
            kwargs['tech_message'] = f"Ошибка валидации поля '{field}'"
            if value is not None:
                kwargs['tech_message'] += f": значение '{value}'"
            if expected:
                kwargs['tech_message'] += f", ожидалось: {expected}"

        if 'user_message' not in kwargs:
            kwargs['user_message'] = Messages.Errors.VALIDATION_ERROR

        kwargs.setdefault('log_level', 'warning')

        super().__init__(**kwargs)


class InputValidationException(ValidationException):
    """Исключение для ошибок валидации ввода."""

    def __init__(self, input_type='manual', **kwargs):
        self.input_type = input_type
        kwargs.setdefault('context', f'input_validation_{input_type}')
        super().__init__(**kwargs)


class DataValidationException(ValidationException):
    """Исключение для ошибок валидации данных."""

    def __init__(self, data_type=None, **kwargs):
        self.data_type = data_type
        kwargs.setdefault('context', f'data_validation_{data_type or "unknown"}')
        super().__init__(**kwargs)


# ============================================================================
# КОНКРЕТНЫЕ ИСКЛЮЧЕНИЯ ВАЛИДАЦИИ
# ============================================================================

class EmptyInputException(InputValidationException):
    """Исключение для пустого ввода."""

    def __init__(self, field, **kwargs):
        tech_msg = f"Пустой ввод для поля '{field}'"
        user_msg = f"{Messages.Errors.EMPTY_INPUT}: '{field}'"

        super().__init__(
            field=field,
            tech_message=tech_msg,
            user_message=user_msg,
            expected="непустое значение",
            **kwargs
        )


class InvalidNumberException(InputValidationException):
    """Исключение для некорректного числа."""

    def __init__(self, field, value, **kwargs):
        tech_msg = f"Некорректное число для поля '{field}': '{value}'"
        user_msg = f"{Messages.Errors.INVALID_NUMBER} для '{field}'"

        super().__init__(
            field=field,
            value=value,
            tech_message=tech_msg,
            user_message=user_msg,
            expected="корректное число",
            **kwargs
        )


class InvalidChoiceException(InputValidationException):
    """Исключение для неверного выбора."""

    def __init__(self, field, value, valid_choices, **kwargs):
        tech_msg = f"Неверный выбор для '{field}': '{value}'"
        user_msg = f"{Messages.Errors.INVALID_CHOICE}. Доступно: {valid_choices}"

        super().__init__(
            field=field,
            value=value,
            tech_message=tech_msg,
            user_message=user_msg,
            expected=f"один из {valid_choices}",
            **kwargs
        )


class ArraySizeException(DataValidationException):
    """Исключение для ошибки размера массива."""

    def __init__(self, expected, actual, array_name="массив", **kwargs):
        tech_msg = f"Неверный размер {array_name}: ожидалось {expected}, получено {actual}"
        user_msg = f"{Messages.Errors.ARRAY_SIZE_MISMATCH}: {array_name} должен иметь размер {expected}"

        super().__init__(
            field='size',
            value=actual,
            tech_message=tech_msg,
            user_message=user_msg,
            expected=f"размер {expected}",
            data_type='array',
            **kwargs
        )


class MatrixDimensionException(DataValidationException):
    """Исключение для ошибки размерности матрицы."""

    def __init__(self, expected_rows, expected_cols, actual_rows, actual_cols, **kwargs):
        tech_msg = f"Неверные размеры матрицы: ожидалось {expected_rows}x{expected_cols}, получено {actual_rows}x{actual_cols}"
        user_msg = f"{Messages.Errors.MATRIX_DIMENSION_INVALID}: требуется {expected_rows}x{expected_cols}"

        super().__init__(
            field='dimensions',
            value=f"{actual_rows}x{actual_cols}",
            tech_message=tech_msg,
            user_message=user_msg,
            expected=f"{expected_rows}x{expected_cols}",
            data_type='matrix',
            **kwargs
        )


class ValueRangeException(DataValidationException):
    """Исключение для значения вне диапазона."""

    def __init__(self, field, value, min_val, max_val, **kwargs):
        tech_msg = f"Значение '{value}' вне диапазона [{min_val}, {max_val}] для поля '{field}'"
        user_msg = f"{Messages.Errors.VALUE_OUT_OF_RANGE} для '{field}': от {min_val} до {max_val}"

        super().__init__(
            field=field,
            value=value,
            tech_message=tech_msg,
            user_message=user_msg,
            expected=f"значение в [{min_val}, {max_val}]",
            **kwargs
        )


# ============================================================================
# ИСКЛЮЧЕНИЯ СОСТОЯНИЯ ПРИЛОЖЕНИЯ
# ============================================================================

class StateException(AppException):
    """Базовое исключение для ошибок состояния приложения."""

    def __init__(self, current_state, required_state, operation, **kwargs):
        self.current_state = current_state
        self.required_state = required_state
        self.operation = operation

        tech_msg = f"Невозможно выполнить '{operation}' в состоянии '{current_state}'"
        user_msg = f"Сначала выполните: {required_state}"

        kwargs.setdefault('log_level', 'warning')
        kwargs.setdefault('context', 'state_error')

        super().__init__(tech_msg, user_msg, **kwargs)


class NoTaskSelectedException(StateException):
    """Исключение при попытке операции без выбранного задания."""

    def __init__(self, operation, **kwargs):
        super().__init__(
            current_state="задание не выбрано",
            required_state="выбор задания",
            operation=operation,
            **kwargs
        )


class NoDataEnteredException(StateException):
    """Исключение при попытке операции без введенных данных."""

    def __init__(self, operation, **kwargs):
        super().__init__(
            current_state="данные не введены",
            required_state="ввод данных",
            operation=operation,
            **kwargs
        )


class AlgorithmNotExecutedException(StateException):
    """Исключение при попытке операции без выполненного алгоритма."""

    def __init__(self, operation, **kwargs):
        super().__init__(
            current_state="алгоритм не выполнен",
            required_state="выполнение алгоритма",
            operation=operation,
            **kwargs
        )


# ============================================================================
# ИСКЛЮЧЕНИЯ АЛГОРИТМОВ
# ============================================================================

class AlgorithmException(AppException):
    """Базовое исключение для ошибок алгоритмов."""

    def __init__(self, algorithm_name, step=None, **kwargs):
        self.algorithm_name = algorithm_name
        self.step = step

        tech_msg = f"Ошибка в алгоритме '{algorithm_name}'"
        if step:
            tech_msg += f" на шаге '{step}'"

        user_msg = Messages.Errors.ALGORITHM_EXECUTION_ERROR

        kwargs.setdefault('log_level', 'error')
        kwargs.setdefault('context', f'algorithm_{algorithm_name}')

        super().__init__(tech_msg, user_msg, **kwargs)


class AlgorithmExecutionException(AlgorithmException):
    """Исключение при ошибке выполнения алгоритма."""

    def __init__(self, algorithm_name, step=None, error_details=None, **kwargs):
        self.error_details = error_details

        if error_details and 'details' not in kwargs:
            kwargs['details'] = error_details

        super().__init__(algorithm_name, step, **kwargs)


class AlgorithmDataException(AlgorithmException):
    """Исключение при ошибке данных для алгоритма."""

    def __init__(self, algorithm_name, data_description, issue, **kwargs):
        tech_msg = f"Некорректные данные для алгоритма '{algorithm_name}': {data_description} - {issue}"
        user_msg = Messages.Errors.ALGORITHM_DATA_ERROR

        kwargs['tech_message'] = tech_msg
        kwargs['user_message'] = user_msg

        super().__init__(algorithm_name, **kwargs)


# ============================================================================
# ИСКЛЮЧЕНИЯ ФАЙЛОВОЙ СИСТЕМЫ
# ============================================================================

class FileSystemException(AppException):
    """Базовое исключение для ошибок файловой системы."""

    def __init__(self, operation, path=None, **kwargs):
        self.operation = operation
        self.path = path

        tech_msg = f"Ошибка при {operation}"
        if path:
            tech_msg += f" пути '{path}'"

        kwargs.setdefault('log_level', 'error')
        kwargs.setdefault('context', 'file_system')

        super().__init__(tech_msg, **kwargs)


class FileReadException(FileSystemException):
    """Исключение при ошибке чтения файла."""

    def __init__(self, filename, issue, **kwargs):
        super().__init__(
            operation="чтении файла",
            path=filename,
            details=issue,
            **kwargs
        )


class FileWriteException(FileSystemException):
    """Исключение при ошибке записи в файл."""

    def __init__(self, filename, issue, **kwargs):
        super().__init__(
            operation="записи в файл",
            path=filename,
            details=issue,
            **kwargs
        )


# ============================================================================
# ДЕКОРАТОРЫ И УТИЛИТЫ ДЛЯ ОБРАБОТКИ ИСКЛЮЧЕНИЙ
# ============================================================================

def exception_handler(default_return=None, log_unhandled=True):
    """
    Декоратор для обработки исключений в функциях.

    Args:
        default_return: Значение, возвращаемое при возникновении исключения
        log_unhandled: Логировать ли необработанные исключения
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except AppException as e:
                # Исключения приложения уже залогированы
                return default_return
            except Exception as e:
                if log_unhandled:
                    logger.error(
                        f"НЕОБРАБОТАННОЕ ИСКЛЮЧЕНИЕ в {func.__name__}: "
                        f"{type(e).__name__}: {str(e)}"
                    )
                return default_return

        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        return wrapper

    return decorator


def safe_execute(func, *args, error_return=None, **kwargs):
    """
    Безопасное выполнение функции с обработкой исключений.

    Args:
        func: Функция для выполнения
        error_return: Значение, возвращаемое при ошибке
        *args, **kwargs: Аргументы функции

    Returns:
        tuple: (success, result, exception)
    """
    try:
        result = func(*args, **kwargs)
        return True, result, None
    except AppException as e:
        return False, error_return, e
    except Exception as e:
        logger.error(f"Неожиданная ошибка в {func.__name__}: {e}")
        return False, error_return, e


class ExceptionManager:
    """Менеджер для централизованного управления исключениями."""

    def __init__(self):
        self.error_history = []
        self.logger = get_logger('exception_manager')

    def handle(self, exception, context=None):
        """
        Обработка исключения с сохранением в истории.

        Args:
            exception: Исключение для обработки
            context: Контекст возникновения

        Returns:
            dict: Информация об обработанном исключении
        """
        error_info = {
            'timestamp': self.logger.get_now(),
            'type': type(exception).__name__,
            'message': str(exception),
            'context': context,
            'details': exception.to_dict() if hasattr(exception, 'to_dict') else None
        }

        self.error_history.append(error_info)

        # Ограничиваем размер истории
        if len(self.error_history) > 100:
            self.error_history = self.error_history[-50:]

        self.logger.debug(f"Исключение обработано: {error_info}")
        return error_info

    def get_error_history(self, limit=10):
        """Получение истории ошибок."""
        return self.error_history[-limit:] if limit else self.error_history

    def clear_history(self):
        """Очистка истории ошибок."""
        self.error_history.clear()
        self.logger.info("История ошибок очищена")

    def get_last_error(self):
        """Получение последней ошибки."""
        return self.error_history[-1] if self.error_history else None


# Глобальный менеджер исключений
exception_manager = ExceptionManager()
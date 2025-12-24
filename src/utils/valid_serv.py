"""
СЕРВИС ВАЛИДАЦИИ
================

Отдельный сервис для проверки данных.
Отделяет логику валидации от обработки исключений.
"""

from utils.messages import Messages
from utils.exceptions import (
    EmptyInputException, InvalidNumberException, InvalidChoiceException,
    ArraySizeException, MatrixDimensionException, ValueRangeException
)
from utils.logger import get_logger

logger = get_logger('validation_service')


class ValidationService:
    """Сервис для валидации различных типов данных."""

    @staticmethod
    def validate_not_empty(value, field_name):
        """
        Проверка, что значение не пустое.

        Args:
            value: Значение для проверки
            field_name: Название поля

        Raises:
            EmptyInputException: Если значение пустое
        """
        if not value and value != 0:
            raise EmptyInputException(field=field_name)
        logger.debug(f"Поле '{field_name}' не пустое")

    @staticmethod
    def validate_number(value, field_name, allow_float=True):
        """
        Проверка, что значение является числом.

        Args:
            value: Значение для проверки
            field_name: Название поля
            allow_float: Разрешать ли вещественные числа

        Returns:
            int or float: Преобразованное число

        Raises:
            InvalidNumberException: Если значение не число
        """
        try:
            if allow_float:
                num = float(value)
                if num.is_integer():
                    num = int(num)
            else:
                num = int(value)

            logger.debug(f"Поле '{field_name}' содержит корректное число: {num}")
            return num

        except (ValueError, TypeError):
            raise InvalidNumberException(field=field_name, value=value)

    @staticmethod
    def validate_choice(value, field_name, valid_choices):
        """
        Проверка, что значение есть в списке допустимых.

        Args:
            value: Значение для проверки
            field_name: Название поля
            valid_choices: Список допустимых значений

        Raises:
            InvalidChoiceException: Если значение не в списке
        """
        if value not in valid_choices:
            raise InvalidChoiceException(
                field=field_name,
                value=value,
                valid_choices=valid_choices
            )
        logger.debug(f"Поле '{field_name}': значение '{value}' допустимо")

    @staticmethod
    def validate_array_size(array, expected_size, array_name="массив"):
        """
        Проверка размера массива.

        Args:
            array: Массив для проверки
            expected_size: Ожидаемый размер
            array_name: Название массива для сообщений

        Raises:
            ArraySizeException: Если размер не соответствует
        """
        actual_size = len(array)
        if actual_size != expected_size:
            raise ArraySizeException(
                expected=expected_size,
                actual=actual_size,
                array_name=array_name
            )
        logger.debug(f"Массив '{array_name}' имеет корректный размер: {expected_size}")

    @staticmethod
    def validate_matrix_dimensions(matrix, min_rows=1, min_cols=1):
        """
        Проверка размеров матрицы.

        Args:
            matrix: Матрица для проверки
            min_rows: Минимальное количество строк
            min_cols: Минимальное количество столбцов

        Returns:
            tuple: (rows, cols) - размеры матрицы

        Raises:
            MatrixDimensionException: Если размеры не корректны
        """
        if not matrix or not isinstance(matrix, list):
            raise MatrixDimensionException(
                expected_rows=min_rows,
                expected_cols=min_cols,
                actual_rows=0,
                actual_cols=0
            )

        rows = len(matrix)
        if rows < min_rows:
            raise MatrixDimensionException(
                expected_rows=min_rows,
                expected_cols=min_cols,
                actual_rows=rows,
                actual_cols=0
            )

        if not matrix[0] or not isinstance(matrix[0], list):
            raise MatrixDimensionException(
                expected_rows=min_rows,
                expected_cols=min_cols,
                actual_rows=rows,
                actual_cols=0
            )

        cols = len(matrix[0])
        if cols < min_cols:
            raise MatrixDimensionException(
                expected_rows=min_rows,
                expected_cols=min_cols,
                actual_rows=rows,
                actual_cols=cols
            )

        # Проверяем, что все строки одинаковой длины
        for i, row in enumerate(matrix):
            if len(row) != cols:
                raise MatrixDimensionException(
                    expected_rows=rows,
                    expected_cols=cols,
                    actual_rows=rows,
                    actual_cols=len(row)
                )

        logger.debug(f"Матрица имеет корректные размеры: {rows}x{cols}")
        return rows, cols

    @staticmethod
    def validate_value_range(value, field_name, min_val=None, max_val=None):
        """
        Проверка, что значение в допустимом диапазоне.

        Args:
            value: Значение для проверки
            field_name: Название поля
            min_val: Минимальное значение
            max_val: Максимальное значение

        Raises:
            ValueRangeException: Если значение вне диапазона
        """
        if min_val is not None and value < min_val:
            raise ValueRangeException(
                field=field_name,
                value=value,
                min_val=min_val,
                max_val=max_val
            )

        if max_val is not None and value > max_val:
            raise ValueRangeException(
                field=field_name,
                value=value,
                min_val=min_val,
                max_val=max_val
            )

        logger.debug(f"Значение '{value}' в диапазоне [{min_val}, {max_val}]")
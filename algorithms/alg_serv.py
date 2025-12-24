"""
СЕРВИС ЗАДАНИЙ
==============

Сервис для управления заданиями и их выполнения.
Отделяет бизнес-логику заданий от UI.
"""

from utils.messages import Messages
from utils.exceptions import (
    AlgorithmExecutionException, AlgorithmDataException,
    NoTaskSelectedException, NoDataEnteredException
)
from utils.logger import get_logger, FunctionLogger
from services.validation_service import ValidationService

logger = get_logger('task_service')


class TaskService:
    """Сервис для управления и выполнения заданий."""

    def __init__(self):
        self.current_task = None
        self.task_data = None
        self.task_result = None
        self.validation_service = ValidationService()

    @FunctionLogger('task_service')
    def select_task(self, task_number):
        """
        Выбор задания для выполнения.

        Args:
            task_number: Номер задания (1, 3, 8)

        Returns:
            str: Название выбранного задания

        Raises:
            InvalidChoiceException: Если номер задания недопустим
        """
        # Валидация номера задания
        self.validation_service.validate_choice(
            task_number,
            'номер задания',
            [1, 3, 8]
        )

        self.current_task = task_number
        self.task_data = None
        self.task_result = None

        task_name = Messages.Menu.TASK_DESCRIPTIONS[task_number]
        logger.info(f"Выбрано задание: {task_name}")

        return task_name

    @FunctionLogger('task_service')
    def set_task_data(self, data):
        """
        Установка данных для текущего задания.

        Args:
            data: Данные для задания

        Returns:
            bool: True если данные установлены
        """
        if self.current_task is None:
            raise NoTaskSelectedException("установка данных")

        # Валидация данных в зависимости от задания
        if self.current_task in [1, 8]:
            self._validate_array_data(data)
        elif self.current_task == 3:
            self._validate_matrix_data(data)

        self.task_data = data
        logger.info(f"Данные для задания {self.current_task} установлены")
        return True

    def _validate_array_data(self, data):
        """Валидация данных для заданий с массивами."""
        if not isinstance(data, tuple) or len(data) != 2:
            raise AlgorithmDataException(
                algorithm_name=f"Задание {self.current_task}",
                data_description="входные данные",
                issue="ожидался кортеж из двух массивов"
            )

        arr1, arr2 = data
        self.validation_service.validate_array_size(arr1, len(arr1), "массив 1")
        self.validation_service.validate_array_size(arr2, len(arr2), "массив 2")

    def _validate_matrix_data(self, data):
        """Валидация данных для задания с матрицей."""
        self.validation_service.validate_matrix_dimensions(data)

    @FunctionLogger('task_service')
    def execute_task(self, **kwargs):
        """
        Выполнение текущего задания.

        Args:
            **kwargs: Дополнительные параметры для задания

        Returns:
            any: Результат выполнения задания

        Raises:
            NoTaskSelectedException: Если задание не выбрано
            NoDataEnteredException: Если данные не установлены
            AlgorithmExecutionException: Если ошибка выполнения
        """
        if self.current_task is None:
            raise NoTaskSelectedException("выполнение задания")

        if self.task_data is None:
            raise NoDataEnteredException("выполнение задания")

        try:
            if self.current_task == 1:
                result = self._execute_task1(**kwargs)
            elif self.current_task == 3:
                result = self._execute_task3(**kwargs)
            elif self.current_task == 8:
                result = self._execute_task8(**kwargs)
            else:
                raise AlgorithmExecutionException(
                    algorithm_name=f"Задание {self.current_task}",
                    error_details="неизвестный номер задания"
                )

            self.task_result = result
            logger.info(f"Задание {self.current_task} выполнено успешно")
            return result

        except Exception as e:
            # Преобразуем любую ошибку в AlgorithmExecutionException
            raise AlgorithmExecutionException(
                algorithm_name=f"Задание {self.current_task}",
                error_details=str(e)
            )

    def _execute_task1(self, **kwargs):
        """Выполнение задания 1: сумма массивов."""
        from algorithms.algorithm1 import sum_arrays_special

        arr1, arr2 = self.task_data
        return sum_arrays_special(arr1, arr2)

    def _execute_task3(self, direction='clockwise', **kwargs):
        """Выполнение задания 3: поворот матрицы."""
        from algorithms.algorithm3 import (
            rotate_clockwise, rotate_counterclockwise
        )

        if direction not in ['clockwise', 'counterclockwise']:
            direction = 'clockwise'

        if direction == 'clockwise':
            return rotate_clockwise(self.task_data)
        else:
            return rotate_counterclockwise(self.task_data)

    def _execute_task8(self, **kwargs):
        """Выполнение задания 8: поиск общих чисел."""
        from algorithms.algorithm8 import find_common_numbers

        arr1, arr2 = self.task_data
        return find_common_numbers(arr1, arr2)

    @FunctionLogger('task_service')
    def get_result_display(self):
        """
        Получение форматированного результата для отображения.

        Returns:
            str: Отформатированный результат

        Raises:
            AlgorithmNotExecutedException: Если задание не выполнено
        """
        if self.task_result is None:
            from utils.exceptions import AlgorithmNotExecutedException
            raise AlgorithmNotExecutedException("получение результата")

        if self.current_task == 1:
            return self._format_task1_result()
        elif self.current_task == 3:
            return self._format_task3_result()
        elif self.current_task == 8:
            return self._format_task8_result()

        return str(self.task_result)

    def _format_task1_result(self):
        """Форматирование результата для задания 1."""
        arr1, arr2 = self.task_data
        result = self.task_result

        display = Messages.Format.section(
            f"РЕЗУЛЬТАТ ЗАДАНИЯ 1: {Messages.Tasks.Task1.NAME}"
        )

        display += f"\nИсходные данные:\n"
        display += f"  Массив 1: {Messages.Format.array_display(arr1, 'Массив 1')}\n"
        display += f"  Массив 2: {Messages.Format.array_display(arr2, 'Массив 2')}\n"

        display += f"\nРезультат:\n"
        display += f"  {Messages.Tasks.Task1.RESULT_LABEL}: "
        display += f"{Messages.Format.array_display(result, Messages.Tasks.Task1.RESULT_LABEL)}"

        # Дополнительная информация
        zero_count = result.count(0) if result else 0
        display += f"\n\nАнализ:\n"
        display += f"  • Количество нулей: {zero_count}\n"
        display += f"  • Минимальное значение: {min(result) if result else 'N/A'}\n"
        display += f"  • Максимальное значение: {max(result) if result else 'N/A'}"

        return display

    def _format_task3_result(self):
        """Форматирование результата для задания 3."""
        matrix = self.task_data
        result = self.task_result

        display = Messages.Format.section(
            f"РЕЗУЛЬТАТ ЗАДАНИЯ 3: {Messages.Tasks.Task3.NAME}"
        )

        display += f"\nИсходная матрица:\n"
        display += Messages.Format.matrix_display(matrix, "Исходная матрица")

        display += f"\n\nРезультат:\n"
        display += Messages.Format.matrix_display(result, Messages.Tasks.Task3.RESULT_LABEL)

        return display

    def _format_task8_result(self):
        """Форматирование результата для задания 8."""
        arr1, arr2 = self.task_data
        result = self.task_result

        display = Messages.Format.section(
            f"РЕЗУЛЬТАТ ЗАДАНИЯ 8: {Messages.Tasks.Task8.NAME}"
        )

        display += f"\nИсходные данные:\n"
        display += f"  Массив 1: {Messages.Format.array_display(arr1, 'Массив 1')}\n"
        display += f"  Массив 2: {Messages.Format.array_display(arr2, 'Массив 2')}\n"

        display += f"\nРезультат:\n"
        display += f"  {Messages.Tasks.Task8.RESULT_LABEL}: "

        if result:
            display += f"{Messages.Format.array_display(result, Messages.Tasks.Task8.RESULT_LABEL)}\n"
            display += f"  • Найдено общих чисел: {len(result)}"
        else:
            display += "Общих чисел не найдено"

        return display
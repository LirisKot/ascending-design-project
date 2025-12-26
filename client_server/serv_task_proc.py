"""
ОБРАБОТЧИК ЗАДАЧ СЕРВЕРА
=======================

Выполняет вычисления и эмулирует длительные расчеты.
"""

import time
import random
import threading
from datetime import datetime
from typing import Any, Dict

from shared.protocols import TaskRequest, TaskResponse, TaskType
from server.server_logger import ServerLogger


class TaskProcessor:
    """Обработчик задач сервера."""

    def __init__(self, logger: ServerLogger):
        """
        Инициализация обработчика задач.

        Args:
            logger: Логгер сервера
        """
        self.logger = logger
        self.task_handlers = {
            TaskType.TASK1_SUM_ARRAYS: self._handle_task1,
            TaskType.TASK3_ROTATE_MATRIX: self._handle_task3,
            TaskType.TASK8_COMMON_NUMBERS: self._handle_task8,
            TaskType.GENERATE_ARRAY: self._handle_generate_array,
            TaskType.GENERATE_MATRIX: self._handle_generate_matrix,
            TaskType.VALIDATE_DATA: self._handle_validate_data
        }

        # Статистика выполнения задач
        self.stats = {
            'total_tasks': 0,
            'successful_tasks': 0,
            'failed_tasks': 0,
            'total_execution_time': 0
        }
        self.stats_lock = threading.Lock()

    def process_task(self, task_request: TaskRequest) -> TaskResponse:
        """
        Обработка задачи.

        Args:
            task_request: Запрос на выполнение задачи

        Returns:
            Ответ с результатом выполнения
        """
        start_time = time.time()

        try:
            self.logger.info(f"Обработка задачи: {task_request.task_type.value}")

            # Обновление статистики
            with self.stats_lock:
                self.stats['total_tasks'] += 1

            # Эмуляция длительных вычислений
            self._emulate_heavy_computation()

            # Выполнение задачи
            handler = self.task_handlers.get(task_request.task_type)
            if handler:
                result = handler(task_request.parameters)

                # Обновление статистики
                execution_time = time.time() - start_time
                with self.stats_lock:
                    self.stats['successful_tasks'] += 1
                    self.stats['total_execution_time'] += execution_time

                self.logger.info(f"Задача {task_request.task_type.value} выполнена за {execution_time:.2f}с")

                return TaskResponse(
                    success=True,
                    result=result,
                    error_message=None,
                    execution_time=execution_time
                )
            else:
                error_msg = f"Неизвестный тип задачи: {task_request.task_type}"
                self.logger.error(error_msg)

                with self.stats_lock:
                    self.stats['failed_tasks'] += 1

                return TaskResponse(
                    success=False,
                    result=None,
                    error_message=error_msg,
                    execution_time=time.time() - start_time
                )

        except Exception as e:
            error_msg = f"Ошибка выполнения задачи: {str(e)}"
            self.logger.error(error_msg)

            with self.stats_lock:
                self.stats['failed_tasks'] += 1

            return TaskResponse(
                success=False,
                result=None,
                error_message=error_msg,
                execution_time=time.time() - start_time
            )

    def _emulate_heavy_computation(self):
        """Эмуляция длительных вычислений."""
        # Случайная задержка от 1 до 3 секунд
        delay = random.uniform(1.0, 3.0)
        self.logger.debug(f"Эмуляция вычислений: задержка {delay:.2f}с")
        time.sleep(delay)

    def _handle_task1(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Обработка задачи 1: сумма массивов."""
        from algorithms.algorithm1 import sum_arrays_special

        arr1 = parameters['array1']
        arr2 = parameters['array2']

        self.logger.info(f"Выполнение задачи 1: массивы размера {len(arr1)} и {len(arr2)}")

        result = sum_arrays_special(arr1, arr2)

        return {
            'result': result,
            'input_size': len(arr1),
            'result_size': len(result)
        }

    def _handle_task3(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Обработка задачи 3: поворот матрицы."""
        from algorithms.algorithm3 import rotate_clockwise, rotate_counterclockwise

        matrix = parameters['matrix']
        direction = parameters.get('direction', 'clockwise')

        rows = len(matrix)
        cols = len(matrix[0]) if rows > 0 else 0

        self.logger.info(f"Выполнение задачи 3: матрица {rows}x{cols}, направление {direction}")

        if direction == 'clockwise':
            result = rotate_clockwise(matrix)
        else:
            result = rotate_counterclockwise(matrix)

        return {
            'result': result,
            'original_dimensions': f"{rows}x{cols}",
            'result_dimensions': f"{len(result)}x{len(result[0])}" if result else "0x0"
        }

    def _handle_task8(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Обработка задачи 8: поиск общих чисел."""
        from algorithms.algorithm8 import find_common_numbers

        arr1 = parameters['array1']
        arr2 = parameters['array2']

        self.logger.info(f"Выполнение задачи 8: массивы размера {len(arr1)} и {len(arr2)}")

        result = find_common_numbers(arr1, arr2)

        return {
            'result': result,
            'common_count': len(result),
            'input_sizes': [len(arr1), len(arr2)]
        }

    def _handle_generate_array(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Генерация случайного массива."""
        size = parameters.get('size', 10)
        min_val = parameters.get('min_val', 1)
        max_val = parameters.get('max_val', 100)

        self.logger.info(f"Генерация массива: размер {size}, диапазон [{min_val}, {max_val}]")

        import random
        array = [random.randint(min_val, max_val) for _ in range(size)]

        return {
            'array': array,
            'size': size,
            'min': min(array) if array else 0,
            'max': max(array) if array else 0
        }

    def _handle_generate_matrix(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Генерация случайной матрицы."""
        rows = parameters.get('rows', 3)
        cols = parameters.get('cols', 3)
        min_val = parameters.get('min_val', 1)
        max_val = parameters.get('max_val', 10)

        self.logger.info(f"Генерация матрицы: {rows}x{cols}, диапазон [{min_val}, {max_val}]")

        import random
        matrix = [
            [random.randint(min_val, max_val) for _ in range(cols)]
            for _ in range(rows)
        ]

        return {
            'matrix': matrix,
            'dimensions': f"{rows}x{cols}",
            'total_elements': rows * cols
        }

    def _handle_validate_data(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Валидация данных."""
        data_type = parameters.get('type', 'array')
        data = parameters.get('data', [])

        self.logger.info(f"Валидация данных типа {data_type}")

        if data_type == 'array':
            is_valid = isinstance(data, list) and all(isinstance(x, (int, float)) for x in data)
            return {
                'is_valid': is_valid,
                'data_type': 'array',
                'size': len(data) if is_valid else 0
            }

        elif data_type == 'matrix':
            is_valid = (
                    isinstance(data, list) and
                    all(isinstance(row, list) for row in data) and
                    all(isinstance(x, (int, float)) for row in data for x in row)
            )

            if is_valid and data:
                rows = len(data)
                cols = len(data[0]) if data[0] else 0
                consistent = all(len(row) == cols for row in data)
                is_valid = is_valid and consistent

            return {
                'is_valid': is_valid,
                'data_type': 'matrix',
                'rows': len(data) if is_valid and data else 0,
                'cols': len(data[0]) if is_valid and data and data[0] else 0
            }

        return {
            'is_valid': False,
            'data_type': data_type,
            'error': 'Неизвестный тип данных'
        }

    def get_stats(self) -> Dict[str, Any]:
        """Получение статистики выполнения задач."""
        with self.stats_lock:
            avg_time = (self.stats['total_execution_time'] / self.stats['total_tasks']
                        if self.stats['total_tasks'] > 0 else 0)

            return {
                **self.stats,
                'average_execution_time': avg_time,
                'success_rate': (self.stats['successful_tasks'] / self.stats['total_tasks'] * 100
                                 if self.stats['total_tasks'] > 0 else 0)
            }
"""
ОБРАБОТЧИК ЗАДАЧ СЕРВЕРА
=======================

Выполняет вычисления и эмулирует длительные расчеты.
"""

# 1. СНАЧАЛА импорты sys и os для настройки путей
import sys
import os

# Добавляем корень проекта в sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)  # Выходим из client_server в корень

# Важно: добавляем пути в правильном порядке
paths_to_add = [
    project_root,  # корень проекта
    os.path.join(project_root, 'algorithms'),  # папка algorithms
    os.path.join(project_root, 'utils'),  # папка utils
]

for path in paths_to_add:
    if os.path.exists(path) and path not in sys.path:
        sys.path.insert(0, path)

print(f"Пути Python после настройки (первые 5):")
for i, p in enumerate(sys.path[:5]):
    print(f"  {i + 1}. {p}")

# 2. ТЕПЕРЬ импортируем остальные модули
import time
import random
import threading
from datetime import datetime
from typing import Any, Dict

try:
    from protocols import TaskRequest, TaskResponse, TaskType
    from logger_serv import ServerLogger

    print("✓ Основные модули импортированы успешно")
except ImportError as e:
    print(f"✗ Ошибка импорта основных модулей: {e}")
    raise

# 3. Импортируем алгоритмы из правильных мест
try:
    print("\nИмпорт алгоритмов:")

    # Импортируем из algorithm1.py
    algorithm1_path = os.path.join(project_root, 'algorithms', 'algorithm1.py')
    if os.path.exists(algorithm1_path):
        import importlib.util
        spec = importlib.util.spec_from_file_location("algorithm1", algorithm1_path)
        algorithm1_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(algorithm1_module)

        # Получаем функцию sum_arrays_special
        if hasattr(algorithm1_module, 'sum_arrays_special'):
            sum_arrays_special = algorithm1_module.sum_arrays_special
            print("✓ algorithm1.sum_arrays_special импортирован")
        else:
            raise AttributeError("Функция sum_arrays_special не найдена в algorithm1.py")
    else:
        raise FileNotFoundError(f"Файл {algorithm1_path} не найден")

    # Импортируем из algorithm3.py (исправлено с algorithm8 на algorithm3)
    algorithm3_path = os.path.join(project_root, 'algorithms', 'algorithm3.py')
    if os.path.exists(algorithm3_path):
        import importlib.util
        spec = importlib.util.spec_from_file_location("algorithm3", algorithm3_path)
        algorithm3_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(algorithm3_module)

        # Пробуем получить функцию rotate_matrix_algorithm или main
        if hasattr(algorithm3_module, 'rotate_matrix_algorithm'):
            # Используем функцию-обертку из algorithm3.py
            rotate_matrix_algorithm = algorithm3_module.rotate_matrix_algorithm
            print("✓ algorithm3.rotate_matrix_algorithm импортирован")

            # Создаем обертки для rotate_clockwise и rotate_counterclockwise
            def rotate_clockwise(matrix):
                """Обертка для поворота по часовой стрелке"""
                return rotate_matrix_algorithm(matrix, direction='clockwise')

            def rotate_counterclockwise(matrix):
                """Обертка для поворота против часовой стрелки"""
                return rotate_matrix_algorithm(matrix, direction='counterclockwise')

        elif hasattr(algorithm3_module, 'main'):
            # Если есть функция main, импортируем rotate_matrix_algorithm из utils
            print("✓ algorithm3.main найден, импортируем функции поворота из utils")
            from utils.matrix_operations import rotate_clockwise, rotate_counterclockwise
        else:
            print("⚠ В algorithm3.py не найдена rotate_matrix_algorithm, импортируем из utils")
            from utils.matrix_operations import rotate_clockwise, rotate_counterclockwise
    else:
        raise FileNotFoundError(f"Файл {algorithm3_path} не найден")

    # Импортируем из algorithm8.py
    algorithm3_path = os.path.join(project_root, 'algorithms', 'algorithm3.py')
    if os.path.exists(algorithm3_path):
        import importlib.util
        spec = importlib.util.spec_from_file_location("algorithm3", algorithm3_path)
        algorithm3_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(algorithm3_module)

        # Получаем функцию find_common_numbers
        if hasattr(algorithm3_module, 'find_common_numbers'):
            find_common_numbers = algorithm3_module.find_common_numbers
            print("✓ algorithm8.find_common_numbers импортирован")
        else:
            # Проверяем разные варианты имен
            for attr_name in ['find_common_numbers', 'main', 'find_common_elements']:
                if hasattr(algorithm3_module, attr_name):
                    find_common_numbers = getattr(algorithm3_module, attr_name)
                    print(f"✓ algorithm8.{attr_name} импортирован")
                    break
            else:
                raise AttributeError("Не найдена функция find_common_numbers в algorithm3.py")
    else:
        raise FileNotFoundError(f"Файл {algorithm3_path} не найден")

    # Если rotate_clockwise и rotate_counterclockwise еще не определены, импортируем из utils
    if 'rotate_clockwise' not in locals() or 'rotate_counterclockwise' not in locals():
        from utils.matrix_operations import rotate_clockwise, rotate_counterclockwise
        print("✓ Функции поворота матрицы импортированы из utils.matrix_operations")
    else:
        print("✓ Функции поворота матрицы созданы из algorithm3")

    # Функции сортировки - простые реализации
    def sort_array_desc(arr):
        return sorted(arr, reverse=True)

    def sort_array_asc(arr):
        return sorted(arr)

    print("✓ Функции сортировки созданы")

except Exception as e:
    print(f"✗ Ошибка импорта алгоритмов: {e}")
    import traceback
    traceback.print_exc()
    print("Создаем полные реализации алгоритмов...")

    # СОЗДАЕМ ПОЛНЫЕ РЕАЛИЗАЦИИ, А НЕ ЗАГЛУШКИ!

    def sum_arrays_special(arr1, arr2):
        """Алгоритм 1: Сумма массивов с разной сортировкой"""
        if not arr1 or not arr2:
            return []

        # 1. Первый массив сортируется по убыванию
        sorted_arr1 = sorted(arr1, reverse=True)

        # 2. Второй массив сортируется по возрастанию
        sorted_arr2 = sorted(arr2)

        # 3. Если числа равны, сумма = 0
        result = []
        for a, b in zip(sorted_arr1, sorted_arr2):
            if a == b:
                result.append(0)
            else:
                result.append(a + b)

        # 4. Итоговый массив сортируется по возрастанию
        return sorted(result)

    def rotate_clockwise(matrix):
        """Алгоритм 3: Поворот матрицы по часовой стрелке"""
        if not matrix:
            return []

        rows = len(matrix)
        cols = len(matrix[0])

        # Создаем новую матрицу с перевернутыми размерами
        rotated = [[0 for _ in range(rows)] for _ in range(cols)]

        # Реальная реализация поворота
        for i in range(rows):
            for j in range(cols):
                rotated[j][rows - 1 - i] = matrix[i][j]

        return rotated

    def rotate_counterclockwise(matrix):
        """Алгоритм 3: Поворот матрицы против часовой стрелки"""
        if not matrix:
            return []

        rows = len(matrix)
        cols = len(matrix[0])

        # Создаем новую матрицу с перевернутыми размерами
        rotated = [[0 for _ in range(rows)] for _ in range(cols)]

        # Реальная реализация поворота
        for i in range(rows):
            for j in range(cols):
                rotated[cols - 1 - j][i] = matrix[i][j]

        return rotated

    def find_common_numbers(arr1, arr2):
        """Алгоритм 8: Поиск общих чисел"""
        if not arr1 or not arr2:
            return []

        # Преобразуем в множества для поиска пересечений
        set1 = set(arr1)
        set2 = set(arr2)

        # Находим общие элементы
        common = set1.intersection(set2)

        # Для каждого числа проверяем его перевернутую версию
        result = set()
        for num in arr1:
            # Преобразуем число в строку и переворачиваем
            str_num = str(num)
            reversed_str = str_num[::-1]

            # Пытаемся преобразовать обратно в число
            try:
                reversed_num = int(reversed_str)
            except ValueError:
                try:
                    reversed_num = float(reversed_str)
                except ValueError:
                    continue

            # Проверяем, есть ли перевернутое число во втором массиве
            if reversed_num in set2:
                result.add(num)

        # Добавляем обычные общие числа
        result.update(common)

        return sorted(list(result))

    def sort_array_desc(arr):
        """Сортировка по убыванию"""
        return sorted(arr, reverse=True)

    def sort_array_asc(arr):
        """Сортировка по возрастанию"""
        return sorted(arr)

    print("✓ Созданы полные реализации всех алгоритмов")


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
        arr1 = parameters['array1']
        arr2 = parameters['array2']

        self.logger.info(f"Выполнение задачи 1: массивы размера {len(arr1)} и {len(arr2)}")

        result = sum_arrays_special(arr1, arr2)

        # Добавляем отладочную информацию
        self.logger.debug(f"Массив 1: {arr1[:5]}...")
        self.logger.debug(f"Массив 2: {arr2[:5]}...")
        self.logger.debug(f"Результат: {result[:5]}...")

        return {
            'result': result,
            'input_size': len(arr1),
            'result_size': len(result),
            'first_5_elements': result[:5] if len(result) > 5 else result
        }

    def _handle_task3(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Обработка задачи 3: поворот матрицы."""
        matrix = parameters['matrix']
        direction = parameters.get('direction', 'clockwise')

        rows = len(matrix)
        cols = len(matrix[0]) if rows > 0 else 0

        self.logger.info(f"Выполнение задачи 3: матрица {rows}x{cols}, направление {direction}")

        # Добавляем отладочную информацию
        self.logger.debug(f"Исходная матрица (первые 2 строки):")
        for i in range(min(2, rows)):
            self.logger.debug(f"  Строка {i}: {matrix[i]}")

        self.logger.debug(f"Вызываем rotate_clockwise: {direction == 'clockwise'}")

        if direction == 'clockwise':
            result = rotate_clockwise(matrix)
            self.logger.debug(f"Поворот по часовой стрелке")
        else:
            result = rotate_counterclockwise(matrix)
            self.logger.debug(f"Поворот против часовой стрелки")

        # Проверяем размеры результата
        if result:
            result_rows = len(result)
            result_cols = len(result[0]) if result_rows > 0 else 0
            self.logger.debug(f"Размер результата: {result_rows}x{result_cols}")
            self.logger.debug(f"Первая строка результата: {result[0] if result_rows > 0 else 'нет'}")

            # Сравниваем с исходной матрицей
            if result_rows == cols and result_cols == rows:
                self.logger.debug("✓ Размеры матрицы правильно изменились")
            else:
                self.logger.warning(f"⚠ Неожиданные размеры: было {rows}x{cols}, стало {result_rows}x{result_cols}")
        else:
            self.logger.debug(f"Результат: пустая матрица")

        return {
            'result': result,
            'original_dimensions': f"{rows}x{cols}",
            'result_dimensions': f"{len(result)}x{len(result[0])}" if result and result[0] else "0x0",
            'direction': direction,
            'original_first_row': matrix[0] if rows > 0 else [],
            'result_first_row': result[0] if result and len(result) > 0 else []
        }

    def _handle_task8(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Обработка задачи 8: поиск общих чисел."""
        arr1 = parameters['array1']
        arr2 = parameters['array2']

        self.logger.info(f"Выполнение задачи 8: массивы размера {len(arr1)} и {len(arr2)}")

        result = find_common_numbers(arr1, arr2)

        # Добавляем отладочную информацию
        self.logger.debug(f"Массив 1 (первые 5): {arr1[:5]}...")
        self.logger.debug(f"Массив 2 (первые 5): {arr2[:5]}...")
        self.logger.debug(f"Найдено общих чисел: {len(result)}")

        return {
            'result': result,
            'common_count': len(result),
            'input_sizes': [len(arr1), len(arr2)],
            'common_numbers_sample': result[:5] if len(result) > 5 else result
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
            'max': max(array) if array else 0,
            'sample': array[:5] if len(array) > 5 else array
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
            'total_elements': rows * cols,
            'first_row': matrix[0] if rows > 0 else []
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
                'size': len(data) if is_valid else 0,
                'sample': data[:3] if is_valid and len(data) > 3 else (data if is_valid else [])
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
                'cols': len(data[0]) if is_valid and data and data[0] else 0,
                'first_row': data[0] if is_valid and data else []
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
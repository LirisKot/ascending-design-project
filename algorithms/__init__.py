# algorithms/__init__.py
import sys
import os

# Добавляем корень проекта в sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Импортируем из utils
try:
    from utils.array_operations import sort_array_desc, sort_array_asc

    HAS_UTILS = True
except ImportError as e:
    print(f"Ошибка импорта из utils: {e}")
    HAS_UTILS = False


    # Создаем заглушки если не работает
    def sort_array_desc(arr):
        return sorted(arr, reverse=True)


    def sort_array_asc(arr):
        return sorted(arr)

# Экспортируем функции алгоритмов
try:
    from .algorithm1 import sum_arrays_special
    from .algorithm3 import rotate_clockwise, rotate_counterclockwise
    from .algorithm8 import find_common_numbers

    ALGORITHMS_IMPORTED = True
except ImportError as e:
    print(f"Ошибка импорта алгоритмов: {e}")
    ALGORITHMS_IMPORTED = False


    # Создаем заглушки для алгоритмов
    def sum_arrays_special(arr1, arr2):
        return [a + b for a, b in zip(arr1, arr2)]


    def rotate_clockwise(matrix):
        return matrix


    def rotate_counterclockwise(matrix):
        return matrix


    def find_common_numbers(arr1, arr2):
        return list(set(arr1) & set(arr2))

__all__ = [
    'sum_arrays_special',
    'rotate_clockwise',
    'rotate_counterclockwise',
    'find_common_numbers',
    'sort_array_desc',
    'sort_array_asc'
]

# Экспортируем только если импорт был успешным
if ALGORITHMS_IMPORTED and HAS_UTILS:
    print("✓ Все модули успешно импортированы в algorithms.__init__.py")
elif not ALGORITHMS_IMPORTED:
    print("⚠ Используются заглушки алгоритмов")
elif not HAS_UTILS:
    print("⚠ Используются заглушки utils функций")
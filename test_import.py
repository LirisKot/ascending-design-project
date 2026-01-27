# test_import.py в корне проекта
import sys

sys.path.append('.')  # Добавляем текущую директорию в путь

try:
    from algorithms.algorithm1 import sum_arrays_special

    print("✓ Успешный импорт из algorithms.algorithm1")

    # Тест функции
    arr1 = [1, 2, 3]
    arr2 = [4, 5, 6]
    result = sum_arrays_special(arr1, arr2)
    print(f"✓ Функция работает. Результат: {result}")

except ImportError as e:
    print(f"✗ Ошибка импорта: {e}")
    print("Текущий путь Python:")
    for p in sys.path:
        print(f"  {p}")
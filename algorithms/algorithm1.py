"""
Алгоритм 1: Сумма массивов с разной сортировкой
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.array_operations import sort_array_desc, sort_array_asc
from utils.input_operations import manual_input_array, generate_random_array


def sum_arrays_special(arr1, arr2):
    """
    Специальная сумма массивов по правилам варианта 1
    """
    if len(arr1) != len(arr2):
        raise ValueError(f"Массивы разного размера: {len(arr1)} != {len(arr2)}")

    sorted1 = sort_array_desc(arr1)  # по убыванию
    sorted2 = sort_array_asc(arr2)  # по возрастанию

    result = []
    for a, b in zip(sorted1, sorted2):
        if a == b:
            result.append(0)
        else:
            result.append(a + b)

    return sort_array_asc(result)


def main():
    print("=" * 50)
    print("АЛГОРИТМ 1: Сумма массивов с разной сортировкой")
    print("=" * 50)

    print("\nВыберите способ ввода данных:")
    print("1. Ввести массивы вручную")
    print("2. Сгенерировать случайные массивы")

    choice = input("Ваш выбор (1 или 2): ")

    if choice == "1":
        print("\n--- Ввод первого массива ---")
        arr1 = manual_input_array("Введите числа через пробел: ")

        print("\n--- Ввод второго массива ---")
        print(f"Второй массив должен иметь такой же размер ({len(arr1)})")
        arr2 = manual_input_array("Введите числа через пробел: ")

    elif choice == "2":
        size = int(input("Размер массивов: "))
        min_val = int(input("Минимальное значение: "))
        max_val = int(input("Максимальное значение: "))

        arr1 = generate_random_array(size, min_val, max_val)
        arr2 = generate_random_array(size, min_val, max_val)

        print(f"\nСгенерированный массив 1: {arr1}")
        print(f"Сгенерированный массив 2: {arr2}")
    else:
        print("Неверный выбор!")
        return

    print("\n" + "-" * 50)
    print("Выполнение алгоритма...")

    try:
        result = sum_arrays_special(arr1, arr2)

        print("\n" + "=" * 50)
        print("РЕЗУЛЬТАТ:")
        print(f"Исходный массив 1: {arr1}")
        print(f"Исходный массив 2: {arr2}")
        print(f"Результирующий массив: {result}")
        print("=" * 50)

    except Exception as e:
        print(f"\nОшибка: {e}")



# Экспорт функции для использования в main.py
if __name__ == "__main__":
    main()
else:
    # Экспортируем только основную функцию
    # main() не экспортируется, чтобы не запускалась автоматически
    pass
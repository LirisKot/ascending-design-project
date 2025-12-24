"""
Алгоритм 8: Поиск общих чисел в массивах
Вариант 8: Входные данные: 2 массива с числами.
Требуется проверить, сколько у массивов общих чисел.
Число считается общим, если оно входит в один массив,
а в другом массиве находится его перевернутая версия.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.input_operations import manual_input_array, generate_random_array
from utils.validation import validate_numbers_only


def find_common_numbers(arr1, arr2):
    """
    Находит общие числа с учетом перевернутых версий
    """
    common = set()

    # Проверяем, что массивы содержат только числа
    if not validate_numbers_only(arr1) or not validate_numbers_only(arr2):
        raise ValueError("Массивы должны содержать только числа")

    for num in arr1:
        # 1. Прямое совпадение
        if num in arr2:
            common.add(num)

        # 2. Совпадение с перевернутым числом (только для целых)
        if isinstance(num, int) and num >= 0:
            try:
                reversed_num = int(str(num)[::-1])
                if reversed_num in arr2:
                    common.add(num)
            except:
                pass

    return list(common)


def main():
    print("=" * 60)
    print("АЛГОРИТМ 8: Поиск общих чисел")
    print("=" * 60)

    print("\nПример: массивы [123, 456] и [321, 654]")
    print("имеют общие числа 123 и 456 (перевернутые версии)")

    arr1, arr2 = None, None

    print("\nВыберите способ ввода данных:")
    print("1. Ввести массивы вручную")
    print("2. Сгенерировать случайные массивы")

    choice = input("Ваш выбор (1 или 2): ")

    if choice == "1":
        print("\n--- Ввод первого массива ---")
        arr1 = manual_input_array("Введите числа через пробел: ")

        print("\n--- Ввод второго массива ---")
        arr2 = manual_input_array("Введите числа через пробел: ")

    elif choice == "2":
        size = int(input("Размер массивов: "))
        min_val = int(input("Минимальное значение (рекомендуется >= 10): "))
        max_val = int(input("Максимальное значение: "))

        arr1 = generate_random_array(size, min_val, max_val)
        arr2 = generate_random_array(size, min_val, max_val)

        print(f"\nСгенерированный массив 1: {arr1}")
        print(f"Сгенерированный массив 2: {arr2}")
    else:
        print("Неверный выбор!")
        return

    print("\n" + "-" * 60)
    print("Поиск общих чисел...")

    try:
        common_numbers = find_common_numbers(arr1, arr2)

        print("\n" + "=" * 60)
        print("РЕЗУЛЬТАТ:")
        print(f"Массив 1: {arr1}")
        print(f"Массив 2: {arr2}")
        print(f"Общие числа: {common_numbers}")
        print(f"Количество общих чисел: {len(common_numbers)}")

        if common_numbers:
            print("\nОбъяснение:")
            for num in common_numbers:
                if num in arr1 and num in arr2:
                    print(f"  {num} - прямое совпадение")
                else:
                    # Найдем перевернутую версию
                    for check_num in arr1:
                        if isinstance(check_num, int) and check_num >= 0:
                            reversed_num = int(str(check_num)[::-1])
                            if reversed_num in arr2:
                                print(f"  {check_num} - совпадает с {reversed_num} (перевернутая версия)")

        print("=" * 60)

    except Exception as e:
        print(f"\nОшибка: {e}")

# Экспорт функции для использования в main.py
if __name__ == "__main__":
    main()
else:
    # Экспортируем только основную функцию
    # main() не экспортируется, чтобы не запускалась автоматически
    pass
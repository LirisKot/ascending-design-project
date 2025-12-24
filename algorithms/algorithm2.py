"""
Алгоритм 3: Поворот матрицы на 90 градусов
Вариант 3: Входные данные: матрица N на M.
Требуется повернуть матрицу на 90 градусов против часовой или по часовой.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.input_operations import manual_input_array, generate_random_matrix, input_with_validation
from utils.matrix_operations import rotate_clockwise, rotate_counterclockwise, print_matrix


def main():
    print("=" * 60)
    print("АЛГОРИТМ 3: Поворот матрицы на 90 градусов")
    print("=" * 60)

    matrix = None

    print("\nВыберите способ ввода матрицы:")
    print("1. Ввести матрицу вручную")
    print("2. Сгенерировать случайную матрицу")

    choice = input("Ваш выбор (1 или 2): ")

    if choice == "1":
        print("\n--- Ручной ввод матрицы ---")
        rows = int(input("Количество строк: "))
        cols = int(input("Количество столбцов: "))

        print(f"\nВведите матрицу {rows}x{cols} (по строкам):")
        matrix = []
        for i in range(rows):
            while True:
                try:
                    row_input = input(f"Строка {i + 1} (числа через пробел): ")
                    row = [float(x) for x in row_input.split()]
                    if len(row) != cols:
                        print(f"Ошибка: нужно ввести ровно {cols} чисел")
                        continue
                    matrix.append(row)
                    break
                except ValueError:
                    print("Ошибка: вводите только числа!")

    elif choice == "2":
        print("\n--- Генерация случайной матрицы ---")
        rows = int(input("Количество строк: "))
        cols = int(input("Количество столбцов: "))
        min_val = int(input("Минимальное значение: "))
        max_val = int(input("Максимальное значение: "))

        matrix = generate_random_matrix(rows, cols, min_val, max_val)
    else:
        print("Неверный выбор!")
        return

    print("\n" + "-" * 60)
    print("Исходная матрица:")
    print_matrix(matrix)

    print("\nВыберите направление поворота:")
    print("1. По часовой стрелке")
    print("2. Против часовой стрелки")

    rotation_choice = input("Ваш выбор (1 или 2): ")

    print("\n" + "-" * 60)
    print("Выполнение поворота...")

    if rotation_choice == "1":
        result = rotate_clockwise(matrix)
        direction = "по часовой стрелке"
    elif rotation_choice == "2":
        result = rotate_counterclockwise(matrix)
        direction = "против часовой стрелки"
    else:
        print("Неверный выбор направления!")
        return

    print("\n" + "=" * 60)
    print("РЕЗУЛЬТАТ:")
    print(f"Матрица повернута {direction}:")
    print_matrix(result)
    print("=" * 60)


# Экспорт функции для использования в main.py
if __name__ == "__main__":
    main()
else:
    # Экспортируем только основную функцию
    # main() не экспортируется, чтобы не запускалась автоматически
    pass
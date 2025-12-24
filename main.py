"""
Главное меню приложения
Объединяет 3 алгоритма: 1 (сумма массивов), 3 (поворот матрицы), 8 (общие числа)
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from algorithms.algorithm1 import sum_arrays_special
from algorithms.algorithm3 import rotate_clockwise, rotate_counterclockwise
from algorithms.algorithm8 import find_common_numbers
from utils.input_operations import manual_input_array, generate_random_array, generate_random_matrix


class ApplicationState:
    """Класс для хранения состояния приложения"""

    def __init__(self):
        self.current_task = None  # 1, 3 или 8
        self.data = None  # Введенные данные
        self.result = None  # Результат выполнения
        self.data_entered = False  # Данные введены
        self.algorithm_executed = False  # Алгоритм выполнен

    def reset_for_new_data(self):
        """Сброс при вводе новых данных"""
        self.result = None
        self.algorithm_executed = False


def display_main_menu():
    """Отображение главного меню"""
    print("\n" + "=" * 60)
    print("ГЛАВНОЕ МЕНЮ КОНСОЛЬНОГО ПРИЛОЖЕНИЯ")
    print("=" * 60)
    print("1. Выбор задания (1, 3 или 8)")
    print("2. Ввод исходных данных")
    print("3. Выполнение алгоритма")
    print("4. Вывод результата")
    print("5. Завершение работы")
    print("=" * 60)


def select_task(state):
    """Пункт 1: Выбор задания"""
    print("\n--- ВЫБОР ЗАДАНИЯ ---")
    print("1. Сумма массивов с разной сортировкой")
    print("3. Поворот матрицы на 90 градусов")
    print("8. Поиск общих чисел с перевернутыми версиями")

    try:
        choice = int(input("Выберите номер задания (1, 3 или 8): "))
        if choice in [1, 3, 8]:
            state.current_task = choice
            state.reset_for_new_data()
            print(f"Выбрано задание {choice}")
        else:
            print("Неверный выбор! Доступны задания 1, 3, 8")
    except ValueError:
        print("Введите число!")


def input_data(state):
    """Пункт 2: Ввод исходных данных"""
    if state.current_task is None:
        print("Сначала выберите задание!")
        return

    print(f"\n--- ВВОД ДАННЫХ ДЛЯ ЗАДАНИЯ {state.current_task} ---")
    print("1. Ввести данные вручную")
    print("2. Сгенерировать случайные данные")

    try:
        choice = int(input("Ваш выбор (1 или 2): "))

        if choice == 1:
            # Ручной ввод
            if state.current_task == 1:
                print("\nВвод двух массивов одинакового размера:")
                size = int(input("Размер массивов: "))
                print("Первый массив:")
                arr1 = manual_input_array(f"Введите {size} чисел через пробел: ")
                if len(arr1) != size:
                    arr1 = arr1[:size] if len(arr1) > size else arr1 + [0] * (size - len(arr1))
                print("Второй массив:")
                arr2 = manual_input_array(f"Введите {size} чисел через пробел: ")
                if len(arr2) != size:
                    arr2 = arr2[:size] if len(arr2) > size else arr2 + [0] * (size - len(arr2))
                state.data = (arr1, arr2)

            elif state.current_task == 3:
                rows = int(input("Количество строк: "))
                cols = int(input("Количество столбцов: "))
                print(f"Введите матрицу {rows}x{cols} (по строкам):")
                matrix = []
                for i in range(rows):
                    row_input = input(f"Строка {i + 1}: ")
                    row = [float(x) for x in row_input.split()]
                    if len(row) != cols:
                        row = row[:cols] if len(row) > cols else row + [0] * (cols - len(row))
                    matrix.append(row)
                state.data = matrix

            elif state.current_task == 8:
                print("\nВвод двух массивов:")
                size = int(input("Размер массивов: "))
                print("Первый массив:")
                arr1 = manual_input_array(f"Введите {size} чисел через пробел: ")
                if len(arr1) != size:
                    arr1 = arr1[:size] if len(arr1) > size else arr1 + [0] * (size - len(arr1))
                print("Второй массив:")
                arr2 = manual_input_array(f"Введите {size} чисел через пробел: ")
                if len(arr2) != size:
                    arr2 = arr2[:size] if len(arr2) > size else arr2 + [0] * (size - len(arr2))
                state.data = (arr1, arr2)

        elif choice == 2:
            # Генерация
            if state.current_task == 1:
                size = int(input("Размер массивов: "))
                min_val = int(input("Минимальное значение: "))
                max_val = int(input("Максимальное значение: "))
                arr1 = generate_random_array(size, min_val, max_val)
                arr2 = generate_random_array(size, min_val, max_val)
                state.data = (arr1, arr2)
                print(f"Сгенерированы массивы:\n1: {arr1}\n2: {arr2}")

            elif state.current_task == 3:
                rows = int(input("Количество строк: "))
                cols = int(input("Количество столбцов: "))
                min_val = int(input("Минимальное значение: "))
                max_val = int(input("Максимальное значение: "))
                matrix = generate_random_matrix(rows, cols, min_val, max_val)
                state.data = matrix
                print(f"Сгенерирована матрица {rows}x{cols}")
                for row in matrix:
                    print(f"  {row}")

            elif state.current_task == 8:
                size = int(input("Размер массивов: "))
                min_val = int(input("Минимальное значение (рекомендуется ≥10): "))
                max_val = int(input("Максимальное значение: "))
                arr1 = generate_random_array(size, min_val, max_val)
                arr2 = generate_random_array(size, min_val, max_val)
                state.data = (arr1, arr2)
                print(f"Сгенерированы массивы:\n1: {arr1}\n2: {arr2}")

        state.data_entered = True
        state.reset_for_new_data()
        print("Данные сохранены!")

    except ValueError as e:
        print(f"Ошибка ввода: {e}")


def execute_algorithm(state):
    """Пункт 3: Выполнение алгоритма"""
    if state.current_task is None:
        print("Сначала выберите задание!")
        return

    if not state.data_entered:
        print("Сначала введите данные!")
        return

    print(f"\n--- ВЫПОЛНЕНИЕ АЛГОРИТМА {state.current_task} ---")

    try:
        if state.current_task == 1:
            arr1, arr2 = state.data
            state.result = sum_arrays_special(arr1, arr2)
            print("Алгоритм суммы массивов выполнен!")

        elif state.current_task == 3:
            matrix = state.data
            print("Выберите направление поворота:")
            print("1. По часовой стрелке")
            print("2. Против часовой стрелки")
            direction = int(input("Ваш выбор (1 или 2): "))

            if direction == 1:
                state.result = rotate_clockwise(matrix)
                print("Матрица повернута по часовой стрелке")
            elif direction == 2:
                state.result = rotate_counterclockwise(matrix)
                print("Матрица повернута против часовой стрелки")
            else:
                print("Неверный выбор направления!")
                return

        elif state.current_task == 8:
            arr1, arr2 = state.data
            state.result = find_common_numbers(arr1, arr2)
            print("Поиск общих чисел выполнен!")

        state.algorithm_executed = True
        print("Алгоритм успешно выполнен!")

    except Exception as e:
        print(f"Ошибка выполнения алгоритма: {e}")


def display_result(state):
    """Пункт 4: Вывод результата"""
    if not state.algorithm_executed:
        print("Сначала выполните алгоритм!")
        return

    print(f"\n--- РЕЗУЛЬТАТ ЗАДАНИЯ {state.current_task} ---")

    if state.current_task == 1:
        arr1, arr2 = state.data
        print(f"Исходный массив 1: {arr1}")
        print(f"Исходный массив 2: {arr2}")
        print(f"Результат (сумма с особыми правилами): {state.result}")

    elif state.current_task == 3:
        print("Исходная матрица:")
        for row in state.data:
            print(f"  {row}")
        print("Повернутая матрица:")
        for row in state.result:
            print(f"  {row}")

    elif state.current_task == 8:
        arr1, arr2 = state.data
        print(f"Массив 1: {arr1}")
        print(f"Массив 2: {arr2}")
        print(f"Общие числа: {state.result}")
        print(f"Количество общих чисел: {len(state.result)}")


def main():
    """Главная функция приложения"""
    state = ApplicationState()

    while True:
        display_main_menu()

        try:
            choice = int(input("Выберите пункт меню (1-5): "))

            if choice == 1:
                select_task(state)
            elif choice == 2:
                input_data(state)
            elif choice == 3:
                execute_algorithm(state)
            elif choice == 4:
                display_result(state)
            elif choice == 5:
                print("\nЗавершение работы...")
                print("Спасибо за использование программы!")
                break
            else:
                print("Неверный выбор! Введите число от 1 до 5")

        except ValueError:
            print("Пожалуйста, введите число!")
        except KeyboardInterrupt:
            print("\n\nПрограмма прервана пользователем")
            break
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")


if __name__ == "__main__":
    main()
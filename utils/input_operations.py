# utils/input_operations.py
import random


def manual_input_array(prompt="Введите числа через пробел: "):
    """Ручной ввод массива"""
    try:
        data = input(prompt)
        return [float(x) if '.' in x else int(x) for x in data.split()]
    except ValueError:
        print("Ошибка ввода! Пожалуйста, введите числа через пробел.")
        return []


def generate_random_array(size, min_val=0, max_val=100):
    """Генерация случайного массива"""
    # Преобразуем значения в целые числа
    size = int(size)
    min_val = int(min_val)
    max_val = int(max_val)

    return [random.randint(min_val, max_val) for _ in range(size)]


def generate_random_matrix(rows, cols, min_val=0, max_val=100):
    """Генерация случайной матрицы"""
    # Преобразуем значения в целые числа
    rows = int(rows)
    cols = int(cols)
    min_val = int(min_val)
    max_val = int(max_val)

    return [
        [random.randint(min_val, max_val) for _ in range(cols)]
        for _ in range(rows)
    ]


def input_with_validation(prompt, validator=None, error_message="Неверный ввод"):
    """
    Ввод с валидацией.

    Args:
        prompt: Подсказка для ввода
        validator: Функция для валидации (возвращает True/False)
        error_message: Сообщение об ошибке

    Returns:
        Введенное значение
    """
    while True:
        try:
            value = input(prompt)
            if validator is None or validator(value):
                return value
            else:
                print(error_message)
        except Exception as e:
            print(f"Ошибка: {e}")


# Тестирование
if __name__ == "__main__":
    # Тест генерации массива
    random_arr = generate_random_array(5, 1, 10)
    print("Сгенерированный массив:", random_arr)

    # Тест генерации матрицы
    random_matrix = generate_random_matrix(3, 4, 1, 20)
    print("\nСгенерированная матрица 3x4:")
    for row in random_matrix:
        print("  ", row)
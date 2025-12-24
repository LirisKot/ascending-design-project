import random


def manual_input_array(prompt="Введите числа через пробел: "):
    """Ручной ввод массива"""
    try:
        data = input(prompt)
        return [float(x) for x in data.split()]
    except ValueError:
        print("Ошибка ввода! Пожалуйста, введите числа через пробел.")
        return []


def generate_random_array(size, min_val=0, max_val=100):
    """Генерация случайного массива"""
    return [random.randint(min_val, max_val) for _ in range(size)]


# Тестирование
if __name__ == "__main__":
    # Тест ручного ввода (закомментировать для автоматических тестов)
    # arr = manual_input_array()
    # print("Введенный массив:", arr)

    # Тест генерации
    random_arr = generate_random_array(5, 1, 10)
    print("Сгенерированный массив:", random_arr)
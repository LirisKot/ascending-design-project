"""
Модуль валидации для конкретных заданий
Итерация 2: Проверки, нужные для заданий 1, 2, 8
"""


def validate_for_task1(arr1, arr2):
    """Валидация для задания 1"""
    # 1. Проверка размера
    if len(arr1) != len(arr2):
        raise ValueError(f"Для задания 1 массивы должны быть одинакового размера: {len(arr1)} != {len(arr2)}")

    # 2. Проверка, что не пустые
    if not arr1 or not arr2:
        raise ValueError("Массивы не должны быть пустыми")

    # 3. Проверка, что все элементы - числа
    for i, (a, b) in enumerate(zip(arr1, arr2)):
        if not (isinstance(a, (int, float)) and isinstance(b, (int, float))):
            raise ValueError(f"Элементы должны быть числами. Индекс {i}: {a}({type(a)}), {b}({type(b)})")

    return True


def validate_for_task2(arr1, arr2, arr3):
    """Валидация для задания 2"""
    sizes = {len(arr1), len(arr2), len(arr3)}
    if len(sizes) > 1:
        raise ValueError(f"Все три массива должны быть одинакового размера")
    return True


def validate_for_task8(arr1, arr2):
    """Валидация для задания 8"""
    # Для задания 8 массивы могут быть разного размера
    # Проверяем только что они не пустые
    if not arr1 or not arr2:
        raise ValueError("Оба массива не должны быть пустыми")
    return True


if __name__ == "__main__":
    print("Тест валидации для задания 1:")
    try:
        validate_for_task1([1, 2, 3], [4, 5, 6])
        print("✓ Валидация пройдена")
    except ValueError as e:
        print(f"✗ Ошибка: {e}")
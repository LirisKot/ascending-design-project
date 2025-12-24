"""
Модуль валидации данных
Итерация 2: Функции проверки входных данных
"""

def validate_arrays_equal_size(arr1, arr2, arr3=None):
    """
    Проверяет, что массивы одинакового размера
    Поддерживает 2 или 3 массива
    """
    sizes = [len(arr1), len(arr2)]
    if arr3 is not None:
        sizes.append(len(arr3))

    if len(set(sizes)) > 1:
        sizes_str = ", ".join(str(s) for s in sizes)
        raise ValueError(f"Массивы должны быть одинакового размера. Получены размеры: {sizes_str}")
    return True

def validate_array_not_empty(arr, name="массив"):
    """Проверяет, что массив не пустой"""
    if not arr:
        raise ValueError(f"{name} не должен быть пустым")
    return True

def validate_numeric_array(arr):
    """Проверяет, что все элементы массива - числа"""
    for i, item in enumerate(arr):
        if not isinstance(item, (int, float)):
            raise ValueError(f"Элемент {i} не является числом: {item}")
    return True

if __name__ == "__main__":
    print("=== Тестирование валидации ===")

    # Тест 1: Одинаковый размер
    try:
        validate_arrays_equal_size([1, 2], [3, 4])
        print("✓ Тест 1 пройден: массивы одинакового размера")
    except ValueError as e:
        print(f"✗ Тест 1 ошибка: {e}")

    # Тест 2: Непустой массив
    try:
        validate_array_not_empty([1, 2, 3], "Тестовый массив")
        print("✓ Тест 2 пройден: массив не пустой")
    except ValueError as e:
        print(f"✗ Тест 2 ошибка: {e}")

    # Тест 3: Числовой массив
    try:
        validate_numeric_array([1, 2.5, 3])
        print("✓ Тест 3 пройден: все элементы - числа")
    except ValueError as e:
        print(f"✗ Тест 3 ошибка: {e}")
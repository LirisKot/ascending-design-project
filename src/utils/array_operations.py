"""
Базовые операции с массивами
Итерация 1.1: Функции сортировки и объединения
"""


def sort_array_desc(arr):
    """Сортировка массива по убыванию"""
    return sorted(arr, reverse=True)


def sort_array_asc(arr):
    """Сортировка массива по возрастанию"""
    return sorted(arr)


def merge_arrays(arr1, arr2):
    """Объединение двух массивов"""
    return arr1 + arr2


if __name__ == "__main__":
    # Тестирование функций
    test_arr = [5, 2, 8, 1, 9]
    print("Тест сортировки по убыванию:", sort_array_desc(test_arr))
    print("Тест сортировки по возрастанию:", sort_array_asc(test_arr))

    arr1 = [1, 2, 3]
    arr2 = [4, 5, 6]
    print("Тест объединения:", merge_arrays(arr1, arr2))


def sort_array_desc(arr):
    """Сортировка массива по убыванию"""
    return sorted(arr, reverse=True)


def sort_array_asc(arr):
    """Сортировка массива по возрастанию"""
    return sorted(arr)


# === НОВЫЕ ФУНКЦИИ ДЛЯ КОММИТА 1.2 ===

def merge_arrays(arr1, arr2):
    """
    Объединение двух массивов
    Возвращает новый массив, содержащий все элементы обоих массивов
    """
    if not isinstance(arr1, list) or not isinstance(arr2, list):
        raise TypeError("Оба аргумента должны быть списками")
    return arr1 + arr2


def find_max(arr):
    """Находит максимальный элемент в массиве"""
    if not arr:
        raise ValueError("Массив не должен быть пустым")
    return max(arr)


def find_min(arr):
    """Находит минимальный элемент в массиве"""
    if not arr:
        raise ValueError("Массив не должен быть пустым")
    return min(arr)


def calculate_sum(arr):
    """Вычисляет сумму всех элементов массива"""
    return sum(arr)


if __name__ == "__main__":
    # Тестирование ВСЕХ функций
    print("=== Тестирование функций ===")

    test_arr = [5, 2, 8, 1, 9]
    arr1 = [1, 2, 3]
    arr2 = [4, 5, 6]

    # Существующие функции
    print("1. Сортировка по убыванию:", sort_array_desc(test_arr))
    print("2. Сортировка по возрастанию:", sort_array_asc(test_arr))

    # Новые функции
    print("3. Объединение массивов:", merge_arrays(arr1, arr2))
    print("4. Максимальный элемент:", find_max(test_arr))
    print("5. Минимальный элемент:", find_min(test_arr))
    print("6. Сумма элементов:", calculate_sum(test_arr))
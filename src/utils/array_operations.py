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
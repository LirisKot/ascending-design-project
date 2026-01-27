# client_server/local_utils.py
"""
Локальные утилиты для работы с массивами.
Используется когда основной utils недоступен.
"""

import random
import sys
import os


def sort_array_desc(arr):
    """Сортировка массива по убыванию."""
    return sorted(arr, reverse=True)


def sort_array_asc(arr):
    """Сортировка массива по возрастанию."""
    return sorted(arr)


def manual_input_array(prompt="Введите числа через пробел: "):
    """Ручной ввод массива."""
    try:
        data = input(prompt)
        values = data.strip().split()
        result = []
        for val in values:
            # Пробуем преобразовать в int, если не получается - в float
            try:
                result.append(int(val))
            except ValueError:
                try:
                    result.append(float(val))
                except ValueError:
                    print(f"Ошибка: '{val}' не является числом")
                    return []
        return result
    except Exception as e:
        print(f"Ошибка ввода: {e}")
        return []


def generate_random_array(size, min_val=0, max_val=100):
    """Генерация случайного массива."""
    try:
        # Преобразуем параметры в целые числа
        size = int(size)
        min_val = int(min_val)
        max_val = int(max_val)

        # Проверяем диапазон
        if min_val > max_val:
            min_val, max_val = max_val, min_val

        return [random.randint(min_val, max_val) for _ in range(size)]
    except ValueError as e:
        print(f"Ошибка параметров генерации: {e}")
        return [random.randint(1, 10) for _ in range(5)]  # значения по умолчанию
    except Exception as e:
        print(f"Ошибка генерации массива: {e}")
        return []


# Экспортируем все функции
__all__ = [
    'sort_array_desc',
    'sort_array_asc',
    'manual_input_array',
    'generate_random_array'
]
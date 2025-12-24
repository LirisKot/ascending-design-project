"""
Модуль для ввода и генерации данных
Итерация 3: Функции ввода данных
"""

import random
from typing import List, Union, Optional


def manual_input_array(prompt: str = "Введите числа через пробел: ") -> List[Union[int, float]]:
    """
    Ручной ввод массива чисел с клавиатуры

    Args:
        prompt: Сообщение для пользователя

    Returns:
        List[Union[int, float]]: Введенный массив чисел

    Examples:
        >>> manual_input_array("Введите числа: ")
        Введите числа: 1 2 3 4
        [1.0, 2.0, 3.0, 4.0]
    """
    try:
        user_input = input(prompt).strip()

        if not user_input:
            print("Ввод пуст. Возвращаю пустой массив.")
            return []

        numbers = []
        for item in user_input.split():
            # Пытаемся преобразовать в число
            try:
                # Сначала пробуем как целое число
                num = int(item)
            except ValueError:
                try:
                    # Потом как дробное
                    num = float(item)
                except ValueError:
                    print(f"⚠ Пропускаем нечисловое значение: '{item}'")
                    continue

            numbers.append(num)

        return numbers

    except KeyboardInterrupt:
        print("\n\n❌ Ввод прерван пользователем")
        return []
    except Exception as e:
        print(f"⚠ Ошибка при вводе: {e}")
        return []


def generate_random_array(
        size: int,
        min_val: int = 0,
        max_val: int = 100,
        allow_duplicates: bool = True
) -> List[int]:
    """
    Генерация случайного массива целых чисел

    Args:
        size: Размер массива
        min_val: Минимальное значение
        max_val: Максимальное значение
        allow_duplicates: Разрешить повторяющиеся значения

    Returns:
        List[int]: Сгенерированный массив

    Raises:
        ValueError: Если размер меньше 1 или min_val > max_val

    Examples:
        >>> generate_random_array(5, 1, 10)
        [3, 7, 2, 9, 5]
    """
    # Валидация входных параметров
    if size < 1:
        raise ValueError(f"Размер массива должен быть положительным, получено: {size}")

    if min_val > max_val:
        min_val, max_val = max_val, min_val
        print(f"⚠ Минимальное значение больше максимального. Меняю местами: min={min_val}, max={max_val}")

    if not allow_duplicates and (max_val - min_val + 1) < size:
        print(f"⚠ Нельзя создать {size} уникальных чисел в диапазоне [{min_val}, {max_val}]")
        print(f"  Разрешаю дубликаты для этого запроса")
        allow_duplicates = True

    if allow_duplicates:
        # С дубликатами
        return [random.randint(min_val, max_val) for _ in range(size)]
    else:
        # Без дубликатов
        possible_values = list(range(min_val, max_val + 1))
        if len(possible_values) < size:
            # Если уникальных значений меньше чем нужно
            return random.choices(possible_values, k=size)
        return random.sample(possible_values, size)


def generate_random_matrix(
        rows: int,
        cols: int,
        min_val: int = 0,
        max_val: int = 100
) -> List[List[int]]:
    """
    Генерация случайной матрицы (двумерного массива)

    Args:
        rows: Количество строк
        cols: Количество столбцов
        min_val: Минимальное значение элемента
        max_val: Максимальное значение элемента

    Returns:
        List[List[int]]: Сгенерированная матрица

    Examples:
        >>> generate_random_matrix(2, 3)
        [[5, 2, 8], [1, 9, 4]]
    """
    if rows < 1 or cols < 1:
        raise ValueError(f"Количество строк и столбцов должно быть положительным, получено: rows={rows}, cols={cols}")

    return [
        [random.randint(min_val, max_val) for _ in range(cols)]
        for _ in range(rows)
    ]


def input_with_validation(
        prompt: str,
        value_type: type = int,
        min_value: Optional[Union[int, float]] = None,
        max_value: Optional[Union[int, float]] = None
) -> Union[int, float]:
    """
    Ввод одного числа с валидацией

    Args:
        prompt: Сообщение для пользователя
        value_type: Тип числа (int или float)
        min_value: Минимальное допустимое значение
        max_value: Максимальное допустимое значение

    Returns:
        Введенное число

    Examples:
        >>> input_with_validation("Введите возраст: ", min_value=0, max_value=120)
    """
    while True:
        try:
            user_input = input(prompt).strip()

            # Преобразуем в нужный тип
            if value_type == int:
                value = int(user_input)
            elif value_type == float:
                value = float(user_input)
            else:
                raise ValueError(f"Неподдерживаемый тип: {value_type}")

            # Проверяем диапазон
            if min_value is not None and value < min_value:
                print(f"⚠ Значение должно быть не меньше {min_value}")
                continue

            if max_value is not None and value > max_value:
                print(f"⚠ Значение должно быть не больше {max_value}")
                continue

            return value

        except ValueError:
            type_name = "целое число" if value_type == int else "число"
            print(f"⚠ Пожалуйста, введите {type_name}")
        except KeyboardInterrupt:
            print("\n\n❌ Ввод прерван")
            raise


def display_array(arr: List[Union[int, float]], name: str = "Массив") -> None:
    """
    Красивое отображение массива

    Args:
        arr: Массив для отображения
        name: Название массива
    """
    if not arr:
        print(f"{name}: [] (пустой)")
        return

    print(f"{name} [{len(arr)} элементов]:")

    # Отображаем максимум 20 элементов
    display_limit = 20
    if len(arr) <= display_limit:
        print("  " + ", ".join(str(x) for x in arr))
    else:
        # Показываем первые и последние 5 элементов
        first_part = arr[:5]
        last_part = arr[-5:]
        print(f"  {', '.join(str(x) for x in first_part)}, ..., {', '.join(str(x) for x in last_part)}")
        print(f"  (показаны первые и последние 5 из {len(arr)} элементов)")


if __name__ == "__main__":
    print("=" * 60)
    print("ТЕСТИРОВАНИЕ МОДУЛЯ ВВОДА ДАННЫХ")
    print("=" * 60)

    # Тест 1: Генерация случайного массива
    print("\n1. Генерация случайного массива:")
    random_arr = generate_random_array(10, 1, 50)
    display_array(random_arr, "Случайный массив")

    # Тест 2: Генерация матрицы
    print("\n2. Генерация случайной матрицы 3x4:")
    matrix = generate_random_matrix(3, 4, 1, 10)
    for i, row in enumerate(matrix):
        print(f"  Строка {i + 1}: {row}")

    # Тест 3: Ручной ввод (закомментировать для автоматического тестирования)
    # print("\n3. Ручной ввод массива:")
    # print("   Попробуйте: 5 3.14 -2 100")
    # manual_arr = manual_input_array("Введите числа: ")
    # display_array(manual_arr, "Введенный массив")

    # Тест 4: Ввод с валидацией (закомментировать для автоматического тестирования)
    # print("\n4. Ввод с валидацией:")
    # print("   Попробуйте ввести число от 1 до 10")
    # validated = input_with_validation("Введите число от 1 до 10: ", min_value=1, max_value=10)
    # print(f"   Вы ввели: {validated}")

    # Тест 5: Генерация без дубликатов
    print("\n5. Генерация массива без дубликатов:")
    unique_arr = generate_random_array(10, 1, 20, allow_duplicates=False)
    display_array(unique_arr, "Массив без дубликатов")

    print("\n" + "=" * 60)
    print("ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
    print("=" * 60)
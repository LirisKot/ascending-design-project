# algorithms/algorithm1.py (добавь в начало)
import sys
import os

# Добавляем пути
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Пробуем импортировать utils, если не получается - используем локальные
try:
    from utils.logger import get_logger, FunctionLogger
    from utils.array_operations import sort_array_desc, sort_array_asc
    from utils.input_operations import manual_input_array, generate_random_array

    HAS_UTILS = True
    print("✓ Используются утилиты из utils")
except ImportError as e:
    print(f"⚠ Не удалось импортировать utils: {e}")
    print("⚠ Используются локальные утилиты")
    HAS_UTILS = False

    # Импортируем локальные утилиты из client_server
    try:
        sys.path.insert(0, os.path.join(project_root, 'client_server'))
        from local_utils import (
            sort_array_desc,
            sort_array_asc,
            manual_input_array,
            generate_random_array
        )

        print("✓ Локальные утилиты загружены")
    except ImportError:
        print("✗ Не удалось загрузить локальные утилиты")


        # Создаем минимальные заглушки
        def sort_array_desc(arr):
            return sorted(arr, reverse=True)


        def sort_array_asc(arr):
            return sorted(arr)


        def manual_input_array(prompt):
            return [1, 2, 3, 4, 5]


        def generate_random_array(size, min_val=0, max_val=100):
            import random
            size = int(size) if not isinstance(size, int) else size
            min_val = int(min_val) if not isinstance(min_val, int) else min_val
            max_val = int(max_val) if not isinstance(max_val, int) else max_val
            return [random.randint(min_val, max_val) for _ in range(size)]

# Создаем логгер
if HAS_UTILS:
    logger = get_logger('algorithm1')
else:
    # Заглушка для логгера
    class DummyLogger:
        def debug(self, msg): pass

        def info(self, msg): print(f"[INFO] {msg}")

        def error(self, msg): print(f"[ERROR] {msg}")

        def warning(self, msg): print(f"[WARNING] {msg}")


    logger = DummyLogger()

# Декоратор FunctionLogger (заглушка если нет настоящего)
if HAS_UTILS:
    FunctionLogger = FunctionLogger
else:
    class FunctionLogger:
        def __init__(self, name):
            self.name = name

        def __call__(self, func):
            return func


@FunctionLogger('algorithm1')
def sum_arrays_special(arr1, arr2):
    """
    Специальная сумма массивов по правилам варианта 1.
    """
    logger.debug(f"Начало выполнения sum_arrays_special")
    logger.debug(f"Входные данные: arr1={arr1}, arr2={arr2}")

    # Проверка размера
    if len(arr1) != len(arr2):
        error_msg = f"Массивы разного размера: {len(arr1)} != {len(arr2)}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    logger.debug("Проверка размера массивов пройдена")

    # Сортировка по условию
    sorted1 = sort_array_desc(arr1)  # по убыванию
    sorted2 = sort_array_asc(arr2)  # по возрастанию

    logger.debug(f"После сортировки: sorted1={sorted1}, sorted2={sorted2}")

    # Сумма с особым правилом
    result = []
    zero_count = 0

    for a, b in zip(sorted1, sorted2):
        if a == b:
            result.append(0)
            zero_count += 1
        else:
            result.append(a + b)

    logger.debug(f"После суммирования: result={result}, нулей: {zero_count}")

    # Финальная сортировка
    final_result = sort_array_asc(result)

    logger.info(f"Алгоритм выполнен. Исходные размеры: {len(arr1)}")
    logger.info(f"Количество нулей в результате: {zero_count}")
    logger.info(f"Финальный результат: {final_result}")

    return final_result


@FunctionLogger('algorithm1')
def main():
    """Основная функция алгоритма (отдельный режим)."""
    logger.info("Запуск алгоритма 1 в автономном режиме")

    print("=" * 50)
    print("АЛГОРИТМ 1: Сумма массивов с разной сортировкой")
    print("=" * 50)

    print("\nВыберите способ ввода данных:")
    print("1. Ввести массивы вручную")
    print("2. Сгенерировать случайные массивы")

    choice = input("Ваш выбор (1 или 2): ")

    if choice == "1":
        print("\n--- Ввод первого массива ---")
        arr1 = manual_input_array("Введите числа через пробел: ")

        print("\n--- Ввод второго массива ---")
        print(f"Второй массив должен иметь такой же размер ({len(arr1)})")
        arr2 = manual_input_array("Введите числа через пробел: ")

    elif choice == "2":
        # Безопасный ввод чисел
        try:
            size = int(input("Размер массивов: "))
            min_val = int(input("Минимальное значение: "))
            max_val = int(input("Максимальное значение: "))
        except ValueError:
            print("Ошибка: введите целые числа!")
            return

        arr1 = generate_random_array(size, min_val, max_val)
        arr2 = generate_random_array(size, min_val, max_val)

        print(f"\nСгенерированный массив 1: {arr1}")
        print(f"Сгенерированный массив 2: {arr2}")
    else:
        print("Неверный выбор!")
        return

    print("\n" + "-" * 50)
    print("Выполнение алгоритма...")

    try:
        result = sum_arrays_special(arr1, arr2)

        print("\n" + "=" * 50)
        print("РЕЗУЛЬТАТ:")
        print(f"Исходный массив 1: {arr1}")
        print(f"Исходный массив 2: {arr2}")
        print(f"Результирующий массив: {result}")
        print("=" * 50)

    except Exception as e:
        print(f"\nОшибка: {e}")


# Экспорт функции для использования в main.py
if __name__ == "__main__":
    main()
else:
    # Экспортируем только основную функцию
    pass
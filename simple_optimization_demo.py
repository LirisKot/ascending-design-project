"""
ПОЛНАЯ ДЕМОНСТРАЦИЯ ОПТИМИЗАЦИИ АЛГОРИТМА 8
Показывает разницу в производительности и потреблении ресурсов
"""

import time
import random
import tracemalloc
import sys
from typing import List, Set

# ============================================================================
# ВЕРСИИ АЛГОРИТМА ДЛЯ СРАВНЕНИЯ
# ============================================================================

def find_common_original(arr1: List[int], arr2: List[int]) -> List[int]:
    """Исходная версия (медленная) - O(n²)"""
    common = set()

    # Для каждого элемента первого массива
    for num in arr1:
        # ПРЯМОЕ СОВПАДЕНИЕ: ищем во втором массиве - O(n)
        if num in arr2:  # ← МЕДЛЕННО: линейный поиск в списке!
            common.add(num)

        # ПЕРЕВЕРНУТОЕ СОВПАДЕНИЕ
        if isinstance(num, int) and num >= 0:
            try:
                # Создаем строку и переворачиваем
                reversed_num = int(str(num)[::-1])  # ← СОЗДАНИЕ СТРОКИ КАЖДЫЙ РАЗ
                # Ищем перевернутое число - еще O(n)
                if reversed_num in arr2:  # ← СНОВА МЕДЛЕННЫЙ ПОИСК!
                    common.add(num)
            except:
                pass

    return list(common)


def find_common_optimized(arr1: List[int], arr2: List[int]) -> List[int]:
    """Оптимизированная версия - O(n)"""
    # ШАГ 1: Преобразуем второй массив в множество - O(n)
    arr2_set = set(arr2)  # ← КЛЮЧЕВАЯ ОПТИМИЗАЦИЯ: теперь поиск O(1)!

    common = set()

    # ШАГ 2: Убираем дубликаты из первого массива
    unique_arr1 = set(arr1)  # ← Меньше итераций!

    # ШАГ 3: Прямые совпадения - O(m) где m = len(unique_arr1)
    common.update(unique_arr1.intersection(arr2_set))

    # ШАГ 4: Перевернутые совпадения
    for num in unique_arr1:
        if num in common:  # Уже нашли как прямое совпадение
            continue

        # Быстрое переворачивание числа
        if isinstance(num, int) and num >= 0:
            # Математическое переворачивание вместо строкового
            reversed_num = 0
            temp = num
            while temp > 0:
                reversed_num = reversed_num * 10 + (temp % 10)
                temp //= 10

            if reversed_num != 0 and reversed_num != num and reversed_num in arr2_set:  # ← БЫСТРЫЙ ПОИСК O(1)!
                common.add(num)

    return list(common)


# ============================================================================
# ИНСТРУМЕНТЫ ИЗМЕРЕНИЯ
# ============================================================================

def measure_time(func, *args, iterations: int = 1) -> float:
    """Измеряет время выполнения функции"""
    total_time = 0

    for _ in range(iterations):
        start_time = time.perf_counter()
        func(*args)
        total_time += time.perf_counter() - start_time

    return total_time / iterations


def measure_memory(func, *args) -> float:
    """Измеряет пиковое использование памяти"""
    tracemalloc.start()
    func(*args)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak / 1024  # в КБ


def count_operations_original(n: int) -> int:
    """Считает примерное количество операций для исходного алгоритма"""
    # Для каждого из n элементов:
    # - Поиск в arr2: n операций
    # - Переворот числа: ~k операций (длина числа)
    # - Поиск перевернутого: еще n операций
    return n * (n + 5 + n)  # Примерно: n * (поиск + переворот + поиск)


def count_operations_optimized(n: int) -> int:
    """Считает примерное количество операций для оптимизированного алгоритма"""
    # Создание множества: n операций
    # Удаление дубликатов из arr1: n операций
    # Проверка каждого уникального элемента: m операций (m ≤ n)
    # Поиск в множестве: 1 операция (вместо n)
    return n + n + n * 2  # Примерно


# ============================================================================
# НАГЛЯДНАЯ ДЕМОНСТРАЦИЯ
# ============================================================================

def demonstrate_with_small_example():
    """Демонстрация на маленьком примере - показываем каждый шаг"""
    print("=" * 80)
    print("НАГЛЯДНАЯ ДЕМОНСТРАЦИЯ НА МАЛЕНЬКОМ ПРИМЕРЕ")
    print("=" * 80)

    arr1 = [123, 456, 789, 111, 222, 123]  # Есть дубликат 123
    arr2 = [321, 654, 987, 333, 444]

    print(f"\nМассив 1: {arr1}")
    print(f"Массив 2: {arr2}")
    print(f"Длина arr1: {len(arr1)}, arr2: {len(arr2)}")

    print("\n" + "-" * 80)
    print("ИСХОДНЫЙ АЛГОРИТМ (пошагово):")
    print("-" * 80)

    print("\n1. Для числа 123:")
    print("   - Ищем 123 в arr2: проверяем 321, 654, 987, 333, 444 → не нашли")
    print("   - Переворачиваем: '123' → '321'")
    print("   - Ищем 321 в arr2: проверяем 321 (первый же!) → НАШЛИ!")
    print("   → Добавляем 123 в результат")

    print("\n2. Для числа 456:")
    print("   - Ищем 456 в arr2: проверяем все 5 чисел → не нашли")
    print("   - Переворачиваем: '456' → '654'")
    print("   - Ищем 654 в arr2: проверяем 321, 654 (второй!) → НАШЛИ!")
    print("   → Добавляем 456 в результат")

    print("\n3. Для числа 789: аналогично → находим через 987")
    print("4. Для чисел 111 и 222: не находим ни прямых, ни перевернутых совпадений")
    print("5. Для второго числа 123: ДУБЛИКАТ! Снова делаем те же 10+ проверок!")

    total_checks = len(arr1) * len(arr2) * 2  # Два поиска для каждого элемента
    print(f"\n✓ ВСЕГО ПРОВЕРОК: {total_checks}")
    print(f"✓ ИЗ НИХ ИЗБЫТОЧНЫХ (из-за дубликата 123): {len(arr2) * 2}")

    print("\n" + "-" * 80)
    print("ОПТИМИЗИРОВАННЫЙ АЛГОРИТМ (пошагово):")
    print("-" * 80)

    print("\n1. Преобразуем arr2 в множество:")
    print(f"   set(arr2) = {{{', '.join(map(str, arr2))}}}")
    print("   → Поиск в множестве выполняется мгновенно!")

    print("\n2. Убираем дубликаты из arr1:")
    print(f"   unique(arr1) = {{{', '.join(map(str, set(arr1)))}}}")
    print("   → Теперь обрабатываем 5 чисел вместо 6!")

    print("\n3. Для каждого уникального числа:")
    print("   123: есть в множестве? НЕТ → проверяем перевернутое 321 → ЕСТЬ! ✓")
    print("   456: есть? НЕТ → 654 → ЕСТЬ! ✓")
    print("   789: есть? НЕТ → 987 → ЕСТЬ! ✓")
    print("   111: есть? НЕТ → 111 → НЕТ (такое же) ✗")
    print("   222: есть? НЕТ → 222 → НЕТ ✗")

    total_checks = len(set(arr1)) * 2  # Две проверки для каждого уникального
    print(f"\n✓ ВСЕГО ПРОВЕРОК: {total_checks}")
    print("✓ ДУБЛИКАТЫ: не обрабатываются вообще!")

    # Запускаем оба алгоритма
    print("\n" + "-" * 80)
    print("РЕЗУЛЬТАТЫ ВЫПОЛНЕНИЯ:")
    print("-" * 80)

    result1 = find_common_original(arr1, arr2)
    result2 = find_common_optimized(arr1, arr2)

    print(f"Исходный алгоритм:    {result1}")
    print(f"Оптимизированный:     {result2}")
    print(f"Результаты совпадают? {set(result1) == set(result2)}")


def performance_comparison():
    """Сравнение производительности на разных размерах данных"""
    print("\n" + "=" * 80)
    print("СРАВНЕНИЕ ПРОИЗВОДИТЕЛЬНОСТИ НА РАЗНЫХ РАЗМЕРАХ ДАННЫХ")
    print("=" * 80)

    test_cases = [
        ("Очень маленькие", 10),
        ("Маленькие", 100),
        ("Средние", 1000),
        ("Большие", 5000),
        ("Очень большие", 20000),
    ]

    print("\nПодготовка тестовых данных...")

    for test_name, size in test_cases:
        print(f"\n{'-'*60}")
        print(f"{test_name.upper()} массивы ({size} элементов):")
        print(f"{'-'*60}")

        # Генерируем тестовые данные
        random.seed(42)  # Для воспроизводимости
        arr1 = [random.randint(100, 99999) for _ in range(size)]
        arr2 = [random.randint(100, 99999) for _ in range(size)]

        # Добавляем совпадения
        common_count = size // 10
        for i in range(common_count):
            if i % 2 == 0:
                # Прямые совпадения
                val = random.randint(100, 9999)
                arr1[i] = val
                arr2[i] = val
            else:
                # Перевернутые совпадения
                val = random.randint(100, 9999)
                arr1[i] = val
                arr2[i] = int(str(val)[::-1])

        print(f"Тестирование...")

        # Тестируем исходный алгоритм
        time1 = measure_time(find_common_original, arr1, arr2, iterations=1)
        mem1 = measure_memory(find_common_original, arr1, arr2)
        ops1 = count_operations_original(size)

        # Тестируем оптимизированный алгоритм
        time2 = measure_time(find_common_optimized, arr1, arr2, iterations=1)
        mem2 = measure_memory(find_common_optimized, arr1, arr2)
        ops2 = count_operations_optimized(size)

        # Выводим результаты
        print(f"\n{'Метод':<25} {'Время (сек)':<15} {'Память (КБ)':<15} {'Операции':<15}")
        print(f"{'-'*70}")
        print(f"{'Исходный':<25} {time1:<15.6f} {mem1:<15.2f} {ops1:<15,}")
        print(f"{'Оптимизированный':<25} {time2:<15.6f} {mem2:<15.2f} {ops2:<15,}")

        # Считаем улучшение
        if time1 > 0 and time2 > 0:
            speedup = time1 / time2
            print(f"\n✓ УСКОРЕНИЕ: {speedup:.1f}× быстрее")

        if mem1 > 0 and mem2 > 0:
            memory_saving = (mem1 - mem2) / mem1 * 100
            print(f"✓ ЭКОНОМИЯ ПАМЯТИ: {memory_saving:+.1f}%")

        if ops1 > 0 and ops2 > 0:
            ops_reduction = (ops1 - ops2) / ops1 * 100
            print(f"✓ МЕНЬШЕ ОПЕРАЦИЙ: {ops_reduction:+.1f}%")


def big_o_comparison():
    """Наглядное сравнение сложности алгоритмов"""
    print("\n" + "=" * 80)
    print("СРАВНЕНИЕ СЛОЖНОСТИ АЛГОРИТМОВ (Big O Notation)")
    print("=" * 80)

    print("\nИСХОДНЫЙ АЛГОРИТМ:")
    print("-" * 40)
    print("for num in arr1:                    # O(n)")
    print("    if num in arr2:                 # O(n) - линейный поиск в списке")
    print("        common.add(num)")
    print("    reversed_num = int(str(num)[::-1])  # O(k) - k = длина числа")
    print("    if reversed_num in arr2:        # O(n) - снова линейный поиск")
    print("        common.add(num)")
    print(f"\nОБЩАЯ СЛОЖНОСТЬ: O(n × (n + k + n)) ≈ O(n²)")
    print("При n=1000: ~1,000,000 операций")
    print("При n=10000: ~100,000,000 операций")

    print("\nОПТИМИЗИРОВАННЫЙ АЛГОРИТМ:")
    print("-" * 40)
    print("arr2_set = set(arr2)                # O(n)")
    print("unique_arr1 = set(arr1)             # O(n)")
    print("for num in unique_arr1:             # O(m) где m ≤ n")
    print("    if num in arr2_set:             # O(1) - хеш-таблица!")
    print("        common.add(num)")
    print("    reversed_num = reverse(num)     # O(k)")
    print("    if reversed_num in arr2_set:    # O(1)")
    print("        common.add(num)")
    print(f"\nОБЩАЯ СЛОЖНОСТЬ: O(n + m × (1 + k + 1)) ≈ O(n)")
    print("При n=1000: ~2,000 операций")
    print("При n=10000: ~20,000 операций")

    # Таблица сравнения
    print("\n" + "=" * 80)
    print("ТАБЛИЦА СРАВНЕНИЯ ПРОИЗВОДИТЕЛЬНОСТИ:")
    print("=" * 80)

    headers = ["Размер n", "Исходный O(n²)", "Оптимизированный O(n)", "Ускорение", "Разница в операциях"]
    print(f"{headers[0]:<12} {headers[1]:<20} {headers[2]:<25} {headers[3]:<12} {headers[4]}")
    print("-" * 90)

    sizes = [10, 100, 1000, 5000, 10000]
    for n in sizes:
        ops_original = n * (n + 5 + n)  # Примерно n² операций
        ops_optimized = n + n + n * 2   # Примерно n операций
        speedup = ops_original / ops_optimized if ops_optimized > 0 else 0
        ops_diff = ops_original - ops_optimized

        print(f"{n:<12} {ops_original:<20,} {ops_optimized:<25,} {speedup:<12.0f}x {ops_diff:<20,}")


# ============================================================================
# ГЛАВНАЯ ФУНКЦИЯ
# ============================================================================

def main():
    """Главная функция демонстрации"""
    print("=" * 80)
    print("ДЕМОНСТРАЦИЯ ОПТИМИЗАЦИИ АЛГОРИТМА ПОИСКА ОБЩИХ ЧИСЕЛ")
    print("=" * 80)

    # Показываем меню
    print("\nВыберите демонстрацию:")
    print("1. Наглядный пример на маленьких данных")
    print("2. Сравнение производительности")
    print("3. Сравнение сложности алгоритмов (O)")
    print("4. Все демонстрации")

    choice = input("\nВаш выбор (1-4): ")

    if choice == "1":
        demonstrate_with_small_example()
    elif choice == "2":
        performance_comparison()
    elif choice == "3":
        big_o_comparison()
    elif choice == "4":
        demonstrate_with_small_example()
        performance_comparison()
        big_o_comparison()

    else:
        print("Неверный выбор!")
        return

    print("\n" + "=" * 80)
    print("ВЫВОДЫ:")
    print("=" * 80)
    print("""
    1. ИСПОЛЬЗУЙТЕ МНОЖЕСТВА (set) для поиска - это меняет O(n) → O(1)
    
    2. УБИРАЙТЕ ДУБЛИКАТЫ на раннем этапе - меньше итераций
    
    3. ИЗБЕГАЙТЕ ВЛОЖЕННЫХ ЦИКЛОВ - они создают O(n²) сложность
    
    4. КЕШИРУЙТЕ РЕЗУЛЬТАТЫ дорогих операций (переворот чисел)
    
    5. ВЫБИРАЙТЕ ПРАВИЛЬНЫЕ СТРУКТУРЫ ДАННЫХ:
       - Списки (list) для последовательного доступа
       - Множества (set) для поиска
       - Словари (dict) для ключ-значение
    
    Эти оптимизации можно применить к ВСЕМ вашим алгоритмам!
    """)

if __name__ == "__main__":
    main()
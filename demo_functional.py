"""
ДЕМОНСТРАЦИЯ ФУНКЦИОНАЛЬНОГО ПРОГРАММИРОВАНИЯ
===========================================

Примеры применения принципов ФП без изменения существующего кода
"""

import functools
from typing import Callable, Any, List, Dict, TypeVar
from collections import defaultdict

T = TypeVar('T')
U = TypeVar('U')


# ============================================================================
# ПРИНЦИП 1: ЧИСТЫЕ ФУНКЦИИ
# ============================================================================

def pure_sum_arrays(arr1: List[int], arr2: List[int]) -> List[int]:
    """
    Чистая функция:
    - Не изменяет входные данные
    - Не имеет побочных эффектов
    - Всегда одинаковый результат для одинаковых входов
    """
    # Проверка (не изменяет входные данные)
    if len(arr1) != len(arr2):
        raise ValueError("Массивы должны быть одного размера")

    # Создание НОВОГО списка (не изменяем существующие)
    return [a + b for a, b in zip(sorted(arr1, reverse=True), sorted(arr2))]


def pure_rotate_matrix(matrix: List[List[Any]], clockwise: bool = True) -> List[List[Any]]:
    """
    Чистая функция поворота матрицы
    Возвращает новую матрицу, не изменяя исходную
    """
    if not matrix:
        return []

    rows, cols = len(matrix), len(matrix[0])

    if clockwise:
        # Создаем новую матрицу для результата
        return [
            [matrix[rows - 1 - j][i] for j in range(rows)]
            for i in range(cols)
        ]
    else:
        return [
            [matrix[j][cols - 1 - i] for j in range(rows)]
            for i in range(cols)
        ]


# ============================================================================
# ПРИНЦИП 2: ФУНКЦИИ ВЫСШЕГО ПОРЯДКА
# ============================================================================

def create_array_processor(
        transform_fn: Callable[[int], int],
        filter_fn: Callable[[int], bool] = lambda x: True
) -> Callable[[List[int]], List[int]]:
    """
    Функция высшего порядка:
    Принимает другие функции как аргументы и возвращает новую функцию
    """

    def processor(array: List[int]) -> List[int]:
        return [
            transform_fn(x)
            for x in array
            if filter_fn(x)
        ]

    return processor


# ============================================================================
# ПРИНЦИП 3: КАРРИРОВАНИЕ И ЧАСТИЧНОЕ ПРИМЕНЕНИЕ
# ============================================================================

def curry_sum_arrays():
    """Каррированная версия сложения массивов"""

    def sum_step1(arr1: List[int]) -> Callable:
        def sum_step2(arr2: List[int]) -> List[int]:
            return [a + b for a, b in zip(arr1, arr2)]

        return sum_step2

    return sum_step1


# ============================================================================
# ПРИНЦИП 4: КОМПОЗИЦИЯ ФУНКЦИЙ
# ============================================================================

def compose(*funcs: Callable) -> Callable:
    """Композиция функций (справа налево)"""

    def _compose(data: Any) -> Any:
        return functools.reduce(lambda acc, f: f(acc), reversed(funcs), data)

    return _compose


def pipe(*funcs: Callable) -> Callable:
    """Пайплайн функций (слева направо)"""

    def _pipe(data: Any) -> Any:
        return functools.reduce(lambda acc, f: f(acc), funcs, data)

    return _pipe


# ============================================================================
# ПРИНЦИП 5: НЕИЗМЕНЯЕМОСТЬ (IMMUTABILITY)
# ============================================================================

class ImmutableArrayProcessor:
    """
    Класс, демонстрирующий работу с неизменяемыми данными
    Каждая операция возвращает новый объект
    """

    def __init__(self, data: List[int]):
        # Копируем данные для обеспечения неизменяемости
        self._data = data.copy()

    def sort_desc(self) -> 'ImmutableArrayProcessor':
        """Сортировка по убыванию (возвращает новый объект)"""
        return ImmutableArrayProcessor(sorted(self._data, reverse=True))

    def filter(self, predicate: Callable[[int], bool]) -> 'ImmutableArrayProcessor':
        """Фильтрация (возвращает новый объект)"""
        return ImmutableArrayProcessor([x for x in self._data if predicate(x)])

    def map(self, transform: Callable[[int], int]) -> 'ImmutableArrayProcessor':
        """Трансформация (возвращает новый объект)"""
        return ImmutableArrayProcessor([transform(x) for x in self._data])

    def get_data(self) -> List[int]:
        """Получение данных (без возможности изменения)"""
        return self._data.copy()  # Возвращаем копию!


# ============================================================================
# ПРИНЦИП 6: MAP, FILTER, REDUCE
# ============================================================================

def functional_array_operations():
    """Демонстрация функциональных операций над массивами"""

    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # 1. MAP (трансформация)
    squared = list(map(lambda x: x ** 2, data))

    # 2. FILTER (фильтрация)
    evens = list(filter(lambda x: x % 2 == 0, data))

    # 3. REDUCE (агрегация)
    product = functools.reduce(lambda x, y: x * y, data)

    # 4. Цепочка операций
    result = functools.reduce(
        lambda acc, x: acc + x,
        map(lambda x: x * 2,
            filter(lambda x: x > 5, data)
            ),
        0  # Начальное значение
    )

    return {
        'squared': squared,
        'evens': evens,
        'product': product,
        'chained_result': result
    }


# ============================================================================
# ПРИНЦИП 7: ЛЯМБДА-ФУНКЦИИ
# ============================================================================

def lambda_demo():
    """Демонстрация использования лямбда-функций"""

    # Сортировка по кастомному ключу
    points = [(1, 2), (3, 1), (5, 4), (2, 2)]
    sorted_by_y = sorted(points, key=lambda p: p[1])

    # Группировка
    words = ['apple', 'banana', 'apricot', 'blueberry', 'avocado']
    grouped = defaultdict(list)
    for word in words:
        grouped[word[0]].append(word)

    # Функция-генератор с лямбдой
    create_multiplier = lambda factor: lambda x: x * factor
    double = create_multiplier(2)
    triple = create_multiplier(3)

    return {
        'sorted_points': sorted_by_y,
        'grouped_words': dict(grouped),
        'double_5': double(5),
        'triple_5': triple(5)
    }


# ============================================================================
# ПРИНЦИП 8: ДЕКОРАТОРЫ (ФУНКЦИИ ВЫСШЕГО ПОРЯДКА)
# ============================================================================

def memoize(func: Callable) -> Callable:
    """Декоратор для мемоизации (кеширования) результатов"""
    cache = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, tuple(kwargs.items()))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    wrapper.clear_cache = lambda: cache.clear()
    return wrapper


def log_execution(func: Callable) -> Callable:
    """Декоратор для логирования выполнения функции"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] Вызов {func.__name__} с args={args[:2] if args else args}...")
        result = func(*args, **kwargs)
        print(f"[LOG] Результат {func.__name__}: {result[:3] if isinstance(result, list) else result}...")
        return result

    return wrapper


# Пример использования декоратора
@memoize
@log_execution
def expensive_computation(n: int) -> int:
    """Дорогая вычисляемая функция"""
    return sum(i * i for i in range(n))


# ============================================================================
# ПРИНЦИП 9: МОНОИДЫ И ФУНКТОРЫ (упрощенно)
# ============================================================================

class Maybe:
    """
    Упрощенная реализация Maybe (Option) монады
    Для безопасной работы с nullable значениями
    """

    def __init__(self, value):
        self._value = value

    def map(self, f: Callable) -> 'Maybe':
        """Применяет функцию к значению, если оно существует"""
        if self._value is None:
            return Maybe(None)
        return Maybe(f(self._value))

    def get_or_else(self, default):
        """Возвращает значение или значение по умолчанию"""
        return self._value if self._value is not None else default

    @staticmethod
    def of(value):
        """Фабричный метод"""
        return Maybe(value)


# ============================================================================
# ДЕМОНСТРАЦИОННЫЕ ФУНКЦИИ ДЛЯ СУЩЕСТВУЮЩИХ АЛГОРИТМОВ
# ============================================================================

def demo_algorithm1_functional():
    """Функциональная версия алгоритма 1"""

    def process_arrays_functional(arr1, arr2):
        """
        Функциональная обработка массивов:
        - Только чистые функции
        - Неизменяемые данные
        - Композиция операций
        """

        # Конвейер обработки
        process = pipe(
            # Шаг 1: Проверка размеров
            lambda data: (
                data[0], data[1]
            if len(data[0]) == len(data[1])
            else None
            ),

            # Шаг 2: Сортировка
            lambda data: (
                sorted(data[0], reverse=True),
                sorted(data[1])
            ) if data else None,

            # Шаг 3: Обработка пар
            lambda data: list(map(
                lambda pair: 0 if pair[0] == pair[1] else pair[0] + pair[1],
                zip(data[0], data[1])
            )) if data else None,

            # Шаг 4: Финальная сортировка
            lambda data: sorted(data) if data else None
        )

        return process((arr1, arr2))

    # Тестовый пример
    test_arr1 = [3, 1, 4, 1, 5]
    test_arr2 = [9, 2, 6, 5, 3]

    result = process_arrays_functional(test_arr1, test_arr2)

    return {
        'algorithm': '1 (Сумма массивов)',
        'input': {'arr1': test_arr1, 'arr2': test_arr2},
        'functional_result': result,
        'description': 'Обработка через пайплайн чистых функций'
    }


def demo_algorithm3_functional():
    """Функциональная версия алгоритма 3"""

    def rotate_matrix_functional(matrix, direction='clockwise'):
        """Функциональный поворот матрицы"""

        if direction == 'clockwise':
            # Транспонирование + обращение строк
            transposed = list(zip(*matrix))
            return [list(reversed(row)) for row in transposed]
        else:
            # Обращение строк + транспонирование
            reversed_rows = [list(reversed(row)) for row in matrix]
            return list(zip(*reversed_rows))

    # Тестовый пример
    test_matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]

    clockwise = rotate_matrix_functional(test_matrix, 'clockwise')
    counterclockwise = rotate_matrix_functional(test_matrix, 'counterclockwise')

    return {
        'algorithm': '3 (Поворот матрицы)',
        'input': test_matrix,
        'clockwise': clockwise,
        'counterclockwise': counterclockwise,
        'description': 'Использование zip и map для поворота'
    }


def demo_algorithm8_functional():
    """Функциональная версия алгоритма 8"""

    def find_common_functional(arr1, arr2):
        """Функциональный поиск общих чисел"""

        # Создаем множество перевернутых чисел
        reversed_nums = set(
            int(str(x)[::-1])
            for x in arr1
            if isinstance(x, int) and x >= 0
        )

        # Поиск совпадений
        direct_matches = set(arr1) & set(arr2)
        reversed_matches = set(
            x for x in arr1
            if int(str(x)[::-1]) in arr2
        )

        return list(direct_matches | reversed_matches)

    # Тестовый пример
    test_arr1 = [123, 456, 789, 101]
    test_arr2 = [321, 654, 987, 202]

    result = find_common_functional(test_arr1, test_arr2)

    return {
        'algorithm': '8 (Общие числа)',
        'input': {'arr1': test_arr1, 'arr2': test_arr2},
        'result': result,
        'description': 'Использование множеств и генераторов'
    }


# ============================================================================
# ПРИМЕР ПАЙПЛАЙНА ОБРАБОТКИ ДАННЫХ
# ============================================================================

# Пример конвейера обработки данных
data_pipeline = pipe(
    lambda arr: [x for x in arr if x > 0],  # Фильтр
    lambda arr: sorted(arr),  # Сортировка
    lambda arr: [x * 2 for x in arr],  # Трансформация
    lambda arr: sum(arr)  # Агрегация
)


# ============================================================================
# ГЛАВНАЯ ДЕМОНСТРАЦИОННАЯ ФУНКЦИЯ
# ============================================================================

def run_all_demos():
    """Запуск всех демонстраций функционального программирования"""

    print("=" * 70)
    print("ДЕМОНСТРАЦИЯ ПРИНЦИПОВ ФУНКЦИОНАЛЬНОГО ПРОГРАММИРОВАНИЯ")
    print("=" * 70)

    # Демонстрация 1: Чистые функции
    print("\n1. ЧИСТЫЕ ФУНКЦИИ")
    print("-" * 40)

    arr1 = [1, 3, 2]
    arr2 = [4, 6, 5]

    result = pure_sum_arrays(arr1, arr2)
    print(f"Вход: arr1={arr1}, arr2={arr2}")
    print(f"Результат: {result}")
    print(f"Исходные массивы не изменились: arr1={arr1}, arr2={arr2}")

    # Демонстрация 2: Функции высшего порядка
    print("\n\n2. ФУНКЦИИ ВЫСШЕГО ПОРЯДКА")
    print("-" * 40)

    processor = create_array_processor(
        transform_fn=lambda x: x ** 2,
        filter_fn=lambda x: x % 2 == 1
    )
    data = [1, 2, 3, 4, 5]
    processed = processor(data)
    print(f"Обработка {data}: {processed}")

    # Демонстрация 3: Map, Filter, Reduce
    print("\n\n3. MAP, FILTER, REDUCE")
    print("-" * 40)

    map_filter_reduce = functional_array_operations()
    for key, value in map_filter_reduce.items():
        print(f"{key}: {value}")

    # Демонстрация 4: Лямбда-функции
    print("\n\n4. ЛЯМБДА-ФУНКЦИИ")
    print("-" * 40)

    lambda_results = lambda_demo()
    for key, value in lambda_results.items():
        print(f"{key}: {value}")

    # Демонстрация 5: Декораторы
    print("\n\n5. ДЕКОРАТОРЫ")
    print("-" * 40)

    print("Первое вычисление (с логированием):")
    result1 = expensive_computation(5)
    print(f"Результат: {result1}")

    print("\nВторое вычисление (из кеша, без логирования):")
    result2 = expensive_computation(5)
    print(f"Результат: {result2}")

    # Демонстрация 6: Функциональные версии алгоритмов
    print("\n\n6. ФУНКЦИОНАЛЬНЫЕ ВЕРСИИ АЛГОРИТМОВ")
    print("-" * 40)

    # Алгоритм 1
    algo1 = demo_algorithm1_functional()
    print(f"\n{algo1['algorithm']}:")
    print(f"Вход: {algo1['input']}")
    print(f"Результат: {algo1['functional_result']}")
    print(f"Описание: {algo1['description']}")

    # Алгоритм 3
    algo3 = demo_algorithm3_functional()
    print(f"\n{algo3['algorithm']}:")
    print(f"Входная матрица:")
    for row in algo3['input']:
        print(f"  {row}")
    print(f"По часовой стрелке:")
    for row in algo3['clockwise']:
        print(f"  {list(row)}")

    # Алгоритм 8
    algo8 = demo_algorithm8_functional()
    print(f"\n{algo8['algorithm']}:")
    print(f"Вход: {algo8['input']}")
    print(f"Общие числа: {algo8['result']}")

    # Демонстрация 7: Пайплайны
    print("\n\n7. ПАЙПЛАЙНЫ ОБРАБОТКИ ДАННЫХ")
    print("-" * 40)

    test_data = [5, -3, 8, 1, -2, 4]
    pipeline_result = data_pipeline(test_data)
    print(f"Входные данные: {test_data}")
    print(f"Пайплайн (фильтр >0 -> сортировка -> x2 -> сумма): {pipeline_result}")

    # Демонстрация 8: Неизменяемость
    print("\n\n8. НЕИЗМЕНЯЕМОСТЬ (IMMUTABILITY)")
    print("-" * 40)

    original = [3, 1, 4, 1, 5, 9, 2, 6]
    processor = ImmutableArrayProcessor(original)

    # Цепочка операций, каждая возвращает новый объект
    result = (processor
              .filter(lambda x: x > 3)
              .map(lambda x: x * 10)
              .sort_desc()
              .get_data())

    print(f"Исходные данные: {original}")
    print(f"После цепочки (фильтр >3 -> x10 -> сортировка по убыванию): {result}")
    print(f"Исходные данные не изменились: {original}")

    # Демонстрация 9: Maybe монада
    print("\n\n9. MONAD (MAYBE)")
    print("-" * 40)

    maybe_value = Maybe.of(5)
    result = (maybe_value
              .map(lambda x: x * 2)
              .map(lambda x: x + 1)
              .get_or_else(0))
    print(f"Maybe(5).map(x*2).map(x+1) = {result}")

    maybe_none = Maybe.of(None)
    result_none = (maybe_none
                   .map(lambda x: x * 2)  # Не выполнится
                   .get_or_else("default"))
    print(f"Maybe(None).map(...).get_or_else('default') = '{result_none}'")

    print("\n" + "=" * 70)
    print("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
    print("=" * 70)


# ============================================================================
# ЭКСПОРТ ДЛЯ ИСПОЛЬЗОВАНИЯ В СУЩЕСТВУЮЩЕМ КОДЕ
# ============================================================================

# Утилиты для массивов
functional_utils = {
    'pure_sum_arrays': pure_sum_arrays,
    'pure_rotate_matrix': pure_rotate_matrix,
    'create_array_processor': create_array_processor,
    'compose': compose,
    'pipe': pipe,
    'data_pipeline': data_pipeline,
}

# Утилиты для работы с матрицами
matrix_utils = {
    'rotate_clockwise': lambda m: pure_rotate_matrix(m, True),
    'rotate_counterclockwise': lambda m: pure_rotate_matrix(m, False),
}

# Декораторы (можно использовать в существующем коде)
decorators = {
    'memoize': memoize,
    'log_execution': log_execution,
}

# ============================================================================
# ТОЧКА ВХОДА
# ============================================================================

if __name__ == "__main__":
    # Запуск демонстрации
    run_all_demos()

    print("\n\nЭкспортированные функции:")
    print("-" * 40)
    print("functional_utils содержит:", list(functional_utils.keys()))
    print("matrix_utils содержит:", list(matrix_utils.keys()))
    print("decorators содержит:", list(decorators.keys()))
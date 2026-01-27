"""
Модуль операций с матрицами
Для алгоритма 3 (поворот матрицы на 90 градусов)
"""


def create_matrix(rows, cols, fill_value=0):
    """Создание матрицы заданного размера"""
    return [[fill_value for _ in range(cols)] for _ in range(rows)]


def rotate_clockwise(matrix):
    """Поворот матрицы на 90° по часовой стрелке"""
    if not matrix:
        return []

    rows = len(matrix)
    cols = len(matrix[0])

    # Создаем новую матрицу с перевернутыми размерами
    rotated = [[0 for _ in range(rows)] for _ in range(cols)]

    for i in range(rows):
        for j in range(cols):
            rotated[j][rows - 1 - i] = matrix[i][j]

    return rotated


def rotate_counterclockwise(matrix):
    """Поворот матрицы на 90° против часовой стрелки"""
    if not matrix:
        return []

    rows = len(matrix)
    cols = len(matrix[0])

    rotated = [[0 for _ in range(rows)] for _ in range(cols)]

    for i in range(rows):
        for j in range(cols):
            rotated[cols - 1 - j][i] = matrix[i][j]

    return rotated


def print_matrix(matrix, name="Матрица"):
    """Красивый вывод матрицы"""
    if not matrix:
        print(f"{name}: [] (пустая)")
        return

    print(f"{name} [{len(matrix)}x{len(matrix[0])}]:")
    for row in matrix:
        print("  " + " ".join(f"{x:4}" for x in row))


# Тестирование
if __name__ == "__main__":
    print("Тестирование модуля матричных операций:")

    test_matrix = [[1, 2, 3], [4, 5, 6]]
    print_matrix(test_matrix, "Исходная матрица")

    clockwise = rotate_clockwise(test_matrix)
    print_matrix(clockwise, "Повернута по часовой")

    counterclockwise = rotate_counterclockwise(test_matrix)
    print_matrix(counterclockwise, "Повернута против часовой")
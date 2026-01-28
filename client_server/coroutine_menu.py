"""
КОРУТИНОВОЕ МЕНЮ - АВТОМАТНОЕ ПРОГРАММИРОВАНИЕ
=============================================

Реализация меню через корутины и автоматное программирование.
Каждое состояние меню - отдельная корутина.
"""

import asyncio
import sys
import os
from typing import Dict, Any, Optional, Callable
from enum import Enum
from datetime import datetime
import random

# ============================================================================
# ОПРЕДЕЛЕНИЕ СОСТОЯНИЙ АВТОМАТА
# ============================================================================

class MenuState(Enum):
    """Состояния автомата меню."""
    INITIAL = "initial"          # Начальное состояние
    MAIN_MENU = "main_menu"      # Главное меню
    TASK_SELECTION = "task_selection"  # Выбор задания
    TASK1_MENU = "task1_menu"    # Меню задания 1
    TASK3_MENU = "task3_menu"    # Меню задания 3 (поворот матрицы)
    TASK8_MENU = "task8_menu"    # Меню задания 8
    INPUT_METHOD = "input_method"  # Выбор способа ввода
    MANUAL_INPUT = "manual_input"  # Ручной ввод
    AUTO_INPUT = "auto_input"    # Автоматический ввод
    EXECUTION = "execution"      # Выполнение алгоритма
    RESULT = "result"            # Отображение результата
    SETTINGS = "settings"        # Настройки
    LOGGING_SETTINGS = "logging_settings"  # Настройки логирования
    ERROR = "error"              # Ошибка
    EXIT = "exit"                # Выход


class MenuEvent(Enum):
    """События автомата меню."""
    START = "start"              # Запуск автомата
    SELECT_MAIN = "select_main"  # Выбор главного меню
    SELECT_TASK = "select_task"  # Выбор задания
    SELECT_INPUT = "select_input"  # Выбор ввода
    SELECT_MANUAL_INPUT = "select_manual_input"  # Выбор ручного ввода
    SELECT_AUTO_INPUT = "select_auto_input"  # Выбор автоматического ввода
    INPUT_COMPLETE = "input_complete"  # Ввод завершен
    EXECUTE = "execute"          # Выполнить
    BACK = "back"                # Назад
    SETTINGS = "settings"        # Настройки
    ERROR = "error"              # Ошибка
    EXIT = "exit"                # Выход


# ============================================================================
# КЛАСС АВТОМАТА МЕНЮ
# ============================================================================

class MenuAutomaton:
    """Автомат для управления меню через корутины."""

    def __init__(self):
        self.state = MenuState.INITIAL
        self.context: Dict[str, Any] = {
            'selected_task': None,
            'task_data': None,
            'task_result': None,
            'current_input': [],
            'error_message': None,
            'start_time': datetime.now()
        }

        # Создаем заглушку для логгера если нет импорта
        class DummyLogger:
            def debug(self, msg): print(f"[DEBUG] {msg}")
            def info(self, msg): print(f"[INFO] {msg}")
            def error(self, msg): print(f"[ERROR] {msg}")
            def warning(self, msg): print(f"[WARNING] {msg}")

        self.logger = DummyLogger()

        self.transition_table = self._create_transition_table()

        # Регистрация корутин состояний
        self.state_coroutines = {
            MenuState.INITIAL: self._state_initial,
            MenuState.MAIN_MENU: self._state_main_menu,
            MenuState.TASK_SELECTION: self._state_task_selection,
            MenuState.TASK1_MENU: self._state_task1_menu,
            MenuState.TASK3_MENU: self._state_task3_menu,
            MenuState.TASK8_MENU: self._state_task8_menu,
            MenuState.INPUT_METHOD: self._state_input_method,
            MenuState.MANUAL_INPUT: self._state_manual_input,
            MenuState.AUTO_INPUT: self._state_auto_input,
            MenuState.EXECUTION: self._state_execution,
            MenuState.RESULT: self._state_result,
            MenuState.SETTINGS: self._state_settings,
            MenuState.LOGGING_SETTINGS: self._state_logging_settings,
            MenuState.ERROR: self._state_error,
            MenuState.EXIT: self._state_exit
        }

        self.logger.info("Автомат меню инициализирован")

    def _create_transition_table(self) -> Dict[MenuState, Dict[MenuEvent, MenuState]]:
        """Создание таблицы переходов автомата."""
        return {
            MenuState.INITIAL: {
                MenuEvent.START: MenuState.MAIN_MENU,
                MenuEvent.ERROR: MenuState.ERROR,
                MenuEvent.EXIT: MenuState.EXIT
            },
            MenuState.MAIN_MENU: {
                MenuEvent.SELECT_TASK: MenuState.TASK_SELECTION,
                MenuEvent.SETTINGS: MenuState.SETTINGS,
                MenuEvent.EXIT: MenuState.EXIT,
                MenuEvent.ERROR: MenuState.ERROR
            },
            MenuState.TASK_SELECTION: {
                MenuEvent.SELECT_TASK: MenuState.TASK1_MENU,  # После выбора задачи
                MenuEvent.BACK: MenuState.MAIN_MENU,
                MenuEvent.ERROR: MenuState.ERROR
            },
            MenuState.TASK1_MENU: {
                MenuEvent.SELECT_INPUT: MenuState.INPUT_METHOD,
                MenuEvent.BACK: MenuState.TASK_SELECTION,
                MenuEvent.ERROR: MenuState.ERROR
            },
            MenuState.TASK3_MENU: {
                MenuEvent.SELECT_INPUT: MenuState.INPUT_METHOD,
                MenuEvent.BACK: MenuState.TASK_SELECTION,
                MenuEvent.ERROR: MenuState.ERROR
            },
            MenuState.TASK8_MENU: {
                MenuEvent.SELECT_INPUT: MenuState.INPUT_METHOD,
                MenuEvent.BACK: MenuState.TASK_SELECTION,
                MenuEvent.ERROR: MenuState.ERROR
            },
            MenuState.INPUT_METHOD: {
                MenuEvent.SELECT_MANUAL_INPUT: MenuState.MANUAL_INPUT,
                MenuEvent.SELECT_AUTO_INPUT: MenuState.AUTO_INPUT,
                MenuEvent.BACK: MenuState.TASK_SELECTION,
                MenuEvent.ERROR: MenuState.ERROR
            },
            MenuState.MANUAL_INPUT: {
                MenuEvent.INPUT_COMPLETE: MenuState.EXECUTION,
                MenuEvent.BACK: MenuState.INPUT_METHOD,
                MenuEvent.ERROR: MenuState.ERROR
            },
            MenuState.AUTO_INPUT: {
                MenuEvent.INPUT_COMPLETE: MenuState.EXECUTION,
                MenuEvent.BACK: MenuState.INPUT_METHOD,
                MenuEvent.ERROR: MenuState.ERROR
            },
            MenuState.EXECUTION: {
                MenuEvent.EXECUTE: MenuState.RESULT,
                MenuEvent.BACK: MenuState.INPUT_METHOD,
                MenuEvent.ERROR: MenuState.ERROR
            },
            MenuState.RESULT: {
                MenuEvent.BACK: MenuState.MAIN_MENU,
                MenuEvent.EXIT: MenuState.EXIT,
                MenuEvent.ERROR: MenuState.ERROR
            },
            MenuState.SETTINGS: {
                MenuEvent.SELECT_MAIN: MenuState.LOGGING_SETTINGS,
                MenuEvent.BACK: MenuState.MAIN_MENU,
                MenuEvent.ERROR: MenuState.ERROR
            },
            MenuState.LOGGING_SETTINGS: {
                MenuEvent.BACK: MenuState.SETTINGS,
                MenuEvent.ERROR: MenuState.ERROR
            },
            MenuState.ERROR: {
                MenuEvent.BACK: MenuState.MAIN_MENU,
                MenuEvent.EXIT: MenuState.EXIT
            },
            MenuState.EXIT: {}
        }

    def transition(self, event: MenuEvent, **kwargs) -> bool:
        """
        Переход между состояниями.

        Args:
            event: Событие для перехода
            **kwargs: Дополнительные параметры

        Returns:
            True если переход успешен
        """
        try:
            old_state = self.state
            new_state = self.transition_table[old_state].get(event)

            if new_state is None:
                self.logger.warning(f"Недопустимый переход: {old_state} -> {event}")
                return False

            # Обновление контекста
            if kwargs:
                self.context.update(kwargs)

            # Логирование перехода
            self.logger.debug(f"Переход состояния: {old_state} -> {new_state} (событие: {event})")

            self.state = new_state
            return True

        except Exception as e:
            self.logger.error(f"Ошибка перехода состояния: {e}")
            self.state = MenuState.ERROR
            self.context['error_message'] = str(e)
            return False

    async def run(self):
        """Запуск автомата."""
        self.logger.info("Запуск автомата меню")

        # Начальный переход
        self.transition(MenuEvent.START)

        # Основной цикл автомата
        while self.state != MenuState.EXIT:
            try:
                # Получаем корутину для текущего состояния
                coroutine = self.state_coroutines.get(self.state)

                if coroutine:
                    # Выполняем корутину состояния
                    event = await coroutine()

                    # Обрабатываем возвращенное событие
                    if event:
                        self.transition(event)
                else:
                    self.logger.error(f"Нет корутины для состояния: {self.state}")
                    self.transition(MenuEvent.ERROR,
                                  error_message=f"Неизвестное состояние: {self.state}")

            except asyncio.CancelledError:
                self.logger.info("Автомат отменен")
                break
            except Exception as e:
                self.logger.error(f"Ошибка в автомате: {e}")
                self.transition(MenuEvent.ERROR, error_message=str(e))

        self.logger.info("Автомат завершен")

    # ============================================================================
    # КОРУТИНЫ СОСТОЯНИЙ
    # ============================================================================

    async def _state_initial(self) -> Optional[MenuEvent]:
        """Корутина начального состояния."""
        print("\n" + "=" * 60)
        print("АВТОМАТНОЕ ПРОГРАММИРОВАНИЕ - МЕНЮ НА КОРУТИНАХ")
        print("=" * 60)

        await asyncio.sleep(0.5)  # Небольшая задержка для эффекта
        return MenuEvent.START

    async def _state_main_menu(self) -> Optional[MenuEvent]:
        """Корутина главного меню."""
        print("\n" + "=" * 60)
        print("ГЛАВНОЕ МЕНЮ")
        print("=" * 60)

        options = [
            "1. Выбор задания",
            "2. Настройки",
            "3. Выход"
        ]

        for option in options:
            print(option)

        try:
            choice = await self._async_input("\nВыберите пункт: ")

            if choice == "1":
                return MenuEvent.SELECT_TASK # Переход к выбору задания
            elif choice == "2":
                return MenuEvent.SETTINGS # Переход к настройкам
            elif choice == "3":
                return MenuEvent.EXIT   # Завершение работы
            else:
                print("Неверный выбор!")
                return None

        except Exception as e:
            print(f"Ошибка: {e}")
            return MenuEvent.ERROR

    async def _state_task_selection(self) -> Optional[MenuEvent]:
        """Корутина выбора задания."""
        print("\n" + "=" * 60)
        print("ВЫБОР ЗАДАНИЯ")
        print("=" * 60)

        tasks = {
            "1": ("Алгоритм 1: Сумма массивов", MenuState.TASK1_MENU),
            "2": ("Алгоритм 3: Поворот матрицы", MenuState.TASK3_MENU),
            "3": ("Алгоритм 8: Поиск общих чисел", MenuState.TASK8_MENU)
        }

        for key, (desc, _) in tasks.items():
            print(f"{key}. {desc}")
        print("4. Назад")

        try:
            choice = await self._async_input("\nВыберите задание: ")

            if choice == "1":
                self.context['selected_task'] = 1
                return MenuEvent.SELECT_TASK
            elif choice == "2":
                self.context['selected_task'] = 3
                return MenuEvent.SELECT_TASK
            elif choice == "3":
                self.context['selected_task'] = 8
                return MenuEvent.SELECT_TASK
            elif choice == "4":
                return MenuEvent.BACK
            else:
                print("Неверный выбор!")
                return None

        except Exception as e:
            print(f"Ошибка: {e}")
            return MenuEvent.ERROR

    async def _state_task1_menu(self) -> Optional[MenuEvent]:
        """Корутина меню задания 1."""
        print("\n" + "=" * 60)
        print("АЛГОРИТМ 1: СУММА МАССИВОВ С РАЗНОЙ СОРТИРОВКОЙ")
        print("=" * 60)

        print("\nОписание:")
        print("Входные данные: 2 массива одинакового размера")
        print("1. Первый массив → сортировка по убыванию")
        print("2. Второй массив → сортировка по возрастанию")
        print("3. Если элементы равны → результат 0, иначе сумма")
        print("4. Результат → сортировка по возрастанию")

        print("\n1. Продолжить")
        print("2. Назад")

        choice = await self._async_input("\nВыберите: ")

        if choice == "1":
            return MenuEvent.SELECT_INPUT
        elif choice == "2":
            return MenuEvent.BACK
        else:
            print("Неверный выбор!")
            return None

    async def _state_task3_menu(self) -> Optional[MenuEvent]:
        """Корутина меню задания 3 (поворот матрицы)."""
        print("\n" + "=" * 60)
        print("АЛГОРИТМ 3: ПОВОРОТ МАТРИЦЫ НА 90 ГРАДУСОВ")
        print("=" * 60)

        print("\nОписание:")
        print("Входные данные: матрица N на M")
        print("Требуется повернуть матрицу на 90 градусов")
        print("по часовой или против часовой стрелки")

        print("\n1. Продолжить")
        print("2. Назад")

        choice = await self._async_input("\nВыберите: ")

        if choice == "1":
            return MenuEvent.SELECT_INPUT
        elif choice == "2":
            return MenuEvent.BACK
        else:
            print("Неверный выбор!")
            return None

    async def _state_task8_menu(self) -> Optional[MenuEvent]:
        """Корутина меню задания 8."""
        print("\n" + "=" * 60)
        print("АЛГОРИТМ 8: ПОИСК ОБЩИХ ЧИСЕЛ")
        print("=" * 60)

        print("\nОписание:")
        print("Входные данные: 2 массива с числами")
        print("Число считается общим, если:")
        print("1. Оно входит в оба массива")
        print("2. Его перевернутая версия входит в другой массив")

        print("\n1. Продолжить")
        print("2. Назад")

        choice = await self._async_input("\nВыберите: ")

        if choice == "1":
            return MenuEvent.SELECT_INPUT
        elif choice == "2":
            return MenuEvent.BACK
        else:
            print("Неверный выбор!")
            return None

    async def _state_input_method(self) -> Optional[MenuEvent]:
        """Корутина выбора способа ввода."""
        print("\n" + "=" * 40)
        print("ВЫБОР СПОСОБА ВВОДА")
        print("=" * 40)

        print("\n1. Ручной ввод")
        print("2. Автоматическая генерация")
        print("3. Назад")

        choice = await self._async_input("\nВыберите способ: ")

        if choice == "1":
            print("Выбран ручной ввод")
            return MenuEvent.SELECT_MANUAL_INPUT
        elif choice == "2":
            print("Выбрана автоматическая генерация")
            return MenuEvent.SELECT_AUTO_INPUT
        elif choice == "3":
            return MenuEvent.BACK
        else:
            print("Неверный выбор!")
            return None

    async def _state_manual_input(self) -> Optional[MenuEvent]:
        """Корутина ручного ввода."""
        task_num = self.context.get('selected_task', 1)

        print("\n" + "=" * 40)
        print(f"РУЧНОЙ ВВОД ДЛЯ ЗАДАНИЯ {task_num}")
        print("=" * 40)

        try:
            if task_num == 1:
                # Ввод двух массивов
                print("\n--- Массив 1 ---")
                arr1_str = await self._async_input("Введите числа через пробел: ")
                arr1 = list(map(float, arr1_str.split()))

                print("\n--- Массив 2 ---")
                print(f"Должен быть такой же размер ({len(arr1)})")
                arr2_str = await self._async_input("Введите числа через пробел: ")
                arr2 = list(map(float, arr2_str.split()))

                if len(arr1) != len(arr2):
                    print("Ошибка: массивы разного размера!")
                    return MenuEvent.ERROR

                self.context['task_data'] = (arr1, arr2)
                print(f"\n✓ Массивы сохранены: {len(arr1)} элементов")

            elif task_num == 3:
                # Ввод матрицы
                rows = int(await self._async_input("Количество строк: "))
                cols = int(await self._async_input("Количество столбцов: "))

                matrix = []
                print("\nВведите матрицу по строкам:")
                for i in range(rows):
                    row_str = await self._async_input(f"Строка {i+1}: ")
                    row = list(map(float, row_str.split()))
                    if len(row) != cols:
                        print(f"Ошибка: нужно {cols} чисел!")
                        return MenuEvent.ERROR
                    matrix.append(row)

                self.context['task_data'] = matrix
                print(f"\n✓ Матрица сохранена: {rows}x{cols}")

            elif task_num == 8:
                # Ввод двух массивов для поиска общих чисел
                print("\n--- Массив 1 ---")
                arr1_str = await self._async_input("Введите числа через пробел: ")
                arr1 = list(map(int, arr1_str.split()))

                print("\n--- Массив 2 ---")
                arr2_str = await self._async_input("Введите числа через пробел: ")
                arr2 = list(map(int, arr2_str.split()))

                self.context['task_data'] = (arr1, arr2)
                print(f"\n✓ Массивы сохранены: {len(arr1)} и {len(arr2)} элементов")

            return MenuEvent.INPUT_COMPLETE

        except ValueError as e:
            print(f"Ошибка ввода чисел: {e}")
            return MenuEvent.ERROR
        except Exception as e:
            print(f"Ошибка: {e}")
            return MenuEvent.ERROR

    async def _state_auto_input(self) -> Optional[MenuEvent]:
        """Корутина автоматического ввода."""
        task_num = self.context.get('selected_task', 1)

        print("\n" + "=" * 40)
        print(f"АВТОМАТИЧЕСКИЙ ВВОД ДЛЯ ЗАДАНИЯ {task_num}")
        print("=" * 40)

        try:
            # Имитация задержки генерации
            print("Генерация данных...")
            await asyncio.sleep(1)

            if task_num == 1:
                # Генерация двух массивов
                size = random.randint(5, 10)
                arr1 = [random.randint(1, 100) for _ in range(size)]
                arr2 = [random.randint(1, 100) for _ in range(size)]

                self.context['task_data'] = (arr1, arr2)
                print(f"\n✓ Сгенерированы 2 массива по {size} элементов")
                print(f"  Массив 1: {arr1}")
                print(f"  Массив 2: {arr2}")

            elif task_num == 3:
                # Генерация матрицы
                rows = random.randint(3, 6)
                cols = random.randint(3, 6)
                matrix = [[random.randint(1, 20) for _ in range(cols)]
                         for _ in range(rows)]

                self.context['task_data'] = matrix
                print(f"\n✓ Сгенерирована матрица {rows}x{cols}")
                for i, row in enumerate(matrix):
                    print(f"  Строка {i+1}: {row}")

            elif task_num == 8:
                # Генерация массивов с возможными перевернутыми числами
                size = random.randint(5, 8)
                arr1 = []
                arr2 = []

                # Генерируем некоторые перевернутые пары
                for _ in range(size):
                    num = random.randint(10, 99)
                    arr1.append(num)
                    # С вероятностью 30% добавляем перевернутое число во второй массив
                    if random.random() < 0.3:
                        arr2.append(int(str(num)[::-1]))
                    else:
                        arr2.append(random.randint(10, 99))

                self.context['task_data'] = (arr1, arr2)
                print(f"\n✓ Сгенерированы 2 массива по {size} элементов")
                print(f"  Массив 1: {arr1}")
                print(f"  Массив 2: {arr2}")
                print("  (некоторые числа могут быть перевернутыми версиями)")

            return MenuEvent.INPUT_COMPLETE

        except Exception as e:
            print(f"Ошибка генерации: {e}")
            return MenuEvent.ERROR

    async def _state_execution(self) -> Optional[MenuEvent]:
        """Корутина выполнения алгоритма."""
        task_num = self.context.get('selected_task', 1)
        task_data = self.context.get('task_data')

        print("\n" + "=" * 60)
        print(f"ВЫПОЛНЕНИЕ АЛГОРИТМА {task_num}")
        print("=" * 60)

        if not task_data:
            print("Ошибка: данные не введены!")
            return MenuEvent.ERROR

        try:
            print("Выполнение алгоритма...")

            # Имитация длительных вычислений
            await asyncio.sleep(2)

            # Здесь должна быть реальная логика алгоритма
            # Для демонстрации просто создаем заглушку

            if task_num == 1:
                arr1, arr2 = task_data
                # Имитация алгоритма 1
                result = [a + b if a != b else 0 for a, b in zip(
                    sorted(arr1, reverse=True),
                    sorted(arr2)
                )]
                result = sorted(result)

            elif task_num == 3:
                matrix = task_data
                # Имитация поворота матрицы (по часовой стрелке)
                rows = len(matrix)
                cols = len(matrix[0])
                result = [[0 for _ in range(rows)] for _ in range(cols)]
                for i in range(rows):
                    for j in range(cols):
                        result[j][rows - 1 - i] = matrix[i][j]

            elif task_num == 8:
                arr1, arr2 = task_data
                # Имитация поиска общих чисел
                common = set(arr1) & set(arr2)
                result = list(common)

            self.context['task_result'] = result
            print("✓ Алгоритм выполнен успешно!")

            return MenuEvent.EXECUTE

        except Exception as e:
            print(f"Ошибка выполнения: {e}")
            return MenuEvent.ERROR

    async def _state_result(self) -> Optional[MenuEvent]:
        """Корутина отображения результата."""
        task_num = self.context.get('selected_task', 1)
        task_data = self.context.get('task_data')
        result = self.context.get('task_result')

        print("\n" + "=" * 60)
        print(f"РЕЗУЛЬТАТ ВЫПОЛНЕНИЯ АЛГОРИТМА {task_num}")
        print("=" * 60)

        print("\nИсходные данные:")
        if task_num == 1:
            arr1, arr2 = task_data
            print(f"  Массив 1: {arr1}")
            print(f"  Массив 2: {arr2}")
        elif task_num == 3:
            matrix = task_data
            print(f"  Матрица {len(matrix)}x{len(matrix[0])}:")
            for row in matrix:
                print(f"    {row}")
        elif task_num == 8:
            arr1, arr2 = task_data
            print(f"  Массив 1: {arr1}")
            print(f"  Массив 2: {arr2}")

        print(f"\nРезультат: {result}")

        print("\n1. Вернуться в главное меню")
        print("2. Выход")

        choice = await self._async_input("\nВыберите: ")

        if choice == "1":
            return MenuEvent.BACK
        elif choice == "2":
            return MenuEvent.EXIT
        else:
            print("Неверный выбор!")
            return None

    async def _state_settings(self) -> Optional[MenuEvent]:
        """Корутина настроек."""
        print("\n" + "=" * 60)
        print("НАСТРОЙКИ")
        print("=" * 60)

        print("\n1. Настройки логирования")
        print("2. О системе")
        print("3. Назад")

        choice = await self._async_input("\nВыберите: ")

        if choice == "1":
            return MenuEvent.SELECT_MAIN
        elif choice == "2":
            await self._show_about()
            return None
        elif choice == "3":
            return MenuEvent.BACK
        else:
            print("Неверный выбор!")
            return None

    async def _state_logging_settings(self) -> Optional[MenuEvent]:
        """Корутина настроек логирования."""
        print("\n" + "=" * 60)
        print("НАСТРОЙКИ ЛОГИРОВАНИЯ")
        print("=" * 60)

        print("\n1. Уровень логирования: INFO")
        print("2. Уровень логирования: DEBUG")
        print("3. Уровень логирования: ERROR")
        print("4. Назад")

        choice = await self._async_input("\nВыберите уровень: ")

        if choice in ["1", "2", "3"]:
            levels = ["INFO", "DEBUG", "ERROR"]
            print(f"✓ Установлен уровень: {levels[int(choice)-1]}")
            await asyncio.sleep(1)
            return MenuEvent.BACK
        elif choice == "4":
            return MenuEvent.BACK
        else:
            print("Неверный выбор!")
            return None

    async def _state_error(self) -> Optional[MenuEvent]:
        """Корутина состояния ошибки."""
        error_msg = self.context.get('error_message', 'Неизвестная ошибка')

        print("\n" + "=" * 60)
        print("ОШИБКА")
        print("=" * 60)

        print(f"\n{error_msg}")

        print("\n1. Вернуться в главное меню")
        print("2. Выход")

        choice = await self._async_input("\nВыберите: ")

        if choice == "1":
            return MenuEvent.BACK
        elif choice == "2":
            return MenuEvent.EXIT
        else:
            return MenuEvent.EXIT

    async def _state_exit(self) -> Optional[MenuEvent]:
        """Корутина выхода."""
        print("\n" + "=" * 60)
        print("ВЫХОД ИЗ ПРОГРАММЫ")
        print("=" * 60)

        elapsed = datetime.now() - self.context['start_time']
        print(f"\nВремя работы: {elapsed.total_seconds():.1f} секунд")
        print("Спасибо за использование программы!")

        return None

    # ============================================================================
    # ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ
    # ============================================================================

    async def _async_input(self, prompt: str) -> str:
        """Асинхронный ввод с обработкой прерывания."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, input, prompt)

    async def _show_about(self):
        """Отображение информации о системе."""
        print("\n" + "=" * 60)
        print("О СИСТЕМЕ")
        print("=" * 60)

        print("\nАвтоматное программирование на корутинах")
        print("Реализация меню через конечный автомат")
        print("\nСостояния:")
        for state in MenuState:
            print(f"  - {state.value}")

        await asyncio.sleep(2)


# ============================================================================
# ТЕСТИРОВАНИЕ АВТОМАТА
# ============================================================================

def run_automaton_test():
    """Запуск теста автоматного программирования."""
    print("\n" + "=" * 60)
    print("ТЕСТ АВТОМАТНОГО ПРОГРАММИРОВАНИЯ")
    print("=" * 60)

    automaton = MenuAutomaton()

    try:
        # Запускаем корутины
        asyncio.run(automaton.run())

    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем")
    except Exception as e:
        print(f"\nКритическая ошибка: {e}")
        import traceback
        traceback.print_exc()


def test_state_transitions():
    """Тест переходов состояний автомата."""
    print("\n" + "=" * 60)
    print("ТЕСТ ПЕРЕХОДОВ СОСТОЯНИЙ")
    print("=" * 60)

    automaton = MenuAutomaton()

    # Тестируем переходы
    test_cases = [
        (MenuState.INITIAL, MenuEvent.START, MenuState.MAIN_MENU, "Старт → Главное меню"),
        (MenuState.MAIN_MENU, MenuEvent.SELECT_TASK, MenuState.TASK_SELECTION, "Главное → Выбор задачи"),
        (MenuState.TASK_SELECTION, MenuEvent.BACK, MenuState.MAIN_MENU, "Назад из выбора задачи"),
        (MenuState.MAIN_MENU, MenuEvent.SETTINGS, MenuState.SETTINGS, "Главное → Настройки"),
        (MenuState.SETTINGS, MenuEvent.BACK, MenuState.MAIN_MENU, "Назад из настроек"),
        (MenuState.MAIN_MENU, MenuEvent.EXIT, MenuState.EXIT, "Выход"),
    ]

    print("\nТестирование переходов:")
    for initial_state, event, expected_state, description in test_cases:
        automaton.state = initial_state
        success = automaton.transition(event)

        status = "✓" if success and automaton.state == expected_state else "✗"
        print(f"  {status} {description}: {initial_state} -> {event} -> {automaton.state}")

    print("\n✓ Тест переходов завершен")


async def test_coroutine_flow():
    """Тест потока корутин."""
    print("\n" + "=" * 60)
    print("ТЕСТ ПОТОКА КОРУТИН")
    print("=" * 60)

    automaton = MenuAutomaton()

    # Тестируем несколько состояний
    print("\nТестирование корутин состояний:")

    # Начальное состояние
    automaton.state = MenuState.INITIAL
    event = await automaton._state_initial()
    print(f"  INITIAL → {event}")

    # Главное меню (имитируем выбор)
    automaton.state = MenuState.MAIN_MENU
    print(f"  MAIN_MENU (корутина запущена)")

    # Состояние ошибки
    automaton.state = MenuState.ERROR
    automaton.context['error_message'] = 'Тестовая ошибка'
    event = await automaton._state_error()
    print(f"  ERROR → {event}")

    print("\n✓ Тест корутин завершен")


def demo_automaton_pattern():
    """Демонстрация шаблона автоматного программирования."""
    print("\n" + "=" * 60)
    print("ДЕМОНСТРАЦИЯ АВТОМАТНОГО ПРОГРАММИРОВАНИЯ")
    print("=" * 60)

    print("\nШаблон автомата:")
    print("1. Определение состояний (enum)")
    print("2. Определение событий (enum)")
    print("3. Таблица переходов (словарь)")
    print("4. Корутины для каждого состояния")
    print("5. Основной цикл автомата")

    print("\nПример таблицы переходов:")
    automaton = MenuAutomaton()
    for state, transitions in automaton.transition_table.items():
        if transitions:
            print(f"\n{state.value}:")
            for event, next_state in transitions.items():
                print(f"  {event.value} → {next_state.value}")

    print("\n✓ Демонстрация завершена")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Тестирование автоматного программирования')
    parser.add_argument('--test', choices=['transitions', 'coroutines', 'demo', 'run'],
                       default='run', help='Тип теста')

    args = parser.parse_args()

    if args.test == 'transitions':
        test_state_transitions()
    elif args.test == 'coroutines':
        asyncio.run(test_coroutine_flow())
    elif args.test == 'demo':
        demo_automaton_pattern()
    else:
        run_automaton_test()
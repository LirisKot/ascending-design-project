"""
ДЕМОНСТРАЦИЯ СИСТЕМЫ ЛОГИРОВАНИЯ
================================

Скрипт демонстрирует работу системы логирования с разными уровнями.
Показывает как включается/выключается логирование при изменении уровня.
"""

import logging
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.logger import setup_logging, get_logger, FunctionLogger


def demonstrate_logging_levels():
    """
    Демонстрация различных уровней логирования.
    """
    print("=" * 60)
    print("ДЕМОНСТРАЦИЯ СИСТЕМЫ ЛОГИРОВАНИЯ")
    print("=" * 60)

    # Тестовая функция с логированием
    @FunctionLogger('demo')
    def test_function(x, y):
        """Тестовая функция для демонстрации логирования."""
        return x * y

    print("\n1. ТЕСТ С УРОВНЕМ INFO (все сообщения видны):")
    print("-" * 40)

    # Устанавливаем уровень INFO
    logger = setup_logging(log_level=logging.INFO, log_to_file=False)

    # Выполняем операции с логированием
    logger.debug("Это сообщение DEBUG - не будет показано")
    logger.info("Это сообщение INFO - будет показано")
    logger.warning("Это сообщение WARNING - будет показано")
    logger.error("Это сообщение ERROR - будет показано")

    result = test_function(5, 3)
    print(f"Результат функции: {result}")

    print("\n2. ТЕСТ С УРОВНЕМ CRITICAL (только критические):")
    print("-" * 40)

    # Меняем уровень на CRITICAL
    logger.setLevel(logging.CRITICAL)
    for handler in logger.handlers:
        handler.setLevel(logging.CRITICAL)

    print("Уровень логирования изменен на CRITICAL")
    print("Теперь будут показаны только CRITICAL сообщения:")

    logger.debug("Это сообщение DEBUG - НЕ будет показано")
    logger.info("Это сообщение INFO - НЕ будет показано")
    logger.warning("Это сообщение WARNING - НЕ будет показано")
    logger.error("Это сообщение ERROR - НЕ будет показано")
    logger.critical("Это сообщение CRITICAL - будет показано")

    # Функция всё равно выполнится, но без логирования вызова
    result = test_function(10, 2)
    print(f"Результат функции: {result} (логирование вызова отключено)")

    print("\n3. ВОССТАНОВЛЕНИЕ УРОВНЯ INFO:")
    print("-" * 40)

    # Возвращаем уровень INFO
    logger.setLevel(logging.INFO)
    for handler in logger.handlers:
        handler.setLevel(logging.INFO)

    logger.info("Уровень логирования восстановлен на INFO")
    logger.info("Все сообщения снова видны")

    print("\n4. ДЕМОНСТРАЦИЯ ЗАПИСИ В ФАЙЛ:")
    print("-" * 40)

    # Создаем логгер с записью в файл
    file_logger = setup_logging(
        log_level=logging.INFO,
        log_to_file=True,
        max_file_size=1024 * 10,  # 10KB для демонстрации
        backup_count=2
    )

    file_logger.info("Это сообщение записано в файл логов")
    file_logger.info(f"Файлы логов создаются в папке: logs/")
    file_logger.info("При достижении размера 10KB создается новый файл")

    print("✓ Логи записаны в файл в папке logs/")
    print("  Размер файла ограничен 10KB, создается до 2 резервных копий")

    print("\n" + "=" * 60)
    print("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
    print("=" * 60)


def demonstrate_user_actions_logging():
    """
    Демонстрация логирования действий пользователя.
    """
    print("\n\nДЕМОНСТРАЦИЯ ЛОГИРОВАНИЯ ДЕЙСТВИЙ ПОЛЬЗОВАТЕЛЯ:")
    print("=" * 60)

    logger = get_logger('user_actions')

    # Симуляция действий пользователя
    actions = [
        ("Пользователь вошел в систему", "user_login"),
        ("Пользователь выбрал задание 1", "task_selection"),
        ("Пользователь ввел данные (ручной ввод)", "data_input"),
        ("Пользователь выполнил алгоритм", "algorithm_execution"),
        ("Пользователь просмотрел результат", "result_view"),
        ("Пользователь вышел из системы", "user_logout"),
    ]

    for action_description, action_type in actions:
        logger.info(f"ДЕЙСТВИЕ ПОЛЬЗОВАТЕЛЯ: {action_description} [{action_type}]")
        print(f"✓ Записано в лог: {action_description}")

    print("\n✓ Все действия пользователя записаны в лог-файл")
    print("  Можно просмотреть историю действий для отладки или аудита")


if __name__ == "__main__":
    demonstrate_logging_levels()
    demonstrate_user_actions_logging()

    print("\n\nИНСТРУКЦИЯ ПО ИСПОЛЬЗОВАНИЮ ЛОГИРОВАНИЯ:")
    print("=" * 60)
    print("1. В главном меню выберите пункт 6 для изменения уровня логирования")
    print("2. По умолчанию используется уровень INFO (все сообщения)")
    print("3. Уровень CRITICAL отключает все сообщения кроме критических")
    print("4. Логи сохраняются в папке logs/ с ротацией по размеру")
    print("5. Для просмотра логов откройте файлы в папке logs/")
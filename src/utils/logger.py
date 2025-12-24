"""
МОДУЛЬ ЛОГИРОВАНИЯ
==================

Настройка и конфигурация системы логирования для всего приложения.
Поддерживает запись в файл и консоль с различными уровнями логирования.
"""

import logging
import sys
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler


def setup_logging(log_level=logging.INFO, log_to_file=True, max_file_size=1024 * 1024, backup_count=5):
    """
    Настройка системы логирования.

    Параметры:
    ----------
    log_level : int
        Уровень логирования (по умолчанию INFO)
    log_to_file : bool
        Записывать ли логи в файл (по умолчанию True)
    max_file_size : int
        Максимальный размер лог-файла в байтах (по умолчанию 1MB)
    backup_count : int
        Количество резервных копий лог-файлов

    Возвращает:
    -----------
    logging.Logger
        Сконфигурированный логгер
    """
    # Создаем логгер для приложения
    logger = logging.getLogger('ascending_design_app')
    logger.setLevel(log_level)

    # Очищаем существующие обработчики (чтобы не дублировались)
    logger.handlers.clear()

    # Формат для сообщений
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 1. Обработчик для консоли
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 2. Обработчик для файла (если включено)
    if log_to_file:
        # Создаем папку для логов если её нет
        log_dir = 'logs'
        os.makedirs(log_dir, exist_ok=True)

        # Имя файла с текущей датой
        log_filename = f"{log_dir}/app_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

        # Ротация логов (автоматическое создание новых файлов при достижении размера)
        file_handler = RotatingFileHandler(
            log_filename,
            maxBytes=max_file_size,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        logger.info(f"Логирование в файл: {log_filename}")

    logger.info(f"Система логирования инициализирована с уровнем {logging.getLevelName(log_level)}")
    return logger


def get_logger(name=None):
    """
    Получение логгера по имени.

    Параметры:
    ----------
    name : str or None
        Имя логгера. Если None, возвращается корневой логгер.

    Возвращает:
    -----------
    logging.Logger
        Запрошенный логгер
    """
    if name:
        return logging.getLogger(f'ascending_design_app.{name}')
    return logging.getLogger('ascending_design_app')


# Создаем глобальный логгер по умолчанию
app_logger = setup_logging()


class FunctionLogger:
    """
    Декоратор для логирования вызовов функций.

    Пример использования:
    @FunctionLogger()
    def my_function(arg1, arg2):
        return arg1 + arg2
    """

    def __init__(self, logger_name=None, level=logging.INFO):
        """
        Инициализация декоратора логирования.

        Параметры:
        ----------
        logger_name : str or None
            Имя логгера (если None, используется корневой)
        level : int
            Уровень логирования для сообщений
        """
        self.logger = get_logger(logger_name)
        self.level = level

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            # Логируем вызов функции
            self.logger.log(
                self.level,
                f"ВЫЗОВ ФУНКЦИИ: {func.__name__} - "
                f"аргументы: {args if len(args) <= 3 else f'{len(args)} args'}, "
                f"ключевые слова: {kwargs if kwargs else 'нет'}"
            )

            try:
                # Выполняем функцию
                result = func(*args, **kwargs)

                # Логируем успешное выполнение
                self.logger.log(
                    self.level,
                    f"ФУНКЦИЯ ВЫПОЛНЕНА: {func.__name__} - "
                    f"результат тип: {type(result).__name__}"
                )

                return result

            except Exception as e:
                # Логируем ошибку
                self.logger.error(
                    f"ОШИБКА В ФУНКЦИИ: {func.__name__} - {type(e).__name__}: {str(e)}"
                )
                raise

        # Сохраняем оригинальное имя и документацию
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__

        return wrapper


# Экспорт основных функций
__all__ = ['setup_logging', 'get_logger', 'FunctionLogger', 'app_logger']
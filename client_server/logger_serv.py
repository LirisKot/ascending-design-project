"""
ЛОГГЕР СЕРВЕРА
==============

Логирование действий сервера в файл и консоль.
"""

import logging
import sys
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler


class ServerLogger:
    """Логгер для сервера."""

    def __init__(self, log_file: str = 'server.log'):
        """
        Инициализация логгера.

        Args:
            log_file: Путь к файлу логов
        """
        # Создаем директорию для логов если её нет
        log_dir = 'logs'
        os.makedirs(log_dir, exist_ok=True)

        log_path = os.path.join(log_dir, log_file)

        # Настройка логгера
        self.logger = logging.getLogger('server')
        self.logger.setLevel(logging.DEBUG)
        self.logger.handlers.clear()  # Очищаем старые обработчики

        # Формат сообщений
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Обработчик для файла
        file_handler = RotatingFileHandler(
            log_path,
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Обработчик для консоли
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(asctime)s - SERVER - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        self.logger.info(f"Логгер сервера инициализирован. Логи в: {log_path}")

    def info(self, message: str):
        """Логирование информационного сообщения."""
        self.logger.info(message)

    def debug(self, message: str):
        """Логирование отладочного сообщения."""
        self.logger.debug(message)

    def warning(self, message: str):
        """Логирование предупреждения."""
        self.logger.warning(message)

    def error(self, message: str):
        """Логирование ошибки."""
        self.logger.error(message)

    def critical(self, message: str):
        """Логирование критической ошибки."""
        self.logger.critical(message)

    def client_message(self, client_name: str, message: str):
        """
        Логирование сообщения от клиента в специальном формате.

        Args:
            client_name: Имя клиента
            message: Сообщение
        """
        timestamp = datetime.now().strftime('%H:%M:%S')
        formatted_message = f"{timestamp} {client_name}: {message}"

        # Записываем в файл
        self.logger.info(formatted_message)

        # Выводим в консоль
        print(formatted_message)

    def get_now(self) -> str:
        """Получение текущего времени в формате для логов."""
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
"""
ЛОГГЕР КЛИЕНТА
==============

Логирование действий клиента.
"""

import logging
import sys
import os
from datetime import datetime


class ClientLogger:
    """Логгер для клиента."""

    def __init__(self, client_name: str):
        """
        Инициализация логгера.

        Args:
            client_name: Имя клиента
        """
        self.client_name = client_name

        # Настройка логгера
        self.logger = logging.getLogger(f'client_{client_name}')
        self.logger.setLevel(logging.DEBUG)
        self.logger.handlers.clear()

        # Формат для файла
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Создаем директорию для логов клиента
        log_dir = f'logs/clients'
        os.makedirs(log_dir, exist_ok=True)

        # Файл логов для этого клиента
        log_file = os.path.join(log_dir, f'{client_name}.log')
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

        self.logger.info(f"Логгер клиента {client_name} инициализирован")

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

    def client_message(self, message: str):
        """
        Логирование сообщения клиента в специальном формате для консоли.

        Args:
            message: Сообщение
        """
        timestamp = datetime.now().strftime('%H:%M:%S')
        formatted_message = f"{timestamp} {self.client_name}: {message}"

        # Выводим в консоль
        print(formatted_message)

        # Записываем в файл
        self.logger.info(formatted_message)
# setup_paths.py
"""
Настройка путей Python для проекта.
Используй этот файл в начале всех модулей.
"""

import sys
import os


def setup_paths():
    """Настройка путей Python."""
    # Получаем корень проекта
    project_root = os.path.dirname(os.path.abspath(__file__))

    # Добавляем пути
    paths_to_add = [
        project_root,  # корень
        os.path.join(project_root, 'algorithms'),
        os.path.join(project_root, 'utils'),
        os.path.join(project_root, 'client_server'),
    ]

    for path in paths_to_add:
        if path not in sys.path:
            sys.path.insert(0, path)

    return project_root


# Автоматически вызываем при импорте
setup_paths()
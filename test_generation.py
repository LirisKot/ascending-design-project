# test_generation.py в корне проекта
import sys
import os

# Добавляем пути
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'algorithms'))

print("=" * 60)
print("ТЕСТ ГЕНЕРАЦИИ МАССИВОВ")
print("=" * 60)

try:
    from algorithms.algorithm1 import main

    # Запускаем автономный режим алгоритма
    main()

except ImportError as e:
    print(f"✗ Ошибка импорта: {e}")
    print("\nТекущие пути Python:")
    for i, p in enumerate(sys.path[:10]):
        print(f"  {i + 1}. {p}")
except Exception as e:
    print(f"✗ Ошибка: {e}")
    import traceback

    traceback.print_exc()
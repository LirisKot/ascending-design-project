# multithreading_test.py
import sys
import os
import threading
import time
import random
from datetime import datetime
import queue

# Добавляем путь для импорта
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    from client import Client
    from protocols import TaskType

    print("✓ Модули успешно импортированы")
except ImportError as e:
    print(f"✗ Ошибка импорта: {e}")
    sys.exit(1)


class ThreadingMonitor:
    """Мониторинг состояния потоков."""

    def __init__(self):
        self.threads_info = []
        self.lock = threading.Lock()

    def log_thread(self, thread_name, action):
        """Логирование действий потоков."""
        with self.lock:
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            info = f"[{timestamp}] Поток '{thread_name}': {action}"
            self.threads_info.append(info)
            print(info)

    def get_summary(self):
        """Получение сводки по потокам."""
        with self.lock:
            return {
                'total_events': len(self.threads_info),
                'events': self.threads_info[-20:]  # Последние 20 событий
            }


def test_concurrent_connections():
    """Тест конкурентных подключений."""
    print("\n" + "=" * 60)
    print("ТЕСТ КОНКУРЕНТНЫХ ПОДКЛЮЧЕНИЙ")
    print("=" * 60)

    monitor = ThreadingMonitor()
    clients = []
    results = queue.Queue()

    def client_task(client_id):
        """Задача для одного клиента."""
        monitor.log_thread(f"Client-{client_id}", "запущен")

        client = Client(client_name=f"ConcurrentClient-{client_id}")

        start_time = time.time()
        connected = client.connect()
        connect_time = time.time() - start_time

        if connected:
            monitor.log_thread(f"Client-{client_id}", f"подключился за {connect_time:.3f}с")
            time.sleep(random.uniform(0.5, 1.5))  # Имитация работы

            # Выполняем простую задачу
            response = client.execute_task(
                TaskType.GENERATE_ARRAY,
                {'size': random.randint(5, 15)}
            )

            task_time = time.time() - start_time - connect_time

            if response and response.success:
                monitor.log_thread(f"Client-{client_id}", f"задача выполнена за {task_time:.3f}с")
            else:
                monitor.log_thread(f"Client-{client_id}", f"ошибка задачи")

            client.disconnect()
            monitor.log_thread(f"Client-{client_id}", f"отключился, общее время: {time.time() - start_time:.3f}с")
        else:
            monitor.log_thread(f"Client-{client_id}", f"ошибка подключения")

        results.put((client_id, connected, time.time() - start_time))

    # Запускаем много клиентов одновременно
    num_clients = 10
    threads = []

    monitor.log_thread("MAIN", f"запуск {num_clients} клиентов одновременно")

    for i in range(num_clients):
        thread = threading.Thread(target=client_task, args=(i,), daemon=True)
        threads.append(thread)

    # Запускаем ВСЕХ одновременно
    for thread in threads:
        thread.start()
        time.sleep(0.01)  # Минимальная задержка

    monitor.log_thread("MAIN", "все клиенты запущены")

    # Ждем завершения
    for thread in threads:
        thread.join(timeout=30)

    # Анализ результатов
    successful = 0
    total_time = 0
    while not results.empty():
        client_id, connected, duration = results.get()
        if connected:
            successful += 1
        total_time += duration

    print(f"\nРезультаты:")
    print(f"  Успешных подключений: {successful}/{num_clients}")
    print(f"  Среднее время на клиента: {total_time / num_clients:.2f}с")

    return successful == num_clients


def test_parallel_requests():
    """Тест параллельных запросов от одного клиента."""
    print("\n" + "=" * 60)
    print("ТЕСТ ПАРАЛЛЕЛЬНЫХ ЗАПРОСОВ")
    print("=" * 60)

    monitor = ThreadingMonitor()

    # Подключаем один клиент
    client = Client(client_name="ParallelClient")

    if not client.connect():
        print("✗ Не удалось подключить клиент")
        return False

    monitor.log_thread("MAIN", "клиент подключен, запуск параллельных запросов")

    results = queue.Queue()
    request_times = []

    def send_request(request_id, task_type, params):
        """Отправка одного запроса."""
        start_time = time.time()
        monitor.log_thread(f"Request-{request_id}", "отправлен")

        response = client.execute_task(task_type, params)

        elapsed = time.time() - start_time
        monitor.log_thread(f"Request-{request_id}", f"ответ за {elapsed:.3f}с")

        results.put((request_id, elapsed, response.success if response else False))
        request_times.append(elapsed)

    # Создаем разные задачи
    tasks = []
    for i in range(8):
        if i % 3 == 0:
            tasks.append((TaskType.GENERATE_ARRAY, {'size': random.randint(5, 20)}))
        elif i % 3 == 1:
            tasks.append((TaskType.GENERATE_MATRIX, {'rows': random.randint(3, 8), 'cols': random.randint(3, 8)}))
        else:
            tasks.append((TaskType.TASK1_SUM_ARRAYS, {
                'array1': list(range(random.randint(5, 10))),
                'array2': list(range(random.randint(5, 10)))
            }))

    # Запускаем все запросы почти одновременно
    threads = []
    for i, (task_type, params) in enumerate(tasks):
        thread = threading.Thread(
            target=send_request,
            args=(i, task_type, params),
            daemon=True
        )
        threads.append(thread)

    start_time = time.time()

    for thread in threads:
        thread.start()
        time.sleep(0.05)  # Очень маленькая задержка

    # Ждем завершения
    for thread in threads:
        thread.join(timeout=15)

    total_elapsed = time.time() - start_time

    # Анализ результатов
    successful = 0
    total_request_time = 0
    while not results.empty():
        request_id, elapsed, success = results.get()
        if success:
            successful += 1
        total_request_time += elapsed

    print(f"\nРезультаты:")
    print(f"  Успешных запросов: {successful}/{len(tasks)}")
    print(f"  Общее время выполнения: {total_elapsed:.2f}с")
    print(f"  Суммарное время запросов: {total_request_time:.2f}с")
    print(f"  Параллельность: {total_request_time / total_elapsed:.2f}x")

    if request_times:
        print(f"  Минимальное время: {min(request_times):.3f}с")
        print(f"  Максимальное время: {max(request_times):.3f}с")
        print(f"  Среднее время: {sum(request_times) / len(request_times):.3f}с")

    client.disconnect()

    return successful == len(tasks)


def test_server_capacity():
    """Тест емкости сервера - много клиентов, много запросов."""
    print("\n" + "=" * 60)
    print("ТЕСТ ЕМКОСТИ СЕРВЕРА")
    print("=" * 60)

    monitor = ThreadingMonitor()
    all_results = queue.Queue()

    def client_with_requests(client_id):
        """Клиент с несколькими запросами."""
        client_name = f"CapacityClient-{client_id}"
        monitor.log_thread(client_name, "запущен")

        client = Client(client_name=client_name)

        if client.connect():
            monitor.log_thread(client_name, "подключен")

            request_results = []
            for req_id in range(3):  # По 3 запроса от каждого клиента
                task_type = random.choice([
                    TaskType.GENERATE_ARRAY,
                    TaskType.GENERATE_MATRIX
                ])

                if task_type == TaskType.GENERATE_ARRAY:
                    params = {'size': random.randint(5, 15)}
                else:
                    params = {'rows': random.randint(3, 6), 'cols': random.randint(3, 6)}

                start_time = time.time()
                response = client.execute_task(task_type, params)
                elapsed = time.time() - start_time

                request_results.append({
                    'success': response.success if response else False,
                    'time': elapsed
                })

                time.sleep(random.uniform(0.1, 0.3))

            client.disconnect()
            monitor.log_thread(client_name, "отключен")

            all_results.put({
                'client_id': client_id,
                'requests': request_results
            })
        else:
            monitor.log_thread(client_name, "ошибка подключения")

    # Запускаем много клиентов
    num_clients = 15  # 15 клиентов по 3 запроса = 45 запросов
    threads = []

    monitor.log_thread("MAIN", f"запуск {num_clients} клиентов")

    # Запускаем группами по 3 клиента
    group_size = 3
    for group in range(0, num_clients, group_size):
        for i in range(group, min(group + group_size, num_clients)):
            thread = threading.Thread(
                target=client_with_requests,
                args=(i,),
                daemon=True
            )
            threads.append(thread)
            thread.start()
            time.sleep(0.1)

        monitor.log_thread("MAIN", f"группа {group // group_size + 1} запущена")
        time.sleep(0.5)  # Пауза между группами

    # Ждем завершения
    for thread in threads:
        thread.join(timeout=60)

    # Анализ результатов
    clients_data = []
    while not all_results.empty():
        clients_data.append(all_results.get())

    total_requests = 0
    successful_requests = 0
    total_time = 0

    for client_data in clients_data:
        for req in client_data['requests']:
            total_requests += 1
            if req['success']:
                successful_requests += 1
            total_time += req['time']

    print(f"\nРезультаты теста емкости:")
    print(f"  Клиентов: {len(clients_data)}")
    print(f"  Всего запросов: {total_requests}")
    print(f"  Успешных запросов: {successful_requests}")
    print(f"  Общее время выполнения: {total_time:.2f}с")
    print(f"  Среднее время на запрос: {total_time / total_requests if total_requests > 0 else 0:.3f}с")

    return len(clients_data) > 0


def test_thread_safety():
    """Тест потокобезопасности клиента."""
    print("\n" + "=" * 60)
    print("ТЕСТ ПОТОКОБЕЗОПАСНОСТИ")
    print("=" * 60)

    # Создаем один клиент
    client = Client(client_name="ThreadSafeTest")

    if not client.connect():
        print("✗ Не удалось подключить клиент")
        return False

    print("✓ Клиент подключен")
    print("Тестируем конкурентный доступ к методам клиента...")

    counter = {'value': 0, 'lock': threading.Lock()}
    errors = []

    def concurrent_access(thread_id):
        """Конкурентный доступ к клиенту."""
        try:
            # Одновременно получаем информацию о клиенте
            info1 = client.get_client_info()

            # Одновременно отправляем heartbeat
            client.send_heartbeat()

            # Одновременно проверяем подключение
            connected = client.is_connected()

            # Запоминаем, что поток успешно выполнился
            with counter['lock']:
                counter['value'] += 1

            return True

        except Exception as e:
            errors.append(f"Поток {thread_id}: {e}")
            return False

    # Запускаем много потоков с доступом к одному клиенту
    threads = []
    for i in range(20):
        thread = threading.Thread(
            target=concurrent_access,
            args=(i,),
            daemon=True
        )
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join(timeout=5)

    client.disconnect()

    print(f"\nРезультаты:")
    print(f"  Успешных потоков: {counter['value']}/20")

    if errors:
        print(f"  Ошибки: {len(errors)}")
        for error in errors[:5]:  # Показываем первые 5 ошибок
            print(f"    - {error}")
        if len(errors) > 5:
            print(f"    ... и еще {len(errors) - 5} ошибок")

    success = counter['value'] == 20 and len(errors) == 0
    print(f"  Результат: {'✓ УСПЕХ' if success else '✗ ЕСТЬ ПРОБЛЕМЫ'}")

    return success


def main():
    """Основная функция тестирования."""
    print("=" * 60)
    print("КОМПЛЕКСНЫЙ ТЕСТ МНОГОПОТОЧНОСТИ")
    print("=" * 60)
    print("Убедитесь, что сервер запущен на localhost:8888")
    print()

    time.sleep(2)  # Даем время прочитать сообщение

    tests = [
        ("Конкурентные подключения", test_concurrent_connections),
        ("Параллельные запросы", test_parallel_requests),
        ("Емкость сервера", test_server_capacity),
        ("Потокобезопасность", test_thread_safety)
    ]

    results = []

    for test_name, test_func in tests:
        print(f"\n>>> Запуск теста: {test_name}")
        print("-" * 40)

        try:
            start_time = time.time()
            success = test_func()
            elapsed = time.time() - start_time

            result = {
                'name': test_name,
                'success': success,
                'time': elapsed
            }
            results.append(result)

            status = "✓ ПРОЙДЕН" if success else "✗ НЕ ПРОЙДЕН"
            print(f"\nТест '{test_name}' {status} за {elapsed:.2f}с")

        except Exception as e:
            print(f"\n✗ Тест '{test_name}' ВЫЗВАЛ ИСКЛЮЧЕНИЕ: {e}")
            import traceback
            traceback.print_exc()

            results.append({
                'name': test_name,
                'success': False,
                'time': 0,
                'error': str(e)
            })

        time.sleep(1)  # Пауза между тестами

    # Сводка результатов
    print("\n" + "=" * 60)
    print("СВОДКА РЕЗУЛЬТАТОВ")
    print("=" * 60)

    passed = sum(1 for r in results if r['success'])
    total = len(results)

    print(f"\nВсего тестов: {total}")
    print(f"Пройдено: {passed}")
    print(f"Не пройдено: {total - passed}")

    for result in results:
        status = "✓" if result['success'] else "✗"
        print(f"  {status} {result['name']}: {result['time']:.2f}с")

    print("\n" + "=" * 60)

    if passed == total:
        print("ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО! ✓")
        print("Многопоточность работает корректно.")
    else:
        print("НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОЙДЕНЫ.")
        print("Рекомендуется проверить:")
        print("  1. Потокобезопасность структур данных")
        print("  2. Корректность завершения потоков")
        print("  3. Обработку ошибок в потоках")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nТестирование прервано пользователем")
    except Exception as e:
        print(f"\nКритическая ошибка: {e}")
        import traceback

        traceback.print_exc()
# concurrent_test.py
import threading
import time
from client import Client
from protocols import TaskType


def concurrent_request(client_name, task_type, params, results, index):
    """Отправка одного запроса."""
    client = Client(client_name=client_name)

    if client.connect():
        start = time.time()
        response = client.execute_task(task_type, params)
        elapsed = time.time() - start

        results[index] = {
            'success': response.success if response else False,
            'time': elapsed,
            'client': client_name
        }

        client.disconnect()


def test_concurrent_requests():
    """Тест конкурентных запросов."""
    num_requests = 5
    results = [None] * num_requests
    threads = []

    print(f"Запуск {num_requests} конкурентных запросов...")

    for i in range(num_requests):
        thread = threading.Thread(
            target=concurrent_request,
            args=(
                f"Concurrent_{i}",
                TaskType.GENERATE_MATRIX,
                {'rows': 5, 'cols': 5},
                results,
                i
            )
        )
        threads.append(thread)

    # Запускаем все одновременно
    for thread in threads:
        thread.start()

    # Небольшая задержка для одновременного старта
    time.sleep(0.1)

    start_time = time.time()

    # Ждем завершения
    for thread in threads:
        thread.join()

    total_time = time.time() - start_time

    print(f"\nРезультаты конкурентных запросов:")
    print(f"Общее время: {total_time:.2f}с")

    successful = sum(1 for r in results if r and r['success'])
    print(f"Успешных: {successful}/{num_requests}")

    for i, result in enumerate(results):
        if result:
            print(f"  Запрос {i}: {result['client']} - {result['time']:.2f}с")


if __name__ == "__main__":
    test_concurrent_requests()
# load_test.py
import threading
import time
from client import Client


def load_test_client(client_id, num_requests=10):
    """Клиент для нагрузочного теста."""
    client = Client(client_name=f"LoadClient_{client_id}")

    if client.connect():
        print(f"Клиент {client_id} подключен")

        for i in range(num_requests):
            # Отправляем разные типы задач
            import random
            from protocols import TaskType

            task_types = [
                TaskType.GENERATE_ARRAY,
                TaskType.GENERATE_MATRIX,
                TaskType.TASK1_SUM_ARRAYS
            ]

            task_type = random.choice(task_types)

            if task_type == TaskType.GENERATE_ARRAY:
                params = {'size': random.randint(5, 20)}
            elif task_type == TaskType.GENERATE_MATRIX:
                params = {'rows': random.randint(3, 10), 'cols': random.randint(3, 10)}
            else:
                params = {
                    'array1': list(range(random.randint(5, 15))),
                    'array2': list(range(random.randint(5, 15)))
                }

            start_time = time.time()
            response = client.execute_task(task_type, params)
            elapsed = time.time() - start_time

            print(f"Клиент {client_id}, запрос {i + 1}: {task_type.value} за {elapsed:.2f}с")
            time.sleep(random.uniform(0.1, 0.5))

        client.disconnect()
        print(f"Клиент {client_id} отключен")


def run_load_test(num_clients=5, requests_per_client=20):
    """Запуск нагрузочного теста."""
    threads = []

    for i in range(num_clients):
        thread = threading.Thread(
            target=load_test_client,
            args=(i, requests_per_client),
            daemon=True
        )
        threads.append(thread)

    # Запускаем все потоки
    for thread in threads:
        thread.start()
        time.sleep(0.2)  # Небольшая задержка

    # Ждем завершения
    for thread in threads:
        thread.join(timeout=60)

    print(f"\nНагрузочный тест завершен: {num_clients} клиентов, {requests_per_client} запросов на каждого")


if __name__ == "__main__":
    # Сначала запустите сервер!
    run_load_test(num_clients=3, requests_per_client=5)
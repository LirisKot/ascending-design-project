"""
ПРОТОКОЛЫ ОБМЕНА ДАННЫМИ КЛИЕНТ-СЕРВЕР
=======================================
"""

import json
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class MessageType(Enum):
    """Типы сообщений."""
    CONNECT = "connect"
    DISCONNECT = "disconnect"
    TASK_REQUEST = "task_request"
    TASK_RESPONSE = "task_response"
    STATUS = "status"
    ERROR = "error"
    HEARTBEAT = "heartbeat"


class TaskType(Enum):
    """Типы задач."""
    TASK1_SUM_ARRAYS = "task1_sum_arrays"
    TASK3_ROTATE_MATRIX = "task3_rotate_matrix"
    TASK8_COMMON_NUMBERS = "task8_common_numbers"
    GENERATE_ARRAY = "generate_array"
    GENERATE_MATRIX = "generate_matrix"
    VALIDATE_DATA = "validate_data"


@dataclass
class Message:
    """Базовое сообщение."""
    message_id: str
    message_type: MessageType
    client_id: str
    timestamp: str
    data: Dict[str, Any]

    @classmethod
    def create(cls, message_type: MessageType, client_id: str, data: Dict[str, Any] = None):
        """Создание нового сообщения."""
        return cls(
            message_id=str(uuid.uuid4()),
            message_type=message_type,
            client_id=client_id,
            timestamp=datetime.now().isoformat(),
            data=data or {}
        )

    def to_json(self) -> str:
        """Преобразование в JSON."""
        return json.dumps({
            'message_id': self.message_id,
            'message_type': self.message_type.value,
            'client_id': self.client_id,
            'timestamp': self.timestamp,
            'data': self.data
        })

    @classmethod
    def from_json(cls, json_str: str) -> 'Message':
        """Создание из JSON."""
        data = json.loads(json_str)
        return cls(
            message_id=data['message_id'],
            message_type=MessageType(data['message_type']),
            client_id=data['client_id'],
            timestamp=data['timestamp'],
            data=data['data']
        )

    def to_dict(self) -> Dict[str, Any]:
        """Преобразование в словарь."""
        return asdict(self)


@dataclass
class TaskRequest:
    """Запрос на выполнение задачи."""
    task_type: TaskType
    parameters: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            'task_type': self.task_type.value,
            'parameters': self.parameters
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TaskRequest':
        return cls(
            task_type=TaskType(data['task_type']),
            parameters=data['parameters']
        )


@dataclass
class TaskResponse:
    """Ответ на выполнение задачи."""
    success: bool
    result: Optional[Any]
    error_message: Optional[str]
    execution_time: float  # время выполнения в секундах

    def to_dict(self) -> Dict[str, Any]:
        return {
            'success': self.success,
            'result': self.result,
            'error_message': self.error_message,
            'execution_time': self.execution_time
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TaskResponse':
        return cls(
            success=data['success'],
            result=data.get('result'),
            error_message=data.get('error_message'),
            execution_time=data['execution_time']
        )


class ClientServerProtocol:
    """Протокол обмена между клиентом и сервером."""

    @staticmethod
    def create_connect_message(client_id: str, client_name: str) -> Message:
        """Создание сообщения подключения."""
        return Message.create(
            message_type=MessageType.CONNECT,
            client_id=client_id,
            data={'client_name': client_name}
        )

    @staticmethod
    def create_disconnect_message(client_id: str) -> Message:
        """Создание сообщения отключения."""
        return Message.create(
            message_type=MessageType.DISCONNECT,
            client_id=client_id
        )

    @staticmethod
    def create_task_request(client_id: str, task_request: TaskRequest) -> Message:
        """Создание запроса на выполнение задачи."""
        return Message.create(
            message_type=MessageType.TASK_REQUEST,
            client_id=client_id,
            data=task_request.to_dict()
        )

    @staticmethod
    def create_task_response(client_id: str, task_response: TaskResponse) -> Message:
        """Создание ответа на выполнение задачи."""
        return Message.create(
            message_type=MessageType.TASK_RESPONSE,
            client_id=client_id,
            data=task_response.to_dict()
        )

    @staticmethod
    def create_error_message(client_id: str, error_message: str) -> Message:
        """Создание сообщения об ошибке."""
        return Message.create(
            message_type=MessageType.ERROR,
            client_id=client_id,
            data={'error': error_message}
        )

    @staticmethod
    def create_status_message(client_id: str, status: str) -> Message:
        """Создание статусного сообщения."""
        return Message.create(
            message_type=MessageType.STATUS,
            client_id=client_id,
            data={'status': status}
        )

    @staticmethod
    def create_heartbeat_message(client_id: str) -> Message:
        """Создание heartbeat сообщения."""
        return Message.create(
            message_type=MessageType.HEARTBEAT,
            client_id=client_id
        )
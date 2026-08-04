"""
Message Queue Manager for inter-agent communication
Uses Redis for fast, reliable message passing between agents
"""

import json
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
import redis
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class Message:
    """Structured message format for agent communication"""

    def __init__(
        self,
        from_agent: str,
        to_agent: str,
        message_type: str,
        payload: Dict[str, Any],
        priority: str = "normal",
        requires_response: bool = False,
    ):
        self.message_id = str(uuid.uuid4())
        self.from_agent = from_agent
        self.to_agent = to_agent
        self.message_type = message_type
        self.payload = payload
        self.priority = priority
        self.requires_response = requires_response
        self.timestamp = datetime.utcnow().isoformat()
        self.status = "pending"

    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary for JSON serialization"""
        return {
            "message_id": self.message_id,
            "from_agent": self.from_agent,
            "to_agent": self.to_agent,
            "message_type": self.message_type,
            "payload": self.payload,
            "priority": self.priority,
            "requires_response": self.requires_response,
            "timestamp": self.timestamp,
            "status": self.status,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Message":
        """Create message from dictionary"""
        msg = Message(
            from_agent=data["from_agent"],
            to_agent=data["to_agent"],
            message_type=data["message_type"],
            payload=data["payload"],
            priority=data.get("priority", "normal"),
            requires_response=data.get("requires_response", False),
        )
        msg.message_id = data["message_id"]
        msg.timestamp = data["timestamp"]
        msg.status = data.get("status", "pending")
        return msg


class QueueManager:
    """Manages message queues for agent communication"""

    def __init__(self):
        """Initialize Redis connection"""
        try:
            self.redis_client = redis.from_url(settings.REDIS_URL)
            self.redis_client.ping()
            logger.info("✓ Redis connection established")
        except Exception as e:
            logger.error(f"✗ Failed to connect to Redis: {e}")
            raise

    def send_message(self, message: Message) -> bool:
        """
        Send message to queue for target agent
        Returns: True if successful
        """
        try:
            queue_key = f"queue:{message.to_agent}"
            message_json = json.dumps(message.to_dict())

            # Push to queue
            self.redis_client.lpush(queue_key, message_json)
            logger.info(
                f"Message {message.message_id} sent to {message.to_agent}"
            )

            # Set expiration (24 hours)
            self.redis_client.expire(queue_key, 86400)

            return True
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            return False

    def receive_message(self, agent_name: str, timeout: int = 1) -> Optional[Message]:
        """
        Receive message from queue for agent
        Returns: Message object or None if queue empty
        """
        try:
            queue_key = f"queue:{agent_name}"

            # Non-blocking pop (timeout in seconds)
            message_json = self.redis_client.rpop(queue_key)

            if not message_json:
                return None

            message_data = json.loads(message_json)
            return Message.from_dict(message_data)
        except Exception as e:
            logger.error(f"Failed to receive message: {e}")
            return None

    def peek_queue(self, agent_name: str, count: int = 5) -> list:
        """
        Peek at messages in queue without removing them
        Returns: List of messages
        """
        try:
            queue_key = f"queue:{agent_name}"
            messages_json = self.redis_client.lrange(queue_key, 0, count - 1)

            messages = []
            for msg_json in messages_json:
                msg_data = json.loads(msg_json)
                messages.append(Message.from_dict(msg_data))
            return messages
        except Exception as e:
            logger.error(f"Failed to peek queue: {e}")
            return []

    def get_queue_size(self, agent_name: str) -> int:
        """Get number of messages in queue"""
        try:
            queue_key = f"queue:{agent_name}"
            return self.redis_client.llen(queue_key)
        except Exception as e:
            logger.error(f"Failed to get queue size: {e}")
            return 0

    def clear_queue(self, agent_name: str) -> bool:
        """Clear all messages from queue"""
        try:
            queue_key = f"queue:{agent_name}"
            self.redis_client.delete(queue_key)
            logger.info(f"Cleared queue for {agent_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to clear queue: {e}")
            return False

    def store_execution(self, agent_name: str, execution_data: Dict[str, Any]) -> bool:
        """Store agent execution log in Redis for quick access"""
        try:
            key = f"execution:{agent_name}:latest"
            self.redis_client.set(key, json.dumps(execution_data), ex=86400)
            return True
        except Exception as e:
            logger.error(f"Failed to store execution: {e}")
            return False

    def get_agent_status(self, agent_name: str) -> Dict[str, Any]:
        """Get current status of agent"""
        try:
            status_key = f"status:{agent_name}"
            status_json = self.redis_client.get(status_key)

            if not status_json:
                return {"agent": agent_name, "status": "idle", "last_run": None}

            return json.loads(status_json)
        except Exception as e:
            logger.error(f"Failed to get agent status: {e}")
            return {"agent": agent_name, "status": "error"}


# Global queue manager instance
_queue_manager: Optional[QueueManager] = None


def get_queue_manager() -> QueueManager:
    """Get or create global queue manager"""
    global _queue_manager
    if _queue_manager is None:
        _queue_manager = QueueManager()
    return _queue_manager

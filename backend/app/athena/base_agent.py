"""
Base Agent Class - Foundation for all Project Athena agents
Provides: Execution, self-testing, error handling, logging, inter-agent communication
"""

import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod
from app.athena.queue_manager import get_queue_manager, Message

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """
    Abstract base class for all Athena agents

    All agents must:
    - Implement execute() method
    - Call self.validate() before returning results
    - Handle errors gracefully with retries
    - Log all actions
    - Communicate via message queue
    """

    def __init__(self, name: str, api_provider: str = "claude"):
        """
        Initialize agent

        Args:
            name: Agent name (e.g., 'research_agent')
            api_provider: Primary AI provider ('claude', 'openai', 'gemini')
        """
        self.name = name
        self.api_provider = api_provider
        self.queue_manager = get_queue_manager()
        self.execution_start_time = None
        self.execution_end_time = None
        self.errors = []
        self.warnings = []
        self.self_tests_passed = 0
        self.self_tests_failed = 0

    @abstractmethod
    def execute(self) -> Dict[str, Any]:
        """
        Main agent execution logic
        Must be implemented by subclasses

        Returns:
            Dictionary with results and metadata
        """
        raise NotImplementedError

    def validate(self, data: Any) -> bool:
        """
        Self-test: Validate data before returning
        Must be implemented by subclasses

        Args:
            data: Data to validate

        Returns:
            True if valid, False otherwise
        """
        raise NotImplementedError

    def log_execution(self) -> None:
        """Log execution details to database"""
        from app.models import AgentExecution
        from app.database import async_session

        # TODO: Implement logging to database
        pass

    def retry_with_backoff(self, func, max_retries: int = 3, backoff_factor: float = 2):
        """
        Retry function with exponential backoff

        Args:
            func: Function to retry
            max_retries: Maximum retry attempts
            backoff_factor: Multiplier for backoff delay

        Returns:
            Result from function or None if all retries fail
        """
        import time

        for attempt in range(max_retries):
            try:
                return func()
            except Exception as e:
                if attempt == max_retries - 1:
                    self.errors.append(f"Max retries exceeded: {str(e)}")
                    logger.error(f"Max retries failed for {self.name}: {e}")
                    return None

                wait_time = backoff_factor ** attempt
                logger.warning(
                    f"Retry {attempt + 1}/{max_retries} after {wait_time}s: {e}"
                )
                time.sleep(wait_time)

    def send_message_to_agent(
        self,
        to_agent: str,
        message_type: str,
        payload: Dict[str, Any],
        requires_response: bool = False,
    ) -> bool:
        """
        Send message to another agent

        Args:
            to_agent: Name of target agent
            message_type: Type of message (e.g., 'task_completion', 'request')
            payload: Message payload
            requires_response: Whether response is required

        Returns:
            True if sent successfully
        """
        message = Message(
            from_agent=self.name,
            to_agent=to_agent,
            message_type=message_type,
            payload=payload,
            requires_response=requires_response,
        )

        success = self.queue_manager.send_message(message)

        if success:
            logger.info(
                f"{self.name} → {to_agent}: {message_type} ({message.message_id})"
            )
        else:
            logger.error(f"Failed to send message from {self.name} to {to_agent}")

        return success

    def receive_message(self, timeout: int = 1) -> Optional[Message]:
        """
        Receive message from queue

        Args:
            timeout: Timeout in seconds

        Returns:
            Message object or None
        """
        message = self.queue_manager.receive_message(self.name, timeout)

        if message:
            logger.info(f"{self.name} received: {message.message_type}")

        return message

    def request_data_from_agent(
        self, from_agent: str, data_request: str, timeout: int = 30
    ) -> Optional[Dict[str, Any]]:
        """
        Request data from another agent and wait for response

        Args:
            from_agent: Name of agent to request from
            data_request: Description of data needed
            timeout: Timeout in seconds

        Returns:
            Response data or None if timeout
        """
        # Send request
        self.send_message_to_agent(
            to_agent=from_agent,
            message_type="data_request",
            payload={"request": data_request},
            requires_response=True,
        )

        # Wait for response
        import time

        start_time = time.time()

        while time.time() - start_time < timeout:
            message = self.receive_message(timeout=1)

            if message and message.from_agent == from_agent:
                return message.payload

            time.sleep(0.5)

        logger.warning(f"Timeout waiting for data from {from_agent}")
        return None

    def log_action(self, action: str, details: Optional[Dict] = None) -> None:
        """Log an action performed by agent"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "agent": self.name,
            "action": action,
            "details": details or {},
        }
        logger.info(json.dumps(log_entry))

    def record_error(self, error_message: str) -> None:
        """Record an error"""
        self.errors.append(error_message)
        logger.error(f"{self.name}: {error_message}")

    def record_warning(self, warning_message: str) -> None:
        """Record a warning"""
        self.warnings.append(warning_message)
        logger.warning(f"{self.name}: {warning_message}")

    def test_passed(self) -> None:
        """Record a passed self-test"""
        self.self_tests_passed += 1

    def test_failed(self) -> None:
        """Record a failed self-test"""
        self.self_tests_failed += 1

    def get_execution_summary(self) -> Dict[str, Any]:
        """Get summary of execution"""
        duration = None
        if self.execution_start_time and self.execution_end_time:
            duration = (self.execution_end_time - self.execution_start_time).total_seconds()

        return {
            "agent": self.name,
            "api_provider": self.api_provider,
            "duration_seconds": duration,
            "errors": self.errors,
            "warnings": self.warnings,
            "self_tests": {
                "passed": self.self_tests_passed,
                "failed": self.self_tests_failed,
            },
            "status": "failed" if self.self_tests_failed > 0 else "success",
        }

    def run_safely(self) -> Dict[str, Any]:
        """
        Execute agent with error handling and logging

        Returns:
            Execution results with metadata
        """
        from datetime import datetime

        try:
            self.execution_start_time = datetime.utcnow()
            logger.info(f"Starting {self.name}")

            # Execute agent
            result = self.execute()

            # Validate result
            if not self.validate(result):
                self.record_error("Validation failed")
                self.test_failed()
                return {
                    "status": "error",
                    "error": "Validation failed",
                    "summary": self.get_execution_summary(),
                }

            self.test_passed()
            logger.info(f"✓ {self.name} completed successfully")

            self.execution_end_time = datetime.utcnow()

            return {
                "status": "success",
                "result": result,
                "summary": self.get_execution_summary(),
            }

        except Exception as e:
            self.record_error(str(e))
            self.test_failed()
            logger.error(f"✗ {self.name} failed: {e}")
            self.execution_end_time = datetime.utcnow()

            return {
                "status": "error",
                "error": str(e),
                "summary": self.get_execution_summary(),
            }

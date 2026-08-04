"""
Test Project Athena infrastructure
Verify queue manager, base agent, and orchestrator work correctly
"""

import pytest
from app.athena.queue_manager import QueueManager, Message
from app.athena.base_agent import BaseAgent
from app.athena.orchestrator import Orchestrator
from typing import Dict, Any


class MockAgent(BaseAgent):
    """Mock agent for testing"""

    def __init__(self, name: str = "test_agent"):
        super().__init__(name)
        self.executed = False

    def execute(self) -> Dict[str, Any]:
        """Mock execution"""
        self.executed = True
        self.log_action("execute", {"result": "success"})
        return {"result": "success", "data": [1, 2, 3]}

    def validate(self, data: Any) -> bool:
        """Mock validation"""
        return isinstance(data, dict) and "result" in data


# Test Queue Manager
def test_queue_manager_creation():
    """Test creating queue manager"""
    try:
        qm = QueueManager()
        assert qm is not None
        assert qm.redis_client is not None
        print("✓ Queue manager created successfully")
    except Exception as e:
        print(f"✗ Failed to create queue manager: {e}")
        raise


def test_message_creation():
    """Test creating messages"""
    msg = Message(
        from_agent="agent1",
        to_agent="agent2",
        message_type="test",
        payload={"test": "data"},
    )

    assert msg.from_agent == "agent1"
    assert msg.to_agent == "agent2"
    assert msg.status == "pending"
    print("✓ Message created successfully")


def test_message_serialization():
    """Test message serialization"""
    msg = Message(
        from_agent="agent1",
        to_agent="agent2",
        message_type="test",
        payload={"test": "data"},
    )

    msg_dict = msg.to_dict()
    assert "message_id" in msg_dict
    assert msg_dict["from_agent"] == "agent1"

    # Test deserialization
    msg2 = Message.from_dict(msg_dict)
    assert msg2.from_agent == msg.from_agent
    assert msg2.to_agent == msg.to_agent
    print("✓ Message serialization works")


def test_queue_operations():
    """Test queue send/receive"""
    try:
        qm = QueueManager()

        # Clear queue first
        qm.clear_queue("test_agent")

        # Create and send message
        msg = Message(
            from_agent="agent1",
            to_agent="test_agent",
            message_type="test",
            payload={"data": "test"},
        )

        success = qm.send_message(msg)
        assert success is True

        # Receive message
        received = qm.receive_message("test_agent")
        assert received is not None
        assert received.from_agent == "agent1"

        print("✓ Queue operations work")
    except Exception as e:
        print(f"✗ Queue operations failed: {e}")
        raise


def test_base_agent():
    """Test base agent functionality"""
    agent = MockAgent("test_agent")

    # Test execution
    result = agent.run_safely()
    assert result["status"] == "success"
    assert agent.executed is True
    assert result["summary"]["agent"] == "test_agent"

    print("✓ Base agent works")


def test_orchestrator():
    """Test orchestrator workflow"""
    orchestrator = Orchestrator()

    # Create agents
    agent1 = MockAgent("agent1")
    agent2 = MockAgent("agent2")

    # Register agents
    orchestrator.register_agent(agent1)
    orchestrator.register_agent(agent2)

    # Set workflow
    orchestrator.set_workflow(["agent1", "agent2"])

    # Run workflow
    results = orchestrator.run_workflow()

    assert results["workflow_status"] in ["success", "partial_success"]
    assert "agent1" in results["results"]
    assert "agent2" in results["results"]

    print("✓ Orchestrator works")


def test_inter_agent_communication():
    """Test agents communicating with each other"""
    try:
        agent1 = MockAgent("agent1")
        agent2 = MockAgent("agent2")

        # Agent1 sends message to Agent2
        success = agent1.send_message_to_agent(
            to_agent="agent2",
            message_type="test_message",
            payload={"test": "data"},
            requires_response=True,
        )

        assert success is True
        print("✓ Inter-agent communication works")
    except Exception as e:
        print(f"✗ Inter-agent communication failed: {e}")
        raise


# Run all tests
if __name__ == "__main__":
    print("\n🧪 Running Project Athena Infrastructure Tests\n")

    try:
        test_queue_manager_creation()
        test_message_creation()
        test_message_serialization()
        test_queue_operations()
        test_base_agent()
        test_orchestrator()
        test_inter_agent_communication()

        print("\n✅ All infrastructure tests passed!")
    except Exception as e:
        print(f"\n❌ Tests failed: {e}")
        raise

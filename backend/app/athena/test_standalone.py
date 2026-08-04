"""
Standalone tests for Project Athena - No app dependencies needed
"""

import sys
import json
from typing import Dict, Any


# Test 1: Message Format
def test_message_format():
    """Test message structure and serialization"""
    message = {
        "message_id": "test-123",
        "from_agent": "agent1",
        "to_agent": "agent2",
        "message_type": "test",
        "payload": {"data": "test"},
        "timestamp": "2026-08-04T00:00:00Z",
        "status": "pending",
    }

    # Serialize
    json_str = json.dumps(message)
    assert json_str is not None

    # Deserialize
    restored = json.loads(json_str)
    assert restored["from_agent"] == "agent1"
    assert restored["to_agent"] == "agent2"

    print("[PASS] Message format test passed")
    return True


# Test 2: Queue Manager Logic
def test_queue_manager_logic():
    """Test queue manager logic (without Redis)"""

    class SimpleQueue:
        def __init__(self):
            self.queues = {}

        def send_message(self, agent_name: str, message: Dict) -> bool:
            if agent_name not in self.queues:
                self.queues[agent_name] = []
            self.queues[agent_name].append(message)
            return True

        def receive_message(self, agent_name: str):
            if agent_name not in self.queues or len(self.queues[agent_name]) == 0:
                return None
            return self.queues[agent_name].pop(0)

        def get_queue_size(self, agent_name: str) -> int:
            if agent_name not in self.queues:
                return 0
            return len(self.queues[agent_name])

    queue = SimpleQueue()

    # Send message
    msg = {"from": "a1", "to": "a2", "data": "test"}
    success = queue.send_message("a2", msg)
    assert success is True

    # Check size
    assert queue.get_queue_size("a2") == 1

    # Receive message
    received = queue.receive_message("a2")
    assert received is not None
    assert received["from"] == "a1"

    # Check empty
    assert queue.get_queue_size("a2") == 0

    print("[PASS] Queue manager logic test passed")
    return True


# Test 3: Agent Execution Pattern
def test_agent_execution_pattern():
    """Test the agent execution pattern"""

    class SimpleAgent:
        def __init__(self, name: str):
            self.name = name
            self.errors = []
            self.tests_passed = 0
            self.tests_failed = 0

        def execute(self) -> Dict[str, Any]:
            return {"result": "success", "data": [1, 2, 3]}

        def validate(self, data: Any) -> bool:
            if not isinstance(data, dict):
                return False
            if "result" not in data:
                return False
            return True

        def run_safely(self) -> Dict[str, Any]:
            try:
                result = self.execute()
                if not self.validate(result):
                    self.tests_failed += 1
                    return {"status": "error", "error": "Validation failed"}
                self.tests_passed += 1
                return {"status": "success", "result": result}
            except Exception as e:
                self.tests_failed += 1
                return {"status": "error", "error": str(e)}

    agent = SimpleAgent("test_agent")
    result = agent.run_safely()

    assert result["status"] == "success"
    assert agent.tests_passed == 1
    assert agent.tests_failed == 0

    print("[PASS] Agent execution pattern test passed")
    return True


# Test 4: Orchestrator Pattern
def test_orchestrator_pattern():
    """Test orchestrator workflow pattern"""

    class SimpleOrchestrator:
        def __init__(self):
            self.agents = {}
            self.workflow = []
            self.results = {}

        def register_agent(self, name: str, agent) -> None:
            self.agents[name] = agent

        def set_workflow(self, workflow: list) -> None:
            self.workflow = workflow

        def run_workflow(self) -> Dict[str, Any]:
            results = {}
            for agent_name in self.workflow:
                agent = self.agents[agent_name]
                result = agent.run_safely()
                results[agent_name] = result
            return {
                "workflow_status": "success",
                "results": results,
                "agents_completed": len(results),
            }

    class SimpleAgent:
        def __init__(self, name: str):
            self.name = name

        def run_safely(self) -> Dict[str, Any]:
            return {"status": "success", "result": f"{self.name} executed"}

    # Setup
    orch = SimpleOrchestrator()
    a1 = SimpleAgent("agent1")
    a2 = SimpleAgent("agent2")

    orch.register_agent("agent1", a1)
    orch.register_agent("agent2", a2)
    orch.set_workflow(["agent1", "agent2"])

    # Run
    result = orch.run_workflow()

    assert result["workflow_status"] == "success"
    assert result["agents_completed"] == 2
    assert "agent1" in result["results"]
    assert "agent2" in result["results"]

    print("[PASS] Orchestrator pattern test passed")
    return True


# Test 5: Data Validation
def test_data_validation():
    """Test data validation logic"""

    def validate_product(product: Dict) -> bool:
        required = ["name", "price", "rating"]
        for field in required:
            if field not in product:
                return False
        if not isinstance(product["price"], (int, float)):
            return False
        if not 0 <= product["rating"] <= 5:
            return False
        return True

    # Valid product
    valid = {"name": "Test Product", "price": 10.99, "rating": 4.5}
    assert validate_product(valid) is True

    # Invalid - missing field
    invalid1 = {"name": "Test Product", "price": 10.99}
    assert validate_product(invalid1) is False

    # Invalid - bad rating
    invalid2 = {"name": "Test Product", "price": 10.99, "rating": 6.0}
    assert validate_product(invalid2) is False

    print("[PASS] Data validation test passed")
    return True


# Run all tests
if __name__ == "__main__":
    print("\n[TEST] Running Project Athena Standalone Tests\n")

    tests = [
        test_message_format,
        test_queue_manager_logic,
        test_agent_execution_pattern,
        test_orchestrator_pattern,
        test_data_validation,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"[FAIL] {test.__name__} failed: {e}")
            failed += 1

    print(f"\n{'='*50}")
    print(f"Results: {passed} passed, {failed} failed")

    if failed == 0:
        print("[SUCCESS] All tests passed!\n")
        sys.exit(0)
    else:
        print(f"[ERROR] {failed} test(s) failed\n")
        sys.exit(1)

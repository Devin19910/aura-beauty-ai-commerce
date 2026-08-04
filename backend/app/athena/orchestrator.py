"""
Orchestrator - Controls agent workflow and execution
Manages sequential execution of agents, handles dependencies, and tracks progress
"""

import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from app.athena.queue_manager import get_queue_manager

logger = logging.getLogger(__name__)


class Orchestrator:
    """
    Orchestrates Project Athena agent workflow

    Manages:
    - Agent execution order
    - Data flow between agents
    - Progress tracking
    - Error handling
    - Scheduling
    """

    def __init__(self):
        """Initialize orchestrator"""
        self.queue_manager = get_queue_manager()
        self.agents: Dict[str, Any] = {}
        self.workflow: List[str] = []
        self.execution_log: List[Dict[str, Any]] = []
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None

    def register_agent(self, agent) -> None:
        """
        Register an agent with orchestrator

        Args:
            agent: BaseAgent instance
        """
        self.agents[agent.name] = agent
        logger.info(f"✓ Registered agent: {agent.name}")

    def set_workflow(self, workflow: List[str]) -> None:
        """
        Set agent execution order

        Args:
            workflow: List of agent names in execution order
        """
        # Verify all agents exist
        for agent_name in workflow:
            if agent_name not in self.agents:
                raise ValueError(f"Agent not registered: {agent_name}")

        self.workflow = workflow
        logger.info(f"Workflow set: {' → '.join(workflow)}")

    def run_workflow(self) -> Dict[str, Any]:
        """
        Execute the complete workflow

        Returns:
            Dictionary with results from all agents
        """
        self.start_time = datetime.utcnow()
        logger.info(f"🚀 Starting workflow at {self.start_time}")

        results = {}

        for agent_name in self.workflow:
            agent = self.agents[agent_name]

            logger.info(f"▶️ Executing {agent_name}...")

            # Run agent
            execution_result = agent.run_safely()

            # Store result
            results[agent_name] = execution_result
            self.execution_log.append(
                {
                    "agent": agent_name,
                    "timestamp": datetime.utcnow().isoformat(),
                    "result": execution_result,
                }
            )

            # Check for failure
            if execution_result["status"] == "error":
                logger.error(f"✗ {agent_name} failed: {execution_result['error']}")

                # Try fallback or continue?
                # For now, continue to next agent
                continue

            # Log success
            logger.info(f"✓ {agent_name} completed")

            # Send result to next agent if needed
            if self.workflow.index(agent_name) < len(self.workflow) - 1:
                next_agent = self.workflow[self.workflow.index(agent_name) + 1]
                self._send_result_to_next_agent(
                    from_agent=agent_name,
                    to_agent=next_agent,
                    result=execution_result,
                )

        self.end_time = datetime.utcnow()
        logger.info(f"✅ Workflow completed in {self.get_duration()}s")

        return self.get_workflow_summary(results)

    def _send_result_to_next_agent(
        self, from_agent: str, to_agent: str, result: Dict[str, Any]
    ) -> None:
        """Send result from one agent to the next"""
        agent = self.agents[to_agent]

        agent.send_message_to_agent(
            to_agent=to_agent,
            message_type="upstream_result",
            payload={
                "from_agent": from_agent,
                "result": result["result"] if result["status"] == "success" else None,
                "status": result["status"],
            },
        )

    def get_duration(self) -> float:
        """Get total workflow duration in seconds"""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0

    def get_workflow_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get summary of entire workflow execution

        Args:
            results: Results from all agents

        Returns:
            Workflow summary
        """
        total_errors = sum(
            1 for r in results.values() if r["status"] == "error"
        )

        return {
            "workflow_status": "success" if total_errors == 0 else "partial_success",
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_seconds": self.get_duration(),
            "agents_executed": len(results),
            "agents_succeeded": len([r for r in results.values() if r["status"] == "success"]),
            "agents_failed": total_errors,
            "results": results,
        }

    def get_progress(self) -> Dict[str, Any]:
        """Get current progress of workflow"""
        executed = len(self.execution_log)
        total = len(self.workflow)

        return {
            "total_agents": total,
            "agents_completed": executed,
            "agents_remaining": total - executed,
            "progress_percentage": (executed / total * 100) if total > 0 else 0,
            "workflow": self.workflow,
            "recent_logs": self.execution_log[-5:],
        }


class WorkflowBuilder:
    """Builder pattern for constructing workflows"""

    def __init__(self):
        """Initialize builder"""
        self.orchestrator = Orchestrator()
        self.agents_to_register = []

    def add_agent(self, agent) -> "WorkflowBuilder":
        """Add agent to workflow"""
        self.agents_to_register.append(agent)
        return self

    def set_sequence(self, agent_names: List[str]) -> "WorkflowBuilder":
        """Set execution order"""
        self.agent_sequence = agent_names
        return self

    def build(self) -> Orchestrator:
        """Build and return orchestrator"""
        for agent in self.agents_to_register:
            self.orchestrator.register_agent(agent)

        if hasattr(self, "agent_sequence"):
            self.orchestrator.set_workflow(self.agent_sequence)

        return self.orchestrator


# Convenience function for creating standard Project Athena workflow
def create_athena_workflow(agents_dict: Dict[str, Any]) -> Orchestrator:
    """
    Create standard Project Athena workflow:
    Research → Supplier → Validation → Scoring

    Args:
        agents_dict: Dictionary mapping agent names to agent instances

    Returns:
        Configured orchestrator
    """
    builder = WorkflowBuilder()

    # Standard order for Project Athena
    agent_order = [
        "research_agent",
        "supplier_agent",
        "validation_agent",
        "scoring_agent",
    ]

    for agent_name in agent_order:
        if agent_name in agents_dict:
            builder.add_agent(agents_dict[agent_name])

    builder.set_sequence(agent_order)

    return builder.build()

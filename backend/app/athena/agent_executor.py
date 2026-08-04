"""
Agent Executor - Manages agent execution, status tracking, and result aggregation
Bridges agents and API endpoints
"""

import json
from datetime import datetime
from typing import Dict, Any, Optional, List
from enum import Enum


class ExecutionStatus(str, Enum):
    """Execution status enum"""
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class AgentExecutor:
    """
    Manages execution of Project Athena agents
    Tracks status, aggregates results, provides dashboard data
    """

    def __init__(self):
        self.workflow_id = None
        self.status = ExecutionStatus.IDLE
        self.current_agent = None
        self.agents_completed = 0
        self.total_agents = 4
        self.start_time = None
        self.end_time = None

        # Agent references (will be imported)
        self.research_agent = None
        self.supplier_agent = None
        self.validation_agent = None
        self.scoring_agent = None

        # Results storage
        self.results = {
            "research": None,
            "supplier": None,
            "validation": None,
            "scoring": None,
        }

        # Agent status tracking
        self.agent_status = {
            "research_agent": {
                "status": "idle",
                "last_execution": None,
                "is_running": False,
                "execution_time_ms": 0,
            },
            "supplier_agent": {
                "status": "idle",
                "last_execution": None,
                "is_running": False,
                "execution_time_ms": 0,
            },
            "validation_agent": {
                "status": "idle",
                "last_execution": None,
                "is_running": False,
                "execution_time_ms": 0,
            },
            "scoring_agent": {
                "status": "idle",
                "last_execution": None,
                "is_running": False,
                "execution_time_ms": 0,
            },
        }

    def get_workflow_status(self) -> Dict[str, Any]:
        """Get current workflow execution status"""
        if self.status == ExecutionStatus.IDLE:
            progress = 0
        elif self.status == ExecutionStatus.RUNNING:
            progress = (self.agents_completed / self.total_agents) * 100
        else:
            progress = 100

        return {
            "workflow_id": self.workflow_id,
            "workflow_status": self.status.value,
            "progress_percentage": round(progress, 1),
            "agents_completed": self.agents_completed,
            "total_agents": self.total_agents,
            "current_agent": self.current_agent,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "elapsed_seconds": (
                (self.end_time or datetime.now()) - self.start_time
            ).total_seconds()
            if self.start_time
            else None,
        }

    def get_agent_status(self, agent_name: str) -> Dict[str, Any]:
        """Get status of specific agent"""
        if agent_name not in self.agent_status:
            return {"error": f"Agent {agent_name} not found"}

        status = self.agent_status[agent_name]
        return {
            "agent_name": agent_name,
            "status": status["status"],
            "is_running": status["is_running"],
            "last_execution": status["last_execution"],
            "execution_time_ms": status["execution_time_ms"],
        }

    def start_workflow(self) -> str:
        """Start the complete workflow"""
        import uuid

        self.workflow_id = str(uuid.uuid4())
        self.status = ExecutionStatus.RUNNING
        self.agents_completed = 0
        self.start_time = datetime.now()
        self.current_agent = "research_agent"

        return self.workflow_id

    def complete_workflow(self):
        """Mark workflow as completed"""
        self.status = ExecutionStatus.COMPLETED
        self.end_time = datetime.now()
        self.current_agent = None

    def fail_workflow(self, error: str):
        """Mark workflow as failed"""
        self.status = ExecutionStatus.FAILED
        self.end_time = datetime.now()
        self.current_agent = None

    def execute_research_agent(self, products_data: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """Execute research agent"""
        from app.athena.agents.real_scraper import RealProductScraper

        agent_name = "research_agent"
        self.current_agent = agent_name
        self.agent_status[agent_name]["is_running"] = True
        self.agent_status[agent_name]["status"] = "running"

        start_time = datetime.now()

        try:
            scraper = RealProductScraper()
            result = scraper.discover_products()

            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            self.agent_status[agent_name]["execution_time_ms"] = round(execution_time, 1)
            self.agent_status[agent_name]["is_running"] = False
            self.agent_status[agent_name]["status"] = "completed"
            self.agent_status[agent_name]["last_execution"] = datetime.now().isoformat()

            self.results["research"] = result
            self.agents_completed += 1

            return {
                "status": "success",
                "agent": agent_name,
                "products_found": result.get("total_found", 0),
                "execution_time_ms": self.agent_status[agent_name]["execution_time_ms"],
            }
        except Exception as e:
            self.agent_status[agent_name]["is_running"] = False
            self.agent_status[agent_name]["status"] = "failed"
            return {"status": "error", "agent": agent_name, "error": str(e)}

    def execute_supplier_agent(self) -> Dict[str, Any]:
        """Execute supplier agent"""
        from app.athena.agents.supplier_agent import SupplierAgent

        agent_name = "supplier_agent"
        self.current_agent = agent_name
        self.agent_status[agent_name]["is_running"] = True
        self.agent_status[agent_name]["status"] = "running"

        start_time = datetime.now()

        try:
            if not self.results["research"]:
                return {"status": "error", "error": "Research agent results required"}

            products = self.results["research"].get("products", [])
            agent = SupplierAgent()
            result = agent.run_safely(products)

            if result["status"] != "success":
                return {"status": "error", "agent": agent_name, "error": result.get("error")}

            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            self.agent_status[agent_name]["execution_time_ms"] = round(execution_time, 1)
            self.agent_status[agent_name]["is_running"] = False
            self.agent_status[agent_name]["status"] = "completed"
            self.agent_status[agent_name]["last_execution"] = datetime.now().isoformat()

            self.results["supplier"] = result["result"]
            self.agents_completed += 1

            return {
                "status": "success",
                "agent": agent_name,
                "suppliers_found": result["result"].get("total_suppliers_found", 0),
                "execution_time_ms": self.agent_status[agent_name]["execution_time_ms"],
            }
        except Exception as e:
            self.agent_status[agent_name]["is_running"] = False
            self.agent_status[agent_name]["status"] = "failed"
            return {"status": "error", "agent": agent_name, "error": str(e)}

    def execute_validation_agent(self) -> Dict[str, Any]:
        """Execute validation agent"""
        from app.athena.agents.validation_agent import ValidationAgent

        agent_name = "validation_agent"
        self.current_agent = agent_name
        self.agent_status[agent_name]["is_running"] = True
        self.agent_status[agent_name]["status"] = "running"

        start_time = datetime.now()

        try:
            if not self.results["supplier"]:
                return {"status": "error", "error": "Supplier agent results required"}

            products_data = self.results["supplier"].get("products_with_suppliers", [])
            agent = ValidationAgent()
            result = agent.run_safely(products_data)

            if result["status"] != "success":
                return {"status": "error", "agent": agent_name, "error": result.get("error")}

            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            self.agent_status[agent_name]["execution_time_ms"] = round(execution_time, 1)
            self.agent_status[agent_name]["is_running"] = False
            self.agent_status[agent_name]["status"] = "completed"
            self.agent_status[agent_name]["last_execution"] = datetime.now().isoformat()

            self.results["validation"] = result["result"]
            self.agents_completed += 1

            return {
                "status": "success",
                "agent": agent_name,
                "products_validated": result["result"].get("total_validated", 0),
                "execution_time_ms": self.agent_status[agent_name]["execution_time_ms"],
            }
        except Exception as e:
            self.agent_status[agent_name]["is_running"] = False
            self.agent_status[agent_name]["status"] = "failed"
            return {"status": "error", "agent": agent_name, "error": str(e)}

    def execute_scoring_agent(self) -> Dict[str, Any]:
        """Execute scoring agent"""
        from app.athena.agents.scoring_agent import ScoringAgent

        agent_name = "scoring_agent"
        self.current_agent = agent_name
        self.agent_status[agent_name]["is_running"] = True
        self.agent_status[agent_name]["status"] = "running"

        start_time = datetime.now()

        try:
            if not self.results["validation"]:
                return {"status": "error", "error": "Validation agent results required"}

            products_data = self.results["validation"].get("validation_results", [])
            agent = ScoringAgent()
            result = agent.run_safely(products_data)

            if result["status"] != "success":
                return {"status": "error", "agent": agent_name, "error": result.get("error")}

            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            self.agent_status[agent_name]["execution_time_ms"] = round(execution_time, 1)
            self.agent_status[agent_name]["is_running"] = False
            self.agent_status[agent_name]["status"] = "completed"
            self.agent_status[agent_name]["last_execution"] = datetime.now().isoformat()

            self.results["scoring"] = result["result"]
            self.agents_completed += 1

            return {
                "status": "success",
                "agent": agent_name,
                "products_ranked": result["result"].get("total_products", 0),
                "execution_time_ms": self.agent_status[agent_name]["execution_time_ms"],
            }
        except Exception as e:
            self.agent_status[agent_name]["is_running"] = False
            self.agent_status[agent_name]["status"] = "failed"
            return {"status": "error", "agent": agent_name, "error": str(e)}

    def execute_full_workflow(self) -> Dict[str, Any]:
        """Execute complete workflow sequentially"""
        self.start_workflow()

        # Stage 1: Research
        research_result = self.execute_research_agent()
        if research_result["status"] != "success":
            self.fail_workflow(research_result.get("error", "Research agent failed"))
            return research_result

        # Stage 2: Supplier
        supplier_result = self.execute_supplier_agent()
        if supplier_result["status"] != "success":
            self.fail_workflow(supplier_result.get("error", "Supplier agent failed"))
            return supplier_result

        # Stage 3: Validation
        validation_result = self.execute_validation_agent()
        if validation_result["status"] != "success":
            self.fail_workflow(validation_result.get("error", "Validation agent failed"))
            return validation_result

        # Stage 4: Scoring
        scoring_result = self.execute_scoring_agent()
        if scoring_result["status"] != "success":
            self.fail_workflow(scoring_result.get("error", "Scoring agent failed"))
            return scoring_result

        self.complete_workflow()

        return {
            "status": "success",
            "workflow_id": self.workflow_id,
            "message": "All agents executed successfully",
            "results": {
                "research": research_result,
                "supplier": supplier_result,
                "validation": validation_result,
                "scoring": scoring_result,
            },
        }

    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get all data needed for dashboard display"""
        research = self.results.get("research", {})
        supplier = self.results.get("supplier", {})
        validation = self.results.get("validation", {})
        scoring = self.results.get("scoring", {})

        return {
            "workflow_status": self.get_workflow_status(),
            "agents": {
                "research_agent": self.get_agent_status("research_agent"),
                "supplier_agent": self.get_agent_status("supplier_agent"),
                "validation_agent": self.get_agent_status("validation_agent"),
                "scoring_agent": self.get_agent_status("scoring_agent"),
            },
            "summary": {
                "products_discovered": research.get("total_found", 0),
                "suppliers_found": supplier.get("total_suppliers_found", 0),
                "products_validated": validation.get("total_validated", 0),
                "products_ranked": scoring.get("total_products", 0),
                "quality_score": research.get("quality_score", 0),
                "approval_rate": validation.get("approval_rate", 0),
            },
            "top_products": (
                scoring.get("ranked_products", [])[:5] if scoring else []
            ),
            "products": research.get("products", []),
            "suppliers": supplier.get("products_with_suppliers", []),
            "validations": validation.get("validation_results", []),
            "rankings": scoring.get("ranked_products", []),
        }

    def get_latest_report(self) -> Dict[str, Any]:
        """Generate latest execution report"""
        return {
            "timestamp": datetime.now().isoformat(),
            "workflow_id": self.workflow_id,
            "status": self.status.value,
            "total_execution_time_seconds": (
                (self.end_time or datetime.now()) - self.start_time
            ).total_seconds()
            if self.start_time
            else None,
            "agents_completed": self.agents_completed,
            "total_agents": self.total_agents,
            "summary": {
                "products_discovered": self.results.get("research", {}).get(
                    "total_found", 0
                ),
                "suppliers_found": self.results.get("supplier", {}).get(
                    "total_suppliers_found", 0
                ),
                "products_approved": self.results.get("validation", {}).get(
                    "approved", 0
                ),
                "top_product": (
                    self.results.get("scoring", {})
                    .get("ranked_products", [{}])[0]
                    .get("product_name", "N/A")
                ),
            },
        }


# Global executor instance
_executor = AgentExecutor()


def get_executor() -> AgentExecutor:
    """Get global executor instance"""
    return _executor

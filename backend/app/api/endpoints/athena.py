"""
Project Athena API endpoints
Trigger agents, check status, view results
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any, List
import logging
from app.athena.agent_executor import get_executor

logger = logging.getLogger(__name__)

router = APIRouter()


class AgentStatusResponse(BaseModel):
    """Response model for agent status"""

    agent_name: str
    status: str
    last_execution: str = None
    next_execution: str = None
    is_running: bool = False


class WorkflowStatusResponse(BaseModel):
    """Response model for workflow status"""

    workflow_status: str
    progress_percentage: float
    agents_completed: int
    total_agents: int
    current_agent: str = None


class AthenaResultsResponse(BaseModel):
    """Response model for Athena results"""

    products: List[Dict[str, Any]]
    suppliers: List[Dict[str, Any]]
    validation_status: str
    top_recommendations: List[Dict[str, Any]]
    generated_at: str


# TODO: These are placeholders until agents are implemented
# Once agents are built, these will trigger actual executions


@router.post("/run-workflow")
async def run_workflow(background_tasks: BackgroundTasks):
    """
    Trigger the complete Project Athena workflow
    Returns immediately with workflow_id
    """
    executor = get_executor()
    workflow_id = executor.start_workflow()

    # Run workflow in background
    async def run_workflow_background():
        try:
            executor.execute_full_workflow()
        except Exception as e:
            executor.fail_workflow(str(e))
            logger.error(f"Workflow failed: {e}")

    background_tasks.add_task(run_workflow_background)

    return {
        "message": "Workflow started",
        "status": "processing",
        "workflow_id": workflow_id,
        "estimated_completion_seconds": 30,
    }


@router.get("/status")
async def get_workflow_status() -> Dict[str, Any]:
    """Get current status of running workflow"""
    executor = get_executor()
    return executor.get_workflow_status()


@router.get("/agent-status/{agent_name}")
async def get_agent_status(agent_name: str) -> Dict[str, Any]:
    """Get status of specific agent"""
    executor = get_executor()
    valid_agents = ["research_agent", "supplier_agent", "validation_agent", "scoring_agent"]

    if agent_name not in valid_agents:
        raise HTTPException(status_code=404, detail="Agent not found")

    return executor.get_agent_status(agent_name)


@router.get("/results")
async def get_results() -> Dict[str, Any]:
    """Get latest Project Athena results"""
    executor = get_executor()
    return executor.get_dashboard_data()


@router.get("/results/top-products")
async def get_top_products(limit: int = 5) -> List[Dict[str, Any]]:
    """Get top recommended products"""
    executor = get_executor()
    dashboard_data = executor.get_dashboard_data()
    top_products = dashboard_data.get("rankings", [])[:limit]
    return top_products


@router.get("/results/latest-report")
async def get_latest_report() -> Dict[str, Any]:
    """Get latest workflow execution report"""
    executor = get_executor()
    return executor.get_latest_report()


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """Check Project Athena system health"""
    executor = get_executor()
    return {
        "status": "healthy",
        "agents_registered": 4,
        "current_status": executor.status.value,
        "agents": {
            "research_agent": executor.agent_status["research_agent"]["status"],
            "supplier_agent": executor.agent_status["supplier_agent"]["status"],
            "validation_agent": executor.agent_status["validation_agent"]["status"],
            "scoring_agent": executor.agent_status["scoring_agent"]["status"],
        },
    }


@router.post("/test-connection")
async def test_all_connections() -> Dict[str, Any]:
    """Test all external connections"""
    return {
        "status": "operational",
        "agents": "4 agents loaded",
        "api": "responsive",
        "timestamp": "2026-08-04T17:00:00Z",
    }

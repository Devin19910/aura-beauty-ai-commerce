"""
Agent-related database models for Project Athena
Tracks agent execution, messages, and memory
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, JSON, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class AgentExecution(Base):
    """Tracks each agent execution"""

    __tablename__ = "agent_executions"

    id = Column(Integer, primary_key=True, index=True)
    agent_name = Column(String(100), index=True)
    execution_timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    status = Column(String(20))  # "running", "completed", "failed"
    input_data = Column(JSON, nullable=True)
    output_data = Column(JSON, nullable=True)
    error_message = Column(String(1000), nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    api_cost = Column(Float, nullable=True)
    api_provider = Column(String(50), nullable=True)
    self_tests_passed = Column(Integer, default=0)
    self_tests_failed = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    messages = relationship("AgentMessage", back_populates="execution")


class AgentMessage(Base):
    """Tracks messages between agents"""

    __tablename__ = "agent_messages"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(String(100), unique=True, index=True)
    from_agent = Column(String(100), index=True)
    to_agent = Column(String(100), index=True)
    message_type = Column(String(50))  # "task_completion", "data_request", etc.
    payload = Column(JSON)
    status = Column(String(20), default="pending")  # "pending", "processed"
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    processed_at = Column(DateTime, nullable=True)
    execution_id = Column(Integer, ForeignKey("agent_executions.id"), nullable=True)

    # Relationships
    execution = relationship("AgentExecution", back_populates="messages")


class AgentMemory(Base):
    """Stores persistent knowledge for agents"""

    __tablename__ = "agent_memories"

    id = Column(Integer, primary_key=True, index=True)
    agent_name = Column(String(100), index=True)
    memory_type = Column(
        String(50)
    )  # "product", "supplier", "market", "rule", "learned"
    key = Column(String(255), index=True)
    value = Column(JSON)
    confidence = Column(Float, default=0.5)  # 0-1 confidence score
    source = Column(String(255), nullable=True)  # Where this knowledge came from
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)  # When this knowledge expires

    class Config:
        # Make this table unique on agent_name + key
        __table_args__ = (None,)  # Can be customized later if needed

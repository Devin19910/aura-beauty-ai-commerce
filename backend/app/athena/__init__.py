"""
Project Athena - Multi-Agent Intelligence System
Autonomous agents for product research, supplier analysis, validation, and scoring
"""

__version__ = "0.1.0"
__author__ = "Claude - Technical Co-Founder"

from .orchestrator import Orchestrator
from .base_agent import BaseAgent

__all__ = ["Orchestrator", "BaseAgent"]

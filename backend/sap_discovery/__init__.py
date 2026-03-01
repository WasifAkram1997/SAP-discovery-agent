"""SAP Process Discovery Agent - LangGraph-based business process mapper."""

__version__ = "0.1.0"

from sap_discovery.workflow.executor import process_single
from sap_discovery.main_agent.agent import create_main_agent
from sap_discovery.data.loader import load_processes

__all__ = ["process_single", "create_main_agent", "load_processes"]

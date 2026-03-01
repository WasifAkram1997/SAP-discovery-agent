"""Workflow executor for processing business processes."""

from sap_discovery.models.schema import SAPProcessMapping
from sap_discovery.workflow.state import AgentState
from sap_discovery.utils.logging import setup_logger

logger = setup_logger(__name__)


async def process_single(process: dict, graph) -> SAPProcessMapping:
    """Process a single business process through the LangGraph workflow.

    Args:
        process: Business process dictionary with at least 'Process Name' key
        graph: Compiled LangGraph workflow

    Returns:
        SAPProcessMapping with results
    """
    initial_state = AgentState(
        messages=[],
        process_input=process,
        iteration=0,
        structured_output=None,
        collected_sources=[],
        quality_score=None,
        synthesis_success=False
    )

    final_state = await graph.ainvoke(initial_state)

    if not final_state.get("synthesis_success"):
        logger.warning(f"Synthesis failed for process: {process.get('Process Name')}")

    return final_state.get("structured_output")
"""Routing functions for conditional workflow edges."""

from typing import Literal
from sap_discovery.workflow.state import AgentState
from sap_discovery.config import THRESHOLD, MAX_ITERATIONS
from sap_discovery.utils.logging import setup_logger

logger = setup_logger(__name__)


def route_after_plan(state: AgentState) -> Literal["action", "synthesis"]:
    """Route based on whether there are tool calls to execute.

    Args:
        state: Current agent state

    Returns:
        "action" if there are tool calls to execute, "synthesis" otherwise
    """
    messages = state["messages"]
    last_message = messages[-1] if messages else None

    if last_message and hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "action"

    return "synthesis"


def route_after_scoring(state: AgentState) -> Literal["plan", "synthesis"]:
    """Route based on quality score, missing dimensions and iteration count.

    Args:
        state: Current agent state

    Returns:
        "plan" to continue research, "synthesis" when quality is sufficient or max iterations reached
    """
    quality_score = state.get("quality_score")
    iteration = state.get("iteration", 0)

    if iteration >= MAX_ITERATIONS:
        logger.info(f"Max iterations ({MAX_ITERATIONS}) reached -> synthesis")
        return "synthesis"

    if quality_score and quality_score.total >= THRESHOLD and not quality_score.missing:
        logger.info(f"Quality threshold met ({quality_score.total} >= {THRESHOLD}) with no missing dimensions -> synthesis")
        return "synthesis"

    score_display = quality_score.total if quality_score else 0
    missing = quality_score.missing if quality_score else []
    logger.info(f"Score {score_display} | Missing: {missing} -> plan")
    return "plan"
"""LangGraph workflow compilation."""

from langgraph.graph import StateGraph, START, END
from sap_discovery.workflow.state import AgentState
from sap_discovery.workflow.nodes import plan, action, scoring, synthesis
from sap_discovery.workflow.routers.routing import route_after_plan, route_after_scoring
from sap_discovery.utils.logging import setup_logger

logger = setup_logger(__name__)


def compile_workflow(llm_instances: dict, tools: list):
    """Compile the SAP Process Discovery workflow graph.

    Args:
        llm_instances: Dictionary of LLM instances from create_llm_instances
        tools: List of all tools

    Returns:
        Compiled LangGraph workflow
    """
    workflow = StateGraph(AgentState)

    # Create node functions with LLMs/tools bound
    def plan_fn(state):
        return plan.plan_node(state, llm_instances["with_tools"])

    async def action_fn(state):
        return await action.action_node(state, tools)

    def scoring_fn(state):
        return scoring.scoring_node(state, llm_instances["scoring"])

    def synthesis_fn(state):
        return synthesis.synthesis_node(state, llm_instances["structured"])

    # Add nodes
    workflow.add_node("plan", plan_fn)
    workflow.add_node("action", action_fn)
    workflow.add_node("scoring", scoring_fn)
    workflow.add_node("synthesis", synthesis_fn)

    # Add edges
    workflow.add_edge(START, "plan")

    workflow.add_conditional_edges(
        "plan",
        route_after_plan,
        {"action": "action", "synthesis": "synthesis"}
    )

    workflow.add_edge("action", "scoring")

    workflow.add_conditional_edges(
        "scoring",
        route_after_scoring,
        {"plan": "plan", "synthesis": "synthesis"}
    )

    workflow.add_edge("synthesis", END)

    logger.info("LangGraph workflow compiled successfully!")

    return workflow.compile()
"""Plan node - decides tool calls based on quality gaps."""

from langchain_core.messages import HumanMessage
from langgraph.types import Command
from sap_discovery.workflow.state import AgentState
from sap_discovery.config import DIMENSION_SEARCH_GUIDANCE
from sap_discovery.utils.logging import setup_logger

logger = setup_logger(__name__)


def plan_node(state: AgentState, llm_with_tools) -> dict:
    """Plan which tools to call based on iteration and quality score.

    Args:
        state: Current agent state
        llm_with_tools: LLM instance with tools bound

    Returns:
        Dictionary with messages containing tool calls or Command to synthesis
    """
    iteration = state.get("iteration", 0)
    quality_score = state.get("quality_score", None)
    process = state["process_input"]
    process_name = process.get("Process Name", process.get("process", "Unknown Process"))
    process_text = "\n".join([f"{k}: {v}" for k, v in process.items() if k != "_row_id" and v])

    if iteration == 0:
        prompt = f"""You are an SAP expert researching a business process.

Research this process using ALL available tools:
{process_text}

Find the following:
1. SAP modules involved (MM, FI, CO, SD, HR, PM etc.)
2. Standard transaction codes (e.g. ME21N, FB60, VA01)
3. Fiori app names and IDs
4. Contextual description including:
   - Step by step execution flow
   - Configuration dependencies where relevant
   - Integration points where relevant

Guidelines:
- Use SAP documentation tools for official SAP Help information
- Use web search for additional context and exploratory retrieval
- Use SAP specific terminology in queries
- Keep each query under 6 words"""

    else:
        missing = quality_score.missing if quality_score else []

        if not missing:
            return Command(goto="synthesis")

        missing_searches = "\n".join([
            f"- {DIMENSION_SEARCH_GUIDANCE[dim].format(process=process_name)}"
            for dim in missing
        ])

        prompt = f"""You are a routing decision node, not a conversational agent.

Your ONLY job is to call tools for each missing item below.

Missing dimensions and their targeted searches:
{missing_searches}

Rules:
- Use SAP documentation tools for official information
- Use web search for additional context
- DO NOT combine them into one query
- DO NOT explain your reasoning
- DO NOT write summaries"""

    response = llm_with_tools.invoke(state["messages"] + [HumanMessage(content=prompt)])

    tool_count = len(response.tool_calls) if hasattr(response, "tool_calls") and response.tool_calls else 0
    logger.info(f"Iteration {iteration + 1}: {tool_count} tool call(s) planned")
    if quality_score:
        logger.info(f"Current score: {quality_score.total} | Missing: {quality_score.missing}")

    return {"messages": [response]}
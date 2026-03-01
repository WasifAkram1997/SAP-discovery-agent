"""Action node - executes tools and extracts sources."""

import asyncio
from langchain_core.messages import ToolMessage
from sap_discovery.workflow.state import AgentState
from sap_discovery.utils.source_extraction import extract_sources_from_tool_result
from sap_discovery.utils.result_formatter import format_tool_result
from sap_discovery.tools.registry import get_tools_by_name
from sap_discovery.tools.mcp_tools import get_mcp_tool_names
from sap_discovery.utils.logging import setup_logger

logger = setup_logger(__name__)


async def execute_tool_call(tool_call: dict, tools_by_name: dict, mcp_tool_names: set) -> tuple:
    """Execute a single tool call and extract sources.

    Args:
        tool_call: Tool call dictionary with name, args, and id
        tools_by_name: Dictionary mapping tool names to tool instances
        mcp_tool_names: Set of MCP tool names

    Returns:
        Tuple of (ToolMessage, extracted_sources)
    """
    tool = tools_by_name.get(tool_call["name"])

    if tool is None:
        logger.warning(f"Unknown tool requested: {tool_call['name']}")
        return ToolMessage(
            content=f"Error: unknown tool '{tool_call['name']}'",
            tool_call_id=tool_call["id"]
        ), []

    try:
        result = await tool.ainvoke(tool_call["args"])

        # Format result for LLM consumption
        formatted_str = format_tool_result(
            tool_call["name"],
            result,  # pass raw result directly, formatter handles both list and string
            mcp_tool_names
        )

        # Extract sources from formatted result
        extracted = extract_sources_from_tool_result(
            tool_call["name"],
            formatted_str,
            mcp_tool_names
        )

        if extracted:
            logger.info(f"Extracted {len(extracted)} sources from {tool_call['name']}")

        return ToolMessage(
            content=formatted_str,
            tool_call_id=tool_call["id"]
        ), extracted

    except Exception as e:
        logger.error(f"Tool {tool_call['name']} failed: {e}")
        return ToolMessage(
            content="Tool execution failed.",
            tool_call_id=tool_call["id"]
        ), []


async def action_node(state: AgentState, tools: list) -> dict:
    """Execute tool calls in parallel and extract source references.

    Args:
        state: Current agent state
        tools: List of all available tools

    Returns:
        Dictionary with tool messages, incremented iteration, and collected sources
    """
    last_message = state["messages"][-1]
    new_sources = state.get("collected_sources", []).copy()

    tools_by_name = get_tools_by_name(tools)
    mcp_tool_names = get_mcp_tool_names()

    # Execute all tool calls in parallel
    results = await asyncio.gather(*[
        execute_tool_call(tool_call, tools_by_name, mcp_tool_names)
        for tool_call in last_message.tool_calls
    ])

    # Unpack results
    tool_messages = []
    for tool_message, extracted_sources in results:
        tool_messages.append(tool_message)
        new_sources.extend(extracted_sources)

    logger.info(f"Executed {len(tool_messages)} tool calls in parallel, total sources: {len(new_sources)}")

    return {
        "messages": tool_messages,
        "iteration": state.get("iteration", 0) + 1,
        "collected_sources": new_sources
    }
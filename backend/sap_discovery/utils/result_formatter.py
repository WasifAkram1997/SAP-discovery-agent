"""Formatting utilities for tool results."""

import ast
import json
import re
from sap_discovery.utils.logging import setup_logger

logger = setup_logger(__name__)


def clean_html(text: str) -> str:
    """Remove HTML tags from text.

    Args:
        text: Text with HTML tags

    Returns:
        Clean text without HTML tags
    """
    return re.sub(r'<[^>]+>', '', text).strip()


def format_mcp_results(raw_result) -> str:
    """Clean and format MCP tool results for LLM consumption.

    Args:
        raw_result: Raw result from MCP tool call (list or string)

    Returns:
        Cleaned formatted string ready for LLM consumption
    """
    try:
        # Handle both list and string inputs
        parsed = ast.literal_eval(raw_result) if isinstance(raw_result, str) else raw_result

        # Handle nested structure [{'type': 'text', 'text': '{...}'}]
        if isinstance(parsed, list) and len(parsed) > 0:
            inner = parsed[0]
            if isinstance(inner, dict) and "text" in inner:
                parsed = json.loads(inner["text"])

        # Extract results list
        results = parsed.get("results", []) if isinstance(parsed, dict) else []

        if not results:
            logger.warning("No results found in MCP response")
            return "No results found."

        # Format each result cleanly
        formatted = []
        for item in results:
            formatted.append(
                f"ID: {item.get('id', 'N/A')}\n"
                f"Title: {item.get('title', 'N/A')}\n"
                f"URL: {item.get('url', 'N/A')}\n"
                f"Content: {clean_html(item.get('snippet', 'N/A'))}\n"
            )

        cleaned = "\n---\n".join(formatted)
        logger.info(f"Formatted {len(results)} MCP results")
        return cleaned

    except Exception as e:
        logger.error(f"Failed to format MCP results: {e}")
        return str(raw_result)


def format_web_results(raw_result) -> str:
    """Clean and format web search results for LLM consumption.

    Args:
        raw_result: Raw result from web search tool (dict or string)

    Returns:
        Cleaned formatted string ready for LLM consumption
    """
    try:
        # Handle both dict and string inputs
        parsed = ast.literal_eval(raw_result) if isinstance(raw_result, str) else raw_result

        formatted = []

        # Main organic results
        for item in parsed.get("organic", []):
            formatted.append(
                f"Title: {item.get('title', 'N/A')}\n"
                f"URL: {item.get('link', 'N/A')}\n"
                f"Content: {clean_html(item.get('snippet', 'N/A'))}\n"
            )

        # People also ask - good for description quality
        for item in parsed.get("peopleAlsoAsk", []):
            formatted.append(
                f"Title: {item.get('title', 'N/A')}\n"
                f"URL: {item.get('link', 'N/A')}\n"
                f"Content: {clean_html(item.get('snippet', 'N/A'))}\n"
            )

        if not formatted:
            logger.warning("No results found in web search response")
            return "No results found."

        cleaned = "\n---\n".join(formatted)
        logger.info(f"Formatted {len(formatted)} web results")
        return cleaned

    except Exception as e:
        logger.error(f"Failed to format web results: {e}")
        return str(raw_result)


def format_tool_result(tool_name: str, raw_result, mcp_tool_names: set) -> str:
    """Format tool result based on tool type.

    Args:
        tool_name: Name of the tool that was executed
        raw_result: Raw result from tool execution
        mcp_tool_names: Set of MCP tool names

    Returns:
        Formatted result string
    """
    if tool_name in mcp_tool_names:
        return format_mcp_results(raw_result)
    elif tool_name == "web_search":
        return format_web_results(raw_result)

    return str(raw_result)
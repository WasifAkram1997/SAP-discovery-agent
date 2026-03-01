"""Tool registry and initialization."""

from typing import List
from langchain_core.tools import BaseTool
from sap_discovery.tools.mcp_tools import (
    initialize_mcp_client,
    sap_help_search,
    get_mcp_tools,
    is_mcp_available
)
from sap_discovery.tools.web_tools import web_search
from sap_discovery.utils.logging import setup_logger

logger = setup_logger(__name__)


async def get_all_tools() -> List[BaseTool]:
    """Initialize and return all available tools with fallback.

    This handles async initialization of MCP client. If MCP initialization fails,
    it falls back to web search only without crashing the application.

    Returns:
        List of available tools (MCP + web if MCP available, web-only if not)
    """
    # Try to initialize MCP client
    mcp_success = await initialize_mcp_client()

    if mcp_success:
        # MCP available - include all tools
        remaining_mcp = get_mcp_tools()
        all_tools = [sap_help_search] + remaining_mcp + [web_search]
        logger.info(f"Tool registry: {len(all_tools)} tools available (MCP + web)")
    else:
        # MCP unavailable - fallback to web search only
        all_tools = [web_search]
        logger.warning("Tool registry: MCP unavailable, using web_search only")

    return all_tools


def get_tools_by_name(tools: List[BaseTool]) -> dict:
    """Create a name->tool lookup dictionary.

    Args:
        tools: List of tools

    Returns:
        Dictionary mapping tool name to tool instance
    """
    return {t.name: t for t in tools}

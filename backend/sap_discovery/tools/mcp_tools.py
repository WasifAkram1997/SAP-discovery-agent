"""MCP-based SAP documentation search tools."""

import logging
from typing import Optional
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.tools import tool
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log,
    RetryError
)
from sap_discovery.config import (
    MCP_SERVER_CONFIG,
    MCP_RETRY_ATTEMPTS,
    MCP_RETRY_MIN_WAIT,
    MCP_RETRY_MAX_WAIT
)
from sap_discovery.utils.logging import setup_logger

logger = setup_logger(__name__)

# Global client instance (initialized async)
_mcp_client: Optional[MultiServerMCPClient] = None
_raw_search_tool = None
_mcp_tools = None
_mcp_available = False


@retry(
    stop=stop_after_attempt(MCP_RETRY_ATTEMPTS),
    wait=wait_exponential(multiplier=1, min=MCP_RETRY_MIN_WAIT, max=MCP_RETRY_MAX_WAIT),
    retry=retry_if_exception_type((ConnectionError, TimeoutError, Exception)),
    before_sleep=before_sleep_log(logger, logging.WARNING)
)
async def _connect_mcp_client():
    """Connect to MCP server with retry logic.

    Raises:
        Exception: If connection fails after all retries
    """
    mcp_config = {
        name: {"url": config["url"], "transport": config["transport"]}
        for name, config in MCP_SERVER_CONFIG.items()
    }

    logger.info("Attempting to connect to MCP server...")
    client = MultiServerMCPClient(mcp_config)
    tools = await client.get_tools()
    logger.info(f"Successfully connected to MCP server. {len(tools)} tools available.")

    return client, tools


async def initialize_mcp_client():
    """Initialize the MCP client asynchronously with retry and fallback.

    Returns:
        bool: True if MCP initialized successfully, False otherwise
    """
    global _mcp_client, _raw_search_tool, _mcp_tools, _mcp_available

    if _mcp_client is not None:
        return _mcp_available

    try:
        _mcp_client, _mcp_tools = await _connect_mcp_client()
        _raw_search_tool = next(
            (t for t in _mcp_tools if t.name == "search"),
            None
        )

        if _raw_search_tool is None:
            logger.error("Search tool not found in MCP tools")
            _mcp_available = False
            return False

        _mcp_available = True
        logger.info("MCP client initialized successfully")
        return True

    except RetryError as e:
        logger.error(f"Failed to connect to MCP server after retries: {e}")
        _mcp_available = False
        return False

    except Exception as e:
        logger.error(f"Unexpected error initializing MCP client: {e}")
        _mcp_available = False
        return False


@tool
async def sap_help_search(query: str, sources: list[str], k: int = 40) -> str:
    """Search SAP documentation.

    Args:
        query: search terms
        sources: documentation source, use 'sap-help' for SAP Help Portal
        k: number of chunks to retrieve. Default is 40
    """
    if not _mcp_available or _raw_search_tool is None:
        logger.warning("sap_help_search called but MCP unavailable")
        return "SAP documentation search unavailable."

    try:
        return await _raw_search_tool.ainvoke({
            "query": query,
            "sources": sources,
            "k": k
        })
    except Exception as e:
        logger.error(f"Error calling sap_help_search: {e}")
        return f"Error searching SAP documentation: {str(e)}"


def get_mcp_tools():
    """Get all MCP tools excluding raw search.

    Returns:
        List of MCP tools, empty list if MCP unavailable
    """
    if not _mcp_available or _mcp_client is None:
        logger.warning("MCP tools requested but MCP is not available")
        return []

    return [t for t in _mcp_tools if t.name != "search"]


def get_mcp_tool_names() -> set:
    """Get set of MCP tool names for source extraction and formatting.

    Includes both original MCP tool names and custom wrapped tool names.

    Returns:
        Set of MCP tool names (empty if MCP unavailable)
    """
    if not _mcp_available or _mcp_client is None:
        return set()

    # Original MCP tool names
    names = {t.name for t in _mcp_tools}

    # Add custom wrapper names that return same format
    names.add("sap_help_search")       # wrapper around search
    names.add("sap_community_search")  # same result format

    return names


def is_mcp_available() -> bool:
    """Check if MCP client is available.

    Returns:
        True if MCP is connected and ready, False otherwise
    """
    return _mcp_available
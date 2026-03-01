"""Health check utilities."""

from sap_discovery.tools.mcp_tools import is_mcp_available


def get_system_status() -> dict:
    """Get current system health status.

    Returns:
        Dictionary with status information
    """
    mcp_available = is_mcp_available()

    return {
        "mcp_available": mcp_available,
        "web_search_available": True,  # Always available
        "status": "healthy" if mcp_available else "degraded"
    }

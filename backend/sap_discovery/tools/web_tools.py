"""Web search tools for SAP research."""

from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.tools import tool

search = GoogleSerperAPIWrapper(k=5)


@tool
def web_search(query: str) -> str:
    """Search the web for SAP-related information.

    Use this to find additional context about SAP processes.

    Args:
        query: Search query string

    Returns:
        Search results as JSON string
    """
    return search.results(query)

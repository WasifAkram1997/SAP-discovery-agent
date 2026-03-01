"""Search tools for the main agent."""

from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.tools import tool


@tool
def web_search(query: str) -> str:
    """Search the web for SAP-related information.

    Use this to answer general questions about:
    - SAP modules and their purpose
    - Transaction codes and what they do
    - SAP processes and best practices
    - Fiori apps and their functionality
    - General SAP concepts and terminology

    Args:
        query: Search query about SAP

    Returns:
        Search results with relevant information
    """
    search = GoogleSerperAPIWrapper(k=5)
    return search.run(query)

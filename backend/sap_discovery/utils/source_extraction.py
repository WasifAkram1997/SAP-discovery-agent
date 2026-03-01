"""Utilities for extracting source references from tool results."""

import re
import json
from typing import List


def extract_sources_from_tool_result(tool_name: str, result: str, mcp_tool_names: set) -> List[dict]:
    """Extract source references (URLs, titles) from tool execution results.

    Args:
        tool_name: Name of the tool that was executed
        result: Raw result string from tool execution
        mcp_tool_names: Set of MCP tool names to identify SAP docs vs web

    Returns:
        List of source dictionaries with keys: title, url, source_type
    """
    sources = []

    if tool_name == "web_search":
        try:
            data = json.loads(result) if isinstance(result, str) else result
            items = data.get("organic", []) if isinstance(data, dict) else data
            for item in items:
                if isinstance(item, dict) and (item.get("link") or item.get("url")):
                    sources.append({
                        "title": item.get("title", "Web Result"),
                        "url": item.get("link", item.get("url", "")),
                        "source_type": "web"  # matches Literal
                    })
        except (json.JSONDecodeError, TypeError):
            urls = re.findall(r'https?://[^\s<>"\')\]]+', str(result))
            for url in urls[:5]:
                sources.append({"title": "Web Source", "url": url, "source_type": "web"})

    elif tool_name in mcp_tool_names:
        try:
            data = json.loads(result) if isinstance(result, str) else result
            items = data if isinstance(data, list) else [data]
            for item in items:
                if isinstance(item, dict):
                    url = item.get("url", item.get("link", item.get("id", "")))
                    title = item.get("title", item.get("name", item.get("description", "")))
                    if url:
                        sources.append({
                            "title": title[:100] if title else "SAP Documentation",
                            "url": str(url),
                            "source_type": "sap_docs"  # matches Literal
                        })
        except (json.JSONDecodeError, TypeError):
            pass

        urls = re.findall(r'https?://[^\s<>"\')\]]+', str(result))
        existing_urls = {s["url"] for s in sources}
        for url in urls[:5]:
            if url not in existing_urls:
                sources.append({"title": "SAP Reference", "url": url, "source_type": "sap_docs"})

    return sources

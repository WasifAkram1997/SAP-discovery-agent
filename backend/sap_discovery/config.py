"""Configuration constants for SAP Process Discovery Agent."""

# Quality dimension weights (must sum to 1.0)
WEIGHTS = {
    "module_coverage":    0.20,  # easier to find
    "tcode_confidence":   0.30,  # harder, more valuable
    "fiori_presence":     0.30,  # harder, more valuable
    "description_quality": 0.20  # synthesized from all results
}

# Quality threshold for synthesis
THRESHOLD = 0.80

# Maximum iterations before forcing synthesis
MAX_ITERATIONS = 3

# MCP server configuration
MCP_SERVER_CONFIG = {
    "sap-docs": {
        "url": "https://mcp-sap-docs.marianzeis.de/mcp",
        "transport": "streamable_http",
        "erp_type": "SAP"
    }
}

# MCP retry configuration
MCP_RETRY_ATTEMPTS = 3
MCP_RETRY_MIN_WAIT = 1
MCP_RETRY_MAX_WAIT = 10

# Dimension-specific search guidance templates
DIMENSION_SEARCH_GUIDANCE = {
    "module_coverage":    "SAP module classification for {process}",
    "tcode_confidence":   "SAP transaction codes for {process}",
    "fiori_presence":     "SAP Fiori apps for {process}",
    "description_quality": "SAP step by step execution process for {process}"
}

# Missing threshold - scores <= this trigger re-research
MISSING_THRESHOLD = 0.5
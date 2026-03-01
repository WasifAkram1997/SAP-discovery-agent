# SAP Process Discovery Agent - Project Context

## Overview
LangGraph-based agent that maps business processes to SAP artifacts (modules, t-codes, Fiori apps, execution flows). Built for Syntax GenAI Platform Developer assessment.

## Architecture
```
START → perception → plan → action → scoring → synthesis → END
                      ↑                   │
                      └───────────────────┘ (loop until quality ≥ 0.60 or 3 iterations)
```

### Nodes
| Node | Purpose |
|------|---------|
| `perception` | Generates 4 targeted SAP queries (module, t-codes, fiori, flow) |
| `plan` | Decides tool calls based on quality gaps |
| `action` | Executes tools, extracts sources |
| `scoring` | Scores 4 dimensions (0-1 each), identifies gaps |
| `synthesis` | Produces final `SAPProcessMapping` structured output |

### Quality Dimensions (weighted 0.25 each)
- `module_coverage` - SAP modules identified
- `tcode_confidence` - Transaction codes found
- `fiori_presence` - Fiori apps mentioned
- `execution_flow_depth` - Step-by-step flow described

## Key Files
| File | Purpose |
|------|---------|
| `Subagent.ipynb` | Main implementation (LangGraph workflow + main agent) |
| `Car_Rental_Business_Processes_Detailed.xlsx` | Input: 15 business processes |
| `.env` | API keys (OPENAI_API_KEY, SERPER_API_KEY) |
| `requirements.txt` | Python dependencies |
| `sap_process_mappings.xlsx` | Output: generated SAP mappings |

## Tools
1. `sap_help_search` - MCP server → SAP Help Portal docs
2. `web_search` - Google Serper API for supplementary research

## Main Agent (LangChain 1.0)
- Uses `create_agent()` with memory (`MemorySaver`)
- Has `SummarizationMiddleware` (summarizes every 10 messages)
- Tools: `run_sap_discovery`, `export_to_excel`, `display_process_report`

## Current State
- ✅ Subagent workflow complete and tested
- ✅ Main agent with conversational interface working
- ⚠️ `USE_MOCK = True` in notebook (flip to False for real API calls)
- 🔲 No CLI/Streamlit UI yet (runs in Jupyter)
- 🔲 Only processes first item when not mocked

## Models Used
- Subagent: `gpt-5-mini` (structured output)
- Main agent: `gpt-4o`
- Summarization: `gpt-4o-mini`

## MCP Server Config
```python
erp_configs = {
    "sap-docs": {
        "url": "https://mcp-sap-docs.marianzeis.de/mcp",
        "transport": "streamable_http"
    }
}
```

## Output Schema
```python
class SAPProcessMapping:
    process: str
    module: List[str]          # MM, FI, CO, SD, PM, HCM
    transaction_codes: List[str]
    fiori_apps: List[str]
    execution_flow: List[str]
    configuration_dependencies: List[str]
    integration_points: List[str]
    references: List[Reference]
```

## To Run
1. Activate venv: `.\venv\Scripts\Activate.ps1`
2. Open `Subagent.ipynb` in Jupyter/VS Code
3. Run all cells
4. Interact via the chat loop at bottom

## Next Steps
- [ ] Build Streamlit UI or CLI
- [ ] Test with `USE_MOCK = False`
- [ ] Process all 15 business processes
- [ ] Add error handling for API failures

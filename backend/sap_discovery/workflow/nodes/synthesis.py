"""Synthesis node - generates final structured output."""

from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from sap_discovery.workflow.state import AgentState
from sap_discovery.models.schema import SAPProcessMapping, Reference
from sap_discovery.utils.logging import setup_logger
from sap_discovery.utils.deduplicate import build_refs 

logger = setup_logger(__name__)

def synthesis_node(state: AgentState, llm_structured) -> dict:
    """Generate final SAPProcessMapping from research results.

    Args:
        state: Current agent state
        llm_structured: LLM instance with SAPProcessMappingLLM structured output

    Returns:
        Dictionary with structured_output and synthesis_success flag
    """
    process = state["process_input"]
    process_name = process.get("Process Name", process.get("process", "Unknown Process"))
    collected_sources = state.get("collected_sources", [])

    tool_results = [
        msg.content for msg in state["messages"]
        if isinstance(msg, ToolMessage) and msg.content
    ]
    research_summary = "\n\n---\n\n".join(tool_results) if tool_results else "No research data available."

    references = build_refs(collected_sources)

    prompt = f"""You are mapping an SAP business process based on research findings below.
Process: {process_name}

Research Findings:
{research_summary}

Instructions:

**Modules:**
- Include ALL SAP modules mentioned in the findings
- Prefer standard modules: MM, FI, SD, CO, HR, PM, CS, WM, EWM
- Include industry-specific modules if clearly relevant (VMS, DBM, DVH)

**Transaction Codes:**
- Only include valid executable SAP transaction codes
- Valid format: short alphanumeric codes (ME21N, FB60, VELO, VELOM)
- Namespace codes are acceptable if clearly relevant (/DBM/VM, /DBM/VSEARCH)
- ABAP object names, table names, field names are NOT transaction codes
- When in doubt, omit it

**Fiori Apps:**
- Include ANY Fiori app names mentioned in the findings
- Look for:
  * App names from SAP Fiori Apps Reference Library
  * Apps mentioned in SAP Help Portal snippets
  * Apps with F-numbers or app IDs
  * Examples: "Manage Vehicle Processes", "View Vehicles", "Modify Vehicles"
- Do NOT leave empty if Fiori apps are mentioned anywhere in findings

**Description:**
- Write a contextual explanation of the process
- Include step by step execution flow using SAP terminology
- Include configuration dependencies where relevant
- Include integration points with other modules where relevant

**General Rules:**
- Leave fields as empty lists ONLY if truly not mentioned anywhere
- DO NOT generate URLs or references
- DO NOT invent information not present in findings
-ABAP object names, table names, field names are NOT transaction codes
"""
    try:
        llm_result = llm_structured.invoke([
            SystemMessage(content="You are an SAP expert. Extract structured process mapping strictly from the provided research findings."),
            HumanMessage(content=prompt)
        ])

        final_output = SAPProcessMapping(
            **llm_result.model_dump(),
            references=references
        )

        logger.info(f"Modules: {final_output.module}")
        logger.info(f"T-codes: {final_output.transaction_codes}")
        logger.info(f"Fiori apps: {final_output.fiori_apps}")
        logger.info(f"References: {len(references)} total")

        return {
            "structured_output": final_output,
            "synthesis_success": True
        }

    except Exception as e:
        logger.error(f"Synthesis failed: {e}")
        return {
            "structured_output": SAPProcessMapping(
                process=process_name,
                module=[], transaction_codes=[], fiori_apps=[],
                description="Synthesis failed.",
                references=references
            ),
            "synthesis_success": False
        }
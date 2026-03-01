"""Tools for the main conversational agent."""

import json
from io import BytesIO
import pandas as pd
from langchain.tools import tool
from langchain_core.runnables import RunnableConfig
from sap_discovery.models.schema import SAPProcessMapping, Reference
from sap_discovery.utils import session_state


# Workflow graph (stateless, safe to share across sessions)
_workflow_graph = None


def set_workflow_graph(graph):
    """Set the workflow graph for tool execution."""
    global _workflow_graph
    _workflow_graph = graph


def update_processes(session_id: str, job_id: str, processes: list):
    """Store processes for a specific job under a session."""
    from sap_discovery.utils.logging import setup_logger
    logger = setup_logger(__name__)

    session_state.set_processes(session_id, job_id, processes)
    logger.info(f"Session {session_id[:8]}: Job {job_id[:8]}: Stored {len(processes)} processes")


@tool
async def run_sap_discovery(job_id: str, config: RunnableConfig) -> str:
    """Run SAP Process Discovery on all uploaded business processes in parallel batches.

    Args:
        job_id: The job ID returned when the Excel file was uploaded
        config: Injected automatically by LangChain — contains session_id

    Returns:
        Confirmation message with summary
    """
    import asyncio
    from sap_discovery.workflow.executor import process_single
    from sap_discovery.models.schema import SAPProcessMapping
    from sap_discovery.utils.logging import setup_logger

    logger = setup_logger(__name__)

    session_id = config.get("configurable", {}).get("session_id")
    if not session_id:
        return "Error: No session ID found. Please try again."

    processes = session_state.get_processes(session_id, job_id)

    if not processes:
        return f"No processes found for job {job_id}. Please upload an Excel file first."

    if _workflow_graph is None:
        return "Workflow not initialized. Please try again."

    logger.info(f"Session {session_id[:8]}: Job {job_id[:8]}: Starting SAP discovery for {len(processes)} processes...")

    semaphore = asyncio.Semaphore(5)

    async def process_with_semaphore(process: dict, index: int):
        async with semaphore:
            logger.info(f"Session {session_id[:8]} [{index+1}/{len(processes)}] Processing: {process.get('name', 'Unknown')}")
            try:
                result = await process_single(process, _workflow_graph)
                logger.info(f"Session {session_id[:8]} [{index+1}/{len(processes)}] ✓ Completed: {process.get('name', 'Unknown')}")
                return result
            except Exception as e:
                logger.error(f"Session {session_id[:8]} [{index+1}/{len(processes)}] ✗ Failed: {process.get('name', 'Unknown')} - {e}")
                return SAPProcessMapping(
                    process=process.get('name', 'Unknown'),
                    module=[],
                    transaction_codes=[],
                    fiori_apps=[],
                    description=f"Error processing: {str(e)}",
                    references=[]
                )

    results = await asyncio.gather(
        *[process_with_semaphore(proc, i) for i, proc in enumerate(processes)],
        return_exceptions=False
    )

    results_list = [r.model_dump() for r in results if r is not None]
    session_state.set_result(job_id, json.dumps(results_list, indent=2))

    successful = sum(1 for r in results if r and r.module)
    total = len(processes)

    logger.info(f"Session {session_id[:8]}: Job {job_id[:8]}: SAP discovery completed: {successful}/{total} successful")

    return f"""SAP discovery completed successfully!

Job ID: {job_id}
Processed: {total} processes
Successful: {successful} processes

Use 'display results' to view all mappings or 'export to excel' to save them."""


@tool
async def export_to_excel(job_id: str, config: RunnableConfig) -> str:
    """Export SAP process mapping data to an Excel file.

    Args:
        job_id: The job ID from the SAP discovery run
        config: Injected automatically by LangChain — contains session_id
    """
    session_id = config.get("configurable", {}).get("session_id")
    if not session_id:
        return "Error: No session ID found. Please try again."

    last_result = session_state.get_result(session_id, job_id)
    if not last_result:
        return f"No results found for job {job_id}. Please run SAP discovery first."

    try:
        data = json.loads(last_result)

        if isinstance(data, dict):
            results = [data]
        else:
            results = data

        rows = []
        for result in results:
            rows.append({
                'Process':          result.get('process', ''),
                'SAP Modules':      ', '.join(result.get('module', [])),
                'Transaction Codes': ', '.join(result.get('transaction_codes', [])),
                'Fiori Apps':       ', '.join(result.get('fiori_apps', [])),
                'Description':      result.get('description', ''),
                'References':       ', '.join(ref.get('url', '') for ref in result.get('references', [])),
            })

        df = pd.DataFrame(rows)
        buf = BytesIO()
        with pd.ExcelWriter(buf, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='SAP Mappings')

        output_path = f'sap_process_mappings_{session_id[:8]}.xlsx'
        with open(output_path, 'wb') as f:
            f.write(buf.getvalue())

        return f"Excel file exported successfully!\n\nFile: {output_path}\nRows: {len(rows)} processes"

    except Exception as e:
        return f"Error exporting to Excel: {str(e)}"


def format_single_result(r: dict) -> str:
    """Format a single SAPProcessMapping as markdown."""
    def format_list(items: list) -> str:
        return ", ".join(items) if items else "N/A"

    def format_refs(refs: list) -> str:
        if not refs:
            return "  - N/A"
        return "\n".join(
            f"  - [{ref.get('title', 'Unknown')}]({ref.get('url', '')})"
            for ref in refs
        )

    return f"""
## SAP Process Mapping: {r.get('process')}

| Field | Details |
|-------|---------|
| **Modules** | {format_list(r.get('module', []))} |
| **Transaction Codes** | {format_list(r.get('transaction_codes', []))} |
| **Fiori Apps** | {format_list(r.get('fiori_apps', []))} |

**Description:**
{r.get('description', 'N/A')}

**References:**
{format_refs(r.get('references', []))}
""".strip()


def format_multiple_results(results: list) -> str:
    """Format multiple SAPProcessMapping objects as a summary table + details."""
    if not results:
        return "No results to display."

    summary = f"## SAP Process Discovery Results ({len(results)} processes)\n\n"
    summary += "| Process | Modules | T-Codes | Fiori Apps |\n"
    summary += "|---------|---------|---------|------------|\n"

    for r in results:
        process = r.get('process', 'Unknown')[:40]
        modules = len(r.get('module', []))
        tcodes = len(r.get('transaction_codes', []))
        fiori = len(r.get('fiori_apps', []))
        summary += f"| {process} | {modules} | {tcodes} | {fiori} |\n"

    summary += "\n---\n\n"

    for i, r in enumerate(results, 1):
        summary += f"### {i}. {r.get('process', 'Unknown')}\n\n"
        summary += f"**Modules:** {', '.join(r.get('module', [])) or 'N/A'}\n\n"
        summary += f"**Transaction Codes:** {', '.join(r.get('transaction_codes', [])) or 'N/A'}\n\n"
        summary += f"**Fiori Apps:** {', '.join(r.get('fiori_apps', [])) or 'N/A'}\n\n"

        desc = r.get('description', 'N/A')
        if len(desc) > 500:
            desc = desc[:500] + "..."
        summary += f"**Description:** {desc}\n\n"

        refs = r.get('references', [])
        if refs:
            summary += "**References:** " + ", ".join(f"[{ref.get('title', 'Link')}]({ref.get('url', '')})" for ref in refs[:3])
            if len(refs) > 3:
                summary += f" (+{len(refs)-3} more)"
            summary += "\n\n"

        summary += "---\n\n"

    return summary.strip()


@tool(return_direct=True)
async def display_process_report(job_id: str, config: RunnableConfig) -> str:
    """Display SAP process mapping results as a structured report in chat.

    Args:
        job_id: The job ID from the SAP discovery run
        config: Injected automatically by LangChain — contains session_id
    """
    session_id = config.get("configurable", {}).get("session_id")
    if not session_id:
        return "Error: No session ID found. Please try again."

    last_result = session_state.get_result(session_id, job_id)
    if not last_result:
        return f"No results found for job {job_id}. Please run SAP discovery first."

    try:
        data = json.loads(last_result)
        if isinstance(data, list):
            return format_multiple_results(data)
        else:
            return format_single_result(data)
    except json.JSONDecodeError:
        return "Error: Could not parse results."
"""Test the SAP Process Discovery subagent workflow."""

import asyncio
import os
from dotenv import load_dotenv

# Get base directory (project root)
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


async def main():
    # Load environment variables
    load_dotenv()

    print("="*80)
    print("SAP Process Discovery - Subagent Test")
    print("="*80)

    from sap_discovery.data.loader import load_processes
    from sap_discovery.tools.registry import get_all_tools
    from sap_discovery.llm.models import create_llm_instances
    from sap_discovery.workflow.graph import compile_workflow
    from sap_discovery.workflow.executor import process_single

    print("\n[1/5] Loading business processes...")
    excel_path = os.path.join(base_dir, "Car_Rental_Business_Processes_Detailed.xlsx")
    processes = load_processes(excel_path)

    print("\n[2/5] Initializing tools (MCP client)...")
    tools = await get_all_tools()
    print(f"       Loaded {len(tools)} tools: {[t.name for t in tools]}")

    print("\n[3/5] Creating LLM instances...")
    llm_instances = create_llm_instances(tools)
    print(f"       Created {len(llm_instances)} LLM instances")

    print("\n[4/5] Compiling workflow graph...")
    graph = compile_workflow(llm_instances, tools)

    print("\n[5/5] Processing first business process...\n")
    process = processes[0]
    print(f"Process: {process.get('Process Name', 'Unknown')}\n")

    result = await process_single(process, graph)

    print("\n" + "="*80)
    print("RESULT")
    print("="*80)
    print(f"Process: {result.process}")
    print(f"Modules: {', '.join(result.module) if result.module else 'None'}")
    print(f"Transaction Codes: {', '.join(result.transaction_codes) if result.transaction_codes else 'None'}")
    print(f"Fiori Apps: {len(result.fiori_apps)} apps")
    print(f"Description: {result.description[:100]}...")
    # print(f"Execution Flow Steps: {len(result.execution_flow)}")
    # print(f"Integration Points: {len(result.integration_points)}")
    print(f"References: {len(result.references)}")
    print("="*80)

    return result


if __name__ == "__main__":
    result = asyncio.run(main())
    print("\nTest completed successfully!")

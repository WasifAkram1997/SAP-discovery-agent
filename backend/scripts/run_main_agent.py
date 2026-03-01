"""Run the SAP Process Discovery main conversational agent."""

import asyncio
import os
from dotenv import load_dotenv

# Get base directory (project root)
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


async def main():
    # Load environment variables
    load_dotenv()

    print("="*80)
    print("SAP Process Discovery - Main Conversational Agent")
    print("="*80)

    from sap_discovery.data.loader import load_processes
    from sap_discovery.tools.registry import get_all_tools
    from sap_discovery.llm.models import create_llm_instances
    from sap_discovery.workflow.graph import compile_workflow
    from sap_discovery.main_agent.agent import create_main_agent
    from sap_discovery.main_agent.chat import run_chat
    from sap_discovery.main_agent.tools import set_workflow_context

    print("\n[1/6] Loading business processes...")
    excel_path = os.path.join(base_dir, "Car_Rental_Business_Processes_Detailed.xlsx")
    processes = load_processes(excel_path)

    print("\n[2/6] Initializing tools (MCP client)...")
    tools = await get_all_tools()
    print(f"       Loaded {len(tools)} tools")

    print("\n[3/6] Creating LLM instances...")
    llm_instances = create_llm_instances(tools)

    print("\n[4/6] Compiling workflow graph...")
    graph = compile_workflow(llm_instances, tools)

    print("\n[5/6] Setting workflow context for main agent...")
    set_workflow_context(graph, processes)

    print("\n[6/6] Creating main agent...")
    agent = create_main_agent()

    print("\n" + "="*80)
    print("Agent ready! You can now chat with the SAP Process Discovery assistant.")
    print("Try commands like:")
    print("  - 'Run SAP discovery'")
    print("  - 'Display the results'")
    print("  - 'Export to Excel'")
    print("="*80 + "\n")

    # Run chat loop
    await run_chat(agent)

    print("\nGoodbye!")


if __name__ == "__main__":
    asyncio.run(main())

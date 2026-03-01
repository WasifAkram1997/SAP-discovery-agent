"""Test SAP Process Discovery subagent."""

import asyncio
import sys
from dotenv import load_dotenv
sys.path.append('.')

load_dotenv()

from langchain_core.messages import ToolMessage


async def main():
    print("=" * 80)
    print("SAP Process Discovery - Subagent Test")
    print("=" * 80)

    # Import inside to catch import errors clearly
    from sap_discovery.workflow.graph import compile_workflow
    from sap_discovery.tools.registry import get_all_tools
    from sap_discovery.llm.models import create_llm_instances
    from sap_discovery.workflow.executor import process_single

    # Initialize tools
    print("\nInitializing tools...")
    tools = await get_all_tools()
    print(f"Tools available: {[t.name for t in tools]}")

    # Create LLM instances
    print("\nCreating LLM instances...")
    llm_instances = create_llm_instances(tools)

    # Compile workflow
    print("\nCompiling workflow...")
    graph = compile_workflow(llm_instances, tools)

    # Test process
    process = {
        "Process Name": "Vehicle Procurement",
        "Description": "Procurement of vehicles from manufacturers",
        "_row_id": 0
    }

    print(f"\nProcess: {process['Process Name']}")

    # Run workflow
    from sap_discovery.workflow.state import AgentState
    initial_state = AgentState(
        messages=[],
        process_input=process,
        iteration=0,
        structured_output=None,
        collected_sources=[],
        quality_score=None,
        synthesis_success=False
    )

    final_state = await graph.ainvoke(initial_state)

    # Debug tool messages for Fiori mentions
    print("\n--- SEARCHING TOOL MESSAGES FOR FIORI ---")
    for msg in final_state["messages"]:
        if isinstance(msg, ToolMessage):
            if "fiori" in msg.content.lower() or \
               "view vehicles" in msg.content.lower() or \
               "modify vehicles" in msg.content.lower() or \
               "manage vehicle" in msg.content.lower():
                print(f"\n✅ Fiori mention found:")
                print(msg.content[:500])
                print("...")

    # Print scoring
    quality_score = final_state.get("quality_score")
    if quality_score:
        print("\n--- SCORING ---")
        print(f"Module:      {quality_score.dimensions.module_coverage}")
        print(f"TCode:       {quality_score.dimensions.tcode_confidence}")
        print(f"Fiori:       {quality_score.dimensions.fiori_presence}")
        print(f"Description: {quality_score.dimensions.description_quality}")
        print(f"Total:       {quality_score.total}")
        print(f"Missing:     {quality_score.missing}")

    # Print final result
    result = final_state.get("structured_output")
    if result:
        print("\n" + "=" * 80)
        print("RESULT")
        print("=" * 80)
        print(f"Process:     {result.process}")
        print(f"Modules:     {result.module}")
        print(f"T-codes:     {result.transaction_codes}")
        print(f"Fiori Apps:  {result.fiori_apps}")
        print(f"Description: {result.description[:100]}...")
        print(f"References:  {len(result.references)}")
        print("\n--- REFERENCES ---")
        for ref in result.references:
            print(f"  - [{ref.title}]({ref.url})")


asyncio.run(main())
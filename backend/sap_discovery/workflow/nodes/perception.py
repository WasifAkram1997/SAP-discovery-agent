# """Perception node - generates targeted research queries."""

# from langchain_core.messages import SystemMessage, HumanMessage
# from sap_discovery.workflow.state import AgentState


# def perception_node(state: AgentState, llm_perception) -> dict:
#     """Generate 4 targeted SAP research queries.

#     Args:
#         state: Current agent state
#         llm_perception: LLM instance with PerceptionOutput structured output

#     Returns:
#         Dictionary with queries list and iteration reset to 0
#     """
#     process = state["process_input"]
#     process_text = "\n".join([f"{k}: {v}" for k, v in process.items() if k != "_row_id" and v])

#     prompt = f"""You are an SAP expert generating targeted research queries for a specific business process.

# Your goal is to find exactly these 4 things:
# 1. SAP Module (MM, FI, CO, SD, HR, PM, etc.)
# 2. Transaction codes (e.g. ME21N, FB60, VA01)
# 3. Fiori app names and IDs
# 4. Step-by-step execution flow in SAP

# Generate 4 queries — one focused on each target above.

# Rules:
# - Each query <= 6 words
# - Use SAP-specific terminology

# INPUT:
# {process_text}

# OUTPUT: exactly 4 queries, one per target, in order: module → t-codes → fiori apps → execution flow.
# """
#     result = llm_perception.invoke([
#         SystemMessage(content="You are an SAP expert. Generate targeted research queries."),
#         HumanMessage(content=prompt)
#     ])

#     return {
#         "queries": result.queries,
#         "iteration": 0
#     }

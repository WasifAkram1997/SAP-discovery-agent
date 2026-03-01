"""State schema for the SAP Process Discovery workflow."""

from typing import TypedDict, Annotated, List, Optional
from langgraph.graph.message import add_messages
from sap_discovery.models.schema import SAPProcessMapping, QualityScore


class AgentState(TypedDict):
    """State schema for the SAP Process Discovery Agent."""
    messages: Annotated[list, add_messages]  # Conversation history with tool calls
    process_input: dict                       # Current business process being analyzed
    iteration: int                            # Track iterations to prevent infinite loops
    structured_output: Optional[SAPProcessMapping]  # Final synthesized result
    collected_sources: List[dict]             # Track real sources: {"title": str, "url": str, "source_type": "sap_docs"|"web"}
    # queries: List[str]                        # Generated queries from perception
    quality_score: Optional[QualityScore]     # Quality assessment scores
    synthesis_success: bool                # Flag to indicate if synthesis produced a valid output

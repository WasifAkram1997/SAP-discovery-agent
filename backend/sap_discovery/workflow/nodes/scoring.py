"""Scoring node - evaluates quality across 4 dimensions."""

from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from sap_discovery.workflow.state import AgentState
from sap_discovery.models.schema import DimensionScore, QualityScore
from sap_discovery.config import WEIGHTS, MISSING_THRESHOLD
from sap_discovery.utils.logging import setup_logger

logger = setup_logger(__name__)


def scoring_node(state: AgentState, llm_scoring) -> dict:
    """Evaluate quality of research results across 4 dimensions.

    Args:
        state: Current agent state
        llm_scoring: LLM instance with QualityScore structured output

    Returns:
        Dictionary with quality_score
    """
    tool_contents = "\n\n---\n\n".join([
        msg.content for msg in state["messages"]
        if isinstance(msg, ToolMessage) and msg.content
    ])

    if not tool_contents:
        return {
            "quality_score": QualityScore(
                dimensions=DimensionScore(),
                total=0.0,
                missing=list(WEIGHTS.keys())
            )
        }

    prompt = f"""You are evaluating research results for an SAP business process mapping task.

Score each dimension using EXACTLY this scale:

**module_coverage** - Is a specific SAP module identified?
0.0 → no module mentioned at all
0.5 → generic mention only (e.g. "SAP ERP", "SAP system")
1.0 → specific module clearly identified (MM, FI, SD, CO, HR, PM etc.)

**tcode_confidence** - Are specific SAP transaction codes present?
0.0 → no transaction codes found
0.5 → transaction codes mentioned but unclear or unverified
1.0 → specific valid transaction codes found (e.g. ME21N, FB60, VA01, VELO)

**fiori_presence** - Are SAP Fiori app names or IDs present?
0.0 → no Fiori apps found
0.5 → Fiori mentioned generically but no specific app names
1.0 → specific Fiori app names or IDs found (e.g. "Manage Purchase Orders", F1234)

**description_quality** - Is there a contextual description of the process?
0.0 → no description or execution flow found
0.5 → basic description present but missing execution flow OR config OR integration details
1.0 → complete description with execution flow, configuration dependencies and integration points

STRICT RULES:
- Use ONLY these values: 0.0, 0.5, 1.0
- Score based ONLY on what is explicitly present in the research content
- Do NOT infer or assume information that is not clearly stated
- Be strict - partial information scores 0.5, not 1.0

RESEARCH CONTENT:
{tool_contents}
"""

    try:
        result = llm_scoring.invoke([
            SystemMessage(content="You are an SAP expert evaluating research quality. Be strict and objective."),
            HumanMessage(content=prompt)
        ])

        # Code recomputes total for consistency
        total = round(
            result.dimensions.module_coverage * WEIGHTS["module_coverage"] +
            result.dimensions.tcode_confidence * WEIGHTS["tcode_confidence"] +
            result.dimensions.fiori_presence * WEIGHTS["fiori_presence"] +
            result.dimensions.description_quality * WEIGHTS["description_quality"],
            2
        )

        # Code recomputes missing using MISSING_THRESHOLD
        missing = [
            dim for dim, score in result.dimensions.model_dump().items()
            if score <= MISSING_THRESHOLD
        ]

        final_score = QualityScore(
            dimensions=result.dimensions,
            total=total,
            missing=missing
        )

        logger.info(
            f"Module:{result.dimensions.module_coverage} "
            f"TCode:{result.dimensions.tcode_confidence} "
            f"Fiori:{result.dimensions.fiori_presence} "
            f"Description:{result.dimensions.description_quality} "
            f"-> Total:{total}"
        )
        logger.info(f"Missing: {missing}")

        return {"quality_score": final_score}

    except Exception as e:
        logger.error(f"Scoring failed: {e}")
        return {
            "quality_score": QualityScore(
                dimensions=DimensionScore(),
                total=0.0,
                missing=list(WEIGHTS.keys())
            )
        }
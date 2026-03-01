"""LLM model instances and factories."""

from typing import List, Dict
from langchain_openai import ChatOpenAI
from langchain_core.tools import BaseTool
from sap_discovery.models.schema import (
    SAPProcessMappingLLM,
    QualityScore
)


def create_llm_instances(tools: List[BaseTool]) -> Dict:
    """Create all LLM instances needed for the workflow.

    Args:
        tools: List of tools to bind to the planning LLM

    Returns:
        Dictionary with llm instances:
        - base: Base LLM without tools
        - with_tools: LLM with tools bound (for planning)
        - structured: LLM for synthesis output
        - scoring: LLM for quality assessment
    """
    base_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    return {
        "base": base_llm,
        "with_tools": base_llm.bind_tools(tools),
        "structured": base_llm.with_structured_output(SAPProcessMappingLLM),
        "scoring": base_llm.with_structured_output(QualityScore),
    }
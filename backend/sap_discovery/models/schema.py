"""Pydantic models for SAP Process Discovery."""

from typing import List, Literal
from pydantic import BaseModel, Field


class SAPProcessMappingLLM(BaseModel):
    """LLM-generated output - NO references (those are extracted programmatically)."""
    process: str = Field(description="The business process name")
    module: List[str] = Field(description="Relevant SAP module(s) e.g. MM, FI, CO, SD, PM, HCM")
    transaction_codes: List[str] = Field(description="Standard SAP transaction codes e.g. ME21N, FB60, VA01")
    fiori_apps: List[str] = Field(description="Relevant SAP Fiori app names and IDs")
    description: str = Field(description="Contextual explanation of the process including execution flow, configuration dependencies and integration points where relevant")


class Reference(BaseModel):
    """Reference to source documentation."""
    title: str = Field(description="Title of the referenced document or page")
    url: str = Field(description="URL of the referenced document or page")
    source_type: Literal["sap_docs", "web"] = Field(description="Whether this came from SAP documentation or web search")


class SAPProcessMapping(SAPProcessMappingLLM):
    """Final output — extends LLM mapping with real extracted references."""
    references: List[Reference] = Field(default_factory=list, description="References extracted from tool results")

#     List[SAPProcessMapping], filename




class DimensionScore(BaseModel):
    module_coverage: float = 0.0      # SAP module identified?
    tcode_confidence: float = 0.0     # T-codes found?
    fiori_presence: float = 0.0       # Fiori apps found?
    description_quality: float = 0.0  # Contextual description complete?


class QualityScore(BaseModel):
    """Overall quality assessment."""
    dimensions: DimensionScore
    total: float
    missing: List[str]
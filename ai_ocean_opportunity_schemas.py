from __future__ import annotations

from pydantic import BaseModel, Field


class StudentProfile(BaseModel):
    """Placeholder student profile extracted from user-provided context."""

    summary: str | None = None
    interests: list[str] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)
    target_roles: list[str] = Field(default_factory=list)


class OpportunityIntelligence(BaseModel):
    """Placeholder opportunity snapshot extracted from a posting or brief."""

    title: str | None = None
    organization: str | None = None
    summary: str | None = None
    themes: list[str] = Field(default_factory=list)


class FitAnalysis(BaseModel):
    """Placeholder fit analysis for a student against an opportunity."""

    overall_fit: str = "pending"
    strengths: list[str] = Field(default_factory=list)
    gaps: list[str] = Field(default_factory=list)
    notes: str | None = None


class Positioning(BaseModel):
    """Placeholder positioning guidance to help a student stand out."""

    headline: str | None = None
    angle: str | None = None
    talking_points: list[str] = Field(default_factory=list)


class Draft(BaseModel):
    """Placeholder generated draft content for hackathon MVP flows."""

    format: str = "message"
    subject: str | None = None
    body: str = ""


class ParseProfileRequest(BaseModel):
    profile_text: str = ""


class ParseProfileResponse(BaseModel):
    profile: StudentProfile
    status: str = "placeholder"


class ExtractOpportunityRequest(BaseModel):
    opportunity_text: str = ""


class ExtractOpportunityResponse(BaseModel):
    opportunity: OpportunityIntelligence
    status: str = "placeholder"


class AnalyzeFitRequest(BaseModel):
    profile: StudentProfile
    opportunity: OpportunityIntelligence


class AnalyzeFitResponse(BaseModel):
    analysis: FitAnalysis
    status: str = "placeholder"


class GeneratePositioningRequest(BaseModel):
    profile: StudentProfile
    opportunity: OpportunityIntelligence
    analysis: FitAnalysis | None = None


class GeneratePositioningResponse(BaseModel):
    positioning: Positioning
    status: str = "placeholder"


class GenerateDraftRequest(BaseModel):
    profile: StudentProfile
    opportunity: OpportunityIntelligence
    positioning: Positioning | None = None
    draft_format: str = "message"


class GenerateDraftResponse(BaseModel):
    draft: Draft
    status: str = "placeholder"

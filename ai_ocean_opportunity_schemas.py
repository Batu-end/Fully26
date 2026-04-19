from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class StudentEvidence(BaseModel):
    label: str
    detail: str
    source_type: Literal[
        "activity",
        "coursework",
        "work",
        "leadership",
        "award",
        "project",
        "essay",
        "self-report",
        "other",
    ]


class StudentProfile(BaseModel):
    name: str
    school: str
    major: str
    gpa: float | None = None
    student_type: str
    graduation_year: str
    activities: list[str] = Field(default_factory=list)
    work_experience: list[str] = Field(default_factory=list)
    leadership_signals: list[str] = Field(default_factory=list)
    awards: list[str] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)
    interests: list[str] = Field(default_factory=list)
    financial_need_flag: bool
    identity_flags_opt_in: list[str] = Field(default_factory=list)
    core_story_themes: list[str] = Field(default_factory=list)
    evidence_bank: list[StudentEvidence] = Field(default_factory=list)
    career_goals: list[str] = Field(default_factory=list)


class OpportunityRequirement(BaseModel):
    requirement: str
    category: Literal[
        "academic",
        "citizenship",
        "location",
        "experience",
        "skills",
        "materials",
        "timing",
        "other",
    ]
    strictness: Literal["required", "preferred", "unclear"]
    notes: str


class OpportunityEstimatedEffort(BaseModel):
    time_hours_low: float
    time_hours_high: float
    writing_load: Literal["none", "short-response", "essay-heavy"]
    effort_level: Literal["low", "medium", "high"]


class OpportunityIntelligence(BaseModel):
    title: str
    provider: str
    opportunity_type: Literal[
        "scholarship",
        "internship",
        "fellowship",
        "research",
        "lab",
        "grant",
        "field",
        "other",
    ]
    amount_or_stipend: str
    deadline: str
    location: str
    raw_theme: str
    hard_requirements: list[OpportunityRequirement] = Field(default_factory=list)
    soft_preferences: list[str] = Field(default_factory=list)
    essay_themes: list[str] = Field(default_factory=list)
    required_materials: list[str] = Field(default_factory=list)
    estimated_effort: OpportunityEstimatedEffort
    red_flags: list[str] = Field(default_factory=list)
    opportunity_cluster: str


class FitAnalysis(BaseModel):
    eligible: bool | None = None
    hard_filter_failures: list[str] = Field(default_factory=list)
    fit_signals: list[str] = Field(default_factory=list)
    fit_gaps: list[str] = Field(default_factory=list)
    semantic_fit_score: float
    narrative_alignment_score: float
    reasoning: str


class Positioning(BaseModel):
    best_angle: str
    why_this_angle: str
    evidence_to_use: list[str] = Field(default_factory=list)
    things_to_avoid: list[str] = Field(default_factory=list)
    missing_story_piece: str


class DraftField(BaseModel):
    field: str
    value: str
    confidence: float


class Draft(BaseModel):
    autofilled_fields: list[DraftField] = Field(default_factory=list)
    draft_answer: str
    draft_outline: list[str] = Field(default_factory=list)
    user_edit_required: list[str] = Field(default_factory=list)


class ParseProfileRequest(BaseModel):
    resume_text: str
    form_data: dict[str, Any] | None = None
    source_type: str | None = None
    source_label: str | None = None


class ParseProfileResponse(BaseModel):
    student_profile: StudentProfile


class ExtractOpportunityRequest(BaseModel):
    raw_text: str
    source_type: str | None = None
    source_label: str | None = None


class ExtractOpportunityResponse(BaseModel):
    opportunity: OpportunityIntelligence


class AnalyzeFitRequest(BaseModel):
    student_profile: StudentProfile
    opportunity: OpportunityIntelligence


class AnalyzeFitResponse(BaseModel):
    fit_analysis: FitAnalysis


class GeneratePositioningRequest(BaseModel):
    student_profile: StudentProfile
    opportunity: OpportunityIntelligence
    fit_analysis: FitAnalysis


class GeneratePositioningResponse(BaseModel):
    positioning: Positioning


class GenerateDraftRequest(BaseModel):
    student_profile: StudentProfile
    opportunity: OpportunityIntelligence
    positioning: Positioning
    essay_prompt: str | None = None
    application_prompt: str | None = None


class GenerateDraftResponse(BaseModel):
    draft: Draft

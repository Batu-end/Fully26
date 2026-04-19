from __future__ import annotations

from ai_ocean_opportunity_schemas import (
    Draft,
    FitAnalysis,
    OpportunityIntelligence,
    Positioning,
    StudentProfile,
)


def parse_profile(profile_text: str) -> StudentProfile:
    """Parse raw profile text into a lightweight student profile model.

    TODO: Replace placeholder parsing with an LLM-backed extraction flow that
    normalizes student interests, skills, and target roles.
    """

    summary = profile_text.strip() or "Profile parsing placeholder."
    return StudentProfile(
        summary=summary,
        interests=["ocean", "sustainability"],
        skills=["research"],
        target_roles=["strategy"],
    )


def extract_opportunity(opportunity_text: str) -> OpportunityIntelligence:
    """Extract structured opportunity intelligence from a job or program brief.

    TODO: Replace placeholder extraction with AI-assisted opportunity parsing
    and ranking signals for the strategist workflow.
    """

    summary = opportunity_text.strip() or "Opportunity extraction placeholder."
    return OpportunityIntelligence(
        title="Placeholder Ocean Opportunity",
        organization="Placeholder Organization",
        summary=summary,
        themes=["marine innovation", "climate"],
    )


def analyze_fit(
    profile: StudentProfile, opportunity: OpportunityIntelligence
) -> FitAnalysis:
    """Compare a student profile to an opportunity and summarize fit.

    TODO: Add model-backed reasoning that highlights strengths, gaps, and
    confidence signals using the parsed profile and opportunity context.
    """

    return FitAnalysis(
        overall_fit="placeholder",
        strengths=[
            "Student profile and opportunity are available for future analysis."
        ],
        gaps=["Detailed fit scoring is not implemented yet."],
        notes=(
            f"Prepared to compare '{profile.summary or 'student profile'}' with "
            f"'{opportunity.title or 'opportunity'}'."
        ),
    )


def generate_positioning(
    profile: StudentProfile,
    opportunity: OpportunityIntelligence,
    analysis: FitAnalysis | None = None,
) -> Positioning:
    """Generate positioning guidance for how the student should present fit.

    TODO: Add tailored AI-generated positioning language, value propositions,
    and talking points grounded in the fit analysis.
    """

    return Positioning(
        headline="Positioning placeholder",
        angle=(
            f"Connect {profile.summary or 'the student profile'} to "
            f"{opportunity.title or 'the opportunity'}."
        ),
        talking_points=[
            "Highlight relevant motivation.",
            "Reference aligned skills or coursework.",
            "Tie experience to ocean opportunity goals.",
        ],
    )


def generate_draft(
    profile: StudentProfile,
    opportunity: OpportunityIntelligence,
    positioning: Positioning | None = None,
    draft_format: str = "message",
) -> Draft:
    """Generate a first-pass draft for applications or outreach.

    TODO: Replace placeholder drafting with model-generated content that adapts
    tone and structure for the requested draft format.
    """

    angle = positioning.angle if positioning else "a future strategy angle"
    return Draft(
        format=draft_format,
        subject=f"Interest in {opportunity.title or 'ocean opportunity'}",
        body=(
            "This is a placeholder draft for the AI Ocean Opportunity Strategist. "
            f"It will eventually tailor outreach using {angle}."
        ),
    )

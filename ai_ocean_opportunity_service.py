from __future__ import annotations

from ai_ocean_opportunity_schemas import (
    Draft,
    DraftField,
    FitAnalysis,
    OpportunityEstimatedEffort,
    OpportunityIntelligence,
    OpportunityRequirement,
    Positioning,
    StudentEvidence,
    StudentProfile,
)


def parse_profile(
    resume_text: str,
    form_data: dict | None = None,
    source_type: str | None = None,
    source_label: str | None = None,
) -> StudentProfile:
    """Parse raw profile text into the canonical student profile contract.

    TODO: Replace placeholder parsing with an LLM-backed extraction flow that
    normalizes student evidence, story themes, and career goals into the
    canonical StudentProfile schema.
    """

    profile_summary = resume_text.strip() or "Profile parsing placeholder."
    metadata_bits = [value for value in [source_type, source_label] if value]
    if form_data:
        metadata_bits.append("form-data captured")

    return StudentProfile(
        name="Placeholder Student",
        school="Placeholder University",
        major="Undeclared Ocean Opportunity Interest",
        gpa=None,
        student_type="undergraduate",
        graduation_year="TBD",
        activities=["Ocean club participation"],
        work_experience=["Research support placeholder"],
        leadership_signals=["Initiative shown in exploratory profile intake"],
        awards=[],
        skills=["research"],
        interests=["ocean", "sustainability"],
        financial_need_flag=False,
        identity_flags_opt_in=[],
        core_story_themes=[
            "Mission-driven interest in ocean opportunity pathways",
            profile_summary,
        ],
        evidence_bank=[
            StudentEvidence(
                label="Initial profile intake",
                detail=(
                    profile_summary
                    if not metadata_bits
                    else f"{profile_summary} ({', '.join(metadata_bits)})"
                ),
                source_type="self-report",
            )
        ],
        career_goals=["strategy"],
    )


def extract_opportunity(
    raw_text: str,
    source_type: str | None = None,
    source_label: str | None = None,
) -> OpportunityIntelligence:
    """Extract structured opportunity intelligence from raw opportunity text.

    TODO: Replace placeholder extraction with AI-assisted opportunity parsing
    and ranking signals for the strategist workflow.
    """

    summary = raw_text.strip() or "Opportunity extraction placeholder."
    source_note = ", ".join(value for value in [source_type, source_label] if value)
    return OpportunityIntelligence(
        title="Placeholder Ocean Opportunity",
        provider="Placeholder Organization",
        opportunity_type="fellowship",
        amount_or_stipend="TBD",
        deadline="TBD",
        location="Remote / TBD",
        raw_theme=summary,
        hard_requirements=[
            OpportunityRequirement(
                requirement="Full eligibility parsing not implemented yet.",
                category="other",
                strictness="unclear",
                notes=source_note or "Derived from placeholder opportunity intake.",
            )
        ],
        soft_preferences=["Interest in marine innovation", "Climate curiosity"],
        essay_themes=["Mission alignment", "Ocean impact potential"],
        required_materials=["Resume"],
        estimated_effort=OpportunityEstimatedEffort(
            time_hours_low=1.0,
            time_hours_high=3.0,
            writing_load="short-response",
            effort_level="medium",
        ),
        red_flags=[],
        opportunity_cluster="ocean-opportunity-placeholder",
    )


def analyze_fit(
    student_profile: StudentProfile, opportunity: OpportunityIntelligence
) -> FitAnalysis:
    """Compare a student profile to an opportunity with canonical fit fields.

    TODO: Add model-backed reasoning that highlights strengths, gaps, and
    confidence signals using the parsed profile and opportunity context.
    """

    return FitAnalysis(
        eligible=None,
        hard_filter_failures=[],
        fit_signals=[
            "Student profile and opportunity are available for future analysis."
        ],
        fit_gaps=["Detailed fit scoring is not implemented yet."],
        semantic_fit_score=0.0,
        narrative_alignment_score=0.0,
        reasoning=(
            f"Prepared to compare '{student_profile.name or 'student profile'}' with "
            f"'{opportunity.title or 'opportunity'}'."
        ),
    )


def generate_positioning(
    student_profile: StudentProfile,
    opportunity: OpportunityIntelligence,
    fit_analysis: FitAnalysis,
) -> Positioning:
    """Generate positioning guidance for how the student should present fit.

    TODO: Add tailored AI-generated positioning language, value propositions,
    and talking points grounded in the fit analysis.
    """

    return Positioning(
        best_angle="Mission-aligned ocean opportunity candidate",
        why_this_angle=(
            f"Connect {student_profile.name or 'the student'} to "
            f"{opportunity.title or 'the opportunity'} using the available "
            f"fit context: {fit_analysis.reasoning}"
        ),
        evidence_to_use=[
            "Highlight relevant motivation.",
            "Reference aligned skills or coursework.",
            "Tie experience to ocean opportunity goals.",
        ],
        things_to_avoid=[
            "Claiming eligibility before hard requirements are validated.",
            "Overstating domain experience not present in the profile.",
        ],
        missing_story_piece="A concrete proof point with measurable impact.",
    )


def generate_draft(
    student_profile: StudentProfile,
    opportunity: OpportunityIntelligence,
    positioning: Positioning,
    essay_prompt: str | None = None,
    application_prompt: str | None = None,
) -> Draft:
    """Generate a first-pass draft for applications or outreach.

    TODO: Replace placeholder drafting with model-generated content that adapts
    tone and structure for the essay or application prompt.
    """

    prompt_focus = essay_prompt or application_prompt or "the requested application"
    return Draft(
        autofilled_fields=[
            DraftField(
                field="opportunity_title",
                value=opportunity.title,
                confidence=0.95,
            ),
            DraftField(
                field="best_angle",
                value=positioning.best_angle,
                confidence=0.75,
            ),
        ],
        draft_answer=(
            "This is a placeholder draft for the AI Ocean Opportunity Strategist. "
            f"It will eventually tailor content for {student_profile.name} using "
            f"{positioning.best_angle} and {prompt_focus}."
        ),
        draft_outline=[
            f"Open with motivation for {opportunity.title}.",
            "Connect relevant student evidence to the opportunity.",
            "Close with forward-looking contribution and fit.",
        ],
        user_edit_required=[
            "Validate factual claims against the student's real evidence.",
            "Tailor tone and specificity to the exact application prompt.",
        ],
    )

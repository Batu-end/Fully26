from __future__ import annotations

import re

from ai_ocean_opportunity_openai import (
    OceanOpportunityOpenAIError,
    call_openai_json,
)
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
    """Extract structured opportunity intelligence from raw opportunity text."""

    cleaned_text = raw_text.strip()

    try:
        return call_openai_json(
            system_prompt=_build_extract_opportunity_system_prompt(),
            user_prompt=_build_extract_opportunity_user_prompt(
                raw_text=cleaned_text,
                source_type=source_type,
                source_label=source_label,
            ),
            output_model=OpportunityIntelligence,
        )
    except OceanOpportunityOpenAIError:
        return _build_opportunity_fallback(
            raw_text=cleaned_text,
            source_type=source_type,
            source_label=source_label,
        )
    except Exception:
        return _build_opportunity_fallback(
            raw_text=cleaned_text,
            source_type=source_type,
            source_label=source_label,
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


def _build_extract_opportunity_system_prompt() -> str:
    return (
        "You extract structured opportunity intelligence for an AI Ocean "
        "Opportunity Strategist. Return only data that fits the provided JSON "
        "schema. Prioritize ocean, marine science, climate, conservation, ocean "
        "engineering, blue economy, and deep-sea relevance when interpreting the "
        "opportunity. Be conservative: if a detail is missing, use 'TBD' for "
        "short string fields or an empty list where appropriate.\n\n"
        "Classify opportunity_type as one of: scholarship, internship, "
        "fellowship, research, lab, grant, field, other.\n"
        "Fill hard_requirements with explicit requirements from the text, using "
        "required/preferred/unclear strictness.\n"
        "Fill soft_preferences with inferred but non-mandatory preferences.\n"
        "Fill essay_themes and required_materials only when reasonably supported.\n"
        "Set estimated_effort conservatively based on application burden.\n"
        "Set red_flags only for genuine concerns such as unclear eligibility, "
        "tight deadlines, vague compensation, suspicious wording, or missing key "
        "details.\n"
        "Set opportunity_cluster to a short ocean-relevant cluster label such as "
        "marine-research, blue-economy, climate-policy, conservation-fieldwork, "
        "ocean-engineering, or general-ocean."
    )


def _build_extract_opportunity_user_prompt(
    *,
    raw_text: str,
    source_type: str | None,
    source_label: str | None,
) -> str:
    source_lines = []
    if source_type:
        source_lines.append(f"Source type: {source_type}")
    if source_label:
        source_lines.append(f"Source label: {source_label}")

    if not raw_text:
        raw_text = "No opportunity text was provided."

    prompt_sections = [
        "Extract a canonical OpportunityIntelligence object from the opportunity text below.",
    ]
    if source_lines:
        prompt_sections.extend(source_lines)
    prompt_sections.extend(["Opportunity text:", raw_text])
    return "\n\n".join(prompt_sections)


def _build_opportunity_fallback(
    *,
    raw_text: str,
    source_type: str | None,
    source_label: str | None,
) -> OpportunityIntelligence:
    text = raw_text.strip()
    fallback_title = _derive_opportunity_title(text, source_label)
    fallback_type = _infer_opportunity_type(text)
    fallback_cluster = _infer_opportunity_cluster(text)
    fallback_requirements = _extract_requirements(text)
    fallback_materials = _extract_required_materials(text)
    fallback_preferences = _extract_soft_preferences(text)
    fallback_essay_themes = _extract_essay_themes(text)
    fallback_red_flags = _extract_red_flags(text)
    fallback_theme = _derive_raw_theme(text)

    if source_type and source_type.lower() in {"scholarship", "internship", "fellowship"}:
        fallback_type = source_type.lower()

    return OpportunityIntelligence(
        title=fallback_title,
        provider=_derive_provider(text),
        opportunity_type=fallback_type,
        amount_or_stipend=_extract_amount_or_stipend(text),
        deadline=_extract_deadline(text),
        location=_extract_location(text),
        raw_theme=fallback_theme,
        hard_requirements=fallback_requirements,
        soft_preferences=fallback_preferences,
        essay_themes=fallback_essay_themes,
        required_materials=fallback_materials,
        estimated_effort=_estimate_opportunity_effort(text),
        red_flags=fallback_red_flags,
        opportunity_cluster=fallback_cluster,
    )


def _derive_opportunity_title(raw_text: str, source_label: str | None) -> str:
    if source_label:
        return source_label.strip()

    for line in raw_text.splitlines():
        cleaned_line = line.strip(" -:\t")
        if len(cleaned_line) >= 6:
            return cleaned_line[:120]

    return "Ocean Opportunity"


def _derive_provider(raw_text: str) -> str:
    provider_patterns = [
        r"(?:hosted by|offered by|provided by|administered by|run by)\s+([A-Z][^\n,.]{2,80})",
        r"(?:organization|provider|company|institution)\s*:\s*([^\n]{2,80})",
    ]
    for pattern in provider_patterns:
        match = re.search(pattern, raw_text, flags=re.IGNORECASE)
        if match:
            return match.group(1).strip(" .,:;-")
    return "TBD"


def _infer_opportunity_type(raw_text: str) -> str:
    lowered = raw_text.lower()
    type_keywords = [
        ("scholarship", "scholarship"),
        ("internship", "internship"),
        ("fellowship", "fellowship"),
        ("research", "research"),
        ("laboratory", "lab"),
        ("lab", "lab"),
        ("grant", "grant"),
        ("fieldwork", "field"),
        ("field program", "field"),
        ("expedition", "field"),
    ]
    for keyword, opportunity_type in type_keywords:
        if keyword in lowered:
            return opportunity_type
    return "other"


def _extract_amount_or_stipend(raw_text: str) -> str:
    amount_match = re.search(
        r"(\$\s?\d[\d,]*(?:\.\d+)?(?:\s*(?:per\s+\w+|/hour|/week|/month|/year))?)",
        raw_text,
        flags=re.IGNORECASE,
    )
    if amount_match:
        return amount_match.group(1).strip()

    stipend_match = re.search(
        r"((?:stipend|award|funding|salary)\s*[:\-]?\s*[^\n.]{1,80})",
        raw_text,
        flags=re.IGNORECASE,
    )
    if stipend_match:
        return stipend_match.group(1).strip(" .")

    return "TBD"


def _extract_deadline(raw_text: str) -> str:
    date_patterns = [
        r"(?:deadline|apply by|applications due|due date|due)\s*[:\-]?\s*([^\n.]{3,60})",
        r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\.?\s+\d{1,2},?\s+\d{4}\b",
        r"\b\d{1,2}/\d{1,2}/\d{2,4}\b",
        r"\b\d{4}-\d{2}-\d{2}\b",
    ]
    for pattern in date_patterns:
        match = re.search(pattern, raw_text, flags=re.IGNORECASE)
        if not match:
            continue
        if match.lastindex:
            return match.group(1).strip(" .")
        return match.group(0).strip(" .")
    return "TBD"


def _extract_location(raw_text: str) -> str:
    location_patterns = [
        r"(?:location|based in|located in|site)\s*[:\-]?\s*([^\n.]{2,80})",
        r"\b(remote|hybrid|on-site|onsite)\b",
    ]
    for pattern in location_patterns:
        match = re.search(pattern, raw_text, flags=re.IGNORECASE)
        if match:
            if match.lastindex:
                return match.group(1).strip(" .")
            return match.group(0).strip(" .").title()
    return "TBD"


def _derive_raw_theme(raw_text: str) -> str:
    lowered = raw_text.lower()
    theme_keywords = [
        ("deep-sea", "Deep-sea exploration and ocean discovery"),
        ("marine", "Marine science and ocean systems"),
        ("ocean engineering", "Ocean engineering and applied marine technology"),
        ("conservation", "Ocean conservation and ecosystem protection"),
        ("climate", "Climate and coastal resilience"),
        ("blue economy", "Blue economy and ocean innovation"),
        ("policy", "Ocean policy and governance"),
    ]
    for keyword, theme in theme_keywords:
        if keyword in lowered:
            return theme
    if raw_text:
        return raw_text[:180]
    return "General ocean opportunity"


def _extract_requirements(raw_text: str) -> list[OpportunityRequirement]:
    requirement_lines = []
    for line in raw_text.splitlines():
        cleaned_line = line.strip()
        if not cleaned_line:
            continue
        if re.search(
            r"\b(must|required|eligib|minimum|need to|applicants should|applicants must)\b",
            cleaned_line,
            flags=re.IGNORECASE,
        ):
            requirement_lines.append(cleaned_line[:160])

    requirements: list[OpportunityRequirement] = []
    for line in requirement_lines[:5]:
        lowered = line.lower()
        category = "other"
        if any(token in lowered for token in ["gpa", "student", "enrolled", "degree", "major"]):
            category = "academic"
        elif any(token in lowered for token in ["citizen", "visa", "resident", "nationality"]):
            category = "citizenship"
        elif any(token in lowered for token in ["location", "remote", "relocate", "based in"]):
            category = "location"
        elif any(token in lowered for token in ["experience", "internship", "research", "fieldwork"]):
            category = "experience"
        elif any(token in lowered for token in ["skill", "python", "coding", "writing", "analysis"]):
            category = "skills"
        elif any(token in lowered for token in ["resume", "cv", "essay", "transcript", "recommendation"]):
            category = "materials"
        elif any(token in lowered for token in ["deadline", "by ", "before "]):
            category = "timing"

        strictness = "required"
        if re.search(r"\b(preferred|plus|nice to have|ideal)\b", lowered):
            strictness = "preferred"
        elif re.search(r"\b(unclear|may|can|could)\b", lowered):
            strictness = "unclear"

        requirements.append(
            OpportunityRequirement(
                requirement=line,
                category=category,
                strictness=strictness,
                notes="Fallback extraction from raw opportunity text.",
            )
        )

    if requirements:
        return requirements

    return [
        OpportunityRequirement(
            requirement="Eligibility and application requirements require manual review.",
            category="other",
            strictness="unclear",
            notes="Fallback used because structured model extraction was unavailable or invalid.",
        )
    ]


def _extract_soft_preferences(raw_text: str) -> list[str]:
    preferences = []
    lines = raw_text.splitlines()
    for line in lines:
        cleaned_line = line.strip()
        if re.search(
            r"\b(preferred|ideal candidate|nice to have|bonus|strongly encouraged)\b",
            cleaned_line,
            flags=re.IGNORECASE,
        ):
            preferences.append(cleaned_line[:140])

    lowered = raw_text.lower()
    if "marine" in lowered or "ocean" in lowered:
        preferences.append("Interest in ocean or marine issues.")
    if "climate" in lowered:
        preferences.append("Interest in climate or coastal resilience.")

    return _dedupe_keep_order(preferences)[:6]


def _extract_essay_themes(raw_text: str) -> list[str]:
    themes = []
    lowered = raw_text.lower()
    if "essay" in lowered or "statement" in lowered:
        if "leadership" in lowered:
            themes.append("Leadership")
        if "impact" in lowered:
            themes.append("Impact")
        if "motivation" in lowered or "why" in lowered:
            themes.append("Motivation")
        if "community" in lowered:
            themes.append("Community")
        if "research" in lowered:
            themes.append("Research interest")

    return themes[:5]


def _extract_required_materials(raw_text: str) -> list[str]:
    materials = []
    material_keywords = [
        ("resume", "Resume"),
        ("cv", "CV"),
        ("cover letter", "Cover letter"),
        ("transcript", "Transcript"),
        ("recommendation", "Recommendation letter"),
        ("essay", "Essay"),
        ("statement", "Personal statement"),
        ("references", "References"),
        ("portfolio", "Portfolio"),
    ]
    lowered = raw_text.lower()
    for keyword, label in material_keywords:
        if keyword in lowered:
            materials.append(label)
    return _dedupe_keep_order(materials)


def _estimate_opportunity_effort(raw_text: str) -> OpportunityEstimatedEffort:
    lowered = raw_text.lower()
    materials = _extract_required_materials(raw_text)
    has_multiple_essays = "essay" in lowered and (
        "500" in lowered or "750" in lowered or "statement" in lowered
    )

    if has_multiple_essays or len(materials) >= 4:
        return OpportunityEstimatedEffort(
            time_hours_low=6.0,
            time_hours_high=12.0,
            writing_load="essay-heavy",
            effort_level="high",
        )

    if "essay" in lowered or "statement" in lowered or len(materials) >= 2:
        return OpportunityEstimatedEffort(
            time_hours_low=3.0,
            time_hours_high=6.0,
            writing_load="short-response",
            effort_level="medium",
        )

    return OpportunityEstimatedEffort(
        time_hours_low=1.0,
        time_hours_high=3.0,
        writing_load="none",
        effort_level="low",
    )


def _extract_red_flags(raw_text: str) -> list[str]:
    red_flags = []
    lowered = raw_text.lower()
    if "rolling basis" in lowered:
        red_flags.append("Rolling review may favor earlier applications.")
    if "unpaid" in lowered:
        red_flags.append("Opportunity appears unpaid.")
    if "deadline" not in lowered and "apply by" not in lowered:
        red_flags.append("Deadline is not clearly stated.")
    if "eligib" not in lowered and "requirements" not in lowered:
        red_flags.append("Eligibility criteria are not clearly stated.")
    return red_flags[:4]


def _infer_opportunity_cluster(raw_text: str) -> str:
    lowered = raw_text.lower()
    cluster_keywords = [
        ("deep-sea", "deep-sea"),
        ("ocean engineering", "ocean-engineering"),
        ("marine research", "marine-research"),
        ("research", "marine-research"),
        ("conservation", "conservation-fieldwork"),
        ("field", "conservation-fieldwork"),
        ("policy", "climate-policy"),
        ("climate", "climate-policy"),
        ("blue economy", "blue-economy"),
        ("startup", "blue-economy"),
    ]
    for keyword, cluster in cluster_keywords:
        if keyword in lowered:
            return cluster
    return "general-ocean"


def _dedupe_keep_order(items: list[str]) -> list[str]:
    seen = set()
    deduped = []
    for item in items:
        normalized = item.strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        deduped.append(normalized)
    return deduped

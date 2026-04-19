from __future__ import annotations

import json
import re
from typing import Any

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
    resume_text: str | None = None,
    form_data: dict[str, Any] | None = None,
    source_type: str | None = None,
    source_label: str | None = None,
) -> StudentProfile:
    """Parse resume text and optional form data into a canonical profile."""

    cleaned_resume = (resume_text or "").strip()
    normalized_form_data = form_data or {}

    try:
        extracted_profile = call_openai_json(
            system_prompt=_build_parse_profile_system_prompt(),
            user_prompt=_build_parse_profile_user_prompt(
                resume_text=cleaned_resume,
                form_data=normalized_form_data,
                source_type=source_type,
                source_label=source_label,
            ),
            output_model=StudentProfile,
        )
    except OceanOpportunityOpenAIError:
        extracted_profile = _build_profile_fallback(
            resume_text=cleaned_resume,
            form_data=normalized_form_data,
            source_type=source_type,
            source_label=source_label,
        )
    except Exception:
        extracted_profile = _build_profile_fallback(
            resume_text=cleaned_resume,
            form_data=normalized_form_data,
            source_type=source_type,
            source_label=source_label,
        )

    return _merge_profile_with_form_data(
        profile=extracted_profile,
        resume_text=cleaned_resume,
        form_data=normalized_form_data,
        source_type=source_type,
        source_label=source_label,
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


def _build_parse_profile_system_prompt() -> str:
    return (
        "You extract a canonical StudentProfile for an AI Ocean Opportunity "
        "Strategist. Merge resume text with any structured form data, and return "
        "only data that fits the provided JSON schema.\n\n"
        "Prefer explicit form data when it conflicts with inferred resume values. "
        "Be conservative and do not invent credentials. If a scalar value is not "
        "present, use 'TBD' for name, school, major, student_type, or "
        "graduation_year as needed, and null for gpa if unavailable.\n"
        "Normalize activities, work_experience, leadership_signals, awards, "
        "skills, interests, core_story_themes, evidence_bank, and career_goals "
        "into concise lists.\n"
        "Infer useful themes such as leadership, research, community service, "
        "resilience, academic merit, and environmental or ocean interest when "
        "supported by the input.\n"
        "Only include identity_flags_opt_in when explicitly supplied by the user. "
        "Set financial_need_flag to true only when clearly stated in form data or "
        "source text."
    )


def _build_parse_profile_user_prompt(
    *,
    resume_text: str,
    form_data: dict[str, Any],
    source_type: str | None,
    source_label: str | None,
) -> str:
    payload = {
        "source_type": source_type,
        "source_label": source_label,
        "resume_text": resume_text or None,
        "form_data": form_data or None,
    }
    return (
        "Extract a canonical StudentProfile object from the following combined "
        "student input.\n\n"
        f"{json.dumps(payload, indent=2, ensure_ascii=True)}"
    )


def _build_profile_fallback(
    *,
    resume_text: str,
    form_data: dict[str, Any],
    source_type: str | None,
    source_label: str | None,
) -> StudentProfile:
    del source_type

    name = _coerce_str(form_data.get("name")) or _extract_name_from_resume(resume_text)
    school = _coerce_str(form_data.get("school")) or _extract_school_from_resume(
        resume_text
    )
    major = _coerce_str(form_data.get("major")) or _extract_major_from_resume(resume_text)
    gpa = _coerce_float(form_data.get("gpa"))
    if gpa is None:
        gpa = _extract_gpa_from_resume(resume_text)

    student_type = _coerce_str(form_data.get("student_type")) or _infer_student_type(
        resume_text
    )
    graduation_year = _coerce_str(
        form_data.get("graduation_year")
    ) or _extract_graduation_year(resume_text)

    activities = _merge_preferred_list(
        _coerce_list(form_data.get("activities")),
        _extract_activities(resume_text),
    )
    work_experience = _merge_preferred_list(
        _coerce_list(form_data.get("work_experience")),
        _extract_work_experience(resume_text),
    )
    leadership_signals = _merge_preferred_list(
        _coerce_list(form_data.get("leadership_signals")),
        _extract_leadership_signals(resume_text),
    )
    awards = _merge_preferred_list(
        _coerce_list(form_data.get("awards")),
        _extract_awards(resume_text),
    )
    skills = _merge_preferred_list(
        _coerce_list(form_data.get("skills")),
        _extract_skills(resume_text),
    )
    interests = _merge_preferred_list(
        _coerce_list(form_data.get("interests")),
        _extract_interests(resume_text),
    )
    identity_flags_opt_in = _coerce_list(form_data.get("identity_flags_opt_in"))
    career_goals = _merge_preferred_list(
        _coerce_list(form_data.get("career_goals")),
        _extract_career_goals(resume_text),
    )

    evidence_bank = _build_profile_evidence_bank(
        resume_text=resume_text,
        form_data=form_data,
        source_label=source_label,
        activities=activities,
        work_experience=work_experience,
        leadership_signals=leadership_signals,
        awards=awards,
    )

    core_story_themes = _merge_preferred_list(
        _coerce_list(form_data.get("core_story_themes")),
        _infer_profile_themes(
            resume_text=resume_text,
            activities=activities,
            work_experience=work_experience,
            leadership_signals=leadership_signals,
            awards=awards,
            interests=interests,
            gpa=gpa,
        ),
    )

    return StudentProfile(
        name=name or "TBD",
        school=school or "TBD",
        major=major or "TBD",
        gpa=gpa,
        student_type=student_type or "TBD",
        graduation_year=graduation_year or "TBD",
        activities=activities,
        work_experience=work_experience,
        leadership_signals=leadership_signals,
        awards=awards,
        skills=skills,
        interests=interests,
        financial_need_flag=_coerce_bool(form_data.get("financial_need_flag")) or False,
        identity_flags_opt_in=identity_flags_opt_in,
        core_story_themes=core_story_themes,
        evidence_bank=evidence_bank,
        career_goals=career_goals,
    )


def _merge_profile_with_form_data(
    *,
    profile: StudentProfile,
    resume_text: str,
    form_data: dict[str, Any],
    source_type: str | None,
    source_label: str | None,
) -> StudentProfile:
    data = _model_to_dict(profile)

    for scalar_key in ["name", "school", "major", "student_type", "graduation_year"]:
        explicit_value = _coerce_str(form_data.get(scalar_key))
        if explicit_value:
            data[scalar_key] = explicit_value

    explicit_gpa = _coerce_float(form_data.get("gpa"))
    if explicit_gpa is not None:
        data["gpa"] = explicit_gpa

    explicit_financial_need = _coerce_bool(form_data.get("financial_need_flag"))
    if explicit_financial_need is not None:
        data["financial_need_flag"] = explicit_financial_need

    for list_key in [
        "activities",
        "work_experience",
        "leadership_signals",
        "awards",
        "skills",
        "interests",
        "identity_flags_opt_in",
        "core_story_themes",
        "career_goals",
    ]:
        explicit_items = _coerce_list(form_data.get(list_key))
        if explicit_items:
            data[list_key] = _merge_preferred_list(explicit_items, data.get(list_key, []))
        else:
            data[list_key] = _dedupe_keep_order(data.get(list_key, []))

    merged_evidence = _merge_evidence_bank(
        _coerce_evidence_bank(data.get("evidence_bank")),
        _build_profile_evidence_bank(
            resume_text=resume_text,
            form_data=form_data,
            source_label=source_label,
            activities=data["activities"],
            work_experience=data["work_experience"],
            leadership_signals=data["leadership_signals"],
            awards=data["awards"],
        ),
    )
    data["evidence_bank"] = merged_evidence

    inferred_themes = _infer_profile_themes(
        resume_text=resume_text,
        activities=data["activities"],
        work_experience=data["work_experience"],
        leadership_signals=data["leadership_signals"],
        awards=data["awards"],
        interests=data["interests"],
        gpa=data.get("gpa"),
    )
    data["core_story_themes"] = _merge_preferred_list(
        data["core_story_themes"],
        inferred_themes,
    )

    if not data["name"]:
        data["name"] = "TBD"
    if not data["school"]:
        data["school"] = "TBD"
    if not data["major"]:
        data["major"] = "TBD"
    if not data["student_type"]:
        data["student_type"] = "TBD"
    if not data["graduation_year"]:
        data["graduation_year"] = "TBD"

    del source_type

    return StudentProfile(**data)


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


def _extract_name_from_resume(resume_text: str) -> str:
    for line in resume_text.splitlines():
        cleaned_line = line.strip()
        if not cleaned_line:
            continue
        if "@" in cleaned_line or re.search(r"\d", cleaned_line):
            continue
        if len(cleaned_line.split()) <= 4 and cleaned_line == cleaned_line.title():
            return cleaned_line
    return "TBD"


def _extract_school_from_resume(resume_text: str) -> str:
    patterns = [
        r"([A-Z][A-Za-z&.\- ]+(?:University|College|Institute|School))",
        r"(?:school|institution)\s*:\s*([^\n]{3,100})",
    ]
    for pattern in patterns:
        match = re.search(pattern, resume_text, flags=re.IGNORECASE)
        if match:
            return match.group(1).strip(" .,:;-")
    return "TBD"


def _extract_major_from_resume(resume_text: str) -> str:
    patterns = [
        r"(?:major|majoring in)\s*(?:in)?\s*[:\-]?\s*([^\n,;]{3,80})",
        r"(?:B\.?S\.?|B\.?A\.?|M\.?S\.?|M\.?A\.?)\s+(?:in)\s+([^\n,;]{3,80})",
    ]
    for pattern in patterns:
        match = re.search(pattern, resume_text, flags=re.IGNORECASE)
        if match:
            return match.group(1).strip(" .,:;-")
    return "TBD"


def _extract_gpa_from_resume(resume_text: str) -> float | None:
    match = re.search(r"\bGPA\s*[:\-]?\s*(\d\.\d{1,2})\b", resume_text, flags=re.IGNORECASE)
    if not match:
        return None
    try:
        return float(match.group(1))
    except ValueError:
        return None


def _infer_student_type(resume_text: str) -> str:
    lowered = resume_text.lower()
    if "phd" in lowered or "doctoral" in lowered:
        return "doctoral"
    if "master" in lowered or "graduate student" in lowered or "m.s." in lowered:
        return "graduate"
    if "high school" in lowered:
        return "high-school"
    if "undergraduate" in lowered or "b.s." in lowered or "b.a." in lowered:
        return "undergraduate"
    return "TBD"


def _extract_graduation_year(resume_text: str) -> str:
    patterns = [
        r"(?:graduation|expected graduation|class of)\s*[:\-]?\s*(\d{4})",
        r"(?:expected|grad(?:uation)?)\s*(?:date|year)?\s*[:\-]?\s*(\d{4})",
    ]
    for pattern in patterns:
        match = re.search(pattern, resume_text, flags=re.IGNORECASE)
        if match:
            return match.group(1)
    years = re.findall(r"\b20\d{2}\b", resume_text)
    return years[0] if years else "TBD"


def _extract_activities(resume_text: str) -> list[str]:
    keywords = ["club", "society", "volunteer", "association", "team", "organization"]
    return _extract_lines_by_keywords(resume_text, keywords, limit=6)


def _extract_work_experience(resume_text: str) -> list[str]:
    keywords = ["intern", "assistant", "research", "coordinator", "analyst", "engineer"]
    return _extract_lines_by_keywords(resume_text, keywords, limit=6)


def _extract_leadership_signals(resume_text: str) -> list[str]:
    keywords = ["president", "founder", "captain", "lead", "chair", "organizer", "director"]
    return _extract_lines_by_keywords(resume_text, keywords, limit=5)


def _extract_awards(resume_text: str) -> list[str]:
    keywords = ["award", "honor", "scholarship", "dean", "fellow", "prize"]
    return _extract_lines_by_keywords(resume_text, keywords, limit=5)


def _extract_skills(resume_text: str) -> list[str]:
    lowered = resume_text.lower()
    skill_map = [
        ("python", "Python"),
        ("data analysis", "Data analysis"),
        ("gis", "GIS"),
        ("research", "Research"),
        ("writing", "Writing"),
        ("communication", "Communication"),
        ("excel", "Excel"),
        ("matlab", "MATLAB"),
        ("r ", "R"),
        ("policy", "Policy analysis"),
    ]
    found = [label for keyword, label in skill_map if keyword in lowered]
    return found[:8]


def _extract_interests(resume_text: str) -> list[str]:
    lowered = resume_text.lower()
    interest_map = [
        ("ocean", "Ocean"),
        ("marine", "Marine science"),
        ("climate", "Climate resilience"),
        ("conservation", "Conservation"),
        ("sustainability", "Sustainability"),
        ("policy", "Policy"),
        ("engineering", "Ocean engineering"),
        ("research", "Research"),
    ]
    found = [label for keyword, label in interest_map if keyword in lowered]
    return found[:8]


def _extract_career_goals(resume_text: str) -> list[str]:
    goals = []
    patterns = [
        r"(?:interested in|seeking|aspiring to|goal is to)\s+([^\n.]{5,120})",
    ]
    for pattern in patterns:
        for match in re.finditer(pattern, resume_text, flags=re.IGNORECASE):
            goals.append(match.group(1).strip(" ."))
    return _dedupe_keep_order(goals)[:5]


def _build_profile_evidence_bank(
    *,
    resume_text: str,
    form_data: dict[str, Any],
    source_label: str | None,
    activities: list[str],
    work_experience: list[str],
    leadership_signals: list[str],
    awards: list[str],
) -> list[StudentEvidence]:
    evidence: list[StudentEvidence] = []

    explicit_evidence = _coerce_evidence_bank(form_data.get("evidence_bank"))
    evidence.extend(explicit_evidence)

    if resume_text:
        label = source_label or "Resume intake"
        evidence.append(
            StudentEvidence(
                label=label,
                detail=resume_text[:280],
                source_type="self-report",
            )
        )

    for activity in activities[:2]:
        evidence.append(
            StudentEvidence(label="Activity", detail=activity, source_type="activity")
        )
    for work_item in work_experience[:2]:
        evidence.append(
            StudentEvidence(label="Work experience", detail=work_item, source_type="work")
        )
    for leadership_item in leadership_signals[:2]:
        evidence.append(
            StudentEvidence(
                label="Leadership signal",
                detail=leadership_item,
                source_type="leadership",
            )
        )
    for award_item in awards[:2]:
        evidence.append(
            StudentEvidence(label="Award", detail=award_item, source_type="award")
        )

    return _merge_evidence_bank([], evidence)


def _infer_profile_themes(
    *,
    resume_text: str,
    activities: list[str],
    work_experience: list[str],
    leadership_signals: list[str],
    awards: list[str],
    interests: list[str],
    gpa: float | None,
) -> list[str]:
    themes = []
    lowered = resume_text.lower()

    if leadership_signals or any("president" in item.lower() or "lead" in item.lower() for item in activities):
        themes.append("Leadership")
    if "research" in lowered or any("research" in item.lower() for item in work_experience):
        themes.append("Research")
    if "volunteer" in lowered or "community" in lowered or any("volunteer" in item.lower() for item in activities):
        themes.append("Community service")
    if "resilience" in lowered or "overcame" in lowered or "first-generation" in lowered:
        themes.append("Resilience")
    if (gpa is not None and gpa >= 3.5) or any(
        "dean" in item.lower() or "honor" in item.lower() for item in awards
    ):
        themes.append("Academic merit")
    if any("ocean" in interest.lower() or "marine" in interest.lower() for interest in interests) or any(
        token in lowered for token in ["ocean", "marine", "climate", "conservation", "coastal"]
    ):
        themes.append("Environmental or ocean interest")

    return themes


def _merge_preferred_list(explicit_items: list[str], inferred_items: list[str]) -> list[str]:
    return _dedupe_keep_order(explicit_items + inferred_items)


def _coerce_str(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        cleaned = value.strip()
        return cleaned or None
    cleaned = str(value).strip()
    return cleaned or None


def _coerce_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _coerce_bool(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "yes", "1"}:
            return True
        if lowered in {"false", "no", "0"}:
            return False
    if isinstance(value, (int, float)):
        return bool(value)
    return None


def _coerce_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        parts = re.split(r"[\n,;]+", value)
        return _dedupe_keep_order([part.strip() for part in parts if part.strip()])
    if isinstance(value, list):
        return _dedupe_keep_order(
            [_coerce_str(item) for item in value if _coerce_str(item)]
        )
    return []


def _coerce_evidence_bank(value: Any) -> list[StudentEvidence]:
    evidence: list[StudentEvidence] = []
    if not value:
        return evidence

    items = value if isinstance(value, list) else [value]
    for item in items:
        if isinstance(item, StudentEvidence):
            evidence.append(item)
            continue
        if isinstance(item, dict):
            try:
                evidence.append(StudentEvidence(**item))
                continue
            except Exception:
                pass
        item_text = _coerce_str(item)
        if item_text:
            evidence.append(
                StudentEvidence(
                    label="Profile evidence",
                    detail=item_text,
                    source_type="self-report",
                )
            )
    return evidence


def _merge_evidence_bank(
    primary: list[StudentEvidence], secondary: list[StudentEvidence]
) -> list[StudentEvidence]:
    seen = set()
    merged: list[StudentEvidence] = []
    for item in primary + secondary:
        key = (item.label.strip().lower(), item.detail.strip().lower(), item.source_type)
        if key in seen:
            continue
        seen.add(key)
        merged.append(item)
    return merged[:10]


def _extract_lines_by_keywords(
    resume_text: str, keywords: list[str], limit: int
) -> list[str]:
    matches = []
    for line in resume_text.splitlines():
        cleaned_line = line.strip(" -\t")
        if not cleaned_line:
            continue
        lowered = cleaned_line.lower()
        if any(keyword in lowered for keyword in keywords):
            matches.append(cleaned_line[:140])
    return _dedupe_keep_order(matches)[:limit]


def _model_to_dict(model: Any) -> dict[str, Any]:
    if hasattr(model, "model_dump"):
        return model.model_dump()
    return model.dict()


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

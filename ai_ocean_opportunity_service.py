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
    """Compare a canonical student profile and opportunity for fit."""

    hard_filter_failures = _collect_hard_filter_failures(student_profile, opportunity)
    if hard_filter_failures:
        return FitAnalysis(
            eligible=False,
            hard_filter_failures=hard_filter_failures,
            fit_signals=[],
            fit_gaps=[],
            semantic_fit_score=0.0,
            narrative_alignment_score=0.0,
            reasoning=(
                f"'{student_profile.name}' does not clearly meet one or more hard "
                f"requirements for '{opportunity.title}'."
            ),
        )

    try:
        model_fit = call_openai_json(
            system_prompt=_build_fit_analysis_system_prompt(),
            user_prompt=_build_fit_analysis_user_prompt(student_profile, opportunity),
            output_model=FitAnalysis,
        )
        return FitAnalysis(
            eligible=True,
            hard_filter_failures=[],
            fit_signals=_dedupe_keep_order(model_fit.fit_signals)[:5],
            fit_gaps=_dedupe_keep_order(model_fit.fit_gaps)[:5],
            semantic_fit_score=max(0.0, min(1.0, model_fit.semantic_fit_score)),
            narrative_alignment_score=max(
                0.0, min(1.0, model_fit.narrative_alignment_score)
            ),
            reasoning=model_fit.reasoning,
        )
    except OceanOpportunityOpenAIError:
        return _build_fit_analysis_fallback(student_profile, opportunity)
    except Exception:
        return _build_fit_analysis_fallback(student_profile, opportunity)


def generate_positioning(
    student_profile: StudentProfile,
    opportunity: OpportunityIntelligence,
    fit_analysis: FitAnalysis,
) -> Positioning:
    """Generate strategic positioning guidance from canonical fit inputs."""

    if fit_analysis.eligible is False:
        return _build_ineligible_positioning(
            student_profile=student_profile,
            opportunity=opportunity,
            fit_analysis=fit_analysis,
        )

    try:
        model_positioning = call_openai_json(
            system_prompt=_build_positioning_system_prompt(),
            user_prompt=_build_positioning_user_prompt(
                student_profile, opportunity, fit_analysis
            ),
            output_model=Positioning,
        )
        return Positioning(
            best_angle=model_positioning.best_angle.strip(),
            why_this_angle=model_positioning.why_this_angle.strip(),
            evidence_to_use=_dedupe_keep_order(model_positioning.evidence_to_use)[:5],
            things_to_avoid=_dedupe_keep_order(model_positioning.things_to_avoid)[:5],
            missing_story_piece=model_positioning.missing_story_piece.strip(),
        )
    except OceanOpportunityOpenAIError:
        return _build_positioning_fallback(
            student_profile=student_profile,
            opportunity=opportunity,
            fit_analysis=fit_analysis,
        )
    except Exception:
        return _build_positioning_fallback(
            student_profile=student_profile,
            opportunity=opportunity,
            fit_analysis=fit_analysis,
        )


def generate_draft(
    student_profile: StudentProfile,
    opportunity: OpportunityIntelligence,
    positioning: Positioning,
    essay_prompt: str | None = None,
    application_prompt: str | None = None,
) -> Draft:
    """Generate an editable first draft grounded in canonical AI inputs."""

    selected_prompt = essay_prompt or application_prompt

    try:
        model_draft = call_openai_json(
            system_prompt=_build_draft_system_prompt(),
            user_prompt=_build_draft_user_prompt(
                student_profile=student_profile,
                opportunity=opportunity,
                positioning=positioning,
                essay_prompt=essay_prompt,
                application_prompt=application_prompt,
            ),
            output_model=Draft,
        )
        if not model_draft.draft_answer.strip():
            raise ValueError("Model draft answer was empty.")
        return Draft(
            autofilled_fields=_normalize_draft_fields(model_draft.autofilled_fields),
            draft_answer=model_draft.draft_answer.strip(),
            draft_outline=_dedupe_keep_order(model_draft.draft_outline)[:6],
            user_edit_required=_dedupe_keep_order(model_draft.user_edit_required)[:6],
        )
    except OceanOpportunityOpenAIError:
        return _build_draft_fallback(
            student_profile=student_profile,
            opportunity=opportunity,
            positioning=positioning,
            selected_prompt=selected_prompt,
        )
    except Exception:
        return _build_draft_fallback(
            student_profile=student_profile,
            opportunity=opportunity,
            positioning=positioning,
            selected_prompt=selected_prompt,
        )


def _build_fit_analysis_system_prompt() -> str:
    return (
        "You analyze fit between a canonical StudentProfile and canonical "
        "OpportunityIntelligence object for an AI Ocean Opportunity Strategist. "
        "Return only the canonical FitAnalysis schema.\n\n"
        "Do not re-check hard filters beyond the structured inputs provided; those "
        "are already handled in code. Focus only on fit_signals, fit_gaps, "
        "semantic_fit_score, narrative_alignment_score, and concise reasoning.\n"
        "Use scores from 0.0 to 1.0. Be conservative, grounded in the provided "
        "fields only, and do not predict selection odds or chances of winning."
    )


def _build_positioning_system_prompt() -> str:
    return (
        "You generate concise strategic positioning guidance for an AI Ocean "
        "Opportunity Strategist. Return only the canonical Positioning schema.\n\n"
        "Base the advice primarily on fit_analysis fields: eligible, "
        "hard_filter_failures, fit_signals, fit_gaps, semantic_fit_score, "
        "narrative_alignment_score, and reasoning.\n"
        "Use the student evidence bank, story themes, and opportunity themes to "
        "identify the strongest narrative angle.\n"
        "Keep best_angle and why_this_angle specific and concise. Recommend "
        "concrete evidence to use. Flag weak or generic approaches to avoid. If "
        "fit is limited, be honest and do not invent a strong narrative."
    )


def _build_draft_system_prompt() -> str:
    return (
        "You generate an editable first draft for an AI Ocean Opportunity "
        "Strategist. Return only the canonical Draft schema.\n\n"
        "Use only factual student evidence and the provided opportunity details. "
        "Do not fabricate experience, impact, or credentials. If the available "
        "evidence is thin, write a cautious incomplete draft with clear room for "
        "user editing instead of a polished false answer.\n"
        "Use positioning.best_angle, why_this_angle, evidence_to_use, "
        "things_to_avoid, and missing_story_piece as the narrative guide.\n"
        "If both essay_prompt and application_prompt are present, prefer "
        "essay_prompt.\n"
        "Keep the result grounded, specific, concise, and editable."
    )


def _build_draft_user_prompt(
    *,
    student_profile: StudentProfile,
    opportunity: OpportunityIntelligence,
    positioning: Positioning,
    essay_prompt: str | None,
    application_prompt: str | None,
) -> str:
    payload = {
        "student_profile": _model_to_dict(student_profile),
        "opportunity": _model_to_dict(opportunity),
        "positioning": _model_to_dict(positioning),
        "essay_prompt": essay_prompt,
        "application_prompt": application_prompt,
        "selected_prompt": essay_prompt or application_prompt,
    }
    return (
        "Generate a grounded editable first draft for this opportunity.\n\n"
        f"{json.dumps(payload, indent=2, ensure_ascii=True)}"
    )


def _build_positioning_user_prompt(
    student_profile: StudentProfile,
    opportunity: OpportunityIntelligence,
    fit_analysis: FitAnalysis,
) -> str:
    payload = {
        "student_profile": _model_to_dict(student_profile),
        "opportunity": _model_to_dict(opportunity),
        "fit_analysis": _model_to_dict(fit_analysis),
    }
    return (
        "Generate positioning guidance for this student and opportunity.\n\n"
        f"{json.dumps(payload, indent=2, ensure_ascii=True)}"
    )


def _build_fit_analysis_user_prompt(
    student_profile: StudentProfile, opportunity: OpportunityIntelligence
) -> str:
    payload = {
        "student_profile": _model_to_dict(student_profile),
        "opportunity": _model_to_dict(opportunity),
    }
    return (
        "Analyze fit between this canonical student profile and opportunity.\n\n"
        f"{json.dumps(payload, indent=2, ensure_ascii=True)}"
    )


def _collect_hard_filter_failures(
    student_profile: StudentProfile, opportunity: OpportunityIntelligence
) -> list[str]:
    failures: list[str] = []
    for requirement in opportunity.hard_requirements:
        if requirement.strictness != "required":
            continue
        failures.extend(_evaluate_required_requirement(student_profile, requirement))
    return _dedupe_keep_order(failures)


def _evaluate_required_requirement(
    student_profile: StudentProfile, requirement: OpportunityRequirement
) -> list[str]:
    text = " ".join(
        part for part in [requirement.requirement, requirement.notes] if part
    ).lower()

    checks = [
        _check_required_gpa(student_profile, text),
        _check_required_student_type(student_profile, text),
        _check_required_major(student_profile, text),
        _check_required_skills(student_profile, text),
        _check_required_experience(student_profile, text),
        _check_required_graduation_window(student_profile, text),
        _check_required_financial_need(student_profile, text),
    ]

    return [failure for failure in checks if failure]


def _check_required_gpa(student_profile: StudentProfile, requirement_text: str) -> str | None:
    if "gpa" not in requirement_text:
        return None

    match = re.search(
        r"gpa(?:\s*(?:of|>=|>|minimum|min\.?|at least))?\s*(\d\.\d{1,2})",
        requirement_text,
    )
    if not match:
        return None

    required_gpa = float(match.group(1))
    if student_profile.gpa is None:
        return f"GPA requirement of {required_gpa:.1f} is explicit, but the student's GPA is unknown."
    if student_profile.gpa < required_gpa:
        return f"Student GPA {student_profile.gpa:.2f} is below the required {required_gpa:.1f}."
    return None


def _check_required_student_type(
    student_profile: StudentProfile, requirement_text: str
) -> str | None:
    student_type = student_profile.student_type.lower()
    if any(token in requirement_text for token in ["undergraduate", "undergrad"]):
        if "undergraduate" not in student_type:
            return "Opportunity requires an undergraduate student."
    if any(token in requirement_text for token in ["graduate student", "master", "masters"]):
        if "graduate" not in student_type and "master" not in student_type:
            return "Opportunity requires a graduate-level student."
    if any(token in requirement_text for token in ["phd", "doctoral", "doctorate"]):
        if "doctoral" not in student_type and "phd" not in student_type:
            return "Opportunity requires a doctoral-level student."
    if "high school" in requirement_text and "high-school" not in student_type:
        return "Opportunity requires a high-school student."
    return None


def _check_required_major(
    student_profile: StudentProfile, requirement_text: str
) -> str | None:
    major = student_profile.major.lower()
    if major == "tbd":
        return None

    major_buckets = {
        "engineering": ["engineering", "mechanical", "electrical", "robotics"],
        "marine biology": ["marine biology", "biology", "ecology", "oceanography"],
        "computer science": ["computer science", "software", "data science"],
        "policy": ["policy", "political science", "public policy", "government"],
    }
    for label, keywords in major_buckets.items():
        if label in requirement_text:
            if not any(keyword in major for keyword in keywords):
                return f"Opportunity requires {label}-aligned study, which is not evident from the student's major."
    return None


def _check_required_skills(
    student_profile: StudentProfile, requirement_text: str
) -> str | None:
    required_skills = []
    skill_keywords = [
        "python",
        "gis",
        "matlab",
        "excel",
        "writing",
        "communication",
        "research",
        "analysis",
    ]
    for skill in skill_keywords:
        if skill in requirement_text:
            required_skills.append(skill)

    if not required_skills:
        return None

    student_skill_text = " ".join(student_profile.skills).lower()
    missing = [skill for skill in required_skills if skill not in student_skill_text]
    if missing:
        return f"Required skill(s) missing from the student's profile: {', '.join(missing)}."
    return None


def _check_required_experience(
    student_profile: StudentProfile, requirement_text: str
) -> str | None:
    experience_keywords = ["research experience", "fieldwork", "internship experience"]
    if not any(keyword in requirement_text for keyword in experience_keywords):
        return None

    combined_experience = " ".join(
        student_profile.work_experience + student_profile.activities + student_profile.leadership_signals
    ).lower()

    if "research experience" in requirement_text and "research" not in combined_experience:
        return "Opportunity explicitly requires research experience."
    if "fieldwork" in requirement_text and "field" not in combined_experience:
        return "Opportunity explicitly requires fieldwork experience."
    if "internship experience" in requirement_text and "intern" not in combined_experience:
        return "Opportunity explicitly requires internship experience."
    return None


def _check_required_graduation_window(
    student_profile: StudentProfile, requirement_text: str
) -> str | None:
    if student_profile.graduation_year == "TBD":
        return None

    years = re.findall(r"\b20\d{2}\b", requirement_text)
    if "graduat" not in requirement_text and not years:
        return None

    student_year = student_profile.graduation_year
    if len(years) >= 2:
        low_year, high_year = min(years), max(years)
        if not (low_year <= student_year <= high_year):
            return f"Graduation year {student_year} falls outside the required {low_year}-{high_year} window."
    elif len(years) == 1 and any(token in requirement_text for token in ["by", "before", "no later than"]):
        if student_year > years[0]:
            return f"Graduation year {student_year} is later than the required cutoff of {years[0]}."
    return None


def _check_required_financial_need(
    student_profile: StudentProfile, requirement_text: str
) -> str | None:
    if "financial need" not in requirement_text and "need-based" not in requirement_text:
        return None
    if not student_profile.financial_need_flag:
        return "Opportunity explicitly requires financial need, which is not indicated in the student's profile."
    return None


def _build_fit_analysis_fallback(
    student_profile: StudentProfile, opportunity: OpportunityIntelligence
) -> FitAnalysis:
    fit_signals = _derive_fit_signals(student_profile, opportunity)
    fit_gaps = _derive_fit_gaps(student_profile, opportunity)

    semantic_fit_score = 0.35
    if fit_signals:
        semantic_fit_score += min(0.35, 0.08 * len(fit_signals))
    if fit_gaps:
        semantic_fit_score -= min(0.25, 0.05 * len(fit_gaps))
    semantic_fit_score = max(0.0, min(1.0, round(semantic_fit_score, 2)))

    narrative_alignment_score = 0.3
    if any("Environmental or ocean interest" == theme for theme in student_profile.core_story_themes):
        narrative_alignment_score += 0.2
    if any(
        token in opportunity.raw_theme.lower()
        for token in ["ocean", "marine", "climate", "conservation", "coastal"]
    ):
        narrative_alignment_score += 0.15
    if student_profile.leadership_signals:
        narrative_alignment_score += 0.05
    narrative_alignment_score = max(0.0, min(1.0, round(narrative_alignment_score, 2)))

    return FitAnalysis(
        eligible=True,
        hard_filter_failures=[],
        fit_signals=fit_signals,
        fit_gaps=fit_gaps,
        semantic_fit_score=semantic_fit_score,
        narrative_alignment_score=narrative_alignment_score,
        reasoning=(
            f"Fallback fit analysis found {len(fit_signals)} supporting signals "
            f"and {len(fit_gaps)} notable gaps for '{student_profile.name}' "
            f"against '{opportunity.title}'."
        ),
    )


def _build_ineligible_positioning(
    *,
    student_profile: StudentProfile,
    opportunity: OpportunityIntelligence,
    fit_analysis: FitAnalysis,
) -> Positioning:
    return Positioning(
        best_angle="Address the eligibility limitation directly",
        why_this_angle=(
            f"{student_profile.name} appears ineligible for {opportunity.title} "
            f"based on the current hard requirements, so the safest approach is "
            "to verify eligibility before investing in a stronger narrative."
        ),
        evidence_to_use=_select_positioning_evidence(student_profile, opportunity)[:3],
        things_to_avoid=[
            "Do not imply eligibility when hard filters appear unmet.",
            "Do not overbuild a narrative before confirming the requirements.",
            *[
                failure for failure in fit_analysis.hard_filter_failures[:2]
            ],
        ][:5],
        missing_story_piece="Confirmed eligibility or an alternate qualifying pathway.",
    )


def _build_positioning_fallback(
    *,
    student_profile: StudentProfile,
    opportunity: OpportunityIntelligence,
    fit_analysis: FitAnalysis,
) -> Positioning:
    best_angle = _derive_best_angle(student_profile, opportunity, fit_analysis)
    evidence_to_use = _select_positioning_evidence(student_profile, opportunity)
    things_to_avoid = _derive_things_to_avoid(fit_analysis)
    missing_story_piece = _derive_missing_story_piece(student_profile, fit_analysis)

    return Positioning(
        best_angle=best_angle,
        why_this_angle=(
            f"This angle fits because {fit_analysis.reasoning.lower()} It also "
            f"matches the opportunity's {opportunity.opportunity_cluster} focus."
        ),
        evidence_to_use=evidence_to_use[:5],
        things_to_avoid=things_to_avoid[:5],
        missing_story_piece=missing_story_piece,
    )


def _build_draft_fallback(
    *,
    student_profile: StudentProfile,
    opportunity: OpportunityIntelligence,
    positioning: Positioning,
    selected_prompt: str | None,
) -> Draft:
    evidence_snippets = _select_draft_evidence_snippets(student_profile, positioning)
    cautious_mode = _should_use_cautious_draft_mode(student_profile, positioning)
    prompt_label = selected_prompt or f"response for {opportunity.title}"

    opening = (
        f"I am excited to apply for {opportunity.title} because "
        f"{positioning.best_angle.lower()}."
    )
    evidence_sentence = (
        f"From my experience, I can point to {evidence_snippets[0]}."
        if evidence_snippets
        else "My current profile shows interest in this opportunity, but it still needs a stronger concrete example."
    )
    connection_sentence = (
        f"These experiences connect to {opportunity.raw_theme.lower()} and to the values behind {opportunity.provider}."
        if opportunity.raw_theme and opportunity.provider != "TBD"
        else f"These experiences connect to the goals of {opportunity.title}."
    )

    if cautious_mode:
        draft_answer = " ".join(
            [
                opening,
                evidence_sentence,
                connection_sentence,
                f"I would need to add a clearer example showing {positioning.missing_story_piece.lower()} before treating this as a final {prompt_label}.",
            ]
        )
    else:
        extra_evidence = (
            f" I would also highlight {evidence_snippets[1]}."
            if len(evidence_snippets) > 1
            else ""
        )
        draft_answer = " ".join(
            [
                opening,
                evidence_sentence + extra_evidence,
                connection_sentence,
                f"This is the angle I would develop in response to {prompt_label}.",
            ]
        )

    draft_outline = [
        f"Open with motivation for {opportunity.title} and the angle '{positioning.best_angle}'.",
        "Use one verified experience or project as the main proof point.",
        f"Connect that evidence to {opportunity.raw_theme or 'the opportunity theme'}.",
        f"Close with forward-looking contribution while acknowledging {positioning.missing_story_piece.lower()}.",
    ]

    user_edit_required = [
        "Check every factual claim against the student profile and evidence bank.",
        f"Add a concrete example showing {positioning.missing_story_piece.lower()}.",
        "Tailor the tone and length to the exact prompt wording.",
    ]
    if selected_prompt:
        user_edit_required.append("Align the response directly to the selected essay/application prompt.")
    if positioning.things_to_avoid:
        user_edit_required.append(positioning.things_to_avoid[0])

    return Draft(
        autofilled_fields=_build_autofilled_fields(
            opportunity=opportunity,
            positioning=positioning,
            selected_prompt=selected_prompt,
            cautious_mode=cautious_mode,
        ),
        draft_answer=draft_answer.strip(),
        draft_outline=_dedupe_keep_order(draft_outline)[:6],
        user_edit_required=_dedupe_keep_order(user_edit_required)[:6],
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


def _derive_fit_signals(
    student_profile: StudentProfile, opportunity: OpportunityIntelligence
) -> list[str]:
    signals = []
    combined_profile_text = " ".join(
        student_profile.interests
        + student_profile.skills
        + student_profile.core_story_themes
        + student_profile.career_goals
    ).lower()
    opportunity_text = " ".join(
        [
            opportunity.raw_theme,
            opportunity.opportunity_cluster,
            " ".join(opportunity.soft_preferences),
            " ".join(opportunity.essay_themes),
        ]
    ).lower()

    if any(token in combined_profile_text for token in ["ocean", "marine", "conservation"]):
        signals.append("Student profile shows direct ocean or marine interest.")
    if any(token in combined_profile_text for token in ["climate", "sustainability", "policy"]):
        signals.append("Student profile connects to climate or sustainability themes.")
    if any(skill.lower() in opportunity_text for skill in student_profile.skills):
        signals.append("Student skills overlap with the opportunity language.")
    if student_profile.leadership_signals:
        signals.append("Student profile includes leadership evidence.")
    if any(token in opportunity_text for token in ["research", "lab"]) and any(
        "research" in item.lower() for item in student_profile.work_experience + student_profile.core_story_themes
    ):
        signals.append("Student profile shows research alignment.")
    community_evidence = (
        student_profile.activities
        + student_profile.work_experience
        + student_profile.core_story_themes
    )
    if any(token in opportunity_text for token in ["community", "conservation"]) and any(
        "community" in item.lower() or "volunteer" in item.lower()
        for item in community_evidence
    ):
        signals.append("Student profile includes community-oriented evidence.")

    return _dedupe_keep_order(signals)[:5]


def _derive_fit_gaps(
    student_profile: StudentProfile, opportunity: OpportunityIntelligence
) -> list[str]:
    gaps = []
    opportunity_text = " ".join(
        [
            opportunity.raw_theme,
            " ".join(requirement.requirement for requirement in opportunity.hard_requirements),
            " ".join(opportunity.soft_preferences),
        ]
    ).lower()
    combined_profile_text = " ".join(
        student_profile.skills
        + student_profile.interests
        + student_profile.work_experience
        + student_profile.activities
    ).lower()

    for keyword, gap_text in [
        ("research", "Opportunity emphasizes research, but research evidence is limited."),
        ("field", "Opportunity suggests field experience, which is not clearly reflected."),
        ("policy", "Opportunity emphasizes policy, but policy evidence is limited."),
        ("engineering", "Opportunity emphasizes engineering, but engineering evidence is limited."),
    ]:
        if keyword in opportunity_text and keyword not in combined_profile_text:
            gaps.append(gap_text)

    if opportunity.required_materials and not student_profile.evidence_bank:
        gaps.append("Student evidence is limited for supporting application materials.")

    return _dedupe_keep_order(gaps)[:5]


def _derive_best_angle(
    student_profile: StudentProfile,
    opportunity: OpportunityIntelligence,
    fit_analysis: FitAnalysis,
) -> str:
    combined_text = " ".join(
        student_profile.core_story_themes
        + student_profile.interests
        + student_profile.skills
        + fit_analysis.fit_signals
    ).lower()
    opportunity_text = " ".join(
        [
            opportunity.opportunity_cluster,
            opportunity.raw_theme,
            " ".join(opportunity.soft_preferences),
            " ".join(opportunity.essay_themes),
        ]
    ).lower()

    if "engineering" in opportunity_text and any(
        token in combined_text for token in ["engineering", "python", "gis", "matlab"]
    ):
        return "Applied ocean problem-solver with technical relevance"
    if any(token in opportunity_text for token in ["research", "lab"]) and any(
        token in combined_text for token in ["research", "marine", "science"]
    ):
        return "Mission-aligned marine research contributor"
    if any(token in opportunity_text for token in ["policy", "climate"]) and any(
        token in combined_text for token in ["policy", "climate", "sustainability"]
    ):
        return "Climate-focused ocean mission candidate"
    if any(token in opportunity_text for token in ["community", "conservation"]) and any(
        token in combined_text for token in ["leadership", "community", "conservation", "volunteer"]
    ):
        return "Community-minded ocean stewardship leader"
    return "Mission-aligned ocean opportunity candidate"


def _select_positioning_evidence(
    student_profile: StudentProfile, opportunity: OpportunityIntelligence
) -> list[str]:
    evidence_choices = []
    opportunity_text = " ".join(
        [
            opportunity.raw_theme,
            opportunity.opportunity_cluster,
            " ".join(opportunity.soft_preferences),
            " ".join(opportunity.essay_themes),
        ]
    ).lower()
    opportunity_tokens = {
        token
        for token in re.findall(r"[a-z][a-z\-]{3,}", opportunity_text)
        if token not in {"with", "from", "that", "this", "have", "will", "into"}
    }

    for evidence in student_profile.evidence_bank:
        detail = evidence.detail.strip()
        if not detail:
            continue
        detail_lower = detail.lower()
        if any(
            token in detail_lower
            for token in ["ocean", "marine", "climate", "coastal", "research", "lead", "volunteer"]
        ):
            evidence_choices.append(detail)
        elif any(token in detail_lower for token in opportunity_tokens):
            evidence_choices.append(detail)

    if not evidence_choices:
        evidence_choices.extend(student_profile.work_experience[:2])
        evidence_choices.extend(student_profile.activities[:2])
        evidence_choices.extend(student_profile.leadership_signals[:2])

    if not evidence_choices and student_profile.skills:
        evidence_choices.append(
            f"Relevant skills: {', '.join(student_profile.skills[:3])}."
        )

    if not evidence_choices:
        evidence_choices.append("Use the strongest verified experience from the student's profile.")

    return _dedupe_keep_order(evidence_choices)[:5]


def _derive_things_to_avoid(fit_analysis: FitAnalysis) -> list[str]:
    avoid = [
        "Do not rely on generic passion statements without evidence.",
        "Do not overclaim domain expertise that is not in the profile.",
    ]
    if fit_analysis.fit_gaps:
        avoid.append(f"Do not ignore the main gap: {fit_analysis.fit_gaps[0]}")
    if fit_analysis.semantic_fit_score < 0.45:
        avoid.append("Do not frame the fit as stronger than the current evidence supports.")
    return _dedupe_keep_order(avoid)


def _derive_missing_story_piece(
    student_profile: StudentProfile, fit_analysis: FitAnalysis
) -> str:
    if fit_analysis.fit_gaps:
        return fit_analysis.fit_gaps[0]
    if not student_profile.leadership_signals and "Leadership" in student_profile.core_story_themes:
        return "A concrete leadership example with measurable impact."
    if not student_profile.evidence_bank:
        return "A concrete proof point from coursework, work, or community involvement."
    if any("Environmental or ocean interest" == theme for theme in student_profile.core_story_themes):
        return "A quantified example showing impact in an ocean or climate context."
    return "A concise example with measurable impact that supports the core angle."


def _select_draft_evidence_snippets(
    student_profile: StudentProfile, positioning: Positioning
) -> list[str]:
    snippets = []
    positioning_text = " ".join(
        [positioning.best_angle, positioning.why_this_angle] + positioning.evidence_to_use
    ).lower()

    for evidence in student_profile.evidence_bank:
        detail = evidence.detail.strip()
        if not detail:
            continue
        detail_lower = detail.lower()
        if any(token in detail_lower for token in ["ocean", "marine", "climate", "research", "lead", "project"]):
            snippets.append(detail)
        elif any(token in detail_lower for token in re.findall(r"[a-z][a-z\-]{3,}", positioning_text)):
            snippets.append(detail)

    if not snippets:
        snippets.extend(positioning.evidence_to_use[:3])
    if not snippets:
        snippets.extend(student_profile.work_experience[:2])
        snippets.extend(student_profile.activities[:2])

    return _dedupe_keep_order(snippets)[:4]


def _should_use_cautious_draft_mode(
    student_profile: StudentProfile, positioning: Positioning
) -> bool:
    if "eligibility limitation" in positioning.best_angle.lower():
        return True
    if "confirm" in positioning.missing_story_piece.lower():
        return True
    if len(student_profile.evidence_bank) == 0 and not student_profile.work_experience:
        return True
    if any(
        phrase in positioning.missing_story_piece.lower()
        for phrase in ["concrete", "proof point", "measurable impact"]
    ) and len(student_profile.evidence_bank) < 2:
        return True
    return False


def _build_autofilled_fields(
    *,
    opportunity: OpportunityIntelligence,
    positioning: Positioning,
    selected_prompt: str | None,
    cautious_mode: bool,
) -> list[DraftField]:
    fields = [
        DraftField(field="opportunity_title", value=opportunity.title, confidence=0.98),
        DraftField(field="provider", value=opportunity.provider, confidence=0.92),
        DraftField(field="best_angle", value=positioning.best_angle, confidence=0.8),
    ]
    if selected_prompt:
        fields.append(
            DraftField(field="selected_prompt", value=selected_prompt, confidence=0.95)
        )
    fields.append(
        DraftField(
            field="draft_mode",
            value="cautious" if cautious_mode else "standard",
            confidence=0.9,
        )
    )
    return fields[:5]


def _normalize_draft_fields(fields: list[DraftField]) -> list[DraftField]:
    normalized = []
    for field in fields[:5]:
        if not field.field.strip() or not field.value.strip():
            continue
        normalized.append(
            DraftField(
                field=field.field.strip(),
                value=field.value.strip(),
                confidence=max(0.0, min(1.0, field.confidence)),
            )
        )
    return normalized or [
        DraftField(field="draft_mode", value="standard", confidence=0.5)
    ]


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

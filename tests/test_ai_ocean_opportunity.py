import json
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

import ai_ocean_opportunity_service as ai_service
from ai_ocean_opportunity_openai import OceanOpportunityOpenAIError
from ai_ocean_opportunity_schemas import (
    Draft,
    FitAnalysis,
    OpportunityIntelligence,
    Positioning,
    StudentProfile,
)
from auth import verify_supabase_token
from main import app


FIXTURES_DIR = Path(__file__).parent / "data" / "ai_ocean_opportunity"
client = TestClient(app)


def _override_user():
    return {"sub": "test-user", "role": "authenticated"}


def _load_text_fixture(filename: str) -> str:
    return (FIXTURES_DIR / filename).read_text(encoding="utf-8")


def _load_json_fixture(filename: str) -> dict:
    return json.loads((FIXTURES_DIR / filename).read_text(encoding="utf-8"))


def _model_to_dict(model):
    if hasattr(model, "model_dump"):
        return model.model_dump()
    return model.dict()


def _force_ai_fallback():
    return patch(
        "ai_ocean_opportunity_service.call_openai_json",
        side_effect=OceanOpportunityOpenAIError("forced test fallback"),
    )


def _sample_resume_text() -> str:
    return _load_text_fixture("sample_resume.txt")


def _sample_opportunity_text() -> str:
    return _load_text_fixture("sample_opportunity.txt")


def _fallback_profile() -> StudentProfile:
    with _force_ai_fallback():
        return ai_service.parse_profile(_sample_resume_text())


def _fallback_opportunity() -> OpportunityIntelligence:
    with _force_ai_fallback():
        return ai_service.extract_opportunity(_sample_opportunity_text())


def test_fixture_examples_are_schema_valid():
    expected_profile = StudentProfile(**_load_json_fixture("expected_profile.json"))
    expected_opportunity = OpportunityIntelligence(
        **_load_json_fixture("expected_opportunity.json")
    )

    assert expected_profile.name == "Avery Chen"
    assert expected_profile.evidence_bank
    assert expected_opportunity.title == "Blue Ocean Fellowship"
    assert expected_opportunity.hard_requirements


def test_parse_profile_fallback_returns_canonical_profile():
    expected_profile = StudentProfile(**_load_json_fixture("expected_profile.json"))

    with _force_ai_fallback():
        profile = ai_service.parse_profile(
            _sample_resume_text(),
            form_data={
                "financial_need_flag": True,
                "career_goals": ["Ocean policy research"],
            },
        )

    assert isinstance(profile, StudentProfile)
    assert profile.name == expected_profile.name
    assert profile.school == expected_profile.school
    assert profile.major == expected_profile.major
    assert profile.gpa == expected_profile.gpa
    assert profile.student_type == expected_profile.student_type
    assert profile.financial_need_flag is True
    assert profile.evidence_bank
    assert profile.core_story_themes
    assert profile.career_goals[0] == "Ocean policy research"


def test_extract_opportunity_fallback_returns_canonical_opportunity():
    expected_opportunity = OpportunityIntelligence(
        **_load_json_fixture("expected_opportunity.json")
    )

    with _force_ai_fallback():
        opportunity = ai_service.extract_opportunity(_sample_opportunity_text())

    assert isinstance(opportunity, OpportunityIntelligence)
    assert opportunity.title == expected_opportunity.title
    assert opportunity.provider == expected_opportunity.provider
    assert opportunity.opportunity_type == expected_opportunity.opportunity_type
    assert opportunity.deadline == expected_opportunity.deadline
    assert opportunity.location == expected_opportunity.location
    assert opportunity.required_materials
    assert opportunity.estimated_effort.effort_level in {"medium", "high"}


def test_analyze_fit_hard_filter_failure_is_honest_and_canonical():
    profile = _fallback_profile()
    opportunity = OpportunityIntelligence(**_load_json_fixture("expected_opportunity.json"))
    opportunity.hard_requirements[0].requirement = "Applicants must have GPA 3.9 or higher."
    opportunity.hard_requirements[0].strictness = "required"

    analysis = ai_service.analyze_fit(profile, opportunity)

    assert isinstance(analysis, FitAnalysis)
    assert analysis.eligible is False
    assert analysis.hard_filter_failures
    assert "gpa" in analysis.hard_filter_failures[0].lower()
    assert analysis.fit_signals == []
    assert analysis.fit_gaps == []
    assert analysis.semantic_fit_score == 0.0
    assert analysis.narrative_alignment_score == 0.0


def test_analyze_fit_fallback_returns_canonical_soft_analysis():
    profile = _fallback_profile()
    opportunity = _fallback_opportunity()

    with _force_ai_fallback():
        analysis = ai_service.analyze_fit(profile, opportunity)

    assert isinstance(analysis, FitAnalysis)
    assert analysis.eligible is True
    assert analysis.hard_filter_failures == []
    assert analysis.fit_signals
    assert 0.0 <= analysis.semantic_fit_score <= 1.0
    assert 0.0 <= analysis.narrative_alignment_score <= 1.0
    assert analysis.reasoning


def test_generate_positioning_fallback_returns_canonical_positioning():
    profile = _fallback_profile()
    opportunity = _fallback_opportunity()
    with _force_ai_fallback():
        analysis = ai_service.analyze_fit(profile, opportunity)
        positioning = ai_service.generate_positioning(profile, opportunity, analysis)

    assert isinstance(positioning, Positioning)
    assert positioning.best_angle
    assert positioning.why_this_angle
    assert positioning.evidence_to_use
    assert positioning.things_to_avoid
    assert positioning.missing_story_piece


def test_generate_positioning_is_honest_when_ineligible():
    profile = _fallback_profile()
    opportunity = _fallback_opportunity()
    ineligible_analysis = FitAnalysis(
        eligible=False,
        hard_filter_failures=["Student GPA 3.80 is below the required 3.9."],
        fit_signals=[],
        fit_gaps=[],
        semantic_fit_score=0.0,
        narrative_alignment_score=0.0,
        reasoning="Hard filter failure detected.",
    )

    positioning = ai_service.generate_positioning(
        profile, opportunity, ineligible_analysis
    )

    assert positioning.best_angle == "Address the eligibility limitation directly"
    assert "eligibility" in positioning.why_this_angle.lower()
    assert positioning.missing_story_piece


def test_generate_draft_fallback_returns_editable_canonical_draft():
    profile = _fallback_profile()
    opportunity = _fallback_opportunity()
    with _force_ai_fallback():
        analysis = ai_service.analyze_fit(profile, opportunity)
        positioning = ai_service.generate_positioning(profile, opportunity, analysis)
        draft = ai_service.generate_draft(
            profile,
            opportunity,
            positioning,
            essay_prompt="Describe why you want to contribute to ocean resilience research.",
            application_prompt="Fallback prompt should not be selected when essay prompt exists.",
        )

    assert isinstance(draft, Draft)
    assert draft.draft_answer
    assert "blue ocean fellowship" in draft.draft_answer.lower()
    assert draft.draft_outline
    assert draft.user_edit_required
    autofilled = {field.field: field.value for field in draft.autofilled_fields}
    assert autofilled["opportunity_title"] == "Blue Ocean Fellowship"
    assert autofilled["selected_prompt"].startswith("Describe why you want")


def test_parse_profile_route_returns_canonical_response_keys():
    app.dependency_overrides[verify_supabase_token] = _override_user
    try:
        with _force_ai_fallback():
            response = client.post(
                "/api/ai/parse-profile",
                json={
                    "resume_text": _sample_resume_text(),
                    "form_data": {"financial_need_flag": True},
                },
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    payload = response.json()
    assert "student_profile" in payload
    assert "profile" not in payload
    assert payload["student_profile"]["name"] == "Avery Chen"
    assert payload["student_profile"]["financial_need_flag"] is True


def test_extract_opportunity_route_returns_canonical_response_keys():
    app.dependency_overrides[verify_supabase_token] = _override_user
    try:
        with _force_ai_fallback():
            response = client.post(
                "/api/ai/extract-opportunity",
                json={"raw_text": _sample_opportunity_text()},
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    payload = response.json()
    assert list(payload.keys()) == ["opportunity"]
    assert payload["opportunity"]["title"] == "Blue Ocean Fellowship"


def test_analyze_fit_route_returns_canonical_response_keys():
    profile = _fallback_profile()
    opportunity = _fallback_opportunity()

    app.dependency_overrides[verify_supabase_token] = _override_user
    try:
        with _force_ai_fallback():
            response = client.post(
                "/api/ai/analyze-fit",
                json={
                    "student_profile": _model_to_dict(profile),
                    "opportunity": _model_to_dict(opportunity),
                },
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    payload = response.json()
    assert list(payload.keys()) == ["fit_analysis"]
    assert "analysis" not in payload
    assert "semantic_fit_score" in payload["fit_analysis"]


def test_generate_positioning_route_returns_canonical_response_keys():
    profile = _fallback_profile()
    opportunity = _fallback_opportunity()
    with _force_ai_fallback():
        analysis = ai_service.analyze_fit(profile, opportunity)

    app.dependency_overrides[verify_supabase_token] = _override_user
    try:
        with _force_ai_fallback():
            response = client.post(
                "/api/ai/generate-positioning",
                json={
                    "student_profile": _model_to_dict(profile),
                    "opportunity": _model_to_dict(opportunity),
                    "fit_analysis": _model_to_dict(analysis),
                },
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    payload = response.json()
    assert list(payload.keys()) == ["positioning"]
    assert "best_angle" in payload["positioning"]
    assert "missing_story_piece" in payload["positioning"]


def test_generate_draft_route_returns_canonical_response_keys():
    profile = _fallback_profile()
    opportunity = _fallback_opportunity()
    with _force_ai_fallback():
        analysis = ai_service.analyze_fit(profile, opportunity)
        positioning = ai_service.generate_positioning(profile, opportunity, analysis)

    app.dependency_overrides[verify_supabase_token] = _override_user
    try:
        with _force_ai_fallback():
            response = client.post(
                "/api/ai/generate-draft",
                json={
                    "student_profile": _model_to_dict(profile),
                    "opportunity": _model_to_dict(opportunity),
                    "positioning": _model_to_dict(positioning),
                    "essay_prompt": "Describe why you want to contribute to ocean resilience research.",
                    "application_prompt": "This should be ignored when essay_prompt exists.",
                },
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    payload = response.json()
    assert list(payload.keys()) == ["draft"]
    assert "draft_answer" in payload["draft"]
    assert payload["draft"]["autofilled_fields"]
    assert payload["draft"]["draft_outline"]
    assert payload["draft"]["user_edit_required"]

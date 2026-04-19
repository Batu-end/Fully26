from fastapi.testclient import TestClient

from ai_ocean_opportunity_service import (
    analyze_fit,
    extract_opportunity,
    generate_draft,
    generate_positioning,
    parse_profile,
)
from auth import verify_supabase_token
from main import app


client = TestClient(app)


def _override_user():
    return {"sub": "test-user", "role": "authenticated"}


def test_parse_profile_service_returns_placeholder_profile():
    profile = parse_profile("Marine biology student interested in policy.")

    assert profile.name == "Placeholder Student"
    assert profile.school == "Placeholder University"
    assert "ocean" in profile.interests
    assert "research" in profile.skills
    assert profile.evidence_bank[0].source_type == "self-report"


def test_extract_opportunity_service_returns_canonical_opportunity():
    opportunity = extract_opportunity(
        (
            "Blue Ocean Fellowship\n"
            "Hosted by Ocean Lab.\n"
            "Climate fellowship focused on coastal data and marine resilience.\n"
            "Applicants must be enrolled students and submit a resume and essay.\n"
            "Deadline: June 15, 2026.\n"
            "Location: Remote.\n"
            "Stipend: $5,000."
        )
    )

    assert opportunity.title == "Blue Ocean Fellowship"
    assert opportunity.opportunity_type == "fellowship"
    assert opportunity.amount_or_stipend == "$5,000"
    assert opportunity.deadline == "June 15, 2026"
    assert opportunity.location == "Remote"
    assert opportunity.required_materials == ["Resume", "Essay"]
    assert opportunity.estimated_effort.effort_level in {"medium", "high"}


def test_strategy_service_flow_returns_placeholder_models():
    profile = parse_profile("Student profile input")
    opportunity = extract_opportunity("Opportunity input")
    analysis = analyze_fit(profile, opportunity)
    positioning = generate_positioning(profile, opportunity, analysis)
    draft = generate_draft(
        profile,
        opportunity,
        positioning,
        application_prompt="Write a short application response.",
    )

    assert analysis.semantic_fit_score == 0.0
    assert positioning.best_angle == "Mission-aligned ocean opportunity candidate"
    assert "placeholder" in draft.draft_answer.lower()
    assert draft.autofilled_fields[0].field == "opportunity_title"


def test_parse_profile_route_returns_json_payload():
    app.dependency_overrides[verify_supabase_token] = _override_user
    try:
        response = client.post(
            "/api/ai/parse-profile",
            json={"resume_text": "Student exploring blue economy internships."},
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    payload = response.json()
    assert payload["student_profile"]["name"] == "Placeholder Student"
    assert (
        payload["student_profile"]["evidence_bank"][0]["detail"]
        == "Student exploring blue economy internships."
    )


def test_generate_draft_route_returns_placeholder_draft():
    app.dependency_overrides[verify_supabase_token] = _override_user
    try:
        response = client.post(
            "/api/ai/generate-draft",
            json={
                "student_profile": {
                    "name": "Student Example",
                    "school": "Ocean State University",
                    "major": "Marine Policy",
                    "gpa": 3.7,
                    "student_type": "undergraduate",
                    "graduation_year": "2027",
                    "activities": ["Ocean innovation club"],
                    "work_experience": ["Lab assistant"],
                    "leadership_signals": ["Club organizer"],
                    "awards": ["Research travel grant"],
                    "skills": ["research"],
                    "interests": ["ocean"],
                    "financial_need_flag": False,
                    "identity_flags_opt_in": [],
                    "core_story_themes": ["Blue economy curiosity"],
                    "evidence_bank": [
                        {
                            "label": "Club project",
                            "detail": "Led a coastal cleanup project.",
                            "source_type": "project",
                        }
                    ],
                    "career_goals": ["strategy"],
                },
                "opportunity": {
                    "title": "Blue Economy Fellowship",
                    "provider": "Ocean Lab",
                    "opportunity_type": "fellowship",
                    "amount_or_stipend": "$5,000 stipend",
                    "deadline": "2026-06-01",
                    "location": "Remote",
                    "raw_theme": "A program for founders and researchers.",
                    "hard_requirements": [
                        {
                            "requirement": "Current student status",
                            "category": "academic",
                            "strictness": "required",
                            "notes": "Must be enrolled.",
                        }
                    ],
                    "soft_preferences": ["Innovation interest"],
                    "essay_themes": ["Impact"],
                    "required_materials": ["Resume"],
                    "estimated_effort": {
                        "time_hours_low": 2.0,
                        "time_hours_high": 5.0,
                        "writing_load": "short-response",
                        "effort_level": "medium",
                    },
                    "red_flags": [],
                    "opportunity_cluster": "blue-economy",
                },
                "positioning": {
                    "best_angle": "Mission-aligned ocean builder",
                    "why_this_angle": "Connect mission to fellowship work.",
                    "evidence_to_use": ["Cleanup project leadership"],
                    "things_to_avoid": ["Generic claims"],
                    "missing_story_piece": "A quantified impact example",
                },
                "application_prompt": "Why are you a strong fit for this fellowship?",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    payload = response.json()
    assert "placeholder" in payload["draft"]["draft_answer"].lower()
    assert payload["draft"]["autofilled_fields"][0]["field"] == "opportunity_title"

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

    assert profile.summary == "Marine biology student interested in policy."
    assert "ocean" in profile.interests
    assert "research" in profile.skills


def test_extract_opportunity_service_returns_placeholder_opportunity():
    opportunity = extract_opportunity("Climate fellowship focused on coastal data.")

    assert opportunity.title == "Placeholder Ocean Opportunity"
    assert "climate" in opportunity.themes


def test_strategy_service_flow_returns_placeholder_models():
    profile = parse_profile("Student profile input")
    opportunity = extract_opportunity("Opportunity input")
    analysis = analyze_fit(profile, opportunity)
    positioning = generate_positioning(profile, opportunity, analysis)
    draft = generate_draft(profile, opportunity, positioning, "email")

    assert analysis.overall_fit == "placeholder"
    assert positioning.headline == "Positioning placeholder"
    assert draft.format == "email"
    assert "placeholder" in draft.body.lower()


def test_parse_profile_route_returns_json_payload():
    app.dependency_overrides[verify_supabase_token] = _override_user
    try:
        response = client.post(
            "/api/ai/parse-profile",
            json={"profile_text": "Student exploring blue economy internships."},
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "placeholder"
    assert payload["profile"]["summary"] == "Student exploring blue economy internships."


def test_generate_draft_route_returns_placeholder_draft():
    app.dependency_overrides[verify_supabase_token] = _override_user
    try:
        response = client.post(
            "/api/ai/generate-draft",
            json={
                "profile": {
                    "summary": "Student interested in ocean startups.",
                    "interests": ["ocean"],
                    "skills": ["research"],
                    "target_roles": ["strategy"],
                },
                "opportunity": {
                    "title": "Blue Economy Fellowship",
                    "organization": "Ocean Lab",
                    "summary": "A program for founders and researchers.",
                    "themes": ["innovation"],
                },
                "positioning": {
                    "headline": "Positioning placeholder",
                    "angle": "Connect mission to fellowship work.",
                    "talking_points": ["Mission fit"],
                },
                "draft_format": "email",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "placeholder"
    assert payload["draft"]["format"] == "email"
    assert "placeholder" in payload["draft"]["body"].lower()

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


def test_parse_profile_service_returns_canonical_profile():
    profile = parse_profile(
        (
            "Avery Chen\n"
            "Ocean State University\n"
            "B.S. in Marine Biology, GPA: 3.8, Expected Graduation 2027\n"
            "Research Assistant at Coastal Lab\n"
            "President, Marine Conservation Club\n"
            "Volunteer for community beach cleanup programs\n"
            "Skills: Python, data analysis, GIS\n"
            "Interested in ocean conservation and climate resilience."
        )
    )

    assert profile.name == "Avery Chen"
    assert profile.school == "Ocean State University"
    assert profile.major == "Marine Biology"
    assert profile.gpa == 3.8
    assert profile.graduation_year == "2027"
    assert "Python" in profile.skills
    assert "Ocean" in profile.interests
    assert "Leadership" in profile.core_story_themes
    assert profile.evidence_bank[0].source_type == "self-report"


def test_parse_profile_prefers_explicit_form_data():
    profile = parse_profile(
        "Jordan Lee\nCoastal University\nB.S. in Environmental Science",
        form_data={
            "name": "Jordan Rivera",
            "school": "Pacific Tech",
            "major": "Ocean Engineering",
            "financial_need_flag": True,
            "skills": ["Writing", "R"],
            "career_goals": ["Ocean policy"],
        },
    )

    assert profile.name == "Jordan Rivera"
    assert profile.school == "Pacific Tech"
    assert profile.major == "Ocean Engineering"
    assert profile.financial_need_flag is True
    assert profile.skills[:2] == ["Writing", "R"]
    assert profile.career_goals[0] == "Ocean policy"


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


def test_analyze_fit_returns_early_on_hard_filter_failure():
    profile = parse_profile(
        "Avery Chen\nOcean State University\nB.S. in Marine Biology, GPA: 3.2, Expected Graduation 2027"
    )
    opportunity = extract_opportunity(
        (
            "Blue Ocean Fellowship\n"
            "Applicants must have GPA 3.7 or higher.\n"
            "Applicants must be enrolled students.\n"
            "Deadline: June 15, 2026."
        )
    )
    analysis = analyze_fit(profile, opportunity)

    assert analysis.eligible is False
    assert analysis.hard_filter_failures
    assert "gpa" in analysis.hard_filter_failures[0].lower()
    assert analysis.semantic_fit_score == 0.0
    assert analysis.narrative_alignment_score == 0.0

    positioning = generate_positioning(profile, opportunity, analysis)
    assert positioning.best_angle == "Address the eligibility limitation directly"
    assert "eligibility" in positioning.why_this_angle.lower()
    assert positioning.missing_story_piece == "Confirmed eligibility or an alternate qualifying pathway."


def test_analyze_fit_returns_fallback_soft_analysis():
    profile = parse_profile(
        (
            "Avery Chen\n"
            "Ocean State University\n"
            "B.S. in Marine Biology, GPA: 3.8, Expected Graduation 2027\n"
            "Research Assistant at Coastal Lab\n"
            "President, Marine Conservation Club\n"
            "Volunteer for community beach cleanup programs\n"
            "Skills: Python, data analysis, GIS\n"
            "Interested in ocean conservation and climate resilience."
        )
    )
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
    analysis = analyze_fit(profile, opportunity)
    positioning = generate_positioning(profile, opportunity, analysis)
    draft = generate_draft(
        profile,
        opportunity,
        positioning,
        application_prompt="Write a short application response.",
    )

    assert analysis.eligible is True
    assert analysis.hard_filter_failures == []
    assert analysis.semantic_fit_score > 0.0
    assert analysis.narrative_alignment_score > 0.0
    assert analysis.fit_signals
    assert positioning.best_angle != "Mission-aligned ocean opportunity candidate" or positioning.evidence_to_use
    assert positioning.evidence_to_use
    assert positioning.things_to_avoid
    assert positioning.missing_story_piece
    assert draft.draft_answer
    assert draft.draft_outline
    assert draft.user_edit_required
    assert draft.autofilled_fields[0].field == "opportunity_title"


def test_parse_profile_route_returns_json_payload():
    app.dependency_overrides[verify_supabase_token] = _override_user
    try:
        response = client.post(
            "/api/ai/parse-profile",
            json={
                "resume_text": (
                    "Taylor Brooks\n"
                    "Marine Tech University\n"
                    "B.S. in Ocean Engineering, GPA: 3.6, Expected Graduation 2028\n"
                    "Robotics Club Lead\n"
                    "Interested in blue economy internships."
                ),
                "form_data": {"financial_need_flag": True},
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    payload = response.json()
    assert payload["student_profile"]["name"] == "Taylor Brooks"
    assert payload["student_profile"]["school"] == "Marine Tech University"
    assert payload["student_profile"]["financial_need_flag"] is True
    assert payload["student_profile"]["evidence_bank"][0]["source_type"] == "self-report"


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
    assert "blue economy fellowship" in payload["draft"]["draft_answer"].lower()
    assert payload["draft"]["autofilled_fields"][0]["field"] == "opportunity_title"
    assert payload["draft"]["draft_outline"]
    assert payload["draft"]["user_edit_required"]

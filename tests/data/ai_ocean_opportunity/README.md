# AI Ocean Opportunity Fixtures

This directory holds lightweight deterministic fixtures for local AI integration tests.

Files currently included:
- `sample_resume.txt`: realistic student profile input used by `parse_profile(...)`
- `sample_opportunity.txt`: ocean-related fellowship input used by `extract_opportunity(...)`
- `expected_profile.json`: schema-valid example of a canonical parsed `StudentProfile`
- `expected_opportunity.json`: schema-valid example of a canonical extracted `OpportunityIntelligence`

These fixtures are used to validate canonical shapes, fallback behavior, and route-level request/response handling without requiring live OpenAI API access.

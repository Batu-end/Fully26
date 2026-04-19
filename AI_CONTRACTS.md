# AI Contracts

## Overview

This repo's AI layer powers the Ocean Opportunity Strategist backend.
It is intentionally small and contract-driven:
- canonical schemas live in `ai_ocean_opportunity_schemas.py`
- service logic lives in `ai_ocean_opportunity_service.py`
- shared OpenAI JSON-call logic lives in `ai_ocean_opportunity_openai.py`
- HTTP integration lives in `main.py`

Teammates should integrate against these canonical contracts instead of inventing parallel shapes.

## Canonical Models

### `StudentProfile`
- Source of truth for parsed student context.
- Includes identity, academics, experiences, skills, interests, evidence, and career goals.

### `OpportunityIntelligence`
- Source of truth for parsed opportunity context.
- Includes title, provider, type, requirements, effort, themes, materials, and cluster.

### `FitAnalysis`
- Source of truth for eligibility-aware fit output.
- Includes:
  - `eligible`
  - `hard_filter_failures`
  - `fit_signals`
  - `fit_gaps`
  - `semantic_fit_score`
  - `narrative_alignment_score`
  - `reasoning`

### `Positioning`
- Source of truth for strategy guidance.
- Includes:
  - `best_angle`
  - `why_this_angle`
  - `evidence_to_use`
  - `things_to_avoid`
  - `missing_story_piece`

### `Draft`
- Source of truth for editable draft output.
- Includes:
  - `autofilled_fields`
  - `draft_answer`
  - `draft_outline`
  - `user_edit_required`

## AI Endpoints

### `POST /api/ai/parse-profile`
- Request: `ParseProfileRequest`
- Response: `ParseProfileResponse`

### `POST /api/ai/extract-opportunity`
- Request: `ExtractOpportunityRequest`
- Response: `ExtractOpportunityResponse`

### `POST /api/ai/analyze-fit`
- Request: `AnalyzeFitRequest`
- Response: `AnalyzeFitResponse`

### `POST /api/ai/generate-positioning`
- Request: `GeneratePositioningRequest`
- Response: `GeneratePositioningResponse`

### `POST /api/ai/generate-draft`
- Request: `GenerateDraftRequest`
- Response: `GenerateDraftResponse`

## Fallback Behavior

The AI layer is designed to remain usable when live model calls fail or the OpenAI SDK is unavailable.
- `parse_profile(...)` falls back to conservative profile parsing heuristics
- `extract_opportunity(...)` falls back to conservative opportunity parsing heuristics
- `analyze_fit(...)` always performs deterministic hard checks first, then falls back to conservative soft-fit analysis
- `generate_positioning(...)` falls back to deterministic positioning guidance
- `generate_draft(...)` falls back to a cautious editable first draft

Fallbacks must still return canonical models.

## Integration Note

The fields in the canonical models are the source of truth and should not be renamed casually.

High-risk fields for teammate integrations:
- `student_profile`
- `opportunity`
- `fit_analysis`
- `positioning`
- `draft`
- `hard_filter_failures`
- `semantic_fit_score`
- `narrative_alignment_score`
- `evidence_bank`
- `opportunity_cluster`
- `missing_story_piece`
- `autofilled_fields`

If compatibility changes are ever needed, they should be handled in adapters outside the canonical models rather than by mutating these field names.

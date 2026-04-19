from fastapi import FastAPI, Depends
from ai_ocean_opportunity_schemas import (
    AnalyzeFitRequest,
    AnalyzeFitResponse,
    ExtractOpportunityRequest,
    ExtractOpportunityResponse,
    GenerateDraftRequest,
    GenerateDraftResponse,
    GeneratePositioningRequest,
    GeneratePositioningResponse,
    ParseProfileRequest,
    ParseProfileResponse,
)
from ai_ocean_opportunity_service import (
    analyze_fit,
    extract_opportunity,
    generate_draft,
    generate_positioning,
    parse_profile,
)
from auth import verify_supabase_token

app = FastAPI()

# ---------------------------------------------------------
# UNPROTECTED ROUTE (Open to the public)
# Example: A landing page, or a public list of opportunities.
# ---------------------------------------------------------
@app.get("/")
def read_root():
    return {"status": "ok"}

# ---------------------------------------------------------
# PROTECTED ROUTE (Requires User Login)
# Example: Adding a profile, saving a favorite opportunity.
# ---------------------------------------------------------
@app.get("/api/protected")
def protected_route(user=Depends(verify_supabase_token)):
    return {"message": "success", "user": user}


@app.post("/api/ai/parse-profile", response_model=ParseProfileResponse)
def handle_parse_profile(
    request: ParseProfileRequest, user=Depends(verify_supabase_token)
):
    return ParseProfileResponse(
        student_profile=parse_profile(
            request.resume_text,
            request.form_data,
            request.source_type,
            request.source_label,
        )
    )


@app.post("/api/ai/extract-opportunity", response_model=ExtractOpportunityResponse)
def handle_extract_opportunity(
    request: ExtractOpportunityRequest, user=Depends(verify_supabase_token)
):
    return ExtractOpportunityResponse(
        opportunity=extract_opportunity(
            request.raw_text, request.source_type, request.source_label
        )
    )


@app.post("/api/ai/analyze-fit", response_model=AnalyzeFitResponse)
def handle_analyze_fit(request: AnalyzeFitRequest, user=Depends(verify_supabase_token)):
    return AnalyzeFitResponse(
        fit_analysis=analyze_fit(request.student_profile, request.opportunity)
    )


@app.post(
    "/api/ai/generate-positioning", response_model=GeneratePositioningResponse
)
def handle_generate_positioning(
    request: GeneratePositioningRequest, user=Depends(verify_supabase_token)
):
    return GeneratePositioningResponse(
        positioning=generate_positioning(
            request.student_profile, request.opportunity, request.fit_analysis
        )
    )


@app.post("/api/ai/generate-draft", response_model=GenerateDraftResponse)
def handle_generate_draft(
    request: GenerateDraftRequest, user=Depends(verify_supabase_token)
):
    return GenerateDraftResponse(
        draft=generate_draft(
            request.student_profile,
            request.opportunity,
            request.positioning,
            request.essay_prompt,
            request.application_prompt,
        )
    )

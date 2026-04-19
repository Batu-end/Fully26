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
    request: ParseProfileRequest, _user=Depends(verify_supabase_token)
):
    return ParseProfileResponse(
        student_profile=parse_profile(
            resume_text=request.resume_text,
            form_data=request.form_data,
            source_type=request.source_type,
            source_label=request.source_label,
        )
    )


@app.post("/api/ai/extract-opportunity", response_model=ExtractOpportunityResponse)
def handle_extract_opportunity(
    request: ExtractOpportunityRequest, _user=Depends(verify_supabase_token)
):
    return ExtractOpportunityResponse(
        opportunity=extract_opportunity(
            raw_text=request.raw_text,
            source_type=request.source_type,
            source_label=request.source_label,
        )
    )


@app.post("/api/ai/analyze-fit", response_model=AnalyzeFitResponse)
def handle_analyze_fit(
    request: AnalyzeFitRequest, _user=Depends(verify_supabase_token)
):
    return AnalyzeFitResponse(
        fit_analysis=analyze_fit(
            student_profile=request.student_profile,
            opportunity=request.opportunity,
        )
    )


@app.post(
    "/api/ai/generate-positioning", response_model=GeneratePositioningResponse
)
def handle_generate_positioning(
    request: GeneratePositioningRequest, _user=Depends(verify_supabase_token)
):
    return GeneratePositioningResponse(
        positioning=generate_positioning(
            student_profile=request.student_profile,
            opportunity=request.opportunity,
            fit_analysis=request.fit_analysis,
        )
    )


@app.post("/api/ai/generate-draft", response_model=GenerateDraftResponse)
def handle_generate_draft(
    request: GenerateDraftRequest, _user=Depends(verify_supabase_token)
):
    return GenerateDraftResponse(
        draft=generate_draft(
            student_profile=request.student_profile,
            opportunity=request.opportunity,
            positioning=request.positioning,
            essay_prompt=request.essay_prompt,
            application_prompt=request.application_prompt,
        )
    )

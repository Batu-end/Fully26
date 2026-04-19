# PURPOSE: Main FastAPI application entry point, defining all API endpoints.
import io

from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from pypdf import PdfReader

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
import schemas
from database import supabase

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


# ---------------------------------------------------------
# STUDENT ENDPOINTS
# ---------------------------------------------------------
@app.post("/api/students", response_model=schemas.StudentProfileResponse)
def create_student(
    student: schemas.StudentProfileCreate, payload=Depends(verify_supabase_token)
):
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=401, detail="Invalid token payload missing User ID"
        )

    try:
        response = (
            supabase.table("student_profiles")
            .insert(
                {
                    "id": user_id,
                    "name": student.name,
                    "education_level": student.education_level,
                    "major": student.major,
                    "interests": student.interests,
                    "resume_text": student.resume_text,
                }
            )
            .execute()
        )
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------
# OPPORTUNITY ENDPOINTS
# ---------------------------------------------------------
@app.get("/api/opportunities", response_model=list[schemas.OpportunityResponse])
def get_opportunities(payload=Depends(verify_supabase_token)):
    try:
        response = supabase.table("opportunities").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------
# TRACKER / MATCH ENDPOINTS
# ---------------------------------------------------------
@app.get(
    "/api/students/{student_id}/matches",
    response_model=list[schemas.OpportunityMatchResponse],
)
def get_student_matches(student_id: str, payload=Depends(verify_supabase_token)):
    if payload.get("sub") != student_id:
        raise HTTPException(
            status_code=403,
            detail="Forbidden: You can only view your own dashboard.",
        )

    try:
        response = (
            supabase.table("opportunity_matches")
            .select("*, opportunity:opportunities(*)")
            .eq("student_id", student_id)
            .execute()
        )
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------
# RESUME FILE UPLOAD ENDPOINT
# ---------------------------------------------------------
@app.post("/api/students/{id}/analyze-resume")
async def analyze_resume(
    id: str,
    file: UploadFile = File(...),
    payload: dict = Depends(verify_supabase_token),
):
    if payload.get("sub") != id:
        raise HTTPException(status_code=403, detail="Forbidden")

    try:
        file_bytes = await file.read()
        pdf = PdfReader(io.BytesIO(file_bytes))
        raw_text = ""
        for page in pdf.pages:
            raw_text += page.extract_text() + "\n"

        preview = raw_text[:500] if len(raw_text) > 500 else raw_text
        return {"message": "PDF parsed successfully!", "text_preview": preview}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse PDF: {str(e)}")


# ---------------------------------------------------------
# AI OCEAN OPPORTUNITY STRATEGIST ENDPOINTS
# ---------------------------------------------------------
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

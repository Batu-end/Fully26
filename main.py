# PURPOSE: Main FastAPI application entry point, defining all API endpoints.
import io
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
from auth import verify_supabase_token
import schemas
from database import supabase

app = FastAPI()

# ---------------------------------------------------------
# CORS CONFIGURATION (Crucial for Frontend/React connection)
# ---------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, change this to your exact React frontend URL!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
def create_student(student: schemas.StudentProfileCreate, payload=Depends(verify_supabase_token)):
    # 1. Grab the secure User ID directly from the decoded token payload
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload missing User ID")
        
    # 2. Insert the data into our Supabase Postgres table
    try:
        response = supabase.table("student_profiles").insert({
            "id": user_id,
            "name": student.name,
            "education_level": student.education_level,
            "major": student.major,
            "interests": student.interests,
            "resume_text": student.resume_text
        }).execute()
        
        # 3. Return the saved data back to the frontend (automatically checked against schemas.StudentProfileResponse)
        return response.data[0]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------------------------------------------------------
# OPPORTUNITY ENDPOINTS
# ---------------------------------------------------------
@app.get("/api/opportunities", response_model=list[schemas.OpportunityResponse])
def get_opportunities(payload=Depends(verify_supabase_token)):
    # 1. Fetch all available opportunities from the database using our service client
    try:
        # We can limit or paginate here later, but for MVP we fetch all.
        response = supabase.table("opportunities").select("*").execute()
        
        # 2. Return the pure JSON data. FastAPI will automatically check it against schemas.OpportunityResponse
        return response.data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------------------------------------------------------
# TRACKER / MATCH ENDPOINTS
# ---------------------------------------------------------
@app.get("/api/students/{student_id}/matches", response_model=list[schemas.OpportunityMatchResponse])
def get_student_matches(student_id: str, payload=Depends(verify_supabase_token)):
    # 1. Security Check: Ensure the user is only requesting THEIR OWN dashboard, not someone else's.
    if payload.get("sub") != student_id:
        raise HTTPException(status_code=403, detail="Forbidden: You can only view your own dashboard.")
        
    try:
        # 2. Fetch matches. We use Supabase relational querying (`*, opportunity:opportunities(*)`)
        # This grabs the match AND pulling in the full details of the linked Opportunity simultaneously!
        response = supabase.table("opportunity_matches") \
            .select("*, opportunity:opportunities(*)") \
            .eq("student_id", student_id) \
            .execute()
            
        return response.data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------------------------------------------------------
# RESUME FILE UPLOAD ENDPOINT
# ---------------------------------------------------------
@app.post("/api/students/{id}/analyze-resume")
async def analyze_resume(id: str, file: UploadFile = File(...), payload: dict = Depends(verify_supabase_token)):
    if payload.get("sub") != id:
        raise HTTPException(status_code=403, detail="Forbidden")
        
    try:
        # 1. Read the binary PDF data sent by the frontend
        file_bytes = await file.read()
        
        # 2. Use PyPDF to strip away the PDF styling and extract raw text
        pdf = PdfReader(io.BytesIO(file_bytes))
        raw_text = ""
        for page in pdf.pages:
            raw_text += page.extract_text() + "\n"
            
        # 3. (FUTURE STEP): You will hand `raw_text` over to the AI teammate here.
        # 4. (FUTURE STEP): The AI returns a JSON. You save it to Supabase.

        # For now, let's just prove the backend can parse it by returning a preview of the text!
        preview = raw_text[:500] if len(raw_text) > 500 else raw_text
        return {"message": "PDF parsed successfully!", "text_preview": preview}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse PDF: {str(e)}")

# PURPOSE: Main FastAPI application entry point, defining all API endpoints.
from fastapi import FastAPI, Depends, HTTPException
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

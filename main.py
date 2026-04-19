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

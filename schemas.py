# PURPOSE: Defines Pydantic models to strictly validate data coming into and leaving the API.
from pydantic import BaseModel
from typing import Optional, List

# ---------------------------------------------------------
# STUDENT PROFILE SCHEMAS
# ---------------------------------------------------------
class StudentProfileBase(BaseModel):
    # AI will fill these fields in
    name: Optional[str] = None
    education_level: Optional[str] = None
    major: Optional[str] = None
    interests: Optional[str] = None  # e.g., "conservation, robotics, marine biolgy"
    resume_text: Optional[str] = None  # Extracted text from the uploaded resume

class StudentProfileCreate(StudentProfileBase):
    pass

class StudentProfileResponse(StudentProfileBase):
    id: str  # Assuming UUID from Supabase auth
    class Config:
        from_attributes = True


# ---------------------------------------------------------
# OPPORTUNITY SCHEMAS
# ---------------------------------------------------------
class OpportunityBase(BaseModel):
    title: str
    type: str  # scholarship, internship, fellowship, lab
    description: str
    organization: str
    deadline: Optional[str] = None
    effort_level: int  # 1 to 5
    urgency_score: int  # 1 to 5
    ocean_tags: str

class OpportunityCreate(OpportunityBase):
    pass

class OpportunityResponse(OpportunityBase):
    id: int
    class Config:
        from_attributes = True


# ---------------------------------------------------------
# MATCH Tracker SCHEMAS
# ---------------------------------------------------------
class OpportunityMatchBase(BaseModel):
    student_id: str
    opportunity_id: int
    fit_score: float 
    fit_explanation: str # AI's explanation of why this opportunity is a good fit for the student
    suggested_angle: str # AI's suggested angle for the cover letter
    draft_starter_text: str # AI's suggested starter text for the cover letter
    status: str = "new"  # new, saved, applied

class OpportunityMatchCreate(OpportunityMatchBase):
    pass

class OpportunityMatchResponse(OpportunityMatchBase):
    id: int
    opportunity: Optional[OpportunityResponse] = None
    class Config:
        from_attributes = True

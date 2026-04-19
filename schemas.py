# PURPOSE: Defines Pydantic models to strictly validate data coming into and leaving the API.
from pydantic import BaseModel
from typing import Optional, List

# ---------------------------------------------------------
# STUDENT PROFILE SCHEMAS
# ---------------------------------------------------------
class StudentProfileBase(BaseModel):
    name: str
    education_level: str
    major: str
    interests: str  # e.g., "conservation, robotics, marine biolgy"
    resume_text: str  # Extracted text from the uploaded resume

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
    fit_explanation: str
    suggested_angle: str
    draft_starter_text: str
    status: str = "new"  # new, saved, applied

class OpportunityMatchCreate(OpportunityMatchBase):
    pass

class OpportunityMatchResponse(OpportunityMatchBase):
    id: int
    opportunity: Optional[OpportunityResponse] = None
    class Config:
        from_attributes = True

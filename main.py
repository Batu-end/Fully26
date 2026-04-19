# PURPOSE: Main FastAPI application entry point, defining all API endpoints.
from fastapi import FastAPI, Depends
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

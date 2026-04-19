from fastapi import FastAPI, Depends
from auth import verify_supabase_token

app = FastAPI(title="AI Ocean Opportunity Strategist - Phase 1 Auth Check")

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Ocean Opportunity Strategist API - Server is running!"}

@app.get("/api/protected-route")
def protected_route(payload: dict = Depends(verify_supabase_token)):
    # This route will only work if a valid Supabase JWT token is passed in the Authorization header.
    return {
        "message": "Auth successful. You accessed a protected route.",
        "user_payload": payload
    }

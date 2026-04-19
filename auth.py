# PURPOSE: Handles Supabase JWT token verification for securing API routes.
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from database import supabase

# Expects a HTTP bearer token in the Authorization header
security = HTTPBearer()

def verify_supabase_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Validates the JWT token by pinging the Supabase server directly."""
    try:
        # Instead of doing local math (which causes Algorithm Errors), 
        # we ask Supabase itself to verify the token for us! It is bulletproof.
        user_response = supabase.auth.get_user(credentials.credentials)
        
        if not user_response or not user_response.user:
            raise Exception("Invalid or expired session.")
            
        # Mock the payload structure we used previously
        return {"sub": user_response.user.id}
        
    except Exception as e:
        # Rejects the request if the token is invalid, expired, or missing
        print(f"DEBUG TOKEN ERROR: {e}")
        raise HTTPException(status_code=401, detail=f"Token validation failed: {str(e)}")

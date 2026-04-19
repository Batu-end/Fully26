# PURPOSE: Handles Supabase JWT token verification for securing API routes.
import os
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from dotenv import load_dotenv

load_dotenv()

# Expects a HTTP bearer token in the Authorization header
security = HTTPBearer()

def verify_supabase_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Validates the JWT token signed by Supabase."""
    try:
        # Decodes the token using the Supabase JWT secret and math algorithm
        return jwt.decode(
            credentials.credentials,
            os.getenv("SUPABASE_JWT_SECRET"),
            algorithms=["HS256"],
            options={"verify_aud": False}
        )
    except JWTError:
        # Rejects the request if the token is invalid, expired, or missing
        raise HTTPException(status_code=401, detail="Invalid token")

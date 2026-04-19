import os
from fastapi import Request, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from dotenv import load_dotenv

load_dotenv()

# We only need the public JWT secret from Supabase to verify tokens securely
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")

security = HTTPBearer()

def verify_supabase_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Validates the Supabase JWT token present in the Authorization header.
    Requires SUPABASE_JWT_SECRET to be configured in the environment.
    """
    if not SUPABASE_JWT_SECRET:
        # In a real environment, we'd crash on boot, but for the MVP skeleton we'll handle gracefully
        raise HTTPException(
            status_code=500,
            detail="Server configuration error: SUPABASE_JWT_SECRET is missing."
        )

    token = credentials.credentials
    try:
        # Supabase uses HS256 for their JWTs by default
        payload = jwt.decode(
            token,
            SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            options={"verify_aud": False} # Supabase aud usually "authenticated", but we bypass check for simplicity
        )
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials"
        )

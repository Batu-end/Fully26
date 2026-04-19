# PURPOSE: Handles Supabase JWT token verification for securing API routes.
import os
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from dotenv import load_dotenv

load_dotenv()

# Expects a HTTP bearer token in the Authorization header
security = HTTPBearer()
optional_security = HTTPBearer(auto_error=False)


def _is_demo_bypass_enabled() -> bool:
    return os.getenv("DEMO_BYPASS_AUTH", "").strip().lower() == "true"


def _decode_supabase_token(credentials: HTTPAuthorizationCredentials):
    return jwt.decode(
        credentials.credentials,
        os.getenv("SUPABASE_JWT_SECRET"),
        algorithms=["HS256"],
        options={"verify_aud": False}
    )

def verify_supabase_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Validates the JWT token signed by Supabase."""
    try:
        # Decodes the token using the Supabase JWT secret and math algorithm
        return _decode_supabase_token(credentials)
    except JWTError:
        # Rejects the request if the token is invalid, expired, or missing
        raise HTTPException(status_code=401, detail="Invalid token")


def verify_supabase_token_or_demo(
    credentials: HTTPAuthorizationCredentials | None = Security(optional_security),
):
    """Validates a Supabase token unless local demo bypass is explicitly enabled."""

    if _is_demo_bypass_enabled():
        if credentials is None:
            return {"sub": "demo-user", "auth_bypassed": True}

        try:
            payload = _decode_supabase_token(credentials)
            payload["auth_bypassed"] = False
            return payload
        except JWTError:
            return {"sub": "demo-user", "auth_bypassed": True}

    if credentials is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    try:
        payload = _decode_supabase_token(credentials)
        payload["auth_bypassed"] = False
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

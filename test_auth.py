from fastapi.testclient import TestClient
from main import app
from jose import jwt
import os

client = TestClient(app)

def test_auth():
    # 1. Test unauthenticated root route
    res = client.get("/")
    assert res.status_code == 200
    print("GET / passed.")

    # 2. Test protected route without token
    res = client.get("/api/protected-route")
    assert res.status_code == 401
    print("GET /api/protected-route without token properly rejected with 401.")

    # 3. Test protected route with an invalid token
    res = client.get("/api/protected-route", headers={"Authorization": "Bearer invalid_token"})
    assert res.status_code == 401
    print("GET /api/protected-route with invalid token properly rejected with 401.")

    # 4. Test protected route with a valid mock JWT signed with our dummy secret
    SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")
    valid_payload = {"sub": "user123", "role": "authenticated"}
    valid_token = jwt.encode(valid_payload, SUPABASE_JWT_SECRET, algorithm="HS256")
    
    res = client.get("/api/protected-route", headers={"Authorization": f"Bearer {valid_token}"})
    assert res.status_code == 200
    assert "Auth successful" in res.json()["message"]
    print("GET /api/protected-route with valid dummy token passed!")

if __name__ == "__main__":
    test_auth()

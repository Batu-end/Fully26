# PURPOSE: Creates and exposes the Supabase client connection for the backend.
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# We connect using the URL and the Service Role Key. 
# We use the Service Role Key in the backend because the Python backend is fully trusted,
# and it needs to bypass RLS (Row Level Security) when handling AI operations across all users.
# Note: DO NOT put the Service Role key in your React frontend! React only gets the ANON key.

url: str = os.getenv("SUPABASE_URL", "")
key: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", os.getenv("SUPABASE_ANON_KEY", ""))

if not url or not key:
    print("Warning: SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY is missing from environment variables.")

# Provide a safe fallback for local linting before .env is set
supabase: Client = create_client(
    supabase_url=url if url else "https://placeholder.supabase.co", 
    supabase_key=key if key else "placeholder"
)

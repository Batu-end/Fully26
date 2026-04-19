-- PURPOSE: SQL definitions to quickly generate the database tables in Supabase.
-- ---------------------------------------------------------
-- SCHEMAS FOR AI OCEAN OPPORTUNITY STRATEGIST
-- Copy and paste this directly into the Supabase SQL Editor
-- ---------------------------------------------------------

-- 1. Create the Opportunities Table
-- This stores the datasets of curated scholarships/internships.
CREATE TABLE public.opportunities (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    type TEXT NOT NULL,
    description TEXT NOT NULL,
    organization TEXT NOT NULL,
    deadline TEXT,
    effort_level INTEGER NOT NULL,
    urgency_score INTEGER NOT NULL,
    ocean_tags TEXT
);

-- 2. Create the Student Profiles Table
-- This stores the extracted skills from the user's resume.
-- The ID here is a UUID because it matches the Supabase Auth User ID perfectly.
CREATE TABLE public.student_profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    name TEXT,
    education_level TEXT,
    major TEXT,
    interests TEXT,
    resume_text TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. Create the Opportunity Matches Table
-- This table tracks the AI's personalized ranking and generated draft.
CREATE TABLE public.opportunity_matches (
    id SERIAL PRIMARY KEY,
    student_id UUID NOT NULL REFERENCES public.student_profiles(id) ON DELETE CASCADE,
    opportunity_id INTEGER NOT NULL REFERENCES public.opportunities(id) ON DELETE CASCADE,
    fit_score NUMERIC NOT NULL,
    fit_explanation TEXT NOT NULL,
    suggested_angle TEXT NOT NULL,
    draft_starter_text TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'new', -- e.g., 'new', 'saved', 'applied'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security (RLS) as a best practice.
-- Our Python backend uses the SERVICE_ROLE_KEY so it ignores these rules,
-- but this stops hackers from reading the database directly from the frontend React app!
ALTER TABLE public.opportunities ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.student_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.opportunity_matches ENABLE ROW LEVEL SECURITY;

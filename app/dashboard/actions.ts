import { createClient } from "@/lib/supabase/server";

export const getPagedOpportunities = async (page: number) => {
    const supabase = await createClient();
    const {
      data: { session },
    } = await supabase.auth.getSession();
    try {
        const backendUrl =
      process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';
    const res = await fetch(`${backendUrl}/api/opportunities?page=${page}`, {
      headers: {
        Authorization: `Bearer ${session.access_token}`,
      },
    });
    const data = await res.json();
    return data;
    } catch (error) {
        console.error('Error fetching paged opportunities:', error);
        return null;
    }
}
import { createClient } from "@/lib/supabase/server";
import { Suspense } from "react";


async function OpportunityDetail({ id }: { id: string }) {
    const supabase = await createClient();
    const { data: opportunity, error } = await supabase
        .from('opportunities')
        .select('*')
        .eq('id', id)
        .single();

    if (error) {
        console.error('Error fetching opportunity:', error);
        return <div>Error loading opportunity.</div>;
    }

    return (
        <div>
            <h1 className="text-2xl font-bold mb-4">{opportunity.title}</h1>
            <p>{opportunity.description}</p>
            {/* Add more details as needed */}
        </div>
    );
}

export default async function OpportunityDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
    const { id } = await params;
    return (
        <Suspense fallback={<div>Loading...</div>}>
            <OpportunityDetail id={id} />
        </Suspense>
    )
}
export const getPagedOpportunities = async (page: number) => {
    try {
        const backendUrl =
      process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';
    const res = await fetch(`${backendUrl}/api/opportunities?page=${page}`);
    const data = await res.json();
    return data;
    } catch (error) {
        console.error('Error fetching paged opportunities:', error);
        return null;
    }
}
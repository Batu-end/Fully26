import { DashboardGrid } from '@/components/dashboard-components';
import { LogoutButton } from '@/components/logout-button';
import { createClient } from '@/lib/supabase/server';
import Link from 'next/link';
import { redirect } from 'next/navigation';
import { getPagedOpportunities } from './actions';

export default async function DashboardPage({
  searchParams,
}: {
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
}) {
  const searchParamsResolved = await searchParams;
  const page = Number(searchParamsResolved.page) || 1;

  const supabase = await createClient();

  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user) {
    redirect('/auth/signin');
  }

  const { data: profileData } = await supabase
    .from('student_profiles')
    .select('*')
    .eq('id', user.id)
    .single();

  const pagedOpportunities = await getPagedOpportunities(page);
  console.log('Paged Opportunities:', pagedOpportunities);

  const dummyItems = [
    {
      id: '1',
      title: 'Opportunity 1',
      description: 'Description for opportunity 1',
    },
    {
      id: '2',
      title: 'Opportunity 2',
      description: 'Description for opportunity 2',
    },
    {
      id: '3',
      title: 'Opportunity 3',
      description: 'Description for opportunity 3',
    },
  ];

  return (
    <div className='min-h-screen w-full bg-gradient-to-b from-slate-950 via-blue-950 to-slate-900 text-white flex flex-col items-center'>
      {/* ambient glow */}
      <div className='absolute w-[500px] h-[500px] bg-blue-500/20 blur-[140px] rounded-full -z-10 top-40 left-1/2 -translate-x-1/2' />

      {/* NAV */}
      <nav className='w-full border-b border-white/10 backdrop-blur bg-white/5'>
        <div className='max-w-6xl mx-auto flex items-center justify-between p-5'>
          <div>
            <h1 className='text-xl font-semibold tracking-wide'>
              🌊 Mission Control
            </h1>
            <p className='text-xs text-blue-100/60'>
              Ocean Opportunity Strategist Dashboard
            </p>
          </div>

          <div className='flex items-center gap-4'>
            <Link
              href='/profile'
              className='text-sm text-blue-200 hover:text-white transition'
            >
              Profile
            </Link>
            <LogoutButton />
          </div>
        </div>
      </nav>

      {/* CONTENT */}
      <div className='w-full max-w-6xl px-5 py-10 flex flex-col gap-10'>
        {/* WELCOME / STATUS */}
        <section className='grid md:grid-cols-3 gap-6'>
          <div className='md:col-span-2 p-6 rounded-2xl border border-white/10 bg-white/5 backdrop-blur'>
            <h2 className='text-2xl font-bold'>Welcome back, explorer 🌊</h2>

            <p className='text-blue-100/70 mt-2'>
              Here are your best ocean-related opportunities, ranked by fit,
              effort, and urgency.
            </p>

            <div className='mt-4 text-sm text-blue-200/60'>
              Status: Ready to explore new opportunities
            </div>
          </div>

          <div className='p-6 rounded-2xl border border-white/10 bg-gradient-to-br from-blue-500/10 to-cyan-400/10 backdrop-blur'>
            <h3 className='font-semibold'>Your Profile</h3>

            <p className='text-sm text-blue-100/60 mt-2'>
              {profileData?.full_name || 'Incomplete profile'}
            </p>

            <Link
              href='/profile'
              className='inline-block mt-4 text-sm text-cyan-300 hover:text-cyan-200'
            >
              Edit Profile →
            </Link>
          </div>
        </section>

        {/* OPPORTUNITIES HEADER */}
        <section className='flex items-center justify-between'>
          <h2 className='text-xl font-semibold'>Ranked Opportunities</h2>

          <div className='text-sm text-blue-200/60'>Page {page}</div>
        </section>

        {/* GRID */}
        <section>
          <DashboardGrid items={pagedOpportunities} />
        </section>

        {/* OPTIONAL INSIGHT PANEL */}
        <section className='p-6 rounded-2xl border border-white/10 bg-white/5 backdrop-blur'>
          <h3 className='font-semibold text-lg'>AI Insight</h3>

          <p className='text-blue-100/70 mt-2'>
            Focus on opportunities that combine research + field experience.
            Your profile aligns strongly with marine conservation and coastal
            systems roles.
          </p>
        </section>
      </div>
    </div>
  );
}

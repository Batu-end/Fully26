import { MetricChip, PanelEyebrow, PremiumPanel } from '@/components/premium-panel';
import { OceanCanvas } from '@/components/scene/ocean-canvas';
import { createClient } from '@/lib/supabase/server';
import { FileText, Radar, Sparkles, Waves } from 'lucide-react';
import Link from 'next/link';

export default async function ProfilePage() {
  const supabase = await createClient();

  const {
    data: { user },
  } = await supabase.auth.getUser();

  const { data: profile } = await supabase
    .from('student_profiles')
    .select('*')
    .eq('id', user?.id)
    .single();

  const name = profile?.full_name || profile?.name || 'Profile in progress';
  const field = profile?.field || profile?.major || 'Ocean pathway not set';
  const level =
    profile?.level || profile?.education_level || 'Student / early-career';
  const location = profile?.location || 'Location not set';

  return (
    <main className='site-stage text-white'>
      <OceanCanvas variant='profile' />

      <div className='site-shell mx-auto flex min-h-screen w-full max-w-6xl flex-col px-5 py-8 md:px-8 md:py-10'>
        <div className='site-nav rounded-[1.8rem] border border-white/10 px-5 py-5'>
          <div className='flex items-center justify-between gap-4'>
            <div className='flex items-center gap-3'>
              <div className='hero-glow-ring flex h-11 w-11 items-center justify-center rounded-2xl border border-cyan-200/18 bg-cyan-300/10'>
                <Waves className='h-5 w-5 text-cyan-100' />
              </div>
              <div>
                <PanelEyebrow>Profile surface</PanelEyebrow>
                <h1 className='mt-3 text-2xl font-semibold text-white md:text-3xl'>
                  Ocean profile intelligence
                </h1>
              </div>
            </div>
            <Link
              href='/dashboard'
              className='rounded-full border border-white/12 bg-white/[0.04] px-4 py-2 text-sm text-white/84 backdrop-blur-xl transition hover:border-cyan-200/25 hover:bg-white/[0.08]'
            >
              Back to dashboard
            </Link>
          </div>
        </div>

        <div className='grid flex-1 gap-6 py-8 lg:grid-cols-[0.96fr_1.04fr]'>
          <div className='space-y-6'>
            <div className='editorial-block rounded-[2.1rem] p-6 md:p-8'>
              <PanelEyebrow>Parsed profile</PanelEyebrow>
              <h2 className='ocean-title mt-5 text-4xl font-semibold md:text-5xl'>
                {name}
              </h2>
              <p className='mt-4 max-w-xl text-sm leading-8 text-white/72 md:text-base'>
                This page gives the profile layer its own calm, readable surface
                so users can quickly understand how the system currently sees
                their background and direction.
              </p>

              <div className='mt-7 flex flex-wrap gap-3'>
                <MetricChip label='Focus' value={field} />
                <MetricChip label='Stage' value={level} />
                <MetricChip label='Location' value={location} />
              </div>
            </div>

            <PremiumPanel tone='bright'>
              <div className='grid gap-4 sm:grid-cols-2'>
                <div className='field-surface rounded-[1.4rem] p-4'>
                  <div className='text-[0.65rem] uppercase tracking-[0.24em] text-cyan-100/42'>
                    Field focus
                  </div>
                  <p className='mt-3 text-sm leading-7 text-white/80'>{field}</p>
                </div>
                <div className='field-surface rounded-[1.4rem] p-4'>
                  <div className='text-[0.65rem] uppercase tracking-[0.24em] text-cyan-100/42'>
                    Experience level
                  </div>
                  <p className='mt-3 text-sm leading-7 text-white/80'>{level}</p>
                </div>
                <div className='field-surface rounded-[1.4rem] p-4 sm:col-span-2'>
                  <div className='text-[0.65rem] uppercase tracking-[0.24em] text-cyan-100/42'>
                    Location
                  </div>
                  <p className='mt-3 text-sm leading-7 text-white/80'>{location}</p>
                </div>
              </div>
            </PremiumPanel>
          </div>

          <div className='grid gap-6'>
            <PremiumPanel>
              <div className='flex items-center gap-3'>
                <div className='hero-glow-ring flex h-11 w-11 items-center justify-center rounded-2xl border border-cyan-200/15 bg-cyan-300/10'>
                  <Radar className='h-5 w-5 text-cyan-100' />
                </div>
                <div>
                  <PanelEyebrow>Matched opportunities</PanelEyebrow>
                  <h3 className='mt-2 text-xl font-semibold text-white'>
                    Opportunity alignment
                  </h3>
                </div>
              </div>
              <p className='mt-5 text-sm leading-7 text-white/74'>
                Based on the current profile surface, the strongest directions
                combine ocean systems, applied research, and mission-driven
                environmental work.
              </p>
            </PremiumPanel>

            <PremiumPanel>
              <div className='flex items-center gap-3'>
                <div className='hero-glow-ring flex h-11 w-11 items-center justify-center rounded-2xl border border-cyan-200/15 bg-cyan-300/10'>
                  <Sparkles className='h-5 w-5 text-cyan-100' />
                </div>
                <div>
                  <PanelEyebrow>Fit interpretation</PanelEyebrow>
                  <h3 className='mt-2 text-xl font-semibold text-white'>
                    Positioning read
                  </h3>
                </div>
              </div>
              <p className='mt-5 text-sm leading-7 text-white/74'>
                The strongest narrative angle connects curiosity about ocean
                systems with practical initiative, discipline, and a clear
                desire to work where research meets real impact.
              </p>
            </PremiumPanel>

            <PremiumPanel>
              <div className='flex items-center gap-3'>
                <div className='hero-glow-ring flex h-11 w-11 items-center justify-center rounded-2xl border border-cyan-200/15 bg-cyan-300/10'>
                  <FileText className='h-5 w-5 text-cyan-100' />
                </div>
                <div>
                  <PanelEyebrow>Next actions</PanelEyebrow>
                  <h3 className='mt-2 text-xl font-semibold text-white'>
                    Continue the product flow
                  </h3>
                </div>
              </div>
              <div className='mt-5 flex flex-col gap-3 sm:flex-row'>
                <Link
                  href='/dashboard'
                  className='inline-flex items-center justify-center rounded-full bg-cyan-300 px-5 py-3 text-sm font-semibold text-slate-950 transition hover:bg-cyan-200'
                >
                  Review opportunities
                </Link>
                <Link
                  href='/profile/create'
                  className='inline-flex items-center justify-center rounded-full border border-white/12 bg-white/[0.04] px-5 py-3 text-sm text-white/84 transition hover:border-cyan-200/24 hover:bg-white/[0.08]'
                >
                  Update resume
                </Link>
              </div>
            </PremiumPanel>
          </div>
        </div>
      </div>
    </main>
  );
}

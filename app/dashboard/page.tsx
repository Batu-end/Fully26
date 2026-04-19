import { DashboardGrid } from '@/components/dashboard-components';
import { LogoutButton } from '@/components/logout-button';
import { MetricChip, PanelEyebrow, PremiumPanel } from '@/components/premium-panel';
import { OceanCanvas } from '@/components/scene/ocean-canvas';
import { createClient } from '@/lib/supabase/server';
import {
  ArrowRight,
  Compass,
  FileText,
  Radar,
  Shell,
  Sparkles,
  Waves,
} from 'lucide-react';
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
  const realItems = Array.isArray(pagedOpportunities) ? pagedOpportunities : [];

  const fallbackItems = [
    {
      id: '1',
      title: 'NOAA Ocean Exploration Fellowship',
      description:
        'Field-facing research support with strong exposure to marine systems, science communication, and expedition logistics.',
    },
    {
      id: '2',
      title: 'Blue Economy Innovation Internship',
      description:
        'Applied pathway for candidates who blend scientific literacy with systems thinking and operational curiosity.',
    },
    {
      id: '3',
      title: 'Coastal Resilience Research Placement',
      description:
        'A strong fit for students whose profile combines environmental analysis, public impact, and evidence-driven writing.',
    },
  ];

  const items = realItems.length > 0 ? realItems : fallbackItems;
  const profileName =
    profileData?.full_name || profileData?.name || user.email || 'Explorer';
  const profileFocus =
    profileData?.field ||
    profileData?.major ||
    'Marine science, ocean systems, and applied research';
  const profileLevel =
    profileData?.level || profileData?.education_level || 'Student / early-career';
  const profileLocation = profileData?.location || 'Location not set';

  return (
    <main className='site-stage text-white'>
      <OceanCanvas variant='dashboard' />

      <div className='site-shell flex min-h-screen flex-col'>
        <nav className='site-nav'>
          <div className='mx-auto flex w-full max-w-7xl items-center justify-between px-5 py-5 md:px-8'>
            <div className='flex items-center gap-3'>
              <div className='hero-glow-ring flex h-11 w-11 items-center justify-center rounded-2xl border border-cyan-200/18 bg-cyan-300/10'>
                <Waves className='h-5 w-5 text-cyan-100' />
              </div>
              <div>
                <div className='text-xs uppercase tracking-[0.32em] text-cyan-100/48'>
                  Mission control
                </div>
                <h1 className='mt-1 text-xl font-semibold text-white md:text-2xl'>
                  DeepScholar command deck
                </h1>
              </div>
            </div>

            <div className='flex items-center gap-3'>
              <Link
                href='/profile'
                className='rounded-full border border-white/12 bg-white/[0.04] px-4 py-2 text-sm text-white/84 backdrop-blur-xl transition hover:border-cyan-200/25 hover:bg-white/[0.07]'
              >
                Profile
              </Link>
              <LogoutButton />
            </div>
          </div>
        </nav>

        <div className='mx-auto flex w-full max-w-7xl flex-1 flex-col gap-8 px-5 py-8 md:px-8 md:py-10'>
          <section className='grid gap-6 xl:grid-cols-[1.15fr_0.85fr]'>
            <div className='space-y-6'>
              <div className='editorial-block rounded-[2.2rem] p-6 md:p-8'>
                <PanelEyebrow>Live command environment</PanelEyebrow>
                <h2 className='ocean-title mt-6 text-4xl font-semibold md:text-5xl xl:text-[4.5rem]'>
                  Opportunity radar, fit readouts, and application direction in one field.
                </h2>
                <p className='ocean-copy mt-5 max-w-3xl text-base leading-8 md:text-lg'>
                  Mission control is designed to feel calm under pressure. It
                  keeps your profile, ranked opportunities, fit signal, and
                  draft direction in a single high-end surface rather than
                  scattering them across generic utility views.
                </p>

                <div className='mt-8 flex flex-wrap gap-3'>
                  <MetricChip label='Profile' value={profileLevel} />
                  <MetricChip label='Focus' value={profileFocus} />
                  <MetricChip label='Page' value={`0${page}`} />
                </div>
              </div>

              <PremiumPanel tone='bright'>
                <div className='grid gap-4 sm:grid-cols-3'>
                  <div className='field-surface rounded-[1.4rem] p-4'>
                    <div className='text-[0.65rem] uppercase tracking-[0.26em] text-cyan-100/45'>
                      Parsed profile
                    </div>
                    <p className='mt-3 text-sm leading-7 text-white/78'>
                      The intake flow becomes a usable profile foundation instead
                      of staying buried in raw documents and guesswork.
                    </p>
                  </div>
                  <div className='field-surface rounded-[1.4rem] p-4'>
                    <div className='text-[0.65rem] uppercase tracking-[0.26em] text-cyan-100/45'>
                      Opportunity fit
                    </div>
                    <p className='mt-3 text-sm leading-7 text-white/78'>
                      Ranking and fit interpretation focus attention where your
                      effort is most likely to compound.
                    </p>
                  </div>
                  <div className='field-surface rounded-[1.4rem] p-4'>
                    <div className='text-[0.65rem] uppercase tracking-[0.26em] text-cyan-100/45'>
                      Draft vector
                    </div>
                    <p className='mt-3 text-sm leading-7 text-white/78'>
                      Writing support stays close to signal instead of becoming a
                      detached blank-page exercise.
                    </p>
                  </div>
                </div>
              </PremiumPanel>
            </div>

            <div className='grid gap-6'>
              <PremiumPanel>
                <div className='flex items-start justify-between gap-4'>
                  <div>
                    <PanelEyebrow>Current profile surface</PanelEyebrow>
                    <h3 className='mt-4 text-2xl font-semibold text-white'>
                      {profileName}
                    </h3>
                  </div>
                  <div className='hero-glow-ring flex h-12 w-12 items-center justify-center rounded-2xl border border-cyan-200/15 bg-cyan-300/10'>
                    <Shell className='h-5 w-5 text-cyan-100' />
                  </div>
                </div>

                <div className='mt-6 grid gap-4 sm:grid-cols-2'>
                  <div>
                    <div className='text-[0.65rem] uppercase tracking-[0.24em] text-cyan-100/42'>
                      Focus area
                    </div>
                    <p className='mt-2 text-sm leading-7 text-white/78'>
                      {profileFocus}
                    </p>
                  </div>
                  <div>
                    <div className='text-[0.65rem] uppercase tracking-[0.24em] text-cyan-100/42'>
                      Stage
                    </div>
                    <p className='mt-2 text-sm leading-7 text-white/78'>
                      {profileLevel}
                    </p>
                  </div>
                  <div className='sm:col-span-2'>
                    <div className='text-[0.65rem] uppercase tracking-[0.24em] text-cyan-100/42'>
                      Location
                    </div>
                    <p className='mt-2 text-sm leading-7 text-white/78'>
                      {profileLocation}
                    </p>
                  </div>
                </div>

                <Link
                  href='/profile'
                  className='mt-6 inline-flex items-center gap-2 text-sm text-cyan-100/76 transition hover:text-cyan-100'
                >
                  Review profile surface
                  <ArrowRight className='h-4 w-4' />
                </Link>
              </PremiumPanel>

              <PremiumPanel tone='shadow'>
                <PanelEyebrow>Selected target</PanelEyebrow>
                <h3 className='mt-4 text-2xl font-semibold text-white'>
                  {items[0]?.title || 'Opportunity detail surface'}
                </h3>
                <p className='mt-3 text-sm leading-7 text-white/74'>
                  {items[0]?.description ||
                    'Use this panel to hold the current target in view while the rest of mission control interprets fit and narrative direction.'}
                </p>
                <div className='mt-5 inline-flex items-center gap-2 rounded-full border border-cyan-200/14 bg-cyan-300/8 px-3 py-1 text-[0.68rem] uppercase tracking-[0.24em] text-cyan-100/60'>
                  <Compass className='h-4 w-4' />
                  Priority target aligned
                </div>
              </PremiumPanel>
            </div>
          </section>

          <section className='grid gap-6 lg:grid-cols-[1.12fr_0.88fr]'>
            <PremiumPanel tone='bright'>
              <div className='flex items-center justify-between gap-4'>
                <div>
                  <PanelEyebrow>Matched opportunities</PanelEyebrow>
                  <h2 className='mt-4 text-2xl font-semibold text-white md:text-3xl'>
                    Ranked ocean pathways
                  </h2>
                </div>
                <div className='signal-pill inline-flex rounded-full px-4 py-2 text-sm'>
                  Page {page}
                </div>
              </div>

              <div className='mt-6'>
                <DashboardGrid items={items} />
              </div>
            </PremiumPanel>

            <div className='grid gap-6'>
              <PremiumPanel>
                <div className='flex items-center gap-3'>
                  <div className='hero-glow-ring flex h-11 w-11 items-center justify-center rounded-2xl border border-cyan-200/15 bg-cyan-300/10'>
                    <Radar className='h-5 w-5 text-cyan-100' />
                  </div>
                  <div>
                    <PanelEyebrow>Fit analysis</PanelEyebrow>
                    <h3 className='mt-2 text-xl font-semibold text-white'>
                      Where your signal is strongest
                    </h3>
                  </div>
                </div>
                <p className='mt-5 text-sm leading-7 text-white/74'>
                  Your profile currently reads strongest for mission-driven
                  marine research, coastal systems work, and roles that reward
                  evidence-heavy thinking paired with scientific communication.
                </p>
              </PremiumPanel>

              <PremiumPanel>
                <div className='flex items-center gap-3'>
                  <div className='hero-glow-ring flex h-11 w-11 items-center justify-center rounded-2xl border border-cyan-200/15 bg-cyan-300/10'>
                    <Sparkles className='h-5 w-5 text-cyan-100' />
                  </div>
                  <div>
                    <PanelEyebrow>Positioning system</PanelEyebrow>
                    <h3 className='mt-2 text-xl font-semibold text-white'>
                      Narrative angle to develop
                    </h3>
                  </div>
                </div>
                <p className='mt-5 text-sm leading-7 text-white/74'>
                  Lead with systems curiosity, environmental responsibility, and
                  concrete initiative. The strongest story connects technical
                  discipline with real ocean impact.
                </p>
              </PremiumPanel>

              <PremiumPanel>
                <div className='flex items-center gap-3'>
                  <div className='hero-glow-ring flex h-11 w-11 items-center justify-center rounded-2xl border border-cyan-200/15 bg-cyan-300/10'>
                    <FileText className='h-5 w-5 text-cyan-100' />
                  </div>
                  <div>
                    <PanelEyebrow>Draft output</PanelEyebrow>
                    <h3 className='mt-2 text-xl font-semibold text-white'>
                      Writing surface ready
                    </h3>
                  </div>
                </div>
                <p className='mt-5 text-sm leading-7 text-white/74'>
                  Draft work should begin from the signal already visible here,
                  not from a blank page. This keeps the writing phase aligned
                  with fit, evidence, and opportunity shape.
                </p>
              </PremiumPanel>
            </div>
          </section>
        </div>
      </div>
    </main>
  );
}

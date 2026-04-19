import { PanelEyebrow, PremiumPanel } from '@/components/premium-panel';
import { OceanCanvas } from '@/components/scene/ocean-canvas';
import { createClient } from '@/lib/supabase/server';
import { ArrowLeft, Radar, Sparkles, Waves } from 'lucide-react';
import Link from 'next/link';
import { Suspense } from 'react';

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
    <div className='grid gap-6 lg:grid-cols-[1.06fr_0.94fr]'>
      <div className='space-y-6'>
        <div className='editorial-block rounded-[2.1rem] p-6 md:p-8'>
          <PanelEyebrow>Selected opportunity</PanelEyebrow>
          <h1 className='ocean-title mt-5 text-4xl font-semibold md:text-5xl'>
            {opportunity.title}
          </h1>
          <p className='mt-6 text-sm leading-8 text-white/72 md:text-base'>
            {opportunity.description}
          </p>
        </div>

        <PremiumPanel tone='bright'>
          <div className='grid gap-4 sm:grid-cols-2'>
            <div className='field-surface rounded-[1.4rem] p-4'>
              <div className='text-[0.65rem] uppercase tracking-[0.26em] text-cyan-100/45'>
                Surface type
              </div>
              <p className='mt-3 text-sm leading-7 text-white/78'>
                Opportunity detail is designed to keep the target opportunity in
                focus while fit and narrative strategy remain visible beside it.
              </p>
            </div>
            <div className='field-surface rounded-[1.4rem] p-4'>
              <div className='text-[0.65rem] uppercase tracking-[0.26em] text-cyan-100/45'>
                Current role
              </div>
              <p className='mt-3 text-sm leading-7 text-white/78'>
                This surface acts as the bridge between ranked discovery and the
                final application positioning work.
              </p>
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
              <PanelEyebrow>Fit analysis</PanelEyebrow>
              <h2 className='mt-2 text-xl font-semibold text-white'>
                Opportunity review surface
              </h2>
            </div>
          </div>
          <p className='mt-5 text-sm leading-7 text-white/74'>
            This panel is reserved for hard filters, strategic fit, and the
            reasons this opening deserves attention relative to the rest of the
            radar.
          </p>
        </PremiumPanel>

        <PremiumPanel>
          <div className='flex items-center gap-3'>
            <div className='hero-glow-ring flex h-11 w-11 items-center justify-center rounded-2xl border border-cyan-200/15 bg-cyan-300/10'>
              <Sparkles className='h-5 w-5 text-cyan-100' />
            </div>
            <div>
              <PanelEyebrow>Positioning notes</PanelEyebrow>
              <h2 className='mt-2 text-xl font-semibold text-white'>
                Draft direction placeholder
              </h2>
            </div>
          </div>
          <p className='mt-5 text-sm leading-7 text-white/74'>
            Keep narrative strategy, proof points, and writing guidance visible
            here so the user can move from fit to application framing without
            losing the target opportunity context.
          </p>
        </PremiumPanel>
      </div>
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
    <main className='site-stage text-white'>
      <OceanCanvas variant='ambient' />

      <div className='site-shell mx-auto flex min-h-screen w-full max-w-6xl flex-col px-5 py-8 md:px-8 md:py-10'>
        <div className='site-nav mb-8 rounded-[1.8rem] border border-white/10 px-5 py-5'>
          <div className='flex items-center justify-between gap-4'>
            <div className='flex items-center gap-3'>
              <div className='hero-glow-ring flex h-11 w-11 items-center justify-center rounded-2xl border border-cyan-200/18 bg-cyan-300/10'>
                <Waves className='h-5 w-5 text-cyan-100' />
              </div>
              <div>
                <PanelEyebrow>Opportunity detail</PanelEyebrow>
                <h1 className='mt-3 text-2xl font-semibold text-white md:text-3xl'>
                  Opportunity analysis
                </h1>
              </div>
            </div>
            <Link
              href='/dashboard'
              className='inline-flex items-center gap-2 rounded-full border border-white/12 bg-white/[0.04] px-4 py-2 text-sm text-white/84 transition hover:border-cyan-200/25 hover:bg-white/[0.08]'
            >
              <ArrowLeft className='h-4 w-4' />
              Back to dashboard
            </Link>
          </div>
        </div>

        <Suspense fallback={<div className='text-white/70'>Loading opportunity...</div>}>
          <OpportunityDetail id={id} />
        </Suspense>
      </div>
    </main>
  );
}

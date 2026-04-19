import { AuthButton } from '@/components/auth-button';
import { MetricChip, PanelEyebrow, PremiumPanel } from '@/components/premium-panel';
import { OceanCanvas } from '@/components/scene/ocean-canvas';
import { ThemeSwitcher } from '@/components/theme-switcher';
import {
  ArrowRight,
  Compass,
  Cpu,
  FileText,
  Radar,
  Sparkles,
  Waves,
} from 'lucide-react';
import Link from 'next/link';
import { Suspense } from 'react';

const systemMoments = [
  {
    title: 'Profile intelligence',
    copy:
      'Turn raw resumes and profile fragments into something navigable, strategic, and ready for real opportunity decisions.',
    icon: FileText,
  },
  {
    title: 'Opportunity radar',
    copy:
      'Scan ocean-facing pathways through a clearer lens of timing, fit, and what is actually worth a serious application.',
    icon: Radar,
  },
  {
    title: 'Positioning system',
    copy:
      'Move from vague ambition to persuasive application framing with a calmer, evidence-led narrative surface.',
    icon: Sparkles,
  },
];

const commandSignals = [
  'Bioluminescent intake sequence',
  'Opportunity ranking and target selection',
  'Fit and readiness interpretation',
  'Positioning + draft development',
];

export default function Home() {
  return (
    <main className='site-stage text-white'>
      <OceanCanvas variant='landing' />

      <div className='site-shell flex min-h-screen flex-col'>
        <nav className='site-nav sticky top-0 z-30'>
          <div className='mx-auto flex w-full max-w-7xl items-center justify-between px-5 py-4 md:px-8'>
            <Link
              href='/'
              className='group flex items-center gap-3'
            >
              <div className='hero-glow-ring flex h-11 w-11 items-center justify-center rounded-2xl border border-cyan-200/20 bg-cyan-300/10'>
                <Waves className='h-5 w-5 text-cyan-100' />
              </div>
              <div>
                <div className='text-xs uppercase tracking-[0.32em] text-cyan-100/55'>
                  DeepScholar
                </div>
                <div className='text-sm text-white/86 group-hover:text-cyan-100'>
                  Ocean opportunity strategist
                </div>
              </div>
            </Link>

            <div className='flex items-center gap-3'>
              <ThemeSwitcher />
              <Suspense>
                <AuthButton />
              </Suspense>
            </div>
          </div>
        </nav>

        <div className='mx-auto flex w-full max-w-7xl flex-1 flex-col gap-20 px-5 pb-16 pt-8 md:px-8 md:pt-12'>
          <section className='grid min-h-[calc(100vh-10rem)] items-center gap-8 lg:grid-cols-[1.02fr_0.98fr] lg:gap-12'>
            <div className='max-w-3xl'>
              <div className='editorial-block rounded-[2.2rem] p-6 md:p-8'>
                <PanelEyebrow>Luxury ocean-tech discovery system</PanelEyebrow>
                <h1 className='ocean-title mt-6 text-5xl font-semibold leading-[0.9] md:text-7xl xl:text-[5.5rem]'>
                  A cinematic command deck for marine ambition.
                </h1>
                <p className='ocean-copy mt-6 max-w-2xl text-lg leading-8 md:text-xl'>
                  DeepScholar reframes the opportunity search as something
                  atmospheric, precise, and deeply intentional, where profile
                  signal, fit, and application strategy unfold inside a living
                  abyssal interface.
                </p>

                <div className='mt-8 flex flex-col gap-4 sm:flex-row'>
                  <Link
                    href='/profile/create'
                    className='inline-flex items-center justify-center rounded-full bg-cyan-300 px-7 py-3.5 text-sm font-semibold text-slate-950 shadow-[0_18px_40px_rgba(97,247,255,0.28)] transition hover:bg-cyan-200'
                  >
                    Enter the intake sequence
                  </Link>
                  <Link
                    href='/dashboard'
                    className='inline-flex items-center justify-center rounded-full border border-white/12 bg-white/[0.04] px-7 py-3.5 text-sm font-medium text-white/86 backdrop-blur-xl transition hover:border-cyan-200/25 hover:bg-white/[0.07]'
                  >
                    View mission control
                  </Link>
                </div>

                <div className='mt-8 grid gap-3 sm:grid-cols-3'>
                  <MetricChip label='World' value='Living abyss backdrop' />
                  <MetricChip label='Flow' value='Intake to draft' />
                  <MetricChip label='Mood' value='Cinematic restraint' />
                </div>
              </div>
            </div>

            <PremiumPanel tone='bright' className='overflow-hidden'>
              <div className='grid gap-6 md:grid-cols-[0.74fr_1.26fr]'>
                <div className='field-surface rounded-[1.7rem] p-5'>
                  <div className='text-[0.7rem] uppercase tracking-[0.28em] text-cyan-100/45'>
                    Command stack
                  </div>
                  <div className='mt-5 space-y-3'>
                    {commandSignals.map((item, index) => (
                      <div
                        key={item}
                        className='field-surface rounded-[1.25rem] px-4 py-3'
                      >
                        <div className='text-[0.65rem] uppercase tracking-[0.24em] text-cyan-100/42'>
                          {`0${index + 1}`}
                        </div>
                        <div className='mt-1 text-sm text-white/84'>{item}</div>
                      </div>
                    ))}
                  </div>
                </div>

                <div className='space-y-4'>
                  <div className='rounded-[1.75rem] border border-white/10 bg-white/[0.04] p-5 backdrop-blur-xl'>
                    <div className='flex items-start justify-between gap-4'>
                      <div>
                        <div className='text-[0.68rem] uppercase tracking-[0.28em] text-cyan-100/45'>
                          Showcase path
                        </div>
                        <h2 className='mt-2 text-2xl font-semibold text-white md:text-3xl'>
                          Begin with the immersive profile intake, then drop into mission control.
                        </h2>
                      </div>
                      <Cpu className='mt-1 h-5 w-5 text-cyan-200/78' />
                    </div>
                    <p className='mt-4 text-sm leading-7 text-blue-50/70'>
                      The cleanest demo story starts with the live intake
                      environment at `/profile/create`, then shifts into the
                      dashboard to show opportunity ranking, fit interpretation,
                      and writing direction.
                    </p>
                  </div>

                  <div className='grid gap-4 sm:grid-cols-2'>
                    <div className='rounded-[1.55rem] border border-cyan-200/16 bg-cyan-300/[0.07] p-5'>
                      <div className='flex items-center gap-2 text-cyan-100/82'>
                        <Compass className='h-4 w-4' />
                        <span className='text-[0.68rem] uppercase tracking-[0.26em]'>
                          Composition
                        </span>
                      </div>
                      <p className='mt-3 text-sm leading-7 text-white/78'>
                        Strong editorial hierarchy and restrained luxury keep the
                        atmosphere memorable without burying the product.
                      </p>
                    </div>
                    <div className='rounded-[1.55rem] border border-white/10 bg-white/[0.035] p-5'>
                      <div className='text-[0.68rem] uppercase tracking-[0.26em] text-cyan-100/45'>
                        Atmosphere
                      </div>
                      <p className='mt-3 text-sm leading-7 text-white/72'>
                        Jelly glow, ray shadows, light shafts, and fish
                        silhouettes create a living world rather than a static
                        design skin.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </PremiumPanel>
          </section>

          <section className='grid gap-6 lg:grid-cols-3'>
            {systemMoments.map((item) => {
              const Icon = item.icon;
              return (
                <PremiumPanel key={item.title}>
                  <div className='flex items-center gap-3'>
                    <div className='hero-glow-ring flex h-12 w-12 items-center justify-center rounded-2xl border border-cyan-200/15 bg-cyan-300/10'>
                      <Icon className='h-5 w-5 text-cyan-100' />
                    </div>
                    <div className='text-[0.68rem] uppercase tracking-[0.26em] text-cyan-100/45'>
                      System layer
                    </div>
                  </div>
                  <h3 className='mt-5 text-2xl font-semibold text-white'>
                    {item.title}
                  </h3>
                  <p className='mt-3 text-sm leading-7 text-white/72'>
                    {item.copy}
                  </p>
                </PremiumPanel>
              );
            })}
          </section>

          <section className='grid gap-6 lg:grid-cols-[0.88fr_1.12fr]'>
            <PremiumPanel tone='shadow'>
              <PanelEyebrow>Why this matters</PanelEyebrow>
              <h2 className='ocean-title mt-5 text-3xl font-semibold text-white md:text-4xl'>
                Ocean opportunity discovery should feel like navigation, not noise.
              </h2>
              <p className='mt-5 max-w-xl text-sm leading-8 text-white/72 md:text-base'>
                Most applicants are forced into scattered listings, generic
                drafting, and poor fit visibility. This product turns that
                journey into a clear, high-signal interface that feels calm even
                when the decisions are high stakes.
              </p>
            </PremiumPanel>

            <div className='grid gap-4 sm:grid-cols-2'>
              <PremiumPanel className='min-h-[13rem]'>
                <div className='signal-pill inline-flex rounded-full px-3 py-1 text-[0.68rem] uppercase tracking-[0.26em]'>
                  Parse
                </div>
                <h3 className='mt-4 text-xl font-semibold text-white'>
                  Turn raw information into structure
                </h3>
                <p className='mt-3 text-sm leading-7 text-white/70'>
                  Pull academics, evidence, themes, and direction into a profile
                  surface that can actually guide the rest of the product.
                </p>
              </PremiumPanel>
              <PremiumPanel className='min-h-[13rem]'>
                <div className='signal-pill inline-flex rounded-full px-3 py-1 text-[0.68rem] uppercase tracking-[0.26em]'>
                  Analyze
                </div>
                <h3 className='mt-4 text-xl font-semibold text-white'>
                  Reveal fit with honesty
                </h3>
                <p className='mt-3 text-sm leading-7 text-white/70'>
                  Separate hard requirements from softer narrative alignment so
                  effort goes where it can genuinely matter.
                </p>
              </PremiumPanel>
              <PremiumPanel className='min-h-[13rem]'>
                <div className='signal-pill inline-flex rounded-full px-3 py-1 text-[0.68rem] uppercase tracking-[0.26em]'>
                  Position
                </div>
                <h3 className='mt-4 text-xl font-semibold text-white'>
                  Build a stronger application angle
                </h3>
                <p className='mt-3 text-sm leading-7 text-white/70'>
                  Move toward a persuasive narrative that feels specific,
                  elegant, and grounded in the evidence already gathered.
                </p>
              </PremiumPanel>
              <PremiumPanel className='min-h-[13rem]'>
                <div className='signal-pill inline-flex rounded-full px-3 py-1 text-[0.68rem] uppercase tracking-[0.26em]'>
                  Draft
                </div>
                <h3 className='mt-4 text-xl font-semibold text-white'>
                  Start from signal, not a blank page
                </h3>
                <p className='mt-3 text-sm leading-7 text-white/70'>
                  Keep writing support connected to fit, profile evidence, and
                  the opportunity target instead of starting cold.
                </p>
              </PremiumPanel>
            </div>
          </section>

          <section className='pb-8'>
            <PremiumPanel tone='bright' className='overflow-hidden'>
              <div className='grid items-center gap-8 lg:grid-cols-[1fr_auto]'>
                <div>
                  <PanelEyebrow>Recommended showcase order</PanelEyebrow>
                  <h2 className='ocean-title mt-5 text-3xl font-semibold text-white md:text-4xl'>
                    Open the intake sequence first, then move through the command deck.
                  </h2>
                  <p className='mt-4 max-w-2xl text-sm leading-8 text-white/72 md:text-base'>
                    That path gives the strongest three-second impression, then
                    quickly proves the rest of the product world with the
                    dashboard, profile surfaces, and opportunity detail views.
                  </p>
                </div>
                <div className='flex flex-col gap-3 sm:flex-row'>
                  <Link
                    href='/profile/create'
                    className='inline-flex items-center justify-center rounded-full bg-white px-6 py-3 text-sm font-semibold text-slate-950 transition hover:bg-cyan-100'
                  >
                    Launch intake
                  </Link>
                  <Link
                    href='/dashboard'
                    className='inline-flex items-center justify-center gap-2 rounded-full border border-white/15 bg-white/[0.04] px-6 py-3 text-sm font-medium text-white/86 transition hover:border-cyan-200/30'
                  >
                    Mission control
                    <ArrowRight className='h-4 w-4' />
                  </Link>
                </div>
              </div>
            </PremiumPanel>
          </section>
        </div>

        <footer className='site-divider relative z-10'>
          <div className='mx-auto flex w-full max-w-7xl flex-col gap-4 px-5 py-8 text-sm text-blue-100/54 md:flex-row md:items-center md:justify-between md:px-8'>
            <p>DeepScholar pairs marine ambition with a calmer, more strategic application workflow.</p>
            <p className='text-cyan-100/52'>A cinematic deep-sea product world</p>
          </div>
        </footer>
      </div>
    </main>
  );
}

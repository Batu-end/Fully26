import { AuthButton } from '@/components/auth-button';
import { ThemeSwitcher } from '@/components/theme-switcher';
import Link from 'next/link';
import { Suspense } from 'react';

export default function Home() {
  return (
    <main className='min-h-screen flex flex-col items-center bg-gradient-to-b from-slate-950 via-blue-950 to-slate-900 text-white'>
      <div className='flex-1 w-full flex flex-col items-center'>
        {/* NAVBAR */}
        <nav className='w-full flex justify-center border-b border-white/10 backdrop-blur'>
          <div className='w-full max-w-6xl flex justify-between items-center px-5 h-16'>
            <Link
              href='/'
              className='font-semibold text-lg tracking-wide'
            >
              🌊 DeepScholar
            </Link>

            <Suspense>
              <AuthButton />
            </Suspense>
          </div>
        </nav>

        {/* CONTENT */}
        <div className='w-full max-w-6xl px-5 py-20 flex flex-col gap-28'>
          {/* HERO */}
          <section className='text-center flex flex-col items-center gap-6 relative'>
            {/* glow effect */}
            <div className='absolute w-[500px] h-[500px] bg-blue-500/20 blur-[120px] rounded-full -z-10' />

            <h1 className='text-4xl md:text-6xl font-bold leading-tight'>
              Find Your Path Into
              <span className='block text-blue-400'>
                Ocean & Climate Careers
              </span>
            </h1>

            <p className='text-lg text-blue-100/80 max-w-2xl'>
              An AI-powered strategist that helps you discover, prioritize, and
              apply to the best ocean-related opportunities — tailored to you.
            </p>

            <div className='flex gap-4 mt-4'>
              <Link
                href='/dashboard'
                className='px-6 py-3 rounded-xl bg-blue-500 hover:bg-blue-400 text-white font-medium shadow-lg shadow-blue-500/30 transition'
              >
                Get Started
              </Link>

              <Link
                href='/upload'
                className='px-6 py-3 rounded-xl border border-white/20 hover:bg-white/10 transition'
              >
                Upload Resume
              </Link>
            </div>

            <p className='text-sm text-blue-200/60 mt-2'>
              No endless searching. No guesswork. Just clear next steps.
            </p>
          </section>

          {/* PROBLEM */}
          <section className='flex flex-col gap-6'>
            <h2 className='text-2xl font-semibold text-center'>
              Breaking into ocean careers is harder than it should be
            </h2>

            <div className='grid md:grid-cols-2 gap-6 text-blue-100/70'>
              <ul className='space-y-2'>
                <li>• Opportunities are scattered across dozens of sites</li>
                <li>• It’s unclear which ones actually fit your profile</li>
              </ul>
              <ul className='space-y-2'>
                <li>• Applications take time — and strategy matters</li>
                <li>• Most people don’t know where to start</li>
              </ul>
            </div>

            <p className='text-center text-blue-200/60'>
              Opportunities are missed — not because of lack of potential, but
              lack of direction.
            </p>
          </section>

          {/* SOLUTION */}
          <section className='flex flex-col gap-6 text-center'>
            <h2 className='text-2xl font-semibold'>
              A smarter way to navigate opportunities
            </h2>

            <div className='grid md:grid-cols-2 gap-6 text-left'>
              {[
                'Upload your resume and profile',
                'Get matched with curated opportunities',
                'See rankings by fit, effort, urgency',
                'Get positioning advice + draft starters',
              ].map((item, i) => (
                <div
                  key={i}
                  className='p-6 rounded-xl bg-white/5 border border-white/10 backdrop-blur hover:bg-white/10 transition'
                >
                  {item}
                </div>
              ))}
            </div>
          </section>

          {/* HOW IT WORKS */}
          <section className='flex flex-col gap-8'>
            <h2 className='text-2xl font-semibold text-center'>How it works</h2>

            <div className='grid md:grid-cols-4 gap-6'>
              {[
                {
                  title: 'Build Profile',
                  desc: 'Upload resume + interests',
                },
                {
                  title: 'Get Matches',
                  desc: 'AI finds best opportunities',
                },
                {
                  title: 'Prioritize',
                  desc: 'Ranked by fit & urgency',
                },
                {
                  title: 'Apply',
                  desc: 'Drafts + guidance',
                },
              ].map((step, i) => (
                <div
                  key={i}
                  className='p-6 rounded-xl bg-white/5 border border-white/10 backdrop-blur'
                >
                  <h3 className='font-semibold mb-2 text-blue-300'>
                    {step.title}
                  </h3>
                  <p className='text-sm text-blue-100/70'>{step.desc}</p>
                </div>
              ))}
            </div>
          </section>

          {/* FEATURES */}
          <section className='flex flex-col gap-8'>
            <h2 className='text-2xl font-semibold text-center'>
              What makes it different
            </h2>

            <div className='grid md:grid-cols-3 gap-6'>
              {[
                'AI Fit Analysis',
                'Opportunity Ranking',
                'Application Strategy',
                'Draft Generation',
                'Progress Tracking',
                'Focused MVP',
              ].map((feature, i) => (
                <div
                  key={i}
                  className='p-6 rounded-xl bg-gradient-to-br from-blue-500/10 to-cyan-400/10 border border-white/10 text-center'
                >
                  {feature}
                </div>
              ))}
            </div>
          </section>

          {/* FINAL CTA */}
          <section className='text-center flex flex-col gap-6 items-center relative'>
            <div className='absolute w-[400px] h-[400px] bg-cyan-400/20 blur-[100px] rounded-full -z-10' />

            <h2 className='text-3xl font-bold'>
              Start building your ocean career today
            </h2>

            <p className='text-blue-100/70'>
              Upload your profile. Discover your best opportunities. Take
              action.
            </p>

            <Link
              href='/dashboard'
              className='px-8 py-4 rounded-xl bg-cyan-400 hover:bg-cyan-300 text-slate-900 font-semibold shadow-lg shadow-cyan-400/30 transition'
            >
              Dive In
            </Link>
          </section>
        </div>

        {/* FOOTER */}
        <footer className='w-full flex flex-col items-center justify-center border-t border-white/10 text-center text-xs gap-4 py-10'>
          <ThemeSwitcher />
          <p className='text-blue-200/50'>
            Built for Hackathon • Team DeepScholar
          </p>
        </footer>
      </div>
    </main>
  );
}

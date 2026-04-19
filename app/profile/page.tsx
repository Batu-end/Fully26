import { createClient } from '@/lib/supabase/server';

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

  return (
    <div className='min-h-screen w-full bg-gradient-to-b from-slate-950 via-blue-950 to-slate-900 text-white flex flex-col items-center'>
      {/* glow */}
      <div className='absolute w-[500px] h-[500px] bg-cyan-400/10 blur-[140px] rounded-full -z-10 top-40 left-1/2 -translate-x-1/2' />

      {/* NAV */}
      <div className='w-full border-b border-white/10 bg-white/5 backdrop-blur'>
        <div className='max-w-5xl mx-auto p-5 flex justify-between items-center'>
          <h1 className='text-lg font-semibold'>🌊 Ocean Profile</h1>
        </div>
      </div>

      {/* CONTENT */}
      <div className='w-full max-w-4xl px-5 py-12 flex flex-col gap-10'>
        {/* HEADER */}
        <section className='text-center'>
          <h2 className='text-3xl font-bold'>Your Ocean Profile</h2>
          <p className='text-blue-100/60 mt-2'>
            This is how the system understands your skills, interests, and
            direction.
          </p>
        </section>

        {/* PROFILE CARD */}
        <section className='p-6 rounded-2xl border border-white/10 bg-white/5 backdrop-blur flex flex-col gap-6'>
          <div>
            <h3 className='text-xl font-semibold'>Personal Information</h3>

            <div className='mt-4 grid md:grid-cols-2 gap-4 text-sm text-blue-100/70'>
              <div>
                <p className='text-white/60'>Name</p>
                <p>{profile?.full_name || 'Not set'}</p>
              </div>

              <div>
                <p className='text-white/60'>Field of Interest</p>
                <p>{profile?.field || 'Marine Science / Ocean Engineering'}</p>
              </div>

              <div>
                <p className='text-white/60'>Experience Level</p>
                <p>{profile?.level || 'Student / Early Career'}</p>
              </div>

              <div>
                <p className='text-white/60'>Location</p>
                <p>{profile?.location || 'Not set'}</p>
              </div>
            </div>
          </div>
        </section>

        {/* AI UNDERSTANDING PANEL */}
        <section className='p-6 rounded-2xl border border-cyan-400/20 bg-gradient-to-br from-cyan-500/10 to-blue-500/10 backdrop-blur'>
          <h3 className='text-lg font-semibold text-cyan-300'>
            AI Profile Interpretation
          </h3>

          <p className='text-blue-100/70 mt-3'>
            Based on your profile, you align strongly with ocean systems, field
            research, and applied environmental work. The system prioritizes
            opportunities with hands-on marine data collection and
            sustainability impact.
          </p>
        </section>

        {/* ACTIONS */}
        <section className='flex flex-col md:flex-row gap-4 justify-center'>
          <a
            href='/dashboard'
            className='px-6 py-3 rounded-xl bg-cyan-400 text-slate-900 font-semibold hover:bg-cyan-300 transition text-center'
          >
            Go to Opportunities
          </a>

          <a
            href='/upload'
            className='px-6 py-3 rounded-xl border border-white/20 hover:bg-white/10 transition text-center'
          >
            Update Resume
          </a>
        </section>
      </div>
    </div>
  );
}

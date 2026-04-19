import { PanelEyebrow, PremiumPanel } from '@/components/premium-panel';
import { OceanCanvas } from '@/components/scene/ocean-canvas';
import { createClient } from '@/lib/supabase/server';
import { Waves } from 'lucide-react';
import { redirect } from 'next/navigation';

export default async function FinishProfilePage() {
  const supabase = await createClient();

  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user) {
    redirect('/auth/signin');
  }

  const { data: profileData, error } = await supabase
    .from('student_profiles')
    .select('*')
    .eq('id', user.id)
    .single();

  if (error || !profileData) {
    console.error('Error fetching profile:', error);
    redirect('/profile/create');
  }

  const updateProfile = async (formData: FormData) => {
    'use server';

    const supabase = await createClient();

    const name = formData.get('name') as string;
    const education_level = formData.get('education_level') as string;
    const major = formData.get('major') as string;
    const interests = formData.get('interests') as string;
    const resume_text = formData.get('resume_text') as string;

    const {
      data: { user },
    } = await supabase.auth.getUser();

    if (!user) {
      redirect('/auth/signin');
    }

    const { error } = await supabase
      .from('student_profiles')
      .update({
        name,
        education_level,
        major,
        interests,
        resume_text,
      })
      .eq('id', user.id);

    if (error) {
      console.error(error);
      throw new Error('Failed to update profile');
    }

    redirect('/dashboard');
  };

  return (
    <main className='site-stage text-white'>
      <OceanCanvas variant='profile' />

      <div className='site-shell mx-auto flex min-h-screen w-full max-w-4xl flex-col justify-center px-5 py-10 md:px-8'>
        <PremiumPanel tone='bright'>
          <div className='text-center'>
            <div className='mx-auto mb-5 flex h-12 w-12 items-center justify-center rounded-2xl border border-cyan-200/18 bg-cyan-300/10 hero-glow-ring'>
              <Waves className='h-5 w-5 text-cyan-100' />
            </div>
            <PanelEyebrow>Profile completion</PanelEyebrow>
            <h1 className='ocean-title mt-5 text-4xl font-semibold md:text-5xl'>
              Refine your profile before the next dive.
            </h1>
            <p className='mx-auto mt-4 max-w-2xl text-sm leading-8 text-white/70 md:text-base'>
              Review the extracted information, tighten the essentials, and keep
              the mission-control experience grounded in accurate profile signal.
            </p>
          </div>

          <form
            action={updateProfile}
            className='mt-8 grid gap-5'
          >
            <div className='grid gap-5 md:grid-cols-2'>
              <div className='space-y-2'>
                <label className='text-xs uppercase tracking-[0.22em] text-cyan-100/48'>
                  Name
                </label>
                <input
                  name='name'
                  defaultValue={profileData.name ?? ''}
                  className='field-surface w-full rounded-[1.35rem] px-4 py-3 text-white outline-none transition placeholder:text-white/25 focus:border-cyan-200/28'
                />
              </div>

              <div className='space-y-2'>
                <label className='text-xs uppercase tracking-[0.22em] text-cyan-100/48'>
                  Education level
                </label>
                <input
                  name='education_level'
                  defaultValue={profileData.education_level ?? ''}
                  className='field-surface w-full rounded-[1.35rem] px-4 py-3 text-white outline-none transition placeholder:text-white/25 focus:border-cyan-200/28'
                />
              </div>

              <div className='space-y-2'>
                <label className='text-xs uppercase tracking-[0.22em] text-cyan-100/48'>
                  Major
                </label>
                <input
                  name='major'
                  defaultValue={profileData.major ?? ''}
                  className='field-surface w-full rounded-[1.35rem] px-4 py-3 text-white outline-none transition placeholder:text-white/25 focus:border-cyan-200/28'
                />
              </div>

              <div className='space-y-2'>
                <label className='text-xs uppercase tracking-[0.22em] text-cyan-100/48'>
                  Interests
                </label>
                <input
                  name='interests'
                  defaultValue={profileData.interests ?? ''}
                  className='field-surface w-full rounded-[1.35rem] px-4 py-3 text-white outline-none transition placeholder:text-white/25 focus:border-cyan-200/28'
                />
              </div>
            </div>

            <div className='space-y-2'>
              <label className='text-xs uppercase tracking-[0.22em] text-cyan-100/48'>
                Resume text
              </label>
              <textarea
                name='resume_text'
                defaultValue={profileData.resume_text ?? ''}
                className='field-surface min-h-[180px] w-full rounded-[1.6rem] px-4 py-4 text-white outline-none transition placeholder:text-white/25 focus:border-cyan-200/28'
              />
            </div>

            <button
              type='submit'
              className='mt-2 inline-flex h-12 items-center justify-center rounded-full bg-cyan-300 px-6 text-sm font-semibold text-slate-950 transition hover:bg-cyan-200'
            >
              Save profile
            </button>
          </form>
        </PremiumPanel>
      </div>
    </main>
  );
}

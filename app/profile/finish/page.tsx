import { createClient } from '@/lib/supabase/server';
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
    <div className='flex flex-col items-center justify-center min-h-screen py-10'>
      <h1 className='text-4xl font-bold mb-2'>Finish Your Profile</h1>
      <p className='text-muted-foreground mb-8 text-center'>
        Review and complete your information
      </p>

      <form
        action={updateProfile}
        className='w-full max-w-lg space-y-4'
      >
        <div className='space-y-1'>
          <label className='text-sm font-medium'>Name</label>
          <input
            name='name'
            defaultValue={profileData.name ?? ''}
            className='w-full border rounded px-3 py-2'
          />
        </div>

        <div className='space-y-1'>
          <label className='text-sm font-medium'>Education Level</label>
          <input
            name='education_level'
            defaultValue={profileData.education_level ?? ''}
            className='w-full border rounded px-3 py-2'
          />
        </div>

        <div className='space-y-1'>
          <label className='text-sm font-medium'>Major</label>
          <input
            name='major'
            defaultValue={profileData.major ?? ''}
            className='w-full border rounded px-3 py-2'
          />
        </div>

        <div className='space-y-1'>
          <label className='text-sm font-medium'>Interests</label>
          <input
            name='interests'
            defaultValue={profileData.interests ?? ''}
            className='w-full border rounded px-3 py-2'
          />
        </div>

        <div className='space-y-1'>
          <label className='text-sm font-medium'>Resume Text</label>
          <textarea
            name='resume_text'
            defaultValue={profileData.resume_text ?? ''}
            className='w-full border rounded px-3 py-2 min-h-[150px]'
          />
        </div>

        <button
          type='submit'
          className='w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700'
        >
          Save Profile
        </button>
      </form>
    </div>
  );
}

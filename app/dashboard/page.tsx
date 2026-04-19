import { createClient } from '@/lib/supabase/server';
import { redirect } from 'next/navigation';

export default async function DashboardPage() {
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
    redirect('/profile/create');
  }

  return (
    <div className='container flex flex-col items-center gap-6 pt-6 pb-8 md:py-10'>
      <h1 className='text-3xl font-bold tracking-tight text-center'>
        Welcome to your Dashboard
      </h1>
      <p className='text-lg text-center text-muted-foreground'>
        This is where you can manage your account and view your activity.
      </p>
    </div>
  );
}

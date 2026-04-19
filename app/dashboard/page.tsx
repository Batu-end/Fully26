import { DashboardGrid } from '@/components/dashboard-components';
import { LogoutButton } from '@/components/logout-button';
import { createClient } from '@/lib/supabase/server';
import Link from 'next/link';
import { redirect } from 'next/navigation';
import { getPagedOpportunities } from './actions';

export default async function DashboardPage({searchParams} : {searchParams: Promise<{ [key: string]: string | string[] | undefined }>}) {
  const searchParamsResolved = await searchParams;
  console.log('Search params:', searchParamsResolved);
  const page = Number(searchParamsResolved.page) || 1;
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
  console.log('Profile data:', profileData);

  // if (error) {
  //   console.error('Error fetching profile:', error);
  //   redirect('/profile/create');
  // }

  const pagedOpportunities = await getPagedOpportunities(page);
  console.log('Paged opportunities:', pagedOpportunities);

  const dummyItems = [
  { id: '1', title: 'Opportunity 1', description: 'Description for opportunity 1' },
  { id: '2', title: 'Opportunity 2', description: 'Description for opportunity 2' },
  { id: '3', title: 'Opportunity 3', description: 'Description for opportunity 3' },
];

  return (
    <div className='flex flex-col items-center gap-6 pb-8 md:py-5'>
      <nav className='w-full flex items-center justify-between p-10 mb-4 border-b'>
        <div className='text-xl font-bold'>My Dashboard</div>
        <div className='flex items-center gap-4'>
          <Link href='/profile' className='text-sm text-primary hover:underline'>
            View Profile
          </Link>
          <LogoutButton/>
        </div>
      </nav>
      <h1 className='text-3xl font-bold tracking-tight text-center'>
        Welcome to your Dashboard
      </h1>
      <p className='text-lg text-center text-muted-foreground'>
        This is where you can manage your account and view your activity.
      </p>
      <DashboardGrid items={dummyItems} />
    </div>
  );
}

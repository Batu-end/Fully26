'use client';

import { useRouter } from 'next/navigation';

import { Button } from '@/components/ui/button';
import { createClient } from '@/lib/supabase/client';

export function LogoutButton() {
  const router = useRouter();

  const logout = async () => {
    const supabase = createClient();
    await supabase.auth.signOut();
    router.push('/auth/signin');
  };

  return (
    <Button
      onClick={logout}
      size='sm'
      variant='outline'
      className='text-white/78'
    >
      Logout
    </Button>
  );
}

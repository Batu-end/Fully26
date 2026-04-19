'use server';
import { signInWithGoogle } from './actions';

export default async function SignInPage() {
  return (
    <div className='min-h-screen flex items-center justify-center bg-gradient-to-b from-slate-950 via-blue-950 to-slate-900 text-white relative overflow-hidden'>
      {/* ambient glow */}
      <div className='absolute w-[500px] h-[500px] bg-blue-500/20 blur-[120px] rounded-full -z-10 top-1/4 left-1/2 -translate-x-1/2' />
      <div className='absolute w-[400px] h-[400px] bg-cyan-400/10 blur-[120px] rounded-full -z-10 bottom-0 right-0' />

      {/* card */}
      <div className='w-full max-w-md p-8 rounded-2xl border border-white/10 bg-white/5 backdrop-blur-md shadow-2xl'>
        <form
          action={signInWithGoogle}
          className='flex flex-col items-center gap-6'
        >
          {/* title */}
          <div className='text-center'>
            <h1 className='text-4xl font-bold tracking-tight'>Welcome</h1>
            <p className='text-blue-100/60 mt-2'>
              Dive into ocean opportunities tailored to you
            </p>
          </div>

          {/* button */}
          <button
            type='submit'
            className='w-full px-4 py-3 rounded-xl bg-cyan-400 text-slate-900 font-semibold hover:bg-cyan-300 transition shadow-lg shadow-cyan-400/20'
          >
            Sign in with Google
          </button>

          {/* small footer text */}
          <p className='text-xs text-blue-100/50 text-center'>
            By continuing, you agree to explore ocean-focused opportunities
          </p>
        </form>
      </div>
    </div>
  );
}

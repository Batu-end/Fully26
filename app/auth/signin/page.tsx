'use server';
import { signInWithGoogle } from "./actions";

export default async function SignInPage() {
    return (
      <div className='flex flex-col items-center justify-center min-h-screen py-2'>
        <form action={signInWithGoogle}>
          <h1 className='text-4xl font-bold mb-8'>Sign In</h1>
          <button
            type="submit"
            className='px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition'
          >
            Sign in with Google
          </button>
        </form>
      </div>
    );
}
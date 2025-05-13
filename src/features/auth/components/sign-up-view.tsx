import { cn } from '@/lib/utils';
import { SignUp as ClerkSignUpForm } from '@clerk/nextjs';
import Link from 'next/link';

interface SignUpViewPageProps {
  stars: number;
}

export default function SignUpViewPage({ stars }: SignUpViewPageProps) {
  return (
    <div className='relative h-screen flex-col items-center justify-center md:grid lg:max-w-none lg:grid-cols-2 lg:px-0'>
      <div className='bg-muted relative hidden h-full flex-col p-10 text-white lg:flex dark:border-r'>
        <div className='absolute inset-0 bg-zinc-900' />
        <div className='relative z-20 flex items-center text-lg font-medium'>
          <svg
            xmlns='http://www.w3.org/2000/svg'
            viewBox='0 0 24 24'
            fill='none'
            stroke='currentColor'
            strokeWidth='2'
            strokeLinecap='round'
            strokeLinejoin='round'
            className='mr-2 h-6 w-6'
          >
            <path d='M15 6v12a3 3 0 1 0 3-3H6a3 3 0 1 0 3 3V6a3 3 0 1 0-3 3h12a3 3 0 1 0-3-3' />
          </svg>
          Prime Technologies
        </div>
        <div className='relative z-20 mt-auto'>
          <blockquote className='space-y-2'>
            <p className='text-lg'>
              &ldquo;Join Prime Technologies and unlock a world of educational
              opportunities. Start your learning journey today.&rdquo;
            </p>
            <footer className='text-sm'>Prime Technologies Team</footer>
          </blockquote>
        </div>
      </div>
      <div className='lg:p-8'>
        <div className='mx-auto flex w-full flex-col justify-center space-y-6 sm:w-[350px]'>
          <div className='flex flex-col space-y-2 text-center'>
            <h1 className='text-2xl font-semibold tracking-tight'>
              Create your account
            </h1>
            <p className='text-muted-foreground text-sm'>
              Sign up to start your educational journey with Prime Technologies
            </p>
          </div>
          <ClerkSignUpForm />
          <p className='text-muted-foreground px-8 text-center text-sm'>
            Already have an account?{' '}
            <Link
              href='/auth/sign-in'
              className='hover:text-primary underline underline-offset-4'
            >
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}

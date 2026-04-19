import * as React from 'react';

import { cn } from '@/lib/utils';

export function PremiumPanel({
  className,
  children,
  tone = 'default',
}: {
  className?: string;
  children: React.ReactNode;
  tone?: 'default' | 'bright' | 'shadow';
}) {
  return (
    <div
      className={cn(
        'ocean-panel premium-panel relative overflow-hidden rounded-[2rem] border p-6 md:p-7',
        tone === 'bright' &&
          'border-cyan-300/28 bg-[linear-gradient(170deg,rgba(10,28,48,0.88),rgba(5,13,25,0.82)),radial-gradient(circle_at_18%_0%,rgba(114,244,255,0.16),transparent_34%),radial-gradient(circle_at_82%_12%,rgba(63,116,255,0.12),transparent_26%)] shadow-[0_28px_90px_rgba(0,6,18,0.56)]',
        tone === 'shadow' &&
          'border-white/8 bg-[linear-gradient(180deg,rgba(7,15,30,0.9),rgba(2,6,16,0.98))] shadow-[0_22px_72px_rgba(0,4,14,0.58)]',
        tone === 'default' &&
          'shadow-[0_22px_72px_rgba(0,4,14,0.46)]',
        className,
      )}
    >
      <div className='absolute inset-x-8 top-0 h-px bg-gradient-to-r from-transparent via-cyan-100/55 to-transparent' />
      <div className='absolute inset-x-10 bottom-0 h-px bg-gradient-to-r from-transparent via-white/10 to-transparent' />
      <div className='absolute left-6 top-6 h-28 w-28 rounded-full bg-cyan-300/8 blur-3xl' />
      <div className='absolute right-[-2rem] top-[-2rem] h-36 w-36 rounded-full bg-blue-400/10 blur-3xl' />
      <div className='premium-panel-rim absolute inset-[1px] rounded-[calc(2rem-1px)]' />
      <div className='relative z-10'>{children}</div>
    </div>
  );
}

export function PanelEyebrow({
  className,
  children,
}: {
  className?: string;
  children: React.ReactNode;
}) {
  return (
    <div
      className={cn(
        'ocean-eyebrow inline-flex items-center rounded-full border border-cyan-300/18 bg-cyan-300/10 px-3 py-1 text-[0.68rem] font-medium uppercase tracking-[0.28em] text-cyan-100/74 shadow-[inset_0_1px_0_rgba(255,255,255,0.08)]',
        className,
      )}
    >
      {children}
    </div>
  );
}

export function MetricChip({
  className,
  label,
  value,
}: {
  className?: string;
  label: string;
  value: string;
}) {
  return (
    <div
      className={cn(
        'rounded-[1.35rem] border border-white/10 bg-[linear-gradient(180deg,rgba(255,255,255,0.05),rgba(255,255,255,0.025))] px-4 py-3 shadow-[inset_0_1px_0_rgba(255,255,255,0.05)] backdrop-blur-xl',
        className,
      )}
    >
      <div className='text-[0.68rem] uppercase tracking-[0.22em] text-cyan-100/45'>
        {label}
      </div>
      <div className='mt-1 text-base font-medium text-white'>{value}</div>
    </div>
  );
}

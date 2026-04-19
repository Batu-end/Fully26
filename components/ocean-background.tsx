import { cn } from '@/lib/utils';

const plankton = [
  { left: '4%', top: '16%', size: 'h-1 w-1', delay: '0s', duration: '14s' },
  { left: '12%', top: '72%', size: 'h-1.5 w-1.5', delay: '2s', duration: '18s' },
  { left: '18%', top: '38%', size: 'h-1 w-1', delay: '4s', duration: '16s' },
  { left: '26%', top: '58%', size: 'h-2 w-2', delay: '1s', duration: '20s' },
  { left: '34%', top: '18%', size: 'h-1 w-1', delay: '3s', duration: '17s' },
  { left: '41%', top: '76%', size: 'h-1.5 w-1.5', delay: '5s', duration: '19s' },
  { left: '49%', top: '46%', size: 'h-1 w-1', delay: '2.5s', duration: '15s' },
  { left: '57%', top: '24%', size: 'h-2 w-2', delay: '6s', duration: '21s' },
  { left: '66%', top: '66%', size: 'h-1 w-1', delay: '1.5s', duration: '18s' },
  { left: '74%', top: '34%', size: 'h-1.5 w-1.5', delay: '4.5s', duration: '20s' },
  { left: '82%', top: '78%', size: 'h-1 w-1', delay: '7s', duration: '22s' },
  { left: '90%', top: '22%', size: 'h-2 w-2', delay: '3.5s', duration: '16s' },
];

export function OceanBackground({
  className,
  intensity = 'default',
}: {
  className?: string;
  intensity?: 'default' | 'hero';
}) {
  const isHero = intensity === 'hero';

  return (
    <div
      aria-hidden='true'
      className={cn(
        'pointer-events-none absolute inset-0 overflow-hidden',
        className,
      )}
    >
      <div className='absolute inset-0 bg-[radial-gradient(circle_at_20%_10%,rgba(82,226,255,0.12),transparent_28%),radial-gradient(circle_at_80%_20%,rgba(75,114,255,0.14),transparent_32%),radial-gradient(circle_at_50%_90%,rgba(14,184,166,0.1),transparent_28%)]' />
      <div className='ocean-grid absolute inset-0 opacity-35' />

      <div
        className={cn(
          'absolute left-[-8%] top-[8%] h-[18rem] w-[18rem] rounded-full bg-cyan-300/10 blur-3xl ocean-drift-slow',
          isHero && 'h-[24rem] w-[24rem] bg-cyan-300/14',
        )}
      />
      <div
        className={cn(
          'absolute right-[-10%] top-[24%] h-[22rem] w-[22rem] rounded-full bg-blue-500/12 blur-3xl ocean-drift-medium',
          isHero && 'h-[30rem] w-[30rem] bg-blue-500/16',
        )}
      />
      <div className='absolute bottom-[-18%] left-[18%] h-[22rem] w-[42rem] rounded-full bg-teal-400/8 blur-3xl ocean-drift-slow' />

      <div className='absolute left-[6%] top-[18%] h-40 w-56 rounded-[50%] bg-slate-950/55 blur-2xl ocean-ray-drift' />
      <div className='absolute right-[8%] top-[52%] h-32 w-64 rounded-[50%] bg-slate-950/45 blur-2xl ocean-ray-drift-reverse' />

      <div className='absolute left-[11%] top-[14%] ocean-jellyfish ocean-jellyfish-a'>
        <div className='ocean-jelly-cap' />
        <div className='ocean-jelly-tentacles' />
      </div>
      <div className='absolute right-[14%] top-[28%] ocean-jellyfish ocean-jellyfish-b'>
        <div className='ocean-jelly-cap ocean-jelly-cap-alt' />
        <div className='ocean-jelly-tentacles ocean-jelly-tentacles-alt' />
      </div>

      <div className='absolute left-[14%] top-[48%] h-10 w-24 rounded-[999px_999px_999px_999px/70%_70%_30%_30%] bg-slate-200/6 blur-[1px] ocean-fish-drift' />
      <div className='absolute left-[58%] top-[18%] h-8 w-20 rounded-[999px_999px_999px_999px/70%_70%_30%_30%] bg-slate-100/5 blur-[1px] ocean-fish-drift-delayed' />
      <div className='absolute right-[18%] top-[62%] h-12 w-28 rounded-[999px_999px_999px_999px/70%_70%_30%_30%] bg-slate-200/5 blur-[1px] ocean-fish-drift-slow' />

      <div className='absolute inset-x-0 bottom-0 h-56 bg-gradient-to-t from-[#020816] via-[#020816]/70 to-transparent' />

      {plankton.map((particle, index) => (
        <span
          key={`${particle.left}-${particle.top}-${index}`}
          className={cn(
            'absolute rounded-full bg-cyan-200/70 shadow-[0_0_18px_rgba(112,238,255,0.35)] ocean-plankton',
            particle.size,
          )}
          style={{
            left: particle.left,
            top: particle.top,
            animationDelay: particle.delay,
            animationDuration: particle.duration,
          }}
        />
      ))}
    </div>
  );
}

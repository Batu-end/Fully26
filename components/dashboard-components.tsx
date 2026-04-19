import { Aperture, ArrowRight, Radar, Waves } from 'lucide-react';
import Link from 'next/link';

export function DashboardItem({
  id,
  title,
  description,
}: {
  id: string;
  title: string;
  description: string;
}) {
  return (
    <Link href={`/opportunities/${id}`}>
      <div className='group premium-panel relative h-full overflow-hidden rounded-[1.85rem] border border-white/10 bg-[linear-gradient(180deg,rgba(7,19,37,0.86),rgba(4,10,20,0.94))] p-6 transition duration-500 hover:-translate-y-1.5 hover:border-cyan-200/25 hover:bg-[linear-gradient(180deg,rgba(9,23,42,0.92),rgba(4,10,20,0.98))]'>
        <div className='absolute inset-x-8 top-0 h-px bg-gradient-to-r from-transparent via-cyan-200/30 to-transparent' />
        <div className='absolute -right-10 top-5 h-32 w-32 rounded-full bg-cyan-300/10 blur-3xl transition duration-500 group-hover:bg-cyan-300/18' />
        <div className='absolute bottom-[-1.5rem] left-[-1.5rem] h-28 w-28 rounded-full bg-blue-500/10 blur-3xl' />

        <div className='relative z-10 flex h-full flex-col gap-5'>
          <div className='flex items-center justify-between gap-3'>
            <div className='hero-glow-ring flex h-11 w-11 items-center justify-center rounded-2xl border border-cyan-200/15 bg-cyan-300/10 text-cyan-100'>
              <Aperture className='h-5 w-5' />
            </div>
            <div className='inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/[0.04] px-3 py-1 text-[0.65rem] uppercase tracking-[0.26em] text-cyan-100/55'>
              <Radar className='h-3.5 w-3.5' />
              Ranked
            </div>
          </div>

          <div className='space-y-3'>
            <h3 className='text-xl font-semibold text-white transition group-hover:text-cyan-100'>
              {title}
            </h3>
            <p className='text-sm leading-7 text-blue-50/68'>{description}</p>
          </div>

          <div className='field-surface mt-auto rounded-[1.25rem] px-4 py-3'>
            <div className='flex items-center justify-between gap-3 text-sm text-cyan-100/72 transition group-hover:text-cyan-100'>
              <span className='inline-flex items-center gap-2'>
                <Waves className='h-4 w-4' />
                Open opportunity brief
              </span>
              <ArrowRight className='h-4 w-4 transition duration-300 group-hover:translate-x-1' />
            </div>
          </div>
        </div>
      </div>
    </Link>
  );
}

export function DashboardGrid({
  items,
}: {
  items: { id: string; title: string; description: string }[];
}) {
  return (
    <div className='grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-3'>
      {items.map((item, index) => (
        <div
          key={item.id}
          className='animate-fade-in'
          style={{
            animationDelay: `${index * 90}ms`,
            animationFillMode: 'both',
          }}
        >
          <DashboardItem
            id={item.id}
            title={item.title}
            description={item.description}
          />
        </div>
      ))}
    </div>
  );
}

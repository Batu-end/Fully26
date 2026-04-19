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
      <div className='group relative p-6 rounded-2xl border border-white/10 bg-white/5 backdrop-blur hover:bg-white/10 transition-all duration-300 overflow-hidden'>
        {/* glow effect on hover */}
        <div className='absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300 bg-gradient-to-br from-blue-500/10 to-cyan-400/10' />

        {/* content */}
        <div className='relative z-10 flex flex-col gap-3'>
          <h3 className='text-lg font-semibold text-white group-hover:text-cyan-300 transition'>
            {title}
          </h3>

          <p className='text-sm text-blue-100/70 leading-relaxed'>
            {description}
          </p>

          {/* subtle CTA hint */}
          <div className='text-xs text-cyan-300/70 mt-2 group-hover:text-cyan-200 transition'>
            View analysis →
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
    <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6'>
      {items.map((item, index) => (
        <div
          key={item.id}
          className='animate-fade-in'
          style={{
            animationDelay: `${index * 60}ms`,
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

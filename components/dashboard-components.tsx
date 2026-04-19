import Link from "next/link";

// dummy data 



export function DashboardItem({ id, title, description }: { id: string, title: string; description: string }) {
    return (
      <div className='bg-card text-card-foreground shadow-sm border rounded-lg p-6'>
        <Link href={`/opportunities/${id}`}>
          <h3 className='text-xl font-bold mb-2'>{title}</h3>
          <p className='text-muted-foreground'>{description}</p>
        </Link>
      </div>
    );

}

export function DashboardGrid({ items }: { items: { id: string, title: string; description: string }[] }) {
    return (
      <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6'>
        {items.map((item) => (
          <DashboardItem key={item.id} id={item.id} title={item.title} description={item.description} />
        ))}
      </div>
    );
}
import * as React from 'react';
import { Slot } from '@radix-ui/react-slot';
import { cva, type VariantProps } from 'class-variance-authority';

import { cn } from '@/lib/utils';

const buttonVariants = cva(
  'inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-full text-sm font-medium transition-all duration-300 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0',
  {
    variants: {
      variant: {
        default:
          'bg-cyan-300 text-slate-950 shadow-[0_16px_34px_rgba(99,245,255,0.2)] hover:bg-cyan-200 hover:shadow-[0_20px_44px_rgba(99,245,255,0.26)]',
        destructive:
          'bg-destructive text-destructive-foreground shadow-sm hover:bg-destructive/90',
        outline:
          'border border-white/12 bg-white/[0.04] text-white shadow-[inset_0_1px_0_rgba(255,255,255,0.04)] backdrop-blur-xl hover:border-cyan-200/28 hover:bg-white/[0.08] hover:text-white',
        secondary:
          'bg-secondary/85 text-secondary-foreground shadow-sm hover:bg-secondary/70',
        ghost:
          'text-white/76 hover:bg-white/[0.08] hover:text-white',
        link: 'text-cyan-100 underline-offset-4 hover:underline',
      },
      size: {
        default: 'h-10 px-5 py-2.5',
        sm: 'h-8 px-3.5 text-xs',
        lg: 'h-11 px-8 text-sm',
        icon: 'h-10 w-10',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  },
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : 'button';
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    );
  },
);
Button.displayName = 'Button';

export { Button, buttonVariants };

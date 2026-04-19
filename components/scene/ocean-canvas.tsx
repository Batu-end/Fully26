'use client';

import { Canvas } from '@react-three/fiber';
import { useReducedMotion } from 'framer-motion';
import { Suspense, useEffect, useState } from 'react';

import { cn } from '@/lib/utils';

import { AbyssScene, type AbyssSceneVariant } from './abyss-scene';

export function OceanCanvas({
  className,
  variant = 'hero',
}: {
  className?: string;
  variant?: AbyssSceneVariant;
}) {
  const prefersReducedMotion = useReducedMotion();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const overlayClassName =
    variant === 'landing'
      ? 'bg-[radial-gradient(circle_at_18%_14%,rgba(96,242,255,0.13),transparent_18%),radial-gradient(circle_at_84%_18%,rgba(111,125,255,0.16),transparent_18%),linear-gradient(180deg,rgba(2,6,17,0.12),rgba(2,6,17,0.42))]'
      : variant === 'dashboard'
        ? 'bg-[radial-gradient(circle_at_16%_12%,rgba(89,235,255,0.08),transparent_16%),radial-gradient(circle_at_80%_24%,rgba(76,128,255,0.12),transparent_16%),linear-gradient(180deg,rgba(2,6,17,0.22),rgba(2,6,17,0.56))]'
        : variant === 'profile'
          ? 'bg-[radial-gradient(circle_at_22%_14%,rgba(91,235,255,0.08),transparent_18%),radial-gradient(circle_at_78%_16%,rgba(86,116,255,0.1),transparent_18%),linear-gradient(180deg,rgba(2,6,17,0.18),rgba(2,6,17,0.5))]'
          : 'bg-[radial-gradient(circle_at_18%_12%,rgba(96,242,255,0.12),transparent_18%),radial-gradient(circle_at_88%_20%,rgba(86,116,255,0.14),transparent_18%),linear-gradient(180deg,rgba(2,6,17,0.16),rgba(2,6,17,0.48))]';

  return (
    <div
      aria-hidden='true'
      className={cn(
        'pointer-events-none absolute inset-0 overflow-hidden scene-fallback',
        className,
      )}
    >
      <div className='hero-noise' />

      {mounted ? (
        <Canvas
          className='!absolute inset-0'
          camera={{ fov: 42, near: 0.1, far: 100, position: [0, 0.15, 8.8] }}
          dpr={prefersReducedMotion ? [1, 1.15] : [1, 1.5]}
          gl={{ alpha: true, antialias: true, powerPreference: 'high-performance' }}
        >
          <Suspense fallback={null}>
            <AbyssScene
              reducedMotion={prefersReducedMotion}
              variant={variant}
            />
          </Suspense>
        </Canvas>
      ) : null}

      <div className={cn('absolute inset-0', overlayClassName)} />
    </div>
  );
}

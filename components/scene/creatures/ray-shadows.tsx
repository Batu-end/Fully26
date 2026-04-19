'use client';

import { useFrame } from '@react-three/fiber';
import { useMemo, useRef } from 'react';
import type { Group } from 'three';

import type { AbyssSceneVariant } from '../abyss-scene';

type ShadowConfig = {
  id: string;
  position: [number, number, number];
  scale: [number, number, number];
  speed: number;
  rotation: number;
};

function RayShadow({
  config,
  reducedMotion,
}: {
  config: ShadowConfig;
  reducedMotion: boolean;
}) {
  const ref = useRef<Group>(null);

  useFrame((state) => {
    const group = ref.current;
    if (!group) return;

    const t = state.clock.elapsedTime * config.speed;
    const xDrift = reducedMotion ? 0 : Math.sin(t) * 1.8;
    const yDrift = reducedMotion ? 0 : Math.cos(t * 0.6) * 0.32;
    const zDrift = reducedMotion ? 0 : Math.sin(t * 0.4) * 0.18;

    group.position.x = config.position[0] + xDrift;
    group.position.y = config.position[1] + yDrift;
    group.position.z = config.position[2] + zDrift;
    group.rotation.z = config.rotation + (reducedMotion ? 0 : Math.sin(t * 0.5) * 0.08);
  });

  return (
    <group
      ref={ref}
      position={config.position}
      rotation={[0.6, 0.02, config.rotation]}
      scale={config.scale}
    >
      <mesh>
        <circleGeometry args={[1.25, 40]} />
        <meshBasicMaterial
          color='#010408'
          opacity={0.12}
          transparent
        />
      </mesh>
      <mesh
        position={[0, -0.58, 0]}
        rotation={[0, 0, Math.PI]}
        scale={[0.4, 1.4, 0.4]}
      >
        <coneGeometry args={[0.25, 1.2, 18]} />
        <meshBasicMaterial
          color='#010408'
          opacity={0.12}
          transparent
        />
      </mesh>
    </group>
  );
}

export function RayShadows({
  reducedMotion,
  variant,
}: {
  reducedMotion: boolean;
  variant: AbyssSceneVariant;
}) {
  const shadows = useMemo<ShadowConfig[]>(() => {
    const scaleBoost = variant === 'hero' ? 1 : 0.88;

    return [
      {
        id: 'ray-a',
        position: [-2.8, 1.7, -8.5],
        scale: [2.8 * scaleBoost, 1.1 * scaleBoost, 1],
        speed: 0.06,
        rotation: -0.22,
      },
      {
        id: 'ray-b',
        position: [2.4, -0.6, -7.4],
        scale: [2.1 * scaleBoost, 0.92 * scaleBoost, 1],
        speed: 0.04,
        rotation: 0.28,
      },
    ];
  }, [variant]);

  return (
    <group>
      {shadows.map((config) => (
        <RayShadow
          key={config.id}
          config={config}
          reducedMotion={reducedMotion}
        />
      ))}
    </group>
  );
}

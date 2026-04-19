'use client';

import { useFrame } from '@react-three/fiber';
import { useMemo, useRef } from 'react';
import type { Group } from 'three';

import type { AbyssSceneVariant } from '../abyss-scene';

type SchoolConfig = {
  id: string;
  position: [number, number, number];
  scale: number;
  direction: 1 | -1;
  spread: number;
  speed: number;
  fishCount: number;
};

function FishCluster({
  config,
  reducedMotion,
}: {
  config: SchoolConfig;
  reducedMotion: boolean;
}) {
  const ref = useRef<Group>(null);

  useFrame((state) => {
    const group = ref.current;
    if (!group) return;

    const t = state.clock.elapsedTime * config.speed;
    const travel = reducedMotion ? 0 : Math.sin(t) * 1.6;
    const rise = reducedMotion ? 0 : Math.cos(t * 0.8) * 0.18;

    group.position.x = config.position[0] + travel * config.direction;
    group.position.y = config.position[1] + rise;
    group.rotation.y = config.direction === 1 ? 0 : Math.PI;
  });

  return (
    <group
      ref={ref}
      position={config.position}
      scale={config.scale}
    >
      {Array.from({ length: config.fishCount }).map((_, index) => {
        const offset = index / Math.max(config.fishCount - 1, 1);
        const x = -config.spread / 2 + config.spread * offset;
        const y = (index % 2 === 0 ? 1 : -1) * 0.12 * index;
        const z = -0.14 * index;

        return (
          <group
            key={`${config.id}-fish-${index}`}
            position={[x, y, z]}
            rotation={[0, 0, (index % 3 - 1) * 0.12]}
          >
            <mesh scale={[0.32, 0.1, 0.07]}>
              <sphereGeometry args={[1, 12, 10]} />
              <meshBasicMaterial
                color='#08121d'
                opacity={0.2}
                transparent
              />
            </mesh>
            <mesh
              position={[-0.32, 0, 0]}
              rotation={[0, 0, Math.PI / 2]}
              scale={[0.12, 0.18, 0.12]}
            >
              <coneGeometry args={[1, 1.4, 8]} />
              <meshBasicMaterial
                color='#0a1723'
                opacity={0.16}
                transparent
              />
            </mesh>
          </group>
        );
      })}
    </group>
  );
}

export function FishSchool({
  count,
  reducedMotion,
  variant,
}: {
  count: number;
  reducedMotion: boolean;
  variant: AbyssSceneVariant;
}) {
  const schools = useMemo<SchoolConfig[]>(() => {
    const base: SchoolConfig[] = [
      {
        id: 'school-a',
        position: [-3.4, 1.1, -5.4],
        scale: variant === 'hero' ? 1.12 : 0.95,
        direction: 1,
        spread: 2.2,
        speed: 0.14,
        fishCount: 8,
      },
      {
        id: 'school-b',
        position: [3.1, 0.2, -4.2],
        scale: 0.88,
        direction: -1,
        spread: 1.9,
        speed: 0.11,
        fishCount: 6,
      },
      {
        id: 'school-c',
        position: [-1.1, -1.35, -3.8],
        scale: 0.72,
        direction: 1,
        spread: 1.5,
        speed: 0.09,
        fishCount: 5,
      },
    ];

    return base.slice(0, count);
  }, [count, variant]);

  return (
    <group>
      {schools.map((config) => (
        <FishCluster
          key={config.id}
          config={config}
          reducedMotion={reducedMotion}
        />
      ))}
    </group>
  );
}

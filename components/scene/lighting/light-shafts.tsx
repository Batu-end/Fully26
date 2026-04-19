'use client';

import { useFrame } from '@react-three/fiber';
import { useMemo, useRef } from 'react';
import type { Group } from 'three';
import { AdditiveBlending, DoubleSide } from 'three';

import type { AbyssSceneVariant } from '../abyss-scene';

type ShaftConfig = {
  id: string;
  position: [number, number, number];
  rotation: [number, number, number];
  scale: [number, number, number];
  opacity: number;
  speed: number;
  color: string;
};

function LightShaft({
  config,
  reducedMotion,
}: {
  config: ShaftConfig;
  reducedMotion: boolean;
}) {
  const ref = useRef<Group>(null);

  useFrame((state) => {
    const group = ref.current;
    if (!group) return;

    const t = state.clock.elapsedTime * config.speed;
    group.position.x = config.position[0] + (reducedMotion ? 0 : Math.sin(t) * 0.22);
    group.position.y = config.position[1] + (reducedMotion ? 0 : Math.cos(t * 0.7) * 0.12);
    group.rotation.z = config.rotation[2] + (reducedMotion ? 0 : Math.sin(t * 0.5) * 0.04);
  });

  return (
    <group
      ref={ref}
      position={config.position}
      rotation={config.rotation}
      scale={config.scale}
    >
      <mesh>
        <planeGeometry args={[1, 9, 1, 1]} />
        <meshBasicMaterial
          blending={AdditiveBlending}
          color={config.color}
          depthWrite={false}
          opacity={config.opacity}
          side={DoubleSide}
          transparent
        />
      </mesh>
    </group>
  );
}

export function LightShafts({
  reducedMotion,
  variant,
}: {
  reducedMotion: boolean;
  variant: AbyssSceneVariant;
}) {
  const shafts = useMemo<ShaftConfig[]>(() => {
    const opacityBoost = variant === 'hero' ? 1 : 0.78;

    return [
      {
        id: 'shaft-a',
        position: [-2.4, 2.8, -6.2],
        rotation: [0.08, 0.1, -0.18],
        scale: [1.2, 1, 1],
        opacity: 0.07 * opacityBoost,
        speed: 0.12,
        color: '#8bf3ff',
      },
      {
        id: 'shaft-b',
        position: [0.5, 2.7, -5.6],
        rotation: [0.05, -0.02, 0.1],
        scale: [1.6, 1, 1],
        opacity: 0.05 * opacityBoost,
        speed: 0.1,
        color: '#67d8ff',
      },
      {
        id: 'shaft-c',
        position: [2.9, 2.5, -6.8],
        rotation: [0.07, -0.12, 0.22],
        scale: [1.15, 1, 1],
        opacity: 0.045 * opacityBoost,
        speed: 0.08,
        color: '#7fc8ff',
      },
    ];
  }, [variant]);

  return (
    <group>
      {shafts.map((config) => (
        <LightShaft
          key={config.id}
          config={config}
          reducedMotion={reducedMotion}
        />
      ))}

      <mesh
        position={[0, -1.2, -7.8]}
        rotation={[-Math.PI / 2.2, 0, 0]}
      >
        <planeGeometry args={[18, 12, 1, 1]} />
        <meshBasicMaterial
          color='#0b2235'
          opacity={0.22}
          transparent
        />
      </mesh>
    </group>
  );
}

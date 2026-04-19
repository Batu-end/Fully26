'use client';

import { useFrame } from '@react-three/fiber';
import { useMemo, useRef } from 'react';
import type { Group, Mesh } from 'three';

import type { AbyssSceneVariant } from '../abyss-scene';

type JellyConfig = {
  id: string;
  position: [number, number, number];
  scale: number;
  drift: number;
  hue: string;
  emissive: string;
};

function Jellyfish({
  config,
  reducedMotion,
}: {
  config: JellyConfig;
  reducedMotion: boolean;
}) {
  const groupRef = useRef<Group>(null);
  const capRef = useRef<Mesh>(null);

  useFrame((state) => {
    const group = groupRef.current;
    const cap = capRef.current;
    if (!group || !cap) return;

    const t = state.clock.elapsedTime + config.drift * 10;
    const driftY = reducedMotion ? 0 : Math.sin(t * 0.38) * 0.18;
    const driftX = reducedMotion ? 0 : Math.cos(t * 0.22) * 0.12;
    const pulse = reducedMotion ? 0.62 : 0.62 + (Math.sin(t * 0.8) + 1) * 0.16;

    group.position.x = config.position[0] + driftX;
    group.position.y = config.position[1] + driftY;
    group.rotation.z = reducedMotion ? 0.08 : Math.sin(t * 0.28) * 0.08;

    if ('emissiveIntensity' in cap.material) {
      cap.material.emissiveIntensity = pulse;
      cap.material.opacity = 0.56 + pulse * 0.12;
    }
  });

  return (
    <group
      ref={groupRef}
      position={config.position}
      scale={config.scale}
    >
      <mesh
        ref={capRef}
        position={[0, 0.1, 0]}
        scale={[1.05, 0.72, 1.05]}
      >
        <sphereGeometry args={[0.62, 24, 22]} />
        <meshStandardMaterial
          color={config.hue}
          emissive={config.emissive}
          emissiveIntensity={0.72}
          opacity={0.72}
          roughness={0.28}
          transparent
        />
      </mesh>

      <mesh position={[0, 0.06, 0]} scale={[0.46, 0.22, 0.46]}>
        <sphereGeometry args={[0.6, 18, 18]} />
        <meshBasicMaterial
          color='#dfffff'
          opacity={0.22}
          transparent
        />
      </mesh>

      {[-0.2, -0.08, 0.06, 0.18].map((x, index) => (
        <mesh
          key={`${config.id}-tentacle-${index}`}
          position={[x, -0.94 - index * 0.02, 0]}
          rotation={[0.08, 0, x * 0.5]}
          scale={[1, 1 + index * 0.06, 1]}
        >
          <cylinderGeometry args={[0.025, 0.045, 1.8, 8, 1, true]} />
          <meshStandardMaterial
            color={config.hue}
            emissive={config.emissive}
            emissiveIntensity={0.18}
            opacity={0.22}
            roughness={0.38}
            transparent
          />
        </mesh>
      ))}
    </group>
  );
}

export function JellyfishField({
  count,
  reducedMotion,
  variant,
}: {
  count: number;
  reducedMotion: boolean;
  variant: AbyssSceneVariant;
}) {
  const jellyfish = useMemo<JellyConfig[]>(() => {
    const base: JellyConfig[] = [
      {
        id: 'hero-jelly-1',
        position: [-2.9, 0.8, -1.4],
        scale: variant === 'hero' ? 0.9 : 0.74,
        drift: 0.3,
        hue: '#8ef8ff',
        emissive: '#58f3ff',
      },
      {
        id: 'hero-jelly-2',
        position: [2.35, -0.1, -0.8],
        scale: variant === 'hero' ? 0.72 : 0.64,
        drift: 0.58,
        hue: '#9ad5ff',
        emissive: '#7cd4ff',
      },
      {
        id: 'hero-jelly-3',
        position: [1.2, 1.35, -2.5],
        scale: 0.56,
        drift: 0.78,
        hue: '#83e6ff',
        emissive: '#56dfff',
      },
      {
        id: 'hero-jelly-4',
        position: [-0.6, -1.1, -1.9],
        scale: 0.46,
        drift: 0.94,
        hue: '#7fefff',
        emissive: '#4edaff',
      },
    ];

    return base.slice(0, count);
  }, [count, variant]);

  return (
    <group>
      {jellyfish.map((config) => (
        <Jellyfish
          key={config.id}
          config={config}
          reducedMotion={reducedMotion}
        />
      ))}
    </group>
  );
}

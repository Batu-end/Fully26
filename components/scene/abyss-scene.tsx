'use client';

import { useFrame } from '@react-three/fiber';
import { useRef } from 'react';
import type { Group } from 'three';

import { FishSchool } from './creatures/fish-school';
import { JellyfishField } from './creatures/jellyfish-field';
import { PlanktonField } from './creatures/plankton-field';
import { RayShadows } from './creatures/ray-shadows';
import { LightShafts } from './lighting/light-shafts';

export type AbyssSceneVariant =
  | 'hero'
  | 'landing'
  | 'dashboard'
  | 'profile'
  | 'ambient';

const sceneDepth = {
  hero: {
    fogNear: 9,
    fogFar: 24,
    cameraDrift: 0.22,
    jellyCount: 4,
    schoolCount: 3,
    particleCount: 130,
  },
  landing: {
    fogNear: 10,
    fogFar: 25,
    cameraDrift: 0.16,
    jellyCount: 3,
    schoolCount: 2,
    particleCount: 100,
  },
  dashboard: {
    fogNear: 10,
    fogFar: 26,
    cameraDrift: 0.14,
    jellyCount: 3,
    schoolCount: 3,
    particleCount: 96,
  },
  profile: {
    fogNear: 10,
    fogFar: 24,
    cameraDrift: 0.12,
    jellyCount: 2,
    schoolCount: 2,
    particleCount: 92,
  },
  ambient: {
    fogNear: 11,
    fogFar: 28,
    cameraDrift: 0.1,
    jellyCount: 2,
    schoolCount: 2,
    particleCount: 85,
  },
} as const;

function CameraDrift({
  reducedMotion,
  strength,
}: {
  reducedMotion: boolean;
  strength: number;
}) {
  const lookTarget = useRef<Group>(null);

  useFrame((state) => {
    const t = state.clock.elapsedTime;
    const x = reducedMotion ? 0 : Math.sin(t * 0.08) * strength;
    const y = reducedMotion ? 0.12 : 0.12 + Math.cos(t * 0.06) * strength * 0.55;

    state.camera.position.x += (x - state.camera.position.x) * 0.02;
    state.camera.position.y += (y - state.camera.position.y) * 0.02;
    state.camera.lookAt(0, 0, 0);

    if (lookTarget.current) {
      lookTarget.current.rotation.z = reducedMotion ? 0 : Math.sin(t * 0.04) * 0.02;
    }
  });

  return <group ref={lookTarget} />;
}

export function AbyssScene({
  variant = 'hero',
  reducedMotion = false,
}: {
  variant?: AbyssSceneVariant;
  reducedMotion?: boolean;
}) {
  const config = sceneDepth[variant];

  return (
    <>
      <color attach='background' args={['#020611']} />
      <fog attach='fog' args={['#04111f', config.fogNear, config.fogFar]} />

      <ambientLight intensity={0.38} color='#86eeff' />
      <directionalLight
        color='#9ff6ff'
        intensity={variant === 'dashboard' ? 0.74 : 0.85}
        position={[-3, 7, 6]}
      />
      <directionalLight
        color='#4b74ff'
        intensity={variant === 'profile' ? 0.34 : 0.45}
        position={[4, 2, 5]}
      />
      <pointLight
        color='#57edff'
        distance={18}
        intensity={5.5}
        position={[-2.5, 1.3, 4.8]}
      />
      <pointLight
        color='#5a7dff'
        distance={18}
        intensity={3.4}
        position={[3.4, -0.2, 3.8]}
      />

      <group position={[0, -0.2, 0]}>
        <LightShafts reducedMotion={reducedMotion} variant={variant} />
        <RayShadows reducedMotion={reducedMotion} variant={variant} />
        <FishSchool
          count={reducedMotion ? Math.max(1, config.schoolCount - 1) : config.schoolCount}
          reducedMotion={reducedMotion}
          variant={variant}
        />
        <JellyfishField
          count={reducedMotion ? Math.max(2, config.jellyCount - 1) : config.jellyCount}
          reducedMotion={reducedMotion}
          variant={variant}
        />
        <PlanktonField
          count={reducedMotion ? Math.floor(config.particleCount * 0.55) : config.particleCount}
          reducedMotion={reducedMotion}
        />
      </group>

      <CameraDrift
        reducedMotion={reducedMotion}
        strength={config.cameraDrift}
      />
    </>
  );
}

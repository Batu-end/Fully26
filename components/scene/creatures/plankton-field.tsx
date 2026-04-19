'use client';

import { useFrame } from '@react-three/fiber';
import { useMemo, useRef } from 'react';
import type { Points } from 'three';
import { Color } from 'three';

export function PlanktonField({
  count,
  reducedMotion,
}: {
  count: number;
  reducedMotion: boolean;
}) {
  const pointsRef = useRef<Points>(null);

  const { colors, positions } = useMemo(() => {
    const positionArray = new Float32Array(count * 3);
    const colorArray = new Float32Array(count * 3);

    for (let i = 0; i < count; i += 1) {
      const i3 = i * 3;
      const x = (Math.random() - 0.5) * 12;
      const y = (Math.random() - 0.5) * 7;
      const z = -Math.random() * 9 + 1.5;
      const tint = new Color().setHSL(0.52 + Math.random() * 0.06, 0.85, 0.68);

      positionArray[i3] = x;
      positionArray[i3 + 1] = y;
      positionArray[i3 + 2] = z;

      colorArray[i3] = tint.r;
      colorArray[i3 + 1] = tint.g;
      colorArray[i3 + 2] = tint.b;
    }

    return { colors: colorArray, positions: positionArray };
  }, [count]);

  useFrame((state) => {
    const points = pointsRef.current;
    if (!points) return;

    const t = state.clock.elapsedTime;
    points.rotation.y = reducedMotion ? 0.08 : 0.08 + t * 0.01;
    points.rotation.z = reducedMotion ? 0 : Math.sin(t * 0.04) * 0.03;
    points.position.y = reducedMotion ? 0 : Math.sin(t * 0.16) * 0.08;
  });

  return (
    <points ref={pointsRef}>
      <bufferGeometry>
        <bufferAttribute
          attach='attributes-position'
          array={positions}
          count={positions.length / 3}
          itemSize={3}
        />
        <bufferAttribute
          attach='attributes-color'
          array={colors}
          count={colors.length / 3}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial
        depthWrite={false}
        opacity={0.68}
        size={reducedMotion ? 0.028 : 0.034}
        sizeAttenuation
        transparent
        vertexColors
      />
    </points>
  );
}

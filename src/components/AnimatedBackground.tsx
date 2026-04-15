import { useCurrentFrame, useVideoConfig, interpolate } from 'remotion';
import { AbsoluteFill } from 'remotion';

export const AnimatedBackground: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  const time = frame / fps;

  return (
    <AbsoluteFill
      style={{
        overflow: 'hidden',
      }}
    >
      <div
        style={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          width: '200%',
          height: '200%',
          transform: `translate(-50%, -50%) rotate(${time * 5}deg)`,
          background: `
            radial-gradient(circle at 20% 30%, rgba(99, 102, 241, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 80% 70%, rgba(168, 85, 247, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 50% 50%, rgba(59, 130, 246, 0.1) 0%, transparent 70%)
          `,
        }}
      />

      {[...Array(20)].map((_, i) => {
        const x = (i * 137.5) % 100;
        const y = (i * 73.3) % 100;
        const size = 2 + (i % 4);
        const opacity = interpolate(
          frame,
          [0, fps * 2, fps * 4],
          [0.1, 0.6, 0.1],
          { extrapolateRight: 'clamp' }
        );

        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: `${x}%`,
              top: `${y}%`,
              width: size,
              height: size,
              borderRadius: '50%',
              backgroundColor: `rgba(255, 255, 255, ${opacity})`,
              boxShadow: `0 0 ${size * 2}px rgba(99, 102, 241, ${opacity})`,
            }}
          />
        );
      })}

      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'linear-gradient(180deg, rgba(10, 10, 15, 0.3) 0%, transparent 20%, transparent 80%, rgba(10, 10, 15, 0.5) 100%)',
        }}
      />

      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'linear-gradient(90deg, rgba(10, 10, 15, 0.2) 0%, transparent 10%, transparent 90%, rgba(10, 10, 15, 0.2) 100%)',
        }}
      />
    </AbsoluteFill>
  );
};

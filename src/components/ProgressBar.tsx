import { useCurrentFrame, useVideoConfig, interpolate } from 'remotion';
import { AbsoluteFill } from 'remotion';

interface ProgressBarProps {
  totalDuration: number;
}

export const ProgressBar: React.FC<ProgressBarProps> = ({ totalDuration }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = Math.min(frame / (totalDuration * fps), 1);
  const progressWidth = interpolate(progress, [0, 1], [0, 100]);

  return (
    <AbsoluteFill
      style={{
        bottom: 20,
        left: 0,
        right: 0,
        height: 6,
        backgroundColor: 'rgba(255, 255, 255, 0.1)',
      }}
    >
      <div
        style={{
          width: `${progressWidth}%`,
          height: '100%',
          background: 'linear-gradient(90deg, #6366f1, #a855f7)',
          boxShadow: '0 0 20px rgba(99, 102, 241, 0.5)',
        }}
      />
    </AbsoluteFill>
  );
};

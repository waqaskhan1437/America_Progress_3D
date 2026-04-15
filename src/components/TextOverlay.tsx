import { useCurrentFrame, useVideoConfig, interpolate, spring } from 'remotion';
import { AbsoluteFill } from 'remotion';
import { LottieAnimation } from './LottieAnimation';

interface TextOverlayProps {
  title: string;
  subtitle?: string;
  duration: number;
  showLottie?: boolean;
  lottieUrl?: string;
}

export const TextOverlay: React.FC<TextOverlayProps> = ({
  title,
  subtitle,
  duration,
  showLottie = false,
  lottieUrl,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleProgress = interpolate(frame, [0, 20, 30], [0, 1, 1], { extrapolateRight: 'clamp' });
  const subtitleProgress = interpolate(frame, [15, 35, 45], [0, 1, 1], { extrapolateRight: 'clamp' });
  const lottieProgress = interpolate(frame, [10, 40], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill
      style={{
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: '#0a0a0f',
      }}
    >
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: 30,
          opacity: titleProgress,
          transform: `translateY(${(1 - titleProgress) * 30}px)`,
        }}
      >
        {showLottie && lottieUrl && (
          <div style={{ opacity: lottieProgress, transform: `scale(${0.8 + lottieProgress * 0.2})` }}>
            <LottieAnimation url={lottieUrl} />
          </div>
        )}

        <h1
          style={{
            fontSize: 96,
            color: 'white',
            fontWeight: 800,
            textAlign: 'center',
            fontFamily: 'sans-serif',
            textShadow: '0 4px 30px rgba(99, 102, 241, 0.5)',
            letterSpacing: '-2px',
          }}
        >
          {title}
        </h1>

        {subtitle && (
          <p
            style={{
              fontSize: 32,
              color: '#a855f7',
              fontWeight: 500,
              opacity: subtitleProgress,
              fontFamily: 'sans-serif',
              letterSpacing: '4px',
              textTransform: 'uppercase',
            }}
          >
            {subtitle}
          </p>
        )}
      </div>

      <div
        style={{
          position: 'absolute',
          bottom: 100,
          display: 'flex',
          gap: 12,
        }}
      >
        {[0, 1, 2].map((i) => (
          <div
            key={i}
            style={{
              width: 12,
              height: 12,
              borderRadius: '50%',
              backgroundColor: i === 0 ? '#6366f1' : 'rgba(99, 102, 241, 0.3)',
            }}
          />
        ))}
      </div>
    </AbsoluteFill>
  );
};

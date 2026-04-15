import { useLottie } from 'lottie-react';
import { useEffect, useState } from 'react';

interface LottieAnimationProps {
  url: string;
  loop?: boolean;
  autoplay?: boolean;
  width?: number;
  height?: number;
}

export const LottieAnimation: React.FC<LottieAnimationProps> = ({
  url,
  loop = true,
  autoplay = true,
  width = 400,
  height = 400,
}) => {
  const [animationData, setAnimationData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    let mounted = true;

    fetch(url)
      .then((res) => res.json())
      .then((data) => {
        if (mounted) {
          setAnimationData(data);
          setLoading(false);
        }
      })
      .catch(() => {
        if (mounted) {
          setError(true);
          setLoading(false);
        }
      });

    return () => {
      mounted = false;
    };
  }, [url]);

  if (loading) {
    return (
      <div
        style={{
          width,
          height,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          backgroundColor: 'rgba(99, 102, 241, 0.1)',
          borderRadius: 20,
        }}
      >
        <div style={{ color: '#6366f1', fontSize: 18 }}>Loading...</div>
      </div>
    );
  }

  if (error || !animationData) {
    return (
      <div
        style={{
          width,
          height,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          backgroundColor: 'rgba(99, 102, 241, 0.2)',
          borderRadius: 20,
        }}
      >
        <span style={{ fontSize: Math.min(width, height) * 0.25 }}>🌍</span>
      </div>
    );
  }

  const options = {
    animationData,
    loop,
    autoplay,
  };

  const View = useLottie(options).View;

  return (
    <div style={{ width, height }}>
      {View}
    </div>
  );
};

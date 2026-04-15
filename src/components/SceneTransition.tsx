import { useCurrentFrame, interpolate, AbsoluteFill } from 'remotion'

export type TransitionType = 'fade' | 'slideLeft' | 'slideRight' | 'slideUp' | 'zoom' | 'crossDissolve'

interface SceneTransitionProps {
  children: React.ReactNode
  type: TransitionType
  durationFrames: number
  transitionFrames?: number
}

function getTransitionStyle(type: TransitionType, enter: number, exit: number): React.CSSProperties {
  const progress = Math.min(enter, exit)
  switch (type) {
    case 'fade':
      return { opacity: progress }
    case 'slideLeft':
      return {
        opacity: progress,
        transform: `translateX(${(1 - enter) * 100 + (1 - exit) * -100}px)`,
      }
    case 'slideRight':
      return {
        opacity: progress,
        transform: `translateX(${(enter - 1) * 100 + (exit - 1) * 100}px)`,
      }
    case 'slideUp':
      return {
        opacity: progress,
        transform: `translateY(${(1 - enter) * 80}px)`,
      }
    case 'zoom':
      return {
        opacity: progress,
        transform: `scale(${0.3 + enter * 0.7})`,
      }
    case 'crossDissolve':
      return {
        opacity: progress,
        filter: `blur(${(1 - progress) * 8}px)`,
      }
    default:
      return { opacity: progress }
  }
}

export const SceneTransition: React.FC<SceneTransitionProps> = ({
  children,
  type,
  durationFrames,
  transitionFrames = 30,
}) => {
  const frame = useCurrentFrame()

  const enterProgress = interpolate(frame, [0, transitionFrames], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  })

  const exitProgress = interpolate(
    frame,
    [Math.max(0, durationFrames - transitionFrames), durationFrames],
    [1, 0],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  )

  const style = getTransitionStyle(type, enterProgress, exitProgress)

  return <AbsoluteFill style={style}>{children}</AbsoluteFill>
}

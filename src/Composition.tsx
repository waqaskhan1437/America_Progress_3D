import {
  Composition,
  AbsoluteFill,
  Sequence,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
  delayRender,
  continueRender,
  Audio,
} from 'remotion'
import { LottieAnimation } from './components/LottieAnimation'
import { TextOverlay } from './components/TextOverlay'
import { AnimatedBackground } from './components/AnimatedBackground'
import { ProgressBar } from './components/ProgressBar'
import { SceneTransition, TransitionType } from './components/SceneTransition'
import { useEffect, useState } from 'react'

export interface LottieAsset {
  url: string
  label: string
  position: 'left' | 'right' | 'center' | 'background'
  enterAtSecond: number
  scale?: number
}

export interface SceneData {
  title: string
  description: string
  keywords: string[]
  lottieAnimations: LottieAsset[]
  transition?: TransitionType
  voiceUrl?: string // Added for TTS voiceover
}

export interface VideoScript {
  title: string
  scenes: SceneData[]
  duration: number
  targetDurationMinutes?: number
  bgMusicUrl?: string | null // Added for background music
}

interface VideoCompositionProps {
  scriptData?: string
}

const DEFAULT_LOTTIE = 'https://assets2.lottiefiles.com/packages/lf20_yvttable.json'

export const VideoComposition: React.FC<VideoCompositionProps> = ({ scriptData }) => {
  const [script, setScript] = useState<VideoScript | null>(null)
  const { fps, durationInFrames } = useVideoConfig()

  useEffect(() => {
    const handle = delayRender('Parsing video script...')

    if (scriptData) {
      try {
        const parsed = JSON.parse(scriptData)
        setScript(parsed)
      } catch {
        setScript(getDefaultScript())
      }
    } else {
      setScript(getDefaultScript())
    }

    continueRender(handle)
  }, [scriptData])

  if (!script) {
    return (
      <AbsoluteFill style={{ backgroundColor: '#000000', justifyContent: 'center', alignItems: 'center' }}>
        <div style={{ color: 'white', fontSize: 24, fontFamily: 'sans-serif' }}>Loading Experience...</div>
      </AbsoluteFill>
    )
  }

  const totalScenes = script.scenes.length
  const sceneDurationFrames = Math.floor(durationInFrames / (totalScenes + 2)) // +2 for intro and outro
  const introDuration = sceneDurationFrames
  const outroDuration = sceneDurationFrames

  return (
    <AbsoluteFill style={{ backgroundColor: '#000000' }}>
      <AnimatedBackground />

      {/* Global Background Music */}
      {script.bgMusicUrl && (
        <Audio src={script.bgMusicUrl} volume={0.15} />
      )}

      {/* Intro */}
      <Sequence from={0} durationInFrames={introDuration} name="Intro">
        <SceneTransition type="fade" durationFrames={introDuration}>
          <TextOverlay
            title={script.title}
            duration={introDuration / fps}
            showLottie={true}
            lottieUrl={script.scenes[0]?.lottieAnimations?.[0]?.url || DEFAULT_LOTTIE}
          />
        </SceneTransition>
      </Sequence>

      {/* Scenes */}
      {script.scenes.map((scene, index) => {
        const from = introDuration + index * sceneDurationFrames
        return (
          <Sequence
            key={index}
            from={from}
            durationInFrames={sceneDurationFrames}
            name={`Scene ${index + 1}: ${scene.title}`}
          >
            {/* Scene Voiceover */}
            {scene.voiceUrl && (
              <Audio src={scene.voiceUrl} />
            )}
            
            <SceneCard
              scene={scene}
              durationFrames={sceneDurationFrames}
              sceneIndex={index}
              totalScenes={totalScenes}
            />
          </Sequence>
        )
      })}

      {/* Outro */}
      <Sequence
        from={introDuration + totalScenes * sceneDurationFrames}
        durationInFrames={outroDuration}
        name="Outro"
      >
        <SceneTransition type="zoom" durationFrames={outroDuration}>
          <Outro />
        </SceneTransition>
      </Sequence>

      <ProgressBar totalDuration={durationInFrames / fps} />
    </AbsoluteFill>
  )
}

interface SceneCardProps {
  scene: SceneData
  durationFrames: number
  sceneIndex: number
  totalScenes: number
}

const POSITION_STYLES: Record<string, (idx: number) => React.CSSProperties> = {
  left: () => ({ position: 'absolute', left: '10%', top: '20%', width: 500, height: 500 }),
  right: () => ({ position: 'absolute', right: '10%', top: '20%', width: 500, height: 500 }),
  center: () => ({ position: 'absolute', left: '50%', top: '50%', transform: 'translate(-50%, -50%)', width: 600, height: 600 }),
  background: () => ({ position: 'absolute', left: '50%', top: '50%', transform: 'translate(-50%, -50%)', width: 1000, height: 1000, opacity: 0.1 }),
}

const SceneCard: React.FC<SceneCardProps> = ({ scene, durationFrames, sceneIndex, totalScenes }) => {
  const frame = useCurrentFrame()
  const { fps } = useVideoConfig()
  const transition = scene.transition || (['fade', 'slideLeft', 'slideUp', 'zoom', 'crossDissolve'] as TransitionType[])[sceneIndex % 5]

  // Sleek Entrance Animations for Text
  const textSpring = spring({ frame: frame - 10, fps, config: { damping: 14, stiffness: 60 } })
  const descSpring = spring({ frame: frame - 25, fps, config: { damping: 14, stiffness: 60 } })

  return (
    <SceneTransition type={transition} durationFrames={durationFrames}>
      <AbsoluteFill style={{ padding: 80 }}>

        {/* Smooth Glassmorphism Container setup depending on lottie positions */}
        <div style={{
          position: 'absolute',
          top: 0, left: 0, right: 0, bottom: 0,
          display: 'flex',
          flexDirection: 'row',
          alignItems: 'center',
          justifyContent: 'center',
          gap: 60,
          padding: 80,
        }}>

          {/* Left Side: Animations (if any positioned left or default) */}
          <div style={{ flex: 1, position: 'relative', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            {scene.lottieAnimations?.map((asset, i) => {
              const enterFrame = asset.enterAtSecond * fps
              const assetSpring = spring({ frame: frame - enterFrame, fps, config: { damping: 12, stiffness: 80 } })
              if (frame < enterFrame) return null

              const size = (asset.scale || 1) * 600

              return (
                <div key={`anim-${i}`} style={{
                  position: 'absolute',
                  width: size,
                  height: size,
                  opacity: assetSpring,
                  transform: `scale(${0.9 + assetSpring * 0.1}) translateY(${(1 - assetSpring) * 20}px)`,
                  filter: `drop-shadow(0px 20px 40px rgba(0,0,0,0.5))`
                }}>
                  <LottieAnimation url={asset.url} />
                </div>
              )
            })}
            
            {/* Fallback if no animations */}
            {(!scene.lottieAnimations || scene.lottieAnimations.length === 0) && (
              <div style={{ width: 600, height: 600, opacity: textSpring, transform: `scale(${0.9 + textSpring * 0.1})` }}>
                <LottieAnimation url={DEFAULT_LOTTIE} />
              </div>
            )}
          </div>

          {/* Right Side: Professional Typography */}
          <div style={{ 
            flex: 1, 
            display: 'flex', 
            flexDirection: 'column', 
            justifyContent: 'center',
            background: 'linear-gradient(135deg, rgba(255,255,255,0.03) 0%, rgba(255,255,255,0.01) 100%)',
            border: '1px solid rgba(255,255,255,0.05)',
            backdropFilter: 'blur(20px)',
            padding: '60px',
            borderRadius: '30px',
            opacity: textSpring,
            transform: `translateX(${(1 - textSpring) * 100}px)`
          }}>
            <div style={{
              fontSize: 20,
              color: '#818cf8',
              fontWeight: 600,
              marginBottom: 16,
              fontFamily: 'Inter, system-ui, sans-serif',
              letterSpacing: '0.2em',
              textTransform: 'uppercase',
            }}>
              0{sceneIndex + 1} // {totalScenes}
            </div>

            <h3 style={{
              fontSize: 64,
              color: '#ffffff',
              fontWeight: 700,
              marginBottom: 24,
              fontFamily: 'Inter, system-ui, sans-serif',
              lineHeight: 1.1,
              letterSpacing: '-0.02em',
            }}>
              {scene.title}
            </h3>

            <p style={{
              fontSize: 32,
              color: 'rgba(255,255,255,0.7)',
              lineHeight: 1.5,
              fontFamily: 'Inter, system-ui, sans-serif',
              fontWeight: 400,
              opacity: descSpring,
              transform: `translateY(${(1 - descSpring) * 20}px)`
            }}>
              {scene.description}
            </p>
          </div>

        </div>
      </AbsoluteFill>
    </SceneTransition>
  )
}

const Outro: React.FC = () => {
  const frame = useCurrentFrame()
  const { fps } = useVideoConfig()
  const progress = spring({ frame: frame - 15, fps, config: { damping: 15, stiffness: 80 } })

  return (
    <AbsoluteFill style={{
      justifyContent: 'center',
      alignItems: 'center',
      backgroundColor: '#000000',
    }}>
      <div style={{ 
        opacity: progress, 
        transform: `scale(${0.9 + progress * 0.1}) translateY(${(1-progress)*40}px)`,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center'
      }}>
        <div style={{ width: 400, height: 400 }}>
          <LottieAnimation url="https://assets1.lottiefiles.com/packages/lf20_lk80fpsm.json" />
        </div>

        <h2 style={{
          fontSize: 84,
          color: 'white',
          fontWeight: 800,
          marginTop: -20,
          fontFamily: 'Inter, system-ui, sans-serif',
          letterSpacing: '-0.03em',
        }}>
          Get Started Today.
        </h2>
      </div>
    </AbsoluteFill>
  )
}

function getDefaultScript(): VideoScript {
  return {
    title: 'The Future of Connection',
    scenes: [
      {
        title: 'Seamless Workflows',
        description: 'Empower your teams to build faster and collaborate seamlessly anywhere in the world.',
        keywords: ['workflow', 'team'],
        lottieAnimations: [
          { url: 'https://assets2.lottiefiles.com/packages/lf20_yvttable.json', label: 'rocket', position: 'left', enterAtSecond: 0, scale: 1 },
        ],
        transition: 'slideLeft',
      },
      {
        title: 'Global Scale',
        description: 'Reach millions instantly with infrastructure designed for incredible performance.',
        keywords: ['globe', 'scale'],
        lottieAnimations: [
          { url: 'https://assets10.lottiefiles.com/packages/lf20_g5rd6c.json', label: 'globe', position: 'left', enterAtSecond: 0, scale: 1 },
        ],
        transition: 'zoom',
      },
    ],
    duration: 15,
    targetDurationMinutes: 0.25,
  }
}

export const RemotionVideo: React.FC<{ scriptData?: string }> = ({ scriptData }) => {
  let durationInFrames = 900
  if (scriptData) {
    try {
      const parsed = JSON.parse(scriptData)
      durationInFrames = Math.max(300, (parsed.duration || 30) * 30)
    } catch {}
  }

  return (
    <Composition
      id="VideoComposition"
      component={VideoComposition}
      durationInFrames={durationInFrames}
      fps={30}
      width={1920}
      height={1080}
      defaultProps={{ scriptData: undefined }}
    />
  )
}

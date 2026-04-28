import { useEffect, useRef } from 'react'

function LoadingRitualScene() {
  const audioRef = useRef(null)

  useEffect(() => {
    if (audioRef.current) {
      audioRef.current.volume = 0.5 // Subtle background volume
      audioRef.current.play().catch((e) => console.log("Auto-play prevented", e))
    }
  }, [])

  return (
    <section className="scene loading-scene">
      <audio ref={audioRef} src="/ambient3.wav" loop />

      <p className="eyebrow">The Door Is Listening</p>

      <h1>A threshold is forming from what you could no longer carry.</h1>

      <p className="scene-text">
        Your words are not being processed like data. They are being held like
        weight. The ritual is shaping a door from the thing you finally named.
      </p>

      <div className="ritual-loading-card">
        <div className="threshold-line" />

        <div className="loading-steps">
          <span>Your words have reached the threshold.</span>
          <span>The weight is finding a shape.</span>
          <span>A door is gathering around what you named.</span>
          <span>A voice is preparing to meet you gently.</span>
        </div>

        <div className="loader" />
      </div>
    </section>
  )
}

export default LoadingRitualScene

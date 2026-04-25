function LoadingRitualScene() {
  return (
    <section className="scene loading-scene">
      <p className="eyebrow">The Door Is Listening</p>

      <h1>Your badge is being carried to the threshold.</h1>

      <p className="scene-text">
        The ritual is gathering your words, their weight, and the echo behind
        them. A door is forming from what you are ready to leave behind.
      </p>

      <div className="ritual-loading-card">
        <div className="threshold-line" />

        <div className="loading-steps">
          <span>Naming the badge</span>
          <span>Listening for the echo</span>
          <span>Shaping the door</span>
          <span>Preparing the voice</span>
        </div>

        <div className="loader" />
      </div>
    </section>
  )
}

export default LoadingRitualScene


function ThresholdScene({ onBegin }) {
  return (
    <section className="scene">
      <p className="eyebrow">The Badge Ritual</p>

      <h1>Before you knock, name what you can no longer carry.</h1>

      <p className="scene-text">
        You are standing before a door. Not every burden is meant to cross the
        threshold with you.
      </p>

      <button onClick={onBegin}>Begin the Ritual</button>
    </section>
  )
}

export default ThresholdScene

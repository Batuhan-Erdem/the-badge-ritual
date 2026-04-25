function ResultDoorScene({ badge, result, onRestart }) {
  return (
    <section className="scene result-scene">
      <p className="eyebrow">Release</p>

      <h1>{result.badgeTitle}</h1>

      <div className="door-artwork-frame">
        {result.imageUrl ? (
          <img
            src={result.imageUrl}
            alt="AI generated symbolic door artwork"
            className="door-artwork"
          />
        ) : (
          <div className="door-placeholder">
            <span>Symbolic Door Artwork</span>
          </div>
        )}
      </div>

      <div className="result-block">
        <h2>Your Badge</h2>
        <p>{badge}</p>
      </div>

      <div className="result-block">
        <h2>Historical Echo</h2>
        <p>{result.historicalEcho}</p>
      </div>

      <div className="result-block">
        <h2>Release Text</h2>
        <p>{result.releaseText}</p>
      </div>

      <button onClick={onRestart}>Leave Another Badge</button>
    </section>
  )
}

export default ResultDoorScene

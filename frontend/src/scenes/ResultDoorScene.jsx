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

      {result.audioUrl && (
        <div className="audio-block">
          <h2>Voice Narration</h2>
          <p>
            Listen to the ritual text as a quiet spoken narration before leaving
            the badge.
          </p>

          <audio controls src={result.audioUrl}>
            Your browser does not support the audio element.
          </audio>
        </div>
      )}

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


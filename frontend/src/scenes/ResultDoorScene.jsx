import { useState } from 'react'

function ResultDoorScene({ badge, result, onRestart }) {
  const [isReleased, setIsReleased] = useState(false)

  return (
    <section className={`scene result-scene ${isReleased ? 'released' : ''}`}>
      <p className="eyebrow">{isReleased ? 'The Badge Is Left' : 'Release'}</p>

      <h1>{isReleased ? 'You may knock now.' : result.badgeTitle}</h1>

      <div className="result-layout">
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

          {isReleased && (
            <div className="release-overlay">
              <p>
                Not because everything is finished,
                <br />
                but because you are no longer carrying it in the same way.
              </p>
            </div>
          )}
        </div>

        <div className="ritual-output-panel">
          {result.audioUrl && !isReleased && (
            <div className="audio-block">
              <h2>Voice Narration</h2>
              <p>
                Listen to the ritual text as a quiet spoken narration before
                leaving the badge.
              </p>

              <audio controls src={result.audioUrl}>
                Your browser does not support the audio element.
              </audio>
            </div>
          )}

          <div
            className={`result-block badge-block ${
              isReleased ? 'badge-faded' : ''
            }`}
          >
            <h2>Your Badge</h2>
            <p>{badge}</p>
          </div>

          {!isReleased && (
            <>
              <div className="result-block">
                <h2>Historical Echo</h2>
                <p>{result.historicalEcho}</p>
              </div>

              <div className="result-block">
                <h2>Release Text</h2>
                <p>{result.releaseText}</p>
              </div>

              <button onClick={() => setIsReleased(true)}>
                Leave the Badge
              </button>
            </>
          )}

          {isReleased && (
            <div className="final-release-block">
              <p>
                The door does not promise an answer. It only marks the moment
                when you decided that this weight would not cross the threshold
                with you.
              </p>

              <button onClick={onRestart}>Begin Another Ritual</button>
            </div>
          )}
        </div>
      </div>
    </section>
  )
}

export default ResultDoorScene

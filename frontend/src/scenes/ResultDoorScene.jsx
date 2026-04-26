import { useRef, useState } from 'react'
import './ResultDoorScene.css'
import {
  startAmbientSoundscape,
  stopAmbientSoundscape,
} from '../services/ambientSoundscape'

const fallbackGuidance = {
  en: {
    door:
      'This door was shaped from the weight you named. It is not here to judge you; it is here to mark the threshold.',
    badge:
      'Some burdens are not meant to cross the threshold with you. If you are ready, place the badge before the door.',
    afterBadge:
      'The badge has been set down. It has not vanished, but it no longer rests in your hands.',
    knock:
      'Now that the weight is no longer in your hands, you may ask the door to answer. When you are ready, knock twice.',
    response:
      'The door has answered by opening only a little. It does not reveal everything; it only shows that you arrived lighter.',
  },
  tr: {
    door:
      'Bu kapı, adını koyduğun yükten şekillendi. Seni yargılamak için değil, eşiği göstermek için burada.',
    badge:
      'Bazı yükler seninle birlikte eşikten geçmek için değildir. Hazırsan rozeti kapının önüne bırak.',
    afterBadge:
      'Rozet artık yere bırakıldı. Yok olmadı; ama artık ellerinde durmuyor.',
    knock:
      'Yük artık ellerinde değil. Şimdi kapıya ses verebilirsin. Hazırsan iki kez vur ve eşiğin cevabını dinle.',
    response:
      'Kapı yalnızca biraz aralanarak cevap verdi. Her şeyi göstermiyor; sadece artık daha hafif geldiğini söylüyor.',
  },
}

const uiText = {
  en: {
    ritualThreshold: 'The Ritual Threshold',
    doorAnswered: 'The Door Has Answered',
    youMayKnock: 'You may knock now.',
    ritualGuidance: 'Ritual Guidance',
    voiceNarration: 'Voice Narration',
    voiceNarrationDescription:
      'Listen to the ritual text as a quiet spoken narration before approaching the threshold.',
    ambientNote:
      'A very soft instrumental atmosphere will rise under the voice while it plays.',
    playNarration: 'Play Narration',
    pauseNarration: 'Pause Narration',
    yourBadge: 'Your Badge',
    doorCharacter: 'Door Character',
    historicalEcho: 'Historical Echo',
    releaseText: 'Release Text',
    continueToThreshold: 'Continue to the Threshold',
    placeBadge: 'Place the Badge Before the Door',
    approachKnocker: 'Approach the Knocker',
    firstKnock: 'First knock',
    secondKnock: 'Second knock',
    theKnocker: 'The Knocker',
    knockerDescription:
      'The badge is no longer in your hands. Knock twice, not to force the door open, but to ask the threshold to answer.',
    knocksHeard: 'Knocks heard',
    finalRelease:
      'The door does not promise an answer. It only marks the moment when you decided that this weight would not cross the threshold with you.',
    beginAnother: 'Begin Another Ritual',
    overlayLineOne: 'Not because everything is finished,',
    overlayLineTwo: 'but because you are no longer carrying it in the same way.',
  },
  tr: {
    ritualThreshold: 'Ritüel Eşiği',
    doorAnswered: 'Kapı Cevap Verdi',
    youMayKnock: 'Artık kapıyı çalabilirsin.',
    ritualGuidance: 'Ritüel Rehberliği',
    voiceNarration: 'Sesli Anlatı',
    voiceNarrationDescription:
      'Eşiğe yaklaşmadan önce ritüel metnini sakin bir sesli anlatı olarak dinleyebilirsin.',
    ambientNote:
      'Ses çalarken arka planda çok hafif, sözsüz bir atmosfer yükselecek.',
    playNarration: 'Anlatıyı Başlat',
    pauseNarration: 'Anlatıyı Durdur',
    yourBadge: 'Rozetin',
    doorCharacter: 'Kapının Karakteri',
    historicalEcho: 'Tarihsel Yankı',
    releaseText: 'Bırakma Metni',
    continueToThreshold: 'Eşiğe Doğru İlerle',
    placeBadge: 'Rozeti Kapının Önüne Bırak',
    approachKnocker: 'Tokmağa Yaklaş',
    firstKnock: 'İlk vuruş',
    secondKnock: 'İkinci vuruş',
    theKnocker: 'Kapı Tokmağı',
    knockerDescription:
      'Rozet artık ellerinde değil. Kapıyı zorla açmak için değil, eşiğin cevap vermesini istemek için iki kez vur.',
    knocksHeard: 'Duyulan vuruş',
    finalRelease:
      'Kapı sana kesin bir cevap vaat etmiyor. Sadece bu yükün artık seninle birlikte eşikten geçmeyeceğine karar verdiğin anı işaretliyor.',
    beginAnother: 'Yeni Bir Ritüele Başla',
    overlayLineOne: 'Her şey bittiği için değil,',
    overlayLineTwo: 'artık onu aynı şekilde taşımadığın için.',
  },
}

function detectLanguage(text) {
  const normalized = text.toLowerCase()

  const turkishCharacters = /[çğıöşü]/i
  const turkishWords = [
    'ben',
    'bana',
    'beni',
    'insan',
    'korku',
    'taşıyorum',
    'rozeti',
    'kapı',
    'yük',
    'çünkü',
    'değil',
    'özgürlük',
  ]

  if (turkishCharacters.test(normalized)) return 'tr'
  if (turkishWords.some((word) => normalized.includes(word))) return 'tr'

  return 'en'
}

function formatTime(seconds) {
  if (!Number.isFinite(seconds)) return '0:00'

  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
    .toString()
    .padStart(2, '0')

  return `${mins}:${secs}`
}

function playKnockSound(doorMaterial, knockNumber) {
  const AudioContext = window.AudioContext || window.webkitAudioContext
  if (!AudioContext) return

  const audioContext = new AudioContext()
  const now = audioContext.currentTime

  const materialSettings = {
    old_wood: {
      frequency: 180,
      duration: 0.13,
      gain: 0.28,
      type: 'triangle',
      filter: 900,
    },
    heavy_wood: {
      frequency: 135,
      duration: 0.16,
      gain: 0.34,
      type: 'triangle',
      filter: 700,
    },
    rusted_metal: {
      frequency: 420,
      duration: 0.2,
      gain: 0.24,
      type: 'square',
      filter: 1600,
    },
    dark_iron: {
      frequency: 95,
      duration: 0.24,
      gain: 0.38,
      type: 'sawtooth',
      filter: 520,
    },
    fragile_wood: {
      frequency: 240,
      duration: 0.1,
      gain: 0.18,
      type: 'triangle',
      filter: 1200,
    },
  }

  const settings = materialSettings[doorMaterial] || materialSettings.old_wood
  const frequencyOffset = knockNumber === 2 ? 0.88 : 1

  const oscillator = audioContext.createOscillator()
  const gainNode = audioContext.createGain()
  const filter = audioContext.createBiquadFilter()

  oscillator.type = settings.type
  oscillator.frequency.setValueAtTime(
    settings.frequency * frequencyOffset,
    now
  )

  filter.type = 'lowpass'
  filter.frequency.setValueAtTime(settings.filter, now)

  gainNode.gain.setValueAtTime(settings.gain, now)
  gainNode.gain.exponentialRampToValueAtTime(0.001, now + settings.duration)

  oscillator.connect(filter)
  filter.connect(gainNode)
  gainNode.connect(audioContext.destination)

  oscillator.start(now)
  oscillator.stop(now + settings.duration)
}

const doorMaterialLabels = {
  en: {
    old_wood: 'Old wooden threshold',
    heavy_wood: 'Heavy wooden threshold',
    rusted_metal: 'Rusted metal threshold',
    dark_iron: 'Dark iron threshold',
    fragile_wood: 'Fragile wooden threshold',
  },
  tr: {
    old_wood: 'Eski ahşap eşik',
    heavy_wood: 'Ağır ahşap eşik',
    rusted_metal: 'Paslı metal eşik',
    dark_iron: 'Koyu demir eşik',
    fragile_wood: 'Kırılgan ahşap eşik',
  },
}

function ResultDoorScene({ badge, result, onRestart }) {
  const audioRef = useRef(null)

  const [ritualStep, setRitualStep] = useState('door')
  const [knockCount, setKnockCount] = useState(0)
  const [isKnocking, setIsKnocking] = useState(false)
  const [isNarrationPlaying, setIsNarrationPlaying] = useState(false)
  const [audioCurrentTime, setAudioCurrentTime] = useState(0)
  const [audioDuration, setAudioDuration] = useState(0)

  const language = detectLanguage(
    `${badge} ${result?.historicalEcho || ''} ${result?.releaseText || ''}`
  )

  const text = uiText[language]
  const fallback = fallbackGuidance[language]
  const doorMaterial = result?.doorMaterial || 'old_wood'

  const isBadgePlaced =
    ritualStep === 'afterBadge' ||
    ritualStep === 'knock' ||
    ritualStep === 'doorResponse'

  const isDoorResponded = ritualStep === 'doorResponse'

  const guidanceByStep = {
    door: result?.doorGuidance || fallback.door,
    badge: result?.badgePlacementGuidance || fallback.badge,
    afterBadge: result?.afterBadgeGuidance || fallback.afterBadge,
    knock: result?.knockGuidance || fallback.knock,
    doorResponse: result?.doorResponseGuidance || fallback.response,
  }

  const progress =
    audioDuration > 0 ? Math.min((audioCurrentTime / audioDuration) * 100, 100) : 0

  function stopNarrationAndAmbient() {
    if (audioRef.current) {
      audioRef.current.pause()
    }

    setIsNarrationPlaying(false)
    stopAmbientSoundscape()
  }

  async function toggleNarration() {
    if (!audioRef.current) return

    if (isNarrationPlaying) {
      stopNarrationAndAmbient()
      return
    }

    await startAmbientSoundscape(doorMaterial)
    await audioRef.current.play()
    setIsNarrationPlaying(true)
  }

  function goToBadgePlacement() {
    stopNarrationAndAmbient()
    setRitualStep('badge')
  }

  function placeBadge() {
    setRitualStep('afterBadge')
  }

  function approachKnocker() {
    setRitualStep('knock')
    setKnockCount(0)
  }

  function handleKnock() {
    if (ritualStep !== 'knock') return

    const nextCount = knockCount + 1

    playKnockSound(doorMaterial, nextCount)
    setIsKnocking(true)

    setTimeout(() => {
      setIsKnocking(false)
    }, 260)

    setKnockCount(nextCount)

    if (nextCount >= 2) {
      setTimeout(() => {
        setRitualStep('doorResponse')
      }, 520)
    }
  }

  function handleRestart() {
    stopNarrationAndAmbient()
    onRestart()
  }

  return (
    <section className={`scene result-scene ${isDoorResponded ? 'released' : ''}`}>
      <p className="eyebrow">
        {isDoorResponded ? text.doorAnswered : text.ritualThreshold}
      </p>

      <h1>{isDoorResponded ? text.youMayKnock : result?.badgeTitle}</h1>

      <div className="result-layout ritual-result-layout">
        <div
          className={`door-artwork-frame ritual-door-stage material-${doorMaterial} ${
            isDoorResponded ? 'door-has-responded' : ''
          }`}
        >
          {result?.imageUrl ? (
            <>
              <img
                src={result.imageUrl}
                alt="AI generated symbolic door artwork"
                className={`door-artwork ${
                  isDoorResponded ? 'door-artwork-opened' : ''
                }`}
              />

              <div
                className="door-panel door-panel-left"
                style={{ backgroundImage: `url(${result.imageUrl})` }}
              />
              <div
                className="door-panel door-panel-right"
                style={{ backgroundImage: `url(${result.imageUrl})` }}
              />
            </>
          ) : (
            <div className="door-placeholder">
              <span>Symbolic Door Artwork</span>
            </div>
          )}

          {isDoorResponded && <div className="door-depth-glow" />}

          <div className={`badge-token ${isBadgePlaced ? 'badge-placed' : ''}`}>
            <span aria-hidden="true" />
          </div>

          {ritualStep === 'knock' && (
            <button
              className={`door-knocker ${isKnocking ? 'knocking' : ''}`}
              onClick={handleKnock}
              aria-label="Knock on the door"
            >
              <span className="knocker-ring" />
              <span className="knocker-label">
                {knockCount === 0 && text.firstKnock}
                {knockCount === 1 && text.secondKnock}
              </span>
            </button>
          )}

          {isDoorResponded && (
            <>
              <div className="door-opening-seam" />
              <div className="release-overlay">
                <p>
                  {text.overlayLineOne}
                  <br />
                  {text.overlayLineTwo}
                </p>
              </div>
            </>
          )}
        </div>

        <div className="ritual-output-panel">
          <div className="guidance-card">
            <p className="guidance-label">{text.ritualGuidance}</p>
            <p>{guidanceByStep[ritualStep]}</p>
          </div>

          {result?.audioUrl && ritualStep === 'door' && (
            <div className="audio-block custom-audio-block">
              <h2>{text.voiceNarration}</h2>
              <p>{text.voiceNarrationDescription}</p>
              <p className="ambient-note">{text.ambientNote}</p>

              <audio
                ref={audioRef}
                src={result.audioUrl}
                preload="metadata"
                onLoadedMetadata={(event) =>
                  setAudioDuration(event.currentTarget.duration)
                }
                onTimeUpdate={(event) =>
                  setAudioCurrentTime(event.currentTarget.currentTime)
                }
                onEnded={() => {
                  setIsNarrationPlaying(false)
                  setAudioCurrentTime(0)
                  stopAmbientSoundscape()
                }}
              />

              <div className="custom-audio-player">
                <button
                  className="narration-toggle"
                  onClick={toggleNarration}
                  type="button"
                >
                  <span className="narration-icon">
                    {isNarrationPlaying ? 'Ⅱ' : '▶'}
                  </span>
                  <span>
                    {isNarrationPlaying
                      ? text.pauseNarration
                      : text.playNarration}
                  </span>
                </button>

                <div className="audio-progress-shell">
                  <div
                    className="audio-progress-fill"
                    style={{ width: `${progress}%` }}
                  />
                </div>

                <span className="audio-time">
                  {formatTime(audioCurrentTime)} / {formatTime(audioDuration)}
                </span>
              </div>
            </div>
          )}

          <div className={`result-block badge-block ${isBadgePlaced ? 'badge-faded' : ''}`}>
            <h2>{text.yourBadge}</h2>
            <p>{badge}</p>
          </div>

          {ritualStep === 'door' && (
            <>
              <div className="result-block">
                <h2>{text.doorCharacter}</h2>
                <p>
                  {doorMaterialLabels[language][doorMaterial] ||
                    doorMaterialLabels[language].old_wood}
                </p>
              </div>

              <div className="result-block">
                <h2>{text.historicalEcho}</h2>
                <p>{result?.historicalEcho}</p>
              </div>

              <div className="result-block">
                <h2>{text.releaseText}</h2>
                <p>{result?.releaseText}</p>
              </div>

              <button onClick={goToBadgePlacement}>
                {text.continueToThreshold}
              </button>
            </>
          )}

          {ritualStep === 'badge' && (
            <button onClick={placeBadge}>{text.placeBadge}</button>
          )}

          {ritualStep === 'afterBadge' && (
            <button onClick={approachKnocker}>{text.approachKnocker}</button>
          )}

          {ritualStep === 'knock' && (
            <div className="result-block">
              <h2>{text.theKnocker}</h2>
              <p>{text.knockerDescription}</p>
              <p className="knock-count">
                {text.knocksHeard}: {knockCount} / 2
              </p>
            </div>
          )}

          {isDoorResponded && (
            <div className="final-release-block">
              <p>{text.finalRelease}</p>
              <button onClick={handleRestart}>{text.beginAnother}</button>
            </div>
          )}
        </div>
      </div>
    </section>
  )
}

export default ResultDoorScene
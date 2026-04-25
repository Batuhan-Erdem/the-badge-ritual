import { useState } from 'react'
import ThresholdScene from './scenes/ThresholdScene'
import BadgeInputScene from './scenes/BadgeInputScene'
import ReflectionScene from './scenes/ReflectionScene'
import LoadingRitualScene from './scenes/LoadingRitualScene'
import ResultDoorScene from './scenes/ResultDoorScene'
import { createRitual } from './services/ritualApi'


function App() {
  const [scene, setScene] = useState('threshold')
  const [ritualData, setRitualData] = useState({
    badge: '',
    origin: '',
    cost: '',
  })

  const [result, setResult] = useState(null)

  function updateRitualData(field, value) {
    setRitualData((prev) => ({
      ...prev,
      [field]: value,
    }))
  }

async function startRitual() {
  setScene('loading')

  try {
    const backendResult = await createRitual(ritualData)
    setResult(backendResult)
    setScene('result')
  } catch (error) {
    console.error(error)

    setResult({
      badgeTitle: 'The Badge at the Threshold',
      historicalEcho:
        'The ritual could not reach the archive, but the door still remembers the weight you brought here.',
      releaseText:
        'Even when the system fails, the act of naming your burden still matters. You have already begun the ritual by refusing to carry it in silence.',
      imagePrompt: '',
      ttsText: '',
      imageUrl: null,
      audioUrl: null,
    })

    setScene('result')
  }
}
  return (
    <main className="app-shell">
      {scene === 'threshold' && (
        <ThresholdScene onBegin={() => setScene('badge')} />
      )}

      {scene === 'badge' && (
        <BadgeInputScene
          badge={ritualData.badge}
          onChange={(value) => updateRitualData('badge', value)}
          onNext={() => setScene('reflection')}
        />
      )}

      {scene === 'reflection' && (
        <ReflectionScene
          origin={ritualData.origin}
          cost={ritualData.cost}
          onOriginChange={(value) => updateRitualData('origin', value)}
          onCostChange={(value) => updateRitualData('cost', value)}
          onStartRitual={startRitual}
        />
      )}

      {scene === 'loading' && <LoadingRitualScene />}

      {scene === 'result' && result && (
        <ResultDoorScene
          badge={ritualData.badge}
          result={result}
          onRestart={() => {
            setRitualData({
              badge: '',
              origin: '',
              cost: '',
            })
            setResult(null)
            setScene('threshold')
          }}
        />
      )}
    </main>
  )
}

export default App

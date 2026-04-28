let audioContext = null
let masterGain = null
let activeNodes = []
let activeIntervals = []
let isPlaying = false

const materialSoundProfiles = {
  old_wood: {
    droneFrequency: 184, // Octave up
    secondDroneFrequency: 276,
    noiseAmount: 0.1, // Increased
    masterVolume: 2.0, // Increased dramatically
    pulseNotes: [184, 207, 232, 276],
    pluckVolume: 0.6, // Increased
  },
  heavy_wood: {
    droneFrequency: 156,
    secondDroneFrequency: 248,
    noiseAmount: 0.1,
    masterVolume: 2.2,
    pulseNotes: [156, 185, 208, 247],
    pluckVolume: 0.6,
  },
  rusted_metal: {
    droneFrequency: 136,
    secondDroneFrequency: 342,
    noiseAmount: 0.15,
    masterVolume: 2.0,
    pulseNotes: [171, 205, 256, 342],
    pluckVolume: 0.5,
  },
  dark_iron: {
    droneFrequency: 110,
    secondDroneFrequency: 220,
    noiseAmount: 0.15,
    masterVolume: 2.5,
    pulseNotes: [110, 165, 220, 247],
    pluckVolume: 0.6,
  },
  fragile_wood: {
    droneFrequency: 208,
    secondDroneFrequency: 312,
    noiseAmount: 0.1,
    masterVolume: 1.8,
    pulseNotes: [208, 247, 277, 330],
    pluckVolume: 0.5,
  },
}

function getAudioContext() {
  const AudioContext = window.AudioContext || window.webkitAudioContext

  if (!AudioContext) return null

  if (!audioContext) {
    audioContext = new AudioContext()
  }

  return audioContext
}

function createSoftNoiseBuffer(context) {
  const bufferSize = context.sampleRate * 2
  const buffer = context.createBuffer(1, bufferSize, context.sampleRate)
  const data = buffer.getChannelData(0)

  for (let i = 0; i < bufferSize; i += 1) {
    data[i] = (Math.random() * 2 - 1) * 0.3
  }

  return buffer
}

function createDrone(context, frequency, gainValue, type = 'sine') {
  const oscillator = context.createOscillator()
  const gain = context.createGain()
  const filter = context.createBiquadFilter()

  oscillator.type = type
  oscillator.frequency.setValueAtTime(frequency, context.currentTime)

  filter.type = 'lowpass'
  filter.frequency.setValueAtTime(760, context.currentTime)

  gain.gain.setValueAtTime(0.0001, context.currentTime)
  gain.gain.linearRampToValueAtTime(gainValue, context.currentTime + 0.9)

  oscillator.connect(filter)
  filter.connect(gain)
  gain.connect(masterGain)

  oscillator.start()

  activeNodes.push({ source: oscillator, gain })
}

function createBreathingNoise(context, amount) {
  const noiseSource = context.createBufferSource()
  const noiseGain = context.createGain()
  const noiseFilter = context.createBiquadFilter()
  const lfo = context.createOscillator()
  const lfoGain = context.createGain()

  noiseSource.buffer = createSoftNoiseBuffer(context)
  noiseSource.loop = true

  noiseFilter.type = 'lowpass'
  noiseFilter.frequency.setValueAtTime(950, context.currentTime)

  noiseGain.gain.setValueAtTime(amount, context.currentTime)

  lfo.type = 'sine'
  lfo.frequency.setValueAtTime(0.08, context.currentTime)
  lfoGain.gain.setValueAtTime(amount * 0.65, context.currentTime)

  lfo.connect(lfoGain)
  lfoGain.connect(noiseGain.gain)

  noiseSource.connect(noiseFilter)
  noiseFilter.connect(noiseGain)
  noiseGain.connect(masterGain)

  noiseSource.start()
  lfo.start()

  activeNodes.push({ source: noiseSource, gain: noiseGain })
  activeNodes.push({ source: lfo, gain: lfoGain })
}

function playSoftPluck(context, frequency, startTime, volume = 0.06) {
  const oscillator = context.createOscillator()
  const gain = context.createGain()
  const filter = context.createBiquadFilter()
  const delay = context.createDelay()
  const delayGain = context.createGain()

  oscillator.type = 'triangle'
  oscillator.frequency.setValueAtTime(frequency, startTime)

  filter.type = 'lowpass'
  filter.frequency.setValueAtTime(1450, startTime)

  gain.gain.setValueAtTime(0.0001, startTime)
  gain.gain.linearRampToValueAtTime(volume, startTime + 0.025)
  gain.gain.exponentialRampToValueAtTime(0.0001, startTime + 1.25)

  delay.delayTime.setValueAtTime(0.22, startTime)
  delayGain.gain.setValueAtTime(volume * 0.28, startTime)
  delayGain.gain.exponentialRampToValueAtTime(0.0001, startTime + 1.3)

  oscillator.connect(filter)
  filter.connect(gain)
  gain.connect(masterGain)

  gain.connect(delay)
  delay.connect(delayGain)
  delayGain.connect(masterGain)

  oscillator.start(startTime)
  oscillator.stop(startTime + 1.3)

  activeNodes.push({ source: oscillator, gain })
}

function createSparseFolkPulse(context, profile) {
  let step = 0

  const playPattern = () => {
    if (!isPlaying || !audioContext || !masterGain) return

    const now = context.currentTime
    const notes = profile.pulseNotes
    const baseNote = notes[step % notes.length]

    playSoftPluck(context, baseNote, now, profile.pluckVolume)
    playSoftPluck(context, baseNote * 1.5, now + 0.18, profile.pluckVolume * 0.45)

    step += 1
  }

  playPattern()

  const intervalId = window.setInterval(playPattern, 1800)
  activeIntervals.push(intervalId)
}

export async function startAmbientSoundscape(doorMaterial = 'old_wood') {
  if (isPlaying) return

  const context = getAudioContext()
  if (!context) return

  if (context.state === 'suspended') {
    await context.resume()
  }

  const profile =
    materialSoundProfiles[doorMaterial] || materialSoundProfiles.old_wood

  masterGain = context.createGain()
  masterGain.gain.setValueAtTime(0.0001, context.currentTime)
  masterGain.gain.linearRampToValueAtTime(
    profile.masterVolume,
    context.currentTime + 0.75
  )
  masterGain.connect(context.destination)

  isPlaying = true

  createDrone(context, profile.droneFrequency, 0.22, 'sine')
  createDrone(context, profile.secondDroneFrequency, 0.12, 'triangle')
  createBreathingNoise(context, profile.noiseAmount)
  createSparseFolkPulse(context, profile)

  console.log('[AMBIENT] Started soundscape:', doorMaterial)
}

export function stopAmbientSoundscape() {
  if (!audioContext || !isPlaying) return

  isPlaying = false

  if (masterGain) {
    masterGain.gain.cancelScheduledValues(audioContext.currentTime)
    masterGain.gain.setValueAtTime(
      Math.max(masterGain.gain.value, 0.0001),
      audioContext.currentTime
    )
    masterGain.gain.exponentialRampToValueAtTime(
      0.0001,
      audioContext.currentTime + 0.6
    )
  }

  window.setTimeout(() => {
    activeIntervals.forEach((intervalId) => {
      window.clearInterval(intervalId)
    })

    activeIntervals = []

    activeNodes.forEach((node) => {
      if (node.source) {
        try {
          node.source.stop()
        } catch {
          // already stopped
        }
      }

      if (node.gain) {
        try {
          node.gain.disconnect()
        } catch {
          // already disconnected
        }
      }
    })

    activeNodes = []

    if (masterGain) {
      try {
        masterGain.disconnect()
      } catch {
        // already disconnected
      }
    }

    masterGain = null

    console.log('[AMBIENT] Stopped soundscape')
  }, 700)
}
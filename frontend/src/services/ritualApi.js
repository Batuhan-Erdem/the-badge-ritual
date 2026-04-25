const API_BASE_URL = 'http://127.0.0.1:8000'

export async function createRitual(ritualData) {
  const response = await fetch(`${API_BASE_URL}/api/ritual/create`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      badge: ritualData.badge,
      origin: ritualData.origin,
      cost: ritualData.cost,
    }),
  })

  if (!response.ok) {
    throw new Error('Failed to create ritual.')
  }

  return response.json()
}

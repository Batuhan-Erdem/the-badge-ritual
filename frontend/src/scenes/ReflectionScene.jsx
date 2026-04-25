function ReflectionScene({
  origin,
  cost,
  onOriginChange,
  onCostChange,
  onStartRitual,
}) {
  const canContinue = origin.trim().length > 2 && cost.trim().length > 2

  return (
    <section className="scene">
      <p className="eyebrow">The Weight</p>

      <h1>Every badge has a weight.</h1>

      <label>
        When did you first start carrying this badge?
        <textarea
          value={origin}
          onChange={(event) => onOriginChange(event.target.value)}
          placeholder="I think I started carrying it when..."
        />
      </label>

      <label>
        What has it cost you to keep wearing it?
        <textarea
          value={cost}
          onChange={(event) => onCostChange(event.target.value)}
          placeholder="It has cost me..."
        />
      </label>

      <button disabled={!canContinue} onClick={onStartRitual}>
        Let the Door Appear
      </button>
    </section>
  )
}

export default ReflectionScene

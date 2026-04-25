function BadgeInputScene({ badge, onChange, onNext }) {
  const canContinue = badge.trim().length > 2

  return (
    <section className="scene">
      <p className="eyebrow">Name Your Badge</p>

      <h1>What badge are you still carrying?</h1>

      <p className="scene-text">
        A badge can be a fear, a role, a memory, a duty, a guilt, or an identity
        you no longer want to wear.
      </p>

      <textarea
        value={badge}
        onChange={(event) => onChange(event.target.value)}
        placeholder="I always have to look strong..."
      />

      <button disabled={!canContinue} onClick={onNext}>
        Face the Weight
      </button>
    </section>
  )
}

export default BadgeInputScene

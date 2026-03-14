import { useState, useEffect } from 'react'
import './App.css'
import LandingPage from './LandingPage'

// Animated exercise image (toggles between start/end position)
function ExerciseImage({ images, name }) {
  const [frame, setFrame] = useState(0)
  const [expanded, setExpanded] = useState(false)
  const [loaded, setLoaded] = useState(false)

  useEffect(() => {
    if (!images || images.length < 2) return
    const interval = setInterval(() => {
      setFrame((f) => (f === 0 ? 1 : 0))
    }, 1200)
    return () => clearInterval(interval)
  }, [images])

  if (!images || images.length === 0) return null

  return (
    <>
      <div
        className={`exercise-image-wrap ${loaded ? 'loaded' : ''}`}
        onClick={() => setExpanded(true)}
        title="Click to enlarge"
      >
        <img
          src={images[frame]}
          alt={`${name} demonstration`}
          className="exercise-image"
          onLoad={() => setLoaded(true)}
          onError={(e) => { e.target.style.display = 'none' }}
        />
        <div className="image-badge">GIF</div>
      </div>
      {expanded && (
        <div className="image-overlay" onClick={() => setExpanded(false)}>
          <div className="image-overlay-content" onClick={(e) => e.stopPropagation()}>
            <button className="image-close-btn" onClick={() => setExpanded(false)}>✕</button>
            <img
              src={images[frame]}
              alt={`${name} demonstration`}
              className="image-overlay-img"
            />
            <div className="image-overlay-name">{name}</div>
          </div>
        </div>
      )}
    </>
  )
}

const API_URL = 'http://127.0.0.1:5000/api'

const MUSCLE_GROUPS = [
  { name: 'Full Body', icon: '🔥' },
  { name: 'Chest', icon: '🏋️' },
  { name: 'Back', icon: '🔙' },
  { name: 'Legs', icon: '🦵' },
  { name: 'Shoulders', icon: '💪' },
  { name: 'Arms', icon: '💪' },
  { name: 'Core', icon: '🎯' },
]

const DIFFICULTIES = ['Beginner', 'Intermediate', 'Advanced']

const DURATIONS = [
  { value: 'any',  label: '⏳ No Limit' },
  { value: '15',   label: '⚡ 15 min' },
  { value: '30',   label: '🕐 30 min' },
  { value: '45',   label: '🕑 45 min' },
  { value: '60',   label: '🕒 60 min' },
  { value: '90',   label: '🕓 90 min' },
]

function App() {
  const [page, setPage] = useState('landing')
  const [muscleGroup, setMuscleGroup] = useState('Full Body')
  const [difficulty, setDifficulty] = useState('Intermediate')
  const [maxDuration, setMaxDuration] = useState('any')
  const [workout, setWorkout] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const generateWorkout = async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await fetch(
        `${API_URL}/workout?muscle_group=${encodeURIComponent(muscleGroup)}&difficulty=${encodeURIComponent(difficulty)}&max_duration=${encodeURIComponent(maxDuration)}`
      )
      if (!res.ok) throw new Error('Failed to fetch workout')
      const data = await res.json()
      setWorkout(data)
    } catch (err) {
      setError('Could not connect to the server. Make sure the Python backend is running on port 5000.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  if (page === 'landing') {
    return <LandingPage onStartWorkout={() => { setPage('generator'); window.scrollTo(0, 0); }} />
  }

  return (
    <>
      {/* ── Header ─────────────────────────── */}
      <header className="app-header">
        <div className="header-top-bar">
          <button className="back-to-landing" onClick={() => setPage('landing')}>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <path d="M19 12H5M12 19l-7-7 7-7"/>
            </svg>
            Home
          </button>
          <div className="header-brand-small">
            FLOW<span className="brand-text-accent">GEN</span>
          </div>
        </div>
        <div className="header-badge">
          <span className="pulse"></span>
          Python Mini Project
        </div>
        <h1>Random Workout Generator</h1>
        <p className="subtitle">
          Generate personalized workout plans powered by Python. Select your target muscle group and difficulty to get started.
        </p>
      </header>

      {/* ── Main Content ───────────────────── */}
      <main className="app-container">

        {/* Controls Panel */}
        <div className="controls-panel">
          <div className="controls-grid">
            <div className="control-group">
              <label htmlFor="muscle-group">Target Muscle Group</label>
              <select
                id="muscle-group"
                value={muscleGroup}
                onChange={(e) => setMuscleGroup(e.target.value)}
              >
                {MUSCLE_GROUPS.map((g) => (
                  <option key={g.name} value={g.name}>
                    {g.icon} {g.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="control-group">
              <label htmlFor="difficulty">Difficulty Level</label>
              <select
                id="difficulty"
                value={difficulty}
                onChange={(e) => setDifficulty(e.target.value)}
              >
                {DIFFICULTIES.map((d) => (
                  <option key={d} value={d}>
                    {d === 'Beginner' ? '🟢' : d === 'Intermediate' ? '🟡' : '🔴'} {d}
                  </option>
                ))}
              </select>
            </div>

            <div className="control-group">
              <label htmlFor="duration">Workout Duration</label>
              <select
                id="duration"
                value={maxDuration}
                onChange={(e) => setMaxDuration(e.target.value)}
              >
                {DURATIONS.map((d) => (
                  <option key={d.value} value={d.value}>
                    {d.label}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <button
            className="generate-btn"
            onClick={generateWorkout}
            disabled={loading}
          >
            <span className="btn-content">
              {loading ? (
                <>
                  <span className="spinner"></span>
                  Generating...
                </>
              ) : (
                <>⚡ Generate Workout</>
              )}
            </span>
          </button>
        </div>

        {/* Error Message */}
        {error && (
          <div className="quote-card" style={{ borderColor: '#ff4444', color: '#ff8888' }}>
            ⚠️ {error}
          </div>
        )}

        {/* Workout Results */}
        {workout && !error && (
          <div className="workout-results" key={JSON.stringify(workout)}>
            
            {/* Header Card */}
            <div className="workout-header-card">
              <h2 className="workout-title">
                {workout.muscle_group} Workout
              </h2>
              <div className="workout-meta">
                <span className="meta-chip">
                  🎯 Difficulty: <span className="meta-value">{workout.difficulty}</span>
                </span>
                <span className="meta-chip">
                  🏋️ Exercises: <span className="meta-value">{workout.exercise_count}</span>
                </span>
                <span className="meta-chip">
                  ⏱️ Est. Duration: <span className="meta-value">{workout.estimated_duration}</span>
                </span>
                {workout.max_duration && (
                  <span className="meta-chip duration-chip">
                    🎯 Time Limit: <span className="meta-value">{workout.max_duration}</span>
                  </span>
                )}
              </div>
            </div>

            {/* Quote */}
            <div className="quote-card">
              "{workout.quote}"
            </div>

            {/* Warm-Up */}
            <div className="section-card">
              <h3 className="section-title">
                <span className="section-icon">🔥</span> Warm-Up
              </h3>
              <ul className="warmup-list">
                {workout.warmup.map((item, i) => (
                  <li key={i}>{item}</li>
                ))}
              </ul>
            </div>

            {/* Exercises */}
            <div className="section-card">
              <h3 className="section-title">
                <span className="section-icon">💪</span> Exercises
              </h3>
              <div className="exercise-list">
                {workout.exercises.map((ex) => (
                  <div className="exercise-card" key={ex.order}>
                    <div className="exercise-order">{ex.order}</div>
                    <div className="exercise-info">
                      <div className="exercise-name">{ex.name}</div>
                      <div className="exercise-equipment">{ex.equipment}</div>
                    </div>
                    <ExerciseImage images={ex.images} name={ex.name} />
                    <div className="exercise-details">
                      <div className="detail-badge">
                        <span className="detail-value">{ex.sets}</span>
                        <span className="detail-label">Sets</span>
                      </div>
                      <div className="detail-badge">
                        <span className="detail-value">{ex.reps}</span>
                        <span className="detail-label">Reps</span>
                      </div>
                      <div className="detail-badge">
                        <span className="detail-value">{ex.rest}</span>
                        <span className="detail-label">Rest</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Cool-Down */}
            <div className="section-card">
              <h3 className="section-title">
                <span className="section-icon">🧊</span> Cool-Down
              </h3>
              <ul className="cooldown-list">
                {workout.cooldown.map((item, i) => (
                  <li key={i}>{item}</li>
                ))}
              </ul>
            </div>
          </div>
        )}

        {/* Empty State */}
        {!workout && !error && (
          <div className="empty-state">
            <div className="empty-icon">🏋️</div>
            <h3>Ready to Work Out?</h3>
            <p>Select your preferences above and hit the generate button to create a randomized workout plan.</p>
          </div>
        )}
      </main>

      {/* ── Footer ─────────────────────────── */}
      <footer className="app-footer">
        Built with <span>Python</span> & <span>React</span> — Random Workout Generator © 2026
      </footer>
    </>
  )
}

export default App

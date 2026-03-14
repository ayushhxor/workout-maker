import './LandingPage.css'

function LandingPage({ onStartWorkout }) {
  return (
    <div className="landing">
      {/* ── Fixed Header ────────────────────── */}
      <header className="landing-header">
        <div className="landing-header-inner">
          <div className="brand-logo">
            FLOW<span className="brand-accent">GEN</span>
          </div>
          <nav className="landing-nav">
            <a href="#trending">Programs</a>
            <a href="#trending" onClick={(e) => { e.preventDefault(); onStartWorkout(); }}>Workouts</a>
            <a href="#footer">Community</a>
            <a href="#footer">About</a>
          </nav>
          <button className="header-login-btn" onClick={onStartWorkout}>
            Login
          </button>
        </div>
      </header>

      {/* ── Hero Section ────────────────────── */}
      <section className="hero-section">
        <div className="hero-content">
          <span className="hero-tag">Aesthetic Gains Only</span>
          <h1 className="hero-title">
            <span>Sweat</span>
            <span>Your</span>
            <span className="hero-accent">Way</span>
          </h1>
          <p className="hero-desc">
            AI-powered flows tailored to your vibe, your space, and your energy level.
            Join the next generation of athletes.
          </p>
          <button className="hero-cta" onClick={onStartWorkout}>
            Start Your Flow
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
              <path d="M14 5l7 7m0 0l-7 7m7-7H3" />
            </svg>
          </button>
        </div>
        {/* Scroll indicator */}
        <div className="scroll-indicator">
          <div className="scroll-capsule">
            <div className="scroll-dot"></div>
          </div>
        </div>
      </section>

      {/* ── Trending Section ─────────────────── */}
      <section className="trending-section" id="trending">
        <div className="trending-inner">
          <div className="trending-header">
            <div className="trending-title-wrap">
              <h2 className="trending-title">Trending Now</h2>
              <div className="trending-underline"></div>
            </div>
            <button className="see-all-btn" onClick={onStartWorkout}>See All</button>
          </div>
          <div className="trending-grid">
            {/* Card 1 */}
            <article className="trending-card" onClick={onStartWorkout}>
              <div className="card-image-wrap">
                <img
                  src="https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=600&auto=format&fit=crop&q=80"
                  alt="High intensity interval training"
                  className="card-image"
                />
                <span className="card-badge">Hot</span>
              </div>
              <div className="card-body">
                <h3 className="card-title">Phonk Pump HIIT</h3>
                <div className="card-meta">
                  <span>15 Mins</span>
                  <span className="meta-dot"></span>
                  <span>Advanced</span>
                  <span className="meta-dot"></span>
                  <span>No Equipment</span>
                </div>
                <div className="card-footer">
                  <span className="card-saves">#24k SAVED</span>
                  <button className="card-join-btn">Join +</button>
                </div>
              </div>
            </article>
            {/* Card 2 */}
            <article className="trending-card" onClick={onStartWorkout}>
              <div className="card-image-wrap">
                <img
                  src="https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=600&auto=format&fit=crop&q=80"
                  alt="Mobility and flexibility workout"
                  className="card-image"
                />
              </div>
              <div className="card-body">
                <h3 className="card-title">Matrix Mobility</h3>
                <div className="card-meta">
                  <span>30 Mins</span>
                  <span className="meta-dot"></span>
                  <span>Beginner</span>
                  <span className="meta-dot"></span>
                  <span>Mat Only</span>
                </div>
                <div className="card-footer">
                  <span className="card-saves">#18k SAVED</span>
                  <button className="card-join-btn">Join +</button>
                </div>
              </div>
            </article>
            {/* Card 3 */}
            <article className="trending-card" onClick={onStartWorkout}>
              <div className="card-image-wrap">
                <img
                  src="https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=600&auto=format&fit=crop&q=80"
                  alt="Core strength training"
                  className="card-image"
                />
              </div>
              <div className="card-body">
                <h3 className="card-title">Vapor Core 300</h3>
                <div className="card-meta">
                  <span>20 Mins</span>
                  <span className="meta-dot"></span>
                  <span>Intermediate</span>
                  <span className="meta-dot"></span>
                  <span>Bodyweight</span>
                </div>
                <div className="card-footer">
                  <span className="card-saves">#12k SAVED</span>
                  <button className="card-join-btn">Join +</button>
                </div>
              </div>
            </article>
          </div>
        </div>
      </section>

      {/* ── Stats Section ────────────────────── */}
      <section className="stats-section">
        <div className="stats-inner">
          <div className="stat-item">
            <div className="stat-number">50+</div>
            <div className="stat-label">Exercises</div>
          </div>
          <div className="stat-divider"></div>
          <div className="stat-item">
            <div className="stat-number">7</div>
            <div className="stat-label">Muscle Groups</div>
          </div>
          <div className="stat-divider"></div>
          <div className="stat-item">
            <div className="stat-number">3</div>
            <div className="stat-label">Difficulty Levels</div>
          </div>
          <div className="stat-divider"></div>
          <div className="stat-item">
            <div className="stat-number">∞</div>
            <div className="stat-label">Unique Workouts</div>
          </div>
        </div>
      </section>

      {/* ── Footer ──────────────────────────── */}
      <footer className="landing-footer" id="footer">
        <div className="footer-inner">
          <div className="footer-brand">
            FLOW<span className="brand-accent">GEN</span>
          </div>
          <p className="footer-tagline">Generated for the next generation of athletes.</p>
          <div className="footer-links">
            <a href="#">Instagram</a>
            <a href="#">TikTok</a>
            <a href="#">Discord</a>
          </div>
          <div className="footer-copy">
            © 2026 FlowGen Studio. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  )
}

export default LandingPage

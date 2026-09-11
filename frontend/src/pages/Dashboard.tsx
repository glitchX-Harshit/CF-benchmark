import { motion } from "framer-motion";
import { ArrowUpRight, BarChart3, Check, CircleArrowOutUpRight, MessageSquare, TrendingUp, Users, Zap } from "lucide-react";

const stats = [
  { label: "Conversations analyzed", value: "1,248", change: "+12.5%", icon: MessageSquare },
  { label: "Average response score", value: "76.4", change: "+3.2%", icon: TrendingUp },
  { label: "Benchmark runs", value: "342", change: "+28.4%", icon: BarChart3 },
  { label: "Active prospects", value: "89", change: "-2.1%", icon: Users },
];

const evaluations = [
  { company: "Acme Corp", objection: "Price objection", time: "2 hours ago", score: 84 },
  { company: "Globex", objection: "Missing feature", time: "5 hours ago", score: 62 },
  { company: "Initech", objection: "Competitor preference", time: "1 day ago", score: 92 },
  { company: "Soylent", objection: "Timeline push", time: "2 days ago", score: 45 },
];

export default function Dashboard() {
  return (
    <motion.div initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: .6, ease: "easeOut" }} className="dashboard">
      <header className="page-header">
        <div>
          <p className="eyebrow"><span className="eyebrow__line" /> Monday, 14 October 2024</p>
          <h1>Make every<br /><em>conversation</em> count<span className="title-dot">.</span></h1>
          <p className="page-intro">A clearer view of the conversations, patterns, and moments that move a deal forward.</p>
        </div>
        <motion.div className="hero-character" initial={{ opacity: 0, rotate: -8, scale: .9 }} animate={{ opacity: 1, rotate: 0, scale: 1 }} transition={{ delay: .25, duration: .7 }}>
          <span className="hero-character__caption">THE LISTENER / 01</span>
          <span className="hero-character__star">✦</span>
          <span className="hero-character__halo" />
          <span className="hero-character__head"><span className="hero-character__eye" /></span>
          <span className="hero-character__neck" />
          <span className="hero-character__shoulder" />
          <span className="hero-character__orbit" />
        </motion.div>
        <motion.a whileHover={{ y: -3 }} whileTap={{ scale: .98 }} href="/benchmarks" className="primary-button">
          <span>New benchmark</span><ArrowUpRight size={16} />
        </motion.a>
      </header>

      <div className="metric-grid">
        {stats.map((stat, i) => {
          const Icon = stat.icon;
          return (
            <motion.article key={stat.label} initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: .12 + i * .08 }} className="metric-card">
              <div className="metric-card__top"><span className="metric-card__index">0{i + 1}</span><Icon size={17} /></div>
              <p>{stat.label}</p>
              <div className="metric-card__value">{stat.value}<span>{stat.change}</span></div>
              <div className="metric-card__bar"><span style={{ width: `${58 + i * 9}%` }} /></div>
            </motion.article>
          );
        })}
      </div>

      <div className="section-heading">
        <div><p className="eyebrow">Signal / 01</p><h2>Recent evaluations</h2></div>
        <button className="text-button">View archive <CircleArrowOutUpRight size={14} /></button>
      </div>
      <div className="workspace-grid">
        <section className="evaluations-card">
          <div className="card-label">Latest signals <span>04 entries</span></div>
          {evaluations.map((item) => (
            <motion.div key={item.company} whileHover={{ x: 6 }} className="evaluation-row">
              <span className={`score-badge ${item.score > 75 ? "score-badge--good" : item.score > 50 ? "score-badge--mid" : "score-badge--low"}`}>{item.score}</span>
              <div className="evaluation-row__copy"><strong>{item.company}</strong><span>{item.objection} <i>·</i> {item.time}</span></div>
              <button className="row-arrow" aria-label={`Open ${item.company} evaluation`}><ArrowUpRight size={16} /></button>
            </motion.div>
          ))}
        </section>
        <motion.section whileHover={{ y: -4 }} className="feature-card">
          <div className="feature-card__orb" />
          <div className="feature-card__top"><span>CF / BETA</span><Zap size={18} /></div>
          <div className="feature-card__art">↗</div>
          <div className="feature-card__figure"><span /><i /><b /></div>
          <h3>Run a new<br /><em>benchmark.</em></h3>
          <p>Compare a seller response against a real scenario and find the next move hidden inside every objection.</p>
          <a href="/benchmarks" className="feature-card__link">Start evaluation <ArrowUpRight size={15} /></a>
        </motion.section>
      </div>

      <div className="dashboard-footer"><span><span className="status-dot" /> Live data stream</span><span>Last synced 2 min ago</span><span className="footer-check"><Check size={12} /> All systems operational</span></div>
    </motion.div>
  );
}

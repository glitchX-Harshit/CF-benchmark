import { BrowserRouter as Router, Routes, Route, Link, useLocation } from "react-router-dom";
import { motion } from "framer-motion";
import Dashboard from "./pages/Dashboard";
import BenchmarkPage from "./pages/Benchmark";
import { Activity, BarChart2, MessageSquare, Settings, Users, Zap } from "lucide-react";

const links = [
  { path: "/", label: "Overview", icon: BarChart2 },
  { path: "/benchmarks", label: "CF Benchmark", icon: Zap },
  { path: "#", label: "Conversations", icon: MessageSquare },
  { path: "#", label: "Evaluations", icon: Activity },
  { path: "#", label: "Prospects", icon: Users },
  { path: "#", label: "Settings", icon: Settings },
];

function NavLinks() {
  const location = useLocation();

  return (
    <div className="nav-links">
      {links.map((link, index) => {
        const isActive = location.pathname === link.path;
        const Icon = link.icon;
        return (
          <Link
            key={link.label}
            to={link.path}
            aria-current={isActive ? "page" : undefined}
            className={`nav-link ${isActive ? "is-active" : ""}`}
          >
            {isActive && (
              <motion.span
                layoutId="activeTab"
                className="nav-link__active-bg"
                transition={{ type: "spring", stiffness: 350, damping: 30 }}
              />
            )}
            <span className="nav-link__number">0{index + 1}</span>
            <Icon className="nav-link__icon" />
            <span className="nav-link__label">{link.label}</span>
          </Link>
        );
      })}
    </div>
  );
}

function BrandMark() {
  return (
    <div className="brand-mark" aria-label="CF Benchmark">
      <span className="brand-mark__shape" aria-hidden="true">CF</span>
      <span className="brand-mark__lockup">
        <span className="brand-mark__text">cf benchmark<span>.</span></span>
        <span className="brand-mark__tagline">CLOSE MORE. LEARN FASTER.</span>
      </span>
    </div>
  );
}

export default function App() {
  return (
    <Router>
      <div className="app-shell">
        <aside className="sidebar">
          <div className="sidebar__topline">
            <span>CF / PRODUCT</span>
            <span>RESPONSE BENCHMARK</span>
          </div>
          <div className="sidebar__brand">
            <BrandMark />
          </div>
          <div className="sidebar__rule" />
          <nav aria-label="Primary navigation">
            <p className="nav-eyebrow">Workspace</p>
            <NavLinks />
          </nav>
          <div className="sidebar__footer">
            <div className="status-line"><span className="status-dot" /> System online</div>
            <div className="profile-card">
              <div className="profile-avatar">AC</div>
              <div>
                <div className="profile-name">Alex Carter</div>
                <div className="profile-role">Lead Architect</div>
              </div>
              <span className="profile-arrow">↗</span>
            </div>
          </div>
        </aside>

        <main className="main-content">
          <div className="ambient ambient--one" />
          <div className="ambient ambient--two" />
          <div className="main-grid-line" />
          <div className="content-wrap">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/benchmarks" element={<BenchmarkPage />} />
            </Routes>
          </div>
        </main>
      </div>
    </Router>
  );
}

import React, { useState } from 'react';
import { 
  Shield, 
  User, 
  Mail, 
  Lock, 
  Eye, 
  EyeOff, 
  ArrowRight, 
  CheckCircle2, 
  FolderSearch, 
  Database, 
  MessageSquare, 
  BarChart3, 
  Search, 
  Globe, 
  Layers, 
  Activity,
  Sparkles
} from 'lucide-react';

const CAPABILITIES = [
  {
    title: "Natural-Language Investigation",
    desc: "Ask complex case lookups in plain conversational phrasing.",
    icon: FolderSearch,
    animClass: "anim-init-cap-1"
  },
  {
    title: "Multi-Table Relational Reasoning",
    desc: "Automated join inference across FIRs, accused, victims, and officers.",
    icon: Database,
    animClass: "anim-init-cap-2"
  },
  {
    title: "Conversational Case Context",
    desc: "Maintains active case IDs and suspect references across multi-turn queries.",
    icon: MessageSquare,
    animClass: "anim-init-cap-3"
  },
  {
    title: "Analytical Crime Insights",
    desc: "Aggregations, caseload rankings, and time-series trend analysis.",
    icon: BarChart3,
    animClass: "anim-init-cap-4"
  },
  {
    title: "Semantic Modus-Operandi Discovery",
    desc: "In-memory BM25 concept expansion search across case brief facts.",
    icon: Search,
    animClass: "anim-init-cap-5"
  },
  {
    title: "Multilingual Interaction",
    desc: "Native understanding and synthesis in English, ಕನ್ನಡ (Kannada), and हिन्दी (Hindi).",
    icon: Globe,
    animClass: "anim-init-cap-6"
  },
  {
    title: "Visual Analytics & Dossier Export",
    desc: "Live dynamic charts and 1-click confidential law enforcement PDF dossiers.",
    icon: Layers,
    animClass: "anim-init-cap-7"
  }
];

export default function LoginPage({ onLoginSuccess }) {
  const [kgid, setKgid] = useState('KGID-904218');
  const [officerName, setOfficerName] = useState('Inspector Ramesh Rao');
  const [email, setEmail] = useState('r.rao@ksp.gov.in');
  const [password, setPassword] = useState('AlokaKSP@2026');
  const [showPassword, setShowPassword] = useState(false);
  const [isAuthenticating, setIsAuthenticating] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setIsAuthenticating(true);
    // Smooth transition simulation
    setTimeout(() => {
      onLoginSuccess({
        kgid: kgid.trim() || 'KGID-904218',
        name: officerName.trim() || 'Inspector Ramesh Rao',
        email: email.trim() || 'r.rao@ksp.gov.in'
      });
    }, 400);
  };

  return (
    <div className="min-h-screen w-full bg-[#0B1017] text-slate-100 flex flex-col justify-between overflow-y-auto selection:bg-[#2F5DA8] selection:text-white bg-command-grid">
      {/* Top Subtle Status Bar */}
      <header className="w-full h-12 border-b border-[#263142] px-4 sm:px-8 flex items-center justify-between bg-[#101722]/80 backdrop-blur-md shrink-0 z-20">
        <div className="flex items-center gap-2">
          <img 
            src="https://upload.wikimedia.org/wikipedia/commons/a/aa/Seal_of_Karnataka.svg" 
            alt="Karnataka Police Emblem" 
            className="w-6 h-6 object-contain"
          />
          <span className="text-xs font-mono font-black tracking-wider text-slate-100 uppercase">
            KARNATAKA STATE POLICE
          </span>
          <span className="hidden sm:inline-block text-[#263142]">|</span>
          <span className="hidden sm:inline-block text-[10px] font-mono font-semibold text-slate-400 uppercase tracking-widest">
            STATE INTELLIGENCE PORTAL
          </span>
        </div>

        <div className="flex items-center gap-2 text-[10px] font-mono font-bold text-emerald-400 bg-[#102619] px-2.5 py-0.5 rounded border border-emerald-900/60">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
          <span>SYSTEM ONLINE</span>
        </div>
      </header>

      {/* Main Split-Screen Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 lg:p-8 flex flex-col lg:flex-row items-center justify-center gap-8 lg:gap-12 z-10">
        
        {/* ============================================================ */}
        {/* LEFT SIDE: OFFICER LOGIN PANEL (40-45% on Desktop)          */}
        {/* ============================================================ */}
        <section className="w-full lg:w-[42%] max-w-md bg-[#101722] border border-[#263142] rounded-2xl p-6 sm:p-8 shadow-2xl relative">
          {/* Top Form Header */}
          <div className="mb-6 pb-4 border-b border-[#263142]">
            <div className="flex items-center gap-1.5 text-[10px] font-mono font-bold uppercase tracking-wider text-[#93B4E8] bg-[#172640] px-2.5 py-1 rounded w-fit border border-[#263142] mb-3">
              <Shield className="w-3 h-3 text-[#93B4E8]" />
              <span>OFFICER AUTHENTICATION</span>
            </div>
            
            <h2 className="text-xl font-black text-white font-mono tracking-tight uppercase">
              ALOKA INTELLIGENCE
            </h2>
            <p className="text-xs text-slate-400 mt-0.5">
              Authorized personnel access
            </p>
          </div>

          {/* Authentication Form */}
          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Field 1: KGID */}
            <div className="space-y-1.5">
              <label className="text-[11px] font-mono font-semibold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
                <Shield className="w-3 h-3 text-[#93B4E8]" />
                <span>KGID (Govt. ID)</span>
              </label>
              <div className="relative flex items-center">
                <input
                  type="text"
                  required
                  value={kgid}
                  onChange={(e) => setKgid(e.target.value)}
                  placeholder="Enter your KGID"
                  className="w-full bg-[#141C28] border border-[#263142] rounded-lg py-2.5 px-3 text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-[#2F5DA8] focus:ring-1 focus:ring-[#2F5DA8]/50 transition-all font-mono"
                />
              </div>
            </div>

            {/* Field 2: Officer Name */}
            <div className="space-y-1.5">
              <label className="text-[11px] font-mono font-semibold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
                <User className="w-3 h-3 text-[#93B4E8]" />
                <span>Officer Name</span>
              </label>
              <div className="relative flex items-center">
                <input
                  type="text"
                  required
                  value={officerName}
                  onChange={(e) => setOfficerName(e.target.value)}
                  placeholder="Enter your full name"
                  className="w-full bg-[#141C28] border border-[#263142] rounded-lg py-2.5 px-3 text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-[#2F5DA8] focus:ring-1 focus:ring-[#2F5DA8]/50 transition-all font-medium"
                />
              </div>
            </div>

            {/* Field 3: Official Email */}
            <div className="space-y-1.5">
              <label className="text-[11px] font-mono font-semibold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
                <Mail className="w-3 h-3 text-[#93B4E8]" />
                <span>Official Email ID</span>
              </label>
              <div className="relative flex items-center">
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="Enter your official email"
                  className="w-full bg-[#141C28] border border-[#263142] rounded-lg py-2.5 px-3 text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-[#2F5DA8] focus:ring-1 focus:ring-[#2F5DA8]/50 transition-all font-medium"
                />
              </div>
            </div>

            {/* Field 4: Password */}
            <div className="space-y-1.5">
              <label className="text-[11px] font-mono font-semibold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
                <Lock className="w-3 h-3 text-[#93B4E8]" />
                <span>Password</span>
              </label>
              <div className="relative flex items-center">
                <input
                  type={showPassword ? "text" : "password"}
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter your password"
                  className="w-full bg-[#141C28] border border-[#263142] rounded-lg py-2.5 pl-3 pr-10 text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-[#2F5DA8] focus:ring-1 focus:ring-[#2F5DA8]/50 transition-all font-mono"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 p-1 text-slate-400 hover:text-slate-200 transition-colors cursor-pointer"
                  title={showPassword ? "Hide password" : "Show password"}
                  aria-label={showPassword ? "Hide password" : "Show password"}
                >
                  {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </div>

            {/* Submit Action Button */}
            <button
              type="submit"
              disabled={isAuthenticating}
              className="w-full mt-2 bg-[#2F5DA8] hover:bg-[#3A6DBD] text-white py-3 px-4 rounded-xl text-xs font-bold uppercase tracking-wider font-mono shadow-md hover:shadow-lg transition-all flex items-center justify-center gap-2 cursor-pointer disabled:opacity-60"
            >
              {isAuthenticating ? (
                <>
                  <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
                  <span>AUTHENTICATING PROTOCOL...</span>
                </>
              ) : (
                <>
                  <span>AUTHENTICATE & ENTER</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>

            {/* Subtext */}
            <div className="text-center pt-2">
              <span className="text-[10px] font-mono text-slate-400 uppercase tracking-wider">
                Authorized personnel only
              </span>
            </div>
          </form>
        </section>


        {/* ============================================================ */}
        {/* RIGHT SIDE: ALOKA WELCOME & OVERVIEW (55-60% on Desktop)    */}
        {/* ============================================================ */}
        <section className="w-full lg:w-[58%] flex flex-col justify-center py-4 lg:py-2">
          
          {/* 1. Animated Logo (Sequence 0.2s) */}
          <div className="flex items-center gap-3.5 mb-4 anim-init-logo">
            <div className="w-14 h-14 rounded-2xl bg-[#101722] border border-[#263142] p-2.5 flex items-center justify-center shadow-lg shrink-0">
              <img 
                src="https://upload.wikimedia.org/wikipedia/commons/a/aa/Seal_of_Karnataka.svg" 
                alt="Seal of Karnataka State Police" 
                className="w-full h-full object-contain drop-shadow-md"
              />
            </div>
            
            <div className="flex flex-col">
              {/* 2. Title (Sequence 0.5s) */}
              <div className="flex items-center gap-2 anim-init-title">
                <h1 className="text-2xl sm:text-3xl font-black text-white tracking-wider font-mono uppercase">
                  ALOKA INTELLIGENCE
                </h1>
                <span className="px-2 py-0.5 rounded text-[9px] font-bold font-mono bg-[#172640] text-[#93B4E8] border border-[#263142] tracking-widest uppercase">
                  KSP
                </span>
              </div>

              {/* 3. Subtitle (Sequence 0.8s) */}
              <span className="text-[11px] font-mono font-bold uppercase tracking-widest text-[#93B4E8] anim-init-subtitle">
                STATE INTELLIGENCE COMMAND CENTER
              </span>
            </div>
          </div>

          {/* 4. Welcome Message (Sequence 1.1s) */}
          <div className="mb-6 anim-init-welcome">
            <h2 className="text-lg sm:text-xl font-bold text-slate-100 mb-1.5 tracking-tight">
              Welcome to Aloka Intelligence
            </h2>
            <p className="text-xs sm:text-sm text-slate-400 leading-relaxed max-w-xl">
              An AI-powered intelligence assistant for exploring and understanding Karnataka State criminological data.
            </p>
          </div>

          {/* 5. Capability Indicators (Sequence 1.4s Staggered) */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5 max-w-xl">
            {CAPABILITIES.map((cap, idx) => {
              const Icon = cap.icon;
              return (
                <div 
                  key={idx}
                  className={`flex items-start gap-2.5 p-2.5 rounded-xl bg-[#101722]/90 border border-[#263142] hover:border-[#2F5DA8] transition-all group ${cap.animClass}`}
                >
                  <div className="p-1.5 rounded-lg bg-[#141C28] text-[#93B4E8] group-hover:text-white group-hover:bg-[#2F5DA8] transition-colors shrink-0 mt-0.5 border border-[#263142]">
                    <Icon className="w-3.5 h-3.5" />
                  </div>
                  <div className="flex flex-col">
                    <span className="text-xs font-bold text-slate-200 group-hover:text-white transition-colors">
                      {cap.title}
                    </span>
                    <span className="text-[10px] text-slate-400 line-clamp-1 leading-normal">
                      {cap.desc}
                    </span>
                  </div>
                </div>
              );
            })}
          </div>

        </section>
      </main>

      {/* Bottom Institutional Footer */}
      <footer className="w-full h-9 border-t border-[#263142] px-4 sm:px-8 flex items-center justify-between bg-[#101722]/90 text-[10px] font-mono text-slate-400 uppercase tracking-wider shrink-0 z-20">
        <div className="flex items-center gap-2 text-slate-400">
          <Shield className="w-3 h-3 text-[#2F5DA8]" />
          <span>KSP STATE CRIMINOLOGICAL DATABASE</span>
        </div>
        
        <div className="flex items-center gap-2 text-emerald-400 font-semibold">
          <Activity className="w-3 h-3" />
          <span>SYSTEM SECURE & OPERATIONAL</span>
        </div>
      </footer>
    </div>
  );
}

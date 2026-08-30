import React, { useState, useEffect, useRef } from 'react';
import { 
  Shield, 
  User, 
  Lock, 
  Eye, 
  EyeOff, 
  ArrowRight, 
  CheckCircle2, 
  AlertTriangle,
  Loader2,
  FolderSearch, 
  Database, 
  MessageSquare, 
  BarChart3, 
  Search, 
  Globe, 
  Layers, 
  Activity,
  Check,
  Sparkles,
  KeyRound,
  UserCheck
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

const DEMO_OFFICERS = [
  { 
    id: 'divya',
    name: 'Divya', 
    fullName: 'Divya Joshi', 
    rank: 'Sub-Inspector', 
    kgid: 'KGID970867' 
  },
  { 
    id: 'pradeep',
    name: 'Pradeep', 
    fullName: 'Pradeep Kumar', 
    rank: 'Inspector', 
    kgid: 'KGID752959' 
  },
  { 
    id: 'swathi',
    name: 'Swathi', 
    fullName: 'Swathi Kumar', 
    rank: 'Inspector', 
    kgid: 'KGID609762' 
  }
];

export default function LoginPage({ onLoginSuccess }) {
  const [kgid, setKgid] = useState('');
  const [officerData, setOfficerData] = useState(null);
  const [isVerifying, setIsVerifying] = useState(false);
  const [kgidError, setKgidError] = useState(null);
  const [authError, setAuthError] = useState(null);
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isAuthenticating, setIsAuthenticating] = useState(false);
  const [isFormHovered, setIsFormHovered] = useState(false);

  const debounceTimerRef = useRef(null);

  // Auto-verify KGID with 400ms debounce
  useEffect(() => {
    const trimmedKgid = kgid.trim();
    setAuthError(null);

    if (!trimmedKgid || trimmedKgid.length < 3) {
      setOfficerData(null);
      setKgidError(null);
      setIsVerifying(false);
      return;
    }

    if (debounceTimerRef.current) {
      clearTimeout(debounceTimerRef.current);
    }

    setIsVerifying(true);
    setKgidError(null);

    debounceTimerRef.current = setTimeout(async () => {
      try {
        const response = await fetch(`/employee/lookup/${encodeURIComponent(trimmedKgid)}`);
        const data = await response.json();

        if (data.found) {
          setOfficerData(data);
          setKgidError(null);
        } else {
          setOfficerData(null);
          setKgidError(data.message || "KGID NOT FOUND. Please verify the KGID and try again.");
        }
      } catch (err) {
        console.error("KGID lookup error:", err);
        setOfficerData(null);
        setKgidError("Unable to reach verification server. Please verify backend connection.");
      } finally {
        setIsVerifying(false);
      }
    }, 400);

    return () => {
      if (debounceTimerRef.current) {
        clearTimeout(debounceTimerRef.current);
      }
    };
  }, [kgid]);

  // Handle Form Submission / Backend Authentication
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!officerData || isVerifying) return;

    setIsAuthenticating(true);
    setAuthError(null);

    try {
      const response = await fetch('/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          kgid: kgid.trim(),
          password: password
        })
      });

      const data = await response.json();

      if (data.authenticated) {
        onLoginSuccess(data.officer);
      } else {
        setAuthError(data.error || "Authentication failed. Please check your credentials.");
      }
    } catch (err) {
      console.error("Authentication network error:", err);
      setAuthError("Authentication service unreachable. Please ensure the backend is running.");
    } finally {
      setIsAuthenticating(false);
    }
  };

  const handleSelectDemoOfficer = (demoKgid) => {
    setKgid(demoKgid);
    setPassword('KGID@123');
    setAuthError(null);
  };

  return (
    <div className="h-screen w-full bg-[#0B1017] text-slate-100 flex flex-col justify-between overflow-x-hidden overflow-y-auto lg:overflow-hidden selection:bg-[#2F5DA8] selection:text-white bg-command-grid">
      {/* Top Subtle Status Bar */}
      <header className="w-full h-11 border-b border-[#263142] px-4 sm:px-8 flex items-center justify-between bg-[#101722]/90 backdrop-blur-md shrink-0 z-20">
        <div className="flex items-center gap-2">
          <img 
            src="https://upload.wikimedia.org/wikipedia/commons/a/aa/Seal_of_Karnataka.svg" 
            alt="Karnataka Police Emblem" 
            className="w-5 h-5 sm:w-6 sm:h-6 object-contain"
          />
          <span className="text-[11px] sm:text-xs font-mono font-black tracking-wider text-slate-100 uppercase">
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
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-2 sm:py-4 flex flex-col lg:flex-row items-center justify-center gap-6 lg:gap-12 z-10">
        
        {/* ============================================================ */}
        {/* LEFT SIDE: OFFICER LOGIN PANEL (40-45% on Desktop)          */}
        {/* ============================================================ */}
        <section 
          onMouseEnter={() => setIsFormHovered(true)}
          onMouseLeave={() => setIsFormHovered(false)}
          className="w-full lg:w-[440px] max-w-md bg-[#101722] border border-[#263142] rounded-2xl p-5 sm:p-6 shadow-2xl relative shrink-0 transition-all duration-300"
        >
          {/* Top Form Header */}
          <div className="mb-3.5 pb-2.5 border-b border-[#263142]">
            <div className="flex items-center gap-1.5 text-[10px] font-mono font-bold uppercase tracking-wider text-[#93B4E8] bg-[#172640] px-2.5 py-1 rounded w-fit border border-[#263142] mb-2">
              <Shield className="w-3 h-3 text-[#93B4E8]" />
              <span>OFFICER AUTHENTICATION</span>
            </div>
            
            <h2 className="text-lg sm:text-xl font-black text-white font-mono tracking-tight uppercase">
              ALOKA INTELLIGENCE
            </h2>
            <p className="text-[11px] text-slate-400 mt-0.5">
              Authorized personnel access
            </p>
          </div>

          {/* Authentication Form */}
          <form onSubmit={handleSubmit} className="space-y-3">
            
            {/* Field 1: KGID Input */}
            <div className="space-y-1">
              <div className="flex items-center justify-between">
                <label className="text-[10.5px] font-mono font-semibold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
                  <Shield className="w-3 h-3 text-[#93B4E8]" />
                  <span>KGID</span>
                </label>
                {isVerifying && (
                  <span className="flex items-center gap-1 text-[10px] font-mono text-[#93B4E8] animate-pulse">
                    <Loader2 className="w-3 h-3 animate-spin" />
                    <span>Verifying officer...</span>
                  </span>
                )}
                {officerData && !isVerifying && (
                  <span className="flex items-center gap-1 text-[10px] font-mono font-bold text-emerald-400 bg-[#102619] px-2 py-0.2 rounded border border-emerald-900/60">
                    <Check className="w-3 h-3 stroke-[3]" />
                    <span>Officer Identified</span>
                  </span>
                )}
              </div>

              <div className="relative flex items-center">
                <input
                  type="text"
                  required
                  value={kgid}
                  onChange={(e) => setKgid(e.target.value)}
                  placeholder="Enter your KGID"
                  className={`w-full bg-[#141C28] border rounded-lg py-2 px-3 text-xs text-slate-100 placeholder-slate-500 focus:outline-none transition-all font-mono ${
                    kgidError 
                      ? 'border-rose-500/80 focus:border-rose-500 focus:ring-1 focus:ring-rose-500/30' 
                      : officerData 
                      ? 'border-emerald-700/80 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500/30'
                      : 'border-[#263142] focus:border-[#2F5DA8] focus:ring-1 focus:ring-[#2F5DA8]/50'
                  }`}
                />
              </div>

              {/* KGID Lookup Error Banner */}
              {kgidError && !isVerifying && (
                <div className="flex items-start gap-1.5 text-[11px] text-rose-400 bg-rose-950/30 p-2 rounded-lg border border-rose-900/50 animate-fade-in font-medium mt-1">
                  <AlertTriangle className="w-3.5 h-3.5 shrink-0 mt-0.5" />
                  <span>{kgidError}</span>
                </div>
              )}
            </div>

            {/* Field 2: Officer Name (READ-ONLY, AUTO-POPULATED FROM DB) */}
            <div className="space-y-1">
              <div className="flex items-center justify-between">
                <label className="text-[10.5px] font-mono font-semibold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
                  <User className="w-3 h-3 text-[#93B4E8]" />
                  <span>Officer Name</span>
                </label>
                <span className="text-[9px] font-mono uppercase tracking-wider text-slate-400">
                  Database Verified
                </span>
              </div>

              <div className="relative flex items-center">
                <div className={`w-full bg-[#0E1520] border rounded-lg py-2 px-3 text-xs flex items-center justify-between transition-colors select-none ${
                  officerData 
                    ? 'border-emerald-800/60 text-slate-100 font-semibold' 
                    : 'border-[#263142] text-slate-500 italic'
                }`}>
                  <span className="truncate">
                    {isVerifying ? (
                      <span className="text-slate-400 not-italic flex items-center gap-1.5">
                        <Loader2 className="w-3.5 h-3.5 animate-spin text-[#93B4E8]" />
                        <span>Verifying officer...</span>
                      </span>
                    ) : officerData ? (
                      <span className="text-white font-bold not-italic">
                        {officerData.name}
                      </span>
                    ) : (
                      "Auto-identified upon entering KGID"
                    )}
                  </span>

                  {officerData && !isVerifying && (
                    <span className="flex items-center gap-1 text-[10px] font-mono font-bold text-emerald-400 shrink-0 ml-2">
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                      <span>Verified</span>
                    </span>
                  )}
                </div>
              </div>

              {/* Station & Designation Info */}
              {officerData?.unit && (
                <div className="text-[10px] font-mono text-slate-400 flex items-center gap-1.5 pt-0.5">
                  <span className="text-[#93B4E8]">Station:</span>
                  <span className="text-slate-300 truncate">{officerData.unit}</span>
                  {officerData.designation && (
                    <>
                      <span className="text-slate-600">•</span>
                      <span className="text-slate-400 font-semibold">{officerData.designation}</span>
                    </>
                  )}
                </div>
              )}
            </div>

            {/* Field 3: Password */}
            <div className="space-y-1">
              <label className="text-[10.5px] font-mono font-semibold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
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
                  className="w-full bg-[#141C28] border border-[#263142] rounded-lg py-2 pl-3 pr-10 text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-[#2F5DA8] focus:ring-1 focus:ring-[#2F5DA8]/50 transition-all font-mono"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 p-1 text-slate-400 hover:text-slate-200 transition-colors cursor-pointer"
                  title={showPassword ? "Hide password" : "Show password"}
                  aria-label={showPassword ? "Hide password" : "Show password"}
                >
                  {showPassword ? <EyeOff className="w-3.5 h-3.5" /> : <Eye className="w-3.5 h-3.5" />}
                </button>
              </div>
            </div>

            {/* Authentication Failure Error Banner */}
            {authError && (
              <div className="flex items-start gap-1.5 text-[11px] text-rose-400 bg-rose-950/30 p-2.5 rounded-lg border border-rose-900/50 animate-fade-in font-medium">
                <AlertTriangle className="w-4 h-4 shrink-0 mt-0.5 text-rose-400" />
                <span>{authError}</span>
              </div>
            )}

            {/* Primary Action Button */}
            <button
              type="submit"
              disabled={isAuthenticating || !officerData || isVerifying || !password}
              className="w-full mt-1.5 bg-[#2F5DA8] hover:bg-[#3A6DBD] disabled:bg-[#172640] disabled:text-slate-500 text-white py-2.5 px-4 rounded-xl text-xs font-bold uppercase tracking-wider font-mono shadow-md hover:shadow-lg transition-all flex items-center justify-center gap-2 cursor-pointer disabled:cursor-not-allowed"
            >
              {isAuthenticating ? (
                <>
                  <Loader2 className="w-3.5 h-3.5 animate-spin text-white" />
                  <span>AUTHENTICATING...</span>
                </>
              ) : (
                <>
                  <span>AUTHENTICATE & ENTER</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </>
              )}
            </button>
          </form>

          {/* ============================================================ */}
          {/* NOTICEABLE DEMO ACCESS PANEL WITH INTERACTIVE HOVER GLOW     */}
          {/* ============================================================ */}
          <div className={`mt-4 pt-3 p-3.5 rounded-xl border transition-all duration-300 ${
            isFormHovered 
              ? 'bg-[#152338] border-[#3A6DBD] shadow-[0_0_24px_rgba(59,130,246,0.35)] ring-1 ring-[#3A6DBD]/60' 
              : 'bg-[#141C28]/90 border-[#2F5DA8]/40 shadow-inner'
          }`}>
            {/* Header Badge & Subtitle */}
            <div className="flex items-center justify-between mb-1">
              <div className="flex items-center gap-1.5 text-xs font-bold font-mono tracking-wide">
                <Sparkles className={`w-3.5 h-3.5 transition-colors ${isFormHovered ? 'text-cyan-300 animate-pulse' : 'text-[#93B4E8]'}`} />
                <span className={`transition-colors ${isFormHovered ? 'text-cyan-200 drop-shadow-[0_0_8px_rgba(56,189,248,0.5)]' : 'text-[#93B4E8]'}`}>
                  FIRST TIME HERE?
                </span>
              </div>
              <span className={`text-[9px] font-mono px-1.5 py-0.2 rounded uppercase font-bold transition-all ${
                isFormHovered 
                  ? 'bg-[#1e3458] text-cyan-200 border border-[#3A6DBD]' 
                  : 'bg-[#172640] text-[#93B4E8] border border-[#263142]'
              }`}>
                Demo
              </span>
            </div>
            
            <p className="text-[10.5px] text-slate-300 leading-tight mb-2.5">
              Use Demo Access to explore Aloka Intelligence.
            </p>

            {/* Officer Selection Buttons */}
            <div className="space-y-1.5 mb-2.5">
              <span className="text-[9px] font-mono uppercase tracking-widest text-slate-400 font-bold block">
                SELECT DEMO OFFICER
              </span>
              <div className="grid grid-cols-3 gap-1.5">
                {DEMO_OFFICERS.map((officer) => {
                  const isSelected = kgid === officer.kgid;
                  return (
                    <button
                      key={officer.id}
                      type="button"
                      onClick={() => handleSelectDemoOfficer(officer.kgid)}
                      className={`flex flex-col items-center justify-center p-2 rounded-lg border transition-all cursor-pointer text-center ${
                        isSelected 
                          ? 'bg-[#172640] border-[#3A6DBD] text-white ring-1 ring-[#3A6DBD]/60 shadow-xs' 
                          : isFormHovered
                          ? 'bg-[#101722] border-[#2d3e58] text-slate-200 hover:border-[#3A6DBD] hover:bg-[#192b45]'
                          : 'bg-[#101722] border-[#263142] text-slate-300 hover:border-[#2F5DA8] hover:bg-[#141C28]'
                      }`}
                    >
                      <div className="flex items-center gap-1 mb-0.5">
                        <UserCheck className={`w-3 h-3 ${isSelected ? 'text-[#93B4E8]' : isFormHovered ? 'text-cyan-300' : 'text-slate-400'}`} />
                        <span className="text-[11px] font-bold tracking-tight">
                          {officer.name}
                        </span>
                      </div>
                      <span className="text-[9px] font-mono text-slate-400">
                        {officer.kgid}
                      </span>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Demo Password Info */}
            <div className="flex items-center justify-between text-[10px] font-mono text-slate-300 pt-2 border-t border-[#263142]/80">
              <div className="flex items-center gap-1.5">
                <KeyRound className={`w-3 h-3 transition-colors ${isFormHovered ? 'text-cyan-300' : 'text-[#93B4E8]'}`} />
                <span className="text-slate-400">Demo Password:</span>
              </div>
              <code className={`px-2 py-0.5 rounded border font-bold transition-all ${
                isFormHovered 
                  ? 'bg-[#101722] border-[#3A6DBD] text-cyan-200 shadow-[0_0_8px_rgba(56,189,248,0.25)]' 
                  : 'bg-[#101722] border-[#263142] text-[#93B4E8]'
              }`}>
                KGID@123
              </code>
            </div>
          </div>

        </section>


        {/* ============================================================ */}
        {/* RIGHT SIDE: ALOKA WELCOME & OVERVIEW (55-60% on Desktop)    */}
        {/* ============================================================ */}
        <section className="w-full lg:w-[580px] max-w-2xl flex flex-col justify-center py-2">
          
          {/* 1. Animated Logo */}
          <div className="flex items-center gap-3.5 mb-3.5 anim-init-logo">
            <div className="w-12 h-12 sm:w-13 sm:h-13 rounded-2xl bg-[#101722] border border-[#263142] p-2 flex items-center justify-center shadow-lg shrink-0">
              <img 
                src="https://upload.wikimedia.org/wikipedia/commons/a/aa/Seal_of_Karnataka.svg" 
                alt="Seal of Karnataka State Police" 
                className="w-full h-full object-contain drop-shadow-md"
              />
            </div>
            
            <div className="flex flex-col">
              <div className="flex items-center gap-2 anim-init-title">
                <h1 className="text-xl sm:text-2xl font-black text-white tracking-wider font-mono uppercase">
                  ALOKA INTELLIGENCE
                </h1>
                <span className="px-1.5 py-0.5 rounded text-[8.5px] font-bold font-mono bg-[#172640] text-[#93B4E8] border border-[#263142] tracking-widest uppercase">
                  KSP
                </span>
              </div>

              <span className="text-[10.5px] font-mono font-bold uppercase tracking-widest text-[#93B4E8] anim-init-subtitle">
                STATE INTELLIGENCE COMMAND CENTER
              </span>
            </div>
          </div>

          {/* 2. Welcome Message */}
          <div className="mb-4 anim-init-welcome">
            <h2 className="text-base sm:text-lg font-bold text-slate-100 mb-1 tracking-tight">
              Welcome to Aloka Intelligence
            </h2>
            <p className="text-xs sm:text-[13px] text-slate-400 leading-relaxed max-w-xl">
              An AI-powered intelligence assistant for exploring and understanding Karnataka State criminological data.
            </p>
          </div>

          {/* 3. Capability Indicators */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5 max-w-xl">
            {CAPABILITIES.map((cap, idx) => {
              const Icon = cap.icon;
              return (
                <div 
                  key={idx}
                  className={`flex items-start gap-2.5 p-2 rounded-xl bg-[#101722]/90 border border-[#263142] hover:border-[#2F5DA8] transition-all group ${cap.animClass}`}
                >
                  <div className="p-1.5 rounded-lg bg-[#141C28] text-[#93B4E8] group-hover:text-white group-hover:bg-[#2F5DA8] transition-colors shrink-0 mt-0.5 border border-[#263142]">
                    <Icon className="w-3.5 h-3.5" />
                  </div>
                  <div className="flex flex-col">
                    <span className="text-[11.5px] font-bold text-slate-200 group-hover:text-white transition-colors">
                      {cap.title}
                    </span>
                    <span className="text-[9.5px] text-slate-400 line-clamp-1 leading-normal">
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
      <footer className="w-full h-8 border-t border-[#263142] px-4 sm:px-8 flex items-center justify-between bg-[#101722]/90 text-[9.5px] font-mono text-slate-400 uppercase tracking-wider shrink-0 z-20">
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

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
  BarChart3, 
  Globe, 
  Activity,
  Check,
  Sparkles,
  KeyRound,
  UserCheck
} from 'lucide-react';

const SYSTEM_CAPABILITIES = [
  {
    title: "CASE INTELLIGENCE",
    desc: "Search and understand FIRs, accused, victims, officers and case information.",
    icon: FolderSearch
  },
  {
    title: "DATA ANALYSIS",
    desc: "Explore case trends, distributions, rankings and database-driven insights.",
    icon: BarChart3
  },
  {
    title: "INTELLIGENT ASSISTANCE",
    desc: "Ask questions naturally in English, Hindi or Kannada and receive contextual answers.",
    icon: Globe
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
    <div className="h-screen w-full bg-[#EBF0F7] text-slate-800 flex flex-col justify-between overflow-x-hidden overflow-y-auto lg:overflow-hidden selection:bg-blue-700 selection:text-white">
      {/* Top High-Contrast Status Bar */}
      <header className="w-full h-11 border-b border-slate-300/80 px-4 sm:px-8 flex items-center justify-between bg-white/95 backdrop-blur-md shrink-0 z-20 shadow-xs">
        <div className="flex items-center gap-2.5">
          <img 
            src="https://upload.wikimedia.org/wikipedia/commons/a/aa/Seal_of_Karnataka.svg" 
            alt="Karnataka Police Emblem" 
            className="w-5 h-5 sm:w-6 sm:h-6 object-contain drop-shadow-xs"
          />
          <span className="text-[11px] sm:text-xs font-mono font-black tracking-wider text-slate-900 uppercase">
            KARNATAKA STATE POLICE
          </span>
          <span className="hidden sm:inline-block text-slate-400 font-bold">|</span>
          <span className="hidden sm:inline-block text-[10px] font-mono font-bold text-slate-600 uppercase tracking-widest">
            STATE INTELLIGENCE PORTAL
          </span>
        </div>

        <div className="flex items-center gap-2 text-[10px] font-mono font-black text-emerald-800 bg-emerald-100/90 px-3 py-0.5 rounded-full border border-emerald-300 shadow-xs">
          <span className="w-2 h-2 rounded-full bg-emerald-600 animate-pulse"></span>
          <span>SYSTEM ONLINE</span>
        </div>
      </header>

      {/* Main Split-Screen Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-2 sm:py-4 flex flex-col lg:flex-row items-center justify-center gap-6 lg:gap-14 z-10">
        
        {/* ============================================================ */}
        {/* LEFT SIDE: OFFICER LOGIN PANEL (40-45% on Desktop)          */}
        {/* ============================================================ */}
        <section 
          onMouseEnter={() => setIsFormHovered(true)}
          onMouseLeave={() => setIsFormHovered(false)}
          className="w-full lg:w-[440px] max-w-md bg-white border-2 border-slate-300 rounded-2xl p-5 sm:p-6 shadow-[0_20px_45px_rgba(15,23,42,0.12)] relative shrink-0 transition-all duration-300"
        >
          {/* Top Form Header */}
          <div className="mb-3.5 pb-2.5 border-b-2 border-slate-100">
            <div className="flex items-center gap-1.5 text-[10.5px] font-mono font-extrabold uppercase tracking-wider text-blue-800 bg-blue-100/80 px-2.5 py-1 rounded-md w-fit border border-blue-300 mb-2">
              <Shield className="w-3.5 h-3.5 text-blue-700 stroke-[2.5]" />
              <span>OFFICER AUTHENTICATION</span>
            </div>
            
            <h2 className="text-xl font-black text-slate-900 font-mono tracking-tight uppercase">
              ALOKA INTELLIGENCE
            </h2>
            <p className="text-xs font-medium text-slate-600 mt-0.5">
              Authorized personnel access
            </p>
          </div>

          {/* Authentication Form */}
          <form onSubmit={handleSubmit} className="space-y-3.5">
            
            {/* Field 1: KGID Input */}
            <div className="space-y-1">
              <div className="flex items-center justify-between">
                <label className="text-[11px] font-mono font-bold text-slate-800 uppercase tracking-wider flex items-center gap-1.5">
                  <Shield className="w-3.5 h-3.5 text-blue-700" />
                  <span>KGID</span>
                </label>
                {isVerifying && (
                  <span className="flex items-center gap-1 text-[10px] font-mono font-bold text-blue-700 animate-pulse">
                    <Loader2 className="w-3.5 h-3.5 animate-spin" />
                    <span>Verifying officer...</span>
                  </span>
                )}
                {officerData && !isVerifying && (
                  <span className="flex items-center gap-1 text-[10px] font-mono font-black text-emerald-800 bg-emerald-100 px-2 py-0.5 rounded border border-emerald-300">
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
                  className={`w-full bg-slate-50 border-2 rounded-xl py-2 px-3 text-xs text-slate-900 font-semibold placeholder-slate-500 focus:bg-white focus:outline-none transition-all font-mono shadow-xs ${
                    kgidError 
                      ? 'border-rose-500 focus:border-rose-600 focus:ring-4 focus:ring-rose-100' 
                      : officerData 
                      ? 'border-emerald-600 focus:border-emerald-700 focus:ring-4 focus:ring-emerald-100'
                      : 'border-slate-300 focus:border-blue-700 focus:ring-4 focus:ring-blue-100'
                  }`}
                />
              </div>

              {/* KGID Lookup Error Banner */}
              {kgidError && !isVerifying && (
                <div className="flex items-start gap-1.5 text-xs text-rose-800 bg-rose-100/90 p-2.5 rounded-xl border border-rose-300 animate-fade-in font-semibold mt-1">
                  <AlertTriangle className="w-4 h-4 shrink-0 mt-0.5 text-rose-700" />
                  <span>{kgidError}</span>
                </div>
              )}
            </div>

            {/* Field 2: Officer Name (READ-ONLY, AUTO-POPULATED FROM DB) */}
            <div className="space-y-1">
              <div className="flex items-center justify-between">
                <label className="text-[11px] font-mono font-bold text-slate-800 uppercase tracking-wider flex items-center gap-1.5">
                  <User className="w-3.5 h-3.5 text-blue-700" />
                  <span>Officer Name</span>
                </label>
                <span className="text-[9.5px] font-mono uppercase tracking-wider text-slate-500 font-bold">
                  Database Verified
                </span>
              </div>

              <div className="relative flex items-center">
                <div className={`w-full border-2 rounded-xl py-2 px-3 text-xs flex items-center justify-between transition-colors select-none shadow-xs ${
                  officerData 
                    ? 'border-emerald-500 text-slate-900 font-bold bg-emerald-50/70' 
                    : 'border-slate-200 text-slate-500 bg-slate-100/90 font-medium'
                }`}>
                  <span className="truncate">
                    {isVerifying ? (
                      <span className="text-slate-600 font-semibold not-italic flex items-center gap-1.5">
                        <Loader2 className="w-3.5 h-3.5 animate-spin text-blue-700" />
                        <span>Verifying officer...</span>
                      </span>
                    ) : officerData ? (
                      <span className="text-slate-950 font-black not-italic text-[12.5px]">
                        {officerData.name}
                      </span>
                    ) : (
                      "Auto-identified upon entering KGID"
                    )}
                  </span>

                  {officerData && !isVerifying && (
                    <span className="flex items-center gap-1 text-[10px] font-mono font-black text-emerald-800 bg-emerald-100 px-2 py-0.5 rounded border border-emerald-300 shrink-0 ml-2">
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-700" />
                      <span>Verified</span>
                    </span>
                  )}
                </div>
              </div>

              {/* Station & Designation Info */}
              {officerData?.unit && (
                <div className="text-[10.5px] font-mono text-slate-600 flex items-center gap-1.5 pt-0.5 font-medium">
                  <span className="text-blue-800 font-bold">Station:</span>
                  <span className="text-slate-800 font-semibold truncate">{officerData.unit}</span>
                  {officerData.designation && (
                    <>
                      <span className="text-slate-400 font-black">•</span>
                      <span className="text-slate-700 font-bold">{officerData.designation}</span>
                    </>
                  )}
                </div>
              )}
            </div>

            {/* Field 3: Password */}
            <div className="space-y-1">
              <label className="text-[11px] font-mono font-bold text-slate-800 uppercase tracking-wider flex items-center gap-1.5">
                <Lock className="w-3.5 h-3.5 text-blue-700" />
                <span>Password</span>
              </label>
              <div className="relative flex items-center">
                <input
                  type={showPassword ? "text" : "password"}
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter your password"
                  className="w-full bg-slate-50 border-2 border-slate-300 rounded-xl py-2 pl-3 pr-10 text-xs text-slate-900 font-semibold placeholder-slate-500 focus:bg-white focus:outline-none focus:border-blue-700 focus:ring-4 focus:ring-blue-100 transition-all font-mono shadow-xs"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 p-1 text-slate-500 hover:text-slate-800 transition-colors cursor-pointer"
                  title={showPassword ? "Hide password" : "Show password"}
                  aria-label={showPassword ? "Hide password" : "Show password"}
                >
                  {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </div>

            {/* Authentication Failure Error Banner */}
            {authError && (
              <div className="flex items-start gap-1.5 text-xs text-rose-800 bg-rose-100 p-2.5 rounded-xl border border-rose-300 animate-fade-in font-bold">
                <AlertTriangle className="w-4 h-4 shrink-0 mt-0.5 text-rose-700" />
                <span>{authError}</span>
              </div>
            )}

            {/* Primary Action Button */}
            <button
              type="submit"
              disabled={isAuthenticating || !officerData || isVerifying || !password}
              className="w-full mt-1 bg-blue-700 hover:bg-blue-800 disabled:bg-slate-300 disabled:text-slate-600 disabled:border-slate-300 text-white py-2.5 px-4 rounded-xl text-xs font-black uppercase tracking-wider font-mono shadow-md hover:shadow-lg transition-all flex items-center justify-center gap-2 cursor-pointer disabled:cursor-not-allowed border border-blue-800"
            >
              {isAuthenticating ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin text-white" />
                  <span>AUTHENTICATING...</span>
                </>
              ) : (
                <>
                  <span>AUTHENTICATE & ENTER</span>
                  <ArrowRight className="w-4 h-4 stroke-[2.5]" />
                </>
              )}
            </button>
          </form>

          {/* ============================================================ */}
          {/* HIGH-CONTRAST DEMO ACCESS PANEL WITH PROMINENT DESIGN        */}
          {/* ============================================================ */}
          <div className={`mt-4 pt-3 p-3.5 rounded-xl border-2 transition-all duration-300 ${
            isFormHovered 
              ? 'bg-blue-50/95 border-blue-500 shadow-[0_0_24px_rgba(37,99,235,0.25)] ring-2 ring-blue-300' 
              : 'bg-slate-100/90 border-slate-300 shadow-xs'
          }`}>
            {/* Header Badge & Subtitle */}
            <div className="flex items-center justify-between mb-1.5">
              <div className="flex items-center gap-1.5 text-xs font-black font-mono tracking-wide">
                <Sparkles className={`w-4 h-4 transition-colors ${isFormHovered ? 'text-blue-700 animate-pulse' : 'text-blue-700'}`} />
                <span className={`transition-colors ${isFormHovered ? 'text-blue-950 font-black' : 'text-blue-900'}`}>
                  FIRST TIME HERE?
                </span>
              </div>
              <span className={`text-[9.5px] font-mono px-2 py-0.5 rounded-md uppercase font-black transition-all ${
                isFormHovered 
                  ? 'bg-blue-700 text-white border border-blue-800' 
                  : 'bg-blue-100 text-blue-900 border border-blue-300'
              }`}>
                Demo Access
              </span>
            </div>
            
            <p className="text-xs text-slate-700 leading-tight mb-2.5 font-semibold">
              Use Demo Access to explore Aloka Intelligence.
            </p>

            {/* Officer Selection Buttons */}
            <div className="space-y-1.5 mb-2.5">
              <span className="text-[9.5px] font-mono uppercase tracking-widest text-slate-600 font-extrabold block">
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
                      className={`flex flex-col items-center justify-center p-2 rounded-xl border-2 transition-all cursor-pointer text-center ${
                        isSelected 
                          ? 'bg-blue-700 border-blue-800 text-white shadow-md font-bold ring-2 ring-blue-300' 
                          : isFormHovered
                          ? 'bg-white border-blue-300 text-slate-900 hover:border-blue-600 hover:bg-blue-50/80 shadow-xs'
                          : 'bg-white border-slate-300 text-slate-800 hover:border-blue-500 hover:bg-blue-50/40 shadow-xs'
                      }`}
                    >
                      <div className="flex items-center gap-1 mb-0.5">
                        <UserCheck className={`w-3.5 h-3.5 ${isSelected ? 'text-white' : 'text-blue-700'}`} />
                        <span className="text-xs font-bold tracking-tight">
                          {officer.name}
                        </span>
                      </div>
                      <span className={`text-[9.5px] font-mono font-semibold ${isSelected ? 'text-blue-100' : 'text-slate-600'}`}>
                        {officer.kgid}
                      </span>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Demo Password Info */}
            <div className="flex items-center justify-between text-xs font-mono text-slate-800 pt-2 border-t-2 border-slate-200">
              <div className="flex items-center gap-1.5 font-bold">
                <KeyRound className="w-3.5 h-3.5 text-blue-700" />
                <span className="text-slate-600">Demo Password:</span>
              </div>
              <code className="bg-white px-2.5 py-0.5 rounded-lg border-2 border-blue-300 text-blue-900 font-black shadow-xs">
                KGID@123
              </code>
            </div>
          </div>

        </section>


        {/* ============================================================ */}
        {/* RIGHT SIDE: STATE INTELLIGENCE COMMAND CENTER INTRODUCTION  */}
        {/* ============================================================ */}
        <section className="w-full lg:w-[520px] max-w-lg flex flex-col justify-center py-2">
          
          {/* Official Karnataka Police Branding Header */}
          <div className="flex items-center gap-3.5 mb-4">
            <div className="w-12 h-12 sm:w-13 sm:h-13 rounded-2xl bg-white border-2 border-slate-300 p-2 flex items-center justify-center shadow-md shrink-0">
              <img 
                src="https://upload.wikimedia.org/wikipedia/commons/a/aa/Seal_of_Karnataka.svg" 
                alt="Seal of Karnataka State Police" 
                className="w-full h-full object-contain drop-shadow-xs"
              />
            </div>
            
            <div className="flex flex-col">
              <div className="flex items-center gap-2">
                <h1 className="text-xl sm:text-2xl font-black text-slate-900 tracking-wider font-mono uppercase">
                  ALOKA INTELLIGENCE
                </h1>
                <span className="px-1.5 py-0.5 rounded text-[9px] font-black font-mono bg-blue-100 text-blue-800 border border-blue-300 tracking-widest uppercase shadow-2xs">
                  KSP
                </span>
              </div>

              <span className="text-[11px] font-mono font-extrabold uppercase tracking-widest text-blue-800">
                STATE INTELLIGENCE COMMAND CENTER
              </span>
            </div>
          </div>

          {/* Welcome Message */}
          <div className="mb-4">
            <h2 className="text-base sm:text-lg font-black text-slate-900 mb-1 tracking-tight">
              Welcome to Aloka
            </h2>
            <p className="text-xs sm:text-[13px] text-slate-700 leading-relaxed font-medium">
              An AI-powered intelligence assistant for exploring and understanding Karnataka State criminological data.
            </p>
          </div>

          {/* Institutional Overview: WHAT ALOKA PROVIDES */}
          <div className="space-y-2.5">
            <div className="flex items-center gap-2 pb-1 border-b border-slate-300">
              <Shield className="w-3.5 h-3.5 text-blue-700" />
              <span className="text-[10.5px] font-mono font-black uppercase tracking-widest text-slate-700">
                WHAT ALOKA PROVIDES
              </span>
            </div>

            <div className="space-y-2">
              {SYSTEM_CAPABILITIES.map((item, idx) => {
                const Icon = item.icon;
                return (
                  <div 
                    key={idx}
                    className="flex items-start gap-3 p-3 rounded-xl bg-white/95 border border-slate-300 shadow-2xs hover:border-slate-400 transition-colors"
                  >
                    <div className="p-2 rounded-lg bg-blue-50 text-blue-800 border border-blue-200 shrink-0 mt-0.5">
                      <Icon className="w-4 h-4 stroke-[2.2]" />
                    </div>
                    <div className="flex flex-col">
                      <span className="text-xs font-mono font-black text-slate-900 tracking-wide uppercase">
                        {item.title}
                      </span>
                      <span className="text-[11px] text-slate-600 font-medium leading-normal mt-0.5">
                        {item.desc}
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

        </section>
      </main>

      {/* Bottom Institutional Footer */}
      <footer className="w-full h-8 border-t border-slate-300 px-4 sm:px-8 flex items-center justify-between bg-white/95 text-[10px] font-mono text-slate-600 uppercase tracking-wider shrink-0 z-20 shadow-xs font-bold">
        <div className="flex items-center gap-2 text-slate-700">
          <Shield className="w-3.5 h-3.5 text-blue-700" />
          <span>KSP STATE CRIMINOLOGICAL DATABASE</span>
        </div>
        
        <div className="flex items-center gap-2 text-emerald-800 font-extrabold">
          <Activity className="w-3.5 h-3.5 text-emerald-600" />
          <span>SYSTEM SECURE & OPERATIONAL</span>
        </div>
      </footer>
    </div>
  );
}

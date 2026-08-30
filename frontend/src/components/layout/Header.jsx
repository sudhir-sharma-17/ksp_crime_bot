import React from 'react';
import { Sun, Moon, Shield, Database, Globe, MessageSquare, LayoutDashboard, Menu, Lock } from 'lucide-react';

export default function Header({
  isDarkMode,
  setIsDarkMode,
  activeTab,
  setActiveTab,
  hasDataOnCanvas,
  selectedLanguage,
  setSelectedLanguage,
  sidebarOpen,
  setSidebarOpen,
  officerProfile,
  onLogout
}) {
  return (
    <header className="h-14 bg-white dark:bg-[#101722] border-b border-slate-300/80 dark:border-[#263142] flex items-center justify-between px-3 sm:px-5 shrink-0 z-30 transition-colors duration-200 shadow-2xs">
      {/* Left: Sidebar Toggle + Emblem + Title */}
      <div className="flex items-center gap-2.5 sm:gap-3">
        {/* Mobile / Tablet Sidebar Toggle */}
        <button
          type="button"
          onClick={() => setSidebarOpen(!sidebarOpen)}
          className="p-1.5 rounded-lg text-slate-600 hover:text-slate-900 dark:text-slate-400 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-[#141C28] md:hidden cursor-pointer border border-slate-200 dark:border-transparent"
          title="Toggle Sessions Sidebar"
          aria-label="Toggle Sessions Sidebar"
        >
          <Menu className="w-4 h-4" />
        </button>

        <div className="relative flex items-center justify-center shrink-0">
          <img 
            src="https://upload.wikimedia.org/wikipedia/commons/a/aa/Seal_of_Karnataka.svg" 
            alt="Karnataka State Police Emblem" 
            className="w-8 h-8 sm:w-9 sm:h-9 object-contain drop-shadow-2xs"
          />
        </div>

        <div className="flex flex-col">
          <div className="flex items-center gap-1.5">
            <span className="text-xs sm:text-sm font-black tracking-wider text-slate-950 dark:text-slate-100 uppercase font-mono">
              ALOKA INTELLIGENCE
            </span>
            <span className="hidden sm:inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-[9.5px] font-black bg-blue-50 dark:bg-[#172640] text-blue-800 dark:text-[#93B4E8] border border-blue-200 dark:border-[#263142] tracking-wider font-mono">
              <Shield className="w-2.5 h-2.5 text-blue-700 dark:text-[#93B4E8]" />
              KSP
            </span>
          </div>
          <span className="text-[9.5px] font-bold text-blue-800 dark:text-slate-400 uppercase tracking-widest leading-none">
            COMMAND CENTER
          </span>
        </div>
      </div>

      {/* Center: Mobile View Switcher (Chat vs Canvas) */}
      <div className="flex md:hidden items-center bg-slate-100 dark:bg-[#0B1017] p-0.5 rounded-lg border border-slate-300 dark:border-[#263142]">
        <button
          type="button"
          onClick={() => setActiveTab('chat')}
          className={`flex items-center gap-1 px-2.5 py-1 rounded-md text-xs font-bold transition-all ${
            activeTab === 'chat'
              ? 'bg-white dark:bg-[#141C28] text-blue-700 dark:text-[#93B4E8] shadow-xs'
              : 'text-slate-600 hover:text-slate-900 dark:text-slate-400'
          }`}
          aria-label="Switch to Chat view"
        >
          <MessageSquare className="w-3 h-3" />
          <span>Chat</span>
        </button>
        <button
          type="button"
          onClick={() => setActiveTab('canvas')}
          className={`flex items-center gap-1 px-2.5 py-1 rounded-md text-xs font-bold transition-all relative ${
            activeTab === 'canvas'
              ? 'bg-white dark:bg-[#141C28] text-blue-700 dark:text-[#93B4E8] shadow-xs'
              : 'text-slate-600 hover:text-slate-900 dark:text-slate-400'
          }`}
          aria-label="Switch to Data Canvas view"
        >
          <LayoutDashboard className="w-3 h-3" />
          <span>Canvas</span>
          {hasDataOnCanvas && (
            <span className="w-1.5 h-1.5 rounded-full bg-blue-600"></span>
          )}
        </button>
      </div>

      {/* Right: Operational Status + Officer Profile + Language + Theme Toggle + Lock */}
      <div className="flex items-center gap-2 sm:gap-2.5">
        {/* Status Indicators */}
        <div className="hidden lg:flex items-center gap-2 border-r border-slate-300 dark:border-[#263142] pr-3">
          <div className="flex items-center gap-1.5 text-[10.5px] font-mono font-black text-emerald-800 dark:text-emerald-400 bg-emerald-50 dark:bg-[#102619] px-2.5 py-0.5 rounded-full border border-emerald-300 dark:border-emerald-900/60 shadow-2xs">
            <span className="w-2 h-2 rounded-full bg-emerald-600 animate-pulse"></span>
            <span>SYSTEM ONLINE</span>
          </div>

          <div className="flex items-center gap-1.5 text-[10.5px] font-mono font-bold text-slate-800 dark:text-[#93B4E8] bg-slate-100 dark:bg-[#132233] px-2.5 py-0.5 rounded-full border border-slate-300 dark:border-[#263142]">
            <Database className="w-3 h-3 text-blue-700 dark:text-[#93B4E8]" />
            <span>DATABASE CONNECTED</span>
          </div>
        </div>

        {/* Officer Badge */}
        {officerProfile?.name && (
          <div className="hidden xl:flex items-center gap-1.5 text-[11px] font-mono text-slate-900 dark:text-slate-200 bg-blue-50/90 dark:bg-[#141C28] px-3 py-1 rounded-xl border border-blue-200 dark:border-[#263142] shadow-xs">
            <span className="w-2 h-2 rounded-full bg-blue-600"></span>
            <span className="font-extrabold text-blue-950 dark:text-slate-100">{officerProfile.name}</span>
            <span className="text-slate-500 font-semibold">({officerProfile.kgid})</span>
          </div>
        )}

        {/* Global Language Selector */}
        <div className="flex items-center gap-1 bg-slate-100 dark:bg-[#141C28] px-2.5 py-1 rounded-xl border border-slate-300 dark:border-[#263142] text-xs text-slate-800 dark:text-slate-300 shadow-2xs">
          <Globe className="w-3.5 h-3.5 text-blue-700 dark:text-slate-400 shrink-0" />
          <select
            value={selectedLanguage || 'en'}
            onChange={(e) => setSelectedLanguage?.(e.target.value)}
            className="bg-transparent border-none text-xs font-bold focus:ring-0 cursor-pointer outline-none text-slate-800 dark:text-slate-200"
            aria-label="Select Interface Language"
          >
            <option value="en" className="bg-white dark:bg-[#101722] text-slate-900 dark:text-slate-100">English</option>
            <option value="kn" className="bg-white dark:bg-[#101722] text-slate-900 dark:text-slate-100">ಕನ್ನಡ (Kannada)</option>
            <option value="hi" className="bg-white dark:bg-[#101722] text-slate-900 dark:text-slate-100">हिन्दी (Hindi)</option>
          </select>
        </div>

        {/* Theme Toggle Button */}
        <button
          type="button"
          onClick={() => setIsDarkMode(!isDarkMode)}
          className="p-1.5 rounded-xl text-slate-700 hover:text-slate-950 dark:text-slate-400 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-[#141C28] border border-slate-300 dark:border-[#263142] transition-colors cursor-pointer shadow-2xs"
          title={isDarkMode ? "Switch to Light Mode" : "Switch to Dark Mode"}
          aria-label={isDarkMode ? "Switch to Light Mode" : "Switch to Dark Mode"}
        >
          {isDarkMode ? (
            <Sun className="w-4 h-4 text-amber-400" />
          ) : (
            <Moon className="w-4 h-4 text-slate-700" />
          )}
        </button>

        {/* Officer Logout / Lock Icon Button */}
        {onLogout && (
          <button
            type="button"
            onClick={onLogout}
            className="p-1.5 rounded-xl text-slate-600 hover:text-rose-700 dark:text-slate-400 dark:hover:text-rose-400 hover:bg-rose-50 dark:hover:bg-rose-950/40 border border-slate-300 dark:border-[#263142] transition-colors cursor-pointer shadow-2xs"
            title="Lock Session / Logout"
            aria-label="Lock Session / Logout"
          >
            <Lock className="w-4 h-4" />
          </button>
        )}
      </div>
    </header>
  );
}

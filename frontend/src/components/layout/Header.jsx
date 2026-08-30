import React from 'react';
import { Sun, Moon, Shield, Database, Globe, MessageSquare, LayoutDashboard, Menu } from 'lucide-react';

export default function Header({
  isDarkMode,
  setIsDarkMode,
  activeTab,
  setActiveTab,
  hasDataOnCanvas,
  selectedLanguage,
  setSelectedLanguage,
  sidebarOpen,
  setSidebarOpen
}) {
  return (
    <header className="h-14 bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800/90 flex items-center justify-between px-3 sm:px-5 shrink-0 shadow-xs z-30 transition-colors duration-200">
      {/* Left: Sidebar Toggle + Emblem + Title */}
      <div className="flex items-center gap-2.5 sm:gap-3">
        {/* Mobile / Tablet Sidebar Toggle */}
        <button
          type="button"
          onClick={() => setSidebarOpen(!sidebarOpen)}
          className="p-1.5 rounded-lg text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 md:hidden cursor-pointer"
          title="Toggle Sessions Sidebar"
          aria-label="Toggle Sessions Sidebar"
        >
          <Menu className="w-4 h-4" />
        </button>

        <div className="relative flex items-center justify-center shrink-0">
          <img 
            src="https://upload.wikimedia.org/wikipedia/commons/a/aa/Seal_of_Karnataka.svg" 
            alt="Karnataka State Police Emblem" 
            className="w-8 h-8 sm:w-9 sm:h-9 object-contain drop-shadow-xs"
          />
        </div>

        <div className="flex flex-col">
          <div className="flex items-center gap-1.5">
            <span className="text-xs sm:text-sm font-black tracking-wider text-slate-900 dark:text-slate-100 uppercase font-mono">
              ALOKA INTELLIGENCE
            </span>
            <span className="hidden sm:inline-flex items-center gap-1 px-1.5 py-0.2 rounded text-[9px] font-bold bg-blue-100 dark:bg-blue-950 text-blue-800 dark:text-cyan-300 border border-blue-200 dark:border-blue-800/60 tracking-wider font-mono">
              <Shield className="w-2.5 h-2.5 text-blue-600 dark:text-cyan-400" />
              KSP
            </span>
          </div>
          <span className="text-[9px] font-bold text-slate-500 dark:text-slate-400 uppercase tracking-widest leading-none">
            COMMAND CENTER
          </span>
        </div>
      </div>

      {/* Center: Mobile View Switcher (Chat vs Canvas) */}
      <div className="flex md:hidden items-center bg-slate-100 dark:bg-slate-800 p-0.5 rounded-lg border border-slate-200 dark:border-slate-700">
        <button
          type="button"
          onClick={() => setActiveTab('chat')}
          className={`flex items-center gap-1 px-2.5 py-1 rounded-md text-xs font-bold transition-all ${
            activeTab === 'chat'
              ? 'bg-white dark:bg-slate-900 text-blue-600 dark:text-cyan-400 shadow-xs'
              : 'text-slate-500 hover:text-slate-700 dark:text-slate-400'
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
              ? 'bg-white dark:bg-slate-900 text-blue-600 dark:text-cyan-400 shadow-xs'
              : 'text-slate-500 hover:text-slate-700 dark:text-slate-400'
          }`}
          aria-label="Switch to Data Canvas view"
        >
          <LayoutDashboard className="w-3 h-3" />
          <span>Canvas</span>
          {hasDataOnCanvas && (
            <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-ping"></span>
          )}
        </button>
      </div>

      {/* Right: Operational Status + Language + Theme Toggle */}
      <div className="flex items-center gap-2 sm:gap-3">
        {/* Status Indicators */}
        <div className="hidden lg:flex items-center gap-2.5 border-r border-slate-200 dark:border-slate-800 pr-3">
          <div className="flex items-center gap-1.5 text-[10px] font-mono font-bold text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/40 px-2 py-0.5 rounded border border-emerald-200 dark:border-emerald-900/60">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
            <span>SYSTEM ONLINE</span>
          </div>

          <div className="flex items-center gap-1.5 text-[10px] font-mono font-bold text-cyan-700 dark:text-cyan-400 bg-cyan-50 dark:bg-cyan-950/40 px-2 py-0.5 rounded border border-cyan-200 dark:border-cyan-900/60">
            <Database className="w-2.5 h-2.5 text-cyan-600 dark:text-cyan-400" />
            <span>DATABASE CONNECTED</span>
          </div>
        </div>

        {/* Global Language Selector */}
        <div className="flex items-center gap-1 bg-slate-100 dark:bg-slate-800 px-2 py-1 rounded-lg border border-slate-200 dark:border-slate-700/80 text-xs text-slate-700 dark:text-slate-300">
          <Globe className="w-3.5 h-3.5 text-slate-500 dark:text-slate-400 shrink-0" />
          <select
            value={selectedLanguage || 'en'}
            onChange={(e) => setSelectedLanguage?.(e.target.value)}
            className="bg-transparent border-none text-xs font-semibold focus:ring-0 cursor-pointer outline-none text-slate-700 dark:text-slate-200"
            aria-label="Select Interface Language"
          >
            <option value="en" className="dark:bg-slate-900 text-slate-900 dark:text-slate-100">English</option>
            <option value="kn" className="dark:bg-slate-900 text-slate-900 dark:text-slate-100">ಕನ್ನಡ (Kannada)</option>
            <option value="hi" className="dark:bg-slate-900 text-slate-900 dark:text-slate-100">हिन्दी (Hindi)</option>
          </select>
        </div>

        {/* Theme Toggle Button */}
        <button
          type="button"
          onClick={() => setIsDarkMode(!isDarkMode)}
          className="p-1.5 rounded-lg bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-amber-400 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors border border-slate-200 dark:border-slate-700/80 cursor-pointer shadow-xs"
          title={isDarkMode ? "Switch to Government Light Mode" : "Switch to Intelligence Dark Mode"}
          aria-label="Toggle Theme"
        >
          {isDarkMode ? (
            <Sun className="w-4 h-4 text-amber-400" />
          ) : (
            <Moon className="w-4 h-4 text-slate-600" />
          )}
        </button>
      </div>
    </header>
  );
}

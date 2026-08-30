import React from 'react';
import { Sun, Moon, Shield, Radio, Database, LayoutDashboard, MessageSquare } from 'lucide-react';

export default function Header({
  isDarkMode,
  setIsDarkMode,
  activeTab,
  setActiveTab,
  hasDataOnCanvas
}) {
  return (
    <header className="h-16 bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between px-4 sm:px-6 shrink-0 shadow-xs z-30 transition-colors duration-300">
      {/* Left: Police Emblem & Title */}
      <div className="flex items-center gap-3">
        <div className="relative flex items-center justify-center">
          <img 
            src="https://upload.wikimedia.org/wikipedia/commons/a/aa/Seal_of_Karnataka.svg" 
            alt="Karnataka State Police Emblem" 
            className="w-10 h-10 object-contain drop-shadow-sm"
          />
        </div>
        <div className="flex flex-col">
          <div className="flex items-center gap-2">
            <span className="text-sm sm:text-base font-black tracking-wider text-slate-900 dark:text-slate-100 uppercase font-mono">
              Aloka Intelligence
            </span>
            <span className="hidden sm:inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-bold bg-blue-100 dark:bg-blue-950 text-blue-800 dark:text-blue-300 border border-blue-200 dark:border-blue-800/60 tracking-wider font-mono">
              <Shield className="w-3 h-3 text-blue-600 dark:text-blue-400" />
              KSP COMMAND
            </span>
          </div>
          <span className="text-[10px] font-bold text-slate-500 dark:text-slate-400 uppercase tracking-widest">
            State Police Intelligence Center
          </span>
        </div>
      </div>

      {/* Center: Mobile Navigation Switcher (visible on smaller screens) */}
      <div className="flex md:hidden items-center bg-slate-100 dark:bg-slate-800 p-1 rounded-lg border border-slate-200 dark:border-slate-700">
        <button
          onClick={() => setActiveTab('chat')}
          className={`flex items-center gap-1.5 px-3 py-1 rounded-md text-xs font-bold transition-all ${
            activeTab === 'chat'
              ? 'bg-white dark:bg-slate-900 text-blue-600 dark:text-blue-400 shadow-xs'
              : 'text-slate-500 hover:text-slate-700 dark:text-slate-400'
          }`}
        >
          <MessageSquare className="w-3.5 h-3.5" />
          <span>Chat</span>
        </button>
        <button
          onClick={() => setActiveTab('canvas')}
          className={`flex items-center gap-1.5 px-3 py-1 rounded-md text-xs font-bold transition-all relative ${
            activeTab === 'canvas'
              ? 'bg-white dark:bg-slate-900 text-blue-600 dark:text-blue-400 shadow-xs'
              : 'text-slate-500 hover:text-slate-700 dark:text-slate-400'
          }`}
        >
          <LayoutDashboard className="w-3.5 h-3.5" />
          <span>Canvas</span>
          {hasDataOnCanvas && (
            <span className="w-1.5 h-1.5 rounded-full bg-blue-500 animate-ping"></span>
          )}
        </button>
      </div>

      {/* Right: Operational Status Badges & Controls */}
      <div className="flex items-center gap-2 sm:gap-4">
        {/* Real Status Tickers */}
        <div className="hidden lg:flex items-center gap-3 border-r border-slate-200 dark:border-slate-800 pr-4">
          <div className="flex items-center gap-1.5 text-[10px] font-mono font-bold text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/40 px-2 py-1 rounded border border-emerald-200 dark:border-emerald-900/60">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
            <span>SYSTEM ONLINE</span>
          </div>

          <div className="flex items-center gap-1.5 text-[10px] font-mono font-bold text-cyan-600 dark:text-cyan-400 bg-cyan-50 dark:bg-cyan-950/40 px-2 py-1 rounded border border-cyan-200 dark:border-cyan-900/60">
            <Database className="w-3 h-3 text-cyan-500" />
            <span>DATABASE CONNECTED</span>
          </div>
        </div>

        {/* Theme Toggle Button */}
        <button
          onClick={() => setIsDarkMode(!isDarkMode)}
          className="p-2 rounded-lg bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-amber-400 hover:bg-slate-200 dark:hover:bg-slate-700 transition-all border border-slate-200 dark:border-slate-700/80 cursor-pointer shadow-xs"
          title={isDarkMode ? "Switch to Light Mode" : "Switch to Command Dark Mode"}
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

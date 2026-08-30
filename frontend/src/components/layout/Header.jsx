import React from 'react';
import { Sun, Moon, Shield } from 'lucide-react';

export default function Header({ isDarkMode, setIsDarkMode }) {
  return (
    <header className="h-16 bg-white dark:bg-slate-900 flex items-center justify-between px-6 border-b border-slate-200 dark:border-slate-800 shrink-0 shadow-sm z-20 transition-colors duration-300">
      <div className="flex items-center gap-3">
        <img 
          src="https://upload.wikimedia.org/wikipedia/commons/a/aa/Seal_of_Karnataka.svg" 
          alt="Karnataka State Police Logo" 
          className="w-10 h-10 object-contain drop-shadow-sm"
        />
        <div className="flex flex-col">
          <div className="flex items-center gap-2">
            <span className="text-base font-extrabold tracking-wider text-slate-800 dark:text-slate-100 uppercase">
              Aloka Intelligence
            </span>
            <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold bg-blue-100 dark:bg-blue-950/80 text-blue-800 dark:text-blue-300 border border-blue-200 dark:border-blue-800/50">
              <Shield className="w-3 h-3 text-blue-600 dark:text-blue-400" />
              KSP SECURE
            </span>
          </div>
          <span className="text-[11px] font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-widest">
            State Intelligence Command Center
          </span>
        </div>
      </div>

      <div className="flex items-center gap-3">
        <button
          onClick={() => setIsDarkMode(!isDarkMode)}
          className="p-2.5 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-amber-400 hover:bg-slate-200 dark:hover:bg-slate-700 transition-all shadow-sm cursor-pointer"
          title={isDarkMode ? "Switch to Light Mode" : "Switch to Dark Mode"}
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

import React from 'react';
import { ShieldCheck, Activity } from 'lucide-react';

export default function Footer({ currentTime }) {
  const formatTime = (d) =>
    d.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false }) + ' IST';
  
  const formatDate = (d) =>
    d.toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' });

  return (
    <footer className="h-8 bg-slate-900 dark:bg-[#0B1017] border-t border-slate-800 dark:border-[#263142] flex items-center justify-between px-4 sm:px-6 z-50 shrink-0 select-none transition-colors">
      <div className="flex items-center gap-3 text-[10px] font-mono font-bold text-slate-400 uppercase tracking-wider">
        <span className="flex items-center gap-1.5 text-emerald-400">
          <Activity className="w-3 h-3" />
          SYSTEM SECURE & OPERATIONAL
        </span>
        <span className="text-slate-600 dark:text-slate-700 hidden sm:inline">|</span>
        <span className="hidden sm:flex items-center gap-1 text-slate-400">
          <ShieldCheck className="w-3 h-3 text-[#2F5DA8] dark:text-[#93B4E8]" />
          KSP STATE CRIMINOLOGICAL DATABASE
        </span>
      </div>
      <div className="flex items-center gap-3 text-[10px] text-slate-400 font-mono">
        <span className="text-slate-300 font-semibold">{formatTime(currentTime)}</span>
        <span className="text-slate-600">•</span>
        <span className="hidden sm:inline">{formatDate(currentTime)}</span>
      </div>
    </footer>
  );
}

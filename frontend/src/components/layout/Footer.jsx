import React from 'react';
import { ShieldCheck, Activity } from 'lucide-react';

export default function Footer({ currentTime }) {
  const formatTime = (d) =>
    d.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false }) + ' IST';
  
  const formatDate = (d) =>
    d.toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' });

  return (
    <footer className="h-8 bg-slate-900 dark:bg-slate-950 border-t border-slate-800 flex items-center justify-between px-6 z-50 shrink-0 select-none">
      <div className="flex items-center gap-3 text-[10px] font-bold text-slate-400 uppercase tracking-wider">
        <span className="flex items-center gap-1.5 text-emerald-400">
          <Activity className="w-3 h-3 animate-pulse" />
          SYSTEM SECURE & OPERATIONAL
        </span>
        <span className="text-slate-600">|</span>
        <span className="flex items-center gap-1 text-slate-400">
          <ShieldCheck className="w-3 h-3 text-blue-400" />
          KSP STATE CRIMINOLOGICAL DATABASE
        </span>
      </div>
      <div className="flex items-center gap-4 text-[10px] text-slate-400 font-mono">
        <span className="text-slate-300 font-semibold">{formatTime(currentTime)}</span>
        <span className="text-slate-500">•</span>
        <span>{formatDate(currentTime)}</span>
      </div>
    </footer>
  );
}

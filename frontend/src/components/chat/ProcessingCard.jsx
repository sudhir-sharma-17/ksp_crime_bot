import React, { useState, useEffect } from 'react';
import { Shield, Square, Check, Circle, Loader2 } from 'lucide-react';

const STAGES = [
  { id: 1, label: "Understanding request & intent" },
  { id: 2, label: "Resolving investigative context" },
  { id: 3, label: "Querying state intelligence database" },
  { id: 4, label: "Synthesizing analytical insights" },
  { id: 5, label: "Finalizing intelligence report" }
];

export default function ProcessingCard({ onTerminate }) {
  const [currentStageIdx, setCurrentStageIdx] = useState(0);

  // Time-stepped visual progress sequence while awaiting the live API response
  useEffect(() => {
    const timer1 = setTimeout(() => setCurrentStageIdx(1), 1200);
    const timer2 = setTimeout(() => setCurrentStageIdx(2), 2600);
    const timer3 = setTimeout(() => setCurrentStageIdx(3), 5200);
    const timer4 = setTimeout(() => setCurrentStageIdx(4), 8500);

    return () => {
      clearTimeout(timer1);
      clearTimeout(timer2);
      clearTimeout(timer3);
      clearTimeout(timer4);
    };
  }, []);

  return (
    <div className="p-4 sm:p-5 rounded-2xl bg-white dark:bg-slate-900 border border-blue-200 dark:border-slate-800 shadow-sm animate-fade-in mb-4 select-none">
      {/* Card Header: Emblem + System Title + Terminate Action */}
      <div className="flex items-center justify-between pb-3 mb-3.5 border-b border-slate-100 dark:border-slate-800">
        <div className="flex items-center gap-2.5">
          <div className="relative w-6 h-6 flex items-center justify-center">
            <img 
              src="https://upload.wikimedia.org/wikipedia/commons/a/aa/Seal_of_Karnataka.svg" 
              alt="Aloka State Police Emblem" 
              className="w-full h-full object-contain"
            />
          </div>
          <div className="flex flex-col">
            <span className="text-[11px] font-mono font-bold uppercase tracking-wider text-slate-900 dark:text-slate-100">
              ALOKA INTELLIGENCE
            </span>
            <span className="text-[9px] font-mono font-semibold uppercase tracking-widest text-slate-400 dark:text-slate-500">
              State Police AI System
            </span>
          </div>
        </div>

        {/* Terminate Query Button */}
        <button
          type="button"
          onClick={onTerminate}
          className="flex items-center gap-1.5 bg-rose-50 hover:bg-rose-100 dark:bg-rose-950/40 dark:hover:bg-rose-900/60 text-rose-700 dark:text-rose-400 border border-rose-200 dark:border-rose-900/60 text-[11px] font-bold py-1 px-2.5 rounded-lg transition-colors cursor-pointer"
          title="Cancel active inquiry"
          aria-label="Terminate Query"
        >
          <Square className="w-2.5 h-2.5 fill-current" />
          <span>Terminate</span>
        </button>
      </div>

      {/* Main Status Badge */}
      <div className="flex items-center gap-2 mb-3 px-3 py-1.5 rounded-xl bg-blue-50/70 dark:bg-slate-800/60 border border-blue-100 dark:border-slate-700/60 w-fit">
        <span className="relative flex h-2 w-2">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
          <span className="relative inline-flex rounded-full h-2 w-2 bg-cyan-500"></span>
        </span>
        <span className="text-xs font-mono font-bold uppercase tracking-wider text-blue-950 dark:text-cyan-300">
          ANALYZING REQUEST...
        </span>
      </div>

      {/* 5-Step Intelligence Progress Tracker */}
      <div className="space-y-2 pl-1">
        {STAGES.map((stage, idx) => {
          const isCompleted = idx < currentStageIdx;
          const isCurrent = idx === currentStageIdx;
          const isPending = idx > currentStageIdx;

          return (
            <div 
              key={stage.id} 
              className={`flex items-center gap-2.5 text-xs transition-opacity duration-300 ${
                isPending ? 'opacity-40' : 'opacity-100'
              }`}
            >
              {isCompleted ? (
                <div className="w-4 h-4 rounded-full bg-emerald-100 dark:bg-emerald-950 text-emerald-600 dark:text-emerald-400 flex items-center justify-center shrink-0">
                  <Check className="w-2.5 h-2.5 stroke-[3]" />
                </div>
              ) : isCurrent ? (
                <div className="w-4 h-4 rounded-full bg-blue-100 dark:bg-cyan-950 text-blue-600 dark:text-cyan-400 flex items-center justify-center shrink-0">
                  <Loader2 className="w-2.5 h-2.5 animate-spin" />
                </div>
              ) : (
                <div className="w-4 h-4 flex items-center justify-center text-slate-300 dark:text-slate-600 shrink-0">
                  <Circle className="w-2 h-2" />
                </div>
              )}

              <span className={`font-mono text-[11px] sm:text-xs ${
                isCurrent 
                  ? 'font-bold text-slate-900 dark:text-slate-100' 
                  : isCompleted 
                  ? 'text-slate-600 dark:text-slate-400' 
                  : 'text-slate-400 dark:text-slate-500'
              }`}>
                {stage.label}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}

import React, { useState, useEffect } from 'react';
import { Square, Check, Circle, Loader2 } from 'lucide-react';

const STAGES = [
  { id: 1, label: "Understanding request & intent" },
  { id: 2, label: "Resolving investigative context" },
  { id: 3, label: "Querying state intelligence database" },
  { id: 4, label: "Synthesizing analytical insights" },
  { id: 5, label: "Finalizing intelligence report" }
];

export default function ProcessingCard({ onTerminate }) {
  const [currentStageIdx, setCurrentStageIdx] = useState(0);

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
    <div className="p-4 sm:p-5 rounded-2xl bg-white dark:bg-[#141C28] border border-slate-200 dark:border-[#263142] shadow-xs animate-fade-in mb-4 select-none">
      {/* Card Header */}
      <div className="flex items-center justify-between pb-3 mb-3.5 border-b border-slate-100 dark:border-[#263142]">
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
          className="flex items-center gap-1.5 bg-red-50 hover:bg-red-100 dark:bg-red-950/40 dark:hover:bg-red-900/50 text-red-600 dark:text-red-400 border border-red-200 dark:border-red-900/50 text-[11px] font-semibold py-1 px-2.5 rounded-lg transition-colors cursor-pointer"
          title="Cancel active inquiry"
          aria-label="Terminate Query"
        >
          <Square className="w-2.5 h-2.5 fill-current" />
          <span>Terminate</span>
        </button>
      </div>

      {/* Main Status Badge */}
      <div className="flex items-center gap-2 mb-3 px-3 py-1.5 rounded-lg bg-slate-100 dark:bg-[#172640] border border-slate-200 dark:border-[#263142] w-fit">
        <span className="relative flex h-2 w-2">
          <span className="relative inline-flex rounded-full h-2 w-2 bg-[#2F5DA8]"></span>
        </span>
        <span className="text-xs font-mono font-bold uppercase tracking-wider text-[#2F5DA8] dark:text-[#93B4E8]">
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
                <div className="w-4 h-4 rounded-full bg-emerald-50 dark:bg-[#102619] text-emerald-600 dark:text-emerald-400 flex items-center justify-center shrink-0">
                  <Check className="w-2.5 h-2.5 stroke-[3]" />
                </div>
              ) : isCurrent ? (
                <div className="w-4 h-4 rounded-full bg-slate-100 dark:bg-[#101722] text-[#2F5DA8] dark:text-[#93B4E8] flex items-center justify-center shrink-0">
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

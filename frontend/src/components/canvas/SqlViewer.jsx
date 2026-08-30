import React, { useState } from 'react';
import { Terminal, Copy, Check, ChevronDown, ChevronRight } from 'lucide-react';

export default function SqlViewer({ sqlCommand, queryIndex, totalQueries }) {
  const [isOpen, setIsOpen] = useState(false);
  const [copied, setCopied] = useState(false);

  if (!sqlCommand || sqlCommand === 'CHITCHAT') return null;

  const handleCopy = (e) => {
    e.stopPropagation();
    navigator.clipboard.writeText(sqlCommand);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="rounded-xl border border-slate-200 dark:border-slate-800/80 overflow-hidden shadow-xs bg-white dark:bg-slate-900 transition-colors">
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className="w-full bg-slate-50 hover:bg-slate-100 dark:bg-slate-900 dark:hover:bg-slate-850 px-4 py-2.5 flex items-center justify-between cursor-pointer border-b border-transparent transition-colors"
      >
        <div className="flex items-center gap-2">
          {isOpen ? <ChevronDown className="w-3.5 h-3.5 text-slate-400" /> : <ChevronRight className="w-3.5 h-3.5 text-slate-400" />}
          <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></div>
          <Terminal className="w-3.5 h-3.5 text-slate-500 dark:text-slate-400" />
          <span className="text-[11px] font-mono font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider">
            Executed SQL Command {totalQueries > 1 ? `#${queryIndex + 1}` : ''}
          </span>
        </div>

        <div className="flex items-center gap-3">
          <span className="text-[10px] font-mono text-slate-400 dark:text-slate-500 uppercase">
            {isOpen ? 'Hide Query' : 'View Query'}
          </span>
          <button
            type="button"
            onClick={handleCopy}
            className="flex items-center gap-1 text-[11px] text-slate-500 dark:text-slate-400 hover:text-blue-600 dark:hover:text-white transition-colors cursor-pointer px-2 py-0.5 rounded hover:bg-slate-200 dark:hover:bg-slate-800"
            title="Copy SQL query"
          >
            {copied ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
            <span>{copied ? 'Copied' : 'Copy'}</span>
          </button>
        </div>
      </button>

      {isOpen && (
        <pre className="p-4 overflow-x-auto text-cyan-900 dark:text-cyan-300 font-mono text-xs bg-slate-100/70 dark:bg-slate-950/80 border-t border-slate-200 dark:border-slate-800 leading-relaxed">
          <code>{sqlCommand}</code>
        </pre>
      )}
    </div>
  );
}

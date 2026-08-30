import React, { useState } from 'react';
import { Terminal, Copy, Check, ChevronDown, ChevronRight, FileCode2, ShieldAlert } from 'lucide-react';

export default function SqlViewer({ sqlCommand, queryIndex, totalQueries, rowsCount = 0 }) {
  const [isSqlOpen, setIsSqlOpen] = useState(false);
  const [isMetaOpen, setIsMetaOpen] = useState(false);
  const [copied, setCopied] = useState(false);

  if (!sqlCommand || sqlCommand === 'CHITCHAT') return null;

  const handleCopy = (e) => {
    e.stopPropagation();
    navigator.clipboard.writeText(sqlCommand);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="flex flex-col gap-2.5">
      {/* 1. Collapsible Executed SQL */}
      <div className="rounded-2xl border border-slate-200 dark:border-slate-800/80 overflow-hidden shadow-xs bg-white dark:bg-slate-900 transition-colors">
        <button
          type="button"
          onClick={() => setIsSqlOpen(!isSqlOpen)}
          className="w-full bg-slate-50 hover:bg-slate-100 dark:bg-slate-900 dark:hover:bg-slate-850 px-5 py-3 flex items-center justify-between cursor-pointer border-b border-transparent transition-colors"
        >
          <div className="flex items-center gap-2.5">
            {isSqlOpen ? (
              <ChevronDown className="w-4 h-4 text-slate-400" />
            ) : (
              <ChevronRight className="w-4 h-4 text-slate-400" />
            )}
            <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></div>
            <Terminal className="w-4 h-4 text-slate-500 dark:text-slate-400" />
            <span className="text-xs font-mono font-bold text-slate-800 dark:text-slate-200 uppercase tracking-wider">
              Executed SQL {totalQueries > 1 ? `(#${queryIndex + 1})` : ''}
            </span>
          </div>

          <div className="flex items-center gap-3">
            <span className="text-[10px] font-mono text-slate-400 dark:text-slate-500 uppercase tracking-wider">
              {isSqlOpen ? 'Hide SQL' : 'View SQL'}
            </span>
            <button
              type="button"
              onClick={handleCopy}
              className="flex items-center gap-1 text-[11px] text-slate-500 dark:text-slate-400 hover:text-blue-600 dark:hover:text-cyan-400 transition-colors cursor-pointer px-2 py-0.5 rounded hover:bg-slate-200 dark:hover:bg-slate-800"
              title="Copy SQL statement"
              aria-label="Copy SQL statement"
            >
              {copied ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
              <span>{copied ? 'Copied' : 'Copy'}</span>
            </button>
          </div>
        </button>

        {isSqlOpen && (
          <pre className="p-4 sm:p-5 overflow-x-auto text-cyan-900 dark:text-cyan-300 font-mono text-xs bg-slate-100/70 dark:bg-slate-950/80 border-t border-slate-200 dark:border-slate-800 leading-relaxed">
            <code>{sqlCommand}</code>
          </pre>
        )}
      </div>

      {/* 2. Collapsible Query Metadata */}
      <div className="rounded-2xl border border-slate-200 dark:border-slate-800/80 overflow-hidden shadow-xs bg-white dark:bg-slate-900 transition-colors">
        <button
          type="button"
          onClick={() => setIsMetaOpen(!isMetaOpen)}
          className="w-full bg-slate-50 hover:bg-slate-100 dark:bg-slate-900 dark:hover:bg-slate-850 px-5 py-2.5 flex items-center justify-between cursor-pointer transition-colors"
        >
          <div className="flex items-center gap-2.5">
            {isMetaOpen ? (
              <ChevronDown className="w-4 h-4 text-slate-400" />
            ) : (
              <ChevronRight className="w-4 h-4 text-slate-400" />
            )}
            <FileCode2 className="w-4 h-4 text-slate-500 dark:text-slate-400" />
            <span className="text-xs font-mono font-bold text-slate-800 dark:text-slate-200 uppercase tracking-wider">
              Query Metadata
            </span>
          </div>

          <span className="text-[10px] font-mono text-slate-400 dark:text-slate-500 uppercase tracking-wider">
            {isMetaOpen ? 'Hide Metadata' : 'View Metadata'}
          </span>
        </button>

        {isMetaOpen && (
          <div className="p-4 bg-slate-50/60 dark:bg-slate-950/60 border-t border-slate-200 dark:border-slate-800 grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs font-mono">
            <div className="flex flex-col">
              <span className="text-[10px] text-slate-400 uppercase">Execution Status</span>
              <span className="font-bold text-emerald-600 dark:text-emerald-400">SUCCESS (200 OK)</span>
            </div>
            <div className="flex flex-col">
              <span className="text-[10px] text-slate-400 uppercase">Access Mode</span>
              <span className="font-bold text-blue-600 dark:text-cyan-400">READ-ONLY (SELECT)</span>
            </div>
            <div className="flex flex-col">
              <span className="text-[10px] text-slate-400 uppercase">Returned Rows</span>
              <span className="font-bold text-slate-700 dark:text-slate-200">{rowsCount} Records</span>
            </div>
            <div className="flex flex-col">
              <span className="text-[10px] text-slate-400 uppercase">Database Engine</span>
              <span className="font-bold text-slate-700 dark:text-slate-200">MySQL 8.0</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

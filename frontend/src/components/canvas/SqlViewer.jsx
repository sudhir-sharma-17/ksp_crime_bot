import React, { useState } from 'react';
import { Terminal, Copy, Check } from 'lucide-react';

export default function SqlViewer({ sqlCommand, queryIndex, totalQueries }) {
  const [copied, setCopied] = useState(false);

  if (!sqlCommand || sqlCommand === 'CHITCHAT') return null;

  const handleCopy = () => {
    navigator.clipboard.writeText(sqlCommand);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="rounded-xl border border-slate-200 dark:border-slate-800 overflow-hidden shadow-xs bg-white dark:bg-slate-900 transition-colors mb-4">
      <div className="bg-slate-900 dark:bg-slate-800 px-4 py-2 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></div>
          <Terminal className="w-3.5 h-3.5 text-slate-300" />
          <span className="text-[11px] font-mono font-bold text-slate-200 uppercase tracking-wider">
            Executed SQL Command {totalQueries > 1 ? `#${queryIndex + 1}` : ''}
          </span>
        </div>
        <button
          onClick={handleCopy}
          className="flex items-center gap-1 text-[11px] text-slate-400 hover:text-white transition-colors cursor-pointer"
          title="Copy SQL query"
        >
          {copied ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
          <span>{copied ? 'Copied' : 'Copy SQL'}</span>
        </button>
      </div>
      <pre className="p-4 overflow-x-auto text-blue-900 dark:text-blue-300 font-mono text-xs bg-blue-50/25 dark:bg-slate-950/60 leading-relaxed">
        <code>{sqlCommand}</code>
      </pre>
    </div>
  );
}

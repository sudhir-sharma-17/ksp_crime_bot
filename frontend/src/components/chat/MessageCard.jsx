import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Copy, Check, Globe, Shield, User, AlertCircle, ArrowUpRight, FolderLock } from 'lucide-react';

const mdComponents = {
  h1: ({ children }) => (
    <h1 className="text-base sm:text-lg font-black text-slate-900 dark:text-slate-100 mb-2 block border-b border-slate-200 dark:border-slate-800 pb-1 tracking-tight uppercase font-mono">
      {children}
    </h1>
  ),
  h2: ({ children }) => (
    <h2 className="text-sm sm:text-base font-bold text-blue-900 dark:text-cyan-400 mt-3 mb-2 block tracking-tight font-mono">
      {children}
    </h2>
  ),
  h3: ({ children }) => (
    <h3 className="text-xs sm:text-sm font-semibold text-slate-800 dark:text-slate-200 mt-2 mb-1 block uppercase tracking-wider">
      {children}
    </h3>
  ),
  p: ({ children }) => (
    <p className="text-xs sm:text-sm text-slate-700 dark:text-slate-300 mb-2.5 leading-relaxed block font-sans">
      {children}
    </p>
  ),
  strong: ({ children }) => (
    <strong className="font-bold text-slate-900 dark:text-white font-sans">{children}</strong>
  ),
  em: ({ children }) => (
    <em className="italic text-blue-700 dark:text-cyan-300 font-medium">{children}</em>
  ),
  ul: ({ children }) => (
    <ul className="list-disc pl-5 space-y-1 mb-2.5 text-slate-700 dark:text-slate-300 text-xs sm:text-sm">{children}</ul>
  ),
  ol: ({ children }) => (
    <ol className="list-decimal pl-5 space-y-1 mb-2.5 text-slate-700 dark:text-slate-300 text-xs sm:text-sm">{children}</ol>
  ),
  li: ({ children }) => (
    <li className="marker:text-blue-600 dark:marker:text-cyan-400 leading-relaxed pl-0.5">{children}</li>
  ),
  code: ({ inline, children }) =>
    inline ? (
      <code className="font-mono text-cyan-800 dark:text-cyan-300 bg-cyan-50 dark:bg-cyan-950/60 px-1.5 py-0.5 rounded text-[11px] font-semibold border border-cyan-200/80 dark:border-cyan-800/40">
        {children}
      </code>
    ) : (
      <pre className="font-mono text-slate-800 dark:text-slate-200 bg-slate-100 dark:bg-slate-900 p-3 rounded-xl overflow-x-auto text-xs border border-slate-200 dark:border-slate-800 my-2 leading-relaxed shadow-xs">
        <code>{children}</code>
      </pre>
    ),
  blockquote: ({ children }) => (
    <blockquote className="border-l-3 border-blue-600 dark:border-cyan-500 pl-3 text-slate-600 dark:text-slate-400 italic my-2 text-xs">
      {children}
    </blockquote>
  ),
  table: ({ children }) => (
    <div className="overflow-x-auto my-3 rounded-xl border border-slate-200 dark:border-slate-800 shadow-xs">
      <table className="min-w-full text-xs divide-y divide-slate-200 dark:divide-slate-800">{children}</table>
    </div>
  ),
  thead: ({ children }) => (
    <thead className="bg-slate-100 dark:bg-slate-800 text-slate-800 dark:text-slate-200 font-bold uppercase text-[11px] font-mono">
      {children}
    </thead>
  ),
  th: ({ children }) => <th className="px-3.5 py-2.5 text-left tracking-wider">{children}</th>,
  tbody: ({ children }) => <tbody className="divide-y divide-slate-100 dark:divide-slate-800/80">{children}</tbody>,
  td: ({ children }) => <td className="px-3.5 py-2 text-slate-700 dark:text-slate-300">{children}</td>,
  tr: ({ children }) => <tr className="hover:bg-slate-50 dark:hover:bg-slate-850 transition-colors">{children}</tr>,
};

export default function MessageCard({
  msg,
  index,
  isSelected,
  onSelect,
  onTranslate
}) {
  const [copied, setCopied] = useState(false);
  const isUser = msg.sender === 'user';
  const isSystem = msg.sender === 'system';

  const handleCopy = (text) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  // Extract any active case mention (e.g. KSP-CASE-0004) from text or query for context badge
  const textContent = msg.text || msg.response || msg.user_query || '';
  const caseMatch = textContent.match(/KSP-CASE-\d{4}/i);
  const activeCaseId = caseMatch ? caseMatch[0].toUpperCase() : null;

  if (isUser) {
    return (
      <div className="flex justify-end mb-4 animate-fade-in">
        <div className="max-w-[85%] bg-blue-900 dark:bg-blue-950 text-white p-3.5 sm:p-4 rounded-2xl rounded-tr-xs border border-blue-800 dark:border-blue-800/60 shadow-xs">
          <div className="flex items-center justify-between gap-3 mb-1">
            <span className="text-[10px] font-mono font-bold uppercase tracking-wider text-blue-300">
              Investigator Query
            </span>
            {activeCaseId && (
              <span className="inline-flex items-center gap-1 text-[10px] font-mono bg-blue-800/80 dark:bg-blue-900/90 text-cyan-300 px-1.5 py-0.2 rounded border border-blue-700">
                <FolderLock className="w-2.5 h-2.5" />
                {activeCaseId}
              </span>
            )}
          </div>
          <div className="text-xs sm:text-sm font-medium leading-relaxed">
            {textContent}
          </div>
        </div>
      </div>
    );
  }

  if (isSystem) {
    return (
      <div className="bg-amber-50/80 dark:bg-amber-950/20 p-3.5 rounded-2xl border border-amber-200 dark:border-amber-900/40 shadow-xs mb-4 animate-fade-in">
        <div className="flex items-center gap-2 mb-1.5">
          <AlertCircle className="w-4 h-4 text-amber-600 dark:text-amber-400 shrink-0" />
          <span className="text-[10px] font-bold uppercase tracking-wider text-amber-800 dark:text-amber-300 font-mono">
            Intelligence Alert
          </span>
        </div>
        <div className="prose dark:prose-invert prose-sm text-xs sm:text-sm text-amber-900 dark:text-amber-200">
          <ReactMarkdown remarkPlugins={[remarkGfm]} components={mdComponents}>{textContent}</ReactMarkdown>
        </div>
      </div>
    );
  }

  const hasData = (msg.all_sql_results && msg.all_sql_results.length > 0) || (msg.sql_results && msg.sql_results.length > 0);

  return (
    <div
      onClick={() => {
        if (hasData) onSelect(index);
      }}
      className={`p-4 sm:p-5 rounded-2xl border mb-4 transition-all duration-200 animate-fade-in cursor-pointer ${
        isSelected
          ? 'bg-white dark:bg-slate-900 border-blue-500 dark:border-blue-500 shadow-md ring-1 ring-blue-500/25'
          : 'bg-white dark:bg-slate-900/90 border-slate-200 dark:border-slate-800/90 hover:border-blue-300 dark:hover:border-slate-700 shadow-xs'
      }`}
    >
      {/* 1. Header & Insignia */}
      <div className="flex items-center justify-between gap-2 mb-3 pb-2.5 border-b border-slate-100 dark:border-slate-800/80">
        <div className="flex items-center gap-2">
          <img 
            src="https://upload.wikimedia.org/wikipedia/commons/a/aa/Seal_of_Karnataka.svg" 
            alt="Aloka Emblem" 
            className="w-5 h-5 object-contain drop-shadow-xs"
          />
          <div className="flex flex-col">
            <span className="text-[11px] font-mono font-bold uppercase tracking-wider text-slate-900 dark:text-slate-100">
              Aloka Intelligence
            </span>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {activeCaseId && (
            <div className="hidden sm:flex items-center gap-1 text-[10px] font-mono font-bold text-amber-700 dark:text-amber-400 bg-amber-50 dark:bg-amber-950/60 px-2 py-0.5 rounded border border-amber-200 dark:border-amber-900/60">
              <span className="w-1.5 h-1.5 rounded-full bg-amber-500 animate-pulse"></span>
              <span>ACTIVE CASE: {activeCaseId}</span>
            </div>
          )}

          {hasData && (
            <div className="flex items-center gap-1 text-[10px] font-mono font-bold uppercase text-blue-600 dark:text-cyan-400 bg-blue-50 dark:bg-blue-950/80 px-2 py-0.5 rounded border border-blue-200 dark:border-blue-800/60">
              <span>Canvas Linked</span>
              <ArrowUpRight className="w-3 h-3" />
            </div>
          )}
        </div>
      </div>

      {/* 2. Structured Response Body */}
      <div className="prose dark:prose-invert prose-sm max-w-none text-slate-700 dark:text-slate-300">
        <ReactMarkdown remarkPlugins={[remarkGfm]} components={mdComponents}>{textContent}</ReactMarkdown>
      </div>

      {/* 3. Action Toolbar */}
      <div className="flex items-center justify-between gap-4 mt-4 pt-3 border-t border-slate-100 dark:border-slate-800/80 select-none">
        <div className="flex items-center gap-4">
          <button 
            type="button"
            onClick={(e) => {
              e.stopPropagation();
              handleCopy(textContent);
            }}
            className="flex items-center gap-1.5 text-xs font-medium text-slate-500 hover:text-blue-600 dark:text-slate-400 dark:hover:text-cyan-400 transition-colors cursor-pointer" 
            title="Copy intelligence report"
            aria-label="Copy report"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-emerald-500" /> : <Copy className="w-3.5 h-3.5" />}
            <span>{copied ? 'Copied' : 'Copy'}</span>
          </button>
          
          <div className="flex items-center gap-1.5 text-xs font-medium text-slate-500 dark:text-slate-400 hover:text-blue-600 dark:hover:text-cyan-400">
            <Globe className="w-3.5 h-3.5" />
            <select 
              defaultValue=""
              onClick={(e) => e.stopPropagation()}
              onChange={(e) => {
                onTranslate(e, textContent, index);
                e.target.value = "";
              }}
              className="bg-transparent border-none text-xs font-medium focus:ring-0 cursor-pointer outline-none text-slate-500 dark:text-slate-400 hover:text-blue-600 dark:hover:text-cyan-400"
              aria-label="Translate message"
            >
              <option value="" disabled className="dark:bg-slate-900">Translate</option>
              <option value="English" className="dark:bg-slate-900">English</option>
              <option value="Kannada" className="dark:bg-slate-900">Kannada (ಕನ್ನಡ)</option>
              <option value="Hindi" className="dark:bg-slate-900">Hindi (हिन्दी)</option>
            </select>
          </div>
        </div>

        {hasData && (
          <span className="text-[10px] font-mono text-slate-400 dark:text-slate-500">
            Click card to view on Data Canvas
          </span>
        )}
      </div>
    </div>
  );
}

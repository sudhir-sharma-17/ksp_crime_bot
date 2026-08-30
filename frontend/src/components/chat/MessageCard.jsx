import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Copy, Check, Globe, Shield, User, AlertCircle, ArrowUpRight, FolderLock } from 'lucide-react';

const mdComponents = {
  h1: ({ children }) => (
    <h1 className="text-base sm:text-lg font-black text-slate-900 dark:text-slate-100 mb-2 block border-b border-slate-200 dark:border-[#263142] pb-1 tracking-tight uppercase font-mono">
      {children}
    </h1>
  ),
  h2: ({ children }) => (
    <h2 className="text-sm sm:text-base font-bold text-[#2F5DA8] dark:text-[#93B4E8] mt-3 mb-2 block tracking-tight font-mono">
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
    <em className="italic text-[#3A6DBD] dark:text-[#A7C4F2] font-medium">{children}</em>
  ),
  ul: ({ children }) => (
    <ul className="list-disc pl-5 space-y-1 mb-2.5 text-slate-700 dark:text-slate-300 text-xs sm:text-sm">{children}</ul>
  ),
  ol: ({ children }) => (
    <ol className="list-decimal pl-5 space-y-1 mb-2.5 text-slate-700 dark:text-slate-300 text-xs sm:text-sm">{children}</ol>
  ),
  li: ({ children }) => (
    <li className="marker:text-[#2F5DA8] leading-relaxed pl-0.5">{children}</li>
  ),
  code: ({ inline, children }) =>
    inline ? (
      <code className="font-mono text-slate-800 dark:text-[#A7C4F2] bg-slate-100 dark:bg-[#101722] px-1.5 py-0.5 rounded text-[11px] font-semibold border border-slate-200 dark:border-[#263142]">
        {children}
      </code>
    ) : (
      <pre className="font-mono text-slate-800 dark:text-slate-200 bg-slate-50 dark:bg-[#0B1017] p-3 rounded-xl overflow-x-auto text-xs border border-slate-200 dark:border-[#263142] my-2 leading-relaxed">
        <code>{children}</code>
      </pre>
    ),
  blockquote: ({ children }) => (
    <blockquote className="border-l-3 border-[#2F5DA8] pl-3 text-slate-600 dark:text-slate-400 italic my-2 text-xs">
      {children}
    </blockquote>
  ),
  table: ({ children }) => (
    <div className="overflow-x-auto my-3 rounded-xl border border-slate-200 dark:border-[#263142] shadow-xs">
      <table className="min-w-full text-xs divide-y divide-slate-200 dark:divide-[#263142]">{children}</table>
    </div>
  ),
  thead: ({ children }) => (
    <thead className="bg-slate-100 dark:bg-[#101722] text-slate-800 dark:text-slate-200 font-bold uppercase text-[11px] font-mono">
      {children}
    </thead>
  ),
  th: ({ children }) => <th className="px-3.5 py-2.5 text-left tracking-wider">{children}</th>,
  tbody: ({ children }) => <tbody className="divide-y divide-slate-100 dark:divide-[#263142]/80">{children}</tbody>,
  td: ({ children }) => <td className="px-3.5 py-2 text-slate-700 dark:text-slate-300">{children}</td>,
  tr: ({ children }) => <tr className="hover:bg-slate-50 dark:hover:bg-[#172640]/50 transition-colors">{children}</tr>,
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

  const textContent = msg.text || msg.response || msg.user_query || '';
  const caseMatch = textContent.match(/KSP-CASE-\d{4}/i);
  const activeCaseId = caseMatch ? caseMatch[0].toUpperCase() : null;

  if (isUser) {
    return (
      <div className="flex justify-end mb-4 animate-fade-in">
        <div className="max-w-[85%] bg-blue-900 dark:bg-[#172640] text-white p-3.5 sm:p-4 rounded-2xl rounded-tr-xs border border-blue-800 dark:border-[#263142]">
          <div className="flex items-center justify-between gap-3 mb-1">
            <span className="text-[10px] font-mono font-bold uppercase tracking-wider text-blue-300 dark:text-[#93B4E8]">
              Investigator Query
            </span>
            {activeCaseId && (
              <span className="inline-flex items-center gap-1 text-[10px] font-mono bg-blue-800/80 dark:bg-[#101722] text-[#93B4E8] px-1.5 py-0.5 rounded border border-blue-700 dark:border-[#263142]">
                <FolderLock className="w-2.5 h-2.5" />
                {activeCaseId}
              </span>
            )}
          </div>
          <div className="text-xs sm:text-sm font-medium leading-relaxed text-slate-100">
            {textContent}
          </div>
        </div>
      </div>
    );
  }

  if (isSystem) {
    return (
      <div className="bg-amber-50/80 dark:bg-amber-950/20 p-3.5 rounded-2xl border border-amber-200 dark:border-amber-900/40 mb-4 animate-fade-in">
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
          ? 'bg-white dark:bg-[#141C28] border-[#2F5DA8] ring-1 ring-[#2F5DA8]/50 shadow-xs'
          : 'bg-white dark:bg-[#141C28] border-slate-200 dark:border-[#263142] hover:border-[#2F5DA8]/60 dark:hover:border-[#2F5DA8]/60 shadow-xs'
      }`}
    >
      {/* 1. Header & Insignia */}
      <div className="flex items-center justify-between gap-2 mb-3 pb-2.5 border-b border-slate-100 dark:border-[#263142]">
        <div className="flex items-center gap-2">
          <img 
            src="https://upload.wikimedia.org/wikipedia/commons/a/aa/Seal_of_Karnataka.svg" 
            alt="Aloka Emblem" 
            className="w-5 h-5 object-contain"
          />
          <div className="flex flex-col">
            <span className="text-[11px] font-mono font-bold uppercase tracking-wider text-slate-900 dark:text-slate-100">
              Aloka Intelligence
            </span>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {activeCaseId && (
            <div className="hidden sm:flex items-center gap-1 text-[10px] font-mono font-bold text-amber-700 dark:text-amber-400 bg-amber-50 dark:bg-amber-950/40 px-2 py-0.5 rounded border border-amber-200 dark:border-amber-900/50">
              <span className="w-1.5 h-1.5 rounded-full bg-amber-500"></span>
              <span>ACTIVE CASE: {activeCaseId}</span>
            </div>
          )}

          {hasData && (
            <div className="flex items-center gap-1 text-[10px] font-mono font-bold uppercase text-[#2F5DA8] dark:text-[#93B4E8] bg-slate-100 dark:bg-[#172640] px-2 py-0.5 rounded border border-slate-200 dark:border-[#263142]">
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
      <div className="flex items-center justify-between gap-4 mt-4 pt-3 border-t border-slate-100 dark:border-[#263142] select-none">
        <div className="flex items-center gap-4">
          <button 
            type="button"
            onClick={(e) => {
              e.stopPropagation();
              handleCopy(textContent);
            }}
            className="flex items-center gap-1.5 text-xs font-medium text-slate-500 hover:text-[#2F5DA8] dark:text-slate-400 dark:hover:text-[#93B4E8] transition-colors cursor-pointer" 
            title="Copy intelligence report"
            aria-label="Copy report"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-emerald-500" /> : <Copy className="w-3.5 h-3.5" />}
            <span>{copied ? 'Copied' : 'Copy'}</span>
          </button>
          
          <div className="flex items-center gap-1.5 text-xs font-medium text-slate-500 dark:text-slate-400 hover:text-[#2F5DA8] dark:hover:text-[#93B4E8]">
            <Globe className="w-3.5 h-3.5" />
            <select 
              defaultValue=""
              onClick={(e) => e.stopPropagation()}
              onChange={(e) => {
                onTranslate(e, textContent, index);
                e.target.value = "";
              }}
              className="bg-transparent border-none text-xs font-medium focus:ring-0 cursor-pointer outline-none text-slate-500 dark:text-slate-400 hover:text-[#2F5DA8] dark:hover:text-[#93B4E8]"
              aria-label="Translate message"
            >
              <option value="" disabled className="dark:bg-[#101722]">Translate</option>
              <option value="English" className="dark:bg-[#101722]">English</option>
              <option value="Kannada" className="dark:bg-[#101722]">Kannada (ಕನ್ನಡ)</option>
              <option value="Hindi" className="dark:bg-[#101722]">Hindi (हिन्दी)</option>
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

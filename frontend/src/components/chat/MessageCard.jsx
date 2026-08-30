import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Copy, Check, Globe, Shield, User, AlertCircle, ArrowUpRight } from 'lucide-react';

const mdComponents = {
  h1: ({ children }) => (
    <h1 className="text-base sm:text-lg font-bold text-slate-900 dark:text-slate-100 mb-2.5 block border-b border-slate-200 dark:border-slate-800 pb-1 tracking-tight">{children}</h1>
  ),
  h2: ({ children }) => (
    <h2 className="text-sm sm:text-base font-bold text-blue-900 dark:text-blue-400 mt-3 mb-2 block tracking-tight">{children}</h2>
  ),
  h3: ({ children }) => (
    <h3 className="text-xs sm:text-sm font-semibold text-slate-800 dark:text-slate-200 mt-2 mb-1 block uppercase tracking-wider">{children}</h3>
  ),
  p: ({ children }) => (
    <p className="text-xs sm:text-sm text-slate-700 dark:text-slate-300 mb-2 leading-relaxed block">{children}</p>
  ),
  strong: ({ children }) => (
    <strong className="font-bold text-slate-900 dark:text-slate-100">{children}</strong>
  ),
  em: ({ children }) => (
    <em className="italic text-blue-800 dark:text-blue-300 font-medium">{children}</em>
  ),
  ul: ({ children }) => (
    <ul className="list-disc pl-5 space-y-1 mb-2.5 text-slate-700 dark:text-slate-300 text-xs sm:text-sm">{children}</ul>
  ),
  ol: ({ children }) => (
    <ol className="list-decimal pl-5 space-y-1 mb-2.5 text-slate-700 dark:text-slate-300 text-xs sm:text-sm">{children}</ol>
  ),
  li: ({ children }) => (
    <li className="marker:text-blue-600 dark:marker:text-blue-400 leading-relaxed pl-0.5">{children}</li>
  ),
  code: ({ inline, children }) =>
    inline ? (
      <code className="font-mono text-cyan-800 dark:text-cyan-300 bg-cyan-50 dark:bg-cyan-950/60 px-1.5 py-0.5 rounded text-[11px] font-semibold border border-cyan-200/80 dark:border-cyan-800/40">{children}</code>
    ) : (
      <pre className="font-mono text-slate-800 dark:text-slate-200 bg-slate-100 dark:bg-slate-900 p-3 rounded-lg overflow-x-auto text-xs border border-slate-200 dark:border-slate-800 my-2 leading-relaxed shadow-xs">
        <code>{children}</code>
      </pre>
    ),
  blockquote: ({ children }) => (
    <blockquote className="border-l-3 border-blue-600 pl-3 text-slate-600 dark:text-slate-400 italic my-2 text-xs">{children}</blockquote>
  ),
  table: ({ children }) => (
    <div className="overflow-x-auto my-3 rounded-xl border border-slate-200 dark:border-slate-800 shadow-xs">
      <table className="min-w-full text-xs divide-y divide-slate-200 dark:divide-slate-800">{children}</table>
    </div>
  ),
  thead: ({ children }) => <thead className="bg-slate-100 dark:bg-slate-800 text-slate-800 dark:text-slate-200 font-bold uppercase text-[11px]">{children}</thead>,
  th: ({ children }) => <th className="px-3.5 py-2.5 text-left tracking-wider">{children}</th>,
  tbody: ({ children }) => <tbody className="divide-y divide-slate-100 dark:divide-slate-800/80">{children}</tbody>,
  td: ({ children }) => <td className="px-3.5 py-2 text-slate-700 dark:text-slate-300">{children}</td>,
  tr: ({ children }) => <tr className="hover:bg-slate-50 dark:hover:bg-slate-800/40 transition-colors">{children}</tr>,
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

  if (isUser) {
    return (
      <div className="bg-blue-50/70 dark:bg-slate-900/90 p-3.5 rounded-2xl border border-blue-200/70 dark:border-slate-700/80 shadow-xs mb-3 animate-fade-in">
        <div className="flex items-center gap-2 mb-1.5">
          <div className="w-5 h-5 rounded-full bg-blue-900 dark:bg-blue-700 flex items-center justify-center text-[10px] font-bold text-white shadow-xs">
            <User className="w-3 h-3" />
          </div>
          <span className="text-[10px] font-mono font-bold uppercase tracking-wider text-slate-600 dark:text-slate-400">
            Investigator Inquiry
          </span>
        </div>
        <div className="text-xs sm:text-sm text-slate-900 dark:text-slate-100 font-medium leading-relaxed">
          {msg.text || msg.user_query}
        </div>
      </div>
    );
  }

  if (isSystem) {
    return (
      <div className="bg-amber-50/80 dark:bg-amber-950/20 p-3.5 rounded-2xl border border-amber-200 dark:border-amber-900/40 shadow-xs mb-3 animate-fade-in">
        <div className="flex items-center gap-2 mb-1.5">
          <AlertCircle className="w-4 h-4 text-amber-600 dark:text-amber-400 shrink-0" />
          <span className="text-[10px] font-bold uppercase tracking-wider text-amber-800 dark:text-amber-300 font-mono">
            Intelligence Notice
          </span>
        </div>
        <div className="prose dark:prose-invert prose-sm text-xs sm:text-sm text-amber-900 dark:text-amber-200">
          <ReactMarkdown remarkPlugins={[remarkGfm]} components={mdComponents}>{msg.text}</ReactMarkdown>
        </div>
      </div>
    );
  }

  const messageText = msg.text || msg.response || '';
  const hasData = (msg.all_sql_results && msg.all_sql_results.length > 0) || (msg.sql_results && msg.sql_results.length > 0);

  return (
    <div
      onClick={() => {
        if (hasData) onSelect(index);
      }}
      className={`p-4 sm:p-5 rounded-2xl border mb-3 transition-all duration-200 animate-fade-in cursor-pointer ${
        isSelected
          ? 'bg-white dark:bg-slate-900 border-blue-500 dark:border-blue-500 shadow-md ring-1 ring-blue-500/25'
          : 'bg-white dark:bg-slate-900/90 border-slate-200 dark:border-slate-800/90 hover:border-blue-300 dark:hover:border-slate-700 shadow-xs'
      }`}
    >
      {/* Header Avatar & Tag */}
      <div className="flex items-center justify-between gap-2 mb-2.5 pb-2 border-b border-slate-100 dark:border-slate-800/80">
        <div className="flex items-center gap-2">
          <img 
            src="https://upload.wikimedia.org/wikipedia/commons/a/aa/Seal_of_Karnataka.svg" 
            alt="Aloka Emblem" 
            className="w-5 h-5 object-contain drop-shadow-xs"
          />
          <span className="text-[11px] font-mono font-bold uppercase tracking-wider text-slate-800 dark:text-slate-200">
            Aloka Intelligence Report
          </span>
        </div>

        {hasData && (
          <div className="flex items-center gap-1 text-[10px] font-mono font-bold uppercase text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-950/80 px-2 py-0.5 rounded border border-blue-200 dark:border-blue-800/60">
            <span>Canvas Linked</span>
            <ArrowUpRight className="w-3 h-3" />
          </div>
        )}
      </div>

      {/* Structured Prose Response */}
      <div className="prose dark:prose-invert prose-sm max-w-none text-slate-700 dark:text-slate-300">
        <ReactMarkdown remarkPlugins={[remarkGfm]} components={mdComponents}>{messageText}</ReactMarkdown>
      </div>

      {/* Action Toolbar */}
      <div className="flex items-center gap-4 mt-3 pt-2.5 border-t border-slate-100 dark:border-slate-800/80 select-none">
        <button 
          onClick={(e) => {
            e.stopPropagation();
            handleCopy(messageText);
          }}
          className="flex items-center gap-1.5 text-xs font-medium text-slate-500 hover:text-blue-600 dark:text-slate-400 dark:hover:text-blue-400 transition-colors cursor-pointer" 
          title="Copy report to clipboard"
        >
          {copied ? <Check className="w-3.5 h-3.5 text-emerald-500" /> : <Copy className="w-3.5 h-3.5" />}
          <span>{copied ? 'Copied' : 'Copy'}</span>
        </button>
        
        <div className="flex items-center gap-1.5 text-xs font-medium text-slate-500 dark:text-slate-400 hover:text-blue-600 dark:hover:text-blue-400">
          <Globe className="w-3.5 h-3.5" />
          <select 
            defaultValue=""
            onClick={(e) => e.stopPropagation()}
            onChange={(e) => {
              onTranslate(e, messageText, index);
              e.target.value = "";
            }}
            className="bg-transparent border-none text-xs font-medium focus:ring-0 cursor-pointer outline-none text-slate-500 dark:text-slate-400 hover:text-blue-600 dark:hover:text-blue-400"
          >
            <option value="" disabled className="dark:bg-slate-900">Translate</option>
            <option value="English" className="dark:bg-slate-900">English</option>
            <option value="Kannada" className="dark:bg-slate-900">Kannada (ಕನ್ನಡ)</option>
            <option value="Hindi" className="dark:bg-slate-900">Hindi (हिन्दी)</option>
          </select>
        </div>
      </div>
    </div>
  );
}

import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Copy, Check, Globe, User, ShieldAlert } from 'lucide-react';

const mdComponents = {
  h1: ({ children }) => (
    <h1 className="text-lg font-bold text-slate-900 dark:text-slate-100 mb-3 block border-b border-slate-200 dark:border-slate-800 pb-1">{children}</h1>
  ),
  h2: ({ children }) => (
    <h2 className="text-base font-bold text-blue-900 dark:text-blue-400 mt-3 mb-2 block">{children}</h2>
  ),
  h3: ({ children }) => (
    <h3 className="text-sm font-semibold text-slate-800 dark:text-slate-200 mt-2 mb-1 block">{children}</h3>
  ),
  p: ({ children }) => (
    <p className="text-xs text-slate-700 dark:text-slate-300 mb-2.5 leading-relaxed block">{children}</p>
  ),
  strong: ({ children }) => (
    <strong className="font-semibold text-slate-900 dark:text-slate-100">{children}</strong>
  ),
  em: ({ children }) => (
    <em className="italic text-blue-800 dark:text-blue-300">{children}</em>
  ),
  ul: ({ children }) => (
    <ul className="list-disc pl-5 space-y-1 mb-2.5 text-slate-700 dark:text-slate-300 text-xs">{children}</ul>
  ),
  ol: ({ children }) => (
    <ol className="list-decimal pl-5 space-y-1 mb-2.5 text-slate-700 dark:text-slate-300 text-xs">{children}</ol>
  ),
  li: ({ children }) => (
    <li className="marker:text-blue-600 dark:marker:text-blue-400 leading-relaxed">{children}</li>
  ),
  code: ({ inline, children }) =>
    inline ? (
      <code className="font-mono text-blue-800 dark:text-blue-300 bg-blue-50 dark:bg-blue-950/60 px-1 py-0.5 rounded text-[11px] border border-blue-100 dark:border-blue-900/40">{children}</code>
    ) : (
      <pre className="font-mono text-slate-800 dark:text-slate-200 bg-slate-100 dark:bg-slate-900 p-3 rounded-lg overflow-x-auto text-[11px] border border-slate-200 dark:border-slate-800 my-2 leading-relaxed shadow-xs">
        <code>{children}</code>
      </pre>
    ),
  blockquote: ({ children }) => (
    <blockquote className="border-l-4 border-blue-500 pl-3 text-slate-600 dark:text-slate-400 italic my-2 text-xs">{children}</blockquote>
  ),
  table: ({ children }) => (
    <div className="overflow-x-auto my-2.5 rounded-lg border border-slate-200 dark:border-slate-800">
      <table className="min-w-full text-xs divide-y divide-slate-200 dark:divide-slate-800">{children}</table>
    </div>
  ),
  thead: ({ children }) => <thead className="bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-200 font-semibold">{children}</thead>,
  th: ({ children }) => <th className="px-3 py-2 text-left">{children}</th>,
  tbody: ({ children }) => <tbody className="divide-y divide-slate-100 dark:divide-slate-800/60">{children}</tbody>,
  td: ({ children }) => <td className="px-3 py-2 text-slate-700 dark:text-slate-300">{children}</td>,
  tr: ({ children }) => <tr className="hover:bg-slate-50/60 dark:hover:bg-slate-800/40">{children}</tr>,
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
      <div className="bg-blue-50/80 dark:bg-blue-950/25 p-4 rounded-xl border border-blue-100 dark:border-blue-900/40 shadow-xs mb-3 animate-fade-in">
        <div className="flex items-center gap-2 mb-1.5">
          <div className="w-5 h-5 rounded-full bg-blue-900 dark:bg-blue-800 flex items-center justify-center text-[10px] font-bold text-white shadow-xs">
            <User className="w-3 h-3" />
          </div>
          <span className="text-[10px] font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">
            Investigator Query
          </span>
        </div>
        <div className="text-xs text-slate-800 dark:text-slate-100 font-medium leading-relaxed">
          {msg.text || msg.user_query}
        </div>
      </div>
    );
  }

  if (isSystem) {
    return (
      <div className="bg-amber-50 dark:bg-amber-950/30 p-4 rounded-xl border border-amber-200 dark:border-amber-900/50 shadow-xs mb-3 animate-fade-in">
        <div className="flex items-center gap-2 mb-1.5">
          <ShieldAlert className="w-4 h-4 text-amber-600 dark:text-amber-400" />
          <span className="text-[10px] font-bold uppercase tracking-wider text-amber-700 dark:text-amber-300">
            System Notice
          </span>
        </div>
        <div className="prose dark:prose-invert prose-sm text-xs text-amber-900 dark:text-amber-200">
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
      className={`p-4 rounded-xl border mb-3 transition-all duration-200 animate-fade-in cursor-pointer ${
        isSelected
          ? 'bg-white dark:bg-slate-900 border-blue-500 dark:border-blue-500 shadow-md ring-1 ring-blue-500/20'
          : 'bg-white dark:bg-slate-900 border-slate-200/90 dark:border-slate-800 hover:border-blue-300 dark:hover:border-slate-700 shadow-xs'
      }`}
    >
      <div className="flex items-center justify-between gap-2 mb-2">
        <div className="flex items-center gap-2">
          <img 
            src="https://upload.wikimedia.org/wikipedia/commons/a/aa/Seal_of_Karnataka.svg" 
            alt="Aloka Emblem" 
            className="w-5 h-5 object-contain drop-shadow-xs"
          />
          <span className="text-[10px] font-bold uppercase tracking-widest text-slate-600 dark:text-slate-300">
            Aloka Intelligence
          </span>
        </div>
        {hasData && (
          <span className="text-[9px] font-bold uppercase tracking-wider px-1.5 py-0.5 rounded bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400">
            Data Canvas Linked
          </span>
        )}
      </div>

      <div className="prose dark:prose-invert prose-sm max-w-none text-slate-700 dark:text-slate-300">
        <ReactMarkdown remarkPlugins={[remarkGfm]} components={mdComponents}>{messageText}</ReactMarkdown>
      </div>

      {/* Action Toolbar */}
      <div className="flex items-center gap-4 mt-3 pt-2.5 border-t border-slate-100 dark:border-slate-800/80">
        <button 
          onClick={(e) => {
            e.stopPropagation();
            handleCopy(messageText);
          }}
          className="flex items-center gap-1.5 text-[11px] font-medium text-slate-500 hover:text-blue-600 dark:text-slate-400 dark:hover:text-blue-400 transition-colors cursor-pointer" 
          title="Copy response to clipboard"
        >
          {copied ? <Check className="w-3.5 h-3.5 text-emerald-500" /> : <Copy className="w-3.5 h-3.5" />}
          <span>{copied ? 'Copied' : 'Copy'}</span>
        </button>
        
        <div className="flex items-center gap-1.5 text-[11px] font-medium text-slate-500 dark:text-slate-400 hover:text-blue-600 dark:hover:text-blue-400">
          <Globe className="w-3.5 h-3.5" />
          <select 
            defaultValue=""
            onClick={(e) => e.stopPropagation()}
            onChange={(e) => {
              onTranslate(e, messageText, index);
              e.target.value = "";
            }}
            className="bg-transparent border-none text-[11px] font-medium focus:ring-0 cursor-pointer outline-none text-slate-500 dark:text-slate-400 hover:text-blue-600 dark:hover:text-blue-400"
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

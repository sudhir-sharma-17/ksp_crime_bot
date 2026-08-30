import React from 'react';
import MessageCard from './MessageCard';
import Composer from './Composer';
import { Shield, Square, Sparkles, FolderSearch, BarChart3, Search, Building2 } from 'lucide-react';

const SUGGESTIONS = [
  {
    title: "Investigate a Case",
    description: "Lookup accused, victims & IPC sections",
    query: "Who are the accused in KSP-CASE-0004?",
    icon: FolderSearch,
    accent: "text-blue-500"
  },
  {
    title: "Analyze Case Data",
    description: "Time-series crime trends & distributions",
    query: "Show me the number of cases registered over time.",
    icon: BarChart3,
    accent: "text-cyan-500"
  },
  {
    title: "Find Similar Cases",
    description: "Semantic search across brief facts",
    query: "Find cases related to vehicle theft and burglary",
    icon: Search,
    accent: "text-emerald-500"
  },
  {
    title: "Explore Police Stations",
    description: "Station workload and case count rankings",
    query: "Which police station has registered the most cases?",
    icon: Building2,
    accent: "text-amber-500"
  }
];

export default function ChatStream({
  chatWidth,
  messages,
  activeDataIndex,
  setActiveDataIndex,
  handleTranslate,
  isLoading,
  cancelQuery,
  queryQueue,
  setQueryQueue,
  inputVal,
  setInputVal,
  handleSendMessage,
  isListening,
  toggleVoiceCommand,
  messagesEndRef,
  inputRef
}) {
  const isFreshSession = messages.length <= 1;

  const handleSuggestionClick = (query) => {
    setInputVal(query);
    inputRef.current?.focus();
  };

  return (
    <section 
      className="bg-slate-50 dark:bg-slate-950 flex flex-col relative shrink-0 transition-colors duration-200 overflow-hidden h-full select-text"
      style={{ width: `${chatWidth}px` }}
    >
      {/* Stream Messages Scrollable Area */}
      <div className="flex-1 overflow-y-auto p-4 sm:p-5 space-y-3">
        {/* Landing State with Command Center Suggestions */}
        {isFreshSession && (
          <div className="flex flex-col items-center justify-center py-6 px-2 text-center animate-fade-in select-none">
            <div className="w-16 h-16 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 flex items-center justify-center shadow-xs mb-4 p-2.5">
              <img 
                src="https://upload.wikimedia.org/wikipedia/commons/a/aa/Seal_of_Karnataka.svg" 
                alt="KSP Emblem" 
                className="w-full h-full object-contain"
              />
            </div>

            <span className="text-[11px] font-mono font-bold uppercase tracking-widest text-blue-600 dark:text-cyan-400 mb-1">
              State Intelligence Command Center
            </span>
            <h1 className="text-xl sm:text-2xl font-black text-slate-900 dark:text-slate-100 tracking-tight mb-2">
              ALOKA INTELLIGENCE
            </h1>
            <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 max-w-md mb-6 leading-relaxed">
              "How can I assist your investigation today? Ask any case lookup, statistical analysis, or semantic inquiry."
            </p>

            {/* 4 Interactive Suggestion Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5 w-full text-left max-w-lg mb-4">
              {SUGGESTIONS.map((item, idx) => {
                const Icon = item.icon;
                return (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => handleSuggestionClick(item.query)}
                    className="p-3.5 rounded-xl bg-white dark:bg-slate-900 hover:bg-blue-50/60 dark:hover:bg-slate-850 border border-slate-200 dark:border-slate-800 hover:border-blue-400 dark:hover:border-slate-700 shadow-xs transition-all text-left cursor-pointer group"
                  >
                    <div className="flex items-center gap-2 mb-1">
                      <Icon className={`w-4 h-4 ${item.accent}`} />
                      <span className="text-xs font-bold text-slate-900 dark:text-slate-100 group-hover:text-blue-600 dark:group-hover:text-cyan-400 transition-colors">
                        {item.title}
                      </span>
                    </div>
                    <p className="text-[11px] text-slate-500 dark:text-slate-400 line-clamp-1">
                      {item.description}
                    </p>
                  </button>
                );
              })}
            </div>
          </div>
        )}

        {/* Active Conversation Messages */}
        {!isFreshSession && messages.map((msg, index) => (
          <MessageCard
            key={index}
            msg={msg}
            index={index}
            isSelected={activeDataIndex === index}
            onSelect={setActiveDataIndex}
            onTranslate={handleTranslate}
          />
        ))}

        {/* Polished Thinking Status */}
        {isLoading && (
          <div className="flex items-center justify-between p-4 rounded-2xl bg-blue-50/90 dark:bg-slate-900 border border-blue-200 dark:border-slate-800 shadow-xs animate-fade-in mb-3 select-none">
            <div className="flex items-center gap-3">
              <div className="relative w-8 h-8 rounded-xl bg-white dark:bg-slate-800 flex items-center justify-center shadow-xs border border-slate-200 dark:border-slate-700 shrink-0">
                <img 
                  src="https://upload.wikimedia.org/wikipedia/commons/a/aa/Seal_of_Karnataka.svg" 
                  alt="Thinking Emblem" 
                  className="w-4 h-4 object-contain animate-pulse"
                />
              </div>
              <div className="flex flex-col">
                <div className="flex items-center gap-1.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-cyan-500 animate-ping"></span>
                  <span className="text-[11px] font-mono font-bold text-blue-950 dark:text-cyan-300 uppercase tracking-widest">
                    ANALYZING REQUEST
                  </span>
                </div>
                <div className="flex items-center gap-1 text-xs text-slate-600 dark:text-slate-400 font-medium">
                  <span>Querying criminological database</span>
                  <span className="flex gap-0.5 ml-1">
                    <span className="w-1 h-1 bg-cyan-600 dark:bg-cyan-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
                    <span className="w-1 h-1 bg-cyan-600 dark:bg-cyan-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
                    <span className="w-1 h-1 bg-cyan-600 dark:bg-cyan-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
                  </span>
                </div>
              </div>
            </div>

            {/* Terminate Query Button */}
            <button
              type="button"
              onClick={cancelQuery}
              className="flex items-center gap-1.5 bg-rose-600 hover:bg-rose-700 text-white text-xs font-bold py-1.5 px-3 rounded-xl shadow-xs transition-all cursor-pointer select-none"
              title="Cancel running query"
              aria-label="Terminate query"
            >
              <Square className="w-3 h-3 fill-current" />
              <span>Terminate</span>
            </button>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Fixed Sticky Composer */}
      <Composer
        inputVal={inputVal}
        setInputVal={setInputVal}
        handleSendMessage={handleSendMessage}
        isLoading={isLoading}
        queryQueue={queryQueue}
        setQueryQueue={setQueryQueue}
        isListening={isListening}
        toggleVoiceCommand={toggleVoiceCommand}
        inputRef={inputRef}
      />
    </section>
  );
}

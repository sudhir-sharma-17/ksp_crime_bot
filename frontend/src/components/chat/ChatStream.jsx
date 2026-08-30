import React from 'react';
import MessageCard from './MessageCard';
import Composer from './Composer';
import ProcessingCard from './ProcessingCard';
import { FolderSearch, BarChart3, Search, Building2 } from 'lucide-react';

const SUGGESTIONS = [
  {
    title: "Investigate a Case",
    description: "Lookup accused, victims & IPC sections",
    query: "Who are the accused in KSP-CASE-0004?",
    icon: FolderSearch,
    accent: "text-[#2F5DA8] dark:text-[#93B4E8]"
  },
  {
    title: "Analyze Case Data",
    description: "Time-series crime trends & distributions",
    query: "Show me the number of cases registered over time.",
    icon: BarChart3,
    accent: "text-[#4B72B0] dark:text-[#A7C4F2]"
  },
  {
    title: "Find Similar Cases",
    description: "Semantic search across brief facts",
    query: "Find cases related to vehicle theft and burglary",
    icon: Search,
    accent: "text-emerald-600 dark:text-emerald-400"
  },
  {
    title: "Explore Police Stations",
    description: "Station workload and case count rankings",
    query: "Which police station has registered the most cases?",
    icon: Building2,
    accent: "text-amber-600 dark:text-amber-400"
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
      className="bg-[#F4F6F9] dark:bg-[#0B1017] flex flex-col relative shrink-0 transition-colors duration-200 overflow-hidden h-full select-text"
      style={{ width: `${chatWidth}px` }}
    >
      {/* Stream Messages Scrollable Area */}
      <div className="flex-1 overflow-y-auto p-4 sm:p-5 space-y-3">
        {/* Landing State with Command Center Suggestions */}
        {isFreshSession && (
          <div className="flex flex-col items-center justify-center py-6 px-2 text-center animate-fade-in select-none">
            <div className="w-16 h-16 rounded-2xl bg-white dark:bg-[#141C28] border border-slate-200 dark:border-[#263142] flex items-center justify-center shadow-xs mb-4 p-2.5">
              <img 
                src="https://upload.wikimedia.org/wikipedia/commons/a/aa/Seal_of_Karnataka.svg" 
                alt="KSP Emblem" 
                className="w-full h-full object-contain"
              />
            </div>

            <span className="text-[11px] font-mono font-bold uppercase tracking-widest text-[#2F5DA8] dark:text-[#93B4E8] mb-1">
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
                    className="p-3.5 rounded-xl bg-white dark:bg-[#141C28] hover:bg-slate-50 dark:hover:bg-[#172640] border border-slate-200 dark:border-[#263142] hover:border-[#2F5DA8] dark:hover:border-[#2F5DA8] shadow-xs transition-all text-left cursor-pointer group"
                  >
                    <div className="flex items-center gap-2 mb-1">
                      <Icon className={`w-4 h-4 ${item.accent}`} />
                      <span className="text-xs font-bold text-slate-900 dark:text-slate-100 group-hover:text-[#2F5DA8] dark:group-hover:text-[#93B4E8] transition-colors">
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

        {/* AI Analysis Processing Card */}
        {isLoading && (
          <ProcessingCard onTerminate={cancelQuery} />
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Fixed Sticky Composer */}
      <Composer
        inputVal={inputVal}
        setInputVal={setInputVal}
        handleSendMessage={handleSendMessage}
        isLoading={isLoading}
        isListening={isListening}
        toggleVoiceCommand={toggleVoiceCommand}
        queryQueue={queryQueue}
        setQueryQueue={setQueryQueue}
        inputRef={inputRef}
      />
    </section>
  );
}

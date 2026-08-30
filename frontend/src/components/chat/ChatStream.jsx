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
    accent: "text-blue-600 dark:text-[#93B4E8]",
    iconBg: "bg-blue-50 dark:bg-blue-950/40 border-blue-100 dark:border-blue-900/50"
  },
  {
    title: "Analyze Case Data",
    description: "Time-series crime trends & distributions",
    query: "Show me the number of cases registered over time.",
    icon: BarChart3,
    accent: "text-indigo-600 dark:text-[#A7C4F2]",
    iconBg: "bg-indigo-50 dark:bg-indigo-950/40 border-indigo-100 dark:border-indigo-900/50"
  },
  {
    title: "Find Similar Cases",
    description: "Semantic search across brief facts",
    query: "Find cases related to vehicle theft and burglary",
    icon: Search,
    accent: "text-emerald-600 dark:text-emerald-400",
    iconBg: "bg-emerald-50 dark:bg-emerald-950/40 border-emerald-100 dark:border-emerald-900/50"
  },
  {
    title: "Explore Police Stations",
    description: "Station workload and case count rankings",
    query: "Which police station has registered the most cases?",
    icon: Building2,
    accent: "text-amber-600 dark:text-amber-400",
    iconBg: "bg-amber-50 dark:bg-amber-950/40 border-amber-100 dark:border-amber-900/50"
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
      className="bg-[#F8FAFC] dark:bg-[#0B1017] flex flex-col relative shrink-0 transition-colors duration-200 overflow-hidden h-full select-text"
      style={{ width: `${chatWidth}px` }}
    >
      {/* Stream Messages Scrollable Area */}
      <div className="flex-1 overflow-y-auto p-4 sm:p-5 space-y-3.5">
        {/* Landing State with Command Center Suggestions */}
        {isFreshSession && (
          <div className="flex flex-col items-center justify-center py-8 px-2 text-center select-none">
            <div className="w-16 h-16 rounded-2xl bg-white dark:bg-[#141C28] border border-slate-200 dark:border-[#263142] flex items-center justify-center shadow-[0_4px_20px_-4px_rgba(37,99,235,0.12)] mb-4 p-3 anim-landing-seal">
              <img 
                src="https://upload.wikimedia.org/wikipedia/commons/a/aa/Seal_of_Karnataka.svg" 
                alt="KSP Emblem" 
                className="w-full h-full object-contain"
              />
            </div>

            <span className="text-[11px] font-mono font-bold uppercase tracking-widest text-blue-600 dark:text-[#93B4E8] mb-1 anim-landing-badge">
              State Intelligence Command Center
            </span>
            <h1 className="text-2xl sm:text-3xl font-black text-slate-900 dark:text-slate-100 tracking-wider mb-2 font-mono uppercase anim-landing-title">
              ALOKA INTELLIGENCE
            </h1>
            <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 max-w-md mb-7 leading-relaxed font-normal anim-landing-desc">
              "How can I assist your investigation today? Ask any case lookup, statistical analysis, or semantic inquiry."
            </p>

            {/* 4 Interactive Suggestion Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full text-left max-w-lg mb-4">
              {SUGGESTIONS.map((item, idx) => {
                const Icon = item.icon;
                const cardAnimClass = `anim-landing-card-${idx + 1}`;
                return (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => handleSuggestionClick(item.query)}
                    className={`p-3.5 rounded-2xl bg-white dark:bg-[#141C28] hover:bg-slate-50/90 dark:hover:bg-[#172640] border border-slate-200/90 dark:border-[#263142] hover:border-blue-500 dark:hover:border-blue-500 shadow-[0_1px_3px_rgba(0,0,0,0.04)] hover:shadow-md transition-all duration-200 text-left cursor-pointer group ${cardAnimClass}`}
                  >
                    <div className="flex items-center gap-2.5 mb-1.5">
                      <div className={`p-1.5 rounded-xl border ${item.iconBg} shrink-0`}>
                        <Icon className={`w-4 h-4 ${item.accent}`} />
                      </div>
                      <span className="text-xs font-bold text-slate-900 dark:text-slate-100 group-hover:text-blue-600 dark:group-hover:text-[#93B4E8] transition-colors">
                        {item.title}
                      </span>
                    </div>
                    <p className="text-[11px] text-slate-500 dark:text-slate-400 line-clamp-1 font-normal pl-0.5">
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

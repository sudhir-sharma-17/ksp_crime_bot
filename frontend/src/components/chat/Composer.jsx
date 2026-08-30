import React from 'react';
import { ArrowUp, Mic, X, Terminal } from 'lucide-react';

export default function Composer({
  inputVal,
  setInputVal,
  handleSendMessage,
  isLoading,
  queryQueue,
  setQueryQueue,
  isListening,
  toggleVoiceCommand,
  inputRef
}) {
  return (
    <div className="bg-[#F4F6F9] dark:bg-[#0B1017] border-t border-slate-200 dark:border-[#263142] p-3 sm:p-4 shrink-0 transition-colors">
      {/* Queued Queries Indicator */}
      {queryQueue.length > 0 && (
        <div className="mb-2.5 flex items-center justify-between px-3.5 py-2 bg-slate-100 dark:bg-[#141C28] border border-slate-200 dark:border-[#263142] rounded-xl text-xs animate-fade-in">
          <div className="flex items-center gap-2 truncate">
            <span className="flex h-2 w-2 relative shrink-0">
              <span className="relative inline-flex rounded-full h-2 w-2 bg-[#2F5DA8]"></span>
            </span>
            <span className="font-mono font-bold uppercase tracking-wider text-[10px] text-[#2F5DA8] dark:text-[#93B4E8] shrink-0">
              Queued ({queryQueue.length}):
            </span>
            <span className="truncate italic text-slate-700 dark:text-slate-300 font-medium">
              "{queryQueue[0]}"{queryQueue.length > 1 ? ` (+${queryQueue.length - 1} more)` : ''}
            </span>
          </div>
          <button
            type="button"
            onClick={() => setQueryQueue([])}
            className="flex items-center gap-1 text-slate-400 hover:text-red-500 text-[10px] font-bold uppercase ml-2 px-2 py-0.5 rounded hover:bg-red-50 dark:hover:bg-[#101722] cursor-pointer transition-colors"
            title="Clear queued queries"
          >
            <X className="w-3 h-3" />
            <span>Clear</span>
          </button>
        </div>
      )}

      {/* Input Form */}
      <form
        onSubmit={handleSendMessage}
        className="relative flex items-center bg-white dark:bg-[#101722] border border-slate-300 dark:border-[#263142] rounded-xl focus-within:border-[#2F5DA8] dark:focus-within:border-[#2F5DA8] focus-within:ring-1 focus-within:ring-[#2F5DA8]/40 transition-all p-1"
      >
        <div className="pl-3 text-slate-400 dark:text-slate-500 hidden sm:block">
          <Terminal className="w-4 h-4" />
        </div>

        <input
          ref={inputRef}
          type="text"
          value={inputVal}
          onChange={(e) => setInputVal(e.target.value)}
          placeholder={
            isLoading
              ? "Executing inquiry... Type next query to queue for sequential processing..."
              : "Ask Aloka (e.g., 'Who are the accused in KSP-CASE-0004?', 'Show cases by station')..."
          }
          className="flex-1 bg-transparent border-none focus:ring-0 text-slate-900 dark:text-slate-100 text-xs sm:text-sm placeholder-slate-400 dark:placeholder-slate-500 py-2 px-3 outline-none font-medium"
        />

        {/* Voice Command Button */}
        <button 
          type="button"
          onClick={toggleVoiceCommand} 
          className={`p-2 rounded-lg transition-all shrink-0 cursor-pointer ${
            isListening 
              ? 'bg-red-500 text-white animate-pulse' 
              : 'text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-[#141C28]'
          }`}
          title={isListening ? "Listening... Click to stop" : "Voice Command"}
        >
          <Mic className="w-4 h-4" />
        </button>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={!inputVal.trim()}
          className="w-8 h-8 bg-[#2F5DA8] hover:bg-[#3A6DBD] disabled:bg-slate-200 dark:disabled:bg-[#141C28] disabled:text-slate-400 text-white rounded-lg flex items-center justify-center transition-all shrink-0 cursor-pointer disabled:cursor-not-allowed"
          title={isLoading ? "Queue query" : "Send inquiry"}
        >
          <ArrowUp className="w-4 h-4 stroke-[2.5]" />
        </button>
      </form>
    </div>
  );
}

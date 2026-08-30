import React from 'react';
import { ArrowUp, Mic, X } from 'lucide-react';

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
    <div className="bg-slate-50 dark:bg-slate-950 border-t border-slate-200 dark:border-slate-800/80 p-3.5 shrink-0 transition-colors">
      {/* Queued Queries Indicator */}
      {queryQueue.length > 0 && (
        <div className="mb-2.5 flex items-center justify-between px-3 py-1.5 bg-blue-50/90 dark:bg-slate-900/90 border border-blue-200/80 dark:border-blue-900/50 rounded-lg text-xs shadow-xs animate-fade-in">
          <div className="flex items-center gap-2 truncate">
            <span className="flex h-2 w-2 relative shrink-0">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-blue-600"></span>
            </span>
            <span className="font-bold uppercase tracking-wider text-[10px] text-blue-800 dark:text-blue-300 shrink-0">
              Queued ({queryQueue.length}):
            </span>
            <span className="truncate italic text-slate-700 dark:text-slate-300">
              "{queryQueue[0]}"{queryQueue.length > 1 ? ` (+${queryQueue.length - 1} more)` : ''}
            </span>
          </div>
          <button
            type="button"
            onClick={() => setQueryQueue([])}
            className="flex items-center gap-1 text-slate-400 hover:text-red-500 text-[10px] font-bold uppercase ml-2 px-1.5 py-0.5 rounded hover:bg-red-50 dark:hover:bg-slate-800 cursor-pointer transition-colors"
            title="Clear queued queries"
          >
            <X className="w-3 h-3" />
            <span>Clear</span>
          </button>
        </div>
      )}

      {/* Input Composer Form */}
      <form
        onSubmit={handleSendMessage}
        className="relative flex items-center bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700/80 rounded-xl shadow-xs focus-within:border-blue-600 dark:focus-within:border-blue-500 focus-within:ring-2 focus-within:ring-blue-500/20 transition-all"
      >
        <input
          ref={inputRef}
          type="text"
          value={inputVal}
          onChange={(e) => setInputVal(e.target.value)}
          placeholder={
            isLoading
              ? "Executing query... Type next query to queue for execution..."
              : "Query KSP database (cases, accused, status, trends, etc.)..."
          }
          className="flex-1 bg-transparent border-none focus:ring-0 text-slate-900 dark:text-slate-100 text-xs placeholder-slate-400 dark:placeholder-slate-500 py-3 px-3.5 outline-none"
        />

        {/* Voice Command Button */}
        <button 
          type="button"
          onClick={toggleVoiceCommand} 
          className={`p-2 rounded-lg m-1 transition-all shrink-0 cursor-pointer ${
            isListening 
              ? 'bg-red-500 text-white animate-pulse shadow-xs' 
              : 'text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800'
          }`}
          title={isListening ? "Listening... Click to stop" : "Voice Input"}
        >
          <Mic className="w-4 h-4" />
        </button>

        {/* Submit Action Button */}
        <button
          type="submit"
          disabled={!inputVal.trim()}
          className="m-1 w-8 h-8 bg-blue-900 hover:bg-blue-800 disabled:bg-slate-200 dark:disabled:bg-slate-800 disabled:text-slate-400 text-white rounded-lg flex items-center justify-center transition-all shrink-0 cursor-pointer disabled:cursor-not-allowed shadow-xs"
          title={isLoading ? "Queue query for next execution" : "Execute query"}
        >
          <ArrowUp className="w-4 h-4" />
        </button>
      </form>
    </div>
  );
}

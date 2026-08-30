import React from 'react';
import MessageCard from './MessageCard';
import Composer from './Composer';
import { Shield, Square } from 'lucide-react';

export default function ChatStream({
  chatWidth,
  startChatResize,
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
  return (
    <>
      <section 
        className="bg-slate-50 dark:bg-slate-950 flex flex-col relative border-r border-slate-200 dark:border-slate-800/80 shrink-0 transition-colors duration-300 overflow-hidden"
        style={{ width: `${chatWidth}px` }}
      >
        {/* Stream Messages Container */}
        <div className="flex-1 overflow-y-auto p-4 space-y-3">
          {messages.map((msg, index) => (
            <MessageCard
              key={index}
              msg={msg}
              index={index}
              isSelected={activeDataIndex === index}
              onSelect={setActiveDataIndex}
              onTranslate={handleTranslate}
            />
          ))}

          {/* Real-time Thinking Indicator */}
          {isLoading && (
            <div className="flex items-center justify-between p-3.5 rounded-xl bg-blue-50/80 dark:bg-blue-950/40 border border-blue-100 dark:border-blue-900/40 shadow-xs animate-fade-in mb-3">
              <div className="flex items-center gap-3">
                <div className="relative w-8 h-8 rounded-full bg-white dark:bg-slate-800 flex items-center justify-center shadow-xs border border-slate-200 dark:border-slate-700 shrink-0">
                  <img 
                    src="https://upload.wikimedia.org/wikipedia/commons/a/aa/Seal_of_Karnataka.svg" 
                    alt="Thinking Emblem" 
                    className="w-4 h-4 object-contain animate-pulse"
                  />
                </div>
                <div className="flex flex-col">
                  <span className="text-[10px] font-bold text-blue-900 dark:text-blue-300 uppercase tracking-widest">
                    Aloka Intelligence
                  </span>
                  <div className="flex items-center gap-1 text-xs text-slate-600 dark:text-slate-400 font-medium">
                    <span>Analyzing database records</span>
                    <span className="flex gap-0.5 ml-1">
                      <span className="w-1 h-1 bg-blue-600 dark:bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
                      <span className="w-1 h-1 bg-blue-600 dark:bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
                      <span className="w-1 h-1 bg-blue-600 dark:bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
                    </span>
                  </div>
                </div>
              </div>

              {/* Terminate Query Button */}
              <button
                type="button"
                onClick={cancelQuery}
                className="flex items-center gap-1.5 bg-rose-600 hover:bg-rose-700 text-white text-xs font-bold py-1.5 px-3 rounded-lg shadow-xs transition-all cursor-pointer select-none"
                title="Cancel running query and clear queue"
              >
                <Square className="w-3 h-3 fill-current" />
                <span>Terminate</span>
              </button>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Composer */}
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

      {/* Resize Handle */}
      <div
        onMouseDown={startChatResize}
        className="w-1.5 hover:w-2 bg-transparent hover:bg-blue-600/30 cursor-col-resize self-stretch select-none transition-all z-20"
      />
    </>
  );
}

import React from 'react';
import { Plus, Database, Trash2, Search, ChevronLeft, ChevronRight, FolderClock } from 'lucide-react';

export default function Sidebar({
  sidebarOpen,
  setSidebarOpen,
  sidebarWidth,
  startSidebarResize,
  sessionsList,
  sessionId,
  searchQuery,
  setSearchQuery,
  clearChat,
  handleLoadSession,
  handleDeleteSession
}) {
  return (
    <>
      <aside
        className="bg-white dark:bg-slate-900 border-r border-slate-200 dark:border-slate-800 flex flex-col shrink-0 relative z-10 transition-colors duration-300"
        style={{ width: sidebarOpen ? `${sidebarWidth}px` : '64px' }}
      >
        {/* New Session Button */}
        <div className="p-3 border-b border-slate-100 dark:border-slate-800">
          <button
            onClick={clearChat}
            className={`flex items-center gap-2.5 w-full text-xs font-bold text-white bg-blue-900 hover:bg-blue-800 dark:bg-blue-800 dark:hover:bg-blue-700 shadow-sm py-2.5 px-3 rounded-xl transition-all cursor-pointer ${
              !sidebarOpen ? 'justify-center px-0' : ''
            }`}
            title="Start New Investigation Session"
          >
            <Plus className="w-4 h-4 shrink-0" />
            {sidebarOpen && <span>New Session</span>}
          </button>
        </div>

        {/* Sessions Stream */}
        {sidebarOpen && (
          <div className="flex-1 flex flex-col overflow-hidden px-3 py-2">
            <div className="flex items-center gap-1.5 text-[10px] font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider px-2 mb-2 shrink-0">
              <FolderClock className="w-3 h-3 text-slate-400" />
              <span>Recent Protocols</span>
            </div>
            
            {/* Protocol Search Box */}
            <div className="mb-2 relative shrink-0">
              <Search className="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-1/2 -translate-y-1/2" />
              <input 
                type="text"
                placeholder="Search protocols..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-8 pr-3 py-1.5 bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700/80 rounded-lg text-xs text-slate-700 dark:text-slate-200 placeholder-slate-400 focus:outline-none focus:border-blue-500 focus:bg-white dark:focus:bg-slate-900 transition-all"
              />
            </div>

            <div className="flex-1 overflow-y-auto space-y-1 pr-1">
              {sessionsList
                .filter(s => (s.title || '').toLowerCase().includes(searchQuery.toLowerCase()))
                .map((item) => {
                  const isActive = sessionId === item.id;
                  return (
                    <button
                      key={item.id}
                      onClick={() => handleLoadSession(item.id)}
                      className={`group flex items-center justify-between w-full text-left text-xs px-3 py-2 rounded-lg transition-all cursor-pointer border ${
                        isActive 
                          ? 'bg-blue-50 dark:bg-blue-950/60 text-blue-900 dark:text-blue-200 font-semibold border-blue-200 dark:border-blue-800/80 shadow-xs' 
                          : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800/70 hover:text-slate-900 dark:hover:text-slate-100 border-transparent'
                      }`}
                    >
                      <div className="flex items-center gap-2 overflow-hidden">
                        <Database className={`w-3.5 h-3.5 shrink-0 ${isActive ? 'text-blue-600 dark:text-blue-400' : 'text-slate-400'}`} />
                        <span className="truncate">{item.title || 'Untitled Session'}</span>
                      </div>
                      <Trash2 
                        onClick={(e) => handleDeleteSession(e, item.id)}
                        className="w-3.5 h-3.5 text-slate-400 hover:text-red-500 shrink-0 opacity-0 group-hover:opacity-100 transition-opacity p-0.5" 
                        title="Delete protocol"
                      />
                    </button>
                  );
                })}
              
              {sessionsList.length === 0 && (
                <div className="text-xs text-slate-400 italic text-center py-6">
                  No active protocols.
                </div>
              )}
            </div>
          </div>
        )}

        {/* Clear History Button */}
        {sidebarOpen && (
          <div className="p-3 border-t border-slate-100 dark:border-slate-800">
            <button
              onClick={clearChat}
              className="flex items-center gap-2 w-full text-xs font-medium text-slate-500 hover:text-red-600 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-950/30 px-3 py-2 rounded-lg transition-colors cursor-pointer"
            >
              <Trash2 className="w-3.5 h-3.5 shrink-0" />
              <span>Clear History</span>
            </button>
          </div>
        )}

        {/* Collapse Drawer Toggle */}
        <button
          onClick={() => setSidebarOpen(!sidebarOpen)}
          className="absolute -right-3 top-1/2 -translate-y-1/2 w-6 h-6 bg-white dark:bg-slate-800 hover:bg-slate-50 dark:hover:bg-slate-700 border border-slate-300 dark:border-slate-700 shadow-sm rounded-full flex items-center justify-center transition-all z-30 cursor-pointer"
          title={sidebarOpen ? "Collapse Sidebar" : "Expand Sidebar"}
        >
          {sidebarOpen
            ? <ChevronLeft className="w-3 h-3 text-slate-500 dark:text-slate-300" />
            : <ChevronRight className="w-3 h-3 text-slate-500 dark:text-slate-300" />}
        </button>
      </aside>

      {/* Resize Handle */}
      {sidebarOpen && (
        <div
          onMouseDown={startSidebarResize}
          className="w-1.5 hover:w-2 bg-transparent hover:bg-blue-600/30 cursor-col-resize self-stretch select-none transition-all z-20"
        />
      )}
    </>
  );
}

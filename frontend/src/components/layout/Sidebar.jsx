import React from 'react';
import { Plus, Database, Trash2, Search, ChevronLeft, ChevronRight, Clock, X, FolderLock } from 'lucide-react';

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
  const formatSessionTime = (isoString) => {
    if (!isoString) return 'Active Protocol';
    try {
      const d = new Date(isoString);
      return d.toLocaleDateString('en-IN', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
    } catch {
      return 'Recent';
    }
  };

  const filteredSessions = sessionsList.filter(s =>
    (s.title || '').toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <>
      {/* Mobile Backdrop Drawer Overlay */}
      {sidebarOpen && (
        <div 
          onClick={() => setSidebarOpen(false)} 
          className="fixed inset-0 bg-slate-950/60 backdrop-blur-xs z-30 md:hidden"
        />
      )}

      <aside
        className={`bg-white dark:bg-slate-900 border-r border-slate-200 dark:border-slate-800/90 flex flex-col shrink-0 relative transition-all duration-200 select-none ${
          sidebarOpen ? 'z-40' : 'z-20'
        } ${
          // On mobile, position as absolute drawer overlay; on desktop, position normally
          'fixed inset-y-0 left-0 md:relative md:inset-auto'
        } ${
          !sidebarOpen && 'hidden md:flex'
        }`}
        style={{ width: sidebarOpen ? `${sidebarWidth}px` : '60px' }}
      >
        {/* + NEW INVESTIGATION Button */}
        <div className="p-3 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between gap-2">
          <button
            type="button"
            onClick={() => {
              clearChat();
              if (window.innerWidth < 768) setSidebarOpen(false);
            }}
            className={`flex items-center gap-2 w-full text-xs font-black text-white bg-blue-900 hover:bg-blue-800 dark:bg-blue-800 dark:hover:bg-blue-700 shadow-xs py-2.5 px-3 rounded-xl transition-colors cursor-pointer ${
              !sidebarOpen ? 'justify-center px-0' : ''
            }`}
            title="Start New Investigation Session"
            aria-label="New Investigation"
          >
            <Plus className="w-4 h-4 shrink-0 stroke-[3]" />
            {sidebarOpen && <span className="uppercase tracking-wider font-mono">NEW INVESTIGATION</span>}
          </button>

          {/* Mobile Close Drawer Button */}
          {sidebarOpen && (
            <button
              type="button"
              onClick={() => setSidebarOpen(false)}
              className="p-1.5 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 md:hidden rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800"
              aria-label="Close sidebar"
            >
              <X className="w-4 h-4" />
            </button>
          )}
        </div>

        {/* Sessions Stream */}
        {sidebarOpen && (
          <div className="flex-1 flex flex-col overflow-hidden px-3 py-3">
            <div className="flex items-center justify-between px-1 mb-2 shrink-0">
              <span className="text-[10px] font-mono font-bold text-slate-400 dark:text-slate-500 uppercase tracking-widest">
                RECENT SESSIONS ({filteredSessions.length})
              </span>
            </div>
            
            {/* Session Search Input */}
            <div className="mb-3 relative shrink-0">
              <Search className="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-1/2 -translate-y-1/2" />
              <input 
                type="text"
                placeholder="Search sessions..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-8 pr-7 py-1.5 bg-slate-50 dark:bg-slate-800/70 border border-slate-200 dark:border-slate-700/80 rounded-lg text-xs text-slate-800 dark:text-slate-200 placeholder-slate-400 focus:outline-none focus:border-blue-500 dark:focus:border-cyan-500 transition-colors font-medium"
              />
              {searchQuery && (
                <button
                  type="button"
                  onClick={() => setSearchQuery('')}
                  className="absolute right-2 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"
                >
                  <X className="w-3 h-3" />
                </button>
              )}
            </div>

            {/* Session Cards List */}
            <div className="flex-1 overflow-y-auto space-y-1.5 pr-0.5">
              {filteredSessions.map((item) => {
                const isActive = sessionId === item.id;
                return (
                  <div
                    key={item.id}
                    onClick={() => {
                      handleLoadSession(item.id);
                      if (window.innerWidth < 768) setSidebarOpen(false);
                    }}
                    className={`group relative flex flex-col p-2.5 rounded-xl transition-all cursor-pointer border ${
                      isActive 
                        ? 'bg-blue-50/90 dark:bg-slate-800 text-blue-900 dark:text-slate-100 font-semibold border-blue-400 dark:border-cyan-500/80 shadow-xs' 
                        : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800/60 hover:text-slate-900 dark:hover:text-slate-200 border-transparent'
                    }`}
                  >
                    <div className="flex items-center justify-between gap-1.5 overflow-hidden">
                      <div className="flex items-center gap-2 overflow-hidden">
                        <Database className={`w-3.5 h-3.5 shrink-0 ${isActive ? 'text-blue-600 dark:text-cyan-400' : 'text-slate-400'}`} />
                        <span className="truncate text-xs font-semibold leading-tight">
                          {item.title || 'Untitled Investigation'}
                        </span>
                      </div>

                      <button
                        type="button"
                        onClick={(e) => handleDeleteSession(e, item.id)}
                        className="opacity-0 group-hover:opacity-100 p-1 text-slate-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-slate-700 rounded transition-all shrink-0" 
                        title="Delete session"
                        aria-label="Delete session"
                      >
                        <Trash2 className="w-3 h-3" />
                      </button>
                    </div>

                    <div className="flex items-center justify-between mt-1 text-[10px] text-slate-400 dark:text-slate-500 font-mono">
                      <div className="flex items-center gap-1">
                        <Clock className="w-2.5 h-2.5" />
                        <span>{formatSessionTime(item.updated_at)}</span>
                      </div>
                      {isActive && (
                        <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-pulse"></span>
                      )}
                    </div>
                  </div>
                );
              })}
              
              {filteredSessions.length === 0 && (
                <div className="text-xs text-slate-400 dark:text-slate-500 italic text-center py-8">
                  No sessions found.
                </div>
              )}
            </div>
          </div>
        )}

        {/* Clear History Button */}
        {sidebarOpen && (
          <div className="p-3 border-t border-slate-100 dark:border-slate-800/80">
            <button
              type="button"
              onClick={clearChat}
              className="flex items-center justify-center gap-2 w-full text-xs font-bold text-slate-500 hover:text-red-600 dark:text-slate-400 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-950/30 px-3 py-2 rounded-lg transition-colors cursor-pointer"
              aria-label="Clear all session history"
            >
              <Trash2 className="w-3.5 h-3.5 shrink-0" />
              <span>Clear History</span>
            </button>
          </div>
        )}

        {/* Desktop Collapse Drawer Toggle Button */}
        <button
          type="button"
          onClick={() => setSidebarOpen(!sidebarOpen)}
          className="hidden md:flex absolute -right-3 top-1/2 -translate-y-1/2 w-6 h-6 bg-white dark:bg-slate-800 hover:bg-slate-50 dark:hover:bg-slate-700 border border-slate-300 dark:border-slate-700 shadow-sm rounded-full items-center justify-center transition-colors z-30 cursor-pointer"
          title={sidebarOpen ? "Collapse Sidebar" : "Expand Sidebar"}
          aria-label="Collapse or expand sidebar"
        >
          {sidebarOpen
            ? <ChevronLeft className="w-3 h-3 text-slate-500 dark:text-slate-300" />
            : <ChevronRight className="w-3 h-3 text-slate-500 dark:text-slate-300" />}
        </button>
      </aside>

      {/* Desktop Resize Handle */}
      {sidebarOpen && (
        <div
          onMouseDown={startSidebarResize}
          className="hidden md:block w-1 hover:w-1.5 bg-transparent hover:bg-cyan-500/40 cursor-col-resize self-stretch select-none transition-colors z-20"
        />
      )}
    </>
  );
}

import React from 'react';
import { Plus, Database, Trash2, Search, ChevronLeft, ChevronRight, Clock, ShieldCheck } from 'lucide-react';

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
    if (!isoString) return 'Active Session';
    try {
      const d = new Date(isoString);
      return d.toLocaleDateString('en-IN', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
    } catch {
      return 'Recent';
    }
  };

  return (
    <>
      <aside
        className="bg-white dark:bg-slate-900 border-r border-slate-200 dark:border-slate-800/90 flex flex-col shrink-0 relative z-20 transition-colors duration-300 select-none"
        style={{ width: sidebarOpen ? `${sidebarWidth}px` : '64px' }}
      >
        {/* New Investigation Action */}
        <div className="p-3 border-b border-slate-100 dark:border-slate-800">
          <button
            onClick={clearChat}
            className={`flex items-center gap-2.5 w-full text-xs font-black text-white bg-blue-900 hover:bg-blue-800 dark:bg-blue-800 dark:hover:bg-blue-700 shadow-sm py-2.5 px-3.5 rounded-xl transition-all cursor-pointer ${
              !sidebarOpen ? 'justify-center px-0' : ''
            }`}
            title="Start New Investigation Session"
          >
            <Plus className="w-4 h-4 shrink-0 stroke-[3]" />
            {sidebarOpen && <span className="uppercase tracking-wider">New Investigation</span>}
          </button>
        </div>

        {/* Sessions List */}
        {sidebarOpen && (
          <div className="flex-1 flex flex-col overflow-hidden px-3 py-3">
            <div className="flex items-center justify-between px-1 mb-2 shrink-0">
              <span className="text-[10px] font-mono font-bold text-slate-400 dark:text-slate-500 uppercase tracking-widest">
                Recent Sessions ({sessionsList.length})
              </span>
            </div>
            
            {/* Protocol Search Box */}
            <div className="mb-3 relative shrink-0">
              <Search className="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-1/2 -translate-y-1/2" />
              <input 
                type="text"
                placeholder="Filter sessions..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-8 pr-3 py-1.5 bg-slate-50 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700 rounded-lg text-xs text-slate-800 dark:text-slate-200 placeholder-slate-400 focus:outline-none focus:border-blue-500 focus:bg-white dark:focus:bg-slate-900 transition-all font-medium"
              />
            </div>

            <div className="flex-1 overflow-y-auto space-y-1.5 pr-0.5">
              {sessionsList
                .filter(s => (s.title || '').toLowerCase().includes(searchQuery.toLowerCase()))
                .map((item) => {
                  const isActive = sessionId === item.id;
                  return (
                    <div
                      key={item.id}
                      onClick={() => handleLoadSession(item.id)}
                      className={`group relative flex flex-col p-2.5 rounded-xl transition-all cursor-pointer border ${
                        isActive 
                          ? 'bg-blue-50/80 dark:bg-slate-800 text-blue-900 dark:text-blue-200 font-semibold border-blue-300 dark:border-blue-600 shadow-xs' 
                          : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100/80 dark:hover:bg-slate-800/60 hover:text-slate-900 dark:hover:text-slate-100 border-transparent'
                      }`}
                    >
                      <div className="flex items-center justify-between gap-1 overflow-hidden">
                        <div className="flex items-center gap-2 overflow-hidden">
                          <Database className={`w-3.5 h-3.5 shrink-0 ${isActive ? 'text-blue-600 dark:text-blue-400' : 'text-slate-400'}`} />
                          <span className="truncate text-xs font-semibold leading-snug">
                            {item.title || 'Untitled Session'}
                          </span>
                        </div>
                        <button
                          type="button"
                          onClick={(e) => handleDeleteSession(e, item.id)}
                          className="opacity-0 group-hover:opacity-100 p-1 text-slate-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-slate-700 rounded transition-all shrink-0" 
                          title="Delete protocol"
                        >
                          <Trash2 className="w-3 h-3" />
                        </button>
                      </div>

                      {item.updated_at && (
                        <div className="flex items-center gap-1 mt-1 text-[10px] text-slate-400 dark:text-slate-500 font-mono">
                          <Clock className="w-2.5 h-2.5" />
                          <span>{formatSessionTime(item.updated_at)}</span>
                        </div>
                      )}
                    </div>
                  );
                })}
              
              {sessionsList.length === 0 && (
                <div className="text-xs text-slate-400 dark:text-slate-500 italic text-center py-8">
                  No previous sessions found.
                </div>
              )}
            </div>
          </div>
        )}

        {/* Clear History Button */}
        {sidebarOpen && (
          <div className="p-3 border-t border-slate-100 dark:border-slate-800/80">
            <button
              onClick={clearChat}
              className="flex items-center justify-center gap-2 w-full text-xs font-bold text-slate-500 hover:text-red-600 dark:text-slate-400 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-950/30 px-3 py-2 rounded-lg transition-colors cursor-pointer"
            >
              <Trash2 className="w-3.5 h-3.5 shrink-0" />
              <span>Clear History</span>
            </button>
          </div>
        )}

        {/* Collapse Drawer Toggle Button */}
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

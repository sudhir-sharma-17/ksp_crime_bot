import { useState, useRef, useEffect } from 'react';
import Header from './layout/Header';
import Footer from './layout/Footer';
import Sidebar from './layout/Sidebar';
import ChatStream from './chat/ChatStream';
import DataCanvas from './canvas/DataCanvas';
import { GripVertical } from 'lucide-react';

const DEFAULT_WELCOME = [
  {
    sender: 'ai',
    text: `## Welcome to Aloka Intelligence

### State Police Intelligence Assistant
* **Direct Database Access:** 500 active FIR cases, accused records, victim profiles, investigating officers, legal sections, and police units.
* **Capabilities:** Multi-table relational queries, time-series crime trends, status distributions, semantic search over brief facts, and instant translations (English, Kannada, Hindi).

Ask any criminological inquiry, case lookup, or analytical question to begin.`
  }
];

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = SpeechRecognition ? new SpeechRecognition() : null;

// Calculate optimal default conversation width (63% of available space)
const getDefaultChatWidth = (sidebarW = 250) => {
  if (typeof window !== 'undefined') {
    const available = window.innerWidth - sidebarW;
    return Math.max(620, Math.round(available * 0.63));
  }
  return 850;
};

export default function Dashboard() {
  const [messages, setMessages] = useState(DEFAULT_WELCOME);
  const [inputVal, setInputVal] = useState('');
  const [activeDataIndex, setActiveDataIndex] = useState(null);
  const [sessionId, setSessionId] = useState(() => crypto.randomUUID());
  const [sessionsList, setSessionsList] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [isDarkMode, setIsDarkMode] = useState(true);
  const [cachedSql, setCachedSql] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [queryQueue, setQueryQueue] = useState([]);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [currentTime, setCurrentTime] = useState(new Date());
  const [isListening, setIsListening] = useState(false);
  const [activeTab, setActiveTab] = useState('chat'); // 'chat' | 'canvas' for mobile/tablet responsive views
  const [selectedLanguage, setSelectedLanguage] = useState('en');
  const [isCanvasMaximized, setIsCanvasMaximized] = useState(false);

  // Layout Dimensions (Exact Initial Layout)
  const [sidebarWidth, setSidebarWidth] = useState(250);
  const [chatWidth, setChatWidth] = useState(() => getDefaultChatWidth(250));
  const [isDraggingChatActive, setIsDraggingChatActive] = useState(false);
  const isDraggingSidebar = useRef(false);
  const isDraggingChat = useRef(false);

  const isProcessingRef = useRef(false);
  const abortControllerRef = useRef(null);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // ── Dark Mode Class Sync ──────────────────────────────────────────────────
  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [isDarkMode]);

  // ── Window Resize Listener to adapt default layout if uncustomized ────────
  useEffect(() => {
    const handleWindowResize = () => {
      if (!isDraggingChat.current && !isCanvasMaximized) {
        const offsetLeft = sidebarOpen ? sidebarWidth : 60;
        const maxChatWidth = Math.max(300, window.innerWidth - offsetLeft - 300);
        setChatWidth(prev => Math.min(prev, maxChatWidth));
      }
    };
    window.addEventListener('resize', handleWindowResize);
    return () => window.removeEventListener('resize', handleWindowResize);
  }, [sidebarOpen, sidebarWidth, isCanvasMaximized]);

  // ── Resize Handlers ────────────────────────────────────────────────────────
  const startSidebarResize = (e) => {
    e.preventDefault();
    isDraggingSidebar.current = true;
    document.body.style.cursor = 'col-resize';
    document.addEventListener('mousemove', onSidebarMouseMove);
    document.addEventListener('mouseup', onSidebarMouseUp);
  };

  const onSidebarMouseMove = (e) => {
    if (!isDraggingSidebar.current) return;
    const newWidth = Math.max(180, Math.min(e.clientX, 450));
    setSidebarWidth(newWidth);
  };

  const onSidebarMouseUp = () => {
    isDraggingSidebar.current = false;
    document.body.style.cursor = '';
    document.removeEventListener('mousemove', onSidebarMouseMove);
    document.removeEventListener('mouseup', onSidebarMouseUp);
  };

  const startChatResize = (e) => {
    e.preventDefault();
    isDraggingChat.current = true;
    setIsDraggingChatActive(true);
    document.body.style.cursor = 'col-resize';
    document.addEventListener('mousemove', onChatMouseMove);
    document.addEventListener('mouseup', onChatMouseUp);
  };

  const onChatMouseMove = (e) => {
    if (!isDraggingChat.current) return;
    const offsetLeft = sidebarOpen ? sidebarWidth : 60;
    const maxChatWidth = Math.max(300, window.innerWidth - offsetLeft - 300);
    const newWidth = Math.max(260, Math.min(e.clientX - offsetLeft, maxChatWidth));
    setChatWidth(newWidth);
  };

  const onChatMouseUp = () => {
    isDraggingChat.current = false;
    setIsDraggingChatActive(false);
    document.body.style.cursor = '';
    document.removeEventListener('mousemove', onChatMouseMove);
    document.removeEventListener('mouseup', onChatMouseUp);
  };

  // ── Data Center Quick Size Presets ─────────────────────────────────────────
  const handleSetPreset = (mode) => {
    const currentSidebar = sidebarOpen ? sidebarWidth : 60;
    const availableWidth = window.innerWidth - currentSidebar;

    if (mode === 'default') {
      // Restore the exact default 63% / 37% layout
      setChatWidth(getDefaultChatWidth(currentSidebar));
      setIsCanvasMaximized(false);
    } else if (mode === 'balanced') {
      // 50% Chat / 50% Data Center
      setChatWidth(Math.round(availableWidth * 0.5));
      setIsCanvasMaximized(false);
    } else if (mode === 'expanded') {
      // 30% Chat / 70% Data Center
      setChatWidth(Math.max(280, Math.round(availableWidth * 0.3)));
      setIsCanvasMaximized(false);
    } else if (mode === 'max') {
      // 18% Chat / 82% Data Center
      setChatWidth(Math.max(260, Math.round(availableWidth * 0.18)));
      setIsCanvasMaximized(false);
    }
  };

  // ── Speech Recognition ────────────────────────────────────────────────────
  const toggleVoiceCommand = () => {
    if (!recognition) {
      alert("Voice recognition is not supported in this browser.");
      return;
    }
    if (isListening) {
      recognition.stop();
      setIsListening(false);
    } else {
      setIsListening(true);
      recognition.start();
      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setInputVal((prev) => (prev ? `${prev} ${transcript}` : transcript));
        recognition.stop();
        setIsListening(false);
      };
      recognition.onerror = () => {
        setIsListening(false);
      };
    }
  };

  // ── Session Sync (Called only when new query/message occurs) ─────────────
  const saveSession = async (currSessionId, currMessages) => {
    if (!currSessionId || !currMessages || currMessages.length <= 1) return;
    try {
      const title = currMessages.find(m => m.sender === 'user')?.text || 'New Protocol';
      await fetch(`/api/sessions/${currSessionId}`, {
        headers: { 'X-KSP-Auth-Token': 'ksp-secure-demo-123', 'Content-Type': 'application/json' },
        method: 'POST',
        body: JSON.stringify({ title, messages: currMessages })
      });
      fetchSessions();
    } catch (err) {
      console.error("Session sync failed:", err);
    }
  };

  const fetchSessions = async () => {
    try {
      const res = await fetch(`/api/sessions`, { headers: { 'X-KSP-Auth-Token': 'ksp-secure-demo-123' } });
      if (res.ok) {
        const data = await res.json();
        setSessionsList(data);
      }
    } catch (err) {
      console.error("Failed to fetch sessions:", err);
    }
  };

  useEffect(() => {
    fetchSessions();
  }, []);

  // ── Global Keyboard Auto-Focus & Auto Scroll ─────────────────────────────
  useEffect(() => {
    const handleGlobalKeyDown = (e) => {
      // Ignore modifier keys, tab, escape, function keys
      if (e.ctrlKey || e.metaKey || e.altKey || e.key === 'Tab' || e.key === 'Escape') {
        return;
      }

      const activeTag = document.activeElement?.tagName?.toLowerCase();
      const isInputActive = activeTag === 'input' || activeTag === 'textarea' || activeTag === 'select';

      // If user is not currently typing in another input (like session search), focus main composer
      if (!isInputActive && inputRef.current) {
        inputRef.current.focus();
      }
    };

    window.addEventListener('keydown', handleGlobalKeyDown);
    return () => window.removeEventListener('keydown', handleGlobalKeyDown);
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    // Always keep focus on the composer search bar
    inputRef.current?.focus();
  }, [messages, isLoading]);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  // ── Protocol / Session Actions ────────────────────────────────────────────
  const clearChat = () => {
    setMessages(DEFAULT_WELCOME);
    setActiveDataIndex(null);
    setSessionId(crypto.randomUUID());
    setInputVal('');
    setQueryQueue([]);
    setActiveTab('chat');
  };

  const handleLoadSession = async (id) => {
    try {
      const res = await fetch(`/api/sessions/${id}`, { headers: { 'X-KSP-Auth-Token': 'ksp-secure-demo-123' } });
      if (res.ok) {
        const data = await res.json();
        setMessages(data.messages || DEFAULT_WELCOME);
        setSessionId(id);
        setActiveDataIndex(null);
        setActiveTab('chat');
      }
    } catch (err) {
      console.error("Failed to load session:", err);
    }
  };

  const handleDeleteSession = async (e, id) => {
    e.stopPropagation();
    try {
      await fetch(`/api/sessions/${id}`, { method: 'DELETE', headers: { 'X-KSP-Auth-Token': 'ksp-secure-demo-123' } });
      if (sessionId === id) {
        clearChat();
      }
      fetchSessions();
    } catch (err) {
      console.error("Failed to delete session:", err);
    }
  };

  // ── Query Execution Engine ────────────────────────────────────────────────
  const cancelQuery = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;
    }
    setQueryQueue([]);
    isProcessingRef.current = false;
    setIsLoading(false);
    setMessages((prev) => [
      ...prev,
      {
        sender: 'system',
        text: '⚠️ **Query Terminated**\n\nThe query execution and all queued requests were canceled by the investigator.'
      }
    ]);
  };

  const executeQuery = async (queryText) => {
    if (!queryText || !queryText.trim()) return;
    
    const query = queryText.trim();
    isProcessingRef.current = true;
    setIsLoading(true);

    const controller = new AbortController();
    abortControllerRef.current = controller;
    setCachedSql(null);

    let currentHistory = [];
    setMessages((prev) => {
      const updated = [...prev, { sender: 'user', text: query }];
      currentHistory = updated.slice(-6).map(m => ({
        role: m.sender === 'user' ? "user" : "assistant",
        content: m.user_query || m.text || m.response
      }));
      return updated;
    });

    try {
      const response = await fetch(`/query`, {
        headers: { 'X-KSP-Auth-Token': 'ksp-secure-demo-123', 'Content-Type': 'application/json' },
        method: 'POST',
        signal: controller.signal,
        body: JSON.stringify({ 
          query,
          chat_history: currentHistory.slice(0, -1),
          session_id: sessionId
        }),
      });
      if (!response.ok) throw new Error(`API Error: ${response.status}`);
      const data = await response.json();
      
      if (data.generated_sql) {
        setCachedSql(data.generated_sql);
      }

      setMessages((prev) => {
        const newMsg = {
          sender: 'ai',
          text: data.response,
          generated_sql: data.generated_sql,
          sql_results: data.sql_results,
          all_generated_sql: data.all_generated_sql,
          all_sql_results: data.all_sql_results,
          all_pagination: data.all_pagination || [],
          chart_metadata: data.chart_metadata,
          visualization: data.visualization || data.chart_metadata,
        };
        setActiveDataIndex(prev.length);
        const updated = [...prev, newMsg];
        saveSession(sessionId, updated);
        return updated;
      });
    } catch (err) {
      if (err.name === 'AbortError') {
        return;
      }
      console.error(err);
      setMessages((prev) => [
        ...prev,
        {
          sender: 'system',
          text: '⚠️ **ANALYSIS INTERRUPTED**\n\nAloka could not complete this request. Unable to reach the database service.',
        },
      ]);
    } finally {
      abortControllerRef.current = null;
      isProcessingRef.current = false;
      setIsLoading(false);
      inputRef.current?.focus();
    }
  };

  // ── FIFO Queue Consumer ───────────────────────────────────────────────────
  useEffect(() => {
    if (!isLoading && !isProcessingRef.current && queryQueue.length > 0) {
      const nextQuery = queryQueue[0];
      setQueryQueue((prev) => prev.slice(1));
      executeQuery(nextQuery);
    }
  }, [isLoading, queryQueue]);

  const handleSendMessage = (e) => {
    e?.preventDefault();
    const query = inputVal.trim();
    if (!query) return;
    
    setInputVal('');
    setTimeout(() => {
      inputRef.current?.focus();
    }, 10);

    if (isLoading || isProcessingRef.current) {
      setQueryQueue((prev) => [...prev, query]);
    } else {
      executeQuery(query);
    }
  };

  // ── Translation Action ────────────────────────────────────────────────────
  const handleTranslate = async (e, text, index) => {
    const targetLang = e.target.value;
    if (!targetLang || !text) return;

    try {
      const res = await fetch(`/api/translate`, {
        method: 'POST',
        headers: { 'X-KSP-Auth-Token': 'ksp-secure-demo-123', 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, target_language: targetLang })
      });
      if (res.ok) {
        const data = await res.json();
        setMessages((prev) => {
          const updated = [...prev];
          updated[index] = { ...updated[index], text: data.translated_text };
          saveSession(sessionId, updated);
          return updated;
        });
      }
    } catch (err) {
      console.error("Translation failed:", err);
    }
  };

  // ── Pagination Load More ──────────────────────────────────────────────────
  const handleLoadMore = async (queryIdx) => {
    if (activeDataIndex === null) return;
    const msg = messages[activeDataIndex];
    const sql = cachedSql || msg.all_generated_sql[queryIdx];
    const offset = msg.all_pagination[queryIdx]?.next_offset ?? 0;
    
    try {
      const response = await fetch(`/query`, {
        headers: { 'X-KSP-Auth-Token': 'ksp-secure-demo-123', 'Content-Type': 'application/json' },
        method: 'POST',
        body: JSON.stringify({ 
          is_pagination: true, 
          sql: sql, 
          offset: offset 
        }),
      });
      if (!response.ok) throw new Error(`API Error: ${response.status}`);
      const data = await response.json();
      
      const hasMoreData = data.has_more || data.hasMore || false;
      
      setMessages(prev => {
        const newMsgs = [...prev];
        const newMsg = { ...newMsgs[activeDataIndex] };
        
        newMsg.all_sql_results = [...newMsg.all_sql_results];
        newMsg.all_pagination = [...newMsg.all_pagination];
        
        newMsg.all_sql_results[queryIdx] = [
          ...newMsg.all_sql_results[queryIdx],
          ...data.data
        ];
        
        newMsg.all_pagination[queryIdx] = {
          has_more: hasMoreData,
          total: data.total,
          remaining_count: Math.max(0, data.total - (offset + 15)),
          next_offset: offset + 15
        };
        
        if (queryIdx === 0) {
          newMsg.sql_results = newMsg.all_sql_results[0];
        }
        
        newMsgs[activeDataIndex] = newMsg;
        return newMsgs;
      });
    } catch (err) {
      console.error("Load more failed:", err);
    }
  };

  const activeMessageWithData = activeDataIndex !== null ? messages[activeDataIndex] : null;
  const hasDataOnCanvas = Boolean(activeMessageWithData && activeMessageWithData.all_sql_results && activeMessageWithData.all_sql_results.length > 0);

  return (
    <div className="h-screen flex flex-col bg-slate-100 dark:bg-slate-900 text-slate-900 dark:text-slate-100 font-sans overflow-hidden transition-colors duration-200 select-none">
      <Header 
        isDarkMode={isDarkMode} 
        setIsDarkMode={setIsDarkMode} 
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        hasDataOnCanvas={hasDataOnCanvas}
        selectedLanguage={selectedLanguage}
        setSelectedLanguage={setSelectedLanguage}
        sidebarOpen={sidebarOpen}
        setSidebarOpen={setSidebarOpen}
      />

      <div className="flex flex-1 overflow-hidden relative">
        {/* Sidebar (Hidden in Fullscreen Canvas mode) */}
        {!isCanvasMaximized && (
          <Sidebar
            sidebarOpen={sidebarOpen}
            setSidebarOpen={setSidebarOpen}
            sidebarWidth={sidebarWidth}
            startSidebarResize={startSidebarResize}
            sessionsList={sessionsList}
            sessionId={sessionId}
            searchQuery={searchQuery}
            setSearchQuery={setSearchQuery}
            clearChat={clearChat}
            handleLoadSession={handleLoadSession}
            handleDeleteSession={handleDeleteSession}
          />
        )}

        {/* Conversation Stream (hidden on mobile if canvas tab is selected, or when canvas is maximized) */}
        {!isCanvasMaximized && (
          <div className={`${activeTab === 'canvas' ? 'hidden md:flex' : 'flex'} flex-col h-full shrink-0 relative`}>
            <ChatStream
              chatWidth={chatWidth}
              messages={messages}
              activeDataIndex={activeDataIndex}
              setActiveDataIndex={setActiveDataIndex}
              handleTranslate={handleTranslate}
              isLoading={isLoading}
              cancelQuery={cancelQuery}
              queryQueue={queryQueue}
              setQueryQueue={setQueryQueue}
              inputVal={inputVal}
              setInputVal={setInputVal}
              handleSendMessage={handleSendMessage}
              isListening={isListening}
              toggleVoiceCommand={toggleVoiceCommand}
              messagesEndRef={messagesEndRef}
              inputRef={inputRef}
            />
          </div>
        )}

        {/* ── DRAGGABLE DIVIDER RESIZE HANDLE ─────────────────────────────── */}
        {!isCanvasMaximized && (
          <div
            onMouseDown={startChatResize}
            className={`hidden md:flex w-2 hover:w-2.5 bg-slate-200 dark:bg-slate-800 hover:bg-cyan-500 dark:hover:bg-cyan-500 cursor-col-resize self-stretch items-center justify-center transition-all z-20 group relative ${
              isDraggingChatActive ? 'bg-cyan-500 dark:bg-cyan-500 w-2.5' : ''
            }`}
            title="Drag to resize Data Center & Conversation"
          >
            <GripVertical className="w-3.5 h-3.5 text-slate-400 group-hover:text-white dark:group-hover:text-slate-900 transition-colors pointer-events-none" />
          </div>
        )}

        {/* Data Center / Data Canvas */}
        <div className={`${activeTab === 'chat' && !isCanvasMaximized ? 'hidden md:flex' : 'flex'} flex-1 h-full overflow-hidden`}>
          <DataCanvas
            activeMessageWithData={activeMessageWithData}
            activeDataIndex={activeDataIndex}
            handleLoadMore={handleLoadMore}
            onSetPreset={handleSetPreset}
            isCanvasMaximized={isCanvasMaximized}
            setIsCanvasMaximized={setIsCanvasMaximized}
          />
        </div>
      </div>

      <Footer currentTime={currentTime} />
    </div>
  );
}

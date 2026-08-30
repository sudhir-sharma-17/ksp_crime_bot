import { useState, useRef, useEffect } from 'react';
import Header from './layout/Header';
import Footer from './layout/Footer';
import Sidebar from './layout/Sidebar';
import ChatStream from './chat/ChatStream';
import DataCanvas from './canvas/DataCanvas';

const DEFAULT_WELCOME = [
  {
    sender: 'ai',
    text: `## Welcome to Aloka Intelligence

### State Police Investigative AI Assistant
* **Database Access:** 500 active FIR cases, accused records, victim profiles, investigating officers, legal sections, and police units.
* **Capabilities:** Multi-table relational queries, time-series crime trends, status distributions, semantic search over brief facts, and instant translations (English, Kannada, Hindi).

Ask any criminological inquiry, case lookup, or analytical question to begin.`
  }
];

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = SpeechRecognition ? new SpeechRecognition() : null;

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

  // Layout Dimensions (Resizable)
  const [sidebarWidth, setSidebarWidth] = useState(250);
  const [chatWidth, setChatWidth] = useState(480);
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

  // ── Resize Handlers ────────────────────────────────────────────────────────
  const startSidebarResize = (e) => {
    e.preventDefault();
    isDraggingSidebar.current = true;
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
    document.removeEventListener('mousemove', onSidebarMouseMove);
    document.removeEventListener('mouseup', onSidebarMouseUp);
  };

  const startChatResize = (e) => {
    e.preventDefault();
    isDraggingChat.current = true;
    document.addEventListener('mousemove', onChatMouseMove);
    document.addEventListener('mouseup', onChatMouseUp);
  };

  const onChatMouseMove = (e) => {
    if (!isDraggingChat.current) return;
    const offsetLeft = sidebarOpen ? sidebarWidth : 64;
    const newWidth = Math.max(340, Math.min(e.clientX - offsetLeft, 800));
    setChatWidth(newWidth);
  };

  const onChatMouseUp = () => {
    isDraggingChat.current = false;
    document.removeEventListener('mousemove', onChatMouseMove);
    document.removeEventListener('mouseup', onChatMouseUp);
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

  // ── Session Sync with Backend ─────────────────────────────────────────────
  useEffect(() => {
    if (messages.length > 1 && sessionId) {
      const title = messages.find(m => m.sender === 'user')?.text || 'New Protocol';
      fetch(`/api/sessions/${sessionId}`, {
        headers: { 'X-KSP-Auth-Token': 'ksp-secure-demo-123', 'Content-Type': 'application/json' },
        method: 'POST',
        body: JSON.stringify({ title, messages })
      })
      .then(() => fetchSessions())
      .catch(err => console.error("Session sync failed:", err));
    }
  }, [messages, sessionId]);

  const fetchSessions = async () => {
    try {
      const res = await fetch(`/api/sessions`, { headers: { 'X-KSP-Auth-Token': 'ksp-secure-demo-123' } });
      if (res.ok) {
        const data = await res.json();
        setSessionsList(data);
      }
    } catch (err) {
      console.error("Failed to fetch protocols:", err);
    }
  };

  useEffect(() => {
    fetchSessions();
  }, []);

  // ── Live Clock & Auto Scroll ──────────────────────────────────────────────
  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  useEffect(() => {
    if (!isLoading) {
      inputRef.current?.focus();
    }
  }, [isLoading]);

  // ── Protocol / Session Actions ────────────────────────────────────────────
  const clearChat = () => {
    setMessages(DEFAULT_WELCOME);
    setActiveDataIndex(null);
    setSessionId(crypto.randomUUID());
    setInputVal('');
    setQueryQueue([]);
  };

  const handleLoadSession = async (id) => {
    try {
      const res = await fetch(`/api/sessions/${id}`, { headers: { 'X-KSP-Auth-Token': 'ksp-secure-demo-123' } });
      if (res.ok) {
        const data = await res.json();
        setMessages(data.messages || DEFAULT_WELCOME);
        setSessionId(id);
        setActiveDataIndex(null);
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
        return [...prev, newMsg];
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
          text: '⚠️ **Connection Error**\n\nUnable to reach the backend database service.',
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

  return (
    <div className="h-screen flex flex-col bg-slate-100 dark:bg-slate-900 text-slate-900 dark:text-slate-100 font-sans overflow-hidden transition-colors duration-300">
      <Header isDarkMode={isDarkMode} setIsDarkMode={setIsDarkMode} />

      <div className="flex flex-1 overflow-hidden">
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

        <ChatStream
          chatWidth={chatWidth}
          startChatResize={startChatResize}
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

        <DataCanvas
          activeMessageWithData={activeMessageWithData}
          activeDataIndex={activeDataIndex}
          handleLoadMore={handleLoadMore}
        />
      </div>

      <Footer currentTime={currentTime} />
    </div>
  );
}

import { useState, useRef, useEffect } from 'react';
import { Plus, MessageSquare, ArrowUp, ChevronLeft, ChevronRight, Sparkles, Trash2, Database, Search, Copy, Check, Globe, Loader2 } from 'lucide-react';
import { PieChart, Pie, Cell, Tooltip as RechartsTooltip, Tooltip, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Legend } from 'recharts';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { jsPDF } from "jspdf";
import autoTable from 'jspdf-autotable';

const headerLogoSrc = 'https://en.wikipedia.org/wiki/Special:FilePath/Seal_of_Karnataka.svg';

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = SpeechRecognition ? new SpeechRecognition() : null;


// ─── Markdown Renderer — Light/Dark Theme (Table elements removed for left pane) ──
const mdComponents = {
  h1: ({ children }) => (
    <h1 className="text-xl font-bold text-gray-900 dark:text-slate-100 mb-3 block border-b border-gray-200 dark:border-slate-800 pb-1">{children}</h1>
  ),
  h2: ({ children }) => (
    <h2 className="text-lg font-semibold text-blue-900 dark:text-blue-400 mt-3 mb-2 block">{children}</h2>
  ),
  h3: ({ children }) => (
    <h3 className="text-base font-medium text-gray-800 dark:text-slate-200 mt-2 mb-1 block">{children}</h3>
  ),
  p: ({ children }) => (
    <p className="text-sm text-gray-700 dark:text-slate-300 mb-3 leading-relaxed block">{children}</p>
  ),
  strong: ({ children }) => (
    <strong className="font-semibold text-gray-900 dark:text-slate-100">{children}</strong>
  ),
  em: ({ children }) => (
    <em className="italic text-blue-800 dark:text-blue-400">{children}</em>
  ),
  ul: ({ children }) => (
    <ul className="list-disc pl-5 space-y-1 mb-3 text-gray-700 dark:text-slate-300 text-sm">{children}</ul>
  ),
  ol: ({ children }) => (
    <ol className="list-decimal pl-5 space-y-1 mb-3 text-gray-700 dark:text-slate-300 text-sm">{children}</ol>
  ),
  li: ({ children }) => (
    <li className="marker:text-blue-600 dark:marker:text-blue-400 leading-relaxed">{children}</li>
  ),
  code: ({ inline, children }) =>
    inline ? (
      <code className="font-mono text-blue-800 dark:text-blue-300 bg-blue-50 dark:bg-blue-950/40 px-1 py-0.5 rounded text-xs border border-blue-100 dark:border-blue-900/30">{children}</code>
    ) : (
      <pre className="font-mono text-gray-800 dark:text-slate-200 bg-gray-50 dark:bg-slate-900/40 p-3 rounded overflow-x-auto text-xs border border-gray-200 dark:border-slate-800 my-2 leading-relaxed shadow-inner">
        <code>{children}</code>
      </pre>
    ),
  blockquote: ({ children }) => (
    <blockquote className="border-l-4 border-blue-500 pl-3 text-gray-600 dark:text-slate-400 italic my-2 text-sm">{children}</blockquote>
  ),
  // Completely strip out markdown tables from rendering in the chat pane
  table: () => null,
  thead: () => null,
  th: () => null,
  td: () => null,
  tr: () => null,
};


// ─── Typing Indicator ─────────────────────────────────────────────────────────
function TypingBubble() {
  return (
     <div className="flex items-center gap-3 p-3 mt-2 mb-4 mx-4 bg-blue-50/50 rounded-lg border border-blue-100 w-fit">
       <div className="relative flex h-5 w-5">
         <img src={headerLogoSrc} alt="Processing" className="w-5 h-5 object-contain absolute opacity-70 animate-ping" />
         <img src={headerLogoSrc} alt="Processing" className="w-5 h-5 object-contain relative" />
       </div>
       <span className="text-xs font-bold text-blue-900 tracking-widest animate-pulse">
         FETCHING SECURE DATA...
       </span>
     </div>
  );
}

// ─── Main Component ───────────────────────────────────────────────────────────

// ─── Smart Cell Rendering ─────────────────────────────────────────────────────
const renderCell = (key, value) => {
  if (value === null || value === undefined) return '-';
  const strVal = String(value);
  const lowerKey = key.toLowerCase();

  // Gender Highlighting
  if (lowerKey.includes('gender')) {
    if (strVal === '1') {
      return <span className="px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">1</span>;
    } else if (strVal === '2') {
      return <span className="px-2.5 py-0.5 rounded-full text-xs font-medium bg-fuchsia-100 text-fuchsia-800">2</span>;
    }
    return <span className="px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">{strVal}</span>;
  }

  // Age Highlighting
  if (lowerKey.includes('age')) {
    return <span className="bg-gray-100 text-gray-700 px-2 py-1 rounded text-xs font-semibold">{strVal}</span>;
  }

  // Case Number Highlighting
  if (lowerKey.includes('case')) {
    return <span className="font-mono text-xs text-blue-900 dark:text-white">{strVal}</span>;
  }

  return strVal;
};

export default function Dashboard() {
  // Action Bar states
  const [copiedMessageIndex, setCopiedMessageIndex] = useState(null);
  const [activeDataIndex, setActiveDataIndex] = useState(null);
  const [translatingMessageIndex, setTranslatingMessageIndex] = useState(null);

  const handleCopy = (text, index) => {
    navigator.clipboard.writeText(text);
    setCopiedMessageIndex(index);
    setTimeout(() => setCopiedMessageIndex(null), 2000);
  };

  const handleTranslate = async (e, text, msgIndex) => {
    const targetLang = e.target.value;
    if (!targetLang) return;
    
    setTranslatingMessageIndex(msgIndex);
    try {
      const res = await fetch('http://localhost:9000/api/translate', {
        headers: { 'X-KSP-Auth-Token': 'ksp-secure-demo-123', 'Content-Type': 'application/json' },
        method: 'POST',
        body: JSON.stringify({ text, target_language: targetLang })
      });
      if (res.ok) {
        const data = await res.json();
        setMessages(prev => {
          const newMessages = [...prev];
          newMessages[msgIndex] = { ...newMessages[msgIndex], text: data.translated_text };
          return newMessages;
        });
      }
    } catch (err) {
      console.error("Translation failed:", err);
    } finally {
      setTranslatingMessageIndex(null);
    }
  };

  const DEFAULT_WELCOME = [{ 
    id: 1, 
    sender: 'ai', 
    text: 'Welcome to the Command Center. I am Aloka, your State Intelligence AI. How can I assist you with the database today?',
    isWelcome: true 
  }];
  
  const [messages, setMessages] = useState(DEFAULT_WELCOME);
  const [sessionsList, setSessionsList] = useState([]);
  const [sessionId, setSessionId] = useState(() => crypto.randomUUID());
  const [searchQuery, setSearchQuery] = useState('');
  const [inputVal, setInputVal] = useState('');
  const [offset, setOffset] = useState(0);
  const [hasMore, setHasMore] = useState(false);
  const [cachedSql, setCachedSql] = useState(null);
  const abortControllerRef = useRef(null);

  const [isListening, setIsListening] = useState(false);

  const [sidebarWidth, setSidebarWidth] = useState(240);
  const [chatWidth, setChatWidth] = useState(380);

  const [isDarkMode, setIsDarkMode] = useState(false);

  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [isDarkMode]);

  const startSidebarResize = (e) => {
    e.preventDefault();
    const startX = e.clientX;
    const startWidth = sidebarWidth;

    const doDrag = (moveEvent) => {
      const newWidth = startWidth + (moveEvent.clientX - startX);
      if (newWidth > 160 && newWidth < 400) {
        setSidebarWidth(newWidth);
      }
    };

    const stopDrag = () => {
      document.removeEventListener('mousemove', doDrag);
      document.removeEventListener('mouseup', stopDrag);
    };

    document.addEventListener('mousemove', doDrag);
    document.addEventListener('mouseup', stopDrag);
  };

  const startChatResize = (e) => {
    e.preventDefault();
    const startX = e.clientX;
    const startWidth = chatWidth;

    const doDrag = (moveEvent) => {
      const newWidth = startWidth + (moveEvent.clientX - startX);
      if (newWidth > 280 && newWidth < 800) {
        setChatWidth(newWidth);
      }
    };

    const stopDrag = () => {
      document.removeEventListener('mousemove', doDrag);
      document.removeEventListener('mouseup', stopDrag);
    };

    document.addEventListener('mousemove', doDrag);
    document.addEventListener('mouseup', stopDrag);
  };

  const toggleVoiceCommand = () => {
    if (!recognition) {
      alert("Your browser does not support the Web Speech API. Please use Google Chrome or Edge.");
      return;
    }
    
    if (isListening) {
      recognition.stop();
      setIsListening(false);
    } else {
      recognition.start();
      setIsListening(true);
      
      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setInputVal((prev) => prev + (prev ? " " : "") + transcript);
      };
      
      recognition.onspeechend = () => {
        recognition.stop();
        setIsListening(false);
      };
      
      recognition.onerror = (event) => {
        console.error("Speech recognition error", event.error);
        setIsListening(false);
      };
    }
  };

  const [isLoading, setIsLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [currentTime, setCurrentTime] = useState(new Date());

  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // ── Session Sync to Backend ────────────────────────────────────────────────
  useEffect(() => {
    if (messages.length > 1 && sessionId) {
      const title = messages.find(m => m.sender === 'user')?.text || 'New Session';
      fetch(`http://localhost:9000/api/sessions/${sessionId}`, {
        headers: { 'X-KSP-Auth-Token': 'ksp-secure-demo-123', 'Content-Type': 'application/json' },
        method: 'POST',
        body: JSON.stringify({ title, messages })
      })
      .then(() => fetchSessions()) // Refresh sidebar
      .catch(err => console.error("Sync failed:", err));
    }
  }, [messages, sessionId]);
  
  // ── Fetch Sessions List on Mount ───────────────────────────────────────────
  const fetchSessions = async () => {
    try {
      const res = await fetch('http://localhost:9000/api/sessions', { headers: { 'X-KSP-Auth-Token': 'ksp-secure-demo-123' } });
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


  // ── Auto scroll ───────────────────────────────────────────────────────────────
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  // ── Live clock ────────────────────────────────────────────────────────────────
  useEffect(() => {
    const t = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(t);
  }, []);

  const formatTime = (d) =>
    d.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false }) + ' IST';
  const formatDate = (d) =>
    d.toLocaleDateString('en-IN', { day: 'numeric', month: 'long', year: 'numeric' });

  // ── Session Actions ──────────────────────────────────────────────────────────
  const clearChat = () => {
    setMessages([]);
    setActiveDataIndex(null);
    setSessionId(crypto.randomUUID());
    setInputVal('');
  };

  const handleLoadSession = async (id) => {
    try {
      const res = await fetch(`http://localhost:9000/api/sessions/${id}`, { headers: { 'X-KSP-Auth-Token': 'ksp-secure-demo-123' } });
      if (res.ok) {
        const data = await res.json();
        setMessages(data.messages || DEFAULT_WELCOME);
        setSessionId(id);
      }
    } catch (err) {
      console.error("Failed to load session:", err);
    }
  };

  const handleDeleteSession = async (e, id) => {
    e.stopPropagation();
    try {
      await fetch(`http://localhost:9000/api/sessions/${id}`, { method: 'DELETE', headers: { 'X-KSP-Auth-Token': 'ksp-secure-demo-123' } });
      if (sessionId === id) {
        clearChat();
      }
      fetchSessions();
    } catch (err) {
      console.error("Failed to delete session:", err);
    }
  };


  // ── Send message ──────────────────────────────────────────────────────────────
  const exportToPDF = () => {
    if (!activeMessageWithData || !activeMessageWithData.all_sql_results || activeMessageWithData.all_sql_results.length === 0) return;
    
    const doc = new jsPDF('landscape');
    
    // Branding
    doc.setFontSize(14);
    doc.setFont("helvetica", "bold");
    doc.text("ALOKA - KSP OFFICIAL INTELLIGENCE REPORT", 14, 15);
    
    doc.setFontSize(10);
    doc.setFont("helvetica", "normal");
    doc.setTextColor(100, 100, 100);
    doc.text("Generated on: " + new Date().toLocaleString(), 14, 22);
    
    doc.setTextColor(220, 38, 38);
    doc.setFont("helvetica", "bold");
    doc.text("CONFIDENTIAL - FOR OFFICIAL USE ONLY", 14, 28);
    
    // Table
    const data = activeMessageWithData.all_sql_results[0];
    if (data && data.length > 0) {
      const columns = Object.keys(data[0]);
      const rows = data.map(row => columns.map(col => String(row[col])));
      
      autoTable(doc, {
        startY: 35,
        head: [columns],
        body: rows,
        theme: 'grid',
        headStyles: { fillColor: [30, 58, 138] },
        styles: { fontSize: 8, cellPadding: 2, overflow: 'linebreak' },
        columnStyles: { text: { cellWidth: 'auto' } }
      });
    }
    
    doc.save('KSP_Intelligence_Report.pdf');
  };

  const cancelQuery = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;
    }
    setIsLoading(false);
    setMessages((prev) => [
      ...prev,
      {
        sender: 'ai',
        text: '⚠️ **Query Terminated**\n\nThe query execution was canceled by the user.'
      }
    ]);
  };

  const handleSendMessage = async (e) => {
    e?.preventDefault();
    const query = inputVal.trim();
    if (!query || isLoading) return;
    
    // Create abort controller for this execution
    const controller = new AbortController();
    abortControllerRef.current = controller;
    
    setCachedSql(null); // Clear cache on new prompt
    setMessages((prev) => [...prev, { sender: 'user', text: query }]);
    setInputVal('');
    setIsLoading(true);

    const recentHistory = messages.slice(-4).map(m => ({
      role: (m.sender === 'user' || m.isUser) ? "user" : "assistant",
      content: m.user_query || m.text || m.response
    }));

    try {
      const response = await fetch('http://localhost:9000/query', {
        headers: { 'X-KSP-Auth-Token': 'ksp-secure-demo-123', 'Content-Type': 'application/json' },
        method: 'POST',
        signal: controller.signal,
        body: JSON.stringify({ 
          query,
          chat_history: recentHistory,
          session_id: sessionId
        }),
      });
      if (!response.ok) throw new Error(`API Error: ${response.status}`);
      const data = await response.json();
      
      // Save the SQL from the response
      if (data.generated_sql) {
        setCachedSql(data.generated_sql);
      }

      const firstPagePagination = data.all_pagination?.[0];
      const hasMoreData = data.has_more || data.hasMore || firstPagePagination?.has_more || firstPagePagination?.hasMore || false;
      setHasMore(hasMoreData);
      setOffset(firstPagePagination?.next_offset || 0);

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
        };
        setActiveDataIndex(prev.length);
        return [...prev, newMsg];
      });
    } catch (err) {
      if (err.name === 'AbortError') {
        console.log("Query fetch was aborted.");
        return;
      }
      console.error(err);
      setMessages((prev) => [
        ...prev,
        {
          sender: 'system',
          text: '⚠️ **Connection Error**\n\nUnable to reach the backend.',
        },
      ]);
    } finally {
      abortControllerRef.current = null;
      setIsLoading(false);
      inputRef.current?.focus();
    }
  };


  const handleLoadMore = async (msgIndex, queryIdx) => {
    const msg = messages[msgIndex];
    const sql = cachedSql || msg.all_generated_sql[queryIdx];
    // Use next_offset from pagination metadata (set correctly by the backend)
    const offset = msg.all_pagination[queryIdx]?.next_offset ?? 0;
    
    try {
      const response = await fetch('http://localhost:9000/query', {
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
      setHasMore(hasMoreData);
      setOffset(offset + 15);
      
      setMessages(prev => {
        const newMsgs = [...prev];
        const newMsg = { ...newMsgs[msgIndex] };
        
        // Deep copy arrays
        newMsg.all_sql_results = [...newMsg.all_sql_results];
        newMsg.all_pagination = [...newMsg.all_pagination];
        
        // APPEND new rows using spread operator from the pagination response data field
        newMsg.all_sql_results[queryIdx] = [
          ...newMsg.all_sql_results[queryIdx],
          ...data.data
        ];
        
        // Update pagination with fresh metadata
        newMsg.all_pagination[queryIdx] = {
          has_more: hasMoreData,
          total: data.total,
          remaining_count: Math.max(0, data.total - (offset + 15)),
          next_offset: offset + 15
        };
        
        // Keep flat sql_results in sync for the first query (legacy fallback)
        if (queryIdx === 0) {
           newMsg.sql_results = newMsg.all_sql_results[0];
        }
        
        newMsgs[msgIndex] = newMsg;
        return newMsgs;
      });
    } catch (err) {
      console.error("Load more failed:", err);
    }
  };

  const hasMessages = messages.length > 0;
  
  const activeMessageWithData = activeDataIndex !== null ? messages[activeDataIndex] : null;
  const message = messages[activeDataIndex];
  const activeData = activeMessageWithData?.all_sql_results?.[0];

  return (
    <div className="h-screen flex flex-col bg-white dark:bg-slate-900 text-gray-900 dark:text-slate-100 font-sans overflow-hidden transition-colors duration-300">
      
      {/* ── TOP NAVBAR / HEADER ─────────────────────────────────────────────── */}
      <header className="h-16 bg-white dark:bg-slate-900 flex items-center px-6 border-b border-gray-200 dark:border-slate-800 shrink-0 shadow-sm z-20 transition-colors duration-300">
        <div className="flex items-center gap-3 px-2">
          {/* Permanent Wikimedia link for the Karnataka State Emblem */}
          <img 
            src="https://upload.wikimedia.org/wikipedia/commons/a/aa/Seal_of_Karnataka.svg" 
            alt="Karnataka State Police Logo" 
            className="w-10 h-10 object-contain drop-shadow-sm"
          />
          <div className="flex flex-col">
            <span className="text-lg font-bold tracking-widest text-slate-700 dark:text-slate-200 uppercase">
              Aloka Intelligence
            </span>
            <span className="text-[10px] font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
              Command Center View
            </span>
          </div>
        </div>

        <button
          onClick={() => setIsDarkMode(!isDarkMode)}
          className="p-2 ml-auto rounded-full bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-amber-400 hover:bg-slate-200 dark:hover:bg-slate-700 transition-all shadow-inner cursor-pointer"
          title="Toggle Night Shift"
        >
          {isDarkMode ? (
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
          ) : (
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path></svg>
          )}
        </button>
      </header>

      <div className="flex flex-1 overflow-hidden">

        {/* ── SIDEBAR ─────────────────────────────────────────────────────────── */}
        <aside
          className="bg-white dark:bg-slate-900 border-r border-gray-200 dark:border-slate-800 flex flex-col shrink-0 relative z-10 transition-colors duration-300"
          style={{ width: sidebarOpen ? `${sidebarWidth}px` : '60px' }}
        >
          {/* New Investigation Button */}
          <div className="px-3 pt-5 pb-3 border-b border-gray-100">
            <button
              onClick={clearChat}
              className={`flex items-center gap-2 w-full text-sm font-medium text-white bg-blue-900 hover:bg-blue-800 shadow-md py-2.5 px-3 rounded transition-colors ${!sidebarOpen ? 'justify-center' : ''}`}
            >
              <Plus className="w-4 h-4 shrink-0" />
              {sidebarOpen && <span>New Session</span>}
            </button>
          </div>

          {/* Chat History */}
          {sidebarOpen && (
            <div className="flex-1 flex flex-col overflow-hidden px-3 py-2 mt-2">
              <div className="text-[10px] font-bold text-gray-400 uppercase tracking-widest px-2 mb-2 shrink-0">
                Recent Protocols
              </div>
              
              {/* Search Box */}
              <div className="mb-3 relative shrink-0">
                <Search className="w-3.5 h-3.5 text-gray-400 absolute left-2.5 top-1/2 -translate-y-1/2" />
                <input 
                  type="text"
                  placeholder="Search protocols..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-8 pr-3 py-1.5 bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded text-xs text-gray-700 dark:text-slate-200 focus:outline-none focus:border-blue-400 focus:bg-white dark:focus:bg-slate-900 transition-colors"
                />
              </div>

              <div className="flex-1 overflow-y-auto">
                {sessionsList
                  .filter(s => s.title.toLowerCase().includes(searchQuery.toLowerCase()))
                  .map((item) => (
                  <button
                    key={item.id}
                    onClick={() => handleLoadSession(item.id)}
                    className={`group flex items-center justify-between w-full text-left text-sm px-3 py-2 rounded transition-colors mb-1 ${
                      sessionId === item.id 
                        ? 'bg-blue-50 dark:bg-blue-950/40 text-blue-900 dark:text-blue-200 font-medium border-l-2 border-blue-600' 
                        : 'text-gray-600 dark:text-slate-400 hover:bg-gray-100 dark:hover:bg-slate-800 hover:text-blue-900 dark:hover:text-blue-300 border-l-2 border-transparent'
                    }`}
                  >
                    <div className="flex items-center gap-2.5 overflow-hidden">
                      <Database className={`w-3.5 h-3.5 shrink-0 ${sessionId === item.id ? 'text-blue-600' : 'text-gray-400'}`} />
                      <span className="truncate">{item.title}</span>
                    </div>
                    <Trash2 
                      onClick={(e) => handleDeleteSession(e, item.id)}
                      className="w-3.5 h-3.5 text-red-400 hover:text-red-600 shrink-0 opacity-0 group-hover:opacity-100 transition-opacity" 
                    />
                  </button>
                ))}
                
                {sessionsList.length === 0 && (
                  <div className="text-xs text-gray-400 italic text-center mt-4">
                    No protocols found.
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Clear History (bottom) */}
          {sidebarOpen && (
            <div className="px-3 pb-4">
              <button
                onClick={clearChat}
                className="flex items-center gap-2 w-full text-xs text-gray-500 hover:text-red-600 hover:bg-red-50 px-3 py-2 rounded transition-colors border border-transparent hover:border-red-100"
              >
                <Trash2 className="w-3.5 h-3.5 shrink-0" />
                <span>Clear History</span>
              </button>
            </div>
          )}

          {/* Collapse Toggle */}
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="absolute -right-3 top-1/2 -translate-y-1/2 w-6 h-6 bg-white hover:bg-gray-50 border border-gray-300 shadow rounded-full flex items-center justify-center transition-colors z-20"
          >
            {sidebarOpen
              ? <ChevronLeft className="w-3 h-3 text-gray-500" />
              : <ChevronRight className="w-3 h-3 text-gray-500" />}
          </button>
        </aside>

        {sidebarOpen && (
          <div
            onMouseDown={startSidebarResize}
            className="w-1.5 hover:w-2 bg-slate-200 hover:bg-blue-600/40 cursor-col-resize self-stretch select-none transition-all z-20"
            style={{ width: '6px' }}
          />
        )}

        <section 
          className="bg-gray-50 dark:bg-slate-950 flex flex-col relative border-r border-gray-300 dark:border-slate-800 shadow-inner shrink-0 transition-colors duration-300"
          style={{ width: `${chatWidth}px` }}
        >
          <div className="flex-1 overflow-y-auto pb-24">
            {messages.map((msg, index) => {
               const isUser = msg.sender === 'user';
               
               if (isUser) {
                 return (
                   <div 
                     key={index} 
                     className="bg-blue-50 dark:bg-blue-950/20 p-4 rounded-xl border border-blue-100/50 dark:border-blue-900/30 shadow-sm mb-4"
                   >
                     <div className="flex items-center gap-2 mb-2">
                       <div className="w-5 h-5 rounded-full bg-blue-900 flex items-center justify-center text-[10px] font-bold text-white">
                         U
                       </div>
                       <span className="text-[10px] font-bold uppercase tracking-wider text-slate-500">
                         User
                       </span>
                     </div>
                     <div className="text-sm text-slate-800 dark:text-slate-200 font-medium">
                       {msg.text || msg.user_query}
                     </div>
                   </div>
                 );
               }

               const isSelected = activeDataIndex === index;
               return (
                 <div 
                   key={index} 
                   onClick={() => {
                     if (msg.all_sql_results && msg.all_sql_results.length > 0) {
                       setActiveDataIndex(index);
                     }
                   }}
                   className={`p-4 rounded-xl border mb-4 transition-all duration-300 cursor-pointer ${
                     isSelected 
                       ? 'bg-blue-50/50 dark:bg-slate-800/80 border-blue-300 dark:border-blue-900 shadow-md ring-1 ring-blue-200/50 dark:ring-blue-950/50' 
                       : 'bg-white dark:bg-slate-900 border-slate-100 dark:border-slate-800 hover:border-blue-200 dark:hover:border-blue-950 shadow-sm hover:shadow-sm'
                   }`}
                 >
                  <div className="flex items-center gap-2 mb-2">
                    <img 
                      src="https://upload.wikimedia.org/wikipedia/commons/a/aa/Seal_of_Karnataka.svg" 
                      alt="Karnataka State Police Avatar" 
                      className="w-5 h-5 object-contain drop-shadow-sm"
                    />
                    <span className="text-[10px] font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">
                      Aloka Intelligence
                    </span>
                  </div>

                  <div className="prose dark:prose-invert prose-sm max-w-none text-slate-700 dark:text-slate-300">
                    <ReactMarkdown remarkPlugins={[remarkGfm]} components={mdComponents}>{msg.text || msg.response}</ReactMarkdown>
                  </div>

                  {/* Action buttons (Copy & Translate) */}
                  <div className="flex items-center gap-3 mt-3 pt-2 border-t border-slate-100">
                    <button 
                      onClick={() => handleCopy(msg.text || msg.response, index)}
                      className="flex items-center gap-1 text-xs text-slate-500 hover:text-blue-600:text-blue-400 transition-colors cursor-pointer" 
                      title="Copy text"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>
                      Copy
                    </button>
                    
                    <div className="flex items-center gap-1 text-xs text-slate-500 hover:text-blue-600:text-blue-400 transition-colors cursor-pointer focus-within:ring-1 focus-within:ring-blue-900 rounded">
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129"></path></svg>
                      <select 
                        defaultValue=""
                        onChange={(e) => {
                          handleTranslate(e, msg.text || msg.response, index);
                          e.target.value = ""; // Reset dropdown after selection
                        }}
                        className="bg-transparent border-none text-xs focus:ring-0 cursor-pointer outline-none w-20 text-slate-500 hover:text-blue-600:text-blue-400"
                      >
                        <option value="" disabled>Translate</option>
                        <option value="English">English</option>
                        <option value="Kannada">Kannada</option>
                        <option value="Hindi">Hindi</option>
                      </select>
                    </div>
                  </div>
                </div>
              );
            })}

             {isLoading && (
               <div className="flex items-center justify-between p-4 mb-4 rounded-lg bg-blue-50/50 border border-blue-100 animate-pulse">
                 <div className="flex items-center gap-3">
                   {/* The Logo / Avatar Element */}
                   <div className="flex-shrink-0 w-8 h-8 rounded-full bg-white flex items-center justify-center shadow-inner overflow-hidden border border-slate-200">
                      <img 
                        src="https://upload.wikimedia.org/wikipedia/commons/a/aa/Seal_of_Karnataka.svg" 
                        alt="Aloka Intelligence Thinking" 
                        className="w-5 h-5 object-contain drop-shadow-sm animate-pulse"
                      />
                   </div>

                   {/* The "Thinking" Text */}
                   <div className="flex flex-col">
                     <span className="text-xs font-bold text-blue-900 uppercase tracking-widest">
                       Aloka Intelligence
                     </span>
                     <span className="text-sm font-medium text-slate-500 flex items-center gap-1">
                       Analyzing database
                       <span className="flex gap-0.5 mt-1">
                         <span className="w-1 h-1 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
                         <span className="w-1 h-1 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
                         <span className="w-1 h-1 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
                       </span>
                     </span>
                   </div>
                 </div>

                 {/* Terminate Button */}
                 <button
                   type="button"
                   onClick={cancelQuery}
                   className="bg-red-600 hover:bg-red-700 text-white text-xs font-bold py-1.5 px-3 rounded shadow transition-all cursor-pointer select-none"
                 >
                   Terminate
                 </button>
               </div>
             )}
             <div ref={messagesEndRef} />
          </div>

          {/* Chat Input */}
          <div className="absolute bottom-0 left-0 right-0 bg-gray-50 dark:bg-slate-950 border-t border-gray-200 dark:border-slate-800 p-4">
            <form
              onSubmit={handleSendMessage}
              className="relative flex items-center bg-white dark:bg-slate-900 border border-gray-300 dark:border-slate-700 shadow-sm rounded focus-within:border-blue-900 dark:focus-within:border-blue-500 focus-within:ring-1 focus-within:ring-blue-900 dark:focus-within:ring-blue-500 transition-all"
            >
              <input
                ref={inputRef}
                type="text"
                value={inputVal}
                onChange={(e) => setInputVal(e.target.value)}
                placeholder="Query database..."
                className={`flex-1 bg-transparent border-none focus:ring-0 text-gray-900 dark:text-slate-100 text-sm placeholder-gray-400 dark:placeholder-slate-500 py-2.5 px-3 ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}`}
                disabled={isLoading}
              />
              <button 
                type="button"
                onClick={toggleVoiceCommand} 
                className={`m-1 p-2 rounded-full transition-all shrink-0 ${isListening ? 'bg-red-500 text-white animate-pulse' : 'bg-gray-100 text-gray-500 hover:bg-gray-200'}`}
                title="Voice Command"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"></path></svg>
              </button>
              <button
                type="submit"
                disabled={isLoading || !inputVal.trim()}
                className="m-1 w-8 h-8 bg-blue-900 hover:bg-blue-800 disabled:bg-gray-300 disabled:text-gray-500 text-white rounded flex items-center justify-center transition-all shrink-0"
              >
                <ArrowUp className="w-4 h-4" />
              </button>
            </form>
          </div>
        </section>

        <div
          onMouseDown={startChatResize}
          className="w-1.5 hover:w-2 bg-slate-200 hover:bg-blue-600/40 cursor-col-resize self-stretch select-none transition-all z-20"
          style={{ width: '6px' }}
        />

        {/* ── RIGHT PANE: DATA CANVAS ────────────────────────────────────── */}
        <section className="flex-1 bg-white dark:bg-slate-900 flex flex-col relative overflow-hidden transition-colors duration-300">
          {/* Header of Canvas */}
          <div className="h-12 bg-gray-100 dark:bg-slate-800 border-b border-gray-200 dark:border-slate-800 flex items-center justify-between px-6 shrink-0 transition-colors duration-300">
            <h2 className="text-sm font-bold text-gray-600 dark:text-slate-300 uppercase tracking-widest flex items-center gap-2">
              <Database className="w-4 h-4" /> Data Canvas {activeDataIndex !== null ? `— Viewing Query #${activeDataIndex}` : ''}
            </h2>
            {activeMessageWithData && activeMessageWithData.all_sql_results && activeMessageWithData.all_sql_results.length > 0 && (
              <button onClick={exportToPDF} className="flex items-center gap-2 bg-blue-900 hover:bg-blue-800 text-white px-3 py-1.5 rounded text-xs font-bold shadow-sm transition-all cursor-pointer">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
                Export Official Report
              </button>
            )}
          </div>

          {/* Canvas Content */}
          <div className="flex-1 flex flex-col gap-6 p-6 overflow-y-auto bg-slate-50 dark:bg-slate-950 transition-colors duration-300">
            {!activeMessageWithData || !activeMessageWithData.all_sql_results || activeMessageWithData.all_sql_results.length === 0 ? (
              <div className="flex h-full items-center justify-center text-slate-600 dark:text-slate-400 font-medium">No database records associated with this query.</div>
            ) : (
              <div className="animate-fade-in flex flex-col gap-6 min-h-full pr-2 pb-10">

                {/* ── CHART CONTAINER (TOP SECTION) ── */}
                <div className="w-full bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 p-5 shadow-sm flex flex-col shrink-0 text-slate-800 dark:text-slate-200 transition-colors duration-300">
                  <h3 className="text-xs font-bold text-slate-500 uppercase tracking-widest">Visual Intelligence Dashboard</h3>
                  <div className="h-64 w-full mt-4">
                    {activeData && activeData.length > 0 ? (
                      <ResponsiveContainer height="100%" width="100%">
                        <BarChart data={activeData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                          <CartesianGrid stroke="#e2e8f0" strokeDasharray="3 3" vertical={false}/>
                          {/* Dynamically grab the first key for X-Axis, and fallback to a default if needed */}
                          <XAxis dataKey={Object.keys(activeData[0])[0] || Object.keys(activeData[0])[1]} fontSize={12} stroke="#64748b" tickLine={false} />
                          <YAxis axisLine={false} fontSize={12} stroke="#64748b" tickLine={false}/>
                          <Tooltip contentStyle={{ backgroundColor: '#fff', border: 'none', borderRadius: '8px', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)' }}/>
                          {/* Dynamically grab a numeric key for the Bar, or just use the last column */}
                          <Bar dataKey={Object.keys(activeData[0])[Object.keys(activeData[0]).length - 1]} fill="#3b82f6" radius={[4, 4, 0, 0]}/>
                        </BarChart>
                      </ResponsiveContainer>
                    ) : (
                      <div className="flex h-full w-full items-center justify-center border-2 border-dashed border-slate-200 rounded-lg">
                        <p className="text-slate-400 text-sm font-medium">No visual data available for this query.</p>
                      </div>
                    )}
                  </div>
                </div>
                {activeMessageWithData.all_sql_results.map((resultSet, idx) => {
                  const sqlCommand = activeMessageWithData.all_generated_sql?.[idx];
                  if (sqlCommand === 'CHITCHAT') return null;

                  return (
                    <div key={idx} className="mb-10 last:mb-0 shrink-0">
                      {/* SQL Code Block */}
                      {sqlCommand && (
                        <div className="mb-4 rounded-xl border border-slate-200 dark:border-slate-850 overflow-hidden shadow-sm bg-white dark:bg-slate-900 transition-colors duration-300">
                          <div className="bg-blue-900 dark:bg-slate-800 px-4 py-2 flex items-center gap-2">
                            <div className="w-2.5 h-2.5 rounded-full bg-green-400 animate-pulse"></div>
                            <span className="text-xs font-mono text-blue-100 dark:text-slate-300 uppercase tracking-wider">Executed SQL Command {activeMessageWithData.all_sql_results.length > 1 ? idx + 1 : ''}</span>
                          </div>
                          <pre className="p-4 overflow-x-auto text-blue-900 dark:text-blue-300 font-mono text-sm bg-blue-50/30 dark:bg-blue-950/20">
                            {sqlCommand}
                          </pre>
                        </div>
                      )}

                      {/* Premium Table Data Grid */}
                      {resultSet && resultSet.length > 0 ? (
                        <>
                          {/* ── TABLE CONTAINER (BOTTOM SECTION) ── */}
                          <div className="w-full bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden flex-shrink-0 transition-colors duration-300">
                            <div className="overflow-x-auto">
                              <table className="w-full text-sm text-left">
                                <thead className="text-xs text-white uppercase bg-blue-900 dark:bg-slate-800 sticky top-0 z-10 shadow">
                                  <tr>
                                    <th scope="col" className="px-6 py-4 whitespace-nowrap border-r border-blue-800 dark:border-slate-700 tracking-wider w-16">
                                      #
                                    </th>
                                    {Object.keys(resultSet[0] || {}).map((key) => (
                                      <th key={key} scope="col" className="px-6 py-4 whitespace-nowrap border-r border-blue-800 dark:border-slate-700 last:border-0 tracking-wider">
                                        {key}
                                      </th>
                                    ))}
                                  </tr>
                                </thead>
                                <tbody className="divide-y divide-slate-200 dark:divide-slate-800">
                                  {resultSet.map((row, index) => (
                                    <tr key={index} className="hover:bg-slate-50 dark:hover:bg-slate-800/50 hover:shadow-sm border-b border-slate-100 dark:border-slate-800 transition-all group relative">
                                      <td className="px-6 py-3 border-r border-slate-200 dark:border-slate-800 text-slate-500 font-mono text-xs whitespace-nowrap group-hover:border-l-4 group-hover:border-blue-600">
                                        {index + 1}
                                      </td>
                                      {Object.entries(row).map(([key, val], i) => (
                                        <td key={i} className="px-6 py-3 border-r border-slate-200 dark:border-slate-800 last:border-0 text-slate-700 dark:text-slate-200 whitespace-nowrap">
                                          {renderCell(key, val)}
                                        </td>
                                      ))}
                                    </tr>
                                  ))}
                                </tbody>
                              </table>
                            </div>
                          </div>
                          
                          {/* Load More Button — only shown when backend confirms has_more/hasMore: true */}
                          {(activeMessageWithData.all_pagination?.[idx]?.has_more === true || activeMessageWithData.all_pagination?.[idx]?.hasMore === true) && (
                            <div className="mt-4 border-t border-gray-200 pt-4">
                              <button 
                                onClick={() => {
                                  const msgIndex = messages.indexOf(activeMessageWithData);
                                  handleLoadMore(msgIndex, idx);
                                }}
                                className="w-full bg-blue-50 text-blue-900 border border-blue-200 py-2.5 rounded-md hover:bg-blue-100 transition-colors font-semibold shadow-sm flex items-center justify-center text-sm"
                              >
                                <Database className="w-4 h-4 mr-2" /> Load Next 15 Records
                              </button>
                            </div>
                          )}
                        </>
                      ) : (
                        <div className="rounded-xl border border-gray-200 shadow-sm bg-gray-50 p-4 text-gray-500 text-sm italic">
                          No records found for this query.
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </section>

      </div>

      {/* ── FOOTER STATUS BAR ─────────────────────────────────────────────────── */}
      <footer className="h-8 bg-blue-950 flex items-center justify-between px-6 z-50 shrink-0">
        <div className="flex items-center gap-4 text-[10px] font-bold text-blue-300 uppercase tracking-widest">
        </div>
        <div className="flex items-center gap-4 text-[10px] text-blue-300/80 font-mono">
          <span>{formatTime(currentTime)}</span>
          <span>{formatDate(currentTime)}</span>
        </div>
      </footer>
    </div>
  );
}

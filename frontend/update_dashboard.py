with open("src/components/Dashboard.jsx", "r") as f:
    content = f.read()

# 1. Add Search lucide icon import
content = content.replace("Trash2, Database } from 'lucide-react';", "Trash2, Database, Search } from 'lucide-react';")

# 2. Remove MOCK_HISTORY
import re
content = re.sub(r'// ─── Mock Chat History.*?];\n', '', content, flags=re.DOTALL)

# 3. Modify States
old_states = """  const [messages, setMessages] = useState(() => {
    try {
      const saved = localStorage.getItem('ksp_chat_history');
      if (saved) return JSON.parse(saved);
    } catch (_) {}
    return [{ 
      id: 1, 
      sender: 'ai', 
      text: 'Welcome to the Command Center. I am Aloka, your State Intelligence AI. How can I assist you with the database today?',
      isWelcome: true 
    }];
  });"""
new_states = """  const DEFAULT_WELCOME = [{ 
    id: 1, 
    sender: 'ai', 
    text: 'Welcome to the Command Center. I am Aloka, your State Intelligence AI. How can I assist you with the database today?',
    isWelcome: true 
  }];
  
  const [messages, setMessages] = useState(DEFAULT_WELCOME);
  const [sessionsList, setSessionsList] = useState([]);
  const [currentSessionId, setCurrentSessionId] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');"""
content = content.replace(old_states, new_states)

# 4. Remove localstorage useEffect
old_localstorage = """  // ── Persist messages to localStorage ─────────────────────────────────────────
  useEffect(() => {
    try {
      localStorage.setItem('ksp_chat_history', JSON.stringify(messages));
    } catch (_) {}
  }, [messages]);"""
new_localstorage = """  // ── Session Sync to Backend ────────────────────────────────────────────────
  useEffect(() => {
    // Only save if it's a real conversation (more than just the welcome message)
    if (messages.length > 1 && currentSessionId) {
      const title = messages.find(m => m.sender === 'user')?.text || 'New Session';
      fetch(`http://localhost:8000/api/sessions/${currentSessionId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, messages })
      })
      .then(() => fetchSessions()) // Refresh sidebar
      .catch(err => console.error("Sync failed:", err));
    }
  }, [messages, currentSessionId]);
  
  // ── Fetch Sessions List on Mount ───────────────────────────────────────────
  const fetchSessions = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/sessions');
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
"""
content = content.replace(old_localstorage, new_localstorage)

# 5. Update clearChat and add session actions
old_clearchat = """  // ── Clear chat ────────────────────────────────────────────────────────────────
  const clearChat = () => {
    localStorage.removeItem('ksp_chat_history');
    setMessages([{ 
      id: 1, 
      sender: 'ai', 
      text: 'Welcome to the Command Center. I am Aloka, your State Intelligence AI. How can I assist you with the database today?',
      isWelcome: true 
    }]);
    setInputVal('');
  };"""
new_clearchat = """  // ── Session Actions ──────────────────────────────────────────────────────────
  const clearChat = () => {
    setMessages(DEFAULT_WELCOME);
    setCurrentSessionId(null);
    setInputVal('');
  };

  const handleLoadSession = async (id) => {
    try {
      const res = await fetch(`http://localhost:8000/api/sessions/${id}`);
      if (res.ok) {
        const data = await res.json();
        setMessages(data.messages || DEFAULT_WELCOME);
        setCurrentSessionId(id);
      }
    } catch (err) {
      console.error("Failed to load session:", err);
    }
  };

  const handleDeleteSession = async (e, id) => {
    e.stopPropagation();
    try {
      await fetch(`http://localhost:8000/api/sessions/${id}`, { method: 'DELETE' });
      if (currentSessionId === id) {
        clearChat();
      }
      fetchSessions();
    } catch (err) {
      console.error("Failed to delete session:", err);
    }
  };
"""
content = content.replace(old_clearchat, new_clearchat)

# 6. Update handleSendMessage to set currentSessionId if null
old_send = """    setMessages((prev) => [...prev, { sender: 'user', text: query }]);
    setInputVal('');
    setIsLoading(true);"""
new_send = """    if (!currentSessionId) {
      setCurrentSessionId(Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15));
    }
    
    setMessages((prev) => [...prev, { sender: 'user', text: query }]);
    setInputVal('');
    setIsLoading(true);"""
content = content.replace(old_send, new_send)

# 7. Update sidebar rendering
old_sidebar_history = """          {/* Chat History */}
          {sidebarOpen && (
            <div className="flex-1 overflow-y-auto px-3 py-2 mt-2">
              <div className="text-[10px] font-bold text-gray-400 uppercase tracking-widest px-2 mb-2">
                Recent Protocols
              </div>
              {MOCK_HISTORY.map((item) => (
                <button
                  key={item.id}
                  className="flex items-center gap-2.5 w-full text-gray-600 hover:bg-gray-100 hover:text-blue-900 px-3 py-2 rounded transition-colors text-left text-sm truncate mb-1"
                >
                  <Database className="w-3.5 h-3.5 shrink-0 text-gray-400" />
                  <span className="truncate">{item.title}</span>
                </button>
              ))}
            </div>
          )}"""

new_sidebar_history = """          {/* Chat History */}
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
                  className="w-full pl-8 pr-3 py-1.5 bg-gray-50 border border-gray-200 rounded text-xs text-gray-700 focus:outline-none focus:border-blue-400 focus:bg-white transition-colors"
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
                      currentSessionId === item.id 
                        ? 'bg-blue-50 text-blue-900 font-medium border-l-2 border-blue-600' 
                        : 'text-gray-600 hover:bg-gray-100 hover:text-blue-900 border-l-2 border-transparent'
                    }`}
                  >
                    <div className="flex items-center gap-2.5 overflow-hidden">
                      <Database className={`w-3.5 h-3.5 shrink-0 ${currentSessionId === item.id ? 'text-blue-600' : 'text-gray-400'}`} />
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
          )}"""
content = content.replace(old_sidebar_history, new_sidebar_history)

with open("src/components/Dashboard.jsx", "w") as f:
    f.write(content)

print("Dashboard.jsx updated for dynamic history.")

import re

with open("frontend/src/components/Dashboard.jsx", "r") as f:
    content = f.read()

# 1. State and Effect
state_effect = """  const [isDarkMode, setIsDarkMode] = useState(false);

  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [isDarkMode]);
"""
if "const [isDarkMode" not in content:
    content = content.replace("const [inputVal, setInputVal] = useState('');", "const [inputVal, setInputVal] = useState('');\n" + state_effect)

# 2. Toggle Switch in Header
old_header = """      <header className="h-16 bg-white flex items-center px-6 border-b border-gray-200 shrink-0 shadow-sm z-20">
        <div className="flex items-center gap-4">
          <img 
            src={headerLogoSrc} 
            alt="Government of Karnataka" 
            className="h-10 w-auto object-contain"
          />
          <div className="flex flex-col">
            <h1 className="text-lg font-black tracking-widest text-blue-900 leading-tight">ALOKA</h1>
            <span className="text-[10px] uppercase font-bold text-gray-500 tracking-widest">State Intelligence Portal</span>
          </div>
        </div>
      </header>"""

new_header = """      <header className="h-16 bg-white dark:bg-slate-900 flex items-center px-6 border-b border-gray-200 dark:border-slate-700 shrink-0 shadow-sm z-20 transition-colors duration-300">
        <div className="flex items-center gap-4">
          <img 
            src={headerLogoSrc} 
            alt="Government of Karnataka" 
            className="h-10 w-auto object-contain"
          />
          <div className="flex flex-col">
            <h1 className="text-lg font-black tracking-widest text-blue-900 dark:text-blue-400 leading-tight">ALOKA</h1>
            <span className="text-[10px] uppercase font-bold text-gray-500 dark:text-slate-400 tracking-widest">State Intelligence Portal</span>
          </div>
        </div>
        
        <button
          onClick={() => setIsDarkMode(!isDarkMode)}
          className="p-2 ml-auto rounded-full bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-amber-400 hover:bg-slate-200 dark:hover:bg-slate-700 transition-all shadow-inner"
          title="Toggle Night Shift"
        >
          {isDarkMode ? (
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
          ) : (
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path></svg>
          )}
        </button>
      </header>"""

content = content.replace(old_header, new_header)

# 3. Main Wrapper
content = content.replace(
    '<div className="h-screen flex flex-col bg-gray-900 text-gray-900 font-sans overflow-hidden">',
    '<div className="h-screen flex flex-col bg-white dark:bg-slate-900 text-gray-900 dark:text-slate-100 font-sans overflow-hidden transition-colors duration-300">'
)

# 4. Left Pane & Main layout body
old_main_body = """      {/* ── MAIN LAYOUT BODY ─────────────────────────────────────────────── */}
      <main className="flex-1 flex overflow-hidden">

        {/* ── LEFT PANE: CHAT INTERFACE ── */}
        <div className="w-full md:w-1/3 flex flex-col border-r border-gray-200 bg-white relative z-10">"""

new_main_body = """      {/* ── MAIN LAYOUT BODY ─────────────────────────────────────────────── */}
      <main className="flex-1 flex overflow-hidden">

        {/* ── LEFT PANE: CHAT INTERFACE ── */}
        <div className="w-full md:w-1/3 flex flex-col border-r border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 relative z-10 transition-colors duration-300">"""
content = content.replace(old_main_body, new_main_body)

# Chat bubble mapping
old_chat_map = """                <div
                  key={idx}
                  onClick={() => { if (!isUser && !isError) setActiveDataIndex(idx); }}
                  className={`w-full border-b border-gray-200 ${!isUser && !isError ? 'cursor-pointer transition-all hover:bg-blue-50/50' : ''} ${
                    isUser ? 'bg-white' : isError ? 'bg-red-50' : isActive ? 'bg-blue-50/30 ring-2 ring-blue-500 shadow-md z-10 relative' : 'bg-transparent'
                  }`}
                >"""

new_chat_map = """                <div
                  key={idx}
                  onClick={() => { if (!isUser && !isError) setActiveDataIndex(idx); }}
                  className={`w-full border-b border-slate-200 dark:border-slate-700 ${!isUser && !isError ? 'cursor-pointer transition-all hover:bg-slate-50 dark:hover:bg-slate-700/50' : ''} ${
                    isUser ? 'bg-blue-50 dark:bg-blue-900/20' : isError ? 'bg-red-50 dark:bg-red-900/20' : isActive ? 'bg-slate-100 dark:bg-slate-700 ring-2 ring-blue-500 shadow-md z-10 relative' : 'bg-white dark:bg-slate-800'
                  }`}
                >"""
content = content.replace(old_chat_map, new_chat_map)

# Right Pane mapping
old_right_pane = """        {/* ── RIGHT PANE: DATA CANVAS ── */}
        <div className="hidden md:flex flex-1 flex-col relative z-0">
          
          {/* Header of Canvas */}
          <div className="h-12 bg-gray-100 border-b border-gray-200 flex items-center justify-between px-6 shrink-0">
            <h2 className="text-sm font-bold text-gray-600 uppercase tracking-widest flex items-center gap-2">
              <Database className="w-4 h-4" /> Data Canvas {activeDataIndex !== null ? `— Viewing Query #${activeDataIndex}` : ''}
            </h2>"""

new_right_pane = """        {/* ── RIGHT PANE: DATA CANVAS ── */}
        <div className="hidden md:flex flex-1 flex-col relative z-0">
          
          {/* Header of Canvas */}
          <div className="h-12 bg-slate-100 dark:bg-slate-800 border-b border-slate-200 dark:border-slate-700 flex items-center justify-between px-6 shrink-0 transition-colors duration-300">
            <h2 className="text-sm font-bold text-slate-600 dark:text-slate-300 uppercase tracking-widest flex items-center gap-2">
              <Database className="w-4 h-4" /> Data Canvas {activeDataIndex !== null ? `— Viewing Query #${activeDataIndex}` : ''}
            </h2>"""
content = content.replace(old_right_pane, new_right_pane)

# Right pane background
content = content.replace('<div className="flex-1 flex flex-col gap-6 p-6 overflow-y-auto bg-gray-50">', '<div className="flex-1 flex flex-col gap-6 p-6 overflow-y-auto bg-slate-50 dark:bg-slate-900 transition-colors duration-300">')

# Chart Background
content = content.replace('<div className="w-full h-80 bg-white rounded-xl border border-slate-200 p-5 shadow-sm flex flex-col shrink-0">', '<div className="w-full h-80 bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 p-5 shadow-sm flex flex-col shrink-0 text-slate-800 dark:text-slate-200 transition-colors duration-300">')

# SQL block background
content = content.replace('<div className="mb-4 rounded-xl border border-gray-200 overflow-hidden shadow-sm bg-white">', '<div className="mb-4 rounded-xl border border-slate-200 dark:border-slate-700 overflow-hidden shadow-sm bg-white dark:bg-slate-800 transition-colors duration-300">')

# Table background
content = content.replace('<div className="w-full bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden flex-shrink-0">', '<div className="w-full bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 shadow-sm overflow-hidden flex-shrink-0 transition-colors duration-300">')
content = content.replace('<thead className="text-xs text-white uppercase bg-blue-900 sticky top-0 z-10 shadow">', '<thead className="text-xs text-white dark:text-slate-200 uppercase bg-blue-900 dark:bg-slate-700 sticky top-0 z-10 shadow">')
content = content.replace('<tbody className="divide-y divide-gray-200">', '<tbody className="divide-y divide-slate-200 dark:divide-slate-700">')
content = content.replace('className="hover:bg-blue-50 hover:shadow-sm border-b border-gray-100 transition-all group relative"', 'className="hover:bg-slate-50 dark:hover:bg-slate-700 hover:shadow-sm border-b border-slate-100 dark:border-slate-700 transition-all group relative"')
content = content.replace('border-gray-200 text-gray-500', 'border-slate-200 dark:border-slate-700 text-slate-500 dark:text-slate-400')
content = content.replace('border-gray-200 last:border-0 text-gray-700', 'border-slate-200 dark:border-slate-700 last:border-0 text-slate-700 dark:text-slate-300')

with open("frontend/src/components/Dashboard.jsx", "w") as f:
    f.write(content)
print("Dark Mode UI logic patched")

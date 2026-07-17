import re

with open("frontend/src/components/Dashboard.jsx", "r") as f:
    content = f.read()

# 1. Add state variable
if "const [activeDataIndex, setActiveDataIndex]" not in content:
    content = content.replace(
        "const [copiedMessageIndex, setCopiedMessageIndex] = useState(null);",
        "const [copiedMessageIndex, setCopiedMessageIndex] = useState(null);\n  const [activeDataIndex, setActiveDataIndex] = useState(null);"
    )

# 2. Update handleSendMessage
old_set_messages = """      setMessages((prev) => [
        ...prev,
        {
          sender: 'ai',
          text: data.response,
          generated_sql: data.generated_sql,
          sql_results: data.sql_results,
          all_generated_sql: data.all_generated_sql,
          all_sql_results: data.all_sql_results,
          all_pagination: data.all_pagination || [],
          chart_metadata: data.chart_metadata,
        },
      ]);"""

new_set_messages = """      setMessages((prev) => {
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
      });"""

content = content.replace(old_set_messages, new_set_messages)

# 3. Update Left Pane click handler
old_message_map = """            {messages.map((msg, idx) => {
              const isUser = msg.sender === 'user';
              const isError = msg.sender === 'system';

              return (
                <div
                  key={idx}
                  className={`w-full border-b border-gray-200 ${
                    isUser ? 'bg-white' : isError ? 'bg-red-50' : 'bg-transparent'
                  }`}
                >"""

new_message_map = """            {messages.map((msg, idx) => {
              const isUser = msg.sender === 'user';
              const isError = msg.sender === 'system';
              const isActive = activeDataIndex === idx;

              return (
                <div
                  key={idx}
                  onClick={() => { if (!isUser && !isError) setActiveDataIndex(idx); }}
                  className={`w-full border-b border-gray-200 ${!isUser && !isError ? 'cursor-pointer transition-all hover:bg-blue-50/50' : ''} ${
                    isUser ? 'bg-white' : isError ? 'bg-red-50' : isActive ? 'bg-blue-50/30 ring-2 ring-blue-500 shadow-md z-10 relative' : 'bg-transparent'
                  }`}
                >"""

content = content.replace(old_message_map, new_message_map)

# 4. Right Pane logic update
old_active_msg = """  // Find the last AI message that contains sql_results to display on the canvas
  const activeMessageWithData = [...messages].reverse().find(m => m.sender === 'ai' && m.all_sql_results && m.all_sql_results.length > 0);"""

new_active_msg = """  const activeMessageWithData = activeDataIndex !== null ? messages[activeDataIndex] : null;"""

content = content.replace(old_active_msg, new_active_msg)

# 5. Right pane header polish & fallback logic
old_header = """          {/* Header of Canvas */}
          <div className="h-12 bg-gray-100 border-b border-gray-200 flex items-center px-6 shrink-0">
            <h2 className="text-sm font-bold text-gray-600 uppercase tracking-widest flex items-center gap-2">
              <Database className="w-4 h-4" /> Data Canvas
            </h2>
          </div>

          {/* Canvas Content */}
          <div className="flex-1 flex flex-col gap-6 p-6 overflow-y-auto bg-gray-50">
            {!activeMessageWithData ? ("""

new_header = """          {/* Header of Canvas */}
          <div className="h-12 bg-gray-100 border-b border-gray-200 flex items-center px-6 shrink-0">
            <h2 className="text-sm font-bold text-gray-600 uppercase tracking-widest flex items-center gap-2">
              <Database className="w-4 h-4" /> Data Canvas {activeDataIndex !== null ? `— Viewing Query #${activeDataIndex}` : ''}
            </h2>
          </div>

          {/* Canvas Content */}
          <div className="flex-1 flex flex-col gap-6 p-6 overflow-y-auto bg-gray-50">
            {!activeMessageWithData || !activeMessageWithData.all_sql_results || activeMessageWithData.all_sql_results.length === 0 ? ("""

content = content.replace(old_header, new_header)


with open("frontend/src/components/Dashboard.jsx", "w") as f:
    f.write(content)

print("Dashboard active state patched")

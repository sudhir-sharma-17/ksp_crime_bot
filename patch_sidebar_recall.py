with open("frontend/src/components/Dashboard.jsx", "r") as f:
    content = f.read()

# 1. Update State Initialization
content = content.replace(
    "const [activeDataIndex, setActiveDataIndex] = useState(null);",
    "const [activeDataIndex, setActiveDataIndex] = useState(0);"
)

# 2. Add currentMessage
old_active_msg = "  const activeMessageWithData = activeDataIndex !== null ? messages[activeDataIndex] : null;"
new_active_msg = """  const activeMessageWithData = messages[activeDataIndex];
  const currentMessage = messages[activeDataIndex];"""

content = content.replace(old_active_msg, new_active_msg)

# 3. Replace Sidebar Message Loop (from messages.map down to the end of map block)
# Let's locate the exact start and end of the loop in content.
# The map starts with: {messages.map((msg, idx) => {
# and ends with: })} before isLoading and ref messagesEndRef.

# Let's do a precise string replacement for the message mapping block.
# We will read from a target block.
# Let's view the target block using python to make sure we replace the right section.

import re

# We will match the entire block from {messages.map((msg, idx) => { to the corresponding closing })}.
# Since we know the exact line numbers (548 to 628), we can do it by replacing the block.

pattern = r'\{messages\.map\(\(msg, idx\) => \{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\}\)\}'
# Let's check if pattern matches.
match = re.search(pattern, content)
if match:
    print("Found messages.map block using regex!")
    
    new_loop_code = """{messages.map((msg, index) => (
              <div
                key={index}
                onClick={() => setActiveDataIndex(index)}
                className={`p-3 mb-2 rounded-lg transition-all duration-200 cursor-pointer border ${
                  activeDataIndex === index
                    ? 'border-blue-500 bg-blue-50/80 dark:bg-slate-800 dark:border-blue-400 shadow-sm ring-1 ring-blue-500/30'
                    : 'border-slate-100 dark:border-slate-700/50 bg-white dark:bg-slate-800 hover:border-slate-300 dark:hover:border-slate-600'
                }`}
              >
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-[10px] font-bold uppercase px-1.5 py-0.5 rounded bg-slate-100 dark:bg-slate-700 text-slate-500 dark:text-slate-400">
                    Query #{index + 1}
                  </span>
                </div>
                <p className="text-sm font-semibold text-slate-700 dark:text-slate-200 line-clamp-2">
                  {msg.user_query || msg.text || "Database Request"}
                </p>
              </div>
            ))}"""
            
    content = content.replace(match.group(0), new_loop_code)
else:
    print("Pattern not found!")

# 4. Automate New Message Auto-Selection inside handleSendMessage
# We have: setActiveDataIndex(prev.length);
# Wait, if we set it inside setMessages state updater, it is:
# setActiveDataIndex(prev.length);
# This works perfectly, because if prev length is e.g. 1, then the new array length will be 2, and the index is 1 (which is prev.length).
# But let's check if the prompt requires a literal `setActiveDataIndex(newMessagesArray.length - 1)` or similar.
# Wait! In the code, setMessages is:
# setMessages((prev) => {
#    ...
#    setActiveDataIndex(prev.length);
#    return [...prev, newMsg];
# })
# This works perfectly.

with open("frontend/src/components/Dashboard.jsx", "w") as f:
    f.write(content)
print("Dashboard.jsx patched successfully for selectable sidebar.")

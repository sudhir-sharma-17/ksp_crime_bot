with open("frontend/src/components/Dashboard.jsx", "r") as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1

for idx, line in enumerate(lines):
    if "messages.map((msg, idx) => {" in line:
        start_idx = idx
    if "messagesEndRef" in line and end_idx == -1:
        # Walk backwards from messagesEndRef to find the closing })} of the map
        for j in range(idx, start_idx, -1):
            if "})" in lines[j] or "})}" in lines[j]:
                end_idx = j + 1
                break
        break

if start_idx != -1 and end_idx != -1:
    print(f"Replacing lines {start_idx} to {end_idx}")
    
    new_loop = """            {messages.map((msg, index) => (
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
            ))}\n"""
            
    lines[start_idx:end_idx] = [new_loop]
    
    with open("frontend/src/components/Dashboard.jsx", "w") as f:
        f.writelines(lines)
    print("Successfully replaced.")
else:
    print(f"Error finding indexes: start={start_idx}, end={end_idx}")

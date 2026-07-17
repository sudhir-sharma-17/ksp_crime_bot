with open("src/components/Dashboard.jsx", "r") as f:
    content = f.read()

# 1. Add handleLoadMore before `const hasMessages = messages.length > 0;`
handle_load_more_func = """
  const handleLoadMore = async (msgIndex, queryIdx) => {
    const msg = messages[msgIndex];
    const sql = msg.all_generated_sql[queryIdx];
    const offset = msg.all_pagination[queryIdx].next_offset;
    
    try {
      const response = await fetch('http://localhost:8000/query_more', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sql, offset }),
      });
      if (!response.ok) throw new Error(`API Error: ${response.status}`);
      const data = await response.json();
      
      setMessages(prev => {
        const newMsgs = [...prev];
        const newMsg = { ...newMsgs[msgIndex] };
        
        // Deep copy arrays
        newMsg.all_sql_results = [...newMsg.all_sql_results];
        newMsg.all_pagination = [...newMsg.all_pagination];
        
        // Append rows
        newMsg.all_sql_results[queryIdx] = [
          ...newMsg.all_sql_results[queryIdx],
          ...data.sql_results
        ];
        
        // Update pagination
        newMsg.all_pagination[queryIdx] = data.pagination;
        
        // Also update the flat sql_results if it's the first query, just for fallback
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

"""
content = content.replace("  const hasMessages = messages.length > 0;", handle_load_more_func + "  const hasMessages = messages.length > 0;")

# 2. Add the button after the table wrapper `</div>\n                        </div>` (around line 408)
# We can just replace the end of the premium table data grid block.
# Let's find:
#                           </div>
#                         </div>
#                       ) : (
old_table_end = """                          </div>
                        </div>
                      ) : ("""

new_table_end = """                          </div>
                        </div>
                        
                        {/* Load More Button */}
                        {activeMessageWithData.all_pagination?.[idx]?.has_more && (
                          <button 
                            onClick={() => {
                              // We need the index of this message in the main array
                              const msgIndex = messages.indexOf(activeMessageWithData);
                              handleLoadMore(msgIndex, idx);
                            }}
                            className="mt-4 w-full bg-blue-50 text-blue-900 border border-blue-200 py-2 rounded-md hover:bg-blue-100 transition-colors font-semibold shadow-sm"
                          >
                            Load Next 15 Records (Remaining: {activeMessageWithData.all_pagination[idx].remaining_count})
                          </button>
                        )}

                      ) : ("""
content = content.replace(old_table_end, new_table_end)

# Also update the `setMessages` in `handleSendMessage` to initialize `all_pagination`
old_set_msgs = """          all_generated_sql: data.all_generated_sql,
          all_sql_results: data.all_sql_results,
        },"""
new_set_msgs = """          all_generated_sql: data.all_generated_sql,
          all_sql_results: data.all_sql_results,
          all_pagination: data.all_pagination || [],
        },"""
content = content.replace(old_set_msgs, new_set_msgs)

with open("src/components/Dashboard.jsx", "w") as f:
    f.write(content)

print("Dashboard.jsx updated for pagination.")

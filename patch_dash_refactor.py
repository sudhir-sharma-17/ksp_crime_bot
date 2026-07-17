import re

with open("frontend/src/components/Dashboard.jsx", "r") as f:
    content = f.read()

# Make sure CHART_COLORS is defined at the top
if "CHART_COLORS" not in content:
    content = content.replace("const headerLogoSrc", "const CHART_COLORS = ['#1e3a8a', '#2563eb', '#3b82f6', '#60a5fa', '#93c5fd', '#bfdbfe'];\nconst headerLogoSrc")

old_chart_block = """                {/* ── CHART CONTAINER (TOP SECTION) ── */}
                {activeMessageWithData.chart_metadata && activeMessageWithData.chart_metadata.type !== 'none' && (
                  <div className="w-full h-80 bg-white rounded-xl border border-slate-200 p-5 shadow-sm flex flex-col shrink-0">
                    <h3 className="text-xs font-bold text-slate-500 mb-4 uppercase tracking-widest">Visual Intelligence Dashboard</h3>
                    <div className="h-full w-full">
                      <ResponsiveContainer width="100%" height="100%">
                        {activeMessageWithData.chart_metadata.type === 'pie' ? (
                          <PieChart>
                            <Pie
                              data={activeMessageWithData.chart_metadata.data}
                              dataKey="value"
                              nameKey="name"
                              cx="50%"
                              cy="50%"
                              outerRadius={100}
                              fill="#1e3a8a"
                              label
                            >
                              {activeMessageWithData.chart_metadata.data?.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={['#1e3a8a', '#3b82f6', '#93c5fd', '#60a5fa', '#bfdbfe'][index % 5]} />
                              ))}
                            </Pie>
                            <RechartsTooltip />
                            <Legend />
                          </PieChart>
                        ) : activeMessageWithData.chart_metadata.type === 'bar' ? (
                          <BarChart data={activeMessageWithData.chart_metadata.data}>
                            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                            <XAxis dataKey="name" tick={{fontSize: 12, fill: '#64748b'}} axisLine={false} tickLine={false} />
                            <YAxis tick={{fontSize: 12, fill: '#64748b'}} axisLine={false} tickLine={false} />
                            <RechartsTooltip cursor={{fill: '#f1f5f9'}} />
                            <Bar dataKey="value" fill="#1e3a8a" radius={[4, 4, 0, 0]} />
                          </BarChart>
                        ) : null}
                      </ResponsiveContainer>
                    </div>
                  </div>
                )}"""

new_chart_block = """                {/* ── CHART CONTAINER (TOP SECTION) ── */}
                {activeMessageWithData.chart_metadata && activeMessageWithData.chart_metadata.type !== 'none' && activeMessageWithData.all_sql_results && activeMessageWithData.all_sql_results[0] && (
                  <div className="w-full h-80 bg-white rounded-xl border border-slate-200 p-5 shadow-sm flex flex-col shrink-0">
                    <h3 className="text-xs font-bold text-slate-500 mb-4 uppercase tracking-widest">
                      Visual Intelligence: {activeMessageWithData.chart_metadata.type} Chart
                    </h3>
                    <div className="h-full w-full">
                      <ResponsiveContainer height="100%" width="100%">
                        {activeMessageWithData.chart_metadata.type === 'pie' ? (
                          <PieChart>
                            <Pie 
                              cx="50%" cy="50%" 
                              data={activeMessageWithData.all_sql_results[0]} 
                              dataKey={activeMessageWithData.chart_metadata.value_column} 
                              nameKey={activeMessageWithData.chart_metadata.label_column} 
                              fill="#1e3a8a" label outerRadius={80}
                            >
                              {activeMessageWithData.all_sql_results[0].map((entry, index) => (
                                <Cell fill={CHART_COLORS[index % CHART_COLORS.length]} key={`cell-${index}`}/>
                              ))}
                            </Pie>
                            <RechartsTooltip/>
                            <Legend />
                          </PieChart>
                        ) : activeMessageWithData.chart_metadata.type === 'bar' ? (
                          <BarChart data={activeMessageWithData.all_sql_results[0]}>
                            <CartesianGrid strokeDasharray="3 3" vertical={false}/>
                            <XAxis dataKey={activeMessageWithData.chart_metadata.label_column} tick={{fontSize: 12}}/>
                            <YAxis tick={{fontSize: 12}}/>
                            <RechartsTooltip cursor={{fill: '#f3f4f6'}}/>
                            <Bar dataKey={activeMessageWithData.chart_metadata.value_column} fill="#2563eb" radius={[4, 4, 0, 0]}/>
                          </BarChart>
                        ) : null}
                      </ResponsiveContainer>
                    </div>
                  </div>
                )}"""

content = content.replace(old_chart_block, new_chart_block)

with open("frontend/src/components/Dashboard.jsx", "w") as f:
    f.write(content)
print("Dashboard chart logic refactored")

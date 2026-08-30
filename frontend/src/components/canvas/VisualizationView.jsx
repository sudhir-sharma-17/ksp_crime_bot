import React from 'react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend
} from 'recharts';
import { BarChart3, PieChart as PieIcon, TrendingUp, Lightbulb } from 'lucide-react';

const CHART_COLORS = [
  '#2563eb', // Blue
  '#06b6d4', // Cyan
  '#10b981', // Emerald
  '#f59e0b', // Amber
  '#8b5cf6', // Purple
  '#ec4899', // Pink
  '#f97316', // Orange
  '#64748b'  // Slate
];

export default function VisualizationView({ visualization, keyInsight }) {
  if (!visualization || visualization.response_type !== 'chart' || visualization.chart_type === 'none' || !visualization.data || visualization.data.length === 0) {
    return null;
  }

  const chartType = visualization.chart_type;
  const chartData = visualization.data;
  const chartTitle = visualization.title || "Visual Crime Analytics";

  // Calculate highest/dominant data point for automated key insight if not provided
  let topInsight = keyInsight;
  if (!topInsight && chartData.length > 0) {
    const sorted = [...chartData].sort((a, b) => (b.value || 0) - (a.value || 0));
    const topItem = sorted[0];
    const total = chartData.reduce((acc, curr) => acc + (curr.value || 0), 0);
    if (topItem && total > 0) {
      const pct = Math.round((topItem.value / total) * 100);
      topInsight = `Top category: **${topItem.label}** with **${topItem.value.toLocaleString()}** cases (${pct}% of analyzed records).`;
    }
  }

  return (
    <div className="w-full bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-5 sm:p-6 shadow-sm flex flex-col shrink-0 text-slate-800 dark:text-slate-200 transition-colors">
      {/* Chart Header */}
      <div className="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3 mb-4">
        <div className="flex items-center gap-2.5">
          {chartType === 'line' ? (
            <TrendingUp className="w-5 h-5 text-cyan-500" />
          ) : chartType === 'pie' ? (
            <PieIcon className="w-5 h-5 text-amber-500" />
          ) : (
            <BarChart3 className="w-5 h-5 text-blue-600 dark:text-cyan-400" />
          )}
          <h3 className="text-sm font-bold text-slate-900 dark:text-slate-100 uppercase tracking-wider font-mono">
            {chartTitle}
          </h3>
        </div>
        <span className="text-[10px] font-bold font-mono uppercase px-2.5 py-0.5 rounded-md bg-blue-50 dark:bg-slate-800 text-blue-700 dark:text-cyan-400 border border-blue-200 dark:border-slate-700">
          {chartType.toUpperCase()} VISUALIZATION
        </span>
      </div>

      {/* Dynamic Recharts Rendering */}
      <div className="h-64 sm:h-72 w-full">
        <ResponsiveContainer width="100%" height="100%">
          {chartType === 'pie' ? (
            <PieChart>
              <Pie
                data={chartData}
                dataKey="value"
                nameKey="label"
                cx="50%"
                cy="50%"
                outerRadius={90}
                innerRadius={50}
                paddingAngle={3}
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
              >
                {chartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={CHART_COLORS[index % CHART_COLORS.length]} />
                ))}
              </Pie>
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#0f172a', 
                  color: '#f8fafc',
                  border: '1px solid #334155', 
                  borderRadius: '10px', 
                  fontSize: '12px',
                  boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.3)' 
                }} 
              />
              <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '12px' }} />
            </PieChart>
          ) : chartType === 'line' ? (
            <LineChart data={chartData} margin={{ top: 10, right: 25, left: -10, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" opacity={0.3} vertical={false} />
              <XAxis dataKey="label" fontSize={11} stroke="#64748b" tickLine={false} />
              <YAxis axisLine={false} fontSize={11} stroke="#64748b" tickLine={false} />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#0f172a', 
                  color: '#f8fafc',
                  border: '1px solid #334155', 
                  borderRadius: '10px', 
                  fontSize: '12px',
                  boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.3)' 
                }} 
              />
              <Line 
                type="monotone" 
                dataKey="value" 
                stroke="#06b6d4" 
                strokeWidth={3} 
                dot={{ r: 4, fill: '#06b6d4' }} 
                activeDot={{ r: 6, fill: '#38bdf8' }} 
              />
            </LineChart>
          ) : (
            <BarChart data={chartData} margin={{ top: 10, right: 25, left: -10, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" opacity={0.3} vertical={false} />
              <XAxis dataKey="label" fontSize={11} stroke="#64748b" tickLine={false} />
              <YAxis axisLine={false} fontSize={11} stroke="#64748b" tickLine={false} />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#0f172a', 
                  color: '#f8fafc',
                  border: '1px solid #334155', 
                  borderRadius: '10px', 
                  fontSize: '12px',
                  boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.3)' 
                }} 
              />
              <Bar dataKey="value" fill="#2563eb" radius={[6, 6, 0, 0]}>
                {chartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={CHART_COLORS[index % CHART_COLORS.length]} />
                ))}
              </Bar>
            </BarChart>
          )}
        </ResponsiveContainer>
      </div>

      {/* Prominent Key Insight Section */}
      {topInsight && (
        <div className="mt-4 pt-3.5 border-t border-slate-100 dark:border-slate-800/80 flex items-start gap-2.5 bg-blue-50/60 dark:bg-slate-800/50 p-3 rounded-xl border border-blue-100 dark:border-slate-700/60">
          <Lightbulb className="w-4 h-4 text-amber-500 shrink-0 mt-0.5" />
          <div className="flex flex-col">
            <span className="text-[10px] font-mono font-bold uppercase tracking-wider text-blue-900 dark:text-cyan-300">
              Key Insight
            </span>
            <p 
              className="text-xs text-slate-700 dark:text-slate-300 leading-relaxed font-medium"
              dangerouslySetInnerHTML={{ 
                __html: topInsight.replace(/\*\*(.*?)\*\*/g, '<strong class="text-slate-900 dark:text-white font-bold">$1</strong>') 
              }}
            />
          </div>
        </div>
      )}
    </div>
  );
}

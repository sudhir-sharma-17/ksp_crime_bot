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
  '#2F5DA8', // Government Blue
  '#4B72B0', // Medium Slate Blue
  '#608BC1', // Soft Blue
  '#D97706', // Amber Accent
  '#059669', // Emerald
  '#6366F1', // Indigo
  '#64748B', // Slate
  '#0284C7'  // Cyan Accent
];

export default function VisualizationView({ visualization, keyInsight }) {
  if (!visualization || visualization.response_type !== 'chart' || visualization.chart_type === 'none' || !visualization.data || visualization.data.length === 0) {
    return null;
  }

  const chartType = visualization.chart_type;
  const chartData = visualization.data;
  const chartTitle = visualization.title || "Visual Crime Analytics";

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
    <div className="w-full bg-white dark:bg-[#141C28] rounded-2xl border border-slate-200 dark:border-[#263142] p-5 sm:p-6 shadow-xs flex flex-col shrink-0 text-slate-800 dark:text-slate-200 transition-colors">
      {/* Chart Header */}
      <div className="flex items-center justify-between border-b border-slate-100 dark:border-[#263142] pb-3 mb-4">
        <div className="flex items-center gap-2.5">
          {chartType === 'line' ? (
            <TrendingUp className="w-5 h-5 text-[#2F5DA8] dark:text-[#93B4E8]" />
          ) : chartType === 'pie' ? (
            <PieIcon className="w-5 h-5 text-amber-500" />
          ) : (
            <BarChart3 className="w-5 h-5 text-[#2F5DA8] dark:text-[#93B4E8]" />
          )}
          <h3 className="text-sm font-bold text-slate-900 dark:text-slate-100 uppercase tracking-wider font-mono">
            {chartTitle}
          </h3>
        </div>
        <span className="text-[10px] font-bold font-mono uppercase px-2.5 py-0.5 rounded bg-slate-100 dark:bg-[#172640] text-[#2F5DA8] dark:text-[#93B4E8] border border-slate-200 dark:border-[#263142]">
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
                  backgroundColor: '#101722', 
                  color: '#F8FAFC',
                  border: '1px solid #263142', 
                  borderRadius: '8px', 
                  fontSize: '12px'
                }} 
              />
              <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '12px' }} />
            </PieChart>
          ) : chartType === 'line' ? (
            <LineChart data={chartData} margin={{ top: 10, right: 25, left: -10, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#263142" opacity={0.5} vertical={false} />
              <XAxis dataKey="label" fontSize={11} stroke="#64748B" tickLine={false} />
              <YAxis axisLine={false} fontSize={11} stroke="#64748B" tickLine={false} />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#101722', 
                  color: '#F8FAFC',
                  border: '1px solid #263142', 
                  borderRadius: '8px', 
                  fontSize: '12px'
                }} 
              />
              <Line 
                type="monotone" 
                dataKey="value" 
                stroke="#2F5DA8" 
                strokeWidth={2.5} 
                dot={{ r: 4, fill: '#2F5DA8' }} 
                activeDot={{ r: 6, fill: '#93B4E8' }} 
              />
            </LineChart>
          ) : (
            <BarChart data={chartData} margin={{ top: 10, right: 25, left: -10, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#263142" opacity={0.5} vertical={false} />
              <XAxis dataKey="label" fontSize={11} stroke="#64748B" tickLine={false} />
              <YAxis axisLine={false} fontSize={11} stroke="#64748B" tickLine={false} />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#101722', 
                  color: '#F8FAFC',
                  border: '1px solid #263142', 
                  borderRadius: '8px', 
                  fontSize: '12px'
                }} 
              />
              <Bar dataKey="value" fill="#2F5DA8" radius={[4, 4, 0, 0]}>
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
        <div className="mt-4 pt-3.5 border-t border-slate-100 dark:border-[#263142] flex items-start gap-2.5 bg-amber-50/60 dark:bg-[#1A1813] p-3.5 rounded-xl border border-amber-200 dark:border-amber-900/40">
          <Lightbulb className="w-4 h-4 text-amber-500 shrink-0 mt-0.5" />
          <div className="flex flex-col">
            <span className="text-[10px] font-mono font-bold uppercase tracking-wider text-amber-800 dark:text-amber-400">
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

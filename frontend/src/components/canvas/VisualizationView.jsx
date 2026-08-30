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
import { BarChart3, PieChart as PieIcon, TrendingUp } from 'lucide-react';

const CHART_COLORS = [
  '#2563eb', // Blue
  '#059669', // Emerald
  '#d97706', // Amber
  '#dc2626', // Red
  '#7c3aed', // Purple
  '#0891b2', // Cyan
  '#db2777', // Pink
  '#ea580c'  // Orange
];

export default function VisualizationView({ visualization }) {
  if (!visualization || visualization.response_type !== 'chart' || visualization.chart_type === 'none' || !visualization.data || visualization.data.length === 0) {
    return null;
  }

  const chartType = visualization.chart_type;
  const chartData = visualization.data;
  const chartTitle = visualization.title || "Visual Intelligence Dashboard";

  return (
    <div className="w-full bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 p-5 shadow-xs flex flex-col shrink-0 text-slate-800 dark:text-slate-200 transition-colors">
      <div className="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
        <div className="flex items-center gap-2">
          {chartType === 'line' ? (
            <TrendingUp className="w-4 h-4 text-blue-600 dark:text-blue-400" />
          ) : chartType === 'pie' ? (
            <PieIcon className="w-4 h-4 text-amber-500 dark:text-amber-400" />
          ) : (
            <BarChart3 className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
          )}
          <h3 className="text-xs font-bold text-slate-800 dark:text-slate-200 uppercase tracking-wider">
            {chartTitle}
          </h3>
        </div>
        <span className="text-[10px] font-bold uppercase px-2.5 py-0.5 rounded-full bg-blue-50 dark:bg-blue-950 text-blue-700 dark:text-blue-300 font-mono border border-blue-100 dark:border-blue-900/60">
          {chartType.toUpperCase()} CHART
        </span>
      </div>

      <div className="h-64 w-full mt-4">
        <ResponsiveContainer width="100%" height="100%">
          {chartType === 'pie' ? (
            <PieChart>
              <Pie
                data={chartData}
                dataKey="value"
                nameKey="label"
                cx="50%"
                cy="50%"
                outerRadius={85}
                innerRadius={45}
                paddingAngle={4}
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
                  border: 'none', 
                  borderRadius: '8px', 
                  fontSize: '12px',
                  boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.2)' 
                }} 
              />
              <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
            </PieChart>
          ) : chartType === 'line' ? (
            <LineChart data={chartData} margin={{ top: 10, right: 30, left: -10, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" opacity={0.5} vertical={false} />
              <XAxis dataKey="label" fontSize={11} stroke="#64748b" tickLine={false} />
              <YAxis axisLine={false} fontSize={11} stroke="#64748b" tickLine={false} />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#0f172a', 
                  color: '#f8fafc',
                  border: 'none', 
                  borderRadius: '8px', 
                  fontSize: '12px',
                  boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.2)' 
                }} 
              />
              <Line 
                type="monotone" 
                dataKey="value" 
                stroke="#2563eb" 
                strokeWidth={3} 
                dot={{ r: 4, fill: '#2563eb' }} 
                activeDot={{ r: 6, fill: '#1d4ed8' }} 
              />
            </LineChart>
          ) : (
            <BarChart data={chartData} margin={{ top: 10, right: 30, left: -10, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" opacity={0.5} vertical={false} />
              <XAxis dataKey="label" fontSize={11} stroke="#64748b" tickLine={false} />
              <YAxis axisLine={false} fontSize={11} stroke="#64748b" tickLine={false} />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#0f172a', 
                  color: '#f8fafc',
                  border: 'none', 
                  borderRadius: '8px', 
                  fontSize: '12px',
                  boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.2)' 
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
    </div>
  );
}

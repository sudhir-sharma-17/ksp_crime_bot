import React, { useState } from 'react';
import { Database, ChevronDown, ChevronRight, Table as TableIcon } from 'lucide-react';

const renderCell = (key, value) => {
  if (value === null || value === undefined) return '-';
  const strVal = String(value);
  const lowerKey = key.toLowerCase();

  // Gender Highlighting
  if (lowerKey.includes('gender')) {
    if (strVal === '1') {
      return <span className="px-2 py-0.5 rounded text-[11px] font-bold bg-blue-100 dark:bg-blue-950/80 text-blue-800 dark:text-blue-300 border border-blue-200 dark:border-blue-800/60">1 (Male)</span>;
    } else if (strVal === '2') {
      return <span className="px-2 py-0.5 rounded text-[11px] font-bold bg-pink-100 dark:bg-pink-950/80 text-pink-800 dark:text-pink-300 border border-pink-200 dark:border-pink-800/60">2 (Female)</span>;
    }
  }

  // Case Number Badge
  if (lowerKey === 'caseno' || strVal.startsWith('KSP-CASE-')) {
    return <span className="font-mono font-bold text-blue-700 dark:text-cyan-400 bg-blue-50 dark:bg-slate-800 px-2 py-0.5 rounded border border-blue-200 dark:border-slate-700">{strVal}</span>;
  }

  // Status Badge
  if (lowerKey.includes('status')) {
    return <span className="px-2 py-0.5 rounded-full text-[11px] font-semibold bg-emerald-100 dark:bg-emerald-950/80 text-emerald-800 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800/60">{strVal}</span>;
  }

  return strVal;
};

export default function DataTable({
  resultSet,
  paginationInfo,
  onLoadMore,
  queryIndex,
  totalQueries
}) {
  const [isOpen, setIsOpen] = useState(true);

  if (!resultSet || resultSet.length === 0) {
    return (
      <div className="rounded-xl border border-slate-200 dark:border-slate-800 shadow-xs bg-white dark:bg-slate-900 p-4 text-slate-500 text-xs italic">
        No database records returned for this query.
      </div>
    );
  }

  const columns = Object.keys(resultSet[0] || {});
  const hasMore = paginationInfo?.has_more === true || paginationInfo?.hasMore === true;

  return (
    <div className="w-full bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800/80 shadow-xs overflow-hidden transition-colors mb-4">
      {/* Table Section Header */}
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className="w-full bg-slate-50 hover:bg-slate-100 dark:bg-slate-900 dark:hover:bg-slate-850 px-4 py-2.5 flex items-center justify-between cursor-pointer border-b border-slate-200 dark:border-slate-800 transition-colors"
      >
        <div className="flex items-center gap-2">
          {isOpen ? <ChevronDown className="w-3.5 h-3.5 text-slate-400" /> : <ChevronRight className="w-3.5 h-3.5 text-slate-400" />}
          <TableIcon className="w-3.5 h-3.5 text-blue-600 dark:text-blue-400" />
          <span className="text-[11px] font-mono font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider">
            Structured Case Records {totalQueries > 1 ? `#${queryIndex + 1}` : ''} ({resultSet.length} Rows)
          </span>
        </div>

        <span className="text-[10px] font-mono text-slate-400 dark:text-slate-500 uppercase">
          {isOpen ? 'Collapse Table' : 'Expand Table'}
        </span>
      </button>

      {isOpen && (
        <div className="p-4 flex flex-col gap-3">
          <div className="overflow-x-auto max-h-[460px] rounded-lg border border-slate-200 dark:border-slate-800">
            <table className="w-full text-xs text-left border-collapse">
              <thead className="text-[11px] text-white uppercase bg-slate-900 dark:bg-slate-800 sticky top-0 z-10 shadow-xs font-mono">
                <tr>
                  <th scope="col" className="px-4 py-3 whitespace-nowrap border-r border-slate-700 dark:border-slate-700 tracking-wider w-12 text-center font-bold">
                    #
                  </th>
                  {columns.map((key) => (
                    <th key={key} scope="col" className="px-4 py-3 whitespace-nowrap border-r border-slate-700 dark:border-slate-700 last:border-0 tracking-wider font-semibold">
                      {key}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200 dark:divide-slate-800">
                {resultSet.map((row, index) => (
                  <tr key={index} className="hover:bg-blue-50/40 dark:hover:bg-slate-800/60 transition-colors">
                    <td className="px-4 py-2.5 border-r border-slate-200 dark:border-slate-800 text-slate-400 font-mono text-[11px] text-center">
                      {index + 1}
                    </td>
                    {columns.map((key, i) => (
                      <td key={i} className="px-4 py-2.5 border-r border-slate-200 dark:border-slate-800 last:border-0 text-slate-700 dark:text-slate-200 whitespace-nowrap">
                        {renderCell(key, row[key])}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Pagination Load More Button */}
          {hasMore && (
            <button 
              onClick={onLoadMore}
              className="w-full bg-blue-50 hover:bg-blue-100 dark:bg-slate-800 dark:hover:bg-slate-750 text-blue-900 dark:text-blue-300 border border-blue-200 dark:border-slate-700 py-2.5 rounded-xl transition-all font-semibold shadow-xs flex items-center justify-center gap-2 text-xs cursor-pointer"
            >
              <Database className="w-3.5 h-3.5" />
              <span>Load Next 15 Records</span>
              <ChevronDown className="w-3.5 h-3.5" />
            </button>
          )}
        </div>
      )}
    </div>
  );
}

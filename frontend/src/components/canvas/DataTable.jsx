import React from 'react';
import { Database, ChevronDown } from 'lucide-react';

const renderCell = (key, value) => {
  if (value === null || value === undefined) return '-';
  const strVal = String(value);
  const lowerKey = key.toLowerCase();

  // Gender Highlighting
  if (lowerKey.includes('gender')) {
    if (strVal === '1') {
      return <span className="px-2 py-0.5 rounded-md text-[11px] font-bold bg-blue-100 dark:bg-blue-950 text-blue-800 dark:text-blue-300">1 (M)</span>;
    } else if (strVal === '2') {
      return <span className="px-2 py-0.5 rounded-md text-[11px] font-bold bg-pink-100 dark:bg-pink-950 text-pink-800 dark:text-pink-300">2 (F)</span>;
    }
  }

  // Case Number Badge
  if (lowerKey === 'caseno' || strVal.startsWith('KSP-CASE-')) {
    return <span className="font-mono font-bold text-blue-700 dark:text-blue-400 bg-blue-50 dark:bg-blue-950/60 px-2 py-0.5 rounded border border-blue-200 dark:border-blue-800/60">{strVal}</span>;
  }

  // Status Badge
  if (lowerKey.includes('status')) {
    return <span className="px-2 py-0.5 rounded-full text-[11px] font-semibold bg-emerald-100 dark:bg-emerald-950 text-emerald-800 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800/60">{strVal}</span>;
  }

  return strVal;
};

export default function DataTable({
  resultSet,
  paginationInfo,
  onLoadMore,
  queryIndex
}) {
  if (!resultSet || resultSet.length === 0) {
    return (
      <div className="rounded-xl border border-slate-200 dark:border-slate-800 shadow-xs bg-slate-50 dark:bg-slate-900/50 p-4 text-slate-500 text-xs italic">
        No records returned for this query.
      </div>
    );
  }

  const columns = Object.keys(resultSet[0] || {});
  const hasMore = paginationInfo?.has_more === true || paginationInfo?.hasMore === true;

  return (
    <div className="flex flex-col gap-3">
      <div className="w-full bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 shadow-xs overflow-hidden transition-colors">
        <div className="overflow-x-auto max-h-[500px]">
          <table className="w-full text-xs text-left border-collapse">
            <thead className="text-[11px] text-white uppercase bg-slate-900 dark:bg-slate-800 sticky top-0 z-10 shadow-xs">
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
                <tr key={index} className="hover:bg-blue-50/40 dark:hover:bg-slate-800/50 transition-colors">
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
      </div>

      {/* Pagination Load More Button */}
      {hasMore && (
        <button 
          onClick={onLoadMore}
          className="w-full bg-blue-50 hover:bg-blue-100 dark:bg-slate-800/80 dark:hover:bg-slate-800 text-blue-900 dark:text-blue-300 border border-blue-200 dark:border-slate-700 py-2.5 rounded-xl transition-all font-semibold shadow-xs flex items-center justify-center gap-2 text-xs cursor-pointer"
        >
          <Database className="w-3.5 h-3.5" />
          <span>Load Next 15 Records</span>
          <ChevronDown className="w-3.5 h-3.5" />
        </button>
      )}
    </div>
  );
}

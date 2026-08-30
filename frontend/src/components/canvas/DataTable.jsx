import React, { useState } from 'react';
import { Database, ChevronDown, ChevronRight, Table as TableIcon, Info } from 'lucide-react';

const renderCell = (key, value) => {
  if (value === null || value === undefined) return '-';
  const strVal = String(value);
  const lowerKey = key.toLowerCase();

  // Gender Highlighting (Restrained)
  if (lowerKey.includes('gender')) {
    if (strVal === '1') {
      return (
        <span className="px-2 py-0.5 rounded text-[11px] font-semibold bg-slate-100 dark:bg-[#172640] text-slate-800 dark:text-[#93B4E8] border border-slate-200 dark:border-[#263142]">
          1 (Male)
        </span>
      );
    } else if (strVal === '2') {
      return (
        <span className="px-2 py-0.5 rounded text-[11px] font-semibold bg-slate-100 dark:bg-[#172640] text-slate-800 dark:text-[#93B4E8] border border-slate-200 dark:border-[#263142]">
          2 (Female)
        </span>
      );
    }
  }

  // Case Number Badge
  if (lowerKey === 'caseno' || strVal.startsWith('KSP-CASE-')) {
    return (
      <span className="font-mono font-bold text-[#2F5DA8] dark:text-[#93B4E8] bg-slate-100 dark:bg-[#101722] px-2 py-0.5 rounded border border-slate-200 dark:border-[#263142]">
        {strVal}
      </span>
    );
  }

  // Status Badge
  if (lowerKey.includes('status')) {
    return (
      <span className="px-2.5 py-0.5 rounded text-[11px] font-semibold bg-emerald-50 dark:bg-[#102619] text-emerald-700 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-900/50">
        {strVal}
      </span>
    );
  }

  return strVal;
};

export default function DataTable({
  resultSet,
  paginationInfo,
  onLoadMore,
  queryIndex,
  totalQueries,
  defaultOpen = true
}) {
  const [isOpen, setIsOpen] = useState(defaultOpen);

  if (!resultSet || resultSet.length === 0) {
    return (
      <div className="w-full rounded-2xl border border-slate-200 dark:border-[#263142] shadow-xs bg-white dark:bg-[#141C28] p-6 flex items-center gap-3 text-slate-500 dark:text-slate-400 text-xs">
        <Info className="w-5 h-5 text-slate-400 shrink-0" />
        <div>
          <span className="font-bold text-slate-700 dark:text-slate-200 block text-xs">No matching records found.</span>
          <span className="text-[11px]">The database returned zero matching records for this specific filter.</span>
        </div>
      </div>
    );
  }

  const columns = Object.keys(resultSet[0] || {});
  const hasMore = paginationInfo?.has_more === true || paginationInfo?.hasMore === true;

  return (
    <div className="w-full bg-white dark:bg-[#141C28] rounded-2xl border border-slate-200 dark:border-[#263142] shadow-xs overflow-hidden transition-colors">
      {/* Collapsible Section Header: View Data */}
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className="w-full bg-slate-50 hover:bg-slate-100 dark:bg-[#101722] dark:hover:bg-[#141C28] px-5 py-3 flex items-center justify-between cursor-pointer border-b border-slate-200 dark:border-[#263142] transition-colors"
      >
        <div className="flex items-center gap-2.5">
          {isOpen ? (
            <ChevronDown className="w-4 h-4 text-slate-400" />
          ) : (
            <ChevronRight className="w-4 h-4 text-slate-400" />
          )}
          <TableIcon className="w-4 h-4 text-[#2F5DA8] dark:text-[#93B4E8]" />
          <span className="text-xs font-mono font-bold text-slate-800 dark:text-slate-200 uppercase tracking-wider">
            View Data {totalQueries > 1 ? `(#${queryIndex + 1})` : ''}
          </span>
          <span className="text-[10px] font-mono font-bold text-slate-500 dark:text-slate-400 bg-slate-200 dark:bg-[#172640] px-2 py-0.5 rounded">
            {resultSet.length} rows
          </span>
        </div>

        <span className="text-[10px] font-mono text-slate-400 dark:text-slate-500 uppercase tracking-wider">
          {isOpen ? 'Collapse Data' : 'Expand Data'}
        </span>
      </button>

      {/* Table Body */}
      {isOpen && (
        <div className="p-4 sm:p-5 flex flex-col gap-3.5">
          <div className="overflow-x-auto max-h-[460px] rounded-xl border border-slate-200 dark:border-[#263142] shadow-xs">
            <table className="w-full text-xs text-left border-collapse">
              <thead className="text-[11px] text-white uppercase bg-slate-900 dark:bg-[#101722] sticky top-0 z-10 font-mono">
                <tr>
                  <th scope="col" className="px-4 py-3 whitespace-nowrap border-r border-slate-700 dark:border-[#263142] tracking-wider w-12 text-center font-bold">
                    #
                  </th>
                  {columns.map((key) => (
                    <th key={key} scope="col" className="px-4 py-3 whitespace-nowrap border-r border-slate-700 dark:border-[#263142] last:border-0 tracking-wider font-semibold">
                      {key}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200 dark:divide-[#263142]">
                {resultSet.map((row, index) => (
                  <tr key={index} className="hover:bg-slate-50 dark:hover:bg-[#172640]/40 transition-colors">
                    <td className="px-4 py-2.5 border-r border-slate-200 dark:border-[#263142] text-slate-400 font-mono text-[11px] text-center">
                      {index + 1}
                    </td>
                    {columns.map((key, i) => (
                      <td key={i} className="px-4 py-2.5 border-r border-slate-200 dark:border-[#263142] last:border-0 text-slate-700 dark:text-slate-200 whitespace-nowrap font-medium">
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
              className="w-full bg-slate-100 hover:bg-slate-200 dark:bg-[#101722] dark:hover:bg-[#172640] text-[#2F5DA8] dark:text-[#93B4E8] border border-slate-200 dark:border-[#263142] py-2.5 rounded-lg transition-all font-semibold flex items-center justify-center gap-2 text-xs cursor-pointer"
            >
              <Database className="w-3.5 h-3.5" />
              <span>Load More Records</span>
            </button>
          )}
        </div>
      )}
    </div>
  );
}

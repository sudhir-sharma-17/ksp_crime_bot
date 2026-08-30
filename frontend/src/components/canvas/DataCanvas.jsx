import React from 'react';
import { Database, FileDown, LineChart, Maximize2, Minimize2 } from 'lucide-react';
import { jsPDF } from "jspdf";
import autoTable from 'jspdf-autotable';
import VisualizationView from './VisualizationView';
import SqlViewer from './SqlViewer';
import DataTable from './DataTable';

export default function DataCanvas({
  activeMessageWithData,
  activeDataIndex,
  handleLoadMore,
  onSetPreset,
  isCanvasMaximized,
  setIsCanvasMaximized
}) {
  const exportToPDF = () => {
    if (!activeMessageWithData || !activeMessageWithData.all_sql_results || activeMessageWithData.all_sql_results.length === 0) return;
    
    const doc = new jsPDF('landscape');
    
    // Official Police Header & Confidentiality
    doc.setFontSize(14);
    doc.setFont("helvetica", "bold");
    doc.text("ALOKA — KARNATAKA STATE POLICE INTELLIGENCE DOSSIER", 14, 15);
    
    doc.setFontSize(9);
    doc.setFont("helvetica", "normal");
    doc.setTextColor(100, 100, 100);
    doc.text("Generated: " + new Date().toLocaleString() + " IST", 14, 21);
    
    doc.setTextColor(220, 38, 38);
    doc.setFont("helvetica", "bold");
    doc.text("CONFIDENTIAL — LAW ENFORCEMENT & INVESTIGATION USE ONLY", 14, 27);
    
    // Table Rendering
    const data = activeMessageWithData.all_sql_results[0];
    if (data && data.length > 0) {
      const columns = Object.keys(data[0]);
      const rows = data.map(row => columns.map(col => String(row[col] === null || row[col] === undefined ? '-' : row[col])));
      
      autoTable(doc, {
        startY: 33,
        head: [columns],
        body: rows,
        theme: 'grid',
        headStyles: { fillColor: [47, 93, 168], textColor: [255, 255, 255], fontStyle: 'bold' },
        styles: { fontSize: 7, cellPadding: 2, overflow: 'linebreak' },
        columnStyles: { text: { cellWidth: 'auto' } }
      });
    }
    
    doc.save('KSP_Aloka_Intelligence_Report.pdf');
  };

  const hasResults = activeMessageWithData && activeMessageWithData.all_sql_results && activeMessageWithData.all_sql_results.length > 0;
  const visualizationData = activeMessageWithData?.chart_metadata || activeMessageWithData?.visualization;

  return (
    <section className="flex-1 bg-white dark:bg-[#101722] flex flex-col relative overflow-hidden transition-colors duration-200 h-full">
      {/* Canvas Top Bar */}
      <div className="h-14 sm:h-16 bg-slate-50 dark:bg-[#101722] border-b border-slate-200 dark:border-[#263142] flex items-center justify-between px-4 sm:px-6 shrink-0 transition-colors gap-2 select-none">
        <div className="flex items-center gap-2 sm:gap-2.5">
          <Database className="w-4 h-4 text-[#2F5DA8] dark:text-[#93B4E8] shrink-0" />
          <div className="flex items-center gap-2">
            <h2 className="text-xs font-bold text-slate-800 dark:text-slate-100 uppercase tracking-widest font-mono truncate">
              Data Center
            </h2>
            {activeDataIndex !== null && (
              <span className="text-[10px] font-mono font-bold text-slate-600 dark:text-[#93B4E8] bg-slate-200 dark:bg-[#172640] px-2 py-0.5 rounded shrink-0 border border-transparent dark:border-[#263142]">
                Query #{activeDataIndex}
              </span>
            )}
          </div>
        </div>

        {/* Action Controls: Size Presets + PDF Export */}
        <div className="flex items-center gap-2">
          {/* Quick Width Adjust Presets (Hidden on Mobile) */}
          <div className="hidden lg:flex items-center bg-slate-100 dark:bg-[#141C28] p-0.5 rounded-lg border border-slate-200 dark:border-[#263142] text-[11px] font-mono text-slate-600 dark:text-slate-300">
            <button
              type="button"
              onClick={() => onSetPreset?.('default')}
              className="px-2 py-1 rounded hover:bg-white dark:hover:bg-[#172640] transition-colors"
              title="Default Layout"
            >
              Default
            </button>
            <button
              type="button"
              onClick={() => onSetPreset?.('balanced')}
              className="px-2 py-1 rounded hover:bg-white dark:hover:bg-[#172640] transition-colors"
              title="50% Chat / 50% Data Center"
            >
              50/50
            </button>
            <button
              type="button"
              onClick={() => onSetPreset?.('expanded')}
              className="px-2 py-1 rounded hover:bg-white dark:hover:bg-[#172640] transition-colors font-bold text-[#2F5DA8] dark:text-[#93B4E8]"
              title="70% Data Center Focus"
            >
              70%
            </button>
            <button
              type="button"
              onClick={() => onSetPreset?.('max')}
              className="px-2 py-1 rounded hover:bg-white dark:hover:bg-[#172640] transition-colors"
              title="85% Wide Data Center"
            >
              85%
            </button>
          </div>

          {/* Fullscreen Toggle */}
          <button
            type="button"
            onClick={() => setIsCanvasMaximized?.(!isCanvasMaximized)}
            className="p-1.5 sm:p-2 rounded-lg bg-slate-100 dark:bg-[#141C28] text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-[#172640] border border-slate-200 dark:border-[#263142] transition-colors cursor-pointer"
            title={isCanvasMaximized ? "Restore Split View" : "Maximize Data Center"}
            aria-label="Toggle Fullscreen Data Center"
          >
            {isCanvasMaximized ? <Minimize2 className="w-3.5 h-3.5" /> : <Maximize2 className="w-3.5 h-3.5" />}
          </button>

          {/* Export Dossier Button */}
          {hasResults && (
            <button 
              type="button"
              onClick={exportToPDF} 
              className="flex items-center gap-1.5 bg-[#2F5DA8] hover:bg-[#3A6DBD] text-white px-3 py-1.5 sm:py-2 rounded-lg text-xs font-bold transition-colors cursor-pointer shrink-0"
              title="Download PDF intelligence dossier"
              aria-label="Export Official Report"
            >
              <FileDown className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">Export Report</span>
            </button>
          )}
        </div>
      </div>

      {/* Canvas Scrollable Body */}
      <div className="flex-1 overflow-y-auto p-4 sm:p-6 bg-slate-100/70 dark:bg-[#0B1017] transition-colors">
        {!hasResults ? (
          <div className="flex flex-col h-full items-center justify-center text-center text-slate-400 dark:text-slate-500 gap-3 py-16 animate-fade-in select-none">
            <div className="w-14 h-14 rounded-2xl bg-white dark:bg-[#141C28] border border-slate-200 dark:border-[#263142] flex items-center justify-center shadow-xs">
              <LineChart className="w-6 h-6 text-slate-400 dark:text-slate-500" />
            </div>
            <div className="flex flex-col gap-1 max-w-sm">
              <span className="text-sm font-bold text-slate-700 dark:text-slate-300">
                No analytical result to display yet.
              </span>
              <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
                Select a query or ask Aloka a question to inspect visual crime analytics and structured database records.
              </p>
            </div>
          </div>
        ) : (
          <div className="flex flex-col gap-6 max-w-7xl mx-auto animate-fade-in pb-8">
            {/* 1. Primary Visualization + Key Insight */}
            <VisualizationView visualization={visualizationData} />

            {/* 2. Structured Data Section */}
            {activeMessageWithData.all_sql_results.map((resultSet, idx) => {
              const sqlCommand = activeMessageWithData.all_generated_sql?.[idx];
              const paginationInfo = activeMessageWithData.all_pagination?.[idx];
              const hasVisualization = Boolean(visualizationData && visualizationData.response_type === 'chart');

              return (
                <div key={idx} className="flex flex-col gap-4">
                  {/* Collapsible View Data Table */}
                  <DataTable
                    resultSet={resultSet}
                    paginationInfo={paginationInfo}
                    queryIndex={idx}
                    totalQueries={activeMessageWithData.all_sql_results.length}
                    defaultOpen={!hasVisualization || idx === 0}
                    onLoadMore={() => handleLoadMore(idx)}
                  />

                  {/* Collapsible Executed SQL & Query Metadata */}
                  <SqlViewer
                    sqlCommand={sqlCommand}
                    queryIndex={idx}
                    totalQueries={activeMessageWithData.all_sql_results.length}
                    rowsCount={resultSet?.length || 0}
                  />
                </div>
              );
            })}
          </div>
        )}
      </div>
    </section>
  );
}

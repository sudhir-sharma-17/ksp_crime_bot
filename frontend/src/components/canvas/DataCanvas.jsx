import React from 'react';
import { Database, FileDown, Layers, Sparkles } from 'lucide-react';
import { jsPDF } from "jspdf";
import autoTable from 'jspdf-autotable';
import VisualizationView from './VisualizationView';
import SqlViewer from './SqlViewer';
import DataTable from './DataTable';

export default function DataCanvas({
  activeMessageWithData,
  activeDataIndex,
  handleLoadMore
}) {
  const exportToPDF = () => {
    if (!activeMessageWithData || !activeMessageWithData.all_sql_results || activeMessageWithData.all_sql_results.length === 0) return;
    
    const doc = new jsPDF('landscape');
    
    // Official Header & Confidentiality
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
        headStyles: { fillColor: [30, 58, 138], textColor: [255, 255, 255], fontStyle: 'bold' },
        styles: { fontSize: 7, cellPadding: 2, overflow: 'linebreak' },
        columnStyles: { text: { cellWidth: 'auto' } }
      });
    }
    
    doc.save('KSP_Aloka_Intelligence_Report.pdf');
  };

  const hasResults = activeMessageWithData && activeMessageWithData.all_sql_results && activeMessageWithData.all_sql_results.length > 0;
  const visualizationData = activeMessageWithData?.chart_metadata || activeMessageWithData?.visualization;

  return (
    <section className="flex-1 bg-white dark:bg-slate-900 flex flex-col relative overflow-hidden transition-colors duration-300">
      {/* Canvas Top Bar */}
      <div className="h-16 bg-slate-50 dark:bg-slate-900/90 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between px-6 shrink-0 transition-colors">
        <div className="flex items-center gap-2.5">
          <Database className="w-4 h-4 text-blue-600 dark:text-cyan-400" />
          <h2 className="text-xs font-bold text-slate-800 dark:text-slate-200 uppercase tracking-widest font-mono">
            Data Canvas {activeDataIndex !== null ? `• Query #${activeDataIndex}` : ''}
          </h2>
        </div>

        {hasResults && (
          <button 
            onClick={exportToPDF} 
            className="flex items-center gap-1.5 bg-blue-900 hover:bg-blue-800 dark:bg-blue-800 dark:hover:bg-blue-700 text-white px-3.5 py-2 rounded-xl text-xs font-bold shadow-xs transition-all cursor-pointer"
            title="Download PDF intelligence dossier"
          >
            <FileDown className="w-3.5 h-3.5" />
            <span>Export Official Dossier</span>
          </button>
        )}
      </div>

      {/* Canvas Content Container */}
      <div className="flex-1 overflow-y-auto p-6 bg-slate-100/70 dark:bg-slate-950 transition-colors">
        {!hasResults ? (
          <div className="flex flex-col h-full items-center justify-center text-slate-400 dark:text-slate-600 gap-2.5">
            <Layers className="w-12 h-12 stroke-1 opacity-40" />
            <span className="text-xs font-medium font-mono uppercase tracking-wider">Awaiting structured intelligence data</span>
          </div>
        ) : (
          <div className="flex flex-col gap-6 max-w-7xl mx-auto animate-fade-in pb-8">
            {/* 1. Priority: Visual Intelligence Dashboard */}
            <VisualizationView visualization={visualizationData} />

            {/* 2. Structured Data Tables & 3. Collapsible Executed SQL */}
            {activeMessageWithData.all_sql_results.map((resultSet, idx) => {
              const sqlCommand = activeMessageWithData.all_generated_sql?.[idx];
              const paginationInfo = activeMessageWithData.all_pagination?.[idx];

              return (
                <div key={idx} className="flex flex-col gap-3">
                  {/* Structured Case Table */}
                  <DataTable
                    resultSet={resultSet}
                    paginationInfo={paginationInfo}
                    queryIndex={idx}
                    totalQueries={activeMessageWithData.all_sql_results.length}
                    onLoadMore={() => handleLoadMore(idx)}
                  />

                  {/* Collapsible Executed SQL (Secondary) */}
                  <SqlViewer
                    sqlCommand={sqlCommand}
                    queryIndex={idx}
                    totalQueries={activeMessageWithData.all_sql_results.length}
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

import re

with open("frontend/src/components/Dashboard.jsx", "r") as f:
    content = f.read()

# 1. Imports
if "import jsPDF" not in content:
    content = content.replace(
        "import remarkGfm from 'remark-gfm';",
        "import remarkGfm from 'remark-gfm';\nimport jsPDF from 'jspdf';\nimport 'jspdf-autotable';"
    )

# 2. PDF Logic inside Dashboard function
pdf_logic = """
  const exportToPDF = () => {
    if (!activeMessageWithData || !activeMessageWithData.all_sql_results || activeMessageWithData.all_sql_results.length === 0) return;
    
    const doc = new jsPDF('landscape');
    
    // Branding
    doc.setFontSize(14);
    doc.setFont("helvetica", "bold");
    doc.text("ALOKA - KSP OFFICIAL INTELLIGENCE REPORT", 14, 15);
    
    doc.setFontSize(10);
    doc.setFont("helvetica", "normal");
    doc.setTextColor(100, 100, 100);
    doc.text("Generated on: " + new Date().toLocaleString(), 14, 22);
    
    doc.setTextColor(220, 38, 38);
    doc.setFont("helvetica", "bold");
    doc.text("CONFIDENTIAL - FOR OFFICIAL USE ONLY", 14, 28);
    
    // Table
    const data = activeMessageWithData.all_sql_results[0];
    if (data && data.length > 0) {
      const columns = Object.keys(data[0]);
      const rows = data.map(row => columns.map(col => String(row[col])));
      
      doc.autoTable({
        startY: 35,
        head: [columns],
        body: rows,
        theme: 'grid',
        headStyles: { fillColor: [30, 58, 138] },
        styles: { fontSize: 8, cellPadding: 2, overflow: 'linebreak' },
        columnStyles: { text: { cellWidth: 'auto' } }
      });
    }
    
    doc.save('KSP_Intelligence_Report.pdf');
  };
"""

if "exportToPDF" not in content:
    # insert before "const handleSendMessage"
    content = content.replace("const handleSendMessage", pdf_logic.strip() + "\n\n  const handleSendMessage")

# 3. Header integration
old_header = """          {/* Header of Canvas */}
          <div className="h-12 bg-gray-100 border-b border-gray-200 flex items-center px-6 shrink-0">
            <h2 className="text-sm font-bold text-gray-600 uppercase tracking-widest flex items-center gap-2">
              <Database className="w-4 h-4" /> Data Canvas {activeDataIndex !== null ? `— Viewing Query #${activeDataIndex}` : ''}
            </h2>
          </div>"""

new_header = """          {/* Header of Canvas */}
          <div className="h-12 bg-gray-100 border-b border-gray-200 flex items-center justify-between px-6 shrink-0">
            <h2 className="text-sm font-bold text-gray-600 uppercase tracking-widest flex items-center gap-2">
              <Database className="w-4 h-4" /> Data Canvas {activeDataIndex !== null ? `— Viewing Query #${activeDataIndex}` : ''}
            </h2>
            {activeMessageWithData && activeMessageWithData.all_sql_results && activeMessageWithData.all_sql_results.length > 0 && (
              <button onClick={exportToPDF} className="flex items-center gap-2 bg-blue-900 hover:bg-blue-800 text-white px-3 py-1.5 rounded text-xs font-bold shadow-sm transition-all">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
                Export Official Report
              </button>
            )}
          </div>"""

content = content.replace(old_header, new_header)

with open("frontend/src/components/Dashboard.jsx", "w") as f:
    f.write(content)

print("Dashboard PDF logic patched")

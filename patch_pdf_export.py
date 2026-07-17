with open("frontend/src/components/Dashboard.jsx", "r") as f:
    content = f.read()

# 1. Fix imports
old_imports = """import jsPDF from 'jspdf';
import 'jspdf-autotable';"""
new_imports = """import { jsPDF } from "jspdf";
import autoTable from 'jspdf-autotable';"""

content = content.replace(old_imports, new_imports)

# 2. Fix autoTable call
old_autotable = """      doc.autoTable({
        startY: 35,"""
new_autotable = """      autoTable(doc, {
        startY: 35,"""

content = content.replace(old_autotable, new_autotable)

with open("frontend/src/components/Dashboard.jsx", "w") as f:
    f.write(content)

print("PDF export patched successfully.")

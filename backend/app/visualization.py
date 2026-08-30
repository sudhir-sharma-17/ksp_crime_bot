import re
from typing import List, Dict, Any, Optional

def determine_visualization(
    user_query: str,
    query_plan: Optional[Dict[str, Any]] = None,
    sql_results: Optional[List[Dict[str, Any]]] = None,
    generated_sql: Optional[str] = None
) -> Dict[str, Any]:
    """
    Deterministically determines the optimal visualization (Bar, Pie, Line, Table, Text)
    based on the user query, structured query plan, and database results.
    """
    q_lower = (user_query or "").lower().strip()
    plan = query_plan or {}
    results = sql_results or []
    sql_upper = (generated_sql or "").upper()

    # ── 1. Empty Results or Non-DB Queries ──
    if not results or generated_sql in ["CHITCHAT", "CLARIFICATION"]:
        return {
            "response_type": "text",
            "chart_type": "none",
            "title": "",
            "label_column": "",
            "value_column": "",
            "data": []
        }

    # ── 2. Explicit Non-Chart Questions (Single Case / Narrative / Lookup) ──
    non_chart_patterns = [
        r'\bwho\s+is\s+the\s+(victim|accused|complainant|officer|io)\b',
        r'\bwhat\s+happened\b',
        r'\bshow\s+the\s+accused,\s*victim\b',
        r'\bwho\s+was\s+the\s+accused\b',
        r'\bwhat\s+acts\s+and\s+sections\b',
        r'\bdetails\s+of\b',
        r'\bwas\s+the\s+accused\b'
    ]
    for pattern in non_chart_patterns:
        if re.search(pattern, q_lower):
            if len(results) == 1 and len(results[0]) <= 2 and not any(k.lower() in ["case_count", "total_cases", "count"] for k in results[0].keys()):
                return {
                    "response_type": "text",
                    "chart_type": "none",
                    "title": "",
                    "label_column": "",
                    "value_column": "",
                    "data": []
                }
            return {
                "response_type": "table",
                "chart_type": "none",
                "title": "",
                "label_column": "",
                "value_column": "",
                "data": results
            }

    # ── 3. Find Label Column and Numeric Value Column from Results ──
    first_row = results[0]
    keys = list(first_row.keys())
    
    # Identify numeric column for chart values
    numeric_cols = []
    text_cols = []
    date_cols = []

    for k in keys:
        val = first_row[k]
        k_lower = k.lower()
        if any(dt in k_lower for dt in ["date", "time", "month", "year", "day"]):
            date_cols.append(k)
        elif isinstance(val, (int, float)) or (isinstance(val, str) and val.isdigit()):
            numeric_cols.append(k)
        else:
            text_cols.append(k)

    # ── 4. Line Chart: Time Series / Trend Analytics ──
    time_keywords = ["over time", "trend", "by month", "by year", "by date", "monthly", "yearly", "timeline", "registered over time"]
    if any(tk in q_lower for tk in time_keywords) or (date_cols and (numeric_cols or "GROUP BY" in sql_upper)):
        label_col = date_cols[0] if date_cols else (text_cols[0] if text_cols else keys[0])
        val_col = numeric_cols[0] if numeric_cols else (keys[-1] if len(keys) > 1 else keys[0])
        
        chart_data = []
        for r in results:
            chart_data.append({
                "label": str(r.get(label_col, "")),
                "value": float(r.get(val_col, 0)) if str(r.get(val_col, "0")).replace(".", "", 1).isdigit() else 0
            })
            
        chart_data.sort(key=lambda x: str(x.get("label", "")))

        return {
            "response_type": "chart",
            "chart_type": "line",
            "title": "Cases Registered Over Time",
            "label_column": label_col,
            "value_column": val_col,
            "data": chart_data
        }

    # ── 5. Pie / Donut Chart: Categorical Distribution / Proportions ──
    pie_keywords = ["by status", "case status", "proportion", "distribution", "share", "by category", "percentage"]
    if any(pk in q_lower for pk in pie_keywords) and len(results) <= 10 and (numeric_cols or "COUNT" in sql_upper):
        label_col = text_cols[0] if text_cols else keys[0]
        val_col = numeric_cols[0] if numeric_cols else (keys[-1] if len(keys) > 1 else keys[0])
        
        chart_data = []
        for r in results:
            chart_data.append({
                "label": str(r.get(label_col, "")),
                "value": float(r.get(val_col, 0)) if str(r.get(val_col, "0")).replace(".", "", 1).isdigit() else 0
            })

        title = "Cases by Status" if "status" in q_lower else "Case Distribution"
        return {
            "response_type": "chart",
            "chart_type": "pie",
            "title": title,
            "label_column": label_col,
            "value_column": val_col,
            "data": chart_data
        }

    # ── 6. Bar Chart: Ranking / Top N / Comparison / Station Counts ──
    bar_keywords = ["most cases", "top", "rank", "ranking", "by police station", "by station", "highest", "lowest", "compare", "for each police station", "each police station"]
    is_grouped_query = "GROUP BY" in sql_upper or plan.get("group_by") or plan.get("order_by")
    
    if (any(bk in q_lower for bk in bar_keywords) or is_grouped_query) and (numeric_cols or "COUNT" in sql_upper or "case_count" in [k.lower() for k in keys]):
        label_col = text_cols[0] if text_cols else keys[0]
        val_col = numeric_cols[0] if numeric_cols else (keys[-1] if len(keys) > 1 else keys[0])
        
        chart_data = []
        for r in results:
            raw_val = r.get(val_col, 0)
            try:
                numeric_val = float(raw_val)
            except (ValueError, TypeError):
                numeric_val = 0
            chart_data.append({
                "label": str(r.get(label_col, "")),
                "value": numeric_val
            })

        title = "Cases by Police Station" if "station" in q_lower else "Comparative Crime Analytics"
        return {
            "response_type": "chart",
            "chart_type": "bar",
            "title": title,
            "label_column": label_col,
            "value_column": val_col,
            "data": chart_data
        }

    # ── 7. Single Numeric Total Count ──
    if len(results) == 1 and len(keys) == 1 and numeric_cols:
        return {
            "response_type": "text",
            "chart_type": "none",
            "title": "",
            "label_column": "",
            "value_column": "",
            "data": results
        }

    # ── 8. Default Table Response ──
    return {
        "response_type": "table",
        "chart_type": "none",
        "title": "",
        "label_column": "",
        "value_column": "",
        "data": results
    }

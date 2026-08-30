import asyncio
import os
import sys

# Ensure backend directory is in sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding='utf-8')

if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app.visualization import determine_visualization
from app.agent import get_db_connection
from sqlalchemy import text

async def run_phase6_tests():
    print("=" * 80)
    print("PHASE 6 — AUTOMATIC VISUALIZATION FAST VERIFICATION SUITE")
    print("=" * 80)

    engine = get_db_connection()

    # -------------------------------------------------------------
    # TEST 1: "Which police station has the most cases?" (Expected: BAR CHART)
    # -------------------------------------------------------------
    print("\n[TEST 1] 'Which police station has the most cases?'")
    q1 = "Which police station has the most cases?"
    sql1 = (
        "SELECT u.UnitName, COUNT(cm.CaseMasterID) AS case_count "
        "FROM casemaster cm JOIN unit u ON cm.PoliceStationID = u.UnitID "
        "GROUP BY u.UnitName ORDER BY case_count DESC LIMIT 1"
    )
    with engine.connect() as conn:
        res1 = [dict(r._mapping) for r in conn.execute(text(sql1)).fetchall()]
    
    viz1 = determine_visualization(q1, {"group_by": ["unit.UnitName"]}, res1, sql1)
    print(f"  Response Type: {viz1.get('response_type')}")
    print(f"  Chart Type: {viz1.get('chart_type')}")
    print(f"  Title: {viz1.get('title')}")
    print(f"  Data Sample: {viz1.get('data')}")
    assert viz1["response_type"] == "chart", f"Test 1 failed: Expected 'chart', got '{viz1['response_type']}'"
    assert viz1["chart_type"] == "bar", f"Test 1 failed: Expected 'bar', got '{viz1['chart_type']}'"
    assert len(viz1["data"]) > 0, "Test 1 failed: Empty chart data"
    print("  -> TEST 1 PASSED [OK]")

    # -------------------------------------------------------------
    # TEST 2: "Show the top 5 police stations by number of cases." (Expected: BAR CHART)
    # -------------------------------------------------------------
    print("\n[TEST 2] 'Show the top 5 police stations by number of cases.'")
    q2 = "Show the top 5 police stations by number of cases."
    sql2 = (
        "SELECT u.UnitName, COUNT(cm.CaseMasterID) AS case_count "
        "FROM casemaster cm JOIN unit u ON cm.PoliceStationID = u.UnitID "
        "GROUP BY u.UnitName ORDER BY case_count DESC LIMIT 5"
    )
    with engine.connect() as conn:
        res2 = [dict(r._mapping) for r in conn.execute(text(sql2)).fetchall()]

    viz2 = determine_visualization(q2, {"group_by": ["unit.UnitName"], "limit": 5}, res2, sql2)
    print(f"  Response Type: {viz2.get('response_type')}")
    print(f"  Chart Type: {viz2.get('chart_type')}")
    print(f"  Title: {viz2.get('title')}")
    print(f"  Data Points: {len(viz2.get('data'))}")
    assert viz2["response_type"] == "chart", f"Test 2 failed: Expected 'chart', got '{viz2['response_type']}'"
    assert viz2["chart_type"] == "bar", f"Test 2 failed: Expected 'bar', got '{viz2['chart_type']}'"
    assert len(viz2["data"]) == 5, f"Test 2 failed: Expected 5 data points, got {len(viz2['data'])}"
    print("  -> TEST 2 PASSED [OK]")

    # -------------------------------------------------------------
    # TEST 3: "Show the number of cases by status." (Expected: PIE/DONUT CHART)
    # -------------------------------------------------------------
    print("\n[TEST 3] 'Show the number of cases by status.'")
    q3 = "Show the number of cases by status."
    sql3 = (
        "SELECT csm.CaseStatusName, COUNT(cm.CaseMasterID) AS case_count "
        "FROM casemaster cm JOIN casestatusmaster csm ON cm.CaseStatusID = csm.CaseStatusID "
        "GROUP BY csm.CaseStatusName"
    )
    with engine.connect() as conn:
        res3 = [dict(r._mapping) for r in conn.execute(text(sql3)).fetchall()]

    viz3 = determine_visualization(q3, {"group_by": ["casestatusmaster.CaseStatusName"]}, res3, sql3)
    print(f"  Response Type: {viz3.get('response_type')}")
    print(f"  Chart Type: {viz3.get('chart_type')}")
    print(f"  Title: {viz3.get('title')}")
    print(f"  Data Points: {viz3.get('data')}")
    assert viz3["response_type"] == "chart", f"Test 3 failed: Expected 'chart', got '{viz3['response_type']}'"
    assert viz3["chart_type"] == "pie", f"Test 3 failed: Expected 'pie', got '{viz3['chart_type']}'"
    print("  -> TEST 3 PASSED [OK]")

    # -------------------------------------------------------------
    # TEST 4: "Show the number of cases registered over time." (Expected: LINE CHART)
    # -------------------------------------------------------------
    print("\n[TEST 4] 'Show the number of cases registered over time.'")
    q4 = "Show the number of cases registered over time."
    sql4 = (
        "SELECT DATE(CrimeRegisteredDate) AS reg_date, COUNT(CaseMasterID) AS case_count "
        "FROM casemaster WHERE CrimeRegisteredDate IS NOT NULL "
        "GROUP BY DATE(CrimeRegisteredDate) ORDER BY reg_date ASC LIMIT 10"
    )
    with engine.connect() as conn:
        res4 = [dict(r._mapping) for r in conn.execute(text(sql4)).fetchall()]

    viz4 = determine_visualization(q4, {"group_by": ["casemaster.CrimeRegisteredDate"]}, res4, sql4)
    print(f"  Response Type: {viz4.get('response_type')}")
    print(f"  Chart Type: {viz4.get('chart_type')}")
    print(f"  Title: {viz4.get('title')}")
    print(f"  Data Points: {len(viz4.get('data'))}")
    assert viz4["response_type"] == "chart", f"Test 4 failed: Expected 'chart', got '{viz4['response_type']}'"
    assert viz4["chart_type"] == "line", f"Test 4 failed: Expected 'line', got '{viz4['chart_type']}'"
    print("  -> TEST 4 PASSED [OK]")

    # -------------------------------------------------------------
    # TEST 5: "Who is the victim of KSP-CASE-0004?" (Expected: NOT CHART)
    # -------------------------------------------------------------
    print("\n[TEST 5] 'Who is the victim of KSP-CASE-0004?' (Expected: Non-Chart Table/Text)")
    q5 = "Who is the victim of KSP-CASE-0004?"
    sql5 = (
        "SELECT v.VictimName FROM casemaster cm "
        "JOIN victim v ON cm.CaseMasterID = v.CaseMasterID WHERE cm.CaseNo = 'KSP-CASE-0004'"
    )
    with engine.connect() as conn:
        res5 = [dict(r._mapping) for r in conn.execute(text(sql5)).fetchall()]

    viz5 = determine_visualization(q5, {"entities": {"case_no": "KSP-CASE-0004"}}, res5, sql5)
    print(f"  Response Type: {viz5.get('response_type')}")
    print(f"  Chart Type: {viz5.get('chart_type')}")
    assert viz5["chart_type"] == "none", f"Test 5 failed: Expected chart_type 'none', got '{viz5['chart_type']}'"
    assert viz5["response_type"] in ["table", "text"], f"Test 5 failed: Expected table/text, got '{viz5['response_type']}'"
    print("  -> TEST 5 PASSED [OK] (Properly suppressed chart generation)")

    # -------------------------------------------------------------
    # TEST 6: "What happened in KSP-CASE-0004?" (Expected: NOT CHART)
    # -------------------------------------------------------------
    print("\n[TEST 6] 'What happened in KSP-CASE-0004?' (Expected: Non-Chart Text)")
    q6 = "What happened in KSP-CASE-0004?"
    sql6 = "SELECT cm.BriefFacts FROM casemaster cm WHERE cm.CaseNo = 'KSP-CASE-0004'"
    with engine.connect() as conn:
        res6 = [dict(r._mapping) for r in conn.execute(text(sql6)).fetchall()]

    viz6 = determine_visualization(q6, {"entities": {"case_no": "KSP-CASE-0004"}}, res6, sql6)
    print(f"  Response Type: {viz6.get('response_type')}")
    print(f"  Chart Type: {viz6.get('chart_type')}")
    assert viz6["chart_type"] == "none", f"Test 6 failed: Expected chart_type 'none', got '{viz6['chart_type']}'"
    print("  -> TEST 6 PASSED [OK] (Properly suppressed chart generation)")

    print("\n" + "=" * 80)
    print("ALL PHASE 6 VISUALIZATION TESTS PASSED WITH 0 ERRORS!")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(run_phase6_tests())

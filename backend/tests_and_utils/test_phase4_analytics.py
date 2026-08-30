import asyncio
import os
import sys

# Ensure backend directory is in sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app.agent import (
    DB_SCHEMA,
    resolve_conversation_context,
    resolve_table_joins,
    schema_validator_node,
    execute_sql_node,
    agent_app
)

async def run_phase4_tests():
    print("=" * 80)
    print("PHASE 4 — ANALYTICS & DATA INSIGHTS FAST VERIFICATION SUITE")
    print("=" * 80)

    # -------------------------------------------------------------
    # TEST 1: "How many cases are there?"
    # -------------------------------------------------------------
    print("\n[TEST 1] 'How many cases are there?'")
    state_1 = {
        "user_query": "How many cases are there?",
        "queries": ["How many cases are there?"],
        "current_query_index": 0,
        "query_plan": {
            "intent": "count_cases",
            "target_tables": ["casemaster"],
            "ambiguous": False,
            "clarification_question": "",
            "entities": {"case_no": None, "person_name": None, "station_name": None},
            "filters": [],
            "requested_fields": ["COUNT(*) AS total_cases"],
            "relationships_required": [],
            "aggregation": {"function": "COUNT", "expression": "*"}
        },
        "chat_history": []
    }
    validated_state_1 = await schema_validator_node(state_1)
    plan_1 = validated_state_1["query_plan"]
    print(f"  Intent: {plan_1['intent']}")
    print(f"  Aggregation: {plan_1.get('aggregation')}")
    print(f"  Target Tables: {plan_1['target_tables']}")
    
    sql_1 = "SELECT COUNT(*) AS total_cases FROM casemaster"
    exec_state_1 = await execute_sql_node({**validated_state_1, "generated_sql": sql_1})
    print(f"  SQL: {sql_1}")
    print(f"  Result: {exec_state_1['sql_results'][0] if exec_state_1['sql_results'] else 'None'}")
    assert exec_state_1["sql_results_total"] > 0, "Test 1 failed: No rows returned"
    print("  -> TEST 1 PASSED [OK]")

    # -------------------------------------------------------------
    # TEST 2: "Which police station has the most cases?"
    # -------------------------------------------------------------
    print("\n[TEST 2] 'Which police station has the most cases?'")
    state_2 = {
        "user_query": "Which police station has the most cases?",
        "queries": ["Which police station has the most cases?"],
        "current_query_index": 0,
        "query_plan": {
            "intent": "rank_police_stations_by_cases",
            "target_tables": ["casemaster", "unit"],
            "ambiguous": False,
            "clarification_question": "",
            "entities": {"case_no": None, "person_name": None, "station_name": None},
            "filters": [],
            "requested_fields": ["unit.UnitName", "COUNT(casemaster.CaseMasterID) AS case_count"],
            "relationships_required": [],
            "aggregation": {"function": "COUNT", "expression": "casemaster.CaseMasterID"},
            "group_by": ["unit.UnitName"],
            "order_by": {"expression": "COUNT(casemaster.CaseMasterID)", "direction": "DESC"},
            "limit": 1
        },
        "chat_history": []
    }
    validated_state_2 = await schema_validator_node(state_2)
    plan_2 = validated_state_2["query_plan"]
    print(f"  Intent: {plan_2['intent']}")
    print(f"  Target Tables: {plan_2['target_tables']}")
    print(f"  Group By: {plan_2.get('group_by')}")
    print(f"  Order By: {plan_2.get('order_by')}")
    print(f"  Limit: {plan_2.get('limit')}")
    assert len(plan_2["relationships_required"]) == 1, "Test 2 failed: Join not inferred"
    
    sql_2 = (
        "SELECT unit.UnitName, COUNT(casemaster.CaseMasterID) AS case_count "
        "FROM casemaster "
        "JOIN unit ON casemaster.PoliceStationID = unit.UnitID "
        "GROUP BY unit.UnitName "
        "ORDER BY case_count DESC "
        "LIMIT 1"
    )
    exec_state_2 = await execute_sql_node({**validated_state_2, "generated_sql": sql_2})
    print(f"  SQL: {sql_2}")
    print(f"  Rows Returned: {exec_state_2['sql_results_total']}")
    print(f"  Top Station: {exec_state_2['sql_results'][0] if exec_state_2['sql_results'] else 'None'}")
    assert exec_state_2["sql_results_total"] == 1, f"Test 2 failed: Expected 1 row, got {exec_state_2['sql_results_total']}"
    print("  -> TEST 2 PASSED [OK]")

    # -------------------------------------------------------------
    # TEST 3: "Show the top 5 police stations by number of cases."
    # -------------------------------------------------------------
    print("\n[TEST 3] 'Show the top 5 police stations by number of cases.'")
    state_3 = {
        "user_query": "Show the top 5 police stations by number of cases.",
        "queries": ["Show the top 5 police stations by number of cases."],
        "current_query_index": 0,
        "query_plan": {
            "intent": "rank_police_stations_by_cases",
            "target_tables": ["casemaster", "unit"],
            "ambiguous": False,
            "clarification_question": "",
            "entities": {"case_no": None, "person_name": None, "station_name": None},
            "filters": [],
            "requested_fields": ["unit.UnitName", "COUNT(casemaster.CaseMasterID) AS case_count"],
            "relationships_required": [],
            "aggregation": {"function": "COUNT", "expression": "casemaster.CaseMasterID"},
            "group_by": ["unit.UnitName"],
            "order_by": {"expression": "COUNT(casemaster.CaseMasterID)", "direction": "DESC"},
            "limit": 5
        },
        "chat_history": []
    }
    validated_state_3 = await schema_validator_node(state_3)
    plan_3 = validated_state_3["query_plan"]
    print(f"  Target Tables: {plan_3['target_tables']}")
    print(f"  Limit: {plan_3.get('limit')}")
    
    sql_3 = (
        "SELECT unit.UnitName, COUNT(casemaster.CaseMasterID) AS case_count "
        "FROM casemaster "
        "JOIN unit ON casemaster.PoliceStationID = unit.UnitID "
        "GROUP BY unit.UnitName "
        "ORDER BY case_count DESC "
        "LIMIT 5"
    )
    exec_state_3 = await execute_sql_node({**validated_state_3, "generated_sql": sql_3})
    print(f"  SQL: {sql_3}")
    print(f"  Rows Returned: {exec_state_3['sql_results_total']}")
    print(f"  Top 5 Stations: {exec_state_3['sql_results']}")
    assert exec_state_3["sql_results_total"] == 5, f"Test 3 failed: Expected 5 rows, got {exec_state_3['sql_results_total']}"
    print("  -> TEST 3 PASSED [OK]")

    # -------------------------------------------------------------
    # TEST 4: "How many cases are there for each police station?"
    # -------------------------------------------------------------
    print("\n[TEST 4] 'How many cases are there for each police station?'")
    state_4 = {
        "user_query": "How many cases are there for each police station?",
        "queries": ["How many cases are there for each police station?"],
        "current_query_index": 0,
        "query_plan": {
            "intent": "count_cases_by_station",
            "target_tables": ["casemaster", "unit"],
            "ambiguous": False,
            "clarification_question": "",
            "entities": {"case_no": None, "person_name": None, "station_name": None},
            "filters": [],
            "requested_fields": ["unit.UnitName", "COUNT(casemaster.CaseMasterID) AS case_count"],
            "relationships_required": [],
            "aggregation": {"function": "COUNT", "expression": "casemaster.CaseMasterID"},
            "group_by": ["unit.UnitName"],
            "order_by": {"expression": "COUNT(casemaster.CaseMasterID)", "direction": "DESC"}
        },
        "chat_history": []
    }
    validated_state_4 = await schema_validator_node(state_4)
    plan_4 = validated_state_4["query_plan"]
    print(f"  Target Tables: {plan_4['target_tables']}")
    print(f"  Group By: {plan_4.get('group_by')}")
    
    sql_4 = (
        "SELECT unit.UnitName, COUNT(casemaster.CaseMasterID) AS case_count "
        "FROM casemaster "
        "JOIN unit ON casemaster.PoliceStationID = unit.UnitID "
        "GROUP BY unit.UnitName "
        "ORDER BY case_count DESC"
    )
    exec_state_4 = await execute_sql_node({**validated_state_4, "generated_sql": sql_4})
    print(f"  SQL: {sql_4}")
    print(f"  Rows Returned: {exec_state_4['sql_results_total']}")
    print(f"  Sample Station Count: {exec_state_4['sql_results'][0] if exec_state_4['sql_results'] else 'None'}")
    assert exec_state_4["sql_results_total"] > 0, "Test 4 failed: No rows returned"
    print("  -> TEST 4 PASSED [OK]")

    # -------------------------------------------------------------
    # TEST 5: "Which crime category has the most cases?"
    # -------------------------------------------------------------
    print("\n[TEST 5] 'Which crime category has the most cases?'")
    state_5 = {
        "user_query": "Which crime category has the most cases?",
        "queries": ["Which crime category has the most cases?"],
        "current_query_index": 0,
        "query_plan": {
            "intent": "rank_categories_by_cases",
            "target_tables": ["casemaster", "casecategory"],
            "ambiguous": False,
            "clarification_question": "",
            "entities": {"case_no": None, "person_name": None, "station_name": None},
            "filters": [],
            "requested_fields": ["casecategory.LookupValue AS CategoryName", "COUNT(casemaster.CaseMasterID) AS case_count"],
            "relationships_required": [],
            "aggregation": {"function": "COUNT", "expression": "casemaster.CaseMasterID"},
            "group_by": ["casecategory.LookupValue"],
            "order_by": {"expression": "COUNT(casemaster.CaseMasterID)", "direction": "DESC"},
            "limit": 1
        },
        "chat_history": []
    }
    validated_state_5 = await schema_validator_node(state_5)
    plan_5 = validated_state_5["query_plan"]
    print(f"  Target Tables: {plan_5['target_tables']}")
    print(f"  Group By: {plan_5.get('group_by')}")
    assert len(plan_5["relationships_required"]) == 1, "Test 5 failed: Join casemaster->casecategory not inferred"
    
    sql_5 = (
        "SELECT casecategory.LookupValue AS CategoryName, COUNT(casemaster.CaseMasterID) AS case_count "
        "FROM casemaster "
        "JOIN casecategory ON casemaster.CaseCategoryID = casecategory.CaseCategoryID "
        "GROUP BY casecategory.LookupValue "
        "ORDER BY case_count DESC "
        "LIMIT 1"
    )
    exec_state_5 = await execute_sql_node({**validated_state_5, "generated_sql": sql_5})
    print(f"  SQL: {sql_5}")
    print(f"  Rows Returned: {exec_state_5['sql_results_total']}")
    print(f"  Top Category: {exec_state_5['sql_results'][0] if exec_state_5['sql_results'] else 'None'}")
    assert exec_state_5["sql_results_total"] == 1, f"Test 5 failed: Expected 1 row, got {exec_state_5['sql_results_total']}"
    print("  -> TEST 5 PASSED [OK]")

    # -------------------------------------------------------------
    # TEST 6: "How many cases are open?"
    # -------------------------------------------------------------
    print("\n[TEST 6] 'How many cases are open?'")
    state_6 = {
        "user_query": "How many cases are open?",
        "queries": ["How many cases are open?"],
        "current_query_index": 0,
        "query_plan": {
            "intent": "count_open_cases",
            "target_tables": ["casemaster", "casestatusmaster"],
            "ambiguous": False,
            "clarification_question": "",
            "entities": {"case_no": None, "person_name": None, "station_name": None},
            "filters": [{"table": "casestatusmaster", "column": "CaseStatusName", "operator": "LIKE", "value": "%Under Investigation%"}],
            "requested_fields": ["COUNT(*) AS open_cases"],
            "relationships_required": [],
            "aggregation": {"function": "COUNT", "expression": "*"}
        },
        "chat_history": []
    }
    validated_state_6 = await schema_validator_node(state_6)
    plan_6 = validated_state_6["query_plan"]
    print(f"  Target Tables: {plan_6['target_tables']}")
    print(f"  Filters: {plan_6['filters']}")
    assert len(plan_6["relationships_required"]) == 1, "Test 6 failed: Join casemaster->casestatusmaster not inferred"
    
    sql_6 = (
        "SELECT COUNT(*) AS open_cases "
        "FROM casemaster "
        "JOIN casestatusmaster ON casemaster.CaseStatusID = casestatusmaster.CaseStatusID "
        "WHERE casestatusmaster.CaseStatusName LIKE '%Under Investigation%'"
    )
    exec_state_6 = await execute_sql_node({**validated_state_6, "generated_sql": sql_6})
    print(f"  SQL: {sql_6}")
    print(f"  Result: {exec_state_6['sql_results'][0] if exec_state_6['sql_results'] else 'None'}")
    assert exec_state_6["sql_results_total"] > 0, "Test 6 failed: No rows returned"
    print("  -> TEST 6 PASSED [OK]")

    # -------------------------------------------------------------
    # TEST 7: Turn 1: "Show KSP-CASE-0004." -> Turn 2: "How many accused are in this case?"
    # -------------------------------------------------------------
    print("\n[TEST 7] Contextual Count: Turn 1: 'Show KSP-CASE-0004.' -> Turn 2: 'How many accused are in this case?'")
    chat_hist_7 = [
        {"role": "user", "content": "Show KSP-CASE-0004."},
        {"role": "assistant", "content": "Here are the details for KSP-CASE-0004."}
    ]
    ctx_7 = resolve_conversation_context("How many accused are in this case?", chat_hist_7)
    print(f"  Context State: active_case='{ctx_7['active_case']}', is_global={ctx_7['is_global_query']}")
    assert ctx_7["active_case"] == "KSP-CASE-0004", "Test 7 failed: Active case context not preserved"
    assert not ctx_7["is_global_query"], "Test 7 failed: Contextual count incorrectly flagged as global"
    
    state_7 = {
        "user_query": "How many accused are in this case?",
        "queries": ["How many accused are in this case?"],
        "current_query_index": 0,
        "context_state": ctx_7,
        "query_plan": {
            "intent": "count_accused",
            "target_tables": ["casemaster", "accused"],
            "ambiguous": False,
            "clarification_question": "",
            "entities": {"case_no": "KSP-CASE-0004", "person_name": None, "station_name": None},
            "filters": [{"table": "casemaster", "column": "CaseNo", "operator": "=", "value": "KSP-CASE-0004"}],
            "requested_fields": ["COUNT(accused.AccusedMasterID) AS accused_count"],
            "relationships_required": [],
            "aggregation": {"function": "COUNT", "expression": "accused.AccusedMasterID"}
        },
        "chat_history": chat_hist_7
    }
    validated_state_7 = await schema_validator_node(state_7)
    plan_7 = validated_state_7["query_plan"]
    assert any(f.get("value") == "KSP-CASE-0004" for f in plan_7["filters"]), "Test 7 failed: Context case filter not present"
    
    sql_7 = (
        "SELECT COUNT(accused.AccusedMasterID) AS accused_count "
        "FROM casemaster "
        "JOIN accused ON casemaster.CaseMasterID = accused.CaseMasterID "
        "WHERE casemaster.CaseNo = 'KSP-CASE-0004'"
    )
    exec_state_7 = await execute_sql_node({**validated_state_7, "generated_sql": sql_7})
    print(f"  SQL: {sql_7}")
    print(f"  Result: {exec_state_7['sql_results'][0] if exec_state_7['sql_results'] else 'None'}")
    assert exec_state_7["sql_results_total"] > 0, "Test 7 failed: No rows returned"
    print("  -> TEST 7 PASSED [OK]")

    # -------------------------------------------------------------
    # TEST 8: Turn 1: "Show KSP-CASE-0004." -> Turn 2: "How many cases are there?"
    # -------------------------------------------------------------
    print("\n[TEST 8] Global Count Override: Turn 1: 'Show KSP-CASE-0004.' -> Turn 2: 'How many cases are there?'")
    chat_hist_8 = [
        {"role": "user", "content": "Show KSP-CASE-0004."},
        {"role": "assistant", "content": "Here are the details for KSP-CASE-0004."}
    ]
    ctx_8 = resolve_conversation_context("How many cases are there?", chat_hist_8)
    print(f"  Context State: active_case={ctx_8['active_case']}, is_global={ctx_8['is_global_query']}")
    assert ctx_8["is_global_query"] is True, "Test 8 failed: Global query not detected"
    assert ctx_8["active_case"] is None, "Test 8 failed: active_case was not suppressed for global query"
    
    state_8 = {
        "user_query": "How many cases are there?",
        "queries": ["How many cases are there?"],
        "current_query_index": 0,
        "context_state": ctx_8,
        "query_plan": {
            "intent": "count_cases",
            "target_tables": ["casemaster"],
            "ambiguous": False,
            "clarification_question": "",
            "entities": {"case_no": None, "person_name": None, "station_name": None},
            "filters": [],
            "requested_fields": ["COUNT(*) AS total_cases"],
            "relationships_required": [],
            "aggregation": {"function": "COUNT", "expression": "*"}
        },
        "chat_history": chat_hist_8
    }
    validated_state_8 = await schema_validator_node(state_8)
    plan_8 = validated_state_8["query_plan"]
    assert len(plan_8["filters"]) == 0, "Test 8 failed: Global query must not have filters"
    
    sql_8 = "SELECT COUNT(*) AS total_cases FROM casemaster"
    exec_state_8 = await execute_sql_node({**validated_state_8, "generated_sql": sql_8})
    print(f"  SQL: {sql_8}")
    print(f"  Result: {exec_state_8['sql_results'][0] if exec_state_8['sql_results'] else 'None'}")
    assert exec_state_8["sql_results_total"] > 0, "Test 8 failed: No rows returned"
    print("  -> TEST 8 PASSED [OK]")

    # -------------------------------------------------------------
    # LIVE END-TO-END TEST: StateGraph Execution on Analytics Query
    # -------------------------------------------------------------
    print("\n[LIVE END-TO-END TEST] Running live workflow execution against Railway MySQL...")
    live_input = {
        "user_query": "Show the top 3 police stations by number of cases",
        "chat_history": []
    }
    live_result = await agent_app.ainvoke(live_input, config={"configurable": {"thread_id": "phase4_live_thread"}})
    print("  Live Graph Result:")
    print(f"  Target Tables: {live_result.get('query_plan', {}).get('target_tables')}")
    print(f"  Generated SQL: {live_result.get('generated_sql')}")
    print(f"  Rows Returned: {live_result.get('sql_results_total')}")
    print(f"  Summary Preview: {live_result.get('analytical_summary', '')[:200]}...")
    assert live_result.get("sql_results_total", 0) > 0 or live_result.get("all_sql_results", [[]])[0], "Live analytics test returned 0 rows"
    print("  -> LIVE END-TO-END TEST PASSED [OK]")

    print("\n" + "=" * 80)
    print("ALL PHASE 4 ANALYTICS & DATA INSIGHTS TESTS PASSED WITH 0 ERRORS!")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(run_phase4_tests())

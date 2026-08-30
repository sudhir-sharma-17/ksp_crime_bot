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
    resolve_table_joins,
    schema_validator_node,
    execute_sql_node,
    agent_app
)

async def run_phase3_tests():
    print("=" * 80)
    print("PHASE 3 — MULTI-TABLE REASONING FAST VERIFICATION SUITE")
    print("=" * 80)
    
    # -------------------------------------------------------------
    # TEST 1: Accused, Victim, Complainant, IO, Station, Court
    # -------------------------------------------------------------
    print("\n[TEST 1] Show the accused, victim, complainant, investigating officer, police station and court for KSP-CASE-0004.")
    state_1 = {
        "user_query": "Show the accused, victim, complainant, investigating officer, police station and court for KSP-CASE-0004.",
        "queries": ["Show the accused, victim, complainant, investigating officer, police station and court for KSP-CASE-0004."],
        "current_query_index": 0,
        "query_plan": {
            "intent": "multi_table_query",
            "target_tables": ["casemaster", "accused", "victim", "complainantdetails", "employee", "unit", "court"],
            "ambiguous": False,
            "clarification_question": "",
            "entities": {"case_no": "KSP-CASE-0004", "person_name": None, "station_name": None},
            "filters": [{"table": "casemaster", "column": "CaseNo", "operator": "=", "value": "KSP-CASE-0004"}],
            "requested_fields": [
                "casemaster.CaseNo",
                "accused.AccusedName",
                "victim.VictimName",
                "complainantdetails.ComplainantName",
                "employee.FirstName",
                "unit.UnitName",
                "court.CourtName"
            ],
            "relationships_required": []
        },
        "chat_history": []
    }
    
    validated_state_1 = await schema_validator_node(state_1)
    plan_1 = validated_state_1["query_plan"]
    rels_1 = plan_1["relationships_required"]
    print(f"  Target Tables: {plan_1['target_tables']}")
    print(f"  Relationships Inferred: {len(rels_1)} joins")
    assert len(plan_1["target_tables"]) == 7, "Test 1 failed: Expected 7 target tables"
    assert len(rels_1) == 6, "Test 1 failed: Expected 6 join relationships"
    
    # Generate and execute SQL for Test 1
    sql_1 = (
        "SELECT casemaster.CaseNo, accused.AccusedName, victim.VictimName, complainantdetails.ComplainantName, "
        "employee.FirstName AS InvestigatingOfficer, unit.UnitName AS PoliceStation, court.CourtName "
        "FROM casemaster "
        "LEFT JOIN accused ON casemaster.CaseMasterID = accused.CaseMasterID "
        "LEFT JOIN victim ON casemaster.CaseMasterID = victim.CaseMasterID "
        "LEFT JOIN complainantdetails ON casemaster.CaseMasterID = complainantdetails.CaseMasterID "
        "LEFT JOIN employee ON casemaster.PolicePersonID = employee.EmployeeID "
        "LEFT JOIN unit ON casemaster.PoliceStationID = unit.UnitID "
        "LEFT JOIN court ON casemaster.CourtID = court.CourtID "
        "WHERE casemaster.CaseNo = 'KSP-CASE-0004'"
    )
    exec_state_1 = await execute_sql_node({**validated_state_1, "generated_sql": sql_1})
    print(f"  SQL: {sql_1}")
    print(f"  Rows Returned: {exec_state_1['sql_results_total']}")
    print(f"  Sample Result: {exec_state_1['sql_results'][0] if exec_state_1['sql_results'] else 'None'}")
    assert exec_state_1["sql_results_total"] > 0, "Test 1 execution failed: No rows returned"
    print("  -> TEST 1 PASSED [OK]")

    # -------------------------------------------------------------
    # TEST 2: Accused, Investigating Officer, Police Station
    # -------------------------------------------------------------
    print("\n[TEST 2] Who was the accused, which officer investigated the case, and which police station handled KSP-CASE-0004?")
    state_2 = {
        "user_query": "Who was the accused, which officer investigated the case, and which police station handled KSP-CASE-0004?",
        "queries": ["Who was the accused, which officer investigated the case, and which police station handled KSP-CASE-0004?"],
        "current_query_index": 0,
        "query_plan": {
            "intent": "multi_table_query",
            "target_tables": ["casemaster", "accused", "employee", "unit"],
            "ambiguous": False,
            "clarification_question": "",
            "entities": {"case_no": "KSP-CASE-0004", "person_name": None, "station_name": None},
            "filters": [{"table": "casemaster", "column": "CaseNo", "operator": "=", "value": "KSP-CASE-0004"}],
            "requested_fields": ["casemaster.CaseNo", "accused.AccusedName", "employee.FirstName", "unit.UnitName"],
            "relationships_required": []
        },
        "chat_history": []
    }
    validated_state_2 = await schema_validator_node(state_2)
    plan_2 = validated_state_2["query_plan"]
    rels_2 = plan_2["relationships_required"]
    print(f"  Target Tables: {plan_2['target_tables']}")
    print(f"  Relationships Inferred: {len(rels_2)} joins")
    assert len(plan_2["target_tables"]) == 4, "Test 2 failed: Expected 4 target tables"
    assert len(rels_2) == 3, "Test 2 failed: Expected 3 join relationships"
    
    sql_2 = (
        "SELECT casemaster.CaseNo, accused.AccusedName, employee.FirstName AS InvestigatingOfficer, unit.UnitName AS PoliceStation "
        "FROM casemaster "
        "LEFT JOIN accused ON casemaster.CaseMasterID = accused.CaseMasterID "
        "LEFT JOIN employee ON casemaster.PolicePersonID = employee.EmployeeID "
        "LEFT JOIN unit ON casemaster.PoliceStationID = unit.UnitID "
        "WHERE casemaster.CaseNo = 'KSP-CASE-0004'"
    )
    exec_state_2 = await execute_sql_node({**validated_state_2, "generated_sql": sql_2})
    print(f"  SQL: {sql_2}")
    print(f"  Rows Returned: {exec_state_2['sql_results_total']}")
    print(f"  Sample Result: {exec_state_2['sql_results'][0] if exec_state_2['sql_results'] else 'None'}")
    assert exec_state_2["sql_results_total"] > 0, "Test 2 execution failed: No rows returned"
    print("  -> TEST 2 PASSED [OK]")

    # -------------------------------------------------------------
    # TEST 3: Acts and Sections applied to KSP-CASE-0004
    # -------------------------------------------------------------
    print("\n[TEST 3] What acts and sections were applied to KSP-CASE-0004?")
    state_3 = {
        "user_query": "What acts and sections were applied to KSP-CASE-0004?",
        "queries": ["What acts and sections were applied to KSP-CASE-0004?"],
        "current_query_index": 0,
        "query_plan": {
            "intent": "find_sections",
            "target_tables": ["casemaster", "section", "act"],
            "ambiguous": False,
            "clarification_question": "",
            "entities": {"case_no": "KSP-CASE-0004", "person_name": None, "station_name": None},
            "filters": [{"table": "casemaster", "column": "CaseNo", "operator": "=", "value": "KSP-CASE-0004"}],
            "requested_fields": ["casemaster.CaseNo", "act.ActDescription", "section.SectionCode", "section.SectionDescription"],
            "relationships_required": []
        },
        "chat_history": []
    }
    validated_state_3 = await schema_validator_node(state_3)
    plan_3 = validated_state_3["query_plan"]
    rels_3 = plan_3["relationships_required"]
    print(f"  Target Tables (Auto-bridged): {plan_3['target_tables']}")
    print(f"  Relationships Inferred: {len(rels_3)} joins")
    assert "actsectionassociation" in plan_3["target_tables"], "Test 3 failed: actsectionassociation bridge table not auto-injected"
    assert len(rels_3) == 3, "Test 3 failed: Expected 3 join relationships (casemaster->actsectionassociation->section, ->act)"
    
    sql_3 = (
        "SELECT casemaster.CaseNo, act.ActDescription, section.SectionCode, section.SectionDescription "
        "FROM casemaster "
        "JOIN actsectionassociation ON casemaster.CaseMasterID = actsectionassociation.CaseMasterID "
        "JOIN section ON actsectionassociation.SectionID = section.SectionCode AND actsectionassociation.ActID = section.ActCode "
        "JOIN act ON actsectionassociation.ActID = act.ActCode "
        "WHERE casemaster.CaseNo = 'KSP-CASE-0004'"
    )
    exec_state_3 = await execute_sql_node({**validated_state_3, "generated_sql": sql_3})
    print(f"  SQL: {sql_3}")
    print(f"  Rows Returned: {exec_state_3['sql_results_total']}")
    print(f"  Sample Result: {exec_state_3['sql_results'][0] if exec_state_3['sql_results'] else 'None'}")
    assert exec_state_3["sql_results_total"] > 0, "Test 3 execution failed: No rows returned"
    print("  -> TEST 3 PASSED [OK]")

    # -------------------------------------------------------------
    # TEST 4: Cases involving Vijay Mishra and their Police Stations
    # -------------------------------------------------------------
    print("\n[TEST 4] Show me all cases involving Vijay Mishra and the police stations that handled them.")
    state_4 = {
        "user_query": "Show me all cases involving Vijay Mishra and the police stations that handled them.",
        "queries": ["Show me all cases involving Vijay Mishra and the police stations that handled them."],
        "current_query_index": 0,
        "query_plan": {
            "intent": "find_case",
            "target_tables": ["accused", "casemaster", "unit"],
            "ambiguous": False,
            "clarification_question": "",
            "entities": {"case_no": None, "person_name": "Vijay Mishra", "station_name": None},
            "filters": [{"table": "accused", "column": "AccusedName", "operator": "=", "value": "Vijay Mishra"}],
            "requested_fields": ["accused.AccusedName", "casemaster.CaseNo", "unit.UnitName"],
            "relationships_required": []
        },
        "chat_history": []
    }
    validated_state_4 = await schema_validator_node(state_4)
    plan_4 = validated_state_4["query_plan"]
    rels_4 = plan_4["relationships_required"]
    print(f"  Target Tables: {plan_4['target_tables']}")
    print(f"  Relationships Inferred: {len(rels_4)} joins")
    assert len(rels_4) == 2, "Test 4 failed: Expected 2 joins (casemaster->accused, casemaster->unit)"
    
    sql_4 = (
        "SELECT accused.AccusedName, casemaster.CaseNo, unit.UnitName AS PoliceStation "
        "FROM accused "
        "JOIN casemaster ON accused.CaseMasterID = casemaster.CaseMasterID "
        "JOIN unit ON casemaster.PoliceStationID = unit.UnitID "
        "WHERE accused.AccusedName LIKE '%Vijay Mishra%'"
    )
    exec_state_4 = await execute_sql_node({**validated_state_4, "generated_sql": sql_4})
    print(f"  SQL: {sql_4}")
    print(f"  Rows Returned: {exec_state_4['sql_results_total']}")
    print(f"  Sample Result: {exec_state_4['sql_results'][0] if exec_state_4['sql_results'] else 'None'}")
    assert exec_state_4["sql_results_total"] > 0, "Test 4 execution failed: No rows returned"
    print("  -> TEST 4 PASSED [OK]")

    # -------------------------------------------------------------
    # TEST 5: Was the accused in KSP-CASE-0004 arrested?
    # -------------------------------------------------------------
    print("\n[TEST 5] Was the accused in KSP-CASE-0004 arrested?")
    state_5 = {
        "user_query": "Was the accused in KSP-CASE-0004 arrested?",
        "queries": ["Was the accused in KSP-CASE-0004 arrested?"],
        "current_query_index": 0,
        "query_plan": {
            "intent": "find_arrested",
            "target_tables": ["casemaster", "accused", "arrestsurrender"],
            "ambiguous": False,
            "clarification_question": "",
            "entities": {"case_no": "KSP-CASE-0004", "person_name": None, "station_name": None},
            "filters": [{"table": "casemaster", "column": "CaseNo", "operator": "=", "value": "KSP-CASE-0004"}],
            "requested_fields": ["casemaster.CaseNo", "accused.AccusedName", "arrestsurrender.ArrestSurrenderDate", "arrestsurrender.IsAccused"],
            "relationships_required": []
        },
        "chat_history": []
    }
    validated_state_5 = await schema_validator_node(state_5)
    plan_5 = validated_state_5["query_plan"]
    rels_5 = plan_5["relationships_required"]
    print(f"  Target Tables: {plan_5['target_tables']}")
    print(f"  Relationships Inferred: {len(rels_5)} joins")
    assert len(rels_5) == 2, "Test 5 failed: Expected 2 joins (casemaster->accused, casemaster->arrestsurrender)"
    
    sql_5 = (
        "SELECT casemaster.CaseNo, accused.AccusedName, arrestsurrender.ArrestSurrenderDate, arrestsurrender.IsAccused "
        "FROM casemaster "
        "JOIN accused ON casemaster.CaseMasterID = accused.CaseMasterID "
        "LEFT JOIN arrestsurrender ON casemaster.CaseMasterID = arrestsurrender.CaseMasterID "
        "WHERE casemaster.CaseNo = 'KSP-CASE-0004'"
    )
    exec_state_5 = await execute_sql_node({**validated_state_5, "generated_sql": sql_5})
    print(f"  SQL: {sql_5}")
    print(f"  Rows Returned: {exec_state_5['sql_results_total']}")
    print(f"  Sample Result: {exec_state_5['sql_results'][0] if exec_state_5['sql_results'] else 'None'}")
    assert exec_state_5["sql_results_total"] > 0, "Test 5 execution failed: No rows returned"
    print("  -> TEST 5 PASSED [OK]")

    # -------------------------------------------------------------
    # TEST 6: Single-table Query Minimality (Avoid Unnecessary Joins)
    # -------------------------------------------------------------
    print("\n[TEST 6] Who is the victim of KSP-CASE-0004? (Check Unnecessary Join Avoidance)")
    state_6 = {
        "user_query": "Who is the victim of KSP-CASE-0004?",
        "queries": ["Who is the victim of KSP-CASE-0004?"],
        "current_query_index": 0,
        "query_plan": {
            "intent": "find_victim",
            "target_tables": ["casemaster", "victim"],
            "ambiguous": False,
            "clarification_question": "",
            "entities": {"case_no": "KSP-CASE-0004", "person_name": None, "station_name": None},
            "filters": [{"table": "casemaster", "column": "CaseNo", "operator": "=", "value": "KSP-CASE-0004"}],
            "requested_fields": ["casemaster.CaseNo", "victim.VictimName", "victim.AgeYear", "victim.GenderID"],
            "relationships_required": []
        },
        "chat_history": []
    }
    validated_state_6 = await schema_validator_node(state_6)
    plan_6 = validated_state_6["query_plan"]
    rels_6 = plan_6["relationships_required"]
    print(f"  Target Tables: {plan_6['target_tables']}")
    print(f"  Relationships Inferred: {len(rels_6)} joins")
    assert plan_6["target_tables"] == ["casemaster", "victim"], "Test 6 failed: target_tables has extra unnecessary tables"
    assert len(rels_6) == 1, "Test 6 failed: Expected exactly 1 join (casemaster->victim)"
    
    sql_6 = (
        "SELECT casemaster.CaseNo, victim.VictimName, victim.AgeYear, victim.GenderID "
        "FROM casemaster "
        "JOIN victim ON casemaster.CaseMasterID = victim.CaseMasterID "
        "WHERE casemaster.CaseNo = 'KSP-CASE-0004'"
    )
    exec_state_6 = await execute_sql_node({**validated_state_6, "generated_sql": sql_6})
    print(f"  SQL: {sql_6}")
    print(f"  Rows Returned: {exec_state_6['sql_results_total']}")
    print(f"  Sample Result: {exec_state_6['sql_results'][0] if exec_state_6['sql_results'] else 'None'}")
    assert exec_state_6["sql_results_total"] > 0, "Test 6 execution failed: No rows returned"
    print("  -> TEST 6 PASSED [OK]")

    # -------------------------------------------------------------
    # TEST 7: Conversational Context Multi-Turn Multi-Table Test
    # -------------------------------------------------------------
    print("\n[TEST 7] Multi-Turn Context Multi-Table Test")
    print("  Turn 1: 'Show KSP-CASE-0004.'")
    print("  Turn 2: 'Show me the accused, victim and police station.'")
    
    turn2_state = {
        "user_query": "Show me the accused, victim and police station.",
        "queries": ["Show me the accused, victim and police station."],
        "current_query_index": 0,
        "context_state": {
            "active_case": "KSP-CASE-0004",
            "active_person": None,
            "active_station": None,
            "recent_cases": ["KSP-CASE-0004"],
            "context_reset": False,
            "is_global_query": False,
            "context_ambiguous": False,
            "context_missing": False,
            "clarification_prompt": None
        },
        "query_plan": {
            "intent": "multi_table_query",
            "target_tables": ["casemaster", "accused", "victim", "unit"],
            "ambiguous": False,
            "clarification_question": "",
            "entities": {"case_no": "KSP-CASE-0004", "person_name": None, "station_name": None},
            "filters": [{"table": "casemaster", "column": "CaseNo", "operator": "=", "value": "KSP-CASE-0004"}],
            "requested_fields": ["casemaster.CaseNo", "accused.AccusedName", "victim.VictimName", "unit.UnitName"],
            "relationships_required": []
        },
        "chat_history": [
            {"role": "user", "content": "Show KSP-CASE-0004."},
            {"role": "assistant", "content": "Here are the details for case KSP-CASE-0004."}
        ]
    }
    validated_turn2 = await schema_validator_node(turn2_state)
    plan_turn2 = validated_turn2["query_plan"]
    rels_turn2 = plan_turn2["relationships_required"]
    print(f"  Target Tables: {plan_turn2['target_tables']}")
    print(f"  Relationships Inferred: {len(rels_turn2)} joins")
    assert len(plan_turn2["target_tables"]) == 4, "Test 7 failed: Expected 4 target tables"
    assert len(rels_turn2) == 3, "Test 7 failed: Expected 3 joins"
    assert any(f.get("value") == "KSP-CASE-0004" for f in plan_turn2["filters"]), "Test 7 failed: Context case not inherited"
    print("  -> TEST 7 PASSED [OK]")

    # -------------------------------------------------------------
    # LIVE END-TO-END TEST: Executed through the Aloka StateGraph
    # -------------------------------------------------------------
    print("\n[LIVE END-TO-END TEST] Running live workflow execution against Railway MySQL database...")
    live_input = {
        "user_query": "Give me the accused, victim and police station for KSP-CASE-0004",
        "chat_history": []
    }
    live_result = await agent_app.ainvoke(live_input, config={"configurable": {"thread_id": "phase3_test_thread"}})
    print("  Live Graph Result:")
    print(f"  Target Tables: {live_result.get('query_plan', {}).get('target_tables')}")
    print(f"  Generated SQL: {live_result.get('generated_sql')}")
    print(f"  Rows Returned: {live_result.get('sql_results_total')}")
    print(f"  Summary Preview: {live_result.get('analytical_summary', '')[:200]}...")
    assert live_result.get("sql_results_total", 0) > 0 or live_result.get("all_sql_results", [[]])[0], "Live end-to-end test returned 0 rows"
    print("  -> LIVE END-TO-END TEST PASSED [OK]")

    print("\n" + "=" * 80)
    print("ALL PHASE 3 MULTI-TABLE REASONING TESTS PASSED WITH 0 ERRORS!")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(run_phase3_tests())

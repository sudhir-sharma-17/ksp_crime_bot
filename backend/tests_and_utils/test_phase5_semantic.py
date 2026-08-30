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

from app.semantic_search import semantic_index, is_semantic_search_query
from app.agent import semantic_search_node, agent_app

async def run_phase5_tests():
    print("=" * 80)
    print("PHASE 5 — SEMANTIC SEARCH OVER BRIEF FACTS FAST VERIFICATION SUITE")
    print("=" * 80)

    # Build / load index once
    num_indexed = semantic_index.build_index()
    print(f"\n[SEMANTIC INDEX] Total case records indexed: {num_indexed}")
    assert num_indexed > 0, "Semantic index failed to build"

    # -------------------------------------------------------------
    # TEST 1: "Find cases involving phishing."
    # -------------------------------------------------------------
    print("\n[TEST 1] 'Find cases involving phishing.'")
    q1 = "Find cases involving phishing."
    is_sem_1 = is_semantic_search_query(q1)
    print(f"  Intent: Semantic Search Detected = {is_sem_1}")
    assert is_sem_1 is True, "Test 1 failed: Semantic search intent not detected"
    
    r1 = semantic_index.search(q1, top_k=5)
    print(f"  Matches Found: {len(r1)}")
    for c in r1[:2]:
        print(f"    - Case: {c['CaseNo']} | Relevance: {c['relevance_level']} ({c['relevance_score']}) | Facts: {c['BriefFacts'][:100]}...")
    assert len(r1) > 0, "Test 1 failed: No cases returned"
    assert any("phishing" in c["BriefFacts"].lower() or "sms" in c["BriefFacts"].lower() or "link" in c["BriefFacts"].lower() for c in r1), "Test 1 failed: BriefFacts do not match phishing"
    print("  -> TEST 1 PASSED [OK]")

    # -------------------------------------------------------------
    # TEST 2: "Find cases where victims lost money through a fake link or message."
    # -------------------------------------------------------------
    print("\n[TEST 2] 'Find cases where victims lost money through a fake link or message.'")
    q2 = "Find cases where victims lost money through a fake link or message."
    is_sem_2 = is_semantic_search_query(q2)
    print(f"  Intent: Semantic Search Detected = {is_sem_2}")
    assert is_sem_2 is True, "Test 2 failed: Semantic search intent not detected"
    
    r2 = semantic_index.search(q2, top_k=5)
    print(f"  Matches Found: {len(r2)}")
    for c in r2[:2]:
        print(f"    - Case: {c['CaseNo']} | Relevance: {c['relevance_level']} ({c['relevance_score']}) | Facts: {c['BriefFacts'][:100]}...")
    assert len(r2) > 0, "Test 2 failed: No cases returned"
    print("  -> TEST 2 PASSED [OK]")

    # -------------------------------------------------------------
    # TEST 3: "Find cases related to online financial fraud."
    # -------------------------------------------------------------
    print("\n[TEST 3] 'Find cases related to online financial fraud.'")
    q3 = "Find cases related to online financial fraud."
    is_sem_3 = is_semantic_search_query(q3)
    print(f"  Intent: Semantic Search Detected = {is_sem_3}")
    assert is_sem_3 is True, "Test 3 failed: Semantic search intent not detected"
    
    r3 = semantic_index.search(q3, top_k=5)
    print(f"  Matches Found: {len(r3)}")
    for c in r3[:2]:
        print(f"    - Case: {c['CaseNo']} | Relevance: {c['relevance_level']} ({c['relevance_score']}) | Facts: {c['BriefFacts'][:100]}...")
    assert len(r3) > 0, "Test 3 failed: No cases returned"
    print("  -> TEST 3 PASSED [OK]")

    # -------------------------------------------------------------
    # TEST 4: "Find cases involving fraudulent SMS messages."
    # -------------------------------------------------------------
    print("\n[TEST 4] 'Find cases involving fraudulent SMS messages.'")
    q4 = "Find cases involving fraudulent SMS messages."
    is_sem_4 = is_semantic_search_query(q4)
    print(f"  Intent: Semantic Search Detected = {is_sem_4}")
    assert is_sem_4 is True, "Test 4 failed: Semantic search intent not detected"
    
    r4 = semantic_index.search(q4, top_k=5)
    print(f"  Matches Found: {len(r4)}")
    for c in r4[:2]:
        print(f"    - Case: {c['CaseNo']} | Relevance: {c['relevance_level']} ({c['relevance_score']}) | Facts: {c['BriefFacts'][:100]}...")
    assert len(r4) > 0, "Test 4 failed: No cases returned"
    print("  -> TEST 4 PASSED [OK]")

    # -------------------------------------------------------------
    # TEST 5: "Find phishing cases registered in 2024." (Hybrid Search)
    # -------------------------------------------------------------
    print("\n[TEST 5] 'Find phishing cases registered in 2024.' (Hybrid Search)")
    q5 = "Find phishing cases registered in 2024."
    is_sem_5 = is_semantic_search_query(q5)
    print(f"  Intent: Semantic Search Detected = {is_sem_5}")
    assert is_sem_5 is True, "Test 5 failed: Semantic search intent not detected"
    
    r5 = semantic_index.search(q5, top_k=5, filters={"year": "2024"})
    print(f"  Matches Found: {len(r5)}")
    for c in r5[:2]:
        print(f"    - Case: {c['CaseNo']} | Date: {c.get('CrimeRegisteredDate')} | Relevance: {c['relevance_level']} | Facts: {c['BriefFacts'][:100]}...")
    assert len(r5) > 0, "Test 5 failed: No cases returned"
    for c in r5:
        assert "2024" in str(c.get("CrimeRegisteredDate")), f"Test 5 failed: Result {c['CaseNo']} not from year 2024"
    print("  -> TEST 5 PASSED [OK]")

    # -------------------------------------------------------------
    # TEST 6: Structured SQL Non-Interference Check
    # -------------------------------------------------------------
    print("\n[TEST 6] 'Who is the victim of KSP-CASE-0004?' (Ensure Structured SQL Path is Preserved)")
    q6 = "Who is the victim of KSP-CASE-0004?"
    is_sem_6 = is_semantic_search_query(q6)
    print(f"  Is Semantic Search Query: {is_sem_6}")
    assert is_sem_6 is False, "Test 6 failed: Structured SQL query wrongly classified as semantic search"
    print("  -> TEST 6 PASSED [OK] (Correctly routed to Text-to-SQL pipeline)")

    # -------------------------------------------------------------
    # LIVE END-TO-END WORKFLOW TEST: Semantic Search via LangGraph
    # -------------------------------------------------------------
    print("\n[LIVE END-TO-END TEST] Executing Semantic Search through Aloka LangGraph Engine...")
    live_input = {
        "user_query": "Find cases involving phishing and fake links where victims lost money",
        "chat_history": []
    }
    live_result = await agent_app.ainvoke(live_input, config={"configurable": {"thread_id": "phase5_semantic_thread"}})
    print("  Live Result:")
    print(f"  Generated Action: {live_result.get('generated_sql')}")
    print(f"  Matches Returned: {live_result.get('sql_results_total')}")
    print(f"  Summary Preview: {live_result.get('analytical_summary', '')[:250]}...")
    assert live_result.get("sql_results_total", 0) > 0 or live_result.get("all_sql_results", [[]])[0], "Live semantic test returned 0 results"
    print("  -> LIVE END-TO-END TEST PASSED [OK]")

    print("\n" + "=" * 80)
    print("ALL PHASE 5 SEMANTIC SEARCH TESTS PASSED WITH 0 ERRORS!")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(run_phase5_tests())

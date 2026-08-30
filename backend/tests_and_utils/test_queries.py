import os
import sys
import asyncio

# Ensure backend directory is in sys.path to allow absolute imports
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, backend_path)

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from app.agent import agent_app

async def run_dialog(thread_id: str, steps: list):
    print(f"\n" + "="*80)
    print(f"RUNNING DIALOG SUITE: {thread_id}")
    print("="*80)
    
    chat_history = []
    
    for i, user_msg in enumerate(steps, 1):
        print(f"\n[Turn {i}] User: '{user_msg}'")
        res = await agent_app.ainvoke(
            {
                "user_query": user_msg,
                "user_role": "Investigator",
                "language_preference": "English",
                "chat_history": chat_history
            },
            config={"configurable": {"thread_id": f"thread_{thread_id}"}}
        )
        
        ctx = res.get("context_state", {}) or {}
        plan = res.get("query_plan", {}) or {}
        
        active_case = ctx.get("active_case")
        is_global = ctx.get("is_global_query")
        ambiguous = plan.get("ambiguous", False)
        
        print(f"  Context -> Active Case: {active_case} | Is Global: {is_global} | Ambiguous: {ambiguous}")
        
        if ambiguous:
            summary = res.get("analytical_summary", "")
            print(f"  Clarification Question Generated:\n  '{summary}'")
        else:
            sqls = res.get("all_generated_sql", [])
            sql_str = sqls[0] if sqls else res.get("generated_sql", "")
            print(f"  Generated SQL: {sql_str}")
            
            rows = res.get("all_sql_results", [[]])[0]
            print(f"  Rows Returned: {len(rows)}")
            if rows:
                print(f"  Sample Result: {rows[0]}")
            print(f"  Aloka Response:\n  {res.get('analytical_summary', '')[:200]}...")
            
        chat_history.append({"role": "user", "content": user_msg})
        chat_history.append({"role": "assistant", "content": res.get("analytical_summary", "")})
        print("-" * 80)


async def main():
    # Suite A: Basic Case Context
    await run_dialog("Suite_A_BasicContext", [
        "Show KSP-CASE-0004.",
        "Who are the accused?"
    ])

    # Suite B: Multiple Follow-ups
    await run_dialog("Suite_B_MultipleFollowups", [
        "Show KSP-CASE-0004.",
        "Who is the victim?",
        "What happened?",
        "Which court?",
        "Which police station?",
        "Who was the investigating officer?"
    ])

    # Suite C: Context Switching
    await run_dialog("Suite_C_ContextSwitching", [
        "Show KSP-CASE-0004.",
        "Who is the victim?",
        "Now show KSP-CASE-0012.",
        "Who is the victim?"
    ])

    # Suite D: Global Query (Excludes Active Case)
    await run_dialog("Suite_D_GlobalQueryExclusion", [
        "Show KSP-CASE-0004.",
        "How many cases are there?"
    ])

    # Suite E: Pronoun Resolution
    await run_dialog("Suite_E_PronounResolution", [
        "Show KSP-CASE-0004.",
        "What happened in this case?"
    ])

    # Suite F: Multi-Case Ambiguity Detection
    await run_dialog("Suite_F_MultiCaseAmbiguity", [
        "Show KSP-CASE-0004.",
        "Show KSP-CASE-0012.",
        "What happened in that case?"
    ])

    # Suite G: Explicit Context Reset
    await run_dialog("Suite_G_ExplicitReset", [
        "Show KSP-CASE-0004.",
        "Forget that case.",
        "What happened?"
    ])

    # Suite H: Phase 1 Regression Suite (Single Scenarios A to M)
    print("\n" + "="*80)
    print("PART H: PHASE 1 REGRESSION SUITE (14 SCENARIOS)")
    print("="*80)
    
    p1_scenarios = [
        ("A", "Find case KSP-CASE-0004"),
        ("B", "Who are the people accused in case KSP-CASE-0004?"),
        ("C", "Who are the victims in case KSP-CASE-0004?"),
        ("D", "Who filed the complaint?"),
        ("E", "Which officer registered the FIR?"),
        ("F", "Which police station registered the case?"),
        ("G", "What happened in this case?"),
        ("H", "How many cases are there?"),
        ("I", "Show me the cases involving Vijay Mishra"),
        ("J", "Who was arrested in case KSP-CASE-0004?"),
        ("K", "Which court is handling this case?"),
        ("L", "What sections were applied?"),
        ("M", "Who is Ravi's case?")
    ]
    
    for tag, q in p1_scenarios:
        res = await agent_app.ainvoke(
            {"user_query": q, "user_role": "Investigator", "language_preference": "English", "chat_history": []},
            config={"configurable": {"thread_id": f"reg_{tag}"}}
        )
        plan = res.get("query_plan", {}) or {}
        print(f"[{tag}] '{q}' -> Intent: {plan.get('intent')} | Ambiguous: {plan.get('ambiguous')}")

if __name__ == "__main__":
    asyncio.run(main())

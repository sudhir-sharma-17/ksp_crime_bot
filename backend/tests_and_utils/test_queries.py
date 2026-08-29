import os
import sys
import asyncio

# Ensure backend directory is in sys.path to allow absolute imports
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, backend_path)

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from app.agent import agent_app

single_scenarios = [
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
    ("M", "Who is Ravi's case?")  # Ambiguity test -> should ask for clarification
]

conversation_scenario_N = [
    "Show case KSP-CASE-0004.",
    "Who are the accused?",
    "Was anyone arrested?"
]

async def run_single_scenarios():
    print("="*80)
    print("PART 1: TESTING SCENARIOS A THROUGH M")
    print("="*80)
    
    results_summary = []
    
    for tag, query in single_scenarios:
        print(f"\n[{tag}] Query: '{query}'")
        try:
            res = await agent_app.ainvoke(
                {
                    "user_query": query,
                    "user_role": "Investigator",
                    "language_preference": "English",
                    "chat_history": []
                },
                config={"configurable": {"thread_id": f"thread_{tag}"}}
            )
            
            plan = res.get("query_plan", {})
            print(f"  Plan Intent: {plan.get('intent')} | Ambiguous: {plan.get('ambiguous')}")
            if plan.get("ambiguous"):
                print(f"  Clarification Prompt: {res.get('analytical_summary')}")
                results_summary.append((tag, query, "CLARIFICATION PROMPT (SUCCESS)", None))
            else:
                sqls = res.get("all_generated_sql", [])
                sql_str = sqls[0] if sqls else res.get("generated_sql", "")
                print(f"  Generated SQL: {sql_str}")
                
                rows = res.get("all_sql_results", [[]])[0]
                row_count = len(rows)
                print(f"  Rows Returned: {row_count}")
                if rows:
                    print(f"  Sample Row: {rows[0]}")
                print(f"  Summary Headline:\n{res.get('analytical_summary', '')[:200]}...")
                results_summary.append((tag, query, "SUCCESS", sql_str))
        except Exception as e:
            print(f"  [FAIL] Exception: {e}")
            results_summary.append((tag, query, f"FAILED: {e}", None))
            
        print("-" * 80)
        
    return results_summary


async def run_conversation_scenario_N():
    print("\n" + "="*80)
    print("PART 2: TESTING MULTI-TURN CONVERSATIONAL SCENARIO N")
    print("="*80)
    
    chat_history = []
    thread_id = "thread_scenario_N"
    
    for step_idx, user_msg in enumerate(conversation_scenario_N, 1):
        print(f"\n[Turn {step_idx}] User: '{user_msg}'")
        res = await agent_app.ainvoke(
            {
                "user_query": user_msg,
                "user_role": "Investigator",
                "language_preference": "English",
                "chat_history": chat_history
            },
            config={"configurable": {"thread_id": thread_id}}
        )
        
        plan = res.get("query_plan", {})
        print(f"  Resolved Case No from Context: {plan.get('entities', {}).get('case_no')}")
        sqls = res.get("all_generated_sql", [])
        sql_str = sqls[0] if sqls else res.get("generated_sql", "")
        print(f"  Generated SQL: {sql_str}")
        
        rows = res.get("all_sql_results", [[]])[0]
        print(f"  Rows Returned: {len(rows)}")
        if rows:
            print(f"  Sample Row: {rows[0]}")
            
        summary = res.get("analytical_summary", "")
        print(f"  Aloka Response:\n{summary[:250]}...")
        
        # Update chat history for next turn
        chat_history.append({"role": "user", "content": user_msg})
        chat_history.append({"role": "assistant", "content": summary})
        print("-" * 80)

async def main():
    await run_single_scenarios()
    await run_conversation_scenario_N()

if __name__ == "__main__":
    asyncio.run(main())

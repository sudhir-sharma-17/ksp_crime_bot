import os
import sys
import asyncio

# Ensure backend directory is in sys.path to allow absolute imports
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, backend_path)

# Set standard output encoding to UTF-8 to prevent CP1252 encoding crashes on Windows console
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from app.agent import agent_app

test_queries = [
    "Find case KSP-CASE-0004",
    "Show the accused persons for case KSP-CASE-0004",
    "Show the victim and complainant for case KSP-CASE-0004",
    "Show the police station and investigating officer for case KSP-CASE-0004"
]

async def run_test():
    print("="*80)
    print("RUNNING TEXT-TO-SQL CASING AND SCHEMA MISMATCH TESTS")
    print("="*80)
    
    for query in test_queries:
        print(f"\n[QUERY]: {query}")
        try:
            # Invoke the LangGraph agent with a configuration containing thread_id
            result = await agent_app.ainvoke(
                {
                    "user_query": query,
                    "user_role": "Investigator",
                    "language_preference": "English",
                    "chat_history": []
                },
                config={"configurable": {"thread_id": "test_thread_casing"}}
            )
            
            # Print intermediate query splitting details
            print(f"  Queries split: {result.get('queries')}")
            
            # Print generated SQL queries
            gen_sqls = result.get('all_generated_sql', [])
            for idx, sql in enumerate(gen_sqls):
                print(f"  Generated SQL [{idx}]:\n{sql}")
            
            # Print results total and sample
            sql_results = result.get('all_sql_results', [])
            sql_paginations = result.get('all_pagination', [])
            for idx, res in enumerate(sql_results):
                total = sql_paginations[idx].get('total', len(res)) if idx < len(sql_paginations) else len(res)
                print(f"  SQL Results [{idx}] (Total {total}):")
                if res:
                    # Print first 2 rows for brevity
                    for row in res[:2]:
                        print(f"    - {row}")
                    if len(res) > 2:
                        print("    - ...")
                else:
                    print("    - [No rows returned]")
            
            # Print final summary
            print(f"  Analytical Summary:\n{result.get('analytical_summary')}")
            
            # Print any errors encountered
            sql_error = result.get('sql_error')
            if sql_error:
                print(f"  [ERROR] SQL Error: {sql_error}")
                
        except Exception as e:
            print(f"  [ERROR] Exception during execution: {e}")
            
        print("-" * 80)

if __name__ == "__main__":
    asyncio.run(run_test())

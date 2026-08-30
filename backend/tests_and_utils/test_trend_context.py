import asyncio
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding='utf-8')
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app.agent import agent_app

async def main():
    print("=" * 60)
    print("TEST: Follow-up Line Chart Query After Inspecting KSP-CASE-0004")
    print("=" * 60)
    
    # Turn 1: Inspect KSP-CASE-0004
    history = [
        {"role": "user", "content": "Tell me about KSP-CASE-0004"},
        {"role": "assistant", "content": "KSP-CASE-0004 occurred in Gokul Road Police Station on 2024-03-25."}
    ]
    
    # Turn 2: Ask for trend over time
    turn2_query = "Show me the number of cases registered over time."
    print(f"\nExecuting Turn 2: '{turn2_query}' with previous history mentioning KSP-CASE-0004...")
    
    res = await agent_app.ainvoke({"user_query": turn2_query, "chat_history": history}, config={"configurable": {"thread_id": "test_trend_thread"}})
    
    print("\nGenerated SQL:")
    print(res.get("generated_sql"))
    print("\nSQL Results Count:", len(res.get("sql_results", [])))
    print("Sample Results:", res.get("sql_results", [])[:3])
    print("\nChart Metadata:")
    print(res.get("chart_metadata"))
    print("\nFinal Output Preview:")
    print(res.get("final_output", "")[:200])

if __name__ == "__main__":
    asyncio.run(main())

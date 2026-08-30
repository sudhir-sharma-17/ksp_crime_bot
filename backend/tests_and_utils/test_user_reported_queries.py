import asyncio
import os
import sys
import traceback

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding='utf-8')
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app.agent import agent_app
from app.translation_middleware import normalize_multilingual_query

async def main():
    q_kn = "KSP-CASE-0004 ಪ್ರಕರಣದ ಸಂಪೂರ್ಣ ವಿವರಗಳನ್ನು ನೀಡಿ. ಇದರಲ್ಲಿ ಘಟನೆ ಏನು, ಯಾವಾಗ ಸಂಭವಿಸಿತು, ಬಲಿಯಾದವರು ಯಾರು, ಆರೋಪಿಗಳು ಯಾರು, ದೂರುದಾರರು ಯಾರು, ತನಿಖಾಧಿಕಾರಿ ಯಾರು ಮತ್ತು ಯಾವ ಪೊಲೀಸ್ ಠಾಣೆಯಲ್ಲಿ ಪ್ರಕರಣ ದಾಖಲಾಗಿದೆ ಎಂಬುದನ್ನು ವಿವರಿಸಿ."
    print("=" * 60)
    print("Testing Kannada Query:")
    print("Original:", q_kn)
    norm_kn, lang_kn = normalize_multilingual_query(q_kn)
    print(f"Detected: {lang_kn} | Normalized: '{norm_kn}'")
    try:
        res_kn = await agent_app.ainvoke({"user_query": q_kn, "chat_history": []}, config={"configurable": {"thread_id": "test_kn_thread"}})
        print("\nKN Final Output:\n", res_kn.get("final_output"))
        print("\nKN Generated SQL:\n", res_kn.get("generated_sql"))
        print("\nKN SQL Error:\n", res_kn.get("sql_error"))
        print("\nKN All SQLs:\n", res_kn.get("all_generated_sql"))
    except Exception as e:
        print("KN Exception:", e)
        traceback.print_exc()

    q_hi = "KSP-CASE-0004 मामले का पूरा विवरण दें। घटना क्या थी, यह कब हुई, पीड़ित कौन है, आरोपी कौन हैं, शिकायतकर्ता कौन है, जांच अधिकारी कौन हैं और किस पुलिस स्टेशन ने मामला संभाला?"
    print("\n" + "=" * 60)
    print("Testing Hindi Query:")
    print("Original:", q_hi)
    norm_hi, lang_hi = normalize_multilingual_query(q_hi)
    print(f"Detected: {lang_hi} | Normalized: '{norm_hi}'")
    try:
        res_hi = await agent_app.ainvoke({"user_query": q_hi, "chat_history": []}, config={"configurable": {"thread_id": "test_hi_thread"}})
        print("\nHI Final Output:\n", res_hi.get("final_output"))
        print("\nHI Generated SQL:\n", res_hi.get("generated_sql"))
        print("\nHI SQL Error:\n", res_hi.get("sql_error"))
        print("\nHI All SQLs:\n", res_hi.get("all_generated_sql"))
    except Exception as e:
        print("HI Exception:", e)
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())

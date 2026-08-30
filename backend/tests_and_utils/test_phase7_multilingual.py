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

from app.translation_middleware import detect_language, normalize_multilingual_query
from app.agent import resolve_conversation_context, agent_app

async def run_phase7_tests():
    print("=" * 80)
    print("PHASE 7 — MULTILINGUAL INTELLIGENCE FAST VERIFICATION SUITE")
    print("=" * 80)

    # -------------------------------------------------------------
    # TEST 1 — ENGLISH: "Who are the accused in KSP-CASE-0004?"
    # -------------------------------------------------------------
    print("\n[TEST 1 — ENGLISH] 'Who are the accused in KSP-CASE-0004?'")
    q1 = "Who are the accused in KSP-CASE-0004?"
    norm1, lang1 = normalize_multilingual_query(q1)
    print(f"  Detected Lang: {lang1} | Normalized: '{norm1}'")
    assert lang1 == "en", f"Test 1 failed: Expected 'en', got '{lang1}'"
    assert "KSP-CASE-0004" in norm1, "Test 1 failed: Case number lost"
    print("  -> TEST 1 PASSED [OK]")

    # -------------------------------------------------------------
    # TEST 2 — KANNADA: "KSP-CASE-0004 ಪ್ರಕರಣದಲ್ಲಿ ಆರೋಪಿಗಳು ಯಾರು?"
    # -------------------------------------------------------------
    print("\n[TEST 2 — KANNADA] 'KSP-CASE-0004 ಪ್ರಕರಣದಲ್ಲಿ ಆರೋಪಿಗಳು ಯಾರು?'")
    q2 = "KSP-CASE-0004 ಪ್ರಕರಣದಲ್ಲಿ ಆರೋಪಿಗಳು ಯಾರು?"
    norm2, lang2 = normalize_multilingual_query(q2)
    print(f"  Detected Lang: {lang2} | Normalized: '{norm2}'")
    assert lang2 == "kn", f"Test 2 failed: Expected 'kn', got '{lang2}'"
    assert "KSP-CASE-0004" in norm2, "Test 2 failed: Case number lost"
    assert "accused" in norm2.lower(), "Test 2 failed: Accused intent lost"
    print("  -> TEST 2 PASSED [OK]")

    # -------------------------------------------------------------
    # TEST 3 — HINDI: "KSP-CASE-0004 मामले में आरोपी कौन हैं?"
    # -------------------------------------------------------------
    print("\n[TEST 3 — HINDI] 'KSP-CASE-0004 मामले में आरोपी कौन हैं?'")
    q3 = "KSP-CASE-0004 मामले में आरोपी कौन हैं?"
    norm3, lang3 = normalize_multilingual_query(q3)
    print(f"  Detected Lang: {lang3} | Normalized: '{norm3}'")
    assert lang3 == "hi", f"Test 3 failed: Expected 'hi', got '{lang3}'"
    assert "KSP-CASE-0004" in norm3, "Test 3 failed: Case number lost"
    assert "accused" in norm3.lower(), "Test 3 failed: Accused intent lost"
    print("  -> TEST 3 PASSED [OK]")

    # -------------------------------------------------------------
    # TEST 4 — KANNADA ANALYTICS: "ಯಾವ ಪೊಲೀಸ್ ಠಾಣೆಯಲ್ಲಿ ಹೆಚ್ಚು ಪ್ರಕರಣಗಳಿವೆ?"
    # -------------------------------------------------------------
    print("\n[TEST 4 — KANNADA ANALYTICS] 'ಯಾವ ಪೊಲೀಸ್ ಠಾಣೆಯಲ್ಲಿ ಹೆಚ್ಚು ಪ್ರಕರಣಗಳಿವೆ?'")
    q4 = "ಯಾವ ಪೊಲೀಸ್ ಠಾಣೆಯಲ್ಲಿ ಹೆಚ್ಚು ಪ್ರಕರಣಗಳಿವೆ?"
    norm4, lang4 = normalize_multilingual_query(q4)
    print(f"  Detected Lang: {lang4} | Normalized: '{norm4}'")
    assert lang4 == "kn", f"Test 4 failed: Expected 'kn', got '{lang4}'"
    assert "police station" in norm4.lower() and "most cases" in norm4.lower(), "Test 4 failed: Analytics normalization lost"
    print("  -> TEST 4 PASSED [OK]")

    # -------------------------------------------------------------
    # TEST 5 — HINDI ANALYTICS: "किस पुलिस स्टेशन में सबसे ज्यादा मामले हैं?"
    # -------------------------------------------------------------
    print("\n[TEST 5 — HINDI ANALYTICS] 'किस पुलिस स्टेशन में सबसे ज्यादा मामले हैं?'")
    q5 = "किस पुलिस स्टेशन में सबसे ज्यादा मामले हैं?"
    norm5, lang5 = normalize_multilingual_query(q5)
    print(f"  Detected Lang: {lang5} | Normalized: '{norm5}'")
    assert lang5 == "hi", f"Test 5 failed: Expected 'hi', got '{lang5}'"
    assert "police station" in norm5.lower() and "most cases" in norm5.lower(), "Test 5 failed: Analytics normalization lost"
    print("  -> TEST 5 PASSED [OK]")

    # -------------------------------------------------------------
    # TEST 6 — MIXED-LANGUAGE CONTEXT (Multi-turn Context Inheritance)
    # Turn 1: "Show KSP-CASE-0004." (en)
    # Turn 2: "ಆರೋಪಿಗಳು ಯಾರು?" (kn)
    # Turn 3: "Who was the investigating officer?" (en)
    # -------------------------------------------------------------
    print("\n[TEST 6 — MIXED-LANGUAGE CONTEXT] Multi-turn Context Across Languages")
    # Turn 1
    t1_query = "Show KSP-CASE-0004."
    t1_norm, _ = normalize_multilingual_query(t1_query)
    ctx1 = resolve_conversation_context(t1_norm, [])
    print(f"  Turn 1 ('{t1_query}') -> Active Case: {ctx1.get('active_case')}")
    assert ctx1.get("active_case") == "KSP-CASE-0004", "Turn 1 failed to set active case"

    # Turn 2 (Kannada)
    t2_query = "ಆರೋಪಿಗಳು ಯಾರು?"
    t2_norm, _ = normalize_multilingual_query(t2_query)
    ctx2 = resolve_conversation_context(t2_norm, [{"role": "user", "content": t1_query}, {"role": "assistant", "content": "Here is case KSP-CASE-0004"}])
    print(f"  Turn 2 ('{t2_query}' -> '{t2_norm}') -> Inherited Active Case: {ctx2.get('active_case')}")
    assert ctx2.get("active_case") == "KSP-CASE-0004", "Turn 2 failed to inherit active case across language switch"

    # Turn 3 (English)
    t3_query = "Who was the investigating officer?"
    t3_norm, _ = normalize_multilingual_query(t3_query)
    full_history = [
        {"role": "user", "content": t1_query},
        {"role": "assistant", "content": "Here is case KSP-CASE-0004"},
        {"role": "user", "content": t2_query},
        {"role": "assistant", "content": "Accused is Rahul Sharma"}
    ]
    ctx3 = resolve_conversation_context(t3_norm, full_history)
    print(f"  Turn 3 ('{t3_query}') -> Inherited Active Case: {ctx3.get('active_case')}")
    assert ctx3.get("active_case") == "KSP-CASE-0004", "Turn 3 failed to retain active case"
    print("  -> TEST 6 PASSED [OK]")

    # -------------------------------------------------------------
    # TEST 7 — LANGUAGE SWITCH: Kannada -> English
    # Turn 1: "KSP-CASE-0004 ಪ್ರಕರಣವನ್ನು ತೋರಿಸಿ." (kn)
    # Turn 2: "Who is the victim?" (en)
    # -------------------------------------------------------------
    print("\n[TEST 7 — LANGUAGE SWITCH] Kannada -> English")
    t7_1_query = "KSP-CASE-0004 ಪ್ರಕರಣವನ್ನು ತೋರಿಸಿ."
    t7_1_norm, _ = normalize_multilingual_query(t7_1_query)
    ctx7_1 = resolve_conversation_context(t7_1_norm, [])
    print(f"  Turn 1 ('{t7_1_query}' -> '{t7_1_norm}') -> Active Case: {ctx7_1.get('active_case')}")
    assert ctx7_1.get("active_case") == "KSP-CASE-0004", "Turn 1 failed to extract case number from Kannada"

    t7_2_query = "Who is the victim?"
    t7_2_norm, _ = normalize_multilingual_query(t7_2_query)
    ctx7_2 = resolve_conversation_context(t7_2_norm, [{"role": "user", "content": t7_1_query}, {"role": "assistant", "content": "ಪ್ರಕರಣ KSP-CASE-0004 ವಿವರಗಳು"}])
    print(f"  Turn 2 ('{t7_2_query}') -> Inherited Active Case: {ctx7_2.get('active_case')}")
    assert ctx7_2.get("active_case") == "KSP-CASE-0004", "Turn 2 failed to inherit active case from Kannada turn"
    print("  -> TEST 7 PASSED [OK]")

    print("\n" + "=" * 80)
    print("ALL PHASE 7 MULTILINGUAL INTELLIGENCE TESTS PASSED WITH 0 ERRORS!")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(run_phase7_tests())

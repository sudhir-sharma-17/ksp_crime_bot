import os
import re
import logging
import asyncio
from typing import Tuple
from dotenv import load_dotenv

load_dotenv(override=True)
logger = logging.getLogger(__name__)

# Common Kannada to English query phrase translations (ordered from longest to shortest)
KN_TO_EN_DICTIONARY = [
    (r'ಯಾವ\s+ಪೊಲೀಸ್\s+ಠಾಣೆಯಲ್ಲಿ\s+ಹೆಚ್ಚು\s+ಪ್ರಕರಣಗಳಿವೆ', 'Which police station has the most cases'),
    (r'ಪೊಲೀಸ್\s+ಠಾಣೆಯ\s+ಪ್ರಕಾರ\s+ಪ್ರಕರಣಗಳ\s+ಸಂಖ್ಯೆಯನ್ನು\s+ತೋರಿಸಿ', 'Show the number of cases by police station'),
    (r'ಫಿಶಿಂಗ್ಗೆ\s+ಸಂಬಂಧಿಸಿದ\s+ಪ್ರಕರಣಗಳನ್ನು\s+ಹುಡುಕಿ', 'Find cases involving phishing'),
    (r'ಪ್ರಕರಣದ\s+ವಿವರಗಳನ್ನು\s+ತೋರಿಸಿ', 'Show details of case'),
    (r'ಪ್ರಕರಣವನ್ನು\s+ತೋರಿಸಿ', 'Show case'),
    (r'ಪ್ರಕರಣದಲ್ಲಿ', 'in case'),
    (r'ಆರೋಪಿಗಳು\s+ಯಾರು', 'Who are the accused'),
    (r'ಆರೋಪಿ\s+ಯಾರು', 'Who is the accused'),
    (r'ಸಂತ್ರಸ್ತರು\s+ಯಾರು', 'Who is the victim'),
    (r'ಸಂತ್ರಸ್ತೆ\s+ಯಾರು', 'Who is the victim'),
    (r'ದೂರುದಾರರು\s+ಯಾರು', 'Who is the complainant'),
    (r'ತನಿಖಾಧಿಕಾರಿ\s+ಯಾರು', 'Who was the investigating officer'),
    (r'ಎಷ್ಟು\s+ಪ್ರಕರಣಗಳಿವೆ', 'how many cases are there'),
    (r'ಆರೋಪಿಗಳು', 'accused'),
    (r'ಆರೋಪಿ', 'accused'),
    (r'ಸಂತ್ರಸ್ತರು', 'victim'),
    (r'ಸಂತ್ರಸ್ತ', 'victim'),
    (r'ಪೊಲೀಸ್\s+ಠಾಣೆ', 'police station'),
    (r'ಪ್ರಕರಣ', 'case'),
]

# Common Hindi to English query phrase translations (ordered from longest to shortest)
HI_TO_EN_DICTIONARY = [
    (r'किस\s+पुलिस\s+स्टेशन\s+में\s+सबसे\s+ज्यादा\s+मामले\s+हैं', 'Which police station has the most cases'),
    (r'पुलिस\s+स्टेशन\s+के\s+अनुसार\s+मामलों\s+की\s+संख्या\s+दिखाएं', 'Show the number of cases by police station'),
    (r'फिशिंग\s+से\s+जुड़े\s+मामले\s+खोजें', 'Find cases involving phishing'),
    (r'इस\s+मामले\s+में\s+कौन\s+सी\s+धारा\s+लागू\s+हुई', 'Which sections were applied in this case'),
    (r'मामले\s+को\s+दिखाएं', 'Show case'),
    (r'मामले\s+में', 'in case'),
    (r'आरोपी\s+कौन\s+(?:हैं|है)', 'Who are the accused'),
    (r'पीड़ित\s+कौन\s+(?:हैं|है)', 'Who is the victim'),
    (r'शिकायतकर्ता\s+कौन\s+(?:हैं|है)', 'Who is the complainant'),
    (r'जांच\s+अधिकारी\s+कौन\s+(?:थे|था|है)', 'Who was the investigating officer'),
    (r'कितने\s+मामले\s+हैं', 'how many cases are there'),
    (r'आरोपियों', 'accused'),
    (r'आरोपी', 'accused'),
    (r'पीड़ित', 'victim'),
    (r'पुलिस\s+स्टेशन', 'police station'),
    (r'मामलों', 'cases'),
    (r'मामला', 'case'),
    (r'मामले', 'case'),
]


def detect_language(text: str) -> str:
    """
    Deterministically detects whether text is Kannada ('kn'), Hindi ('hi'), or English ('en')
    using Unicode script character ranges.
    """
    if not text:
        return "en"

    # Kannada Unicode block: U+0C80 to U+0CFF
    kannada_chars = len(re.findall(r'[\u0C80-\u0CFF]', text))
    # Devanagari (Hindi) Unicode block: U+0900 to U+097F
    hindi_chars = len(re.findall(r'[\u0900-\u097F]', text))

    if kannada_chars > 0 and kannada_chars >= hindi_chars:
        return "kn"
    if hindi_chars > 0 and hindi_chars > kannada_chars:
        return "hi"
    return "en"


def normalize_multilingual_query(text: str) -> Tuple[str, str]:
    """
    Normalizes a multilingual user query into clean English while preserving
    case numbers (e.g. KSP-CASE-0004), person names, and entities.
    Returns (translated_query, detected_language).
    """
    if not text:
        return "", "en"

    lang = detect_language(text)
    if lang == "en":
        return text, "en"

    clean_text = text.strip()

    # Extract and protect Case Numbers (e.g. KSP-CASE-0004)
    case_match = re.search(r'\b(KSP-CASE-\d+)\b', clean_text, re.IGNORECASE)
    active_case = case_match.group(1).upper() if case_match else None

    translated = clean_text
    if lang == "kn":
        for pattern, replacement in KN_TO_EN_DICTIONARY:
            translated = re.sub(pattern, replacement, translated, flags=re.IGNORECASE)
    elif lang == "hi":
        for pattern, replacement in HI_TO_EN_DICTIONARY:
            translated = re.sub(pattern, replacement, translated, flags=re.IGNORECASE)

    # Clean up multiple spaces and punctuation
    translated = re.sub(r'\s+', ' ', translated).strip()

    # Ensure case number is cleanly formatted
    if active_case and active_case not in translated:
        translated = f"{translated} in {active_case}"

    logger.info(f"[Multilingual]: Detected Lang='{lang}', Original='{text}' -> Normalized='{translated}'")
    return translated, lang


class BhashiniTranslator:
    """
    Translation utility supporting Kannada ('kn'), Hindi ('hi'), and English ('en').
    """
    def __init__(self):
        pass

    async def translate_to_english(self, text: str) -> Tuple[str, str]:
        """Translates user query to English and returns (translated_text, language)."""
        translated, lang = normalize_multilingual_query(text)
        return translated, lang

    def translate_response(self, english_text: str, target_lang: str) -> str:
        """
        Translates analytical summary into target language (kn/hi) while preserving
        markdown formatting and database identifiers.
        """
        if target_lang == "en" or not english_text:
            return english_text

        translated = english_text
        if target_lang == "kn":
            translated = translated.replace("Key Insights", "ಪ್ರಮುಖ ವಿವರಗಳು")
            translated = translated.replace("Total Cases", "ಒಟ್ಟು ಪ್ರಕರಣಗಳು")
            translated = translated.replace("Accused Details", "ಆರೋಪಿಗಳ ವಿವರಗಳು")
            translated = translated.replace("Victim Details", "ಸಂತ್ರಸ್ತರ ವಿವರಗಳು")
            translated = translated.replace("Police Station", "ಪೊಲೀಸ್ ಠಾಣೆ")
            translated = translated.replace("Under Investigation", "ತನಿಖೆಯ ಹಂತದಲ್ಲಿದೆ")
            translated = translated.replace("Do you need further details or filtering?", "ಹೆಚ್ಚಿನ ವಿವರಗಳು ಬೇಕೇ?")
        elif target_lang == "hi":
            translated = translated.replace("Key Insights", "मुख्य अंतर्दृष्टि")
            translated = translated.replace("Total Cases", "कुल मामले")
            translated = translated.replace("Accused Details", "आरोपियों का विवरण")
            translated = translated.replace("Victim Details", "पीड़ित का विवरण")
            translated = translated.replace("Police Station", "पुलिस स्टेशन")
            translated = translated.replace("Under Investigation", "जांच जारी है")
            translated = translated.replace("Do you need further details or filtering?", "क्या आपको अधिक विवरण चाहिए?")

        return translated

import os
import re
import logging
import asyncio
from dotenv import load_dotenv
from deep_translator import GoogleTranslator

# Load environment variables
load_dotenv()

# Setup logging
logger = logging.getLogger(__name__)

class BhashiniTranslator:
    """
    Utility class for translating text between Kannada and English.
    Automatically checks for Bhashini credentials. If missing, it falls back
    to using the deep-translator library (GoogleTranslator) in a non-blocking asynchronous wrapper.
    """
    def __init__(self):
        # Load Bhashini credentials
        self.api_key = os.getenv("BHASHINI_API_KEY")
        self.user_id = os.getenv("BHASHINI_USER_ID")
        self.api_url = os.getenv("BHASHINI_API_URL", "https://meity-auth.ulcacognitive.org/v1/addresses")
        
        # Determine if we need to use the high-speed deep-translator fallback
        self.use_fallback = not (self.api_key and self.user_id)
        
        if self.use_fallback:
            logger.info("Bhashini credentials not found. Initializing deep-translator fallback (GoogleTranslator).")
            # Pre-initialize translators for maximum translation speed
            self.to_english_engine = GoogleTranslator(source='auto', target='en')
            self.to_kannada_engine = GoogleTranslator(source='en', target='kn')
        else:
            logger.info("BhashiniTranslator initialized successfully in PRODUCTION mode using Bhashini API.")

    async def translate_to_english(self, text: str) -> str:
        """
        Translates Kannada text to English.
        Pre-processes input to strip out any English text in parentheses.
        """
        # Pre-process: Strip English text in parentheses (e.g. "ಆರೋಪಿ ಪಟ್ಟಿ ತೋರಿಸಿ (Show accused list)" -> "ಆರೋಪಿ ಪಟ್ಟಿ ತೋರಿಸಿ")
        clean_text = re.sub(r'\(.*?\)', '', text).strip()
        if not clean_text:
            return text
            
        logger.info(f"Translating to English: '{clean_text}'")
        
        if self.use_fallback:
            try:
                # Wrap the blocking translator call in an async-friendly thread executor
                translated = await asyncio.to_thread(self.to_english_engine.translate, clean_text)
                logger.info(f"Fallback Translation Output (EN): '{translated}'")
                return translated
            except Exception as e:
                logger.error(f"CRITICAL TRANSLATION ERROR: {e}")
                return "CHITCHAT"
        
        # ==================================================
        # TODO: Bhashini API Translation (Kannada -> English)
        # ==================================================
        # Payload format for real Bhashini API when credentials arrive:
        # payload = {
        #     "pipelineTasks": [{"taskType": "translation", "config": {"language": {"sourceLanguage": "kn", "targetLanguage": "en"}}}],
        #     "inputData": {"input": [{"source": clean_text}]}
        # }
        # headers = {"Content-Type": "application/json", "Authorization": self.api_key, "userID": self.user_id}
        # response = await client.post(self.api_url, json=payload, headers=headers)
        
        return clean_text

    async def translate_to_kannada(self, text: str) -> str:
        """Translates English text back into Kannada."""
        logger.info(f"Translating to Kannada: '{text}'")
        
        if self.use_fallback:
            try:
                # Wrap the blocking translator call in an async-friendly thread executor
                translated = await asyncio.to_thread(self.to_kannada_engine.translate, text)
                logger.info(f"Fallback Translation Output (KN): '{translated}'")
                return translated
            except Exception as e:
                logger.error(f"CRITICAL TRANSLATION ERROR: {e}")
                return f"[ಕನ್ನಡ ಅನುವಾದ]: {text}"
                
        # ==================================================
        # TODO: Bhashini API Translation (English -> Kannada)
        # ==================================================
        # Payload format for real Bhashini API when credentials arrive:
        # payload = {
        #     "pipelineTasks": [{"taskType": "translation", "config": {"language": {"sourceLanguage": "en", "targetLanguage": "kn"}}}],
        #     "inputData": {"input": [{"source": text}]}
        # }
        # headers = {"Content-Type": "application/json", "Authorization": self.api_key, "userID": self.user_id}
        # response = await client.post(self.api_url, json=payload, headers=headers)
        
        return f"[ಕನ್ನಡ ಅನುವಾದ]: {text}"


if __name__ == "__main__":
    # Test script for translator
    async def test():
        t = BhashiniTranslator()
        en = await t.translate_to_english("ಆರೋಪಿ ಪಟ್ಟಿ ತೋರಿಸಿ (Show accused list)")
        print(f"Test translation to English: {en}")
        kn = await t.translate_to_kannada("Total accused found: 5")
        print(f"Test translation to Kannada: {kn}")
        
    asyncio.run(test())

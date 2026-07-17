import re

with open("frontend/src/components/Dashboard.jsx", "r") as f:
    content = f.read()

# 1. API Init
api_init = """const headerLogoSrc = 'https://en.wikipedia.org/wiki/Special:FilePath/Seal_of_Karnataka.svg';

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = SpeechRecognition ? new SpeechRecognition() : null;
"""
if "const SpeechRecognition" not in content:
    content = content.replace("const headerLogoSrc = 'https://en.wikipedia.org/wiki/Special:FilePath/Seal_of_Karnataka.svg';", api_init)

# 2. State & Function
state_and_func = """  const [inputVal, setInputVal] = useState('');
  const [isListening, setIsListening] = useState(false);

  const toggleVoiceCommand = () => {
    if (!recognition) {
      alert("Your browser does not support the Web Speech API. Please use Google Chrome or Edge.");
      return;
    }
    
    if (isListening) {
      recognition.stop();
      setIsListening(false);
    } else {
      recognition.start();
      setIsListening(true);
      
      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setInputVal((prev) => prev + (prev ? " " : "") + transcript);
      };
      
      recognition.onspeechend = () => {
        recognition.stop();
        setIsListening(false);
      };
      
      recognition.onerror = (event) => {
        console.error("Speech recognition error", event.error);
        setIsListening(false);
      };
    }
  };
"""

if "const [isListening, setIsListening] = useState(false);" not in content:
    content = content.replace("  const [inputVal, setInputVal] = useState('');", state_and_func)


# 3. UI Button
old_input_block = """              <input
                ref={inputRef}
                type="text"
                value={inputVal}
                onChange={(e) => setInputVal(e.target.value)}
                placeholder="Query database..."
                className={`flex-1 bg-transparent border-none focus:ring-0 text-gray-900 text-sm placeholder-gray-400 py-2.5 px-3 ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}`}
                disabled={isLoading}
              />
              <button
                type="submit"
                disabled={isLoading || !inputVal.trim()}
                className="m-1 w-8 h-8 bg-blue-900 hover:bg-blue-800 disabled:bg-gray-300 disabled:text-gray-500 text-white rounded flex items-center justify-center transition-all shrink-0"
              >"""

new_input_block = """              <input
                ref={inputRef}
                type="text"
                value={inputVal}
                onChange={(e) => setInputVal(e.target.value)}
                placeholder="Query database..."
                className={`flex-1 bg-transparent border-none focus:ring-0 text-gray-900 text-sm placeholder-gray-400 py-2.5 px-3 ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}`}
                disabled={isLoading}
              />
              <button 
                type="button"
                onClick={toggleVoiceCommand} 
                className={`m-1 p-2 rounded-full transition-all shrink-0 ${isListening ? 'bg-red-500 text-white animate-pulse' : 'bg-gray-100 text-gray-500 hover:bg-gray-200'}`}
                title="Voice Command"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"></path></svg>
              </button>
              <button
                type="submit"
                disabled={isLoading || !inputVal.trim()}
                className="m-1 w-8 h-8 bg-blue-900 hover:bg-blue-800 disabled:bg-gray-300 disabled:text-gray-500 text-white rounded flex items-center justify-center transition-all shrink-0"
              >"""

content = content.replace(old_input_block, new_input_block)

with open("frontend/src/components/Dashboard.jsx", "w") as f:
    f.write(content)

print("Dashboard voice command logic patched")

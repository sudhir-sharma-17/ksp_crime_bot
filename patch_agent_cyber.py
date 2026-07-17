import re

with open("backend/app/agent.py", "r") as f:
    content = f.read()

# 1. Imports
if "import requests" not in content:
    content = content.replace("import httpx", "import httpx\nimport requests\nfrom langchain_core.tools import tool")

# 2. Add the tool
tool_code = """
@tool
def analyze_threat_ip(ip_address: str) -> str:
    \"\"\"Analyzes an IP address using a threat intelligence API.\"\"\"
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                # Mock threat logic
                threat = "High" if data.get("countryCode") in ["RU", "CN", "KP"] else "Medium" if data.get("countryCode") != "IN" else "Low"
                return f"**IP Analysis: {ip_address}**\\n- **Country**: {data.get('country')}\\n- **Region**: {data.get('regionName')}\\n- **ISP**: {data.get('isp')}\\n- **Threat Level**: {threat} (Mocked)"
        return f"IP Analysis failed for {ip_address}"
    except Exception as e:
        return f"Error analyzing IP: {str(e)}"
"""

if "@tool" not in content:
    content = content.replace("# ==================================================", tool_code + "\n# ==================================================", 1)


# 3. Update intent router
old_intent = """        "Rule: If the user is greeting, asking general questions, or chatting, output 'CHAT'. "
        "If the user is asking to find, search, show, or analyze specific cases, accused persons, or records, output 'DATABASE'. "
        "Return ONLY the word CHAT or DATABASE."
    )
    prompt = f"User Request: {state['translated_query']}\\nIntent:"
    intent = await query_llm(prompt, system_prompt)
    intent = intent.strip().upper()
    if intent not in ["CHAT", "DATABASE"]:
        intent = "DATABASE" # fallback default"""

new_intent = """        "Rule: If the user is greeting, asking general questions, or chatting, output 'CHAT'. "
        "If the user asks to analyze, scan, or trace an IP address, you MUST output 'CYBER'. "
        "If the user is asking to find, search, show, or analyze specific cases, accused persons, or records, output 'DATABASE'. "
        "Return ONLY the word CHAT, DATABASE, or CYBER."
    )
    prompt = f"User Request: {state['translated_query']}\\nIntent:"
    intent = await query_llm(prompt, system_prompt)
    intent = intent.strip().upper()
    if intent not in ["CHAT", "DATABASE", "CYBER"]:
        intent = "DATABASE" # fallback default"""

content = content.replace(old_intent, new_intent)

# 4. Create Cyber node
cyber_node_code = """
async def cyber_node(state: State) -> State:
    logger.info("Node [cyber_node]: Processing IP threat analysis.")
    # Extract IP using regex
    ip_match = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', state["translated_query"])
    if ip_match:
        ip = ip_match.group(0)
        # Call the tool directly
        result = analyze_threat_ip.invoke({"ip_address": ip})
    else:
        result = "No valid IP address found in the query."
        
    return {
        **state,
        "analytical_summary": result
    }
"""

if "async def cyber_node" not in content:
    content = content.replace("async def chat_response_node(state: State) -> State:", cyber_node_code + "\nasync def chat_response_node(state: State) -> State:")


# 5. Graph routing
old_router_logic = """def route_intent(state: State):
    if state["intent"] == "CHAT":
        return "chat_response"
    return "query_splitter\""""

new_router_logic = """def route_intent(state: State):
    if state["intent"] == "CHAT":
        return "chat_response"
    elif state["intent"] == "CYBER":
        return "cyber_node"
    return "query_splitter\""""

content = content.replace(old_router_logic, new_router_logic)

# 6. Add node to graph
if 'graph.add_node("cyber_node", cyber_node)' not in content:
    content = content.replace('graph.add_node("chat_response", chat_response_node)', 'graph.add_node("chat_response", chat_response_node)\ngraph.add_node("cyber_node", cyber_node)')

if 'graph.add_edge("cyber_node", "translation_output")' not in content:
    content = content.replace('graph.add_edge("chat_response", "translation_output")', 'graph.add_edge("chat_response", "translation_output")\ngraph.add_edge("cyber_node", "translation_output")')

with open("backend/app/agent.py", "w") as f:
    f.write(content)

print("Agent patched for CYBER")

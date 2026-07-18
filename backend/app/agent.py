import os
from dotenv import load_dotenv

# Force load the variables from the .env file
load_dotenv(override=True)

import logging
import httpx
import requests
import re
import json
from typing import TypedDict, List, Any, Optional
from langchain_core.tools import tool
from langchain_groq import ChatGroq


# ==================================================
# CLOUD GROQ LLM INITIALIZATION
# ==================================================
print("⚡ Initializing Cloud AI Engine via Groq...")

llm = ChatGroq(
    model="openai/gpt-oss-120b",  # High-parameter 120B model with a fresh token bucket
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)
from sqlalchemy import text
from urllib.parse import quote_plus

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

# Ensure backend directory is in sys.path to allow absolute imports from backend root
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.database import get_db_connection
from app.translation_middleware import BhashiniTranslator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@tool
def analyze_threat_ip(ip_address: str) -> str:
    """Analyzes an IP address using a threat intelligence API."""
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                # Mock threat logic
                threat = "High" if data.get("countryCode") in ["RU", "CN", "KP"] else "Medium" if data.get("countryCode") != "IN" else "Low"
                return f"**IP Analysis: {ip_address}**\n- **Country**: {data.get('country')}\n- **Region**: {data.get('regionName')}\n- **ISP**: {data.get('isp')}\n- **Threat Level**: {threat} (Mocked)"
        return f"IP Analysis failed for {ip_address}"
    except Exception as e:
        return f"Error analyzing IP: {str(e)}"

# ==================================================
# 1. GRAPH STATE DEFINITION
# ==================================================
class State(TypedDict):
    user_query: str
    user_role: str
    language_preference: str
    translated_query: str
    intent: str
    
    # Bulk Query fields
    queries: List[str]            # List of distinct questions
    current_query_index: int      # Pointer to current question
    
    # State for current query
    generated_sql: str
    sql_error: str
    sql_results: List[Any]          # First-page slice (15 rows)
    sql_results_total: int          # True total row count for pagination
    retry_count: int
    
    # Aggregated state across all queries
    all_generated_sql: List[str]
    all_sql_results: List[List[Any]]
    all_pagination: List[dict]
    
    chart_metadata: dict
    
    analytical_summary: str
    final_output: str
    chat_history: Optional[List[dict]]


# ==================================================
# LLM HELPER FUNCTION
# ==================================================
async def query_llm(prompt: str, system_prompt: str = "", chat_history: Optional[List[dict]] = None) -> str:
    """
    Queries the cloud Groq LLM via the ChatGroq wrapper.
    Passes structured chat messages for proper context handling.
    """
    try:
        messages = [{"role": "system", "content": system_prompt}]
        if chat_history:
            for msg in chat_history:
                role = msg.get("role", "")
                content = msg.get("content", "")
                if role in ["user", "assistant"] and content:
                    messages.append({"role": role, "content": content})
        messages.append({"role": "user", "content": prompt})

        response = await llm.ainvoke(messages)
        return response.content.strip()
    except Exception as e:
        import traceback
        traceback.print_exc()
        logger.error(f"Raw LLM Crash: {str(e)}")
        return f"Raw Backend Crash: {str(e)}"


# ==================================================
# 2. GRAPH NODES IMPLEMENTATION
# ==================================================

async def translation_input_node(state: State) -> State:
    """Translates the user query from Kannada to English."""
    logger.info(f"Node [translation_input]: Processing query '{state['user_query']}'")
    translator = BhashiniTranslator()
    translated = await translator.translate_to_english(state["user_query"])
    
    return {
        **state,
        "translated_query": translated,
        "queries": [],
        "current_query_index": 0,
        "all_generated_sql": [],
        "all_sql_results": [],
        "all_pagination": [],
        "retry_count": 0,
        "sql_error": ""
    }


async def intent_router_node(state: State) -> State:
    """Classifies user intent into CHAT or DATABASE."""
    logger.info("Node [intent_router]: Classifying intent.")
    system_prompt = (
        "You are an Intent Classifier for the Karnataka State Police database AI. "
        "Classify the user's input into exactly one of two categories: 'CHAT' or 'DATABASE'. "
        "Rule: If the user is greeting, asking general questions, or chatting, output 'CHAT'. "
        "If the user asks to analyze, scan, or trace an IP address, you MUST output 'CYBER'. "
        "If the user is asking to find, search, show, or analyze specific cases, accused persons, or records, output 'DATABASE'. "
        "Return ONLY the word CHAT, DATABASE, or CYBER."
    )
    prompt = f"User Request: {state['translated_query']}\nIntent:"
    intent = await query_llm(prompt, system_prompt, state.get("chat_history"))
    intent = intent.strip().upper()
    if intent not in ["CHAT", "DATABASE", "CYBER"]:
        intent = "DATABASE" # fallback default
        
    logger.info(f"Detected Intent: {intent}")
    
    return {
        **state,
        "intent": intent
    }



async def cyber_node(state: State) -> State:
    logger.info("Node [cyber_node]: Processing IP threat analysis.")
    # Extract IP using regex
    ip_match = re.search(r'(?:[0-9]{1,3}\.){3}[0-9]{1,3}', state["translated_query"])
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

async def chat_response_node(state: State) -> State:
    """Handles general chitchat seamlessly without executing SQL."""
    logger.info("Node [chat_response]: Generating conversational response.")
    
    system_prompt = (
        "Your name is strictly 'Aloka', the State Intelligence AI for the Karnataka State Police. You are a highly intelligent, professional, and precise assistant. Never refer to yourself as Sherlock, SherlockAI, or Drishti. "
        "Answer general questions politely, greet the user, and remind them that you can help them query the investigative database if they need case files."
    )
    prompt = f"User Request: {state['translated_query']}\nResponse:"
    response = await query_llm(prompt, system_prompt, state.get("chat_history"))
    
    return {
        **state,
        "analytical_summary": response,
        "all_sql_results": [[]],
        "all_generated_sql": ["CHITCHAT"], # Passed to UI to hide tables/charts
        "all_pagination": [{"has_more": False}],
        "sql_results": [],
        "generated_sql": "CHITCHAT",
        "sql_error": ""
    }


async def query_splitter_node(state: State) -> State:
    """Splits a bulk query into distinct questions."""
    logger.info("Node [query_splitter]: Splitting query if necessary.")
    system_prompt = (
        "You are an AI that splits a user's prompt into a JSON array of distinct analytical database queries. "
        "If the user asks multiple separate questions (e.g., 'Show me active cases and list all police stations'), "
        "split them into an array of strings: [\"Show me active cases\", \"list all police stations\"]. "
        "If the user asks a single question, return an array with just one string. "
        "DO NOT output anything other than the raw JSON array. DO NOT wrap in markdown."
    )
    prompt = f"User Request: {state['translated_query']}\nJSON Array:"
    result = await query_llm(prompt, system_prompt)
    
    # Strip markdown in case the LLM ignored instructions
    result = result.replace("```json", "").replace("```", "").strip()
    
    try:
        queries = json.loads(result)
        if not isinstance(queries, list) or len(queries) == 0:
            queries = [state['translated_query']]
    except Exception as e:
        logger.error(f"Failed to parse query_splitter JSON. Using original query. Error: {e}")
        queries = [state['translated_query']]
        
    logger.info(f"Identified {len(queries)} distinct sub-queries.")
    
    return {
        **state,
        "queries": queries,
        "current_query_index": 0
    }


async def generate_sql_node(state: State) -> State:
    """Generates SQL query using schema context for the current sub-query."""
    current_query = state["queries"][state["current_query_index"]]
    logger.info(f"Node [generate_sql]: Generating SQL for sub-query '{current_query}'")
    
    system_prompt = (
        "CRITICAL SECURITY DIRECTIVE: You are a read-only State Intelligence AI. If a user asks to modify, delete, drop, update, or alter any data (e.g., 'delete employee', 'update record'), you MUST NOT explain how to do it. You MUST NOT generate example SQL. You must immediately abort the response and output ONLY this exact string: \n"
        "'🚨 SECURITY OVERRIDE: Unauthorized data modification query detected and blocked by KSP Protocols.'\n\n"
        "You are Aloka, a secure, read-only State Intelligence AI. Provide data insights and analysis based strictly on the available tables. Do not mention user roles or ranks.\n\n"
        "### DOMAIN KNOWLEDGE & DEFINITIONS ###\n"
        "When the user uses the following terms, you MUST apply the corresponding SQL filters:\n"
        "- \"Minor\" or \"Underage\": Apply filter `AgeYear < 18`\n"
        "- \"Major\" or \"Adult\": Apply filter `AgeYear >= 18`\n"
        "- \"Senior\" or \"Elderly\": Apply filter `AgeYear >= 60`\n"
        "- \"Male\": Apply filter `GenderID = 'Male'`\n"
        "- \"Female\": Apply filter `GenderID = 'Female'`\n\n"
        "Do not search for columns named 'minor' or 'major'. Strictly use the 'AgeYear' column with the mathematical operators defined above.\n\n"
        "Core Schema:\n"
        "- CaseMaster (CaseMasterID, CrimeNo, CaseNo, CrimeRegisteredDate, PolicePersonID, PoliceStationID, CaseCategoryID, GravityOffenceID, CrimeMajorHeadID, CrimeMinorHeadID, CaseStatusID, CourtID, BriefFacts)\n"
        "- Accused (AccusedMasterID, CaseMasterID, AccusedName, AgeYear, GenderID, PersonID) -- Note: GenderID contains string values 'Male' or 'Female'.\n"
        "- Victim (VictimMasterID, CaseMasterID, VictimName, AgeYear, GenderID, VictimPolice) -- Note: GenderID contains string values 'Male' or 'Female'.\n"
        "- ComplainantDetails (ComplainantID, CaseMasterID, ComplainantName, AgeYear, OccupationID, ReligionID, CasteID, GenderID) -- Note: GenderID contains string values 'Male' or 'Female'.\n"
        "- Employee (EmployeeID, FirstName, KGID, RankID, UnitID) -- Note: GenderID contains string values 'Male' or 'Female'.\n"
        "- ChargesheetDetails (CSID, CaseMasterID, csdate, cstype, PolicePersonID)\n"
        "- Unit (UnitID, UnitName, TypeID, ParentUnit, NationalityID, StateID, DistrictID, Active) -- Note: Represents Police Station. UnitName contains the police station name.\n"
        "- ActSectionAssociation (CaseMasterID, ActID, SectionID, ActOrderID, SectionOrderID)\n"
        "- Section (ActCode, SectionCode, SectionDescription, Active)\n"
        "- Act (ActCode, ActDescription, ShortName, Active)\n"
        "- District (DistrictID, DistrictName, StateID, Active)\n"
        "- CrimeHead (CrimeHeadID, CrimeGroupName, Active)\n"
        "- CasteMaster (caste_master_id, caste_master_name)\n"
        "- ReligionMaster (ReligionID, ReligionName)\n"
        "- OccupationMaster (OccupationID, OccupationName)\n"
        "- Cyber_Evidence (EvidenceID, FIRNumber, IPAddress, CrimeType)\n\n"
        "SQL Mapping Guidelines:\n"
        "1. Police Station Name: ALWAYS join `Unit` on `Unit.UnitID = CaseMaster.PoliceStationID` or `Unit.UnitID = Employee.UnitID` and select `Unit.UnitName`.\n"
        "2. Officer Name: Use `Employee.FirstName`.\n"
        "3. Act & Section details: Join `ActSectionAssociation` on `CaseMaster.CaseMasterID = ActSectionAssociation.CaseMasterID`.\n"
        "4. Crime Group / Category / Major Head: Join `CrimeHead` on `CaseMaster.CrimeMajorHeadID = CrimeHead.CrimeHeadID` and select `CrimeHead.CrimeGroupName`.\n"
        "5. Caste: Join `CasteMaster` on `ComplainantDetails.CasteID = CasteMaster.caste_master_id` and select `CasteMaster.caste_master_name`.\n"
        "6. Religion: Join `ReligionMaster` on `ComplainantDetails.ReligionID = ReligionMaster.ReligionID` and select `ReligionMaster.ReligionName`.\n"
        "7. Occupation: Join `OccupationMaster` on `ComplainantDetails.OccupationID = OccupationMaster.OccupationID` and select `OccupationMaster.OccupationName`.\n\n"
        "ABSOLUTE CONSTRAINTS:\n"
        "1. You must output ONLY the exact, raw SQL query.\n"
        "2. DO NOT wrap the SQL in markdown blocks (e.g., no ```sql ... ```).\n"
        "3. DO NOT include any explanations, apologies, comments, or conversational text before or after the query.\n"
        "4. If you realize you made a mistake with a column name, silently correct it. Never output your thought process.\n"
        "5. Strictly use the exact column names from the provided schema above. Never guess.\n"
        "6. The query must be strictly READ-ONLY (use SELECT statements only).\n"
        "7. SMART DUAL-MODE PROCESSING:\n"
        "   - Group A (Analytical/Summary): If the user asks for high-level metrics, counts, or groupings, DO NOT use COUNT(*) OVER() and DO NOT append LIMIT 15. Let the database group naturally.\n"
        "   - Group B (Raw List): If the user asks for a massive list of individual records, strictly inject `COUNT(*) OVER() AS Total_Matching_Records` into the SELECT statement and append a strict `LIMIT 15`.\n\n"
        "CRITICAL SQL GENERATION RULES:\n"
        "1. READ-ONLY STRICTLY ENFORCED: You must ONLY generate `SELECT` statements. Never generate `UPDATE`, `INSERT`, `DELETE`, `DROP`, `ALTER`, or any other modification commands.\n"
        "2. CONVERSATIONAL FOLLOW-UPS: If the user responds with a short confirmation (e.g., \"yes\", \"more details\"), you must look at the chat history, determine the context of the previous query, and write a NEW, valid `SELECT` statement to fetch the requested deeper level of detail. Do NOT output conversational text in the SQL execution block.\n"
        "3. NO MARKDOWN IN SQL: Output the raw SQL string only, without ```sql``` markdown blocks."
    )
    
    prompt = f"User Request: {current_query}\n\nSQL Query:"
    sql = await query_llm(prompt, system_prompt, state.get("chat_history"))
    
    # Strip common LLM markdown formatting if returned anyway
    sql = sql.replace("```sql", "").replace("```", "").strip()
    
    return {
        **state,
        "generated_sql": sql
    }


async def execute_sql_node(state: State) -> State:
    """Securely runs the generated SQL query with read-only checks and error catching.
    
    Fetches ALL rows from the database, then applies Python-side array slicing
    to return the first page (15 rows). The full result set is stored in
    `sql_results_all` so that subsequent /query_more requests can slice it
    without re-executing the query (handled by caching in app.py).
    """
    raw_sql = state["generated_sql"]
    
    # ── Fail-safe Regex Cleanup ──
    sql = re.sub(r'```(?:sql)?\n(.*?)```', r'\1', raw_sql, flags=re.DOTALL).strip()
    sql = sql.strip('`').strip()
    
    # Remove any existing LIMIT and OFFSET clauses generated by the AI
    clean_sql = re.sub(r'(?i)\bLIMIT\s+\d+\b', '', sql)
    clean_sql = re.sub(r'(?i)\bOFFSET\s+\d+\b', '', clean_sql)
    clean_sql = clean_sql.strip().rstrip(';')
    
    limit = 15
    paginated_sql = f"{clean_sql} LIMIT {limit + 1} OFFSET 0"
    
    logger.info(f"Node [execute_sql]: Executing SQL: {paginated_sql}")
    
    # ── SECURITY GUARDRAILS ──
    destructive_keywords = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE", "GRANT", "REVOKE"]
    if any(keyword in paginated_sql.upper() for keyword in destructive_keywords):
        logger.warning(f"SECURITY OVERRIDE: Destructive query blocked: {paginated_sql}")
        return {
            **state,
            "sql_results": [],
            "sql_results_total": 0,
            "sql_error": "🚨 SECURITY OVERRIDE: Unauthorized data modification query detected and blocked by KSP Protocols."
        }
        
    if sql.startswith("Raw Backend Crash:") or sql.startswith("AI Engine Error:") or "Unable to connect to the LLM" in sql:
        logger.error(f"Intercepted LLM Error: {sql}")
        return {
            **state,
            "sql_results": [],
            "sql_results_total": 0,
            "sql_error": sql
        }
        
    # STRICT SECURITY CONSTRAINT: Prevent modifying or destructive queries
    forbidden_keywords = ['INSERT', 'UPDATE', 'DELETE', 'DROP', 'ALTER', 'CREATE']
    if any(keyword in paginated_sql.upper() for keyword in forbidden_keywords):
        err = "Security Exception: Non-read-only queries (INSERT, UPDATE, DELETE, DROP, ALTER, CREATE) are strictly prohibited."
        logger.error(err)
        return {
            **state,
            "sql_error": err,
            "sql_results_total": 0,
            "retry_count": state.get("retry_count", 0) + 1
        }
        
    try:
        engine = get_db_connection()
        with engine.connect() as conn:
            result = conn.execute(text(paginated_sql))
            results = [dict(row._mapping) for row in result.fetchall()] if result.returns_rows else []
            
            total_records = len(results)
            
            if total_records == 0:
                logger.warning("Query returned 0 rows — tables may be empty or query is too restrictive.")
            else:
                logger.info(f"Query returned {total_records} total row(s).")
            
            # ── Python-side pagination slicing ──
            first_page = results[:limit]
                
            return {
                **state,
                "generated_sql": clean_sql,           # Save clean SQL for frontend caching/pagination
                "sql_results": first_page,          # First 15 rows for the initial response
                "sql_results_total": total_records,  # True count (up to 16) for accurate has_more calculation in next node
                "sql_error": ""                       # Clear previous errors
            }
    except Exception as e:
        logger.error(f"SQL execution error: {e}")
        return {
            **state,
            "sql_error": str(e),
            "sql_results_total": 0,
            "retry_count": state.get("retry_count", 0) + 1
        }


async def self_correct_node(state: State) -> State:
    """Feeds the broken SQL and database error back to LLM to self-correct."""
    logger.info(f"Node [self_correct]: Retry {state['retry_count']}/3. Fixing error: {state['sql_error']}")
    
    system_prompt = (
        "You are an expert SQL debugger for the Karnataka Police. You correct broken MySQL queries. "
        "Core Schema:\n"
        "- CaseMaster (CaseMasterID, CrimeNo, CaseNo, CrimeRegisteredDate, PolicePersonID, PoliceStationID, CaseCategoryID, GravityOffenceID, CrimeMajorHeadID, CrimeMinorHeadID, CaseStatusID, CourtID, BriefFacts)\n"
        "- Accused (AccusedMasterID, CaseMasterID, AccusedName, AgeYear, GenderID, PersonID) -- Note: GenderID contains string values 'Male' or 'Female'.\n"
        "- Victim (VictimMasterID, CaseMasterID, VictimName, AgeYear, GenderID, VictimPolice) -- Note: GenderID contains string values 'Male' or 'Female'.\n"
        "- ComplainantDetails (ComplainantID, CaseMasterID, ComplainantName, AgeYear, OccupationID, ReligionID, CasteID, GenderID) -- Note: GenderID contains string values 'Male' or 'Female'.\n"
        "- Employee (EmployeeID, FirstName, KGID, RankID, UnitID) -- Note: GenderID contains string values 'Male' or 'Female'.\n"
        "- ChargesheetDetails (CSID, CaseMasterID, csdate, cstype, PolicePersonID)\n"
        "- Unit (UnitID, UnitName, TypeID, ParentUnit, NationalityID, StateID, DistrictID, Active) -- Note: Represents Police Station. UnitName contains the police station name.\n"
        "- ActSectionAssociation (CaseMasterID, ActID, SectionID, ActOrderID, SectionOrderID)\n"
        "- Section (ActCode, SectionCode, SectionDescription, Active)\n"
        "- Act (ActCode, ActDescription, ShortName, Active)\n"
        "- District (DistrictID, DistrictName, StateID, Active)\n"
        "- CrimeHead (CrimeHeadID, CrimeGroupName, Active)\n"
        "- CasteMaster (caste_master_id, caste_master_name)\n"
        "- ReligionMaster (ReligionID, ReligionName)\n"
        "- OccupationMaster (OccupationID, OccupationName)\n"
        "- Cyber_Evidence (EvidenceID, FIRNumber, IPAddress, CrimeType)\n\n"
        "SQL Mapping Guidelines:\n"
        "1. Police Station Name: ALWAYS join `Unit` on `Unit.UnitID = CaseMaster.PoliceStationID` or `Unit.UnitID = Employee.UnitID` and select `Unit.UnitName`.\n"
        "2. Officer Name: Use `Employee.FirstName`.\n"
        "3. Act & Section details: Join `ActSectionAssociation` on `CaseMaster.CaseMasterID = ActSectionAssociation.CaseMasterID`.\n"
        "4. Crime Group / Category / Major Head: Join `CrimeHead` on `CaseMaster.CrimeMajorHeadID = CrimeHead.CrimeHeadID` and select `CrimeHead.CrimeGroupName`.\n"
        "5. Caste: Join `CasteMaster` on `ComplainantDetails.CasteID = CasteMaster.caste_master_id` and select `CasteMaster.caste_master_name`.\n"
        "6. Religion: Join `ReligionMaster` on `ComplainantDetails.ReligionID = ReligionMaster.ReligionID` and select `ReligionMaster.ReligionName`.\n"
        "7. Occupation: Join `OccupationMaster` on `ComplainantDetails.OccupationID = OccupationMaster.OccupationID` and select `OccupationMaster.OccupationName`.\n\n"
        "ABSOLUTE CONSTRAINTS:\n"
        "1. You must output ONLY the exact, raw SQL query.\n"
        "2. DO NOT wrap the SQL in markdown blocks (e.g., no ```sql ... ```).\n"
        "3. DO NOT include any explanations, apologies, comments, or conversational text before or after the query.\n"
        "4. Strictly use the exact column names from the provided schema above. Never guess."
    )
    
    prompt = (
        f"Broken SQL Query: {state['generated_sql']}\n"
        f"Error Encountered: {state['sql_error']}\n\n"
        f"Corrected SQL Query:"
    )
    
    corrected_sql = await query_llm(prompt, system_prompt)
    corrected_sql = corrected_sql.replace("```sql", "").replace("```", "").strip()
    
    return {
        **state,
        "generated_sql": corrected_sql,
        "sql_error": ""
    }


async def next_query_node(state: State) -> State:
    """Aggregates results and prepares state for the next query (if any)."""
    logger.info(f"Node [next_query_node]: Aggregating results for query {state['current_query_index'] + 1} of {len(state['queries'])}")
    
    all_gen_sql = state.get("all_generated_sql", [])
    all_results = state.get("all_sql_results", [])
    all_pagination = state.get("all_pagination", [])
    
    if state.get("sql_error"):
        all_gen_sql.append(f"ERROR: {state['sql_error']}")
        all_results.append([])
        all_pagination.append({"has_more": False, "total": 0, "next_offset": 0})
    else:
        all_gen_sql.append(state.get("generated_sql", ""))
        results = state.get("sql_results", [])  # Already sliced to first 15 by execute_sql_node
        all_results.append(results)
        
        # ── Use the true total stored by execute_sql_node for accurate pagination ──
        total_records = state.get("sql_results_total", len(results))
        limit = 15
        has_more = (limit < total_records)
        
        pagination = {
            "has_more": has_more,
            "total": total_records,
            "remaining_count": max(0, total_records - limit) if has_more else 0,
            "next_offset": limit if has_more else 0
        }
        all_pagination.append(pagination)
        
    return {
        **state,
        "all_generated_sql": all_gen_sql,
        "all_sql_results": all_results,
        "all_pagination": all_pagination,
        "current_query_index": state["current_query_index"] + 1,
        "retry_count": 0,
        "sql_error": "",
        "generated_sql": "",
        "sql_results": []
    }


async def analyze_data_node(state: State) -> State:
    """Generates a professional criminological summary for all executed queries."""
    logger.info("Node [analyze_data]: Analysis started for all queries.")
    
    # Short-circuit if a security override was triggered
    for sql_err in state.get("all_generated_sql", []):
        if str(sql_err).startswith("ERROR: 🚨 SECURITY OVERRIDE"):
            return {
                **state,
                "analytical_summary": "🚨 SECURITY OVERRIDE: Unauthorized data modification query detected and blocked by KSP Protocols."
            }

    # We pass all queries and their corresponding truncated results to the LLM
    context_str = ""
    for i, query in enumerate(state["queries"]):
        results = state["all_sql_results"][i] if i < len(state["all_sql_results"]) else []
        sql_err = state["all_generated_sql"][i] if str(state["all_generated_sql"][i]).startswith("ERROR:") else ""
        
        context_str += f"\n--- Sub-Query {i+1}: {query} ---\n"
        if sql_err:
            context_str += f"Execution Error: {sql_err}\n"
        elif not results:
            context_str += "Result: No matching records found.\n"
        else:
            total_rows = len(results)
            if results and isinstance(results[0], dict) and 'Total_Matching_Records' in results[0]:
                total_rows = results[0]['Total_Matching_Records']
            truncated = results[:5]
            res_str = str(truncated)
            if len(res_str) > 1000:
                res_str = res_str[:1000] + "... [truncated]"
            context_str += f"The database returned {total_rows} total records. Here is a sample of the top 5 records for context:\n{res_str}\n"

    system_prompt = (
        "You are Aloka, an elite State Intelligence AI for the KSP. You must structure all your responses using advanced Markdown.\n"
        "DATA SUMMARY RULE: When summarizing SQL results, you will be given the TOTAL row count and a small data sample. You MUST state the true total row count in your analysis (e.g., 'The database found 800 records'). You MUST NEVER claim the total data size is only 5 rows just because you were only shown a 5-row sample. Base your summary on the total count provided.\n\n"
        "SYSTEM DIRECTIVE: You MUST respond in English. Do not translate headings, analysis, or text into Kannada, Hindi, or French unless the user's prompt is written 100% in that specific language. Default to English for all formatting.\n\n"
        "CRITICAL FORMATTING RULE:\n"
        "You must NEVER output giant walls of text or raw Markdown tables. You must format EVERY response using the exact structure below:\n\n"
        "## [Main Title of the Analysis]\n\n"
        "### Key Insights\n"
        "* [Bullet point 1 explaining a key finding]\n"
        "* [Bullet point 2 explaining a key finding]\n"
        "* [Bullet point 3 explaining a key finding]\n\n"
        "[One single conversational sentence asking the user directly if they need further filtering or details. You must speak directly to the user using first/second person (e.g., \"Would you like me to...\", \"Do you need further details on this?\"). Do NOT use third-person terms like \"the officer\".]\n\n"
        "CHART METADATA GENERATION:\n"
        "At the very end of your response, you MUST include a strict JSON block wrapped in ```json ... ``` that defines a chart for the data if applicable.\n"
        "If the user asks for a 'breakdown', 'distribution', 'comparison', 'count', or explicitly requests a chart, you MUST set `type` to 'pie' or 'bar'.\n"
        "Identify the text column for `label_column` and the numerical count/sum column for `value_column`.\n"
        "Format:\n"
        "```json\n"
        "{\n"
        "  \"type\": \"pie\" or \"bar\" or \"none\",\n"
        "  \"label_column\": \"column_name_for_labels\",\n"
        "  \"value_column\": \"column_name_for_values\"\n"
        "}\n"
        "```\n"
        "Only generate 'pie' or 'bar' if the data is aggregated (like counts, totals). Otherwise, return type 'none'."
    )
    
    prompt = (
        f"Original User Query: {state['user_query']}\n"
        f"Execution Results:\n{context_str}\n\n"
        f"Provide the final professional summary and the chart metadata JSON block."
    )
    
    summary_raw = await query_llm(prompt, system_prompt, state.get("chat_history"))
    
    # Extract JSON chart metadata
    chart_metadata = {"type": "none", "label_column": "", "value_column": ""}
    json_match = re.search(r"```json\s*({.*?})\s*```", summary_raw, re.DOTALL)
    if json_match:
        try:
            import json
            chart_metadata = json.loads(json_match.group(1))
            # Remove the json block from the visible text
            summary_raw = summary_raw.replace(json_match.group(0), "").strip()
        except Exception as e:
            logger.error(f"Failed to parse chart metadata JSON: {e}")
            
    return {
        **state,
        "analytical_summary": summary_raw,
        "chart_metadata": chart_metadata
    }


async def translation_output_node(state: State) -> State:
    """Bypasses automated translation since LLM generates in native language directly."""
    logger.info("Node [translation_output]: Bypassing since LLM handles native language internally.")
    return {
        **state,
        "final_output": state["analytical_summary"]
    }


# ==================================================
# 3. CONDITIONAL ROUTING LOGIC
# ==================================================
def route_intent(state: State) -> str:
    if state.get("intent") == "CHAT":
        return "chat_response"
    return "query_splitter"

def should_continue(state: State) -> str:
    err = state.get("sql_error", "")
    if "SECURITY OVERRIDE" in err or "Security Exception" in err:
        return "next_query_node"
    if err.startswith("Raw Backend Crash:") or err.startswith("AI Engine Error:") or "Unable to connect to the LLM" in err:
        return "next_query_node"
    if err and state.get("retry_count", 0) <= 3:
        return "self_correct"
    return "next_query_node"

def has_more_queries(state: State) -> str:
    if state.get("current_query_index", 0) < len(state.get("queries", [])):
        return "generate_sql"
    return "analyze_data"


# ==================================================
# 4. COMPILING THE STATE GRAPH
# ==================================================
workflow = StateGraph(State)

workflow.add_node("translation_input", translation_input_node)
workflow.add_node("intent_router", intent_router_node)
workflow.add_node("chat_response", chat_response_node)
workflow.add_node("query_splitter", query_splitter_node)
workflow.add_node("generate_sql", generate_sql_node)
workflow.add_node("execute_sql", execute_sql_node)
workflow.add_node("self_correct", self_correct_node)
workflow.add_node("next_query_node", next_query_node)
workflow.add_node("analyze_data", analyze_data_node)
workflow.add_node("translation_output", translation_output_node)

workflow.add_edge(START, "translation_input")
workflow.add_edge("translation_input", "intent_router")
workflow.add_conditional_edges("intent_router", route_intent, {"chat_response": "chat_response", "query_splitter": "query_splitter"})
workflow.add_edge("chat_response", "translation_output")

workflow.add_edge("query_splitter", "generate_sql")
workflow.add_edge("generate_sql", "execute_sql")
workflow.add_conditional_edges("execute_sql", should_continue, {"self_correct": "self_correct", "next_query_node": "next_query_node"})
workflow.add_edge("self_correct", "execute_sql")

workflow.add_conditional_edges("next_query_node", has_more_queries, {"generate_sql": "generate_sql", "analyze_data": "analyze_data"})

workflow.add_edge("analyze_data", "translation_output")
workflow.add_edge("translation_output", END)

checkpointer = MemorySaver()
agent_app = workflow.compile(checkpointer=checkpointer)


if __name__ == "__main__":
    import asyncio
    asyncio.run(agent_app.ainvoke({"user_query": "List all active cases and show all officers"}))

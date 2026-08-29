import os
from dotenv import load_dotenv

# Force load the variables from the .env file using explicit path
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
load_dotenv(dotenv_path=env_path, override=True)

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
print("[Groq] Initializing Cloud AI Engine via Groq...")

groq_key = os.getenv("GROQ_API_KEY", "").strip() or None
groq_model = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b").strip()

if groq_key:
    key_prefix = groq_key[:8] if len(groq_key) >= 8 else groq_key
    print(f"Loaded GROQ key: {key_prefix}...")
else:
    print("Loaded GROQ key: None")

print(f"Model: {groq_model}")

llm = ChatGroq(
    model=groq_model,
    api_key=groq_key,
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
                threat = "High" if data.get("countryCode") in ["RU", "CN", "KP"] else "Medium" if data.get("countryCode") != "IN" else "Low"
                return f"**IP Analysis: {ip_address}**\n- **Country**: {data.get('country')}\n- **Region**: {data.get('regionName')}\n- **ISP**: {data.get('isp')}\n- **Threat Level**: {threat} (Mocked)"
        return f"IP Analysis failed for {ip_address}"
    except Exception as e:
        return f"Error analyzing IP: {str(e)}"

# ==================================================
# AUTHORITATIVE DATABASE SCHEMA DEFINITION & ALIASES
# ==================================================
DB_SCHEMA = {
    "casemaster": {
        "columns": {
            "CaseMasterID": "INTEGER",
            "CrimeNo": "VARCHAR(50)",
            "CaseNo": "VARCHAR(50)",
            "CrimeRegisteredDate": "DATE",
            "PolicePersonID": "INTEGER",
            "PoliceStationID": "INTEGER",
            "CaseCategoryID": "INTEGER",
            "GravityOffenceID": "INTEGER",
            "CrimeMajorHeadID": "INTEGER",
            "CrimeMinorHeadID": "INTEGER",
            "CaseStatusID": "INTEGER",
            "CourtID": "INTEGER",
            "IncidentFromDate": "DATETIME",
            "IncidentToDate": "DATETIME",
            "InfoReceivedPSDate": "DATETIME",
            "latitude": "DECIMAL(10,6)",
            "longitude": "DECIMAL(10,6)",
            "BriefFacts": "TEXT"
        },
        "primary_key": "CaseMasterID",
        "foreign_keys": {
            "PolicePersonID": "employee.EmployeeID",
            "PoliceStationID": "unit.UnitID",
            "CaseCategoryID": "casecategory.CaseCategoryID",
            "GravityOffenceID": "gravityoffence.GravityOffenceID",
            "CrimeMajorHeadID": "crimehead.CrimeHeadID",
            "CrimeMinorHeadID": "crimesubhead.CrimeSubHeadID",
            "CaseStatusID": "casestatusmaster.CaseStatusID",
            "CourtID": "court.CourtID"
        },
        "aliases": ["case", "cases", "fir", "firs", "complaint case", "crime case", "fir record", "incident", "casemaster"]
    },
    "accused": {
        "columns": {
            "AccusedMasterID": "INTEGER",
            "CaseMasterID": "INTEGER",
            "AccusedName": "VARCHAR(255)",
            "AgeYear": "INTEGER",
            "GenderID": "VARCHAR(10)",
            "PersonID": "VARCHAR(50)"
        },
        "primary_key": "AccusedMasterID",
        "foreign_keys": {
            "CaseMasterID": "casemaster.CaseMasterID"
        },
        "aliases": ["accused", "accused person", "accused persons", "offender", "offenders", "person accused", "culprit", "suspect", "accused name"]
    },
    "victim": {
        "columns": {
            "VictimMasterID": "INTEGER",
            "CaseMasterID": "INTEGER",
            "VictimName": "VARCHAR(255)",
            "AgeYear": "INTEGER",
            "GenderID": "VARCHAR(10)",
            "VictimPolice": "VARCHAR(50)"
        },
        "primary_key": "VictimMasterID",
        "foreign_keys": {
            "CaseMasterID": "casemaster.CaseMasterID"
        },
        "aliases": ["victim", "victims", "affected person", "victim of crime", "suffered person"]
    },
    "complainantdetails": {
        "columns": {
            "ComplainantID": "INTEGER",
            "CaseMasterID": "INTEGER",
            "ComplainantName": "VARCHAR(255)",
            "AgeYear": "INTEGER",
            "OccupationID": "INTEGER",
            "ReligionID": "INTEGER",
            "CasteID": "INTEGER",
            "GenderID": "VARCHAR(10)"
        },
        "primary_key": "ComplainantID",
        "foreign_keys": {
            "CaseMasterID": "casemaster.CaseMasterID",
            "OccupationID": "occupationmaster.OccupationID",
            "ReligionID": "religionmaster.ReligionID",
            "CasteID": "castemaster.caste_master_id"
        },
        "aliases": ["complainant", "complainants", "person who filed complaint", "person who reported case", "reporter", "informant", "filed complaint", "filed the complaint"]
    },
    "arrestsurrender": {
        "columns": {
            "ArrestSurrenderID": "INTEGER",
            "CaseMasterID": "INTEGER",
            "ArrestSurrenderTypeID": "INTEGER",
            "ArrestSurrenderDate": "DATE",
            "ArrestSurrenderStateId": "INTEGER",
            "ArrestSurrenderDistrictId": "INTEGER",
            "PoliceStationID": "INTEGER",
            "IOID": "INTEGER",
            "CourtID": "INTEGER",
            "AccusedMasterID": "INTEGER",
            "IsAccused": "BIT",
            "IsComplainantAccused": "BIT"
        },
        "primary_key": "ArrestSurrenderID",
        "foreign_keys": {
            "CaseMasterID": "casemaster.CaseMasterID",
            "AccusedMasterID": "accused.AccusedMasterID",
            "PoliceStationID": "unit.UnitID",
            "IOID": "employee.EmployeeID",
            "CourtID": "court.CourtID",
            "ArrestSurrenderDistrictId": "district.DistrictID",
            "ArrestSurrenderStateId": "state.StateID"
        },
        "aliases": ["arrest", "arrests", "arrested", "arrested person", "surrender", "detained", "was anyone arrested"]
    },
    "actsectionassociation": {
        "columns": {
            "CaseMasterID": "INTEGER",
            "ActID": "VARCHAR(50)",
            "SectionID": "VARCHAR(50)",
            "ActOrderID": "INTEGER",
            "SectionOrderID": "INTEGER"
        },
        "primary_key": None,
        "foreign_keys": {
            "CaseMasterID": "casemaster.CaseMasterID",
            "ActID": "act.ActCode",
            "SectionID": "section.SectionCode"
        },
        "aliases": ["applied laws", "sections applied", "acts applied", "legal sections", "offence sections", "sections", "acts"]
    },
    "act": {
        "columns": {
            "ActCode": "VARCHAR(50)",
            "ActDescription": "VARCHAR(255)",
            "ShortName": "VARCHAR(100)",
            "Active": "BIT"
        },
        "primary_key": "ActCode",
        "foreign_keys": {},
        "aliases": ["act", "acts", "law", "statute", "legal act"]
    },
    "section": {
        "columns": {
            "ActCode": "VARCHAR(50)",
            "SectionCode": "VARCHAR(50)",
            "SectionDescription": "VARCHAR(255)",
            "Active": "BIT"
        },
        "primary_key": "SectionCode",
        "foreign_keys": {
            "ActCode": "act.ActCode"
        },
        "aliases": ["section", "sections", "section of law", "legal section", "what sections were applied"]
    },
    "crimehead": {
        "columns": {
            "CrimeHeadID": "INTEGER",
            "CrimeGroupName": "VARCHAR(255)",
            "Active": "BIT"
        },
        "primary_key": "CrimeHeadID",
        "foreign_keys": {},
        "aliases": ["major head", "crime group", "crime category", "major head name", "crimehead"]
    },
    "crimesubhead": {
        "columns": {
            "CrimeSubHeadID": "INTEGER",
            "CrimeHeadID": "INTEGER",
            "CrimeHeadName": "VARCHAR(255)",
            "SeqID": "INTEGER"
        },
        "primary_key": "CrimeSubHeadID",
        "foreign_keys": {
            "CrimeHeadID": "crimehead.CrimeHeadID"
        },
        "aliases": ["minor head", "crime sub head", "sub head", "minor crime type", "crimesubhead"]
    },
    "employee": {
        "columns": {
            "EmployeeID": "INTEGER",
            "DistrictID": "INTEGER",
            "UnitID": "INTEGER",
            "RankID": "INTEGER",
            "DesignationID": "INTEGER",
            "KGID": "VARCHAR(50)",
            "FirstName": "VARCHAR(100)",
            "EmployeeDOB": "DATE",
            "GenderID": "VARCHAR(10)",
            "BloodGroupID": "INTEGER",
            "PhysicallyChallenged": "BIT",
            "AppointmentDate": "DATE"
        },
        "primary_key": "EmployeeID",
        "foreign_keys": {
            "UnitID": "unit.UnitID",
            "DistrictID": "district.DistrictID",
            "RankID": "rank.RankID",
            "DesignationID": "designation.DesignationID"
        },
        "aliases": ["officer", "officers", "police officer", "investigating officer", "io", "police person", "registering officer", "employee"]
    },
    "unit": {
        "columns": {
            "UnitID": "INTEGER",
            "UnitName": "VARCHAR(255)",
            "TypeID": "INTEGER",
            "ParentUnit": "INTEGER",
            "NationalityID": "INTEGER",
            "StateID": "INTEGER",
            "DistrictID": "INTEGER",
            "Active": "BIT"
        },
        "primary_key": "UnitID",
        "foreign_keys": {
            "TypeID": "unittype.UnitTypeID",
            "StateID": "state.StateID",
            "DistrictID": "district.DistrictID"
        },
        "aliases": ["police station", "station", "police unit", "ps", "unit", "police stations"]
    },
    "court": {
        "columns": {
            "CourtID": "INTEGER",
            "CourtName": "VARCHAR(255)",
            "DistrictID": "INTEGER",
            "StateID": "INTEGER",
            "Active": "BIT"
        },
        "primary_key": "CourtID",
        "foreign_keys": {
            "DistrictID": "district.DistrictID",
            "StateID": "state.StateID"
        },
        "aliases": ["court", "courts", "court handling case", "judiciary", "law court"]
    },
    "district": {
        "columns": {
            "DistrictID": "INTEGER",
            "DistrictName": "VARCHAR(100)",
            "StateID": "INTEGER",
            "Active": "BIT"
        },
        "primary_key": "DistrictID",
        "foreign_keys": {
            "StateID": "state.StateID"
        },
        "aliases": ["district", "districts", "dist"]
    },
    "state": {
        "columns": {
            "StateID": "INTEGER",
            "StateName": "VARCHAR(100)",
            "NationalityID": "INTEGER",
            "Active": "BIT"
        },
        "primary_key": "StateID",
        "foreign_keys": {},
        "aliases": ["state", "states"]
    },
    "chargesheetdetails": {
        "columns": {
            "CSID": "INTEGER",
            "CaseMasterID": "INTEGER",
            "csdate": "DATE",
            "cstype": "VARCHAR(50)",
            "PolicePersonID": "INTEGER"
        },
        "primary_key": "CSID",
        "foreign_keys": {
            "CaseMasterID": "casemaster.CaseMasterID",
            "PolicePersonID": "employee.EmployeeID"
        },
        "aliases": ["charge sheet", "chargesheet", "cs"]
    },
    "castemaster": {
        "columns": {
            "caste_master_id": "INTEGER",
            "caste_master_name": "VARCHAR(100)"
        },
        "primary_key": "caste_master_id",
        "foreign_keys": {},
        "aliases": ["caste"]
    },
    "religionmaster": {
        "columns": {
            "ReligionID": "INTEGER",
            "ReligionName": "VARCHAR(100)"
        },
        "primary_key": "ReligionID",
        "foreign_keys": {},
        "aliases": ["religion"]
    },
    "occupationmaster": {
        "columns": {
            "OccupationID": "INTEGER",
            "OccupationName": "VARCHAR(100)"
        },
        "primary_key": "OccupationID",
        "foreign_keys": {},
        "aliases": ["occupation", "job", "profession"]
    },
    "casecategory": {
        "columns": {
            "CaseCategoryID": "INTEGER",
            "LookupValue": "VARCHAR(100)"
        },
        "primary_key": "CaseCategoryID",
        "foreign_keys": {},
        "aliases": ["case category", "category"]
    },
    "casestatusmaster": {
        "columns": {
            "CaseStatusID": "INTEGER",
            "CaseStatusName": "VARCHAR(100)"
        },
        "primary_key": "CaseStatusID",
        "foreign_keys": {},
        "aliases": ["case status", "status"]
    },
    "gravityoffence": {
        "columns": {
            "GravityOffenceID": "INTEGER",
            "LookupValue": "VARCHAR(100)"
        },
        "primary_key": "GravityOffenceID",
        "foreign_keys": {},
        "aliases": ["gravity offence", "gravity", "seriousness", "serious cases"]
    },
    "designation": {
        "columns": {
            "DesignationID": "INTEGER",
            "DesignationName": "VARCHAR(100)",
            "Active": "BIT",
            "SortOrder": "INTEGER"
        },
        "primary_key": "DesignationID",
        "foreign_keys": {},
        "aliases": ["designation"]
    },
    "rank": {
        "columns": {
            "RankID": "INTEGER",
            "RankName": "VARCHAR(100)",
            "Hierarchy": "INTEGER",
            "Active": "BIT"
        },
        "primary_key": "RankID",
        "foreign_keys": {},
        "aliases": ["rank", "police rank"]
    },
    "unittype": {
        "columns": {
            "UnitTypeID": "INTEGER",
            "UnitTypeName": "VARCHAR(100)",
            "CityDistState": "VARCHAR(100)",
            "Hierarchy": "INTEGER",
            "Active": "BIT"
        },
        "primary_key": "UnitTypeID",
        "foreign_keys": {},
        "aliases": ["unit type"]
    },
    "crimeheadactsection": {
        "columns": {
            "CrimeHeadID": "INTEGER",
            "ActCode": "VARCHAR(50)",
            "SectionCode": "VARCHAR(50)"
        },
        "primary_key": None,
        "foreign_keys": {
            "CrimeHeadID": "crimehead.CrimeHeadID"
        },
        "aliases": ["crime head act section"]
    }
}

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
    
    # Structured Query Intelligence
    query_plan: Optional[dict]
    needs_clarification: bool
    clarification_question: str
    
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
        "query_plan": None,
        "needs_clarification": False,
        "clarification_question": "",
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
    ip_match = re.search(r' (?:[0-9]{1,3}\.){3}[0-9]{1,3} ', state["translated_query"])
    if ip_match:
        ip = ip_match.group(0)
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
        "all_generated_sql": ["CHITCHAT"],
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


async def query_planner_node(state: State) -> State:
    """
    Step A-B: Parses natural-language queries into structured JSON Query Plans.
    Resolves conversational context (e.g. 'this case' -> 'KSP-CASE-0004') from chat history
    and detects ambiguous queries (e.g., 'Show Ravi's case') requiring clarification.
    """
    current_query = state["queries"][state["current_query_index"]]
    logger.info(f"Node [query_planner]: Planning query '{current_query}'")
    
    # ── Context Resolution Helper: Scan history for case numbers ──
    context_case_no = None
    chat_hist = state.get("chat_history", []) or []
    for msg in reversed(chat_hist):
        content = msg.get("content", "")
        match = re.search(r'KSP-CASE-\d+', content, re.IGNORECASE)
        if match:
            context_case_no = match.group(0).upper()
            break
            
    system_prompt = (
        "You are an expert Query Planner and Intent Understanding engine for the Karnataka State Police AI (Aloka).\n"
        "Your task is to parse a natural-language query and conversation history into a strict JSON Query Plan.\n\n"
        "DATABASE CONCEPTS & TABLE MAPPING:\n"
        "- casemaster: case, cases, FIR, FIRs, complaint case, crime case, FIR record, incident (Identifier: CaseNo e.g., 'KSP-CASE-0004')\n"
        "- accused: accused, accused person, offender, culprit, suspect (Columns: AccusedName, AgeYear, GenderID, PersonID)\n"
        "- victim: victim, victims, affected person, suffered person (Columns: VictimName, AgeYear, GenderID)\n"
        "- complainantdetails: complainant, person who filed complaint, reporter, informant (Columns: ComplainantName, AgeYear, GenderID)\n"
        "- arrestsurrender: arrest, arrested, detained, surrender, was anyone arrested (Columns: ArrestSurrenderDate, IOID, PoliceStationID)\n"
        "- employee: officer, police officer, investigating officer, IO, registering officer (Columns: FirstName, EmployeeID, RankID)\n"
        "- unit: police station, station, police unit, PS (Columns: UnitName, UnitID)\n"
        "- court: court, law court, judiciary (Columns: CourtName, CourtID)\n"
        "- act / section / actsectionassociation: sections, acts, applied laws, section of law\n"
        "- crimehead: major head, crime group, category\n"
        "- crimesubhead: minor head, sub head\n"
        "- castemaster / religionmaster / occupationmaster: caste, religion, occupation lookup\n\n"
        "CONVERSATIONAL CONTEXT RULES:\n"
        "1. Inspect the query and history. If the user refers to 'this case', 'the case', 'the accused', 'the victim', 'was anyone arrested', 'who registered the FIR', or follow-up questions, resolve the case number (e.g. 'KSP-CASE-0004') from previous turns.\n"
        f"2. Current active case from history: '{context_case_no}'. If no case is in the current prompt but 'this case' is implied, use '{context_case_no}'.\n"
        "3. If a case number (e.g. 'KSP-CASE-0004') is present or resolved, ALWAYS include filter: casemaster.CaseNo = 'KSP-CASE-0004'.\n\n"
        "AMBIGUITY & CLARIFICATION RULES:\n"
        "1. If the user asks about a person's name (e.g., 'Who is Ravi's case?', 'Show Ravi's case', 'Show Ramesh') without specifying whether that person is an accused, victim, complainant, or police officer, you MUST set \"ambiguous\": true, and set \"clarification_question\": \"Do you mean cases where [Name] is an accused, victim, complainant, or police officer?\".\n"
        "2. If the user explicitly specifies the role (e.g., 'Who are the accused in case KSP-CASE-0004?', 'Show accused Ravi', 'Who filed complaint?'), set \"ambiguous\": false.\n\n"
        "JSON OUTPUT FORMAT STRICTLY REQUIRED:\n"
        "```json\n"
        "{\n"
        "  \"intent\": \"find_accused | find_victim | find_complainant | find_officer | find_station | find_arrested | find_court | find_sections | find_case | count_cases | general_search\",\n"
        "  \"target_tables\": [\"casemaster\", \"accused\"],\n"
        "  \"ambiguous\": false,\n"
        "  \"clarification_question\": \"\",\n"
        "  \"entities\": {\n"
        "    \"case_no\": \"KSP-CASE-0004\" or null,\n"
        "    \"person_name\": \"Ravi\" or null\n"
        "  },\n"
        "  \"filters\": [\n"
        "    {\"table\": \"casemaster\", \"column\": \"CaseNo\", \"operator\": \"=\", \"value\": \"KSP-CASE-0004\"}\n"
        "  ],\n"
        "  \"requested_fields\": [\"accused.AccusedName\", \"accused.AgeYear\", \"accused.GenderID\"],\n"
        "  \"relationships_required\": [\n"
        "    {\"from\": \"casemaster.CaseMasterID\", \"to\": \"accused.CaseMasterID\"}\n"
        "  ]\n"
        "}\n"
        "```\n"
        "Output ONLY the raw JSON object."
    )

    prompt = f"User Request: {current_query}\n\nGenerate JSON Query Plan:"
    result = await query_llm(prompt, system_prompt, chat_hist)
    
    clean_json = re.sub(r'```(?:json)?\n(.*?)```', r'\1', result, flags=re.DOTALL).strip()
    clean_json = clean_json.strip('`').strip()
    
    query_plan = {}
    try:
        query_plan = json.loads(clean_json)
    except Exception as e:
        logger.error(f"Failed to parse query plan JSON: {e}. Raw: {result}")
        query_plan = {
            "intent": "general_search",
            "target_tables": ["casemaster"],
            "ambiguous": False,
            "clarification_question": "",
            "entities": {"case_no": context_case_no, "person_name": None},
            "filters": [{"table": "casemaster", "column": "CaseNo", "operator": "=", "value": context_case_no}] if context_case_no else [],
            "requested_fields": [],
            "relationships_required": []
        }
        
    return {
        **state,
        "query_plan": query_plan
    }


async def schema_validator_node(state: State) -> State:
    """
    Step C: Validates the generated query plan against the authoritative DB_SCHEMA.
    Validates tables, columns, and foreign-key join paths.
    If ambiguity is flagged, prepares clarification routing.
    """
    plan = state.get("query_plan", {})
    logger.info(f"Node [schema_validator]: Validating plan for intent '{plan.get('intent')}'")
    
    if plan.get("ambiguous") or plan.get("clarification_question"):
        clarification_msg = plan.get("clarification_question") or "Could you please clarify your request?"
        logger.info(f"Ambiguity detected. Prepared clarification: {clarification_msg}")
        return {
            **state,
            "needs_clarification": True,
            "clarification_question": clarification_msg
        }
        
    validated_target_tables = []
    for tbl in plan.get("target_tables", []):
        tbl_lower = tbl.lower()
        if tbl_lower in DB_SCHEMA:
            validated_target_tables.append(tbl_lower)
        else:
            matched = False
            for schema_tbl, details in DB_SCHEMA.items():
                if tbl_lower in details["aliases"]:
                    validated_target_tables.append(schema_tbl)
                    matched = True
                    break
            if not matched:
                logger.warning(f"Unrecognized table '{tbl}' removed during schema validation.")
                
    if not validated_target_tables:
        validated_target_tables = ["casemaster"]
        
    validated_filters = []
    for flt in plan.get("filters", []):
        tbl = flt.get("table", "").lower()
        col = flt.get("column", "")
        if tbl in DB_SCHEMA and col in DB_SCHEMA[tbl]["columns"]:
            validated_filters.append({
                "table": tbl,
                "column": col,
                "operator": flt.get("operator", "="),
                "value": flt.get("value")
            })
            
    plan["target_tables"] = validated_target_tables
    plan["filters"] = validated_filters
    
    return {
        **state,
        "query_plan": plan,
        "needs_clarification": False,
        "clarification_question": ""
    }


async def generate_sql_node(state: State) -> State:
    """
    Step D: Converts the validated query plan into an exact MySQL SELECT statement.
    """
    if state.get("needs_clarification"):
        return {
            **state,
            "generated_sql": "CLARIFICATION"
        }

    current_query = state["queries"][state["current_query_index"]]
    query_plan = state.get("query_plan", {})
    logger.info(f"Node [generate_sql]: Generating SQL for sub-query '{current_query}' from validated plan.")

    schema_text = []
    for tbl, info in DB_SCHEMA.items():
        cols_str = ", ".join([f"{col} ({dt})" for col, dt in info["columns"].items()])
        fks_str = ", ".join([f"{k} -> {v}" for k, v in info["foreign_keys"].items()])
        schema_text.append(f"- {tbl} ({cols_str}) | FKs: [{fks_str}]")
    core_schema_str = "\n".join(schema_text)

    system_prompt = (
        "CRITICAL SECURITY DIRECTIVE: You are a read-only State Intelligence AI. If a user asks to modify, delete, drop, update, or alter any data (e.g., 'delete employee', 'update record'), you MUST NOT explain how to do it. You MUST NOT generate example SQL. You must immediately abort the response and output ONLY this exact string: \n"
        "'🚨 SECURITY OVERRIDE: Unauthorized data modification query detected and blocked by KSP Protocols.'\n\n"
        "You are Aloka, an expert SQL generator for the Karnataka State Police. Convert the validated Query Plan into an exact MySQL SELECT statement.\n\n"
        f"AUTHORITATIVE MYSQL SCHEMA (Strictly use ONLY these lowercase table names and exact column cases):\n{core_schema_str}\n\n"
        "STRICT SQL GENERATION RULES:\n"
        "1. TABLE NAMES: Must be strictly lowercase (e.g., casemaster, accused, victim, complainantdetails, employee, unit, court, district, state, arrestsurrender, act, section, actsectionassociation, crimehead, crimesubhead, castemaster, religionmaster, occupationmaster).\n"
        "2. COLUMN NAMES: Must match the exact casing specified in the schema definition (e.g., CaseMasterID, CrimeNo, CaseNo, AccusedName, AgeYear, GenderID, FirstName, UnitName, caste_master_id, caste_master_name).\n"
        "3. CASE IDENTIFIER: Always filter case IDs like 'KSP-CASE-XXXX' using `casemaster.CaseNo = 'KSP-CASE-XXXX'`. Do NOT filter on `CrimeNo`.\n"
        "4. JOINS: Join tables strictly using foreign key relationships (e.g., casemaster.PoliceStationID = unit.UnitID, casemaster.PolicePersonID = employee.EmployeeID, accused.CaseMasterID = casemaster.CaseMasterID, victim.CaseMasterID = casemaster.CaseMasterID, complainantdetails.CaseMasterID = casemaster.CaseMasterID).\n"
        "5. SECTION JOIN: Join section on BOTH `actsectionassociation.SectionID = section.SectionCode` AND `actsectionassociation.ActID = section.ActCode`.\n"
        "6. CASTE / RELIGION / OCCUPATION: Join complainantdetails on CasteID = castemaster.caste_master_id, ReligionID = religionmaster.ReligionID, OccupationID = occupationmaster.OccupationID.\n"
        "7. DUAL MODE PROCESSING:\n"
        "   - Group A (Analytical/Summary): If the user asks for high-level metrics, counts, or groupings, DO NOT use COUNT(*) OVER() and DO NOT append LIMIT 15. Let the database group naturally.\n"
        "   - Group B (Raw List): If the user asks for a massive list of individual records, strictly inject `COUNT(*) OVER() AS Total_Matching_Records` into the SELECT statement and append a strict `LIMIT 15`.\n"
        "8. OUTPUT FORMAT: Output ONLY the raw SQL SELECT query without markdown formatting."
    )

    prompt = (
        f"Natural Language Query: {current_query}\n"
        f"Validated Query Plan: {json.dumps(query_plan, indent=2)}\n\n"
        f"SQL Query:"
    )

    sql = await query_llm(prompt, system_prompt, state.get("chat_history"))
    sql = sql.replace("```sql", "").replace("```", "").strip()

    return {
        **state,
        "generated_sql": sql
    }


async def execute_sql_node(state: State) -> State:
    """
    Step E-F: Securely runs the generated SQL query with pre-execution checks, error catching,
    and graceful handling of empty result sets.
    """
    if state.get("needs_clarification") or state.get("generated_sql") == "CLARIFICATION":
        return {
            **state,
            "sql_results": [],
            "sql_results_total": 0,
            "sql_error": "",
            "analytical_summary": state.get("clarification_question", "Could you please clarify your request?")
        }

    raw_sql = state["generated_sql"]
    
    # Fail-safe Regex Cleanup
    sql = re.sub(r'```(?:sql)?\n(.*?)```', r'\1', raw_sql, flags=re.DOTALL).strip()
    sql = sql.strip('`').strip()
    
    clean_sql = re.sub(r'(?i)\bLIMIT\s+\d+\b', '', sql)
    clean_sql = re.sub(r'(?i)\bOFFSET\s+\d+\b', '', clean_sql)
    clean_sql = clean_sql.strip().rstrip(';')
    
    limit = 15
    paginated_sql = f"{clean_sql} LIMIT {limit + 1} OFFSET 0"
    
    logger.info(f"Node [execute_sql]: Executing SQL: {paginated_sql}")
    
    # SECURITY GUARDRAILS & READ-ONLY ENFORCEMENT
    forbidden_keywords = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE", "GRANT", "REVOKE", "CREATE"]
    if any(keyword in paginated_sql.upper() for keyword in forbidden_keywords):
        logger.warning(f"SECURITY OVERRIDE: Destructive query blocked: {paginated_sql}")
        return {
            **state,
            "sql_results": [],
            "sql_results_total": 0,
            "sql_error": "🚨 SECURITY OVERRIDE: Unauthorized data modification query detected and blocked by KSP Protocols."
        }
        
    try:
        engine = get_db_connection()
        with engine.connect() as conn:
            result = conn.execute(text(paginated_sql))
            results = [dict(row._mapping) for row in result.fetchall()] if result.returns_rows else []
            
            total_records = len(results)
            
            if total_records == 0:
                logger.warning("Query returned 0 rows — no matching records found in database.")
            else:
                logger.info(f"Query returned {total_records} total row(s).")
            
            first_page = results[:limit]
                
            return {
                **state,
                "generated_sql": clean_sql,
                "sql_results": first_page,
                "sql_results_total": total_records,
                "sql_error": ""
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
    
    schema_text = []
    for tbl, info in DB_SCHEMA.items():
        cols_str = ", ".join([f"{col} ({dt})" for col, dt in info["columns"].items()])
        schema_text.append(f"- {tbl} ({cols_str})")
    core_schema_str = "\n".join(schema_text)

    system_prompt = (
        "You are an expert SQL debugger for the Karnataka Police. You correct broken MySQL queries.\n\n"
        f"Core Schema (Strictly use ONLY these lowercase table names and their exact column cases):\n{core_schema_str}\n\n"
        "STRICT CONSTRAINTS:\n"
        "1. Output ONLY the exact, raw SQL query without markdown formatting.\n"
        "2. Table names MUST be strictly lowercase (e.g. casemaster, unit, employee, accused, victim, complainantdetails).\n"
        "3. Column names MUST match the exact casing from the schema definition (e.g. CaseMasterID, AccusedName, caste_master_id)."
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
        results = state.get("sql_results", [])
        all_results.append(results)
        
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
    """Step G: Generates a professional criminological summary or clarification response."""
    logger.info("Node [analyze_data]: Analysis started for all queries.")
    
    if state.get("needs_clarification"):
        return {
            **state,
            "analytical_summary": state.get("clarification_question", "Could you please clarify your request?")
        }
        
    # Short-circuit if a security override was triggered
    for sql_err in state.get("all_generated_sql", []):
        if str(sql_err).startswith("ERROR: 🚨 SECURITY OVERRIDE"):
            return {
                **state,
                "analytical_summary": "🚨 SECURITY OVERRIDE: Unauthorized data modification query detected and blocked by KSP Protocols."
            }

    context_str = ""
    for i, query in enumerate(state["queries"]):
        results = state["all_sql_results"][i] if i < len(state["all_sql_results"]) else []
        sql_err = state["all_generated_sql"][i] if str(state["all_generated_sql"][i]).startswith("ERROR:") else ""
        
        context_str += f"\n--- Sub-Query {i+1}: {query} ---\n"
        if sql_err:
            context_str += f"Execution Error: {sql_err}\n"
        elif not results:
            context_str += "Result: I couldn't find any matching records for that request.\n"
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
        "You are Aloka, an elite State Intelligence AI for the KSP. You structure all responses using clear Markdown.\n"
        "DATA SUMMARY RULE: When summarizing SQL results, state the true total row count provided. If no matching records were found, state clearly: 'I couldn't find any matching records for that request.' Do NOT report zero-row results as database errors.\n\n"
        "SYSTEM DIRECTIVE: Respond in English unless the prompt is strictly in another language.\n\n"
        "FORMATTING RULE:\n"
        "## [Main Title of the Analysis]\n\n"
        "### Key Insights\n"
        "* [Bullet point 1]\n"
        "* [Bullet point 2]\n\n"
        "[One conversational sentence asking the user if they need further details or filtering.]\n\n"
        "CHART METADATA GENERATION:\n"
        "At the end of your response, output a strict JSON block wrapped in ```json ... ``` defining a chart if applicable.\n"
        "Format:\n"
        "```json\n"
        "{\n"
        "  \"type\": \"pie\" or \"bar\" or \"none\",\n"
        "  \"label_column\": \"column_name_for_labels\",\n"
        "  \"value_column\": \"column_name_for_values\"\n"
        "}\n"
        "```"
    )
    
    prompt = (
        f"Original User Query: {state['user_query']}\n"
        f"Execution Results:\n{context_str}\n\n"
        f"Provide the final professional summary and chart metadata JSON block."
    )
    
    summary_raw = await query_llm(prompt, system_prompt, state.get("chat_history"))
    
    chart_metadata = {"type": "none", "label_column": "", "value_column": ""}
    json_match = re.search(r"```json\s*({.*?})\s*```", summary_raw, re.DOTALL)
    if json_match:
        try:
            chart_metadata = json.loads(json_match.group(1))
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
    elif state.get("intent") == "CYBER":
        return "cyber_node"
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
        return "query_planner"
    return "analyze_data"


# ==================================================
# 4. COMPILING THE STATE GRAPH
# ==================================================
workflow = StateGraph(State)

workflow.add_node("translation_input", translation_input_node)
workflow.add_node("intent_router", intent_router_node)
workflow.add_node("chat_response", chat_response_node)
workflow.add_node("cyber_node", cyber_node)
workflow.add_node("query_splitter", query_splitter_node)
workflow.add_node("query_planner", query_planner_node)
workflow.add_node("schema_validator", schema_validator_node)
workflow.add_node("generate_sql", generate_sql_node)
workflow.add_node("execute_sql", execute_sql_node)
workflow.add_node("self_correct", self_correct_node)
workflow.add_node("next_query_node", next_query_node)
workflow.add_node("analyze_data", analyze_data_node)
workflow.add_node("translation_output", translation_output_node)

workflow.add_edge(START, "translation_input")
workflow.add_edge("translation_input", "intent_router")
workflow.add_conditional_edges("intent_router", route_intent, {"chat_response": "chat_response", "cyber_node": "cyber_node", "query_splitter": "query_splitter"})
workflow.add_edge("chat_response", "translation_output")
workflow.add_edge("cyber_node", "translation_output")

workflow.add_edge("query_splitter", "query_planner")
workflow.add_edge("query_planner", "schema_validator")
workflow.add_edge("schema_validator", "generate_sql")
workflow.add_edge("generate_sql", "execute_sql")
workflow.add_conditional_edges("execute_sql", should_continue, {"self_correct": "self_correct", "next_query_node": "next_query_node"})
workflow.add_edge("self_correct", "execute_sql")

workflow.add_conditional_edges("next_query_node", has_more_queries, {"query_planner": "query_planner", "analyze_data": "analyze_data"})

workflow.add_edge("analyze_data", "translation_output")
workflow.add_edge("translation_output", END)

checkpointer = MemorySaver()
agent_app = workflow.compile(checkpointer=checkpointer)


if __name__ == "__main__":
    import asyncio
    asyncio.run(agent_app.ainvoke({"user_query": "List all active cases and show all officers"}, config={"configurable": {"thread_id": "main_thread"}}))

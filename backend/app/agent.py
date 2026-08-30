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
# PHASE 2 CONVERSATION CONTEXT MANAGER HELPER
# ==================================================
def resolve_conversation_context(user_query: str, chat_history: Optional[List[dict]] = None) -> dict:
    """
    Phase 2 Structured Conversation Context Manager:
    Parses user_query and chat_history to maintain active conversation state.
    Handles:
    - Explicit context reset ("forget that case", "start a new search")
    - Explicit case mentions & context switching ("Now show KSP-CASE-0012")
    - Pronoun / reference resolution ("this case", "the victim", "the court", "what happened")
    - Global query detection to avoid false context ("how many cases are there in total?")
    - Multi-case ambiguity detection (multiple cases in history + vague pronoun)
    - Multi-turn entity context tracking (person name and station name)
    """
    def extract_person_name(text: str) -> Optional[str]:
        # 1. "Name's case" or "Name case"
        match = re.search(r'\b([A-Z][a-z]+)(?:\'s|\b)\s+case\b', text)
        if match:
            name = match.group(1).strip()
            if name.lower() not in ["this", "that", "the", "active", "total", "police", "court"]:
                return name
                
        # 2. "involving/about/of/by Name"
        match = re.search(r'\b(?:involving|about|of|by|accused|victim|officer|involve)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b', text, re.IGNORECASE)
        if match:
            name = match.group(1).strip()
            # Ignore common words
            if name.lower() not in ["case", "fir", "police", "station", "court", "victim", "accused", "officer", "incident", "this", "that", "there"]:
                return name
                
        # 3. Capitalized multi-word names (e.g. Vijay Mishra)
        for name in re.findall(r'\b([A-Z][a-z]+\s+[A-Z][a-z]+)\b', text):
            first_word = name.split()[0].lower()
            second_word = name.split()[1].lower()
            if first_word not in ["police", "station", "court", "active", "total", "how", "show", "what", "which", "state"] and \
               second_word not in ["police", "station", "court", "case", "cases", "fir", "firs", "status", "date"]:
                return name
        return None

    def extract_station_name(text: str) -> Optional[str]:
        match = re.search(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:Police\s+Station|PS|Unit))\b', text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return None

    chat_hist = chat_history or []
    query_lower = user_query.lower().strip()
    
    # ── 1. Check for Explicit Context Reset ──
    reset_keywords = ["forget the previous", "forget that case", "forget case", "reset context", "clear context", "start a new search", "start new search", "forget previous"]
    if any(kw in query_lower for kw in reset_keywords):
        logger.info("[ContextManager]: Explicit context reset requested.")
        return {
            "active_case": None,
            "active_person": None,
            "active_station": None,
            "recent_cases": [],
            "context_reset": True,
            "is_global_query": False,
            "context_ambiguous": False,
            "context_missing": False,
            "clarification_prompt": None
        }

    # ── 2. Check for Explicit Case Mentions in current query ──
    explicit_cases = [m.upper() for m in re.findall(r'\bKSP-CASE-\d+\b', user_query, re.IGNORECASE)]
    
    # ── 3. Scan chat_history for recent cases, person, and station ──
    recent_cases = []
    active_person = None
    active_station = None
    
    for msg in reversed(chat_hist):
        content = msg.get("content", "")
        if any(kw in content.lower() for kw in reset_keywords):
            break
        matches = [m.upper() for m in re.findall(r'\bKSP-CASE-\d+\b', content, re.IGNORECASE)]
        for m in matches:
            if m not in recent_cases:
                recent_cases.append(m)
        if not active_person:
            active_person = extract_person_name(content)
        if not active_station:
            active_station = extract_station_name(content)

    # ── 4. Determine Active Case & Context Switching ──
    active_case = None
    if explicit_cases:
        # The newest case mentioned in the user's current query overrides previous context!
        active_case = explicit_cases[-1]
        logger.info(f"[ContextManager]: Explicit case found in query: {active_case}")
    elif recent_cases:
        active_case = recent_cases[0]
        logger.info(f"[ContextManager]: Inherited active case from history: {active_case}")

    # Check for current query updates to person/station
    current_person = extract_person_name(user_query)
    current_station = extract_station_name(user_query)
    
    if current_person:
        active_person = current_person
    elif not active_person:
        # Scan user messages in history backwards
        for msg in reversed(chat_hist):
            if msg.get("role") == "user":
                p = extract_person_name(msg.get("content", ""))
                if p:
                    active_person = p
                    break
                    
    if current_station:
        active_station = current_station
    elif not active_station:
        # Scan user messages in history backwards
        for msg in reversed(chat_hist):
            if msg.get("role") == "user":
                s = extract_station_name(msg.get("content", ""))
                if s:
                    active_station = s
                    break

    # ── 5. Check for Global Query (Avoid False Context) ──
    global_analytical_terms = [
        "over time", "by date", "by year", "by month", "trend", "trends", "timeline",
        "by status", "by category", "by police station", "by station",
        "per police station", "per station", "for each police station", "for each station",
        "distribution of cases", "cases by", "number of cases registered", "cases registered over time",
        "how many cases", "total cases", "total number of cases", "cases registered in total",
        "count of cases", "cases across all", "all police stations", "list all cases", "show all cases",
        "across all stations", "top 5", "top 10", "most cases", "highest cases"
    ]
    is_global_query = any(kw in query_lower for kw in global_analytical_terms)
    
    pronoun_terms = ["this case", "in this case", "for this case", "the case", "that case", "this fir", "the fir", "this incident"]
    has_explicit_pronoun = any(pt in query_lower for pt in pronoun_terms)
    
    # If the user asks "How many cases?" but there is an active person/station in context,
    # it is NOT a global query (it refers to the active person/station).
    # But if the query is explicitly global (e.g. contains "total", "across all", "in total", "over time"), then it IS global.
    explicit_global_terms = ["total", "across all", "all police", "all stations", "in total", "global", "over time", "trend"]
    has_explicit_global = any(egt in query_lower for egt in explicit_global_terms)
    
    if is_global_query:
        if (active_person or active_station) and not has_explicit_global and not ("over time" in query_lower or "by date" in query_lower or "by status" in query_lower):
            logger.info(f"[ContextManager]: Sub-analytical query referring to active context (person/station: {active_person or active_station})")
            is_global_query = False
            # Clear active case context since we don't count cases within a specific case number
            active_case = None
        elif not has_explicit_pronoun and not explicit_cases:
            logger.info("[ContextManager]: Global query detected. Suppressing active case/person context.")
            active_case = None
            active_person = None
            active_station = None

    # ── 6. Check for Multi-Case Ambiguity ──
    context_ambiguous = False
    clarification_prompt = None
    
    vague_case_queries = ["that case", "which case", "what happened in that case", "show details of that case", "in that case", "details of that case"]
    if len(recent_cases) >= 2 and not explicit_cases and any(vq in query_lower for vq in vague_case_queries):
        context_ambiguous = True
        case_list_str = " and ".join(reversed(recent_cases[:2]))
        clarification_prompt = f"I've discussed {case_list_str}. Which case do you mean?"
        logger.info(f"[ContextManager]: Multi-case ambiguity detected between {recent_cases[:2]}. Prompting user.")

    # ── 7. Check for Context Missing Post-Reset ──
    context_missing = False
    followup_patterns = ["what happened", "who is the victim", "who are the accused", "which court", "which police station", "who registered", "was anyone arrested"]
    if not active_case and not explicit_cases and not is_global_query:
        history_has_reset = False
        for msg in reversed(chat_hist[:4]):
            if any(kw in msg.get("content", "").lower() for kw in reset_keywords):
                history_has_reset = True
                break
        if history_has_reset and any(fp in query_lower for fp in followup_patterns):
            context_missing = True
            clarification_prompt = "There is no active case selected. Please specify a case number (e.g., KSP-CASE-0004)."
            logger.info("[ContextManager]: Follow-up asked post-reset with no active case.")

    return {
        "active_case": active_case,
        "active_person": active_person,
        "active_station": active_station,
        "recent_cases": recent_cases,
        "context_reset": False,
        "is_global_query": is_global_query,
        "context_ambiguous": context_ambiguous,
        "context_missing": context_missing,
        "clarification_prompt": clarification_prompt
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
    
    # Structured Query Intelligence & Phase 2 Context
    query_plan: Optional[dict]
    context_state: Optional[dict]
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
    Queries the cloud Groq LLM with robust error handling, TPM/RPM backoff,
    and automatic TPD (daily limit) model fallback.
    """
    import asyncio
    models_to_try = [
        groq_model,                      # Default model from .env
        "openai/gpt-oss-120b",           # fallback 120b
        "openai/gpt-oss-20b",            # fallback 20b
        "qwen/qwen3.8-27b",              # fallback Qwen 3.8
        "qwen/qwen3.6-27b",              # fallback Qwen 3.6
        "groq/compound",                 # fallback Groq Compound
        "groq/compound-mini",            # fallback Groq Compound Mini
        "openai/gpt-oss-safeguard-20b",  # fallback Safeguard 20b
        "canopylabs/orpheus-v1-english"  # fallback Orpheus English
    ]
    # Remove duplicates but maintain order
    unique_models = []
    for m in models_to_try:
        if m and m not in unique_models:
            unique_models.append(m)
            
    messages = [{"role": "system", "content": system_prompt}]
    if chat_history:
        for msg in chat_history:
            role = msg.get("role", "")
            content = msg.get("content", "")
            if role in ["user", "assistant"] and content:
                messages.append({"role": role, "content": content})
    messages.append({"role": "user", "content": prompt})

    model_idx = 0
    while model_idx < len(unique_models):
        current_model = unique_models[model_idx]
        current_llm = ChatGroq(
            model=current_model,
            api_key=groq_key,
            temperature=0,
            max_retries=0
        )
        
        retries = 0
        max_retries = 3
        
        while retries < max_retries:
            try:
                logger.info(f"[LLM] Querying model '{current_model}' (Attempt {retries+1}/{max_retries})...")
                response = await current_llm.ainvoke(messages)
                content = response.content.strip()
                if "<think>" in content:
                    content = re.sub(r'<think>.*?(?:</think>|$)', '', content, flags=re.DOTALL).strip()
                return content
            except Exception as e:
                err_msg = str(e)
                logger.warning(f"[LLM] Error from model '{current_model}': {err_msg}")
                
                # Check for rate limit error
                is_rate_limit = "rate_limit_exceeded" in err_msg or "rate limit" in err_msg.lower() or "429" in err_msg
                
                if "model_not_found" in err_msg or "404" in err_msg:
                    logger.warning(f"[LLM] Model '{current_model}' not found. Switching to next model...")
                    break

                if is_rate_limit:
                    # Check if it is a daily limit (TPD)
                    is_tpd = "tokens per day (TPD)" in err_msg or "TPD" in err_msg
                    
                    if is_tpd:
                        logger.warning(f"[LLM] Daily token limit (TPD) reached for model '{current_model}'. Switching to next model...")
                        break  # Break inner loop, move to next model in models_to_try
                    
                    wait_sec = 2.0
                    match = re.search(r'try again in ([\d\.]+)s', err_msg, re.IGNORECASE)
                    if match:
                        wait_sec = float(match.group(1)) + 0.5
                    if wait_sec > 10:
                        wait_sec = 2.0
                        
                    logger.info(f"[LLM] Short term rate limit hit. Sleeping for {wait_sec:.2f}s before retry...")
                    await asyncio.sleep(wait_sec)
                    retries += 1
                else:
                    logger.error(f"[LLM] Non-rate-limit crash on model '{current_model}': {err_msg}")
                    retries += 1
                    await asyncio.sleep(1.0)
                    
        model_idx += 1
        
    # If all models failed, return final failure message
    logger.error("[LLM] All models failed or rate-limited.")
    return "Raw Backend Crash: All LLM models failed or rate-limited. Please try again later."


# ==================================================
# 2. GRAPH NODES IMPLEMENTATION
# ==================================================

async def translation_input_node(state: State) -> State:
    """Translates the user query to English while detecting language and preserving entities."""
    user_query = state.get("user_query", "")
    logger.info(f"Node [translation_input]: Processing query '{user_query}'")
    translator = BhashiniTranslator()
    translated, detected_lang = await translator.translate_to_english(user_query)
    
    return {
        **state,
        "language_preference": detected_lang,
        "translated_query": translated,
        "queries": [],
        "current_query_index": 0,
        "query_plan": None,
        "context_state": state.get("context_state"),  # Preserve instead of resetting to None
        "needs_clarification": False,
        "clarification_question": "",
        "all_generated_sql": [],
        "all_sql_results": [],
        "all_pagination": [],
        "retry_count": 0,
        "sql_error": ""
    }


async def intent_router_node(state: State) -> State:
    """Classifies user intent into CHAT, DATABASE, CYBER, or SEMANTIC_SEARCH."""
    logger.info("Node [intent_router]: Classifying intent.")
    query = state.get("translated_query", state["user_query"])
    
    # Fast Phase 5 Semantic Search check
    from app.semantic_search import is_semantic_search_query
    if is_semantic_search_query(query):
        logger.info("Detected Intent: SEMANTIC_SEARCH (Direct narrative match)")
        return {
            **state,
            "intent": "SEMANTIC_SEARCH"
        }
        
    system_prompt = (
        "You are an Intent Classifier for the Karnataka State Police database AI. "
        "Classify the user's input into exactly one of two categories: 'CHAT' or 'DATABASE'. "
        "Rule: If the user is greeting, asking general questions, or chatting, output 'CHAT'. "
        "If the user asks to analyze, scan, or trace an IP address, you MUST output 'CYBER'. "
        "If the user is asking to find, search, show, or analyze specific cases, accused persons, or records, output 'DATABASE'. "
        "Return ONLY the word CHAT, DATABASE, or CYBER."
    )
    prompt = f"User Request: {query}\nIntent:"
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


async def semantic_search_node(state: State) -> State:
    """
    Step Phase 5: Performs fast semantic search over indexed BriefFacts.
    Handles hybrid queries (narrative search + metadata filters).
    """
    from app.semantic_search import semantic_index
    query = state.get("translated_query", state["user_query"])
    logger.info(f"Node [semantic_search]: Searching BriefFacts for query: '{query}'")
    
    # Check for hybrid filter (e.g. year: 2024, or active case context)
    filters = {}
    year_match = re.search(r'\b(201\d|202\d)\b', query)
    if year_match:
        filters["year"] = year_match.group(1)
        
    ctx = state.get("context_state") or resolve_conversation_context(query, state.get("chat_history"))
    if "similar" in query.lower() and ctx.get("active_case"):
        filters["case_no"] = ctx["active_case"]
        
    matches = semantic_index.search(query, top_k=5, relevance_threshold=0.15, filters=filters)
    
    if not matches:
        summary = "I couldn't find any cases matching that description."
        return {
            **state,
            "analytical_summary": summary,
            "sql_results": [],
            "sql_results_total": 0,
            "all_sql_results": [[]],
            "all_generated_sql": ["SEMANTIC_SEARCH(casemaster.BriefFacts)"],
            "generated_sql": "SEMANTIC_SEARCH(casemaster.BriefFacts)"
        }
        
    # Build structured results
    structured_results = []
    for m in matches:
        structured_results.append({
            "CaseNo": m["CaseNo"],
            "Relevance": m["relevance_level"],
            "BriefFacts": m["BriefFacts"],
            "CrimeRegisteredDate": m.get("CrimeRegisteredDate", ""),
            "PoliceStation": m.get("UnitName", "")
        })
        
    return {
        **state,
        "queries": [query],
        "current_query_index": 0,
        "sql_results": structured_results,
        "sql_results_total": len(structured_results),
        "all_sql_results": [structured_results],
        "all_generated_sql": ["SEMANTIC_SEARCH(casemaster.BriefFacts)"],
        "generated_sql": "SEMANTIC_SEARCH(casemaster.BriefFacts)"
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
    query = state.get("translated_query", state["user_query"])
    
    # If the query is about a specific case, keep as a single multi-table query to prevent rate limits
    if re.search(r'\bKSP-CASE-\d+\b', query, re.IGNORECASE) and not (" and " in query.lower() and "all" in query.lower() and "stations" in query.lower()):
        logger.info("Single-case multi-entity query detected. Bypassing query splitter.")
        return {
            **state,
            "queries": [query],
            "current_query_index": 0
        }

    system_prompt = (
        "You are an AI that splits a user's prompt into a JSON array of distinct analytical database queries. "
        "If the user asks multiple separate questions (e.g., 'Show me active cases and list all police stations'), "
        "split them into an array of strings: [\"Show me active cases\", \"list all police stations\"]. "
        "If the user asks a single question or questions about one case, return an array with just one string. "
        "DO NOT output anything other than the raw JSON array. DO NOT wrap in markdown."
    )
    prompt = f"User Request: {query}\nJSON Array:"
    result = await query_llm(prompt, system_prompt)
    
    result = result.replace("```json", "").replace("```", "").strip()
    
    try:
        queries = json.loads(result)
        if not isinstance(queries, list) or len(queries) == 0:
            queries = [query]
    except Exception as e:
        logger.error(f"Failed to parse query_splitter JSON. Using original query. Error: {e}")
        queries = [query]
        
    logger.info(f"Identified {len(queries)} distinct sub-queries.")
    
    return {
        **state,
        "queries": queries,
        "current_query_index": 0
    }


def clean_sql_query(sql: str) -> str:
    if "->" in sql:
        sql = sql.split("->")[0].strip()
    if "--" in sql:
        sql = sql.split("--")[0].strip()
    sql = sql.strip('`').strip(';').strip().strip('`').strip()
    
    # Strip any trailing emoji/symbols/explanations
    match_end = re.search(r'(?is).*\bLIMIT\s+\d+|.*\bOFFSET\s+\d+|.*[\'\")\w\d]', sql)
    if match_end:
        sql = match_end.group(0).strip()
    return sql


def extract_sql_query(text: str) -> str:
    # 1. Clean markdown code blocks
    sql = text.replace("```sql", "").replace("```", "").strip()
    
    # 2. Find the last SELECT keyword
    matches = list(re.finditer(r'(?i)\bSELECT\b', sql))
    if not matches:
        return clean_sql_query(sql)
        
    last_select_idx = matches[-1].start()
    query = sql[last_select_idx:].strip()
    
    # 3. Clean line by line: keep lines that belong to the SQL query
    clean_lines = []
    conversational_starters = ("I ", "THE ", "THIS ", "HERE ", "NOTE ", "OUTPUT ", "MATCHES ", "WAIT ", "DONE ", "WHICH ", "WE ", "YOU ", "ONE ")
    
    for line in query.split("\n"):
        line_strip = line.strip()
        if not line_strip:
            continue
            
        if "->" in line_strip:
            line_strip = line_strip.split("->")[0].strip()
        if "--" in line_strip:
            line_strip = line_strip.split("--")[0].strip()
        line_strip = line_strip.strip('`').strip()
        
        if not line_strip:
            continue
            
        if line_strip.upper().startswith(conversational_starters):
            break
            
        clean_lines.append(line_strip)
        
    query_clean = " ".join(clean_lines).strip()
    return clean_sql_query(query_clean)


def resolve_table_joins(target_tables: List[str]) -> List[dict]:
    """
    Computes valid join conditions for the given target tables based on DB_SCHEMA foreign keys.
    Ensures optimal, direct multi-table joins without unnecessary table inclusions.
    """
    tables = set(t.lower() for t in target_tables)
    relationships = []
    
    # casemaster as central hub
    if "casemaster" in tables:
        if "accused" in tables:
            relationships.append({"from": "casemaster.CaseMasterID", "to": "accused.CaseMasterID", "type": "LEFT"})
        if "victim" in tables:
            relationships.append({"from": "casemaster.CaseMasterID", "to": "victim.CaseMasterID", "type": "LEFT"})
        if "complainantdetails" in tables:
            relationships.append({"from": "casemaster.CaseMasterID", "to": "complainantdetails.CaseMasterID", "type": "LEFT"})
        if "employee" in tables:
            relationships.append({"from": "casemaster.PolicePersonID", "to": "employee.EmployeeID", "type": "LEFT"})
        if "unit" in tables:
            relationships.append({"from": "casemaster.PoliceStationID", "to": "unit.UnitID", "type": "LEFT"})
        if "court" in tables:
            relationships.append({"from": "casemaster.CourtID", "to": "court.CourtID", "type": "LEFT"})
        if "actsectionassociation" in tables or "section" in tables or "act" in tables:
            relationships.append({"from": "casemaster.CaseMasterID", "to": "actsectionassociation.CaseMasterID", "type": "JOIN"})
            if "section" in tables:
                relationships.append({"from": "actsectionassociation.SectionID", "to": "section.SectionCode", "extra": "actsectionassociation.ActID = section.ActCode", "type": "JOIN"})
            if "act" in tables:
                relationships.append({"from": "actsectionassociation.ActID", "to": "act.ActCode", "type": "JOIN"})
        if "arrestsurrender" in tables:
            relationships.append({"from": "casemaster.CaseMasterID", "to": "arrestsurrender.CaseMasterID", "type": "LEFT"})
        if "chargesheetdetails" in tables:
            relationships.append({"from": "casemaster.CaseMasterID", "to": "chargesheetdetails.CaseMasterID", "type": "LEFT"})
        if "casecategory" in tables:
            relationships.append({"from": "casemaster.CaseCategoryID", "to": "casecategory.CaseCategoryID", "type": "LEFT"})
        if "casestatusmaster" in tables:
            relationships.append({"from": "casemaster.CaseStatusID", "to": "casestatusmaster.CaseStatusID", "type": "LEFT"})
        if "gravityoffence" in tables:
            relationships.append({"from": "casemaster.GravityOffenceID", "to": "gravityoffence.GravityOffenceID", "type": "LEFT"})
        if "crimehead" in tables:
            relationships.append({"from": "casemaster.CrimeMajorHeadID", "to": "crimehead.CrimeHeadID", "type": "LEFT"})
        if "crimesubhead" in tables:
            relationships.append({"from": "casemaster.CrimeMinorHeadID", "to": "crimesubhead.CrimeSubHeadID", "type": "LEFT"})
            
    # Secondary lookups
    if "complainantdetails" in tables:
        if "castemaster" in tables:
            relationships.append({"from": "complainantdetails.CasteID", "to": "castemaster.caste_master_id", "type": "LEFT"})
        if "religionmaster" in tables:
            relationships.append({"from": "complainantdetails.ReligionID", "to": "religionmaster.ReligionID", "type": "LEFT"})
        if "occupationmaster" in tables:
            relationships.append({"from": "complainantdetails.OccupationID", "to": "occupationmaster.OccupationID", "type": "LEFT"})
            
    if "employee" in tables:
        if "rank" in tables:
            relationships.append({"from": "employee.RankID", "to": "rank.RankID", "type": "LEFT"})
        if "designation" in tables:
            relationships.append({"from": "employee.DesignationID", "to": "designation.DesignationID", "type": "LEFT"})
            
    if "unit" in tables:
        if "unittype" in tables:
            relationships.append({"from": "unit.TypeID", "to": "unittype.UnitTypeID", "type": "LEFT"})
        if "district" in tables:
            relationships.append({"from": "unit.DistrictID", "to": "district.DistrictID", "type": "LEFT"})
            
    if "district" in tables and "state" in tables:
        relationships.append({"from": "district.StateID", "to": "state.StateID", "type": "LEFT"})
        
    return relationships


async def query_planner_node(state: State) -> State:
    """
    Step B: Structured Intent Understanding and Query Planning Engine with Multi-Table Reasoning.
    Produces a strict JSON Query Plan adhering to the authoritative database schema.
    """
    current_query = state["queries"][state["current_query_index"]]
    chat_hist = state.get("chat_history", []) or []
    
    # Extract / Inherit conversation context state
    ctx = state.get("context_state") or resolve_conversation_context(current_query, chat_hist)
    logger.info(f"Node [query_planner]: Planning query '{current_query}' | Active Context: {ctx}")
    
    # Handle explicit context resets (e.g. 'forget that case')
    if ctx.get("context_reset"):
        query_plan = {
            "intent": "general_search",
            "target_tables": ["casemaster"],
            "ambiguous": False,
            "clarification_question": "",
            "entities": {"case_no": None, "person_name": None, "station_name": None},
            "filters": [],
            "requested_fields": [],
            "relationships_required": []
        }
        return {
            **state,
            "query_plan": query_plan,
            "context_state": ctx
        }

    # Handle multi-case ambiguity or post-reset context missing
    if ctx["context_ambiguous"] or ctx["context_missing"]:
        query_plan = {
            "intent": "clarification_required",
            "target_tables": ["casemaster"],
            "ambiguous": True,
            "clarification_question": ctx["clarification_prompt"],
            "entities": {"case_no": None, "person_name": None, "station_name": None},
            "filters": [],
            "requested_fields": [],
            "relationships_required": []
        }
        return {
            **state,
            "query_plan": query_plan,
            "context_state": ctx
        }
    
    # Handle explicit context resets (e.g. 'forget that case')
    if ctx.get("context_reset"):
        query_plan = {
            "intent": "general_search",
            "target_tables": ["casemaster"],
            "ambiguous": False,
            "clarification_question": "",
            "entities": {"case_no": None, "person_name": None, "station_name": None},
            "filters": [],
            "requested_fields": [],
            "relationships_required": []
        }
        return {
            **state,
            "query_plan": query_plan,
            "context_state": ctx
        }
        
    active_case = ctx["active_case"]
    active_person = ctx["active_person"]
    active_station = ctx["active_station"]
    is_global = ctx["is_global_query"]

    system_prompt = (
        "You are an expert Query Planner and Intent Understanding engine for the Karnataka State Police AI (Aloka).\n"
        "Your task is to parse a natural-language query and conversation context into a strict JSON Query Plan.\n\n"
        "DATABASE CONCEPTS & TABLE MAPPING:\n"
        "- casemaster: case, cases, FIR, FIRs, complaint case, crime case, FIR record, incident (Identifier: CaseNo e.g., 'KSP-CASE-0004')\n"
        "- accused: accused, accused person, offender, culprit, suspect (Columns: AccusedName, AgeYear, GenderID, PersonID)\n"
        "- victim: victim, victims, affected person, suffered person (Columns: VictimName, AgeYear, GenderID)\n"
        "- complainantdetails: complainant, person who filed complaint, reporter, informant (Columns: ComplainantName, AgeYear, GenderID)\n"
        "- arrestsurrender: arrest, arrested, detained, surrender, was anyone arrested (Columns: ArrestSurrenderDate, IOID, PoliceStationID, IsAccused)\n"
        "- employee: officer, police officer, investigating officer, IO, registering officer (Columns: FirstName, EmployeeID, RankID)\n"
        "- unit: police station, station, police unit, PS (Columns: UnitName, UnitID)\n"
        "- court: court, law court, judiciary (Columns: CourtName, CourtID)\n"
        "- act / section / actsectionassociation: sections, acts, applied laws, section of law\n"
        "- crimehead: major head, crime group, category\n"
        "- crimesubhead: minor head, sub head\n"
        "- castemaster / religionmaster / occupationmaster: caste, religion, occupation lookup\n\n"
        "MULTI-TABLE REASONING RULES:\n"
        "1. When the user asks for multiple related entities in a single question (e.g. 'Show the accused, victim, complainant, investigating officer, police station and court for KSP-CASE-0004'), include ALL corresponding tables in `target_tables` (e.g. [\"casemaster\", \"accused\", \"victim\", \"complainantdetails\", \"employee\", \"unit\", \"court\"]).\n"
        "2. When the user asks for acts and sections (e.g. 'What acts and sections were applied to KSP-CASE-0004?'), set target_tables to [\"casemaster\", \"actsectionassociation\", \"section\", \"act\"].\n"
        "3. When the user asks if an accused was arrested (e.g. 'Was the accused in KSP-CASE-0004 arrested?'), set target_tables to [\"casemaster\", \"accused\", \"arrestsurrender\"].\n"
        "4. When the user asks for cases involving a person and their police stations (e.g. 'Show me all cases involving Vijay Mishra and the police stations that handled them'), set target_tables to [\"accused\", \"casemaster\", \"unit\"] and add a filter on accused.AccusedName.\n"
        "5. AVOID UNNECESSARY JOINS: When the user asks a single-entity question (e.g. 'Who is the victim of KSP-CASE-0004?'), include ONLY the minimum required tables ([\"casemaster\", \"victim\"]). Do NOT include unrelated tables.\n\n"
        "ANALYTICAL & AGGREGATION REASONING RULES:\n"
        "1. For total counts (e.g. 'How many cases are there?'), set target_tables to [\"casemaster\"], aggregation: {\"function\": \"COUNT\", \"expression\": \"*\"}.\n"
        "2. For station ranking or counts per station (e.g. 'Which police station has the most cases?', 'Show the top 5 police stations by number of cases', 'How many cases does each police station have?', 'How many cases are there for each police station?'):\n"
        "   - target_tables: [\"casemaster\", \"unit\"]\n"
        "   - group_by: [\"unit.UnitName\"]\n"
        "   - aggregation: {\"function\": \"COUNT\", \"expression\": \"casemaster.CaseMasterID\"}\n"
        "   - order_by: {\"expression\": \"COUNT(casemaster.CaseMasterID)\", \"direction\": \"DESC\"}\n"
        "   - limit: 1 (for 'most' or 'highest'), 5 (for 'top 5'), or null (for all stations)\n"
        "3. For crime category ranking (e.g. 'Which crime category has the most cases?'):\n"
        "   - target_tables: [\"casemaster\", \"casecategory\"]\n"
        "   - group_by: [\"casecategory.LookupValue\"]\n"
        "   - aggregation: {\"function\": \"COUNT\", \"expression\": \"casemaster.CaseMasterID\"}\n"
        "   - order_by: {\"expression\": \"COUNT(casemaster.CaseMasterID)\", \"direction\": \"DESC\"}\n"
        "   - limit: 1\n"
        "4. For status queries (e.g. 'How many cases are open?'):\n"
        "   - target_tables: [\"casemaster\", \"casestatusmaster\"]\n"
        "   - filters: [{\"table\": \"casestatusmaster\", \"column\": \"CaseStatusName\", \"operator\": \"LIKE\", \"value\": \"%Under Investigation%\"}]\n"
        "   - aggregation: {\"function\": \"COUNT\", \"expression\": \"*\"}\n"
        "5. For contextual count in an active case (e.g. 'How many accused are in this case?'):\n"
        "   - target_tables: [\"casemaster\", \"accused\"]\n"
        "   - filters: [{\"table\": \"casemaster\", \"column\": \"CaseNo\", \"operator\": \"=\", \"value\": active_case}]\n"
        "   - aggregation: {\"function\": \"COUNT\", \"expression\": \"accused.AccusedMasterID\"}\n"
        "6. For time-series / trend queries (e.g. 'Show me the number of cases registered over time', 'Case registration trends'):\n"
        "   - target_tables: [\"casemaster\"]\n"
        "   - group_by: [\"DATE(casemaster.CrimeRegisteredDate)\"]\n"
        "   - aggregation: {\"function\": \"COUNT\", \"expression\": \"casemaster.CaseMasterID\"}\n"
        "   - order_by: {\"expression\": \"DATE(casemaster.CrimeRegisteredDate)\", \"direction\": \"ASC\"}\n"
        "   - limit: 25\n\n"
        "STRUCTURED CONVERSATION CONTEXT RULES:\n"
        f"1. Active Case Context: '{active_case}'.\n"
        f"2. Active Person Context: '{active_person}'.\n"
        f"3. Active Station Context: '{active_station}'.\n"
        f"4. Global Query Flag: {is_global}.\n"
        "5. IF Active Case is present ('KSP-CASE-XXXX') AND Global Query Flag is False, ALWAYS include filter: casemaster.CaseNo = active_case.\n"
        "6. IF Active Person is present AND Global Query Flag is False, and the query is a follow-up, you can filter by this person name (e.g. search for cases involving this person).\n"
        "7. IF Active Station is present AND Global Query Flag is False, and the query is a follow-up, you can filter by this station name.\n"
        "8. IF Global Query Flag is True (e.g. 'how many cases are there in total?'), do NOT filter by active_case, active_person, or active_station.\n\n"
        "AMBIGUITY RULES:\n"
        "1. If the user asks about a person's name (e.g. 'Show Ravi's case', 'Show Ramesh') without specifying whether that person is an accused, victim, complainant, or police officer, set \"ambiguous\": true, and set \"clarification_question\": \"Do you mean cases where [Name] is an accused, victim, complainant, or police officer?\".\n"
        "2. Otherwise, set \"ambiguous\": false.\n\n"
        "JSON OUTPUT FORMAT STRICTLY REQUIRED:\n"
        "```json\n"
        "{\n"
        "  \"intent\": \"rank_police_stations_by_cases | count_cases | count_open_cases | count_accused | multi_table_query | find_accused | find_victim | find_complainant | find_officer | find_station | find_arrested | find_court | find_sections | find_case | general_search\",\n"
        "  \"target_tables\": [\"casemaster\", \"unit\"],\n"
        "  \"ambiguous\": false,\n"
        "  \"clarification_question\": \"\",\n"
        "  \"entities\": {\n"
        "    \"case_no\": \"KSP-CASE-0004\" or null,\n"
        "    \"person_name\": \"Vijay Mishra\" or null,\n"
        "    \"station_name\": \"Hebbal Police Station\" or null\n"
        "  },\n"
        "  \"filters\": [\n"
        "    {\"table\": \"casemaster\", \"column\": \"CaseNo\", \"operator\": \"=\", \"value\": \"KSP-CASE-0004\"}\n"
        "  ],\n"
        "  \"requested_fields\": [\"unit.UnitName\", \"COUNT(casemaster.CaseMasterID) AS case_count\"],\n"
        "  \"relationships_required\": [\n"
        "    {\"from\": \"casemaster.PoliceStationID\", \"to\": \"unit.UnitID\"}\n"
        "  ],\n"
        "  \"aggregation\": {\n"
        "    \"function\": \"COUNT | SUM | AVG | MIN | MAX\",\n"
        "    \"expression\": \"casemaster.CaseMasterID\"\n"
        "  },\n"
        "  \"group_by\": [\"unit.UnitName\"],\n"
        "  \"order_by\": {\n"
        "    \"expression\": \"COUNT(casemaster.CaseMasterID)\",\n"
        "    \"direction\": \"DESC\"\n"
        "  },\n"
        "  \"limit\": 5\n"
        "}\n"
        "```\n"
        "Output ONLY the raw JSON object."
    )

    prompt = f"User Request: {current_query}\n\nGenerate JSON Query Plan:"
    result = await query_llm(prompt, system_prompt, chat_hist)
    
    # Robust JSON Extraction
    query_plan = {}
    md_match = re.search(r'```(?:json)?\n(.*?)```', result, flags=re.DOTALL)
    if md_match:
        try:
            query_plan = json.loads(md_match.group(1).strip())
        except Exception:
            pass
            
    if not query_plan:
        start_idx = result.find('{')
        end_idx = result.rfind('}')
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            try:
                query_plan = json.loads(result[start_idx:end_idx+1].strip())
            except Exception as e:
                logger.warning(f"Failed to parse query plan JSON candidate: {e}")
                
    if not query_plan:
        logger.error(f"Failed to parse query plan JSON from raw result: {result}")
        query_plan = {
            "intent": "general_search",
            "target_tables": ["casemaster"],
            "ambiguous": False,
            "clarification_question": "",
            "entities": {"case_no": active_case, "person_name": active_person, "station_name": active_station},
            "filters": [{"table": "casemaster", "column": "CaseNo", "operator": "=", "value": active_case}] if active_case else [],
            "requested_fields": [],
            "relationships_required": []
        }
        
    # Ensure active_case filter is present if active_case exists and not a global query or group_by query
    has_group_by = bool(query_plan.get("group_by"))
    if active_case and not is_global and not query_plan.get("ambiguous") and not has_group_by:
        has_case_filter = any(f.get("column") == "CaseNo" for f in query_plan.get("filters", []))
        if not has_case_filter:
            query_plan.setdefault("filters", []).append({
                "table": "casemaster",
                "column": "CaseNo",
                "operator": "=",
                "value": active_case
            })
            
    # Update persistent context_state from newly generated query plan entities
    if query_plan.get("entities"):
        ents = query_plan["entities"]
        if ents.get("case_no"):
            ctx["active_case"] = ents["case_no"]
        if ents.get("person_name"):
            ctx["active_person"] = ents["person_name"]
        if ents.get("station_name"):
            ctx["active_station"] = ents["station_name"]

    return {
        **state,
        "query_plan": query_plan,
        "context_state": ctx
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
    for tbl in (plan.get("target_tables") or []):
        if not tbl:
            continue
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
    for flt in (plan.get("filters") or []):
        if not isinstance(flt, dict):
            continue
        tbl = flt.get("table", "").lower()
        col = flt.get("column", "")
        if tbl in DB_SCHEMA and col in DB_SCHEMA[tbl]["columns"]:
            validated_filters.append({
                "table": tbl,
                "column": col,
                "operator": flt.get("operator", "="),
                "value": flt.get("value")
            })
            
    # ── Multi-Table Join Validation & Resolution ──
    # Ensure tables referenced in group_by or filters are in validated_target_tables
    for col_expr in (plan.get("group_by") or []):
        if isinstance(col_expr, str) and "." in col_expr:
            tbl = col_expr.split(".")[0].lower()
            if tbl in DB_SCHEMA and tbl not in validated_target_tables:
                validated_target_tables.append(tbl)
                
    if ("section" in validated_target_tables or "act" in validated_target_tables) and "casemaster" in validated_target_tables:
        if "actsectionassociation" not in validated_target_tables:
            validated_target_tables.insert(1, "actsectionassociation")

    computed_joins = resolve_table_joins(validated_target_tables)
    plan["relationships_required"] = computed_joins
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
    
    # ── Python Security Guardrail ──
    modification_keywords = ["DELETE", "UPDATE", "INSERT", "DROP", "ALTER", "TRUNCATE", "MODIFY"]
    if any(kw in current_query.upper() for kw in modification_keywords):
        logger.warning(f"SECURITY OVERRIDE: Destructive query blocked: {current_query}")
        return {
            **state,
            "generated_sql": "🚨 SECURITY OVERRIDE: Unauthorized data modification query detected and blocked by KSP Protocols."
        }

    query_plan = state.get("query_plan", {})
    logger.info(f"Node [generate_sql]: Generating SQL for sub-query '{current_query}' from validated plan.")

    schema_text = []
    for tbl, info in DB_SCHEMA.items():
        cols_str = ", ".join([f"{col} ({dt})" for col, dt in info["columns"].items()])
        fks_str = ", ".join([f"{k} -> {v}" for k, v in info["foreign_keys"].items()])
        schema_text.append(f"- {tbl} ({cols_str}) | FKs: [{fks_str}]")
    core_schema_str = "\n".join(schema_text)

    system_prompt = (
        "You are Aloka, an expert SQL generator for the Karnataka State Police. Convert the validated Query Plan into an exact MySQL SELECT statement.\n\n"
        f"AUTHORITATIVE MYSQL SCHEMA (Strictly use ONLY these lowercase table names and exact column cases):\n{core_schema_str}\n\n"
        "STRICT SQL GENERATION RULES:\n"
        "1. TABLE NAMES: Must be strictly lowercase (e.g., casemaster, accused, victim, complainantdetails, employee, unit, court, district, state, arrestsurrender, act, section, actsectionassociation, crimehead, crimesubhead, castemaster, religionmaster, occupationmaster).\n"
        "2. COLUMN NAMES: Must match the exact casing specified in the schema definition (e.g., CaseMasterID, CrimeNo, CaseNo, AccusedName, AgeYear, GenderID, FirstName, UnitName, caste_master_id, caste_master_name).\n"
        "3. CASE IDENTIFIER: Always filter case IDs like 'KSP-CASE-XXXX' using `casemaster.CaseNo = 'KSP-CASE-XXXX'`. Do NOT filter on `CrimeNo`.\n"
        "4. JOINS & MULTI-TABLE REASONING:\n"
        "   - Connect tables strictly using the validated relationships in `relationships_required` or schema foreign keys.\n"
        "   - When querying multiple entities for a case, start FROM casemaster and use LEFT JOIN for each requested related table:\n"
        "     * LEFT JOIN accused ON casemaster.CaseMasterID = accused.CaseMasterID\n"
        "     * LEFT JOIN victim ON casemaster.CaseMasterID = victim.CaseMasterID\n"
        "     * LEFT JOIN complainantdetails ON casemaster.CaseMasterID = complainantdetails.CaseMasterID\n"
        "     * LEFT JOIN employee ON casemaster.PolicePersonID = employee.EmployeeID\n"
        "     * LEFT JOIN unit ON casemaster.PoliceStationID = unit.UnitID\n"
        "     * LEFT JOIN court ON casemaster.CourtID = court.CourtID\n"
        "     * LEFT JOIN arrestsurrender ON casemaster.CaseMasterID = arrestsurrender.CaseMasterID\n"
        "   - When acts and sections are requested, join: `JOIN actsectionassociation ON casemaster.CaseMasterID = actsectionassociation.CaseMasterID JOIN section ON actsectionassociation.SectionID = section.SectionCode AND actsectionassociation.ActID = section.ActCode JOIN act ON actsectionassociation.ActID = act.ActCode`.\n"
        "   - When querying cases for a specific accused person with station: `SELECT accused.AccusedName, casemaster.CaseNo, unit.UnitName AS PoliceStation FROM accused JOIN casemaster ON accused.CaseMasterID = casemaster.CaseMasterID JOIN unit ON casemaster.PoliceStationID = unit.UnitID WHERE accused.AccusedName LIKE '%<Name>%'`.\n"
        "   - Always prefix selected column names with their table name or alias to avoid ambiguity (e.g. `casemaster.CaseNo`, `accused.AccusedName`, `victim.VictimName`, `complainantdetails.ComplainantName`, `employee.FirstName AS InvestigatingOfficer`, `unit.UnitName AS PoliceStation`, `court.CourtName`).\n"
        "   - Do NOT add unnecessary joins if a table is not requested in target_tables.\n"
        "5. CASTE / RELIGION / OCCUPATION: Join complainantdetails on CasteID = castemaster.caste_master_id, ReligionID = religionmaster.ReligionID, OccupationID = occupationmaster.OccupationID.\n"
        "6. ANALYTICAL & AGGREGATION RULES:\n"
        "   - When `group_by` is present, construct GROUP BY SQL:\n"
        "     `SELECT <group_by_columns>, <aggregation_function>(<expression>) AS <alias> FROM <primary_table> [JOINs] [WHERE <filters>] GROUP BY <group_by_columns> [ORDER BY <order_by_expression> <direction>] [LIMIT <limit>]`\n"
        "   - When scalar `aggregation` (e.g. COUNT(*)) is present without group_by:\n"
        "     `SELECT <aggregation_function>(<expression>) AS <alias> FROM <primary_table> [JOINs] [WHERE <filters>]`\n"
        "   - For 'most' / 'highest', use ORDER BY <aggregate> DESC LIMIT 1.\n"
        "   - For 'top N', use ORDER BY <aggregate> DESC LIMIT N.\n"
        "   - For all Group A (Analytical) queries, DO NOT inject `COUNT(*) OVER() AS Total_Matching_Records`.\n"
        "7. OUTPUT FORMAT: Output ONLY the raw SQL SELECT query without markdown formatting."
    )

    prompt = (
        f"Natural Language Query: {current_query}\n"
        f"Validated Query Plan: {json.dumps(query_plan, indent=2)}\n\n"
        f"SQL Query:"
    )

    sql = await query_llm(prompt, system_prompt, state.get("chat_history"))
    sql = extract_sql_query(sql)

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
    sql = extract_sql_query(raw_sql)
    
    # Check if query has an explicit analytical/user limit
    limit = 15
    limit_match = re.search(r'(?i)\bLIMIT\s+(\d+)\b', sql)
    if limit_match:
        limit = int(limit_match.group(1))
        # Keep explicit user/analytical limit (e.g. LIMIT 1, LIMIT 5)
        clean_sql = re.sub(r'(?i)\bOFFSET\s+\d+\b', '', sql).strip().rstrip(';')
        paginated_sql = f"{clean_sql} OFFSET 0"
    else:
        clean_sql = re.sub(r'(?i)\bOFFSET\s+\d+\b', '', sql).strip().rstrip(';')
        paginated_sql = f"{clean_sql} LIMIT {limit + 1} OFFSET 0"
    
    logger.info(f"Node [execute_sql]: Executing SQL: {paginated_sql}")
    
    # SECURITY GUARDRAILS & READ-ONLY ENFORCEMENT
    forbidden_keywords = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE", "GRANT", "REVOKE", "CREATE"]
    if "SECURITY OVERRIDE" in paginated_sql.upper() or any(keyword in paginated_sql.upper() for keyword in forbidden_keywords):
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
    corrected_sql = extract_sql_query(corrected_sql)
    
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

    lang = state.get("language_preference", "en")
    lang_directive = "SYSTEM DIRECTIVE: Respond in English."
    if lang == "kn":
        lang_directive = "SYSTEM DIRECTIVE: You MUST respond in Kannada (ಕನ್ನಡ). Preserve case numbers (e.g. KSP-CASE-0004), person names, and station names accurately."
    elif lang == "hi":
        lang_directive = "SYSTEM DIRECTIVE: You MUST respond in Hindi (हिन्दी). Preserve case numbers (e.g. KSP-CASE-0004), person names, and station names accurately."

    system_prompt = (
        "You are Aloka, an elite State Intelligence AI for the KSP. You structure all responses using clear Markdown.\n"
        "DATA SUMMARY RULE: When summarizing SQL results, state the true total row count provided. If no matching records were found, state clearly: 'I couldn't find any matching records for that request.' Do NOT report zero-row results as database errors.\n\n"
        f"{lang_directive}\n\n"
        "FORMATTING RULE:\n"
        "## [Main Title of the Analysis]\n\n"
        "### Key Insights\n"
        "* [Bullet point 1]\n"
        "* [Bullet point 2]\n\n"
        "[One conversational sentence asking the user if they need further details or filtering.]\n"
    )
    
    prompt = (
        f"Original User Query: {state['user_query']}\n"
        f"Execution Results:\n{context_str}\n\n"
        f"Provide the final professional summary."
    )
    
    summary_raw = await query_llm(prompt, system_prompt, state.get("chat_history"))
    
    from app.visualization import determine_visualization
    primary_results = state["all_sql_results"][0] if state.get("all_sql_results") else state.get("sql_results", [])
    primary_sql = state["all_generated_sql"][0] if state.get("all_generated_sql") else state.get("generated_sql", "")
    
    chart_metadata = determine_visualization(
        user_query=state["user_query"],
        query_plan=state.get("query_plan"),
        sql_results=primary_results,
        generated_sql=primary_sql
    )
    
    # Strip any redundant JSON block from LLM summary
    summary_clean = re.sub(r"```json\s*{.*?}\s*```", "", summary_raw, flags=re.DOTALL).strip()
    
    return {
        **state,
        "analytical_summary": summary_clean,
        "chart_metadata": chart_metadata
    }


async def translation_output_node(state: State) -> State:
    """Ensures final output respects target language preference."""
    logger.info("Node [translation_output]: Formatting output for target language.")
    summary = state.get("analytical_summary", "")
    lang = state.get("language_preference", "en")
    translator = BhashiniTranslator()
    final_output = translator.translate_response(summary, lang)
    return {
        **state,
        "final_output": final_output
    }


# ==================================================
# 3. CONDITIONAL ROUTING LOGIC
# ==================================================
def route_intent(state: State) -> str:
    if state.get("intent") == "CHAT":
        return "chat_response"
    elif state.get("intent") == "CYBER":
        return "cyber_node"
    elif state.get("intent") == "SEMANTIC_SEARCH":
        return "semantic_search"
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
workflow.add_node("semantic_search", semantic_search_node)
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
workflow.add_conditional_edges("intent_router", route_intent, {
    "chat_response": "chat_response",
    "cyber_node": "cyber_node",
    "semantic_search": "semantic_search",
    "query_splitter": "query_splitter"
})
workflow.add_edge("chat_response", "translation_output")
workflow.add_edge("cyber_node", "translation_output")
workflow.add_edge("semantic_search", "analyze_data")

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

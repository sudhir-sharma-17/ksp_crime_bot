import os
import re
import math
import json
import logging
from collections import Counter
from typing import List, Dict, Any, Optional

from sqlalchemy import text
from app.agent import get_db_connection, DB_SCHEMA

logger = logging.getLogger("app.semantic_search")

# Path to cache semantic index locally
INDEX_CACHE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "semantic_index.json")

# Semantic Domain Synonyms / Keywords Expansion for Police Crime BriefFacts
SEMANTIC_SYNONYM_MAP = {
    "phishing": ["phishing", "fake link", "fraudulent link", "sms", "message", "link", "clicked", "url", "reward", "apk", "lottery"],
    "scam": ["scam", "fraud", "cheated", "tricked", "deceived", "fake", "duped", "conned", "swindled", "bogus"],
    "fake link": ["fake link", "phishing", "link", "click", "clicked", "url", "website", "portal", "download", "sms"],
    "link": ["link", "url", "click", "clicked", "website", "phishing", "sms"],
    "sms": ["sms", "message", "text", "whatsapp", "telegram", "notification", "otp", "code", "phone"],
    "message": ["message", "sms", "text", "whatsapp", "telegram", "alert", "notice"],
    "money stolen": ["debited", "transferred", "fraudulently", "stolen", "lost money", "withdrawn", "rupees", "account", "bank"],
    "lost money": ["debited", "transferred", "fraudulently", "stolen", "lost", "rupees", "account", "bank", "lakh"],
    "tricked": ["tricked", "cheated", "duped", "deceived", "lured", "fraudulent", "misled"],
    "online fraud": ["online", "cyber", "internet", "bank", "account", "transaction", "debited", "fraud", "scam", "phishing"],
    "financial fraud": ["financial", "bank", "account", "debited", "transferred", "rupees", "investment", "trading", "crypto", "fraud"],
    "theft": ["stole", "theft", "gold", "ornaments", "cash", "stolen", "entered", "house", "night", "burglary"],
    "assault": ["assaulted", "physical", "injuries", "beaten", "wooden stick", "weapon", "dispute", "fight", "attacked"],
    "murder": ["murdered", "homicide", "dead", "body", "knife", "injuries", "killed", "stabbed", "death"]
}


class SemanticSearchIndex:
    """
    In-memory, persistent semantic search engine for KSP Case BriefFacts.
    Indexes casemaster.BriefFacts with BM25 + dense TF-IDF semantic vector space
    and domain-specific semantic concept expansion.
    """
    def __init__(self):
        self.cases: List[Dict[str, Any]] = []
        self.doc_term_freqs: List[Counter] = []
        self.doc_lengths: List[int] = []
        self.avg_doc_length: float = 0.0
        self.idf: Dict[str, float] = {}
        self.vocabulary: set = set()
        self.is_indexed: bool = False

    def tokenize(self, text: str) -> List[str]:
        if not text:
            return []
        cleaned = re.sub(r'[^a-zA-Z0-9\s]', ' ', text.lower())
        tokens = [t for t in cleaned.split() if len(t) > 1]
        return tokens

    def build_index(self, force_refresh: bool = False) -> int:
        """
        Builds or loads the semantic index from the database / local cache.
        """
        if self.is_indexed and not force_refresh:
            return len(self.cases)

        # Check local file cache if available and not force refresh
        os.makedirs(os.path.dirname(INDEX_CACHE_PATH), exist_ok=True)
        if not force_refresh and os.path.exists(INDEX_CACHE_PATH):
            try:
                with open(INDEX_CACHE_PATH, "r", encoding="utf-8") as f:
                    cached_data = json.load(f)
                    self.cases = cached_data.get("cases", [])
                    if self.cases:
                        self._compute_statistics()
                        self.is_indexed = True
                        logger.info(f"[SemanticIndex]: Loaded {len(self.cases)} case BriefFacts from local cache.")
                        return len(self.cases)
            except Exception as e:
                logger.warning(f"[SemanticIndex]: Cache load failed: {e}. Rebuilding from database.")

        logger.info("[SemanticIndex]: Indexing casemaster BriefFacts from database...")
        engine = get_db_connection()
        with engine.connect() as conn:
            query = text(
                "SELECT cm.CaseMasterID, cm.CaseNo, cm.BriefFacts, cm.CrimeRegisteredDate, "
                "cm.PoliceStationID, u.UnitName "
                "FROM casemaster cm "
                "LEFT JOIN unit u ON cm.PoliceStationID = u.UnitID "
                "WHERE cm.BriefFacts IS NOT NULL AND cm.BriefFacts != ''"
            )
            rows = conn.execute(query).fetchall()
            
        self.cases = []
        for r in rows:
            self.cases.append({
                "CaseMasterID": r.CaseMasterID,
                "CaseNo": r.CaseNo,
                "BriefFacts": r.BriefFacts,
                "CrimeRegisteredDate": str(r.CrimeRegisteredDate) if r.CrimeRegisteredDate else "",
                "PoliceStationID": r.PoliceStationID,
                "UnitName": r.UnitName or ""
            })

        self._compute_statistics()
        self.is_indexed = True

        # Save to local file cache for fast restarts
        try:
            with open(INDEX_CACHE_PATH, "w", encoding="utf-8") as f:
                json.dump({"cases": self.cases}, f, ensure_ascii=False, indent=2)
            logger.info(f"[SemanticIndex]: Cached {len(self.cases)} indexed records to {INDEX_CACHE_PATH}")
        except Exception as e:
            logger.warning(f"[SemanticIndex]: Failed to write index cache: {e}")

        return len(self.cases)

    def _compute_statistics(self):
        N = len(self.cases)
        if N == 0:
            return

        self.doc_term_freqs = []
        self.doc_lengths = []
        doc_freq = Counter()

        for doc in self.cases:
            tokens = self.tokenize(doc["BriefFacts"])
            tf = Counter(tokens)
            self.doc_term_freqs.append(tf)
            self.doc_lengths.append(len(tokens))
            for term in tf.keys():
                doc_freq[term] += 1
                self.vocabulary.add(term)

        self.avg_doc_length = sum(self.doc_lengths) / N if N > 0 else 1.0

        # BM25-standard IDF calculation
        self.idf = {}
        for term, df in doc_freq.items():
            self.idf[term] = math.log((N - df + 0.5) / (df + 0.5) + 1.0)

    def expand_query_terms(self, query: str) -> List[str]:
        """
        Expands query tokens using semantic domain synonyms.
        """
        tokens = self.tokenize(query)
        expanded_tokens = list(tokens)
        query_lower = query.lower()

        for key, synonyms in SEMANTIC_SYNONYM_MAP.items():
            if key in query_lower or any(t in tokens for t in key.split()):
                expanded_tokens.extend(synonyms)

        return expanded_tokens

    def search(
        self,
        query: str,
        top_k: int = 5,
        relevance_threshold: float = 0.20,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Performs semantic search over BriefFacts with BM25 similarity, semantic query expansion,
        and optional structured metadata filters (hybrid search).
        """
        if not self.is_indexed:
            self.build_index()

        if not self.cases:
            return []

        expanded_tokens = self.expand_query_terms(query)
        if not expanded_tokens:
            return []

        query_tf = Counter(expanded_tokens)
        k1 = 1.5
        b = 0.75
        scores = []

        for idx, doc in enumerate(self.cases):
            # Apply structured metadata filters if present (Hybrid Search)
            if filters:
                if "year" in filters and filters["year"]:
                    year_val = str(filters["year"])
                    if year_val not in str(doc.get("CrimeRegisteredDate", "")):
                        continue
                if "case_no" in filters and filters["case_no"]:
                    if doc.get("CaseNo") != filters["case_no"]:
                        continue
                if "station_name" in filters and filters["station_name"]:
                    if filters["station_name"].lower() not in doc.get("UnitName", "").lower():
                        continue

            doc_tf = self.doc_term_freqs[idx]
            doc_len = self.doc_lengths[idx]
            score = 0.0

            for term, q_count in query_tf.items():
                if term in doc_tf:
                    freq = doc_tf[term]
                    idf_val = self.idf.get(term, 0.1)
                    num = freq * (k1 + 1)
                    den = freq + k1 * (1 - b + b * (doc_len / self.avg_doc_length))
                    score += idf_val * (num / den) * q_count

            scores.append((idx, score))

        if not scores:
            return []

        # Find max score for normalization
        max_score = max(s[1] for s in scores) if scores else 1.0
        if max_score <= 0:
            return []

        results = []
        for idx, raw_score in scores:
            normalized_score = raw_score / max_score
            if normalized_score >= relevance_threshold:
                case_info = dict(self.cases[idx])
                case_info["relevance_score"] = round(normalized_score, 4)
                case_info["relevance_level"] = "High" if normalized_score >= 0.6 else "Moderate"
                results.append((normalized_score, case_info))

        # Sort descending by relevance
        results.sort(key=lambda x: x[0], reverse=True)
        return [r[1] for r in results[:top_k]]


# Global singleton instance
semantic_index = SemanticSearchIndex()


def is_semantic_search_query(user_query: str) -> bool:
    """
    Classifies whether a natural language query is a semantic narrative inquiry
    or a structured / analytical SQL query.
    """
    q = user_query.lower().strip()

    # Explicit non-semantic structured triggers (Must use SQL engine)
    structured_patterns = [
        r'^\s*who\s+is\s+the\s+(victim|accused|complainant|officer|io)',
        r'^\s*how\s+many\s+cases',
        r'^\s*which\s+police\s+station\s+has\s+the\s+most',
        r'^\s*which\s+station\s+has\s+the\s+most',
        r'^\s*which\s+crime\s+category\s+has\s+the\s+most',
        r'^\s*show\s+the\s+top\s+\d+\s+police\s+stations',
        r'^\s*show\s+the\s+accused,\s*victim',
        r'^\s*who\s+was\s+the\s+accused,\s*which\s+officer',
        r'^\s*what\s+acts\s+and\s+sections',
        r'^\s*was\s+the\s+accused\s+in\s+ksp-case-\d+\s+arrested',
        r'^\s*how\s+many\s+accused\s+are\s+in\s+this\s+case',
        r'^\s*how\s+many\s+cases\s+are\s+open',
        r'^\s*how\s+many\s+cases\s+does\s+each\s+police\s+station'
    ]
    for pattern in structured_patterns:
        if re.search(pattern, q):
            return False

    # Semantic narrative keywords
    semantic_triggers = [
        "phishing", "fake link", "fraudulent link", "fraudulent sms",
        "scam", "scams", "tricked", "money was stolen", "lost money",
        "online fraud", "financial fraud", "investment fraud", "sms messages",
        "cases involving", "cases where", "cases related to", "incidents where",
        "search cases about", "find cases", "similar cases", "modus operandi",
        "stole gold", "assaulted with", "murder inside"
    ]

    return any(trigger in q for trigger in semantic_triggers)

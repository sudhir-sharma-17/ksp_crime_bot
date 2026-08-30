# ALOKA INTELLIGENCE — HACKATHON PRESENTATION DECK (PPT)

---

## Slide 1: Title Slide — Aloka Intelligence

### Slide Content
* **System Name**: ALOKA INTELLIGENCE (ಆಲೋಕ ಇಂಟೆಲಿಜೆನ್ಸ್)
* **Subtitle**: Multilingual AI-Powered State Police Intelligence & Criminological Command Center
* **Authority**: Built for Karnataka State Police (KSP) & Law Enforcement Investigators
* **Core Paradigm**: Zero-SQL Natural Language Conversational Access over Complex Relational Crime Databases
* **Language Support**: English • ಕನ್ನಡ (Kannada) • हिन्दी (Hindi)

### Speaker Notes
> "Good morning, esteemed judges. Law enforcement officers and intelligence analysts manage massive relational databases containing FIRs, accused profiles, penal sections, and personnel records. However, retrieving actionable intelligence traditionally requires writing complex multi-table SQL queries or waiting for database administrators. Today, we introduce **Aloka Intelligence** — a state-of-the-art, multilingual conversational intelligence assistant that enables officers to query, analyze, semantically search, and visualize state crime records directly in natural language across English, Kannada, and Hindi."

### Visual Suggestion
* Official Karnataka Police emblem centered with a sleek dark command center interface preview (`#0B1017` / `#2F5DA8`), accompanied by the live badge: `SYSTEM SECURE & OPERATIONAL`.

---

## Slide 2: Problem Statement

### Slide Content
* **SQL Barrier for Field Personnel**: Investigating officers and analysts should not need database programming skills during active investigations.
* **Complex Multi-Table Schemas**: Crime data is fragmented across 13+ relational tables (FIRs, Accused, Victims, Officers, Legal Acts, Sections).
* **Semantic Ambiguity**: Search terms like *"fraud"*, *"phishing"*, or *"police personnel"* do not directly match strict database column names.
* **Loss of Conversational Context**: Traditional database search tools cannot understand pronoun follow-up questions (e.g., *"Who was the accused in that case?"*).
* **Linguistic Barriers**: Field officers across Karnataka frequently think and operate in Kannada and Hindi, while databases store data in standardized schemas.

### Speaker Notes
> "When a police officer needs to know 'Who are the accused in KSP-CASE-0004?' or 'Which police station has the highest crime volume this year?', they face multiple friction points: complex join logic across multiple tables, rigid keyword searches, and lack of regional language support. Aloka eliminates these barriers by turning natural language into verified, schema-aware SQL."

### Visual Suggestion
* Split comparison diagram: Left side shows a frustrated officer facing a 15-line SQL query with syntax errors; Right side shows an officer typing a 1-line question in Kannada and getting an instant structured dossier.

---

## Slide 3: Proposed Solution — Aloka Intelligence

### Slide Content
* **Natural Language to Verified SQL**: Translates plain text questions into optimized, schema-validated MySQL queries.
* **14-Node Stateful AI Graph**: Orchestrated via LangGraph with multi-step validation, schema checking, and automated self-correction.
* **Relational Relationship Reasoning**: Automatically navigates foreign key paths (`casemaster → accused`, `employee → rank → designation`).
* **Hybrid Semantic Crime Search**: In-memory BM25 + dense TF-IDF vector space engine to discover similar modus operandi across case brief facts.
* **Instant Visual Analytics & Dossier Export**: Automatic generation of Bar, Pie, and Line charts + 1-click confidential PDF dossier generation.
* **Native Multilingual Pipeline**: End-to-end support for English, Kannada, and Hindi with entity and case-number preservation.

### Speaker Notes
> "Aloka is not just a chatbot wrapping an LLM. It is a deterministic, 14-node LangGraph pipeline with strict schema validation, AST safety filtering, relationship path discovery, in-memory BM25 semantic retrieval, and live data visualization. It delivers high-accuracy answers directly backed by the state's criminological database."

### Visual Suggestion
* 3 Core Pillars graphic: **Conversational Interface** ➔ **14-Node LangGraph Engine** ➔ **Live KSP Relational Database**.

---

## Slide 4: Key Objectives & Implementation Scope

### Slide Content
* **Zero-SQL Data Accessibility**: Enable non-technical personnel to extract relational data seamlessly.
* **Multi-Turn Contextual Memory**: Maintain active case IDs, suspect names, and police stations across continuous conversations.
* **Read-Only Database Safeguards**: Enforce strict `SELECT`-only execution to prevent unauthorized modification or data corruption.
* **Self-Healing SQL Generation**: Automatically catch and repair syntax or schema errors in real time without crashing.
* **Operational Command Center UI**: Modern, high-density dashboard featuring a 3-panel layout, session history, and live SQL inspection.

### Speaker Notes
> "Our primary objectives were security, accuracy, and ease of use. We strictly enforce read-only database operations so no user input can modify police records. Furthermore, we designed an intelligent self-correction loop that retries queries if MySQL returns any syntax error."

### Visual Suggestion
* Feature checklist diagram displaying green verification checkmarks across: *Intent Routing, Schema Validation, Context Tracking, Visual Analytics, and Multilingual Middleware*.

---

## Slide 5: System Architecture & Workflow

### Slide Content
* **Client Layer**: React 19 + Tailwind CSS v4 Command Center with real-time state synchronization.
* **API Gateway**: FastAPI async web service providing non-blocking query streaming.
* **StateGraph Orchestrator**: 14 specialized LangGraph nodes handling language detection, intent classification, planning, SQL generation, execution, and analytics.
* **Inference Layer**: Groq Cloud LPU running high-performance models (`qwen/qwen3.8-27b`, `openai/gpt-oss-safeguard-20b`).
* **Database & Search**: MySQL 8.0 relational case repository + in-memory BM25 semantic index.

### Speaker Notes
> "Here is the architectural overview of Aloka. The user enters a query in our React frontend. The request is processed by FastAPI and enters our 14-node LangGraph state machine. It normalizes language, routes intent, constructs a structured JSON query plan, validates schema foreign keys, generates and executes safe SQL against MySQL, and synthesizes analytical insights."

### Visual Suggestion
* Architectural flow diagram showing:
  `User → React 19 Frontend → FastAPI Gateway → LangGraph Engine (14 Nodes) → MySQL Database / BM25 Index → Recharts / PDF Dossier`.

---

## Slide 6: The AI Query Pipeline in Action

### Slide Content
* **Step 1 — Language Normalization**: Detects Kannada/Hindi, isolates case tokens (`KSP-CASE-0004`), and maps regional phrasing.
* **Step 2 — Intent Router**: Dispatches query to `DATABASE`, `SEMANTIC_SEARCH`, `CYBER`, or `CHAT`.
* **Step 3 — Query Planner**: Produces a formal JSON specification with target tables and required foreign-key joins.
* **Step 4 — Schema Validator**: Inspects tables, injects missing join keys, and verifies field validity against `DB_SCHEMA`.
* **Step 5 — SQL Generation & Safety Guard**: Synthesizes clean SQL and applies strict regex and token security filters.
* **Step 6 — Execution & Synthesis**: Runs query on MySQL, calculates totals, and renders formatted analytical Markdown.

### Speaker Notes
> "When an investigator asks 'Who are the accused in KSP-CASE-0004?', the pipeline doesn't just guess SQL. The Query Planner builds a structured plan with target tables `casemaster` and `accused`. The Schema Validator verifies the foreign key join `casemaster.CaseMasterID = accused.CaseMasterID`. Safe SQL is generated and executed, returning exact accused records with age, gender, and arrest status in milliseconds."

### Visual Suggestion
* Pipeline diagram tracking the step-by-step transformation of *"Who are the accused in KSP-CASE-0004?"* into `SELECT accused.AccusedName, accused.Age, accused.ArrestStatus FROM casemaster LEFT JOIN accused ON casemaster.CaseMasterID = accused.CaseMasterID WHERE casemaster.CaseNo = 'KSP-CASE-0004'`.

---

## Slide 7: Conversational Context & Multi-Turn Intelligence

### Slide Content
* **Active Entity Tracking**: Automatically remembers `active_case`, `active_person`, and `active_station`.
* **Pronoun Resolution**: Understands queries like *"Who was the victim?"* after examining a case.
* **Seamless Context Switching**: Instantly shifts focus when a new case or station ID is introduced.
* **Global Query Isolation**: Bypasses active case filters when users ask broad questions like *"List all police stations"*.
* **Ambiguity Detection**: Prompts the user for clarification if a reference is missing or unclear.

### Speaker Notes
> "In real investigations, conversations happen in multi-step dialogues. If an officer asks 'Show KSP-CASE-0004', Aloka sets the active context. When the officer follows up with 'Which sections of law were applied?', Aloka automatically joins `actsectionassociation`, `act`, and `section` for that specific case without asking the officer to repeat the case number."

### Visual Suggestion
* Multi-turn chat progression graphic showing:
  1. *User*: "Show FIR KSP-CASE-0004" ➔ *Context Badge*: `ACTIVE CASE: KSP-CASE-0004`
  2. *User*: "Who were the accused?" ➔ *Aloka*: Resolves accused for `KSP-CASE-0004`.
  3. *User*: "Now show KSP-CASE-0012" ➔ *Context Switch*: `ACTIVE CASE: KSP-CASE-0012`.

---

## Slide 8: Multi-Table Database Relationship Reasoning

### Slide Content
* **13 Connected Entities**: Full mapping across CaseMaster, Accused, Victims, Complainants, Officers, Ranks, Designations, Acts, and Sections.
* **Automated Join Discovery**: Dynamically resolves 1-to-many and many-to-many relationships without hardcoding queries.
* **MySQL 8 Reserved Keyword Protection**: Safely escapes reserved system keywords like `` `rank` `` in SQL syntax.
* **Domain Synonym Graph**: Connects terms like *"officers"*, *"personnel"*, *"posts"*, and *"statutes"* to their exact database tables.

### Speaker Notes
> "A major breakthrough in Aloka is our relational relationship reasoning engine. When a user asks 'Show employee ID, name, rank and designation for all officers', Aloka reasons over 3 distinct tables: `employee`, `rank`, and `designation`, connecting them via `RankID` and `DesignationID` to produce clean 16-row officer directories."

### Visual Suggestion
* Entity Relationship Diagram (ERD) showing `casemaster` at the core connected to `accused`, `victim`, `complainant`, `actsectionassociation`, and `unit`.

---

## Slide 9: Hybrid Semantic Crime Search

### Slide Content
* **Natural Language Modus Operandi Matching**: Discovers cases based on conceptual descriptions rather than exact keywords.
* **BM25 + Dense TF-IDF Engine**: In-memory vector space indexing 500+ case `BriefFacts`.
* **Domain Concept Expansion**: Expands crime terms (e.g., *"phishing"* expands to *fake link, SMS, OTP, fraud, URL*).
* **Relevance Scoring & Ranking**: Returns top matching cases with similarity scores, brief summaries, and station details.

### Speaker Notes
> "Traditional database searches fail if an investigator searches for 'ATM card cloned' and the database recorded 'debit card skimmed'. Aloka's semantic search engine uses BM25 with criminological synonym expansion to match concepts across case BriefFacts, returning ranked results with similarity scores."

### Visual Suggestion
* Diagram illustrating a query *"Cases involving fraudulent prize SMS"* expanding into semantic tokens, matching `BriefFacts` in the BM25 vector space, and outputting ranked case cards.

---

## Slide 10: Visual Analytics & The Data Center

### Slide Content
* **Automatic Chart Selection**: Deterministically selects the optimal visualization format based on query structure:
  * **Bar Chart**: Station comparisons, top crime categories, officer caseload rankings.
  * **Pie / Donut Chart**: Demographic distributions (gender, age groups, case status).
  * **Line Chart**: Time-series crime trends and chronological FIR registration rates.
* **Interactive Recharts Visualization**: Hover tooltips, responsive legends, and custom command center styling.
* **Key Insight Generation**: Automated analytical bullet points highlighting top categories and statistical percentages.

### Speaker Notes
> "When queries return aggregate or time-series data, Aloka automatically populates the Data Center panel. If you ask for 'Cases registered over time', it renders a smooth Line Chart. If you ask for 'Accused distribution by gender', it renders a Pie Chart with an automated Key Insight summary."

### Visual Suggestion
* Screenshot of the Data Center panel showing a Bar Chart of *Top Police Stations by Case Count* alongside the structured Data Table and Key Insight card.

---

## Slide 11: Multilingual Intelligence (English • ಕನ್ನಡ • हिन्दी)

### Slide Content
* **Universal Language Middleware**: Deterministic Unicode script detection (`\u0C80-\u0CFF` for Kannada, `\u0900-\u097F` for Hindi).
* **Case Token Protection**: Preserves FIR numbers (e.g., `KSP-CASE-0004`), personal names, and station codes during translation.
* **Bhashini & Fallback Engine**: Accurate bidirectional query translation and response generation.
* **Cross-Language Consistency**: Queries in Kannada generate the same accurate SQL and visualizations as English queries.

### Speaker Notes
> "Karnataka is a diverse state where field officers frequently work in Kannada. An officer can type 'ಯಾವ ಪೊಲೀಸ್ ಠಾಣೆಯಲ್ಲಿ ಹೆಚ್ಚು ಪ್ರಕರಣಗಳಿವೆ' (Which police station has the most cases?), and Aloka seamlessly normalizes the query, queries MySQL, and responds in fluent Kannada while rendering the English visualization."

### Visual Suggestion
* Split-screen comparison showing a Kannada question on the left and Hindi question on the right, both converging into the same SQL query and verified charts.

---

## Slide 12: Verified Technology Stack

### Slide Content
* **Frontend**: React 19.2, Vite 8.1, Tailwind CSS v4, Recharts 3.9, jsPDF 4.2, Lucide React.
* **Backend**: FastAPI 0.139, Uvicorn 0.51, LangGraph 1.2, SQLAlchemy 2.0, PyMySQL 1.2.
* **AI & Inference**: Groq Cloud LPU (`qwen/qwen3.8-27b`, `openai/gpt-oss-safeguard-20b`).
* **Database**: MySQL 8.0 Relational Case Database + SQLite 3 Session Store.
* **Containerization**: Docker (Python 3.12-slim) / Zoho Catalyst AppSail / Railway Cloud.

### Speaker Notes
> "Our technology stack was carefully chosen for sub-second latency and rock-solid reliability. We leverage React 19 with Vite on the frontend for instantaneous rendering, FastAPI with LangGraph on the backend for asynchronous agent orchestration, and Groq LPUs for ultra-fast model inference."

### Visual Suggestion
* Technology stack grid displaying official logos for React 19, FastAPI, LangGraph, Groq, MySQL, and Docker.

---

## Slide 13: Command Center User Experience (UI/UX)

### Slide Content
* **Institutional Command Center Design**: Calm, authoritative government dark theme (`#0B1017` / `#101722` / `#2F5DA8`).
* **Three-Panel Reactive Layout**:
  * **Sidebar**: New investigation launcher, session search, and conversation history.
  * **Conversation Stream**: Markdown reports, 5-stage AI processing card, and persistent composer auto-focus.
  * **Data Center**: Interactive charts, paginated data tables, executed SQL viewer, and PDF export.
* **Adjustable Split View**: Interactive drag-handle with layout presets (Default, 50/50, 70% Analytics, 85% Wide).

### Speaker Notes
> "We avoided flashy, neon 'AI chatbot' aesthetics in favor of a clean, institutional Command Center layout tailored for law enforcement. The UI features adjustable split views, interactive paginated data tables, live SQL inspection, and 1-click dossier export."

### Visual Suggestion
* Full-screen preview of the Aloka Command Center interface showing all three panels populated during an active investigation.

---

## Slide 14: Verification, Testing & Empirical Results

### Slide Content
* **100% Test Pass Rate**: Verified across Phase 1–7 test suites (Single case lookups, multi-table joins, analytics, semantic search).
* **Relationship Reasoning Benchmark**: Queries A through F (Employee, Rank, Designation) executed with 100% foreign-key accuracy.
* **Zero Production Build Errors**: Clean `npm run build` compilation (9.18s) and 0 backend crashes.
* **Strict Security Validation**: 100% rejection of non-`SELECT` statements (`DROP`, `DELETE`, `UPDATE`, `INSERT`).

### Speaker Notes
> "We rigorously tested Aloka against comprehensive test suites covering multi-table joins, aggregate queries, semantic search, and regional language translations. All 6 benchmark relationship queries passed with zero errors, and our frontend builds with zero warnings."

### Visual Suggestion
* Test matrix table summarizing test execution results across *Entity Lookups, Join Accuracy, Analytics, Semantic Search, and Safety Filters*.

---

## Slide 15: Impact & Future Scope

### Slide Content
* **Operational Law Enforcement Impact**:
  * Reduces intelligence retrieval time from minutes to milliseconds.
  * Democratizes state crime data access for non-technical field personnel.
  * Bridges linguistic divides with native Kannada and Hindi support.
* **Future Roadmap**:
  * Role-Based Access Control (RBAC) & Officer Authentication.
  * Geospatial Heatmap & GIS Mapping Integration.
  * Predictive Crime Hotspot Analytics & Real-Time Alert Subscriptions.
  * Automated Multilingual Voice Recognition via Edge Microphones.

### Speaker Notes
> "Aloka Intelligence transforms how law enforcement personnel interact with state crime data. By combining conversational ease with strict relational precision and regional language support, Aloka empowers officers to solve cases faster. In future phases, we plan to introduce GIS geospatial crime mapping and role-based access control. Thank you, and we are ready for your questions!"

### Visual Suggestion
* Vision roadmap diagram charting Phase 1–7 (Implemented) ➔ Phase 8 (GIS Mapping & RBAC) ➔ Phase 9 (Predictive Crime Analytics).

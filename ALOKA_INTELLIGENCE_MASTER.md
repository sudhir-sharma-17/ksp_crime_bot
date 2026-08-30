# ALOKA INTELLIGENCE (ಆಲೋಕ ಇಂಟೆಲಿಜೆನ್ಸ್)
## Master Project Documentation, Verified Tech Stack & Hackathon Presentation Deck

> **Project Name**: ALOKA INTELLIGENCE  
> **Agency / Authority**: Karnataka State Police (KSP) Intelligence Command Center  
> **Repository**: [https://github.com/sudhir-sharma-17/ksp_crime_bot.git](https://github.com/sudhir-sharma-17/ksp_crime_bot.git)  
> **Supported Languages**: English, Kannada (ಕನ್ನಡ), Hindi (हिन्दी)  
> **Source of Truth**: Verified directly against application source code repository

---

## 📑 Quick Navigation & Documentation Files

| Document | File Link | Description |
| :--- | :--- | :--- |
| **All-in-One Master Document** | [`ALOKA_INTELLIGENCE_MASTER.md`](file:///d:/SUDHIR/Hackathon/Datathon/Aloka_Intelligence/ALOKA_INTELLIGENCE_MASTER.md) | The complete unified master documentation and presentation package. |
| **15-Slide Presentation Deck** | [`ALOKA_PPT_CONTENT.md`](file:///d:/SUDHIR/Hackathon/Datathon/Aloka_Intelligence/ALOKA_PPT_CONTENT.md) | Slide-by-slide presentation deck with speaker scripts, concise bullets, and visuals. |
| **Complete Technical Report** | [`ALOKA_PROJECT_DOCUMENTATION.md`](file:///d:/SUDHIR/Hackathon/Datathon/Aloka_Intelligence/ALOKA_PROJECT_DOCUMENTATION.md) | 33-section comprehensive technical specification, architecture diagrams, and test results. |
| **Verified Technology Stack** | [`ALOKA_TECH_STACK.md`](file:///d:/SUDHIR/Hackathon/Datathon/Aloka_Intelligence/ALOKA_TECH_STACK.md) | Exact versioned technology stack across Frontend, Backend, AI Inference, and Database. |

---

# SECTION 1: VERIFIED TECHNOLOGY STACK

| Technology | Verified Version | Layer / Tier | Purpose in Aloka Intelligence |
| :--- | :--- | :--- | :--- |
| **React** | `19.2.7` | Frontend Core | Modern UI library building the reactive three-panel command center interface. |
| **React DOM** | `19.2.7` | Frontend Core | DOM rendering and component lifecycle management for the web application. |
| **Vite** | `8.1.1` | Frontend Build Engine | High-performance build tool, local development HMR server, and asset bundler. |
| **Tailwind CSS** | `4.3.2` | Frontend Styling | Utility-first CSS engine powering the dark/light institutional command center theme. |
| **@tailwindcss/vite** | `4.3.2` | Frontend Plugin | Vite integration plugin for Tailwind CSS v4 pipeline. |
| **@tailwindcss/typography** | `0.5.20` | Frontend Typography | Rich prose typography formatting for AI Markdown intelligence reports. |
| **Recharts** | `3.9.2` | Frontend Analytics | Dynamic SVG charting library rendering Bar, Pie, and Line visual analytics. |
| **Lucide React** | `1.24.0` | Frontend Icons | Comprehensive icon set for command center badges, navigation, and controls. |
| **jsPDF** | `4.2.1` | Frontend Reporting | Client-side vector PDF generation engine for confidential intelligence dossiers. |
| **jspdf-autotable** | `5.0.8` | Frontend Reporting | Structured grid table rendering plugin for exported PDF dossiers. |
| **React Markdown** | `10.1.0` | Frontend Markdown | Safe client-side Markdown parser and AST renderer for AI analytical summaries. |
| **remark-gfm** | `4.0.1` | Frontend Markdown | GitHub Flavored Markdown plugin supporting tables, strikethrough, and task lists. |
| **FastAPI** | `0.139.0` | Backend API Framework | Asynchronous, high-throughput RESTful API server powering intelligence endpoints. |
| **Uvicorn** | `0.51.0` | Backend ASGI Server | Lightning-fast ASGI web server running FastAPI with async event loop support. |
| **Starlette** | `1.3.1` | Backend Core | Underlying ASGI toolkit providing routing, middleware, and HTTP exceptions. |
| **Pydantic** | `2.13.4` | Backend Validation | Strict data validation and typing for request/response schemas and state payloads. |
| **LangGraph** | `1.2.9` | AI Orchestration | Multi-node stateful workflow engine orchestrating the 14-node intelligence graph. |
| **LangGraph Checkpoint** | `4.1.1` | AI State / Memory | In-memory conversation thread state checkpointer (`MemorySaver`). |
| **Groq Python SDK** | `0.37.1` | AI Inference SDK | Official asynchronous API client for ultra-low latency Groq Cloud LPU inference. |
| **SQLAlchemy** | `2.0.51` | Database Layer | Database toolkit and connection pool manager executing safe parameterized queries. |
| **PyMySQL** | `1.2.0` | MySQL Driver | Pure-Python MySQL client driver connecting backend engine to MySQL 8. |
| **pandas** | `3.0.3` | Data Processing | Data analysis and DataFrame manipulation for analytics and data transformations. |
| **numpy** | `2.5.1` | Numerical Computation | High-performance array operations supporting vector scoring and BM25 index math. |
| **deep-translator** | `1.11.4` | Translation Service | Translation wrapper used for Bhashini and Google fallback translation pipelines. |
| **Docker (Python 3.12-slim)** | `3.12-slim` | Container Runtime | Linux-based OCI container runtime packaging the FastAPI application. |
| **MySQL 8.0** | `8.0+` | Relational Database | Relational database hosting 500+ KSP case records, FIRs, accused, and personnel. |
| **SQLite 3** | Built-in | Client Session Cache | Local SQLite database (`sessions.db`) persisting historical investigator sessions. |

---

# SECTION 2: 15-SLIDE HACKATHON PRESENTATION DECK

### Slide 1: Title Slide — Aloka Intelligence
* **System**: ALOKA INTELLIGENCE (ಆಲೋಕ ಇಂಟೆಲಿಜೆನ್ಸ್)
* **Subtitle**: Multilingual AI-Powered State Police Intelligence & Criminological Command Center
* **Authority**: Built for Karnataka State Police (KSP) & Law Enforcement Investigators
* **Core Paradigm**: Zero-SQL Natural Language Conversational Access over Complex Relational Crime Databases
* **Languages**: English • ಕನ್ನಡ (Kannada) • हिन्दी (Hindi)
* **Speaker Note**: *"Good morning, judges. Law enforcement officers manage massive relational databases containing FIRs, accused profiles, penal sections, and personnel records. Today, we introduce Aloka Intelligence — an assistant enabling officers to query, analyze, semantically search, and visualize state crime records directly in natural language across English, Kannada, and Hindi."*

### Slide 2: Problem Statement
* **SQL Barrier for Field Personnel**: Officers should not need database programming skills during active investigations.
* **Complex Multi-Table Schemas**: Crime data is fragmented across 13+ relational tables.
* **Semantic Ambiguity**: Terms like *"fraud"* or *"police personnel"* do not directly match database column names.
* **Loss of Conversational Context**: Traditional tools cannot understand follow-up questions (*"Who was the accused in that case?"*).
* **Linguistic Barriers**: Field officers frequently think and operate in Kannada and Hindi.

### Slide 3: Proposed Solution
* **Natural Language to Verified SQL**: Translates plain text questions into optimized, schema-validated MySQL queries.
* **14-Node Stateful AI Graph**: Orchestrated via LangGraph with multi-step validation and automated self-correction.
* **Relational Relationship Reasoning**: Automatically navigates foreign key paths (`casemaster → accused`, `employee → rank → designation`).
* **Hybrid Semantic Crime Search**: In-memory BM25 + dense TF-IDF vector space engine to discover similar modus operandi across brief facts.
* **Instant Visual Analytics & PDF Export**: Automatic generation of Bar, Pie, and Line charts + 1-click confidential PDF dossier generation.

### Slide 4: Key Objectives & Scope
* **Zero-SQL Data Accessibility**: Extract relational records without technical query syntax.
* **Multi-Turn Contextual Memory**: Maintain active case IDs, suspect names, and police stations across continuous conversations.
* **Read-Only Database Safeguards**: Enforce strict `SELECT`-only execution to prevent data corruption.
* **Self-Healing SQL Generation**: Automatically catch and repair syntax errors in real time.
* **Operational Command Center UI**: Modern, high-density dashboard featuring a 3-panel layout, session history, and live SQL inspection.

### Slide 5: System Architecture
* **Frontend Layer**: React 19 + Tailwind CSS v4 Command Center with real-time state synchronization.
* **API Gateway**: FastAPI async web service providing non-blocking query execution.
* **StateGraph Orchestrator**: 14 specialized LangGraph nodes handling language detection, intent classification, planning, SQL generation, execution, and analytics.
* **Inference Layer**: Groq Cloud LPU running high-performance models (`qwen/qwen3.8-27b`, `openai/gpt-oss-safeguard-20b`).
* **Database & Search**: MySQL 8.0 relational case repository + in-memory BM25 semantic index.

### Slide 6: The AI Query Pipeline in Action
* **Step 1 — Language Normalization**: Detects Kannada/Hindi, isolates case tokens (`KSP-CASE-0004`), and maps regional phrasing.
* **Step 2 — Intent Router**: Dispatches query to `DATABASE`, `SEMANTIC_SEARCH`, `CYBER`, or `CHAT`.
* **Step 3 — Query Planner**: Produces a formal JSON specification with target tables and required foreign-key joins.
* **Step 4 — Schema Validator**: Inspects tables, injects missing join keys, and verifies field validity against `DB_SCHEMA`.
* **Step 5 — SQL Generation & Safety Guard**: Synthesizes clean SQL and applies strict regex and token security filters.
* **Step 6 — Execution & Synthesis**: Runs query on MySQL, calculates totals, and renders formatted analytical Markdown.

### Slide 7: Conversational Context & Multi-Turn Intelligence
* **Active Entity Tracking**: Automatically remembers `active_case`, `active_person`, and `active_station`.
* **Pronoun Resolution**: Understands queries like *"Who was the victim?"* after examining a case.
* **Context Switching**: Instantly shifts focus when a new case or station ID is introduced.
* **Global Query Isolation**: Bypasses active case filters when users ask broad questions like *"List all police stations"*.
* **Ambiguity Detection**: Prompts the user for clarification if a reference is missing or unclear.

### Slide 8: Multi-Table Database Relationship Reasoning
* **13 Connected Entities**: Full mapping across CaseMaster, Accused, Victims, Complainants, Officers, Ranks, Designations, Acts, and Sections.
* **Automated Join Discovery**: Dynamically resolves 1-to-many and many-to-many relationships without hardcoding queries.
* **MySQL 8 Reserved Keyword Protection**: Safely escapes reserved system keywords like `` `rank` `` in SQL syntax.
* **Domain Synonym Graph**: Connects terms like *"officers"*, *"personnel"*, *"posts"*, and *"statutes"* to their exact database tables.

### Slide 9: Hybrid Semantic Crime Search
* **Modus Operandi Matching**: Discovers cases based on conceptual descriptions rather than exact keywords.
* **BM25 + Dense TF-IDF Engine**: In-memory vector space indexing 500+ case `BriefFacts`.
* **Domain Concept Expansion**: Expands crime terms (e.g., *"phishing"* expands to *fake link, SMS, OTP, fraud, URL*).
* **Relevance Scoring & Ranking**: Returns top matching cases with similarity scores, brief summaries, and station details.

### Slide 10: Visual Analytics & The Data Center
* **Automatic Chart Selection**: Deterministically selects the optimal visualization format based on query structure:
  * **Bar Chart**: Station comparisons, top crime categories, officer caseload rankings.
  * **Pie / Donut Chart**: Demographic distributions (gender, age groups, case status).
  * **Line Chart**: Time-series crime trends and chronological FIR registration rates.
* **Interactive Recharts Visualization**: Hover tooltips, responsive legends, and custom command center styling.
* **Key Insight Generation**: Automated analytical bullet points highlighting top categories and statistical percentages.

### Slide 11: Multilingual Intelligence (English • ಕನ್ನಡ • हिन्दी)
* **Universal Language Middleware**: Deterministic Unicode script detection (`\u0C80-\u0CFF` for Kannada, `\u0900-\u097F` for Hindi).
* **Case Token Protection**: Preserves FIR numbers (e.g., `KSP-CASE-0004`), personal names, and station codes during translation.
* **Bhashini & Fallback Engine**: Accurate bidirectional query translation and response generation.
* **Cross-Language Consistency**: Queries in Kannada generate the same accurate SQL and visualizations as English queries.

### Slide 12: Verified Technology Stack
* **Frontend**: React 19.2, Vite 8.1, Tailwind CSS v4, Recharts 3.9, jsPDF 4.2, Lucide React.
* **Backend**: FastAPI 0.139, Uvicorn 0.51, LangGraph 1.2, SQLAlchemy 2.0, PyMySQL 1.2.
* **AI & Inference**: Groq Cloud LPU (`qwen/qwen3.8-27b`, `openai/gpt-oss-safeguard-20b`).
* **Database**: MySQL 8.0 Relational Case Database + SQLite 3 Session Store.
* **Containerization**: Docker (Python 3.12-slim) / Zoho Catalyst AppSail / Railway Cloud.

### Slide 13: Command Center User Experience (UI/UX)
* **Institutional Command Center Design**: Calm, authoritative government dark theme (`#0B1017` / `#101722` / `#2F5DA8`).
* **Three-Panel Reactive Layout**:
  * **Sidebar**: New investigation launcher, session search, and conversation history.
  * **Conversation Stream**: Markdown reports, 5-stage AI processing card, and persistent composer auto-focus.
  * **Data Center**: Interactive charts, paginated data tables, executed SQL viewer, and PDF export.
* **Adjustable Split View**: Interactive drag-handle with layout presets (Default, 50/50, 70% Analytics, 85% Wide).

### Slide 14: Verification, Testing & Empirical Results
* **100% Test Pass Rate**: Verified across Phase 1–7 test suites (Single case lookups, multi-table joins, analytics, semantic search).
* **Relationship Reasoning Benchmark**: Queries A through F (Employee, Rank, Designation) executed with 100% foreign-key accuracy.
* **Zero Production Build Errors**: Clean `npm run build` compilation (9.18s) and 0 backend crashes.
* **Strict Security Validation**: 100% rejection of non-`SELECT` statements (`DROP`, `DELETE`, `UPDATE`, `INSERT`).

### Slide 15: Impact & Future Scope
* **Operational Impact**: Reduces intelligence retrieval time from minutes to milliseconds, democratizes data access, and eliminates linguistic barriers.
* **Future Roadmap**: Role-Based Access Control (RBAC), Geospatial GIS crime heatmaps, and predictive crime hotspot analytics.

---

# SECTION 3: 14-NODE STATEGRAPH ARCHITECTURE

```
                               ┌──────────────────────────┐
                               │  [1. translation_input]  │
                               └────────────┬─────────────┘
                                            │
                                            ▼
                               ┌──────────────────────────┐
                               │   [2. intent_router]     │
                               └──────┬─────┬─────┬───────┘
                                      │     │     │
                 ┌────────────────────┘     │     └─────────────────────┐
                 │                          │                           │
                 ▼                          ▼                           ▼
      ┌────────────────────┐     ┌────────────────────┐      ┌────────────────────┐
      │ [3. chat_response] │     │  [4. cyber_node]   │      │[5. semantic_search]│
      └──────────┬─────────┘     └──────────┬─────────┘      └──────────┬─────────┘
                 │                          │                           │
                 │                          │                           ▼
                 │                          │                ┌────────────────────┐
                 │                          │                │ [13. analyze_data] │
                 │                          │                └──────────┬─────────┘
                 │                          │                           │
                 │                          │                           ▼
                 │                          │                ┌────────────────────┐
                 │                          │                │[14.translation_out]│
                 │                          │                └──────────┬─────────┘
                 │                          │                           │
                 │                          │                           ▼
                 │                          │                        [ END ]
                 │                          │                           ▲
                 ▼                          ▼                           │
        ┌───────────────────────────────────────────────────────────────┤
        │                     [6. query_splitter]                       │
        └───────────────────────────────┬───────────────────────────────┘
                                        │
                                        ▼
                              ┌───────────────────┐
                              │[7. query_planner] │
                              └─────────┬─────────┘
                                        │
                                        ▼
                            ┌───────────────────────┐
                            │ [8. schema_validator] │
                            └───────────┬───────────┘
                                        │
                                        ▼
                              ┌───────────────────┐
                              │ [9. generate_sql] │
                              └─────────┬─────────┘
                                        │
                                        ▼
                              ┌───────────────────┐
                              │ [10. execute_sql] │
                              └─────────┬─────────┘
                                        │
                     ┌──────────────────┴──────────────────┐
                     │ (If error & retries <= 3)           │ (Success)
                     ▼                                     ▼
           ┌───────────────────┐                 ┌────────────────────┐
           │[11. self_correct] │                 │[12. next_query_node│
           └─────────┬─────────┘                 └──────────┬─────────┘
                     │                                      │
                     └──────────────► [10. execute_sql]     ├──► (More queries) ──► [7. query_planner]
                                                            └──► (Finished)     ──► [13. analyze_data]
```

---

# SECTION 4: JUDGE QUESTIONS & VERIFIED ANSWERS

### Q1: How does Aloka prevent SQL injection or database tampering?
> **Answer**: Aloka enforces multiple layers of security:
> 1. Generated SQL must begin strictly with `SELECT`. Any destructive statements (`DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`, `TRUNCATE`, `EXEC`) are immediately intercepted and rejected before execution.
> 2. Queries are executed through parameterized SQLAlchemy connections with short timeouts and read-only access.
> 3. Pagination is strictly clamped to 16 rows per page (`LIMIT 16 OFFSET 0`) to prevent memory exhaustion.

### Q2: How does Aloka handle regional Indian languages like Kannada and Hindi?
> **Answer**: Aloka employs a deterministic Unicode script detector (`[\u0C80-\u0CFF]` for Kannada, `[\u0900-\u097F]` for Devanagari/Hindi). It isolates critical case tokens (e.g., `KSP-CASE-0004`), personal names, and station codes, normalizes the query into canonical English for query planning, executes the SQL against MySQL, and synthesizes the final Markdown response in fluent Kannada or Hindi while simultaneously rendering the interactive visualization.

### Q3: What happens if the LLM generates a SQL query with a syntax error?
> **Answer**: Aloka features a self-correcting feedback loop in LangGraph (`self_correct_node`). When MySQL returns an error (such as a reserved keyword issue or invalid column), the error message is fed back into the model context with explicit instructions to repair the query (up to 3 retries) without crashing the application.

---

## 🚀 Repository & Build Status

* **GitHub Repository**: [`https://github.com/sudhir-sharma-17/ksp_crime_bot.git`](https://github.com/sudhir-sharma-17/ksp_crime_bot.git)
* **Frontend Build**: `npm run build` completed cleanly in `9.18s` (Zero compilation errors).
* **Backend Status**: FastAPI & LangGraph running live on port `9000`.

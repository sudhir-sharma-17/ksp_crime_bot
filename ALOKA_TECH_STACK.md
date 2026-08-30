# ALOKA INTELLIGENCE — VERIFIED TECHNOLOGY STACK

> **Source of Truth Verification**: All technologies, frameworks, libraries, drivers, and runtime environments listed below have been directly inspected and verified from the project repository (`frontend/package.json`, `backend/requirements.txt`, `backend/Dockerfile`, and application source modules).

---

## 1. Complete Technology Stack Table

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
| **Three.js** | `0.185.1` | Frontend Graphics | 3D WebGL library used for visual rendering capabilities. |
| **@react-three/fiber** | `9.6.1` | Frontend Graphics | Declarative React renderer wrapper for Three.js. |
| **@react-three/drei** | `10.7.7` | Frontend Graphics | Helper library and shader utilities for React Three Fiber. |
| **Oxlint** | `1.71.0` | Frontend Dev Tools | High-speed Rust-based code linter for JavaScript and JSX code quality. |
| **FastAPI** | `0.139.0` | Backend API Framework | Asynchronous, high-throughput RESTful API server powering intelligence endpoints. |
| **Uvicorn** | `0.51.0` | Backend ASGI Server | Lightning-fast ASGI web server running FastAPI with async event loop support. |
| **Starlette** | `1.3.1` | Backend Core | Underlying ASGI toolkit providing routing, middleware, and HTTP exceptions. |
| **Pydantic** | `2.13.4` | Backend Validation | Strict data validation and typing for request/response schemas and state payloads. |
| **Pydantic Core** | `2.46.4` | Backend Core | High-performance C/Rust serialization core powering Pydantic v2. |
| **LangGraph** | `1.2.9` | AI Orchestration | Multi-node stateful workflow engine orchestrating the 14-node intelligence graph. |
| **LangGraph Checkpoint** | `4.1.1` | AI State / Memory | In-memory conversation thread state checkpointer (`MemorySaver`). |
| **LangChain Core** | `1.4.9` | AI Integration | Base abstractions for messages, prompt templates, and output parsers. |
| **LangChain Groq** | `1.1.3` | AI Provider Driver | Groq Cloud inference client interface for LLM completions. |
| **Groq Python SDK** | `0.37.1` | AI Inference SDK | Official asynchronous API client for ultra-low latency Groq Cloud LPU inference. |
| **SQLAlchemy** | `2.0.51` | Database Layer | Database toolkit and connection pool manager executing safe parameterized queries. |
| **PyMySQL** | `1.2.0` | MySQL Driver | Pure-Python MySQL client driver connecting backend engine to MySQL 8. |
| **mysql-connector-python** | `9.7.0` | MySQL Driver | Official Oracle MySQL client library for administrative and connector routines. |
| **pandas** | `3.0.3` | Data Processing | Data analysis and DataFrame manipulation for analytics and data transformations. |
| **numpy** | `2.5.1` | Numerical Computation | High-performance array operations supporting vector scoring and BM25 index math. |
| **deep-translator** | `1.11.4` | Translation Service | Translation wrapper used for Bhashini and Google fallback translation pipelines. |
| **HTTPX** | `0.28.1` | Async HTTP Client | Asynchronous HTTP client making non-blocking REST calls to external AI APIs. |
| **Requests** | `2.34.2` | Sync HTTP Client | Standard HTTP library for synchronous external data and integration requests. |
| **BeautifulSoup4** | `4.15.0` | Web & Text Parsing | HTML and XML parsing library used for sanitizing and stripping formatted text. |
| **Faker** | `40.28.1` | Synthetic Data | Realistic data generation library used in KSP database seeding and benchmarking. |
| **Python-Dotenv** | `1.2.2` | Configuration | Environment variable loader populating API keys and database credentials. |
| **PyYAML** | `6.0.3` | Configuration | YAML parser for structured configuration schemas and prompts. |
| **Tenacity** | `9.1.4` | Resilience / Retries | Retrying library with exponential backoff for network resilience. |
| **Docker (Python 3.12-slim)** | `3.12-slim` | Container Runtime | Linux-based OCI container runtime packaging the FastAPI application. |
| **MySQL 8.0** | `8.0+` | Relational Database | Relational database hosting 500+ KSP case records, FIRs, accused, and personnel. |
| **SQLite 3** | Built-in | Client Session Cache | Local SQLite database (`sessions.db`) persisting historical investigator sessions. |

---

## 2. Verified LLM Models & Inference Endpoints

| Model Identifier | Provider / Engine | Primary Task in Aloka Pipeline |
| :--- | :--- | :--- |
| `qwen/qwen3.8-27b` | Groq Cloud LPU | Primary reasoning engine for Intent Routing, Query Planning, and SQL Generation. |
| `openai/gpt-oss-safeguard-20b` | Groq Cloud LPU | High-availability fallback engine for SQL generation and safe execution. |
| `qwen/qwen3.6-27b` | Groq Cloud LPU | Secondary fallback engine for structured analytical summaries and translation. |

---

## 3. Database Schema Entities & Tables (Verified from `DB_SCHEMA`)

1. `casemaster` — Central FIR case registry (CaseNo, BriefFacts, CrimeRegisteredDate, Station, District).
2. `accused` — Details of accused individuals (Name, Age, Gender, Occupation, ArrestStatus, CaseMasterID).
3. `victim` — Details of victims associated with criminal incidents (Name, Age, Gender, InjuryType, CaseMasterID).
4. `complainant` — Details of individuals who lodged FIRs (Name, Age, Gender, Address, CaseMasterID).
5. `employee` — Karnataka Police personnel directory (EmployeeID, FirstName, LastName, RankID, DesignationID, UnitID).
6. `rank` — Police hierarchy ranks (RankID, RankName, HierarchyLevel).
7. `designation` — Official post/designation designations (DesignationID, DesignationName).
8. `unit` — Police stations and administrative units (UnitID, UnitName, UnitType, DistrictID).
9. `district` — District jurisdiction registry (DistrictID, DistrictName, StateName).
10. `court` — Designated jurisdictional judicial courts (CourtID, CourtName, CourtType).
11. `act` — Legal acts and statutes (ActID, ActName, EnactmentYear).
12. `section` — Specific penal legal sections (SectionID, SectionName, Description, BailableStatus).
13. `actsectionassociation` — Association bridge linking FIR cases to applicable Acts & Sections.

---

## 4. Hardware & Runtime Infrastructure

* **Container Runtime**: Docker OCI-compliant container (`python:3.12-slim`).
* **Cloud Platform Compatibility**: Zoho Catalyst AppSail (dynamic port binding via `X_ZOHO_CATALYST_LISTEN_PORT`), Railway Cloud Deployment, Docker Compose, Bare-Metal Linux/Windows.
* **Database Protocol**: TCP/IP MySQL connection pooling via SQLAlchemy over port `3306` / SSL.

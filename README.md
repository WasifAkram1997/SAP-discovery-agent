# SAP Process Discovery Agent

AI-powered agentic system that intelligently maps business processes to SAP artifacts (modules, transaction codes, Fiori apps, execution flows) using LangGraph, LangChain, and OpenAI GPT-4.

## 🎯 Overview

Built for the **Syntax GenAI Platform Developer Assessment**, this project demonstrates advanced agentic workflows with quality-based iterative reasoning, multi-user session management, and production-ready architecture.

### Key Capabilities

- **Intelligent Agentic Workflow**: Quality-driven reasoning loop (`plan → action → scoring → synthesis`) that iterates until 60% confidence threshold
- **Multi-User Session Isolation**: Thread-safe session management with job tracking and automatic cleanup
- **Dual-Tool Integration**: MCP Server for SAP documentation + Serper API for web search
- **Conversational Interface**: Natural language chat with context-aware memory
- **Batch Processing**: Handle multiple processes concurrently with progress tracking
- **Production Features**: File logging with rotation, comprehensive testing, Docker deployment

## 🏗️ Architecture

### Agentic Reasoning Loop
```
START → plan → action → scoring → synthesis → END
         ↑                  │
         └──────────────────┘
    (iterates until quality ≥ 0.60 or max 3 iterations)
```

**Quality Dimensions** (weighted equally):
- Module Coverage - SAP modules identified (MM, FI, CO, SD, etc.)
- T-Code Confidence - Transaction codes found
- Fiori Presence - Fiori apps mentioned
- Execution Flow Depth - Step-by-step process flow

### Tech Stack

**Backend:**
- FastAPI (async REST API with Uvicorn)
- LangGraph 1.0 (workflow orchestration)
- LangChain 1.0 (agent framework)
- PostgreSQL (conversation memory via LangGraph checkpointer)
- Python 3.11

**Frontend:**
- React 18 + TypeScript
- Tailwind CSS
- Vite (build tool)
- Axios (HTTP client)

**Infrastructure:**
- Docker + Docker Compose
- PostgreSQL 16
- MCP (Model Context Protocol) Server

## 🚀 Quick Start

### Option 1: Docker (Recommended for Demo)

**Prerequisites**: Docker, Docker Compose

```bash
# 1. Clone repository
git clone <repository-url>
cd sap-process-discovery

# 2. Create .env file (copy from template)
cp .env.example .env

# 3. Edit .env with your API keys
# Required: OPENAI_API_KEY, SERPER_API_KEY
# Optional: LANGSMITH_* (for tracing)

# 4. Start all services with one command
docker-compose up

# Services will be available at:
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:8001
# - API Docs: http://localhost:8001/docs
# - PostgreSQL: localhost:5432
```

### Option 2: Manual Setup (Development)

**Prerequisites**: Python 3.10+, Node.js 18+, PostgreSQL 14+

```bash
# 1. Clone and navigate
git clone <repository-url>
cd sap-process-discovery

# 2. Run automated setup script
./setup.sh

# 3. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 4. Start backend (terminal 1)
cd backend
uvicorn api.main:app --host 0.0.0.0 --port 8001

# 5. Start frontend (terminal 2)
cd frontend
npm run dev

# 6. Open http://localhost:3000
```

## 📋 Configuration

### Environment Variables

Create `.env` with the following:

```bash
# OpenAI API (required)
OPENAI_API_KEY=your_openai_api_key_here

# Web Search (required for supplementary research)
SERPER_API_KEY=your_serper_api_key_here

# Database URL (for LangGraph conversation memory)
LANGGRAPH_DATABASE_URL=postgresql://postgres:abcd1234@localhost:5432/sap_discovery

# LangSmith Tracing (optional)
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_key_here
LANGSMITH_PROJECT=sap-discovery
```

## 🧪 Testing

The project includes unit tests for critical functionality:

```bash
cd backend

# Run all tests
pytest tests/ -v

# Run specific test files
pytest tests/test_session_isolation.py -v
pytest tests/test_api_health.py -v

# Expected output: 4 tests pass
# - 2 session isolation tests (proves multi-user safety)
# - 2 API health tests (proves system works)
```

## 📂 Project Structure

```
sap-process-discovery/
├── backend/
│   ├── api/
│   │   ├── main.py              # FastAPI application entry point
│   │   ├── middleware.py        # Session middleware
│   │   └── models.py            # API request/response models
│   ├── sap_discovery/
│   │   ├── workflow/
│   │   │   ├── graph.py         # LangGraph workflow definition
│   │   │   ├── state.py         # Agent state schema
│   │   │   └── nodes.py         # Workflow nodes (plan, action, scoring, synthesis)
│   │   ├── main_agent/
│   │   │   ├── agent.py         # Main conversational agent
│   │   │   ├── chat.py          # Chat interface
│   │   │   └── tools.py         # Agent tools (run_sap_discovery, export, report)
│   │   ├── models/
│   │   │   └── schema.py        # Structured output schemas (SAPProcessMapping)
│   │   ├── tools/
│   │   │   ├── registry.py      # Tool initialization (MCP)
│   │   │   └── web_tools.py     # Web search tools
│   │   ├── llm/
│   │   │   └── models.py        # LLM instance creation
│   │   ├── utils/
│   │   │   ├── logging.py       # File logging with rotation (10MB FIFO)
│   │   │   ├── session_state.py # In-memory session state management
│   │   │   └── storage.py       # File upload handling
│   │   └── data/
│   │       └── loader.py        # Excel data loading
│   ├── tests/
│   │   ├── conftest.py          # Pytest configuration
│   │   ├── test_session_isolation.py  # Session safety tests
│   │   └── test_api_health.py         # API endpoint tests
|   |
│   ├── requirements.txt         # Python dependencies
│   ├── Dockerfile              # Backend container config
│   └── .env.example            # Environment template
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── services/
│   │   │   └── api.ts          # API client
│   │   ├── types/              # TypeScript interfaces
│   │   └── App.tsx             # Main application
│   ├── package.json
│   ├── Dockerfile              # Frontend container config
│   └── vite.config.ts
├── data/
│   └── input/
│       └── Car_Rental_Business_Processes_Detailed.xlsx
├── docs/
│   ├── QUICKSTART.md           # Detailed setup guide
│   ├── ARCHITECTURE.md         # System architecture
│   └── POSTGRESQL_SETUP.md     # Database setup
├── logs/                       # Application logs (auto-created)
├── uploads/                    # User file uploads (auto-created)
├── docker-compose.yml          # Multi-container orchestration
├── setup.sh                    # Automated setup script
└── README.md
```

## 🎨 Features Deep Dive

### 1. Session-Based Multi-User Architecture

- **Isolation**: Each user session has isolated state (no data cross-contamination)
- **Job Tracking**: Multiple Excel uploads per session tracked with unique job IDs
- **In-Memory Storage**: Fast access to session data and discovery results

### 2. Quality-Driven Agentic Workflow

The discovery subagent uses a sophisticated reasoning loop:

1. **Plan Node**: Analyzes quality gaps and decides which tools to call
2. **Action Node**: Executes SAP docs search and/or web search
3. **Scoring Node**: Evaluates results across 4 dimensions (0-1 scale each)
4. **Synthesis Node**: Produces final structured `SAPProcessMapping`

**Iteration Logic**: Loops until `overall_quality ≥ 0.60` or max 3 iterations

### 3. File Logging with Rotation

- **Location**: `backend/logs/sap_discovery.log`
- **Rotation**: FIFO deletion when file exceeds 10MB
- **Backups**: Keeps 5 old files (60MB total maximum)
- **Format**: `[timestamp] [module] LEVEL: message`

### 4. Structured Output Schema

```python
class SAPProcessMapping(BaseModel):
    process: str                              # Business process name
    module: List[str]                         # SAP modules (MM, FI, CO, SD, etc.)
    transaction_codes: List[str]              # T-codes (ME21N, FB01, etc.)
    fiori_apps: List[str]                     # Fiori app IDs
    execution_flow: List[str]                 # Step-by-step flow
    configuration_dependencies: List[str]      # Config requirements
    integration_points: List[str]             # System integrations
    references: List[Reference]               # Source citations
```

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/health` | GET | Health check (agent status, timestamp) |
| `/chat` | POST | Send message (text + optional Excel file) |
| `/docs` | GET | Interactive API documentation (Swagger UI) |

## 🔧 Development

### Rebuild Docker Containers

```bash
# Rebuild specific service
docker-compose build backend
docker-compose build frontend

# Rebuild all services
docker-compose build

# Start with fresh build
docker-compose up --build
```

### View Logs

```bash
# Docker logs (live)
docker-compose logs -f backend
docker-compose logs -f frontend

# Local file logs
tail -f backend/logs/sap_discovery.log
```

### Database Access

```bash
# Connect to PostgreSQL (Docker)
docker-compose exec postgres psql -U postgres -d sap_discovery

# View conversation memory
SELECT thread_id, checkpoint_id FROM checkpoints LIMIT 10;
```

## 📖 Documentation

- **[Architecture Overview](docs/ARCHITECTURE.md)** - System design, agentic workflow, node descriptions
- **[Quick Start Guide](docs/QUICKSTART.md)** - Detailed manual setup instructions
- **[PostgreSQL Setup](docs/POSTGRESQL_SETUP.md)** - Database configuration guide

## 🚧 Known Limitations & Future Work

**Current Limitations:**
- In-memory session storage (data lost on server restart)
- No authentication/authorization (single-tenant)
- MCP server URL is hardcoded (should be configurable)

**Potential Enhancements:**
- Redis for distributed session cache (horizontal scaling)
- Celery task queue for async job processing
- Response caching for common SAP lookups
- LLM cost tracking per session
- Streaming responses (SSE) for real-time progress
- Export to multiple formats (PDF, JSON, CSV)

## 👥 Contributors

Gazi Wasif Akram

---

**Built for**: Syntax Software Developer Assessment
**Focus**: Agent orchestration, production architecture, scalability thinking
**Date**: 2026

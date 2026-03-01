# Quick Start Guide - SAP Process Discovery

## 🚀 Starting the Application (Windows)

### Backend API

Your PostgreSQL is already configured and ready! Use this command:

```bash
# From project root
python start_api.py
```

**Why not `uvicorn` directly?** Windows + PostgreSQL + async requires special event loop handling. The `start_api.py` script handles this automatically.

Wait for this message:
```
============================================================
API Ready! Agent initialized successfully.
============================================================
INFO:     Uvicorn running on http://0.0.0.0:8001
```

### Frontend (React)

In a **new terminal**:

```bash
cd frontend-react
npm install  # First time only
npm run dev
```

Open: **http://localhost:3000**

## ✅ Test It Works

### 1. Check API Health
```bash
curl http://localhost:8001/health
```

Should return: `{"status":"healthy","agent":true,...}`

### 2. Send a Chat Message
```bash
curl -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, what can you help me with?"}'
```

### 3. Use the React Frontend
- Open http://localhost:3000
- Type: "Run SAP discovery"
- Watch the agent work!

## 📁 Project Structure

```
.
├── api/                          # FastAPI backend
│   ├── main.py                   # API entry point
│   ├── models.py                 # Request/response models
│   └── middleware.py             # Session middleware
│
├── sap_discovery/                # Core agent logic
│   ├── workflow/                 # LangGraph workflow
│   ├── main_agent/               # Conversational agent
│   └── tools/                    # SAP tools (MCP + web)
│
├── frontend-react/               # React UI
│   ├── src/
│   │   ├── components/           # Chat UI components
│   │   ├── services/api.ts       # API client
│   │   └── App.tsx               # Main app
│   └── package.json
│
├── start_api.py                  # Windows-friendly startup
├── .env                          # Configuration
└── POSTGRESQL_SETUP.md           # Detailed setup guide
```

## 🎯 Sample Commands

Try these in the frontend:

1. **Run Discovery**
   ```
   Run SAP discovery
   ```

2. **View Results**
   ```
   Display the results
   ```

3. **Export Data**
   ```
   Export to Excel
   ```

4. **Combined**
   ```
   Run and print
   ```

## 🔧 Configuration

Your `.env` file:
```env
OPENAI_API_KEY=sk-proj-...
DATABASE_URL=postgresql+psycopg://postgres:abcd1234@localhost:5432/sap_discovery
SERPER_API_KEY=347914d...
LANGSMITH_TRACING=true
```

## 📊 What Gets Stored in PostgreSQL

LangGraph automatically creates these tables:
- **checkpoints** - Conversation snapshots
- **checkpoint_writes** - State updates
- **checkpoint_metadata** - Additional data

You can view the data:
```sql
psql -U postgres -d sap_discovery
SELECT * FROM checkpoints;
```

## 🐛 Troubleshooting

### API won't start - "ProactorEventLoop" error
**Solution**: Use `python start_api.py` (not `uvicorn` directly)

### Frontend can't connect
**Solution**: Check API is running on port 8001
```bash
curl http://localhost:8001/health
```

### PostgreSQL connection failed
**Solution**: Check PostgreSQL is running
```bash
psql -U postgres -c "SELECT 1"
```

### Want simpler setup?
**Solution**: Use SQLite instead (see POSTGRESQL_SETUP.md)

## 📚 Documentation

- **POSTGRESQL_SETUP.md** - Detailed PostgreSQL setup
- **frontend-react/README.md** - React frontend docs
- **CLAUDE.md** - Project architecture
- **API Docs** - http://localhost:8001/docs (when running)

## 🎨 Tech Stack

**Backend**:
- FastAPI - Modern Python web framework
- LangGraph - Agent workflow orchestration
- LangChain - LLM application framework
- PostgreSQL - Persistent memory
- OpenAI GPT-4 - Main LLM
- MCP Server - SAP Help Portal integration

**Frontend**:
- React 18 - UI library
- TypeScript - Type safety
- Vite - Build tool
- Tailwind CSS - Styling
- Axios - HTTP client

## 🚢 Next Steps

1. **Explore the UI** - Try different commands
2. **Check Memory** - Restart API, see conversations persist
3. **Customize** - Edit prompts in `sap_discovery/main_agent/prompts.py`
4. **Extend** - Add new tools in `sap_discovery/tools/`

---

**Need help?** Check POSTGRESQL_SETUP.md or the API docs at http://localhost:8001/docs

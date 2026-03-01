# PostgreSQL Integration - Windows Setup

## Issue Summary

PostgreSQL integration with LangGraph on Windows requires special handling due to `psycopg`'s async driver limitations:

- `psycopg` requires `WindowsSelectorEventLoopPolicy` instead of the default `ProactorEventLoop`
- Event loop policy must be set **before** uvicorn creates its event loop
- Standard `uvicorn api.main:app` command doesn't work

## Your Configuration

```env
DATABASE_URL=postgresql+psycopg://postgres:abcd1234@localhost:5432/sap_discovery
```

✅ Database connection tested successfully
✅ psycopg[binary] installed
✅ Connection lifecycle fixed in code

## ✅ Working Solution

Use the provided `start_api.py` script which properly sets up the event loop:

```bash
python start_api.py
```

This script:
1. Sets `WindowsSelectorEventLoopPolicy` before any imports
2. Creates the event loop explicitly
3. Passes it to uvicorn with `loop="none"`

## Alternative: Use SQLite (Simpler for Development)

If you want to avoid Windows async complications, SQLite works perfectly:

### Step 1: Update `.env`
```env
# Comment out PostgreSQL
# DATABASE_URL=postgresql+psycopg://postgres:abcd1234@localhost:5432/sap_discovery

# Use SQLite instead
DATABASE_URL=sqlite:///agent_memory.db
```

### Step 2: Update `api/main.py`
```python
# Change import
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

# In lifespan function, replace:
memory_context = AsyncPostgresSaver.from_conn_string(DATABASE_URL)
# With:
memory_context = AsyncSqliteSaver.from_conn_string(DATABASE_URL)
```

### Benefits of SQLite:
- No event loop issues on Windows
- No external database server needed
- Still persistent across restarts
- File-based: `agent_memory.db`
- Zero configuration

## Testing the API

### Start the server:
```bash
python start_api.py
```

### Expected output:
```
[OK] Set WindowsSelectorEventLoopPolicy for psycopg compatibility
[OK] Created new event loop: SelectorEventLoop
INFO:     Started server process
...
[6/6] Main agent created
============================================================
API Ready! Agent initialized successfully.
============================================================
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8001
```

### Test the chat endpoint:
```bash
curl -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```

### Check health:
```bash
curl http://localhost:8001/health
```

## Starting the React Frontend

Once the API is running:

```bash
cd frontend-react
npm install
npm run dev
```

Open: http://localhost:3000

## Troubleshooting

### "Psycopg cannot use the 'ProactorEventLoop'"
**Solution**: Use `python start_api.py` instead of `uvicorn` directly

### "Connection refused" from frontend
**Solution**: Make sure API is running on port 8001

### Want auto-reload during development?
The `start_api.py` has `reload=False` to avoid event loop conflicts. For development:
1. Option A: Manually restart after code changes
2. Option B: Use SQLite (supports reload with `uvicorn --reload`)

## Production Deployment

For production on Linux/Docker:
- Event loop issue doesn't exist on Linux
- Can use standard `uvicorn api.main:app` command
- PostgreSQL recommended for multi-user deployments

## Architecture

```
┌─────────────────────────────────────────┐
│     FastAPI (api/main.py)               │
│  - WindowsSelectorEventLoop (Windows)   │
│  - Manages PostgreSQL connection        │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│   LangGraph AsyncPostgresSaver          │
│  - Uses psycopg (async driver)          │
│  - Creates tables via SQLAlchemy        │
│     - checkpoints                       │
│     - checkpoint_writes                 │
│     - checkpoint_metadata               │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│    PostgreSQL Database                  │
│    localhost:5432/sap_discovery         │
│  - Stores conversation history          │
│  - Persists agent state                 │
└─────────────────────────────────────────┘
```

## Summary

✅ **Code Fixed**:
- Connection lifecycle properly managed
- Windows event loop policy set
- Cleanup on shutdown added

✅ **Startup Script**:
- `start_api.py` handles event loop correctly

✅ **Two Options**:
1. **PostgreSQL** (production-ready, requires `python start_api.py`)
2. **SQLite** (simpler, works with standard uvicorn)

Choose based on your needs:
- **Development**: SQLite (easier)
- **Production/Multi-user**: PostgreSQL (better)

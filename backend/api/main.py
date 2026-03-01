from dotenv import load_dotenv
load_dotenv()

import os
import uuid
import json
from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from api.models import ChatResponse
from sap_discovery.tools.registry import get_all_tools
from sap_discovery.llm.models import create_llm_instances
from sap_discovery.workflow.graph import compile_workflow
from sap_discovery.main_agent.tools import set_workflow_graph, update_processes
from sap_discovery.main_agent.agent import create_main_agent
from sap_discovery.main_agent.chat import chat as chat_fn
from sap_discovery.utils.logging import setup_logger
from sap_discovery.utils.storage import save_file, validate_excel, parse_excel_processes
from api.middleware import SessionMiddleware

logger = setup_logger(__name__)
LANGGRAPH_DATABASE_URL = os.getenv("LANGGRAPH_DATABASE_URL")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize agent on startup, cleanup on shutdown."""

    logger.info("=" * 60)
    logger.info("SAP Process Discovery API - Starting...")
    logger.info("=" * 60)

    # Store chat function in app state
    app.state.chat_fn = chat_fn

    # 1. Initialize tools
    logger.info("[1/4] Initializing tools (MCP client)...")
    tools = await get_all_tools()
    logger.info(f"[1/4] Loaded {len(tools)} tools: {[t.name for t in tools]}")

    # 2. Create LLM instances
    logger.info("[2/4] Creating LLM instances...")
    llm_instances = create_llm_instances(tools)
    logger.info("[2/4] LLM instances created")

    # 3. Compile workflow
    logger.info("[3/4] Compiling workflow graph...")
    graph = compile_workflow(llm_instances, tools)
    set_workflow_graph(graph)
    logger.info("[3/4] Workflow compiled and graph set")

    # 4. Create main agent with persistent PostgreSQL memory
    logger.info("[4/4] Creating main agent...")
    memory_context = AsyncPostgresSaver.from_conn_string(LANGGRAPH_DATABASE_URL)
    memory = await memory_context.__aenter__()
    await memory.setup()

    app.state.memory = memory
    app.state.memory_context = memory_context

    agent = await create_main_agent(memory)
    app.state.agent = agent
    logger.info("[4/4] Main agent created")

    logger.info("=" * 60)
    logger.info("API Ready! Agent initialized successfully.")
    logger.info("=" * 60)

    yield

    # Shutdown
    logger.info("Shutting down API...")
    if hasattr(app.state, 'memory_context'):
        await app.state.memory_context.__aexit__(None, None, None)
        logger.info("PostgreSQL connection closed")


app = FastAPI(
    title="SAP Process Discovery API",
    description="Chat-based SAP business process discovery agent",
    version="0.1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware)


@app.get("/")
async def root():
    return {
        "name": "SAP Process Discovery API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "agent": app.state.agent is not None,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: Request,
    message: str = Form(...),
    file: UploadFile = File(None)
):
    """Chat with the SAP Process Discovery agent."""
    session_id = request.state.session_id

    try:
        agent = app.state.agent
        chat_fn = app.state.chat_fn

        full_message = message
        if file and file.filename:
            if not validate_excel(file.filename):
                raise HTTPException(
                    status_code=400,
                    detail="Only Excel files (.xlsx, .xls) are supported"
                )

            file_path = await save_file(file, session_id)
            logger.info(f"File uploaded: {file_path}")

            try:
                processes = parse_excel_processes(file_path)

                # Generate unique job_id for this upload
                job_id = str(uuid.uuid4())

                # Store processes under job_id, tracked by session_id
                update_processes(session_id, job_id, processes)
                logger.info(f"Session {session_id[:8]}: Job {job_id[:8]}: Stored {len(processes)} processes")

                full_message = f"""{message}

I've uploaded an Excel file with {len(processes)} business processes.
Job ID: {job_id}
Please run SAP discovery on this job."""

            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))
            except Exception as e:
                logger.error(f"Unexpected error parsing Excel: {e}")
                raise HTTPException(status_code=500, detail="Internal error processing Excel file")

        config = {
            'configurable': {
                'thread_id': session_id,
                'session_id': session_id
            }
        }

        response = await chat_fn(agent, full_message, config)
        return ChatResponse(response=response)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat error for session {session_id[:8]}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        loop="asyncio"
    )
"""Startup script for SAP Discovery API with Windows compatibility."""

import sys
import asyncio

# CRITICAL: Set event loop policy and create event loop BEFORE importing anything
# psycopg requires WindowsSelectorEventLoopPolicy on Windows
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    print("[OK] Set WindowsSelectorEventLoopPolicy for psycopg compatibility")

# Create and set the event loop explicitly
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
print(f"[OK] Created new event loop: {type(loop).__name__}")

# Now import and run uvicorn
import uvicorn

if __name__ == "__main__":
    config = uvicorn.Config(
        "api.main:app",
        host="0.0.0.0",
        port=8001,
        reload=False,
        loop="none"  # Don't let uvicorn create its own loop
    )
    server = uvicorn.Server(config)

    # Run using our pre-configured event loop
    loop.run_until_complete(server.serve())

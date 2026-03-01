"""Run database migrations."""

import os
import asyncio
import sys
from dotenv import load_dotenv
import psycopg

# Set event loop policy for Windows
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

async def run_migration():
    """Run the session_results table migration."""
    with open("migrations/001_create_session_results.sql", "r") as f:
        migration_sql = f.read()

    try:
        async with await psycopg.AsyncConnection.connect(DATABASE_URL) as conn:
            async with conn.cursor() as cur:
                await cur.execute(migration_sql)
                await conn.commit()
        print("[OK] Migration completed successfully!")
        print("     Created session_results table with indexes")
    except Exception as e:
        print(f"[ERROR] Migration failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(run_migration())

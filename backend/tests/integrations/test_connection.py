import asyncio
import pytest
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.sql import text

DATABASE_URL = "postgresql+asyncpg://chatdocuser:PassWord123@localhost:5432/chatdocdb"
# DATABASE_URL = "postgresql+asyncpg://chatdocuser:PassWord123@172.20.0.11:5432/chatdocdb"

@pytest.mark.asyncio
async def test_connection():
    engine = create_async_engine(DATABASE_URL, echo=True)
    try:
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT 1"))
            row = result.fetchone()
            assert row is not None, "Database query returned no rows"
            print(f"Query result: {row}")
    finally:
        await engine.dispose()

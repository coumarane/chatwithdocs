import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.sql import text

DATABASE_URL = "postgresql+asyncpg://chatdocuser:PassWord123@localhost:5432/chatdocdb"

async def test_connection():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        result = await conn.execute(text("SELECT 1"))  # Wrap query in text()
        print(result.fetchone())

asyncio.run(test_connection())

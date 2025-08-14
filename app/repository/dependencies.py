from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.app import app


async def get_db() -> AsyncSession:
    async with app.db.session() as session:
        yield session
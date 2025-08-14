import logging

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from sqlalchemy.sql import text

from app.repository.base import Base


class Database:
    def __init__(self):
        self.engine = None
        self.session_factory = None
        self.Base = Base 
        self.metadata = self.Base.metadata
        self.logger = logging.getLogger("Database")

    async def connect(self, db_url: str):
        self.engine = create_async_engine(
            url=db_url,
            echo=True
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        

        async with self.engine.begin() as conn:
            await conn.run_sync(self.metadata.create_all)
            self.logger.info("Database tables created")

        async with self.session() as session:
            await session.execute(text("SELECT 1"))
            self.logger.info("Database connected successfully")


    async def disconnect(self):
        if self.engine:
            self.logger.info("Database Disconnected")
            await self.engine.dispose()
    
    def session(self):
        if not self.session_factory:
            raise RuntimeError("Database is not connected")
        return self.session_factory()

import os

from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine
from sqlalchemy.orm import sessionmaker

from resource import Database, Oss, BaseTask


class PostgresConsumer:
    def __init__(self,is_production):
        user = os.environ["POSTGRES_USER"]
        password = os.environ["POSTGRES_PASSWORD"]
        host = os.environ["POSTGRES_HOST"]
        port = os.environ["POSTGRES_PORT"]
        database = os.environ["POSTGRES_DB"]
        self.url = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"
        self.engine = create_async_engine(
            self.url,
            echo=not is_production,
            pool_pre_ping=True
        )
        self.async_session_maker = sessionmaker(self.engine,class_=AsyncSession,expire_on_commit=False)

    async def close_engine(self):
        await self.engine.dispose()

    async def get_task(self,task_id):
        async with self.async_session_maker as session:
            task = await session.get(BaseTask,task_id)
            return task

    async def get_database(self,database_id):
        async with self.async_session_maker as session:
            database = await session.get(Database,database_id)
            return database

    async def get_oss(self,oss_id):
        async with self.async_session_maker as session:
            oss = await session.get(Oss,oss_id)
            return oss
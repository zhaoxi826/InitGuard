from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import select

from resource import User, BaseTask, Database, Oss
from utils import PasswordHelper
import os

class PostgresApi:
    def __init__(self, is_production):
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
        self.async_session_maker = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)

    async def close_engine(self):
        await self.engine.dispose()

    async def add_user(self,user_name,user_password,user_email):
        async with self.async_session_maker() as session:
            hashed_pwd = PasswordHelper.hash_password(user_password)
            user = User(user_name=user_name,user_password=hashed_pwd,user_email=user_email)
            session.add(user)
            await session.commit()

    async def login_user(self,user_name,user_password):
        async with self.async_session_maker() as session:
            statement = select(User).where(User.user_name == user_name)
            result = await session.execute(statement)
            user = result.scalars().first()
            if user and PasswordHelper.verify_password(user_password,user.user_password):
                return user.user_id
            return False

    async def add_task(self,task_name,database_id,oss_id,task_type,owner_id,database_name):
        async with self.async_session_maker() as session:
            task_set={"backup_task"}
            if task_type not in task_set:
                raise ValueError(f"不支持的任务类型: {task_type}")
            task = BaseTask(
                task_name=task_name,
                database_id=database_id,
                oss_id=oss_id,
                owner_id=owner_id,
                database_name=database_name,
                task_type=task_type
            )
            session.add(task)
            await session.commit()
            await session.refresh(task)
            return task.task_id

    async def get_task(self,task_id):
        async with self.async_session_maker() as session:
            task = await session.get(BaseTask,task_id)
            return task

    async def add_instance(self,instance):
        async with self.async_session_maker() as session:
            session.add(instance)
            await session.commit()

    async def get_databases(self, owner_id: int):
        async with self.async_session_maker() as session:
            query = select(Database)
            if owner_id != 1:
                query = query.where(Database.owner_id == owner_id)
            result = await session.execute(query)
            return result.scalars().all()

    async def get_oss(self, owner_id: int):
        async with self.async_session_maker() as session:
            query = select(Oss)
            if owner_id != 1:
                query = query.where(Oss.owner_id == owner_id)
            result = await session.execute(query)
            return result.scalars().all()

    async def get_tasks(self, user_id: int, database_id: int | None = None, status: str | None = None,
                        start_time: str | None = None, task_type: str | None = None):
        async with self.async_session_maker() as session:
            query = select(BaseTask)
            if user_id != 1:  # Assuming user_id 1 is superuser
                query = query.where(BaseTask.owner_id == user_id)
            if database_id:
                query = query.where(BaseTask.database_id == database_id)
            if status:
                query = query.where(BaseTask.task_status == status)
            if start_time:
                # Assuming start_time is a string suitable for comparison or convert it
                # For simplicity, let's assume strict equality or handle it as needed.
                # If start_time is a date string, we might want >= start_time.
                # However, without knowing the exact format, I'll use equality for now or >.
                # Let's assume start_time means tasks created after this time.
                from datetime import datetime
                try:
                    dt = datetime.fromisoformat(start_time)
                    query = query.where(BaseTask.create_time >= dt)
                except ValueError:
                    pass # Ignore invalid date format
            if task_type:
                query = query.where(BaseTask.task_type == task_type)

            result = await session.execute(query)
            return result.scalars().all()
from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import select

from resource import User, BaseTask
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
        async with self.async_session_maker as session:
            hashed_pwd = PasswordHelper.hash_password(user_password)
            user = User(user_name=user_name,user_password=hashed_pwd,user_email=user_email)
            session.add(user)
            await session.commit()

    async def login_user(self,user_name,user_password):
        async with self.async_session_maker as session:
            statement = select(User).where(User.user_name == user_name)
            user = await session.exec(statement).first()
            if user and PasswordHelper.verify_password(user_password,user.user_password):
                return user.user_id
            return False

    async def add_task(self,task_name,database_id,oss_id,task_type,owner_id,database_name):
        async with self.async_session_maker as session:
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
        async with self.async_session_maker as session:
            task = await session.get(BaseTask,task_id)
            return task

    async def add_instance(self,instance):
        async with self.async_session_maker as session:
            session.add(instance)
            await session.commit()
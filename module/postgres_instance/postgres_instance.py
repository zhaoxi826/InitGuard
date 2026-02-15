import os
from resource import User,BaseTask,Database,Oss
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from utils import PasswordHelper


class PostgresInstance:
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
        self.async_session_maker = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)

    # 4. 数据库初始化方法改为异步
    async def init(self):
        async with self.engine.begin() as conn:
            # SQLModel 的元数据同步操作需要通过 run_sync 运行
            await conn.run_sync(SQLModel.metadata.create_all)

    def get_engine(self):
        return self.engine

    # 5. 关闭方法改为异步
    async def close_engine(self):
        await self.engine.dispose()

    async def create_superuser(self):
        async with self.async_session_maker() as session:
            superuser = await session.get(User,1)
            if not superuser:
                hashed_pwd = PasswordHelper.hash_password(os.environ.get("SUPERUSER_PASSWORD"))
                superuser = User(user_id=1, user_name=os.environ.get("SUPERUSER_NAME"),user_email=os.environ.get("SUPERUSER_EMAIL"),user_password=hashed_pwd,user_authority="superuser")
                session.add(superuser)
                await session.commit()
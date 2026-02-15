import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
import os

# Set dummy env vars for imports to work if they access os.environ at module level
os.environ["POSTGRES_USER"] = "user"
os.environ["POSTGRES_PASSWORD"] = "password"
os.environ["POSTGRES_HOST"] = "localhost"
os.environ["POSTGRES_PORT"] = "5432"
os.environ["POSTGRES_DB"] = "db"
os.environ["REDIS_HOST"] = "localhost"
os.environ["REDIS_PORT"] = "6379"
os.environ["REDIS_PASSWORD"] = "password"
os.environ["SECRET_KEY"] = "secret"

from fastapi import FastAPI, Depends
from module.webapi.auth_api import router as auth_router
from module.webapi.resource_api import router as resource_router
from module.webapi.task_api import router as task_router
from module.postgres_instance.postgres_api import PostgresApi
from module.redis_instance.redis_api import RedisApi
from module.webapi.dependence import dependence_pg, dependence_redis

# Mock PostgresApi using SQLite
class MockPostgres(PostgresApi):
    def __init__(self, is_production=False):
        # Override to use SQLite
        self.engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
        self.async_session_maker = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)

    async def init_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    async def close_engine(self):
        await self.engine.dispose()

# Mock RedisApi
class MockRedis:
    def __init__(self):
        self.tokens = {}
        self.tasks = []

    async def login_token(self, token, user_id):
        self.tokens[user_id] = token

    async def get_token(self, user_id):
        return self.tokens.get(user_id)

    async def add_task(self, task_id):
        self.tasks.append(task_id)

    async def close_redis(self):
        pass

@pytest_asyncio.fixture
async def app_instance():
    app = FastAPI()
    app.include_router(auth_router)
    app.include_router(resource_router)
    app.include_router(task_router)

    mock_pg = MockPostgres()
    await mock_pg.init_db()
    mock_redis = MockRedis()

    app.state.pg_instance = mock_pg
    app.state.redis_instance = mock_redis

    # Create superuser
    from resource import User
    from utils.security import PasswordHelper # Fix import
    # PasswordHelper is in utils.security in the file read earlier?
    # No, read_file of utils/security.py showed: class PasswordHelper...
    # But read_file of module/postgres_instance/postgres_instance.py imported utils.PasswordHelper
    # Let's check imports in utils/__init__.py

    async with mock_pg.async_session_maker() as session:
        # We need to hash password
        # Assuming PasswordHelper is available via utils
        from utils import PasswordHelper
        hashed_pwd = PasswordHelper.hash_password("admin")
        user = User(user_id=1, user_name="admin", user_email="admin@example.com", user_password=hashed_pwd, user_authority="superuser")
        session.add(user)
        await session.commit()

    yield app

    await mock_pg.close_engine()

@pytest_asyncio.fixture
async def client(app_instance):
    async with AsyncClient(transport=ASGITransport(app=app_instance), base_url="http://test") as ac:
        yield ac

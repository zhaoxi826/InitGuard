import tomllib

from module.postgres_instance.postgres_api import PostgresApi
from contextlib import asynccontextmanager
from fastapi import FastAPI
import asyncio

from module.redis_instance.redis_api import RedisApi


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("InitGuard 正在启动...")
    try:
        with open('pyproject.toml', 'rb') as f:
            config = tomllib.load(f)
            is_production = ("true" == config.get("project", {}).get("is_production", "false"))
    except FileNotFoundError:
        is_production = False
    postgres_instance = PostgresApi(is_production)
    redis_instance = RedisApi()
    app.state.pg_engine = postgres_instance
    app.state.redis_instance = redis_instance
    yield
    # --- 【关闭】 ---
    print("web组件 正在优雅地关闭...")
    await asyncio.gather(
        postgres_instance.close_engine(),
        redis_instance.close_redis()
    )




from module import PostgresInstance,RedisInstance
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("InitGuard 正在启动...")
    postgres_instance = PostgresInstance()
    redis_instance = RedisInstance()
    app.state.pg_instance = postgres_instance
    app.state.redis_instance = redis_instance
    postgres_instance.init_superuser()
    yield
    # --- 【关闭】 ---
    print("web组件 正在优雅地关闭...")
    postgres_instance.close_engine()



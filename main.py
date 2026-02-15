from resource import User,Database,Oss,BaseTask
import uvicorn
import tomllib
import asyncio
from fastapi import FastAPI
from module import PostgresInstance, Consumer
from module.webapi.auth_api import router as auth_router
from module.webapi.resource_api import router as resource_router
from module.webapi.task_api import router as task_router
from module.webapi.lifespan import lifespan
import multiprocessing

def run_api():
    app = FastAPI(lifespan=lifespan())
    app.include_router(auth_router)
    app.include_router(resource_router)
    app.include_router(task_router)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")

def run_consumer(is_production):
    consumer = Consumer(is_production)
    asyncio.run(consumer.run())

def main():
    # 1. 读取配置 (纯展示用)
    try:
        with open('pyproject.toml', 'rb') as f:
            config = tomllib.load(f)
            version = config.get("project", {}).get("version", "0.1.0")
            is_production = ("true" == config.get("project", {}).get("is_production", "false"))
    except FileNotFoundError:
        version = "Unknown"
    print(f"Initguard数据备份系统 v{version} 正在初始化...")

    # 2. 初始化数据库表结构
    print(">>> 正在检查并初始化数据库表结构...")
    temp_pg = PostgresInstance(is_production)
    asyncio.run(temp_pg.init())
    asyncio.run(temp_pg.create_superuser())
    asyncio.run(temp_pg.close_engine())
    print(">>> 数据库表结构初始化完成。")

    #3. 拉起consumer进程和fastapi进程
    api_process = multiprocessing.Process(target=run_api)
    worker_process = multiprocessing.Process(target=run_consumer, args=(is_production,))

    api_process.start()
    worker_process.start()

    api_process.join()
    worker_process.join()

if __name__ == '__main__':
    main()
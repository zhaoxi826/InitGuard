from resource import User,Database,Oss,BaseTask
import uvicorn
import threading
import tomllib
from fastapi import FastAPI
from contextlib import asynccontextmanager
from module import PostgresInstance, RedisInstance, Consumer
from module.webapi.auth_api import router as auth_router
from module.webapi.resource_api import router as resource_router
from module.webapi.task_api import router as task_router
from module.webapi.lifespan import lifespan

def run_consumer_worker():
    print(">>> 启动后台任务消费者线程...")
    try:
        pg_instance = PostgresInstance()
        redis_instance = RedisInstance()
        consumer = Consumer(redis_instance, pg_instance)
        consumer.start()
    except Exception as e:
        print(f"!!! 消费者线程崩溃: {e}")


def main():
    # 1. 读取配置 (纯展示用)
    try:
        with open('pyproject.toml', 'rb') as f:
            config = tomllib.load(f)
            version = config.get("project", {}).get("version", "0.1.0")
    except FileNotFoundError:
        version = "Unknown"
    print(f"Initguard数据备份系统 v{version} 正在初始化...")

    # 2. 初始化数据库表结构
    print(">>> 正在检查并初始化数据库表结构...")
    temp_pg = PostgresInstance()
    temp_pg.init()
    temp_pg.close_engine()
    print(">>> 数据库表结构初始化完成。")

    app = FastAPI(
        title="InitGuard API",
        version=version,
        lifespan=lifespan
    )
    # 4. 注册路由 (这一步非常重要，否则 API 无法访问)
    app.include_router(auth_router)
    app.include_router(resource_router)
    app.include_router(task_router)
    # 5. 启动消费者线程 (Daemon=True 表示主程序退出时它也会自动退出)
    consumer_thread = threading.Thread(target=run_consumer_worker, daemon=True)
    consumer_thread.start()
    # 6. 启动 Web 服务器
    print(f">>> Web 服务启动在 http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

if __name__ == '__main__':
    main()
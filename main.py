import tomllib
from module import PostgresInstance,RedisInstance,Consumer
from fastapi import FastAPI

def main():
    # 读取配置变量
    with open('pyproject.toml', 'r') as f:
        config = tomllib.load(f)
    print("kubeguard数据备份系统，版本号{{}}。".format(config["project"]["version"]))
    #实例化对象
    print("正在初始化中......请稍后")
    postgres_instance = PostgresInstance()  #实例化自动化系统数据库
    redis_instance = RedisInstance()  #实例化自动化系统redis
    fastapi_postgres_instance = PostgresInstance() #实例化web程序数据库
    fastapi_redis_instance = RedisInstance() #实例化web程序redis
    consumer = Consumer(redis_instance,postgres_instance) #实例化consumer模块
    app = FastAPI()
    app.state.pg_instance = fastapi_postgres_instance
    app.state.redis_instance = fastapi_redis_instance

if __name__ == '__main__':
    main()
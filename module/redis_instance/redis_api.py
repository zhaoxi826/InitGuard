import redis.asyncio as redis
import os

class RedisApi:
    def __init__(self):
        host = os.environ['REDIS_HOST']
        port = os.environ['REDIS_PORT']
        password = os.environ['REDIS_PASSWORD']
        self.r = redis.Redis(host=host, port=port,password=password, decode_responses=True)

    async def login_token(self,token,user_id):
        key = f"initguard:auth:user:{user_id}"
        await self.r.set(key, token, ex=3600)

    async def get_token(self,user_id):
        stored_token = await self.r.get(f"initguard:auth:user:{user_id}")
        if not stored_token:
            return False
        return stored_token

    async def add_task(self,task_id):
        await self.r.lpush("initguard:task:task_queue",task_id)

    async def close_redis(self):
        await self.r.close()
import redis.asyncio as redis
import os

class RedisConsumer:
    def __init__(self):
        host = os.environ['REDIS_HOST']
        port = os.environ['REDIS_PORT']
        password = os.environ['REDIS_PASSWORD']
        self.r = redis.Redis(host=host, port=port,password=password, decode_responses=True)

    async def get_task(self):
        result = await self.r.brpop("initguard:task:task_queue",timeout=0)
        return result[1] if result else None

    async def close_redis(self):
        await self.r.close()
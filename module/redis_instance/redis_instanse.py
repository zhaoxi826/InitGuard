import redis
import os

class RedisInstance:
    def __init__(self):
        host = os.environ['REDIS_HOST']
        port = os.environ['REDIS_PORT']
        password = os.environ['REDIS_PASSWORD']
        self.r = redis.Redis(host=host, port=port,password=password, decode_responses=True)

    # 调度器方法
    def push_task(self,task_id):
        self.r.lpush("initguard:task:task_queue",task_id)

    def get_task(self):
        result = self.r.brpop("initguard:task:task_queue",timeout=0)
        return result[1] if result else None

    #fastapi方法
    def login_token(self,token,user_id):
        key = f"initguard:auth:user:{user_id}"
        self.r.set(key, token, ex=3600)

    def get_token(self,user_id):
        stored_token = self.r.get(f"kg:auth:user:{user_id}")
        if not stored_token:
            return False
        return stored_token

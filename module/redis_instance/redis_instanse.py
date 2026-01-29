import redis
class RedisInstance:
    def __init__(self,host,port):
        self.r = redis.Redis(host=host, port=port, decode_responses=True)

    def push_task(self,task_id):
        self.r.lpush("initguard:task:task_queue",task_id)

    def get_task(self):
        result = self.r.brpop("initguard:task:task_queue",timeout=0)
        return result[1] if result else None

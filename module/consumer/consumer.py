from module.redis_instance.redis_consumer import RedisConsumer
from module.postgres_instance.postgres_consumer import PostgresConsumer
from resource.task.backup_task import BackupTaskProcess
import datetime
import asyncio

class Consumer:
    def __init__(self,is_production):
        self.redis_instance = RedisConsumer()
        self.postgres_instance = PostgresConsumer(is_production)

    async def run(self):
        task_id = await self.redis_instance.get_task()
        if task_id:
            task_instance = await self.postgres_instance.get_task(task_id)
            match task_instance.task_type:
                case "backup_task":
                    database_instance, oss_instance = asyncio.gather(
                    self.postgres_instance.get_database(task_instance.database_id),
                    self.postgres_instance.get_oss(task_instance.oss_id))
                    target_path = "/backup/{}/{}.sql".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S"),task_id)
                    await BackupTaskProcess(task_instance,database_instance,oss_instance,target_path).run()
                case _:
                    print(f"收到未知任务类型: {type(task_instance)}")

    async def start(self):
        print("任务调度器开始工作了")
        while True:
            try:
                asyncio.create_task(self.run())
                await asyncio.sleep(5)
            except Exception as e:
                print(f"消费循环出错了: {e}")
                await asyncio.sleep(15)
        await asyncio.gather(self.postgres_instance.close_engine(),self.redis_instance.close_redis())
        return

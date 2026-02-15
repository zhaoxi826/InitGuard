from module.redis_instance.redis_consumer import RedisConsumer
from module.postgres_instance.postgres_consumer import PostgresConsumer
from resource.task.backup_task import BackupTaskProcess
import datetime
import asyncio

class Consumer:
    def __init__(self, is_production):
        self.redis_instance = RedisConsumer()
        self.postgres_instance = PostgresConsumer(is_production)

    async def _process_task(self, task_id):
        try:
            task_instance = await self.postgres_instance.get_task(task_id)
            if not task_instance:
                print(f"未找到任务: {task_id}")
                return

            match task_instance.task_type:
                case "backup_task":
                    database_instance, oss_instance = await asyncio.gather(
                        self.postgres_instance.get_database(task_instance.database_id),
                        self.postgres_instance.get_oss(task_instance.oss_id)
                    )

                    if not database_instance or not oss_instance:
                        print(f"任务 {task_id} 缺少数据库或OSS配置")
                        return

                    target_path = "/backup/{}/{}.sql".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S"), task_id)
                    await BackupTaskProcess(task_instance, database_instance, oss_instance, target_path).run()
                case _:
                    print(f"收到未知任务类型: {task_instance.task_type}")
        except Exception as e:
            print(f"处理任务 {task_id} 时发生错误: {e}")
            import traceback
            traceback.print_exc()

    async def run(self):
        print("任务调度器开始工作了")
        try:
            while True:
                try:
                    task_id = await self.redis_instance.get_task()
                    if task_id:
                        await self._process_task(task_id)
                except Exception as e:
                    print(f"消费循环出错了: {e}")
                    await asyncio.sleep(5)
        finally:
            print("正在关闭消费者资源...")
            await asyncio.gather(
                self.postgres_instance.close_engine(),
                self.redis_instance.close_redis()
            )
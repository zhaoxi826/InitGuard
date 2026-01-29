from module import PostgresInstance,RedisInstance
from resource import BackupTask,BackupTaskProcess
import datetime
import time

class Consumer:
    def __init__(self,redis_instance:RedisInstance,postgre_instance:PostgresInstance):
        self.redis_instanse = redis_instance
        self.postgre_instance = postgre_instance

    def run(self):
        task_id = self.redis_instanse.get_task()
        if task_id:
            task_instance = self.postgre_instance.get_task(task_id)
            match task_instance:
                case BackupTask():
                    database_instance = self.postgre_instance.get_database(task_instance.database_id)
                    oss_instance = self.postgre_instance.get_oss(task_instance.oss_id)
                    target_path = "/backup/{}/{}.sql".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S"),task_id)
                    BackupTaskProcess(task_instance,database_instance,oss_instance,target_path).run()
                case _:
                    print(f"收到未知任务类型: {type(task_instance)}")

    def start(self):
        print("任务调度器开始工作了")
        while True:
            try:
                self.run()
            except Exception as e:
                print(f"消费循环出错了: {e}")
                time.sleep(5)



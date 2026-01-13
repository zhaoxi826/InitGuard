import datetime
from .task_model import Task
from module import Oss,Database,TaskLogger
import time

class SaveTask(Task):
    def __init__(self,oss:Oss,db:Database,type,task_id):
        super().__init__()
        self.name = "save_task"
        self.task_id = task_id
        self.oss = oss
        self.db = db
        self.type = type
        self.logger = TaskLogger(self.task_id,self.name)
        self.target_path = None

    def create_task(self):
        print("保存任务创建中")
        self.state = "PENDING"
        self.target_path = ("{}_{}_备份任务").format(datetime.datetime.now().strftime("%Y%m%d%H%M%S"),self.type)
        self.create_time = datetime.datetime.now()
        self.update_time = datetime.datetime.now()
        print("任务创建完成")

    def restart(self):
        self.state = "FAILED"
        self.update_time = datetime.datetime.now()
        self.restart_times += 1
        self.restart_time += 300
        time.sleep(self.restart_time)

    def work(self):
        self.state = "RUNNING"
        self.logger.log("INFO", "开始备份...")
        db_process,stream,stderr = self.db.get_dump_stream()
        try:
            self.oss.upload_stream(stream,self.target_path)
            db_process.wait()
            if db_process.returncode == 0:
                print("备份并上传成功！")
            else:
                print("数据库备份过程出错。")
                err_info = stderr.read().decode()
                raise Exception(f"数据库备份进程异常退出，状态码: {db_process.returncode}, 原因: {err_info}")
            self.logger.log("INFO", "上传成功")
        except Exception as e:
            db_process.terminate()
            self.logger.log("ERROR", f"备份失败: {str(e)}")
            raise e
        finally:
            self.logger.save()
            stream.close()

    def run(self):
        self.create_task()
        while self.restart_times <= 3:
            try:
                self.work()
                break
            except Exception as e:
                self.error = e
                if self.restart_times == 3:
                    break
                self.restart()
                self.logger.log("WARNING","任务{}:{}出现问题.错误：{}，正在准备第{}次重试".format(self.task_id,self.name,e,self.restart_times+1))

        if self.restart_times == 3:
            self.state = "FAILED"
            self.logger.log("ERROR","任务{}:{}重启失败，错误：{},已结束任务".format(self.task_id,self.name,self.error))
        else:
            self.state = "SUCCESS"
            self.logger.log("INFO","任务{}:{}成功！".format(self.task_id,self.name))
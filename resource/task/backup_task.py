from pydantic import BaseModel
from .task_model import TaskProcess,BaseTask
from resource.object_module import Oss,Database
from sqlmodel import Field,JSON
import datetime
from typing import Dict, Any
from loguru import logger

class BackupTask(BaseTask):
    __mapper_args__ = {
        "polymorphic_identity": "backup",
    }

class BackupTaskProcess(TaskProcess):
    def __init__(self,task:BackupTask,database:Database,oss:Oss,target_path:str=None):
        self.task = task
        self.database = database
        self.oss = oss
        self.target_path = target_path

    def work(self,task_logger):
        task_logger.info( "开始备份...")
        db_process, stream, stderr = self.database.get_dump_stream()
        try:
            self.oss.upload_stream(stream, self.target_path)
            db_process.wait()
            if db_process.returncode == 0:
                print("备份并上传成功！")
            else:
                print("数据库备份过程出错。")
                err_info = stderr.read().decode()
                raise Exception(f"数据库备份进程异常退出，状态码: {db_process.returncode}, 原因: {err_info}")
            task_logger.info("上传成功")
        except Exception as e:
            db_process.terminate()
            task_logger.error( f"备份失败: {str(e)}")
            raise e
        finally:
            stream.close()

    def run(self):

        log_file = f"logs/task_{self.task.task_id}.log"
        handler_id = logger.add(
            log_file,
            filter=lambda record: record["extra"].get("task_id") == self.task.task_id
        )
        task_logger = logger.bind(task_id=self.task.task_id)
        task_logger.info(f"--- 任务 {self.task.task_id} 开始执行 ---")
        self.task.task_status = "RUNNING"
        self.task.update_time = datetime.datetime.now()
        try:
            self.work(task_logger)
            self.task.task_status = "FINISHED"
        except Exception as e:
            self.task.task_status = "ERROR"
            task_logger.exception("任务执行崩溃")
        finally:
            task_logger.info(f"--- 任务 {self.task.task_id} 结束 ---")
            logger.remove(handler_id)
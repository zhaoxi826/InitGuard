from abc import ABC, abstractmethod
from sqlmodel import SQLModel, Field,JSON
import datetime
from typing import Dict, Any

class BaseTask(SQLModel,Table=True):
    __tablename__ = "tasks_list"
    task_id: int | None = Field(default=None, primary_key=True)
    task_name: str = Field(default="backup_task")
    task_status: str = Field(default="Pending")
    create_time: datetime.datetime = Field(default=datetime.datetime.now())
    update_time: datetime.datetime | None = Field(default=None)
    database_id: int | None = Field(default=None)
    oss_id: int | None = Field(default=None)
    logs: Dict[str, Any] = Field(default_factory=dict, sa_type=JSON)
    task_type: str = Field(sa_column_kwargs={"index": True})
    __mapper_args__ = {
        "polymorphic_on": "task_type",
    }

class TaskProcess(ABC):
    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def work(self,task_logger):
        pass

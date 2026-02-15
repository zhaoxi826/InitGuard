import datetime
from abc import ABC, abstractmethod

from sqlmodel import SQLModel, Field


class BaseTask(SQLModel,table=True):
    __tablename__ = "task_list"
    task_id: int | None = Field(default=None, primary_key=True)
    task_name: str = Field(default="default_task")
    task_status: str = Field(default="Pending")
    owner_id: int = Field(default=1,index=True)
    create_time: datetime.datetime = Field(default_factory=datetime.datetime.now)
    update_time: datetime.datetime | None = Field(default=None)
    database_id: int | None = Field(default=None)
    database_name: str
    oss_id: int | None = Field(default=None)
    task_type: str | None = Field(default=None)

class TaskProcess(ABC):
    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def work(self,task_logger):
        pass

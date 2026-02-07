from abc import ABC, abstractmethod
from sqlmodel import SQLModel, Field
import datetime


class BaseTask(SQLModel,table=True):
    __tablename__ = "tasks_list"
    task_id: int | None = Field(default=None, primary_key=True)
    task_name: str = Field(default="default_task")
    task_status: str = Field(default="Pending")
    owner_id: int = Field(default=1,index=True)
    create_time: datetime.datetime = Field(default_factory=datetime.datetime.now)
    update_time: datetime.datetime | None = Field(default=None)
    database_id: int | None = Field(default=None)
    database_name: str
    oss_id: int | None = Field(default=None)
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

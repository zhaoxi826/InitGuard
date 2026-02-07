from sqlmodel import SQLModel,Field
from abc import ABC, abstractmethod

class Database(SQLModel, table=True):
    __tablename__ = "database_list"
    database_id: int | None = Field(default=None, primary_key=True)
    owner_id : int
    database_name: str | None = Field(default=None)
    host: str = Field(default="localhost")
    port: int = Field(default=5432, ge=1, le=65535)
    username: str
    password: str
    database_type: str
    __mapper_args__ = {
        "polymorphic_on": "database_type",
    }

class DatabaseMethod(ABC):
    @abstractmethod
    def get_dump_stream(self):
        pass

    @abstractmethod
    def database_restore(self):
        pass
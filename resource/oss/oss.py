from abc import ABC, abstractmethod
from sqlmodel import SQLModel, Field
from typing import Literal


class Oss(SQLModel,table=True):
    __tablename__ = "oss_list"
    oss_id: int | None =Field(default=None, primary_key=True)
    owner_id : int
    oss_name: str = Field(default=None)
    endpoint: str
    bucket: str
    access_key: str
    secret_key: str
    oss_type: str

class OssMethod(ABC):
    @abstractmethod
    def download_stream(self):
        pass

    @abstractmethod
    def upload_stream(self,stream,path):
        pass
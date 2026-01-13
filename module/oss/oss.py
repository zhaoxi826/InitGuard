import os
from abc import ABC, abstractmethod
class Oss(ABC):
    def __init__(self):
        self.endpoint = os.environ.get("OSS_ENDPOINT")
        self.bucket = os.environ.get("OSS_BUCKET")
        self.access_key = os.environ.get("OSS_ACCESS_KEY")
        self.secret_key = os.environ.get("OSS_SECRET_KEY")

    @abstractmethod
    def download_stream(self):
        pass

    @abstractmethod
    def upload_stream(self,stream,path):
        pass
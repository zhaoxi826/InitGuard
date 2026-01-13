import os
from abc import ABC, abstractmethod
class Database(ABC):
    def __init__(self):
        self.host = os.environ.get('DB_HOST')
        self.port = os.environ.get('DB_PORT')
        self.db_user = os.environ.get('DB_USER')
        self.db_name = os.environ.get('DB_NAME')
        self.password = os.environ.get('DB_PASSWORD')

    @abstractmethod
    def get_dump_stream(self):
        pass

    @abstractmethod
    def database_restore(self):
        pass
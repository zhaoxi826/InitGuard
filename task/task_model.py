from abc import ABC, abstractmethod

class Task(ABC):
    def __init__(self):
        self.name = None
        self.task_id = None
        self.state = None
        self.create_time = None
        self.update_time = None
        self.restart_time = 0
        self.restart_times = 0
        self.error = None


    @abstractmethod
    def create_task(self):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def restart(self):
        pass

    @abstractmethod
    def work(self):
        pass

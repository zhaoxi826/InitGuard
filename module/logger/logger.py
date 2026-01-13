import json
import os
import datetime

class TaskLogger:
    def __init__(self,task_id,task_name):
        self.task_id = task_id
        self.task_name = task_name
        self.create_time = datetime.datetime.now().isoformat()
        self.records = []
        date_str = datetime.datetime.now().strftime("%Y%m%d")
        self.file_path = f"logs/{date_str}_{self.task_id}.json"
        os.makedirs("logs", exist_ok=True)

    def log(self, level, message):
        record = {
            "time": datetime.datetime.now().isoformat(),
            "level": level,
            "msg": message
        }
        self.records.append(record)
        print(f"[{level}] :{message}")

    def save(self):
        data = {
            "task_id": self.task_id,
            "task_name": self.task_name,
            "start_time": self.create_time,
            "end_time": datetime.datetime.now().isoformat(),
            "logs": self.records
        }
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"日志已持久化至: {self.file_path}")
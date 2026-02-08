from resource.user.user_model import User
from resource.database.database import Database
from resource.oss.oss import Oss
from resource.task.task_model import BaseTask, TaskProcess

from resource.oss.minio_oss import MinioMethod
from resource.task.backup_task import BackupTaskProcess
from resource.database.postgres_db import PostgresMethod
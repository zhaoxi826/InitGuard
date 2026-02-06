from sqlmodel import create_engine, SQLModel,Session,select
from utils import PasswordHelper
from resource import User,BackupTask
import os

class PostgresInstance:
    def __init__(self):
        user = os.environ["POSTGRES_USER"]
        password = os.environ["POSTGRES_PASSWORD"]
        host = os.environ["POSTGRES_HOST"]
        port = os.environ["POSTGRES_PORT"]
        database = os.environ["POSTGRES_DB"]
        self.url = "postgresql://{}:{}@{}:{}/{}".format(user, password, host, port, database)
        self.engine = create_engine(self.url,echo=True)

    # 数据库核心方法
    def init(self):
        SQLModel.metadata.create_all(self.engine)

    def close_engine(self):
        self.engine.dispose()

    # 调度器方法
    def get_task(self,task_id):
        with Session(self.engine) as session:
            task = session.get("tasks_list",task_id)
            return task

    def get_database(self,database_id):
        with Session(self.engine) as session:
            database = session.get("databases_list",database_id)
            return database

    def get_oss(self,oss_id):
        with Session(self.engine) as session:
            oss = session.get("oss_list",oss_id)
            return oss

    # fastapi方法
    def add_user(self,user_name,user_password,user_email):
        with Session(self.engine) as session:
            hashed_pwd = PasswordHelper.hash_password(user_password)
            user = User(user_name=user_name,user_password=hashed_pwd,user_email=user_email)
            session.add(user)
            session.commit()

    def login_user(self,user_name,user_password):
        with Session(self.engine) as session:
            statement = select(User).where(User.username == user_name)
            user = session.exec(statement).first()
            if user and PasswordHelper.verify_password(user_password,user.user_password):
                return user.user_id
            return False

    def init_superuser(self):
        with Session(self.engine) as session:
            super_user = session.get(User, 1)
            if not super_user:
                user_name = os.environ.get("SUPERUSER_NAME")
                user_email = os.environ.get("SUPERUSER_EMAIL")
                user_password = os.environ.get("SUPERUSER_PASSWORD")
                hashed_pwd = PasswordHelper.hash_password(user_password)
                super_user = User(user_id=1, username=user_name,user_email=user_email,user_password=hashed_pwd,user_authority="superuser")
                session.add(super_user)
                session.commit()

    def add_task(self,task_name,database_id,oss_id,task_type,owner_id):
        with Session(self.engine) as session:
            task_dict = {
                "backup_task":BackupTask
            }
            task_class = task_dict.get(task_type)
            if not task_class:
                raise ValueError(f"不支持的任务类型: {task_type}")
            task = task_class(
                task_name=task_name,
                database_id=database_id,
                oss_id=oss_id,
                owner_id=owner_id
            )
            session.add(task)
            session.commit()
            session.refresh(task)
            return task.task_id

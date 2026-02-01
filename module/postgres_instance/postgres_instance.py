from sqlmodel import create_engine, SQLModel,Session,select
from utils import PasswordHelper
from resource import User
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

    # 数据库初始化
    def init(self):
        SQLModel.metadata.create_all(self.engine)

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

from sqlmodel import create_engine, SQLModel,Session

class PostgresInstance:
    def __init__(self, host, port, user, password, database):
        self.url = "postgresql://{}:{}@{}:{}/{}".format(user, password, host, port, database)
        self.engine = create_engine(self.url,echo=True)

    def init(self):
        SQLModel.metadata.create_all(self.engine)

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

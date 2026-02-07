from .database import Database, DatabaseMethod
import os
import subprocess

class PostgresDatabase(Database):
    __mapper_args__ = {
        "polymorphic_identity": "postgres",
    }

class PostgresMethod(DatabaseMethod):
    def __init__(self,postgres_db:PostgresDatabase,db_name):
        self.database = postgres_db
        self.db_name = db_name
    def get_dump_stream(self):
        env = os.environ.copy()
        env["PGPASSWORD"] = self.database.password
        command = ["pg_dump",
                   "-h", self.database.host,
                   "-U", self.database.username,
                   "-d", self.db_name,
                   "-Fc"]
        process = subprocess.Popen(command, stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env)
        return process,process.stdout,process.stderr

    def database_restore(self):
        pass
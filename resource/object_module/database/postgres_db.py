from .database import Database
import os
import subprocess

class PostgresDatabase(Database):
    def __init__(self):
        super().__init__()

    def get_dump_stream(self):
        env = os.environ.copy()
        env["PGPASSWORD"] = self.password
        command = ["pg_dump",
                   "-h", self.host,
                   "-U", self.db_user,
                   "-d", self.db_name,
                   "-Fc"]
        process = subprocess.Popen(command, stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env)
        return process,process.stdout,process.stderr

    def database_restore(self):
        pass
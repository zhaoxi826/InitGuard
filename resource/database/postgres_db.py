from .database import Database, DatabaseMethod
import os
import asyncio


class PostgresMethod(DatabaseMethod):
    def __init__(self,postgres_db:Database,db_name):
        self.database = postgres_db
        self.db_name = db_name

    async def get_dump_stream(self):
        env = os.environ.copy()
        env["PGPASSWORD"] = self.database.password
        command = ["pg_dump",
                   "-h", self.database.host,
                   "-U", self.database.username,
                   "-d", self.db_name,
                   "-Fc"]
        process = await asyncio.create_subprocess_exec(*command, stdout=asyncio.subprocess.PIPE,stderr=asyncio.subprocess.PIPE,env=env)
        return process,process.stdout,process.stderr

    def database_restore(self):
        pass
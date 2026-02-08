from resource.database.postgres_db import PostgresMethod
from resource.oss.minio_oss import MinioMethod

class GetObjectMethod():
    @staticmethod
    def get_database_type(database, db_name):
        match database.database_type:
            case "postgres":
                return PostgresMethod(database, db_name)
            case _:
                return None

    @staticmethod
    def get_oss_type(oss):
        match oss.oss_type:
            case "minio":
                return MinioMethod(oss)
            case _:
                return None
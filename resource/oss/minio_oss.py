import os
from .oss import Oss,OssMethod
import boto3

class Minio(Oss):
    __mapper_args__ = {
        "polymorphic_identity": "minio",
    }

class MinioMethod(OssMethod):
    def __init__(self,minio:Minio):
        self.bucket = minio.bucket
        self.s3 = boto3.client(
            's3',
            endpoint_url=minio.endpoint,
            aws_access_key_id=minio.access_key,
            aws_secret_access_key=minio.secret_key
        )
    def upload_stream(self, stream, target_path):
        self.s3.upload_fileobj(stream, self.bucket, target_path)

    def download_stream(self):
        pass


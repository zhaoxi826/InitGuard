import os
from .oss import Oss
import boto3

class MinioOss(Oss):
    def __init__(self):
        super().__init__()
        self.bucket = os.environ.get("OSS_BUCKET")
        if not self.bucket:
            raise ValueError("环境变量 OSS_BUCKET 未设置！")
        self.s3 = boto3.client(
            's3',
            endpoint_url=self.endpoint,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key
        )

    def upload_stream(self, stream, target_path):
        self.s3.upload_fileobj(stream, self.bucket, target_path)

    def download_stream(self):
        pass


from .oss import Oss,OssMethod
import aioboto3


class MinioMethod(OssMethod):
    def __init__(self,minio:Oss):
        self.minio = minio

    async def upload_stream(self, stream, target_path):
        session = aioboto3.Session()
        endpoint = self.minio.endpoint
        if not endpoint.startswith("http"):
            endpoint = f"http://{endpoint}"
        async with session.client("s3",endpoint_url=endpoint,aws_access_key_id=self.minio.access_key,aws_secret_access_key=self.minio.secret_key) as s3_client:
            await s3_client.upload_fileobj(stream, self.minio.bucket, target_path)

    def download_stream(self):
        pass


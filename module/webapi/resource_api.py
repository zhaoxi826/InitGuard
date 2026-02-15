from typing import Union,Literal
from fastapi import APIRouter,Depends,HTTPException,status
from module import PostgresInstance
from .dependence import dependence_pg
from pydantic import BaseModel,Field
from utils.security import get_current_user
from resource import Oss,Database

router = APIRouter(prefix="/api/resource", tags=["资源管理"])


class DatabaseValue(BaseModel):
    type: Literal["database"]
    database_type: Literal["postgres"]
    host: str
    port: int = 5432
    username: str
    password: str

class OssValue(BaseModel):
    type: Literal["oss"]
    oss_type: Literal["minio"]
    endpoint: str
    access_key: str
    secret_key: str
    bucket: str

class ResourceModel(BaseModel):
    resource_name: str
    resource_value: Union[DatabaseValue, OssValue] = Field(discriminator="type")

@router.post("/create")
async def create_resource(resource: ResourceModel,
                    postgres_instance: PostgresInstance=Depends(dependence_pg),
                    user_id:int = Depends(get_current_user)):
    val = resource.resource_value
    instance = None
    if isinstance(val, DatabaseValue):
        match val.database_type:
            case "postgres":
                instance = Database(database_name=resource.resource_name,
                                            host=val.host,
                                            port=val.port,
                                            username=val.username,
                                            password= val.password,
                                            owner_id=user_id,
                                            database_type="postgres"
                                            )
    elif isinstance(val, OssValue):
        match val.oss_type:
            case "minio":
                instance = Oss(oss_name=resource.resource_name,
                                 endpoint=val.endpoint,
                                 access_key=val.access_key,
                                 secret_key=val.secret_key,
                                 bucket=val.bucket,
                                 owner_id=user_id,
                                 oss_type="minio"
                                 )
    if instance is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不支持的资源细分类型"
        )
    try:
        await postgres_instance.add_instance(instance)
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"数据库写入失败: {str(e)}")
    return {"status": "success", "detail":"资源创建成功"}

@router.get("/list")
async def list_resources(
        postgres_instance: PostgresInstance = Depends(dependence_pg),
        user_id: int = Depends(get_current_user)
        ):
    databases = await postgres_instance.get_databases(user_id)
    oss = await postgres_instance.get_oss(user_id)
    return {"databases": databases, "oss": oss}
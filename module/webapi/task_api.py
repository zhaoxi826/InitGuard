from fastapi import APIRouter,Depends,HTTPException,status
from module import PostgresInstance,RedisInstance
from .dependence import dependence_pg,dependence_redis
from pydantic import BaseModel
from utils.security import get_current_user

router = APIRouter(prefix="/api/task", tags=["任务管理"])

class TaskModel(BaseModel):
    task_name: str
    database_id: int | None
    oss_id: int | None
    database_name: str
    task_type: str

@router.post("/create")
async def create_task(task: TaskModel,
                postgres: PostgresInstance = Depends(dependence_pg),
                redis: RedisInstance = Depends(dependence_redis),
                user_id: int = Depends(get_current_user)):
    try:
        task_id = await postgres.add_task(task.task_name,task.database_id,task.oss_id,task.task_type,user_id,task.database_name)
        await redis.add_task(task_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="任务类型不存在"
        )
    return {"status": "success", "detail":"任务创建成功"}

class TaskFilterModel(BaseModel):
    database_id: int | None = None
    status: str | None = None
    start_time: str | None = None
    task_type: str | None = None

@router.get("/list")
async def get_tasks(
        filter: TaskFilterModel = Depends(),
        user_id: int = Depends(get_current_user),
        postgres: PostgresInstance = Depends(dependence_pg)
        ):
    tasks = await postgres.get_tasks(
        user_id=user_id,
        database_id=filter.database_id,
        status=filter.status,
        start_time=filter.start_time,
        task_type=filter.task_type
    )
    return tasks


@router.get("/{task_id}")
async def get_task(task_id: int,user_id: int = Depends(get_current_user),postgres : PostgresInstance = Depends(dependence_pg)):
    task = await postgres.get_task(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="任务不存在"
        )
    if task.owner_id != user_id and user_id != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足"
        )
    return task
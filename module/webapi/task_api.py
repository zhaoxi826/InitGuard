from fastapi import APIRouter,Depends,HTTPException,status
from module import PostgresInstance,RedisInstance
from dependence import dependence_pg,dependence_redis
from pydantic import BaseModel
from utils.security import get_current_user

router = APIRouter(prefix="/api/task", tags=["任务管理"])

class TaskModel(BaseModel):
    task_name: str
    database_id: int | None
    oss_id: int | None
    task_type: str

@router.post("/create")
def create_task(task: TaskModel,
                postgres: PostgresInstance = Depends(dependence_pg),
                redis: RedisInstance = Depends(dependence_redis),
                user_id: int = Depends(get_current_user)):
    try:
        task_id = postgres.add_task(task.task_name,task.database_id,task.oss_id,task.task_type,user_id)
        redis.add_task(task_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="任务类型不存在"
        )
    return {"status": "success", "detail":"任务创建成功"}
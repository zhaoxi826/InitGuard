from fastapi import APIRouter,Depends,HTTPException,status
from pydantic import BaseModel, EmailStr
from .dependence import dependence_pg,dependence_redis
from module import PostgresInstance,RedisInstance
from utils import SecurityHelper

router = APIRouter(prefix="/api/auth", tags=["用户管理"])

class UserRegister(BaseModel):
    username: str
    password: str
    email: EmailStr

class UserLogin(BaseModel):
    username: str
    password: str

@router.post("/register")
async def register_user(user_register: UserRegister,postgres: PostgresInstance = Depends(dependence_pg)):
    await postgres.add_user(user_register.username, user_register.password, user_register.email)
    return {"message": "注册成功"}

@router.post("/login")
async def login_user(user_login:UserLogin,postgres: PostgresInstance = Depends(dependence_pg),redis: RedisInstance = Depends(dependence_redis)):
    result =  await postgres.login_user(user_login.username, user_login.password)
    if result:
        token = await SecurityHelper.login_and_save_token(result,redis)
        return {"token":f"{token}"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码不正确"
        )


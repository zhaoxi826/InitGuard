from fastapi import APIRouter
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/auth", tags=["用户管理"])

class UserRegister(BaseModel):
    username: str
    password: str
    email: EmailStr

@router.post("/register", response_model=UserRegister)
async def register(user_register: UserRegister):
    pass
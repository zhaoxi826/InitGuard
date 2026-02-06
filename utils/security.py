import os
import jwt
import datetime
from module import RedisInstance
from fastapi import Request,HTTPException,Depends
from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials
from passlib.context import CryptContext

security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

class PasswordHelper:
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

class SecurityHelper:
    @staticmethod
    def create_access_token(data: dict, expires_delta: int = 60):
        to_encode = data.copy()
        expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=expires_delta)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def login_and_save_token(user_id: int, redis: RedisInstance):
        token = SecurityHelper.create_access_token({"user_id": user_id})
        redis.login_token(token, user_id)
        return token

    @staticmethod
    def verify_with_redis(user_id: int, incoming_token: str, redis: RedisInstance):
        stored_token = redis.get_token(user_id)
        if not stored_token or stored_token != incoming_token:
            return False
        return True


async def get_current_user(
        request: Request,
        auth: HTTPAuthorizationCredentials = Depends(security)
):
    token = auth.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token 载荷缺失")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token 已过期")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token 无效")
    except Exception:
        raise HTTPException(status_code=401, detail="鉴权失败")
    if not SecurityHelper.verify_with_redis(user_id, token, request.app.state.redis):
        raise HTTPException(status_code=401, detail="登录已失效")
    return user_id
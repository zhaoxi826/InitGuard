import os
from passlib.context import CryptContext
import jwt
import datetime
from module import RedisInstance

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
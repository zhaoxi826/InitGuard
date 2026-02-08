from sqlmodel import SQLModel,Field

class User(SQLModel,table=True):
    __tablename__="user"
    user_id : int = Field(default=None,primary_key=True)
    user_name : str = Field(default=None)
    user_email : str = Field(default=None)
    user_password : str = Field(default=None)
    user_authority : str = Field(default="user")



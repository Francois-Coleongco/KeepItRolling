import os
from pydantic import BaseModel

from dotenv import load_dotenv

load_dotenv()
# constants

SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = "HS256"


ACCESS_TOKEN_EXPIRE_MINUTES = 1440

UPLOAD_DIR = "UPLOADS/"
OUTPUT_DIR = "OUTPUTS/"



# objects

class User(BaseModel):
    username: str

class Token(BaseModel):
    token: str
    token_type: str


class TokenData(BaseModel):
    username: str

class UserInDB(User):
    hashed_password: str



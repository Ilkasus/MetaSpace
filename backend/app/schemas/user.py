from pydantic import BaseModel

class UserCreate(BaseModel):
    nickname: str
    password: str

class UserOut(BaseModel):
    id: int
    nickname: str

    class Config:
        orm_mode = True

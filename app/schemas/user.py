from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    is_superuser: bool = False


# Properties to receive on creation
class UserCreate(UserBase):
    password: str


# Properties to receive on update
class UserUpdate(UserBase):
    pass


class UserInDBBase(UserBase):
    id: int
    is_superuser: bool

    class Config:
        orm_mode = True


# Properties received from API
class User(UserInDBBase):
    pass


# Properties stored in database
class UserInDB(UserInDBBase):
    hashed_password: str

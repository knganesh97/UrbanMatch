from typing_extensions import Annotated
from pydantic import BaseModel, EmailStr, PlainSerializer
from typing import List

class InterestBase(BaseModel):
    hobby: str

class Interest(InterestBase):
    user_id: int
    id: int

    class Config:
        orm_mode = True

class InterestCreate(Interest):
    pass

class UserBase(BaseModel):
    name: str
    age: int
    gender: str
    email: EmailStr
    city: str
    interests: List[str]

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class UserCreate(User):
    pass

CustomListInterests = Annotated[
    List[InterestBase], PlainSerializer(
        lambda interests: [interest.hobby for interest in interests], return_type=List[str]
    )
]

class UserResponse(BaseModel):
    id: int
    name: str
    age: int
    gender: str
    email: EmailStr
    city: str
    interests: CustomListInterests
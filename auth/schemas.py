from typing import Any, Union
import peewee
from pydantic import BaseModel
from pydantic.utils import GetterDict


class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res


class UserLogin(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class UserCreate(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class UserList(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    password: str

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None

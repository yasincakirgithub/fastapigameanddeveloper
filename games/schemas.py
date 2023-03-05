from typing import Any, Union
from datetime import date
import peewee
from pydantic import BaseModel
from pydantic.utils import GetterDict

class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, peewee.ModelSelect):
            return list(res)
        return res

class GameBase(BaseModel):
    name: str
    description: Union[str, None] = None
    publication_date: Union[date, None]
    developer_id: int
    status: bool

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict

from typing import List

from pydantic import BaseModel


class DtoResHealth(BaseModel):
    status: str = "OK"


class DtoResOrder(BaseModel):
    id: int

    class Config:
        from_attributes = True


class DtoResOrders(BaseModel):
    data: List[DtoResOrder]


class DtoResMember(BaseModel):
    name: str

    class Config:
        from_attributes = True


class DtoResMembers(BaseModel):
    data: List[DtoResMember]

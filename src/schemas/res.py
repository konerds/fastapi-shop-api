from typing import List

from pydantic import BaseModel


class DtoResHealth(BaseModel):
    status: str = "OK"


class DtoResOrder(BaseModel):
    id: int

    class Config:
        from_attributes = True


class DtoResOrders(BaseModel):
    orders: List[DtoResOrder]

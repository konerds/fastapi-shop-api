from typing import List

from pydantic import BaseModel


class DtoResHealth(BaseModel):
    status: str = "OK"


class DtoResOrderedProduct(BaseModel):
    id: int
    name: str
    price: int
    quantity: int


class DtoResOrder(BaseModel):
    id: int
    products: List[DtoResOrderedProduct]

    class Config:
        from_attributes = True


class DtoResOrders(BaseModel):
    data: List[DtoResOrder]


class DtoResMember(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class DtoResMembers(BaseModel):
    data: List[DtoResMember]


class DtoResProduct(BaseModel):
    id: int
    name: str
    price: int
    stock: int

    class Config:
        from_attributes = True


class DtoResProducts(BaseModel):
    data: List[DtoResProduct]

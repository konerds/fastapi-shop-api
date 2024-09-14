from pydantic import BaseModel


class DtoReqPostMember(BaseModel):
    name: str
    address: str


class DtoReqPostProduct(BaseModel):
    name: str
    price: int
    stock: int


class DtoReqPostOrder(BaseModel):
    member_id: int
    product_id: int
    quantity: int

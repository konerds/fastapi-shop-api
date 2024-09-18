from pydantic import BaseModel


class DtoReqPostMember(BaseModel):
    email: str
    password: str
    name: str


class DtoReqSigninMember(BaseModel):
    email: str
    password: str


class DtoReqPostProduct(BaseModel):
    name: str
    price: int
    stock: int


class DtoReqPostOrder(BaseModel):
    member_id: int
    product_id: int
    quantity: int

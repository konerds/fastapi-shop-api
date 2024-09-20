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
    product_id: int
    quantity: int
    address: str


class DtoReqPutOrderStatus(BaseModel):
    status: str


class DtoReqPutDeliveryStatus(BaseModel):
    status: str

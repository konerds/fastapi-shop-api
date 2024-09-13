from pydantic import BaseModel


class DtoReqPostMember(BaseModel):
    name: str
    address: str

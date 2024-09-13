import uvicorn
from fastapi import FastAPI

from api import base, orders, members

app = FastAPI()

app.include_router(base.router)
app.include_router(orders.router)
app.include_router(members.router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

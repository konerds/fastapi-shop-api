import uvicorn
from fastapi import FastAPI

from api import base, products, orders, members

app = FastAPI()

app.include_router(base.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(members.router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

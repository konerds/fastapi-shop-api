import uvicorn
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from api import base, products, orders, members
from core.config import settings

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=settings.SESSION_SECRET_KEY)

app.include_router(base.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(members.router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

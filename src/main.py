import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware

from api import base, products, orders, members, admin
from core.config import settings
from db.models import Member
from db.repositories import MemberRepository
from dependencies import get_db, encrypt


@asynccontextmanager
async def lifespan(_: FastAPI):
    session: Session = next(get_db())
    member_repository = MemberRepository(session)
    admin = member_repository.get_one_by_email(settings.ADMIN_EMAIL)
    if admin is None:
        member_repository.save(
            Member.create(
                True,
                settings.ADMIN_EMAIL,
                encrypt(settings.ADMIN_PASSWORD),
                settings.ADMIN_NAME
            )
        )
    session.close()
    yield


app = FastAPI(lifespan=lifespan)
STATIC_DIR = os.path.join(os.path.join(os.path.dirname(__file__), "static"))
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.add_middleware(SessionMiddleware, secret_key=settings.SESSION_SECRET_KEY)

app.include_router(admin.router)
app.include_router(base.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(members.router)


@app.exception_handler(404)
async def not_found_page_handler(request: Request, exception: HTTPException):
    return RedirectResponse("/")


if __name__ == "__main__":
    if settings.ENV == "prod":
        uvicorn.run("main:app", port=settings.PORT, reload=True)
    else:
        uvicorn.run("main:app", port=settings.PORT, log_level="info")

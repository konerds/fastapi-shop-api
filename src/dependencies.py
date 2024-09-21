import os

from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from sqlalchemy import text

from core.config import settings
from db.models import OrderStatus, DeliveryStatus
from db.session import SessionLocal

crypt_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def encrypt(data):
    return crypt_context.hash(data)


def verify(plain, encrypted):
    return crypt_context.verify(plain, encrypted)


def get_db():
    session = SessionLocal()
    try:
        if settings.ENV == "dev":
            session.execute(text("PRAGMA foreign_keys=ON;"))
        yield session
    finally:
        session.close()


SOURCE_DIR = os.path.dirname(__file__)
STATIC_DIR = os.path.join(SOURCE_DIR, "static")
TEMPLATE_DIR = os.path.join(SOURCE_DIR, "templates")

templates = Jinja2Templates(directory=TEMPLATE_DIR)
templates.env.globals['env'] = settings.ENV


def format_datetime(ts):
    ds = ['월', '화', '수', '목', '금', '토', '일']
    d = ds[ts.weekday()]
    return ts.strftime(
        "%Y년 %m월 %d일 ({}) %H:%M:%S"
        .format(d)
        .encode('unicode-escape')
        .decode()
    ).encode().decode(
        'unicode-escape'
    )


templates.env.filters["convert_datetime"] = format_datetime


def convert_order_status(status: OrderStatus):
    if status == OrderStatus.PROCEEDING:
        return "주문 진행"
    if status == OrderStatus.COMPLETED:
        return "결제 완료"
    if status == OrderStatus.CANCELED:
        return "주문 취소"


def convert_delivery_status(status: DeliveryStatus):
    if status == DeliveryStatus.PENDING:
        return "배송 대기"
    if status == DeliveryStatus.PROCEEDING:
        return "배송 진행"
    if status == DeliveryStatus.COMPLETED:
        return "배송 완료"
    if status == DeliveryStatus.CANCELED:
        return "취소"

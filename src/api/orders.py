from typing import List

from fastapi import APIRouter, Depends, Query, Request, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from db.models import Order, OrderedProduct
from db.repositories import OrderRepository, MemberRepository, ProductRepository
from dependencies import get_db
from schema.req import DtoReqPostOrder
from schema.res import DtoResOrders, DtoResOrder, DtoResOrderedProduct

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get(
    "/orders",
    response_model=DtoResOrders
)
def get_orders_handler(
        request: Request,
        sort_type: str = Query(
            "asc",
            alias="sort_type"
        ),
        session: Session = Depends(get_db)
):
    member_id = request.session.get("member_id")
    if member_id is None:
        raise HTTPException(
            status_code=401,
            detail="인가되지 않은 요청입니다..."
        )
    member_repository = MemberRepository(session)
    member = member_repository.get_one(member_id)
    if member is None:
        raise HTTPException(
            status_code=404,
            detail="존재하지 않는 회원입니다..."
        )
    order_repository = OrderRepository(session)
    orders: List[Order] = order_repository.get_all_by_member_id(
        member.id,
        sort_type == "desc"
    )
    return templates.TemplateResponse(
        "orders.html",
        {
            "request": request,
            "orders": orders
        }
    )


@router.post(
    "/api/orders",
    response_model=DtoResOrder
)
def post_order_handler(
        request: Request,
        req_body: DtoReqPostOrder,
        session: Session = Depends(get_db),
):
    member_id = request.session.get("member_id")
    if member_id is None:
        raise HTTPException(
            status_code=401,
            detail="인가되지 않은 요청입니다..."
        )
    member_repository = MemberRepository(session)
    member = member_repository.get_one(member_id)
    if member is None:
        raise HTTPException(
            status_code=404,
            detail="존재하지 않는 회원입니다..."
        )
    product_repository = ProductRepository(session)
    product = product_repository.get_one(req_body.product_id)
    ordered_product = OrderedProduct.create(product, req_body.quantity)
    order_repository = OrderRepository(session)
    order = order_repository.save(
        Order.create(
            member=member,
            ordered_products=[ordered_product]
        )
    )
    return DtoResOrder(
        id=order.id,
        products=[DtoResOrderedProduct(
            id=product.id,
            name=product.name,
            price=product.price,
            quantity=req_body.quantity
        )]
    )


@router.delete(
    "/api/orders/{order_id}"
)
def delete_order_handler(
        order_id: int,
        request: Request,
        session: Session = Depends(get_db),
):
    member_id = request.session.get("member_id")
    if member_id is None:
        raise HTTPException(
            status_code=401,
            detail="인가되지 않은 요청입니다..."
        )
    member_repository = MemberRepository(session)
    member = member_repository.get_one(member_id)
    if member is None:
        raise HTTPException(
            status_code=404,
            detail="존재하지 않는 회원입니다..."
        )
    order_repository = OrderRepository(session)
    order_repository.delete_one(order_id)

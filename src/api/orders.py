from fastapi import status, APIRouter, Depends, Query, Request, HTTPException, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from core.config import settings
from db.models import Order, OrderedProduct, OrderStatus
from db.repositories import OrderRepository, MemberRepository, ProductRepository
from dependencies import get_db, TEMPLATE_DIR
from schema.req import DtoReqPostOrder
from schema.res import DtoResOrders, DtoResOrder, DtoResOrderedProduct

router = APIRouter()
templates = Jinja2Templates(directory=TEMPLATE_DIR)
templates.env.globals['env'] = settings.ENV


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
        return RedirectResponse("/signin")
    member_repository = MemberRepository(session)
    member = member_repository.get_one(member_id)
    if member is None:
        request.session.pop("member_id", None)
        return RedirectResponse("/signin")
    if member.is_admin:
        return RedirectResponse("/")
    product_repository = ProductRepository(session)
    products = product_repository.get_all(sort_type == "desc")
    order_repository = OrderRepository(session)
    orders = order_repository.get_all_by_member_id(
        member.id,
        sort_type == "desc"
    )
    return templates.TemplateResponse(
        "orders.html",
        {
            "title_page": "Shop Service - Orders",
            "title_header": "나의 주문 목록",
            "request": request,
            "products": products,
            "orders": orders
        }
    )


@router.post(
    "/api/orders",
    status_code=status.HTTP_201_CREATED,
    response_model=DtoResOrder
)
def post_order_handler(
        request: Request,
        req_body: DtoReqPostOrder,
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
    product_repository = ProductRepository(session)
    product = product_repository.get_one(req_body.product_id)
    if req_body.quantity > product.stock:
        raise HTTPException(
            status_code=400,
            detail="재고가 없습니다..."
        )
    ordered_product = OrderedProduct.create(product, req_body.quantity)
    order_repository = OrderRepository(session)
    order = order_repository.save(
        Order.create(
            member=member,
            ordered_products=[ordered_product],
            address=req_body.address
        )
    )
    return DtoResOrder(
        id=order.id,
        address=order.delivery.address,
        products=[DtoResOrderedProduct(
            id=product.id,
            name=product.name,
            price=product.price,
            quantity=req_body.quantity
        )]
    )


@router.delete(
    "/api/orders/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_order_handler(
        request: Request,
        order_id: int,
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
    order = order_repository.get_one(order_id)
    order_status = order.get_status()
    if order_status != OrderStatus.PROCEEDING:
        raise HTTPException(
            status_code=400,
            detail="진행중인 주문만 취소할 수 있습니다..."
        )
    order.cancel()
    session.commit()
    return Response()

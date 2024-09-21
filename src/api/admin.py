from fastapi import status, Query, Request, APIRouter, Depends, HTTPException, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from db.models import Product, OrderStatus, DeliveryStatus
from db.repositories import MemberRepository, ProductRepository, OrderRepository
from dependencies import get_db, templates
from schema.req import DtoReqPostProduct, DtoReqPutOrderStatus, DtoReqPutDeliveryStatus
from schema.res import DtoResProduct

router = APIRouter()


@router.get(
    "/admin"
)
def get_admin_page_handler():
    return RedirectResponse("/admin/products")


@router.get(
    "/admin/products"
)
def get_admin_products_page_handler(
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
    if not member.is_admin:
        return RedirectResponse("/")
    product_repository = ProductRepository(session)
    products = product_repository.get_all(sort_type == "desc")
    return templates.TemplateResponse(
        "admin/products.html",
        {
            "request": request,
            "type_page": "products",
            "title_page": "Shop Admin Service - Products",
            "title_header": "관리자 페이지 - 상품 관리",
            "products": products
        }
    )


@router.get(
    "/admin/orders"
)
def get_admin_orders_page_handler(
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
    if member.is_admin is False:
        return RedirectResponse("/")
    order_repository = OrderRepository(session)
    orders = order_repository.get_all(sort_type == "desc")
    return templates.TemplateResponse(
        "admin/orders.html",
        {
            "request": request,
            "type_page": "orders",
            "title_page": "Shop Admin Service - Orders",
            "title_header": "관리자 페이지 - 주문 관리",
            "orders": orders
        }
    )


@router.post(
    "/api/admin/products",
    status_code=status.HTTP_201_CREATED,
    response_model=DtoResProduct
)
def post_product_handler(
        request: Request,
        req_body: DtoReqPostProduct,
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
    if not member.is_admin:
        raise HTTPException(
            status_code=401,
            detail="인가되지 않은 요청입니다..."
        )
    product_repository = ProductRepository(session)
    product = product_repository.get_one_by_name(req_body.name)
    if product is not None:
        raise HTTPException(
            status_code=400,
            detail="이미 존재하는 상품입니다..."
        )
    return DtoResProduct.model_validate(
        product_repository.save(
            Product.create(
                req_body.name,
                req_body.price,
                req_body.stock
            )
        )
    )


@router.put(
    "/api/admin/products/{product_id}",
    response_model=DtoResProduct
)
def put_product_handler(
        request: Request,
        product_id: int,
        req_body: DtoReqPostProduct,
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
    if not member.is_admin:
        raise HTTPException(
            status_code=401,
            detail="인가되지 않은 요청입니다..."
        )
    product_repository = ProductRepository(session)
    product = product_repository.get_one(product_id)
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="존재하지 않는 상품입니다..."
        )
    if product_repository.get_one_by_name(req_body.name).id != product.id:
        raise HTTPException(
            status_code=400,
            detail="이미 존재하는 상품입니다..."
        )
    product.name = req_body.name
    product.price = req_body.price
    product.stock = req_body.stock
    return DtoResProduct.model_validate(
        product_repository.save(
            product
        )
    )


@router.put(
    "/api/admin/orders/{order_id}",
)
def put_order_status_handler(
        request: Request,
        order_id: int,
        req_body: DtoReqPutOrderStatus,
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
    if not member.is_admin:
        raise HTTPException(
            status_code=401,
            detail="인가되지 않은 요청입니다..."
        )
    order_repository = OrderRepository(session)
    order = order_repository.get_one(order_id)
    order_status = order.get_status()
    if order_status == OrderStatus.CANCELED:
        raise HTTPException(
            status_code=400,
            detail="취소된 주문은 변경할 수 없습니다..."
        )
    delivery_status = order.delivery.get_status()
    if order_status == OrderStatus.COMPLETED and delivery_status == DeliveryStatus.COMPLETED:
        raise HTTPException(
            status_code=400,
            detail="결제 및 배송이 완료된 주문은 변경할 수 없습니다..."
        )
    order_status = OrderStatus(req_body.status)
    if order_status == OrderStatus.CANCELED:
        order.cancel()
    else:
        order.set_status(order_status)
        if order_status == OrderStatus.PROCEEDING:
            delivery_status = DeliveryStatus.PENDING
            order.delivery.set_status(delivery_status)
    order = order_repository.save(order)
    return {
        "id": order.id,
        "order_status": order_status.value,
        "delivery_status": delivery_status.value
    }


@router.put(
    "/api/admin/orders/{order_id}/delivery",
)
def put_order_delivery_status_handler(
        request: Request,
        order_id: int,
        req_body: DtoReqPutDeliveryStatus,
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
    if not member.is_admin:
        raise HTTPException(
            status_code=401,
            detail="인가되지 않은 요청입니다..."
        )
    order_repository = OrderRepository(session)
    order = order_repository.get_one(order_id)
    order_status = order.get_status()
    if order_status != OrderStatus.COMPLETED:
        raise HTTPException(
            status_code=400,
            detail="결제가 완료된 주문의 배송 상태만 변경할 수 있습니다..."
        )
    delivery_status = order.delivery.get_status()
    if delivery_status == DeliveryStatus.CANCELED:
        raise HTTPException(
            status_code=400,
            detail="취소된 주문의 배송 상태는 변경할 수 없습니다..."
        )
    if order_status == OrderStatus.COMPLETED and delivery_status == DeliveryStatus.COMPLETED:
        raise HTTPException(
            status_code=400,
            detail="결제 및 배송이 완료된 주문은 변경할 수 없습니다..."
        )
    delivery_status = DeliveryStatus(req_body.status)
    order.delivery.set_status(delivery_status)
    order = order_repository.save(order)
    return {
        "id": order.id,
        "order_status": order_status.value,
        "delivery_status": delivery_status.value
    }


@router.delete(
    "/api/admin/orders/{order_id}",
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
    if not member.is_admin:
        raise HTTPException(
            status_code=401,
            detail="인가되지 않은 요청입니다..."
        )
    order_repository = OrderRepository(session)
    order = order_repository.get_one(order_id)
    order_status = order.get_status()
    if not (order_status == OrderStatus.CANCELED or (
            order_status == OrderStatus.COMPLETED and order.delivery.get_status() == DeliveryStatus.COMPLETED)):
        raise HTTPException(
            status_code=400,
            detail="취소 또는 결제 및 배송 완료된 주문에 대해서만 주문 이력을 삭제할 수 있습니다..."
        )
    session.delete(order)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

from fastapi import status, Query, Request, APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from db.models import Product
from db.repositories import MemberRepository, ProductRepository, OrderRepository
from dependencies import get_db
from schema.req import DtoReqPostProduct
from schema.res import DtoResProduct

router = APIRouter()
templates = Jinja2Templates(directory="templates")


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
        return RedirectResponse("/signin")
    if member.is_admin is False:
        return RedirectResponse("/")
    product_repository = ProductRepository(session)
    products = product_repository.get_all(sort_type == "desc")
    return templates.TemplateResponse(
        "admin/products.html",
        {
            "type_page": "products",
            "title_page": "Shop Admin Service - Products",
            "title_header": "관리자 페이지 - 상품 관리",
            "request": request,
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
        return RedirectResponse("/signin")
    if member.is_admin is False:
        return RedirectResponse("/")
    order_repository = OrderRepository(session)
    orders = order_repository.get_all(sort_type == "desc")
    return templates.TemplateResponse(
        "admin/orders.html",
        {
            "type_page": "orders",
            "title_page": "Shop Admin Service - Orders",
            "title_header": "관리자 페이지 - 주문 관리",
            "request": request,
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
    if member.is_admin is False:
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
    status_code=status.HTTP_201_CREATED,
    response_model=DtoResProduct
)
def post_product_handler(
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
    if member.is_admin is False:
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
    if product_repository.get_one_by_name(req_body.name).id is not product.id:
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

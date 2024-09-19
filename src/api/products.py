from typing import List

from fastapi import status, APIRouter, Depends, Query, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from db.models import Product
from db.repositories import ProductRepository
from dependencies import get_db
from schema.req import DtoReqPostProduct
from schema.res import DtoResProducts, DtoResProduct

router = APIRouter(prefix="/api/products")
templates = Jinja2Templates(directory="templates")


@router.get(
    "/",
    response_model=DtoResProducts
)
def get_products_handler(
        sort_type: str = Query(
            "asc",
            alias="sort_type"
        ),
        session: Session = Depends(get_db)
):
    product_repository = ProductRepository(session)
    products: List[Product] = product_repository.get_all(
        sort_type == "desc"
    )
    return DtoResProducts(
        data=[
            DtoResProduct.model_validate(product)
            for product in products
        ]
    )


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=DtoResProduct
)
def post_product_handler(
        req_body: DtoReqPostProduct,
        session: Session = Depends(get_db),
):
    product_repository = ProductRepository(session)
    product = product_repository.get_one_by_name(req_body.name)
    if product is not None:
        raise HTTPException(
            status_code=400,
            detail="이미 존재하는 제품입니다..."
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

from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from db.models import Product
from db.repositories import ProductRepository
from db.session import get_db
from schema.req import DtoReqPostProduct
from schema.res import DtoResProducts, DtoResProduct

router = APIRouter(prefix="/api/products")


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
    response_model=DtoResProduct
)
def post_product_handler(
        req: DtoReqPostProduct,
        session: Session = Depends(get_db),
):
    product_repository = ProductRepository(session)
    return DtoResProduct.model_validate(
        product_repository.save(
            Product.create(
                req.name,
                req.price,
                req.stock
            )
        )
    )

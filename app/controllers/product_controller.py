from datetime import datetime

from fastapi import APIRouter, Depends, Path, Query, status
from typing import Annotated, Literal
from app.dependencies.product_dependencies import get_product_service
from app.models.user_model import User
from app.schemas.product_schema import ProductCreate, ProductRead, ProductUpdate
from app.security_pack.auth import verify_token_and_get_current_user
from app.services.product_service import ProductService



router = APIRouter(prefix="/products",tags=["products1x"])


@router.post("",response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(product_data: ProductCreate, service: ProductService = Depends(get_product_service)):
    return service.create_product(product_data)

@router.get("",response_model=list[ProductRead], status_code=status.HTTP_200_OK)
def get_all_products(service: ProductService = Depends(get_product_service)):
    return service.get_all_products()

# @router.get("/{product_id}",response_model=ProductRead, status_code=status.HTTP_200_OK)
# def get_product_by_id(product_id: Annotated[int, Path(gt=0, le=1000, description="Product ID")], service: ProductService = Depends(get_product_service)):
#     return service.get_product_by_id(product_id)

@router.put("/{product_id}",response_model=ProductRead, status_code=status.HTTP_200_OK)
def put_product(product_id: Annotated[int, Path(gt=0, le=1000, description="Product ID")], product_data: ProductCreate, service: ProductService = Depends(get_product_service), current_user: User = Depends(verify_token_and_get_current_user)):
    return service.put_product(product_id, product_data)

@router.patch("/{product_id}",response_model=ProductRead, status_code=status.HTTP_200_OK)
def patch_product(product_id: Annotated[int, Path(gt=0, le=1000, description="Product ID")], product_data: ProductUpdate, service: ProductService = Depends(get_product_service), current_user: User = Depends(verify_token_and_get_current_user)):
    return service.patch_product(product_id, product_data)

@router.delete("/{product_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: Annotated[int, Path(gt=0, le=1000, description="Product ID")], service: ProductService = Depends(get_product_service)):
    return service.delete_product(product_id)

@router.get("/filter",response_model=list[ProductRead], status_code=status.HTTP_200_OK)
def get_filtered_products(name_seq: Annotated[str | None, Query( min_length=3, max_length=20, description="Filter products by name sequence")] = None, 
                        description_seq: Annotated[str | None, Query( min_length=3, max_length=200, description="Filter products by description sequence")] = None,
                        min_price: Annotated[float | None, Query(ge=1, le=9999, description="Filter products by minimum price")] = 1,
                        max_price: Annotated[float | None, Query(ge=1, le=9999, description="Filter products by maximum price")] = 9999,
                        active_status: Annotated[bool | None, Query(description="Filter products by active status")] = None,
                        created_after: Annotated[datetime | None, Query(description="Filter products created after this date")] = None,
                        sort_by: Annotated[Literal["id", "name", "price", "stock_quantity", "created_at", "updated_at"] | None, Query(description="Sort products by this field")] = "id",
                        page_size: Annotated[int | None, Query(ge=5, le=20, description="Number of products per page")] = 8,
                        page_no: Annotated[int | None, Query(ge=1, le=2000, description="Page number for pagination")] = 1,
                        service: ProductService = Depends(get_product_service)
                        ):
    return service.get_filtered_products(name_seq, description_seq, min_price, max_price, active_status, created_after, sort_by, page_size, page_no)



@router.get("/{product_id}",response_model=ProductRead, status_code=status.HTTP_200_OK)
def get_product_by_id(product_id: Annotated[int, Path(gt=0, le=1000, description="Product ID")], service: ProductService = Depends(get_product_service)):
    return service.get_product_by_id(product_id)


# GET /products/filter was being matched by the earlier GET /products/{product_id} route. 
# FastAPI captures "filter" as product_id, then fails to parse it as an integer, producing this 422 response.

# In product_controller.py, register the static /filter route before the /{product_id} route. 
# Route matching follows registration order, so the static path will match first. 



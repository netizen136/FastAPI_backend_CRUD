from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing import Annotated, Literal
from datetime import datetime


productName = Annotated[str, Field(min_length=3, max_length=20, description="Name of the product.")]
productDescription = Annotated[str | None, Field(default=None, min_length=1, max_length=200, description="Description of the product.")]
productPrice = Annotated[float, Field(gt=0, lt=10000, description="Price of the product.")]
productStockQuantity = Annotated[int, Field(ge=0, le=1000, description="Stock quantity of the product.")]
productIsActive = Annotated[bool, Field(default=True, description="Indicates if the product is active.")]

productId = Annotated[int, Field( description="Unique identifier for the product.")]
productCreatedAt = Annotated[datetime, Field( description="Timestamp when the product was created.")]
productUpdatedAt = Annotated[datetime, Field( description="Timestamp when the product was last updated.")]

# Keep SAME name as the SQLAlchemy model class name for consistency.
class ProductCreate(BaseModel):
    name : productName
    description: productDescription 
    price: productPrice
    stock_quantity: productStockQuantity
    is_active: productIsActive


# ProductRead validates the final ORM object "product" in controller.
# response_model = ProductRead  & ConfigDict(from_attributes=True)
# Read attributes from the SQLAlchemy Product object.
# Validate them against ProductRead.
# Create and return a ProductRead Pydantic object.

class ProductRead(ProductCreate):
    model_config = ConfigDict(from_attributes=True)

    id: productId
    created_at: productCreatedAt
    updated_at: productUpdatedAt


class ProductUpdate(BaseModel):
    name: productName | None = None
    description: productDescription 
    price: productPrice | None = None
    stock_quantity: productStockQuantity | None = None
    is_active: productIsActive | None = None













from datetime import datetime
from typing import Literal

from app.models.product_model import Product
from app.schemas.product_schema import ProductCreate, ProductRead, ProductUpdate


class ProductRepo:
    def __init__(self, db):
        self.db = db

    def create_product(self, product: ProductCreate) -> Product:
        product_dict = product.model_dump()   # dictonary
        # The ** operator is used to unpack the dictionary 
        # and pass its key-value pairs as keyword arguments to the Product constructor.
        db_product = Product(**product_dict)  # SQLAlchemy object of type Product

        self.db.add(db_product)
        self.db.flush()  # Flush the changes to the database to generate the ID for the new product
        self.db.refresh(db_product)  # Refresh the instance to get the updated values from the database, including the generated ID and timestamps.

        return db_product

    def get_all_products(self) -> list[Product]:
        return self.db.query(Product).all()

    def get_product_by_id(self, product_id: int) -> Product | None:
        return self.db.query(Product).filter(Product.id == product_id).first()


    def put_product(self, product_id: int, product_data: ProductCreate) -> Product | None:
        db_product= self.get_product_by_id(product_id)
        if db_product is None:
            return None
        for key,value in product_data.model_dump().items():
            setattr(db_product,key,value)

        self.db.flush()
        self.db.refresh(db_product)
        return db_product

    def patch_product(self, product_id: int, product_data: ProductUpdate) -> Product | None:
        db_product = self.get_product_by_id(product_id)
        if db_product is None:
            return None

        #  Without exclude_unset=True, dumping it includes defaults for omitted fields, which could overwrite existing values. 
        for key, value in product_data.model_dump(exclude_unset=True).items():
            setattr(db_product, key, value)

        self.db.flush()
        self.db.refresh(db_product)
        return db_product

    def delete_product(self, product_id:int) -> None:
        db_product = self.get_product_by_id(product_id)
        if db_product is None:
            return None

        self.db.delete(db_product)
        self.db.flush()
        return db_product


    def get_filtered_products(self, name_seq: str | None, description_seq: str | None, min_price: float | None, max_price: float | None, active_status: bool | None, created_after: datetime | None, sort_by: str | None, page_size: int | None, page_no: int | None) -> list[Product]:
        query = self.db.query(Product)

        if name_seq:
            query = query.filter(Product.name.ilike(f"%{name_seq}%"))
        if description_seq:
            query = query.filter(Product.description.ilike(f"%{description_seq}%"))
        if min_price:
            query = query.filter(Product.price >= min_price)
        if max_price:
            query = query.filter(Product.price <= max_price)
        print(f"Filtered products: {len(query.all())}")
        print(f"active_status: {active_status}")
        if active_status is not None:
            query = query.filter(Product.is_active == active_status)
        print(f"Filtered products: {len(query.all())}")
        if created_after:
            query = query.filter(Product.created_at > created_after)
        
        # Sorting
        if sort_by:
            sort_column = getattr(Product, sort_by, None) # sort_column = Product.price
            query = query.order_by(sort_column)
        # Pagination
        if page_size and page_no:
            offset = (page_no - 1) * page_size
            query = query.offset(offset).limit(page_size)

        return query.all()

                              

    











from datetime import datetime

from app.models.product_model import Product
from app.repositories.product_repo import ProductRepo
from app.schemas.product_schema import ProductCreate, ProductUpdate


class ProductService:
    def __init__(self, repo : ProductRepo, db):
        self.repo = repo
        self.db = db

    def create_product(self, product_data: ProductCreate) -> Product:
        try:
            product = self.repo.create_product(product_data)
            self.db.commit()  # Commit the transaction to persist the changes in the database
            return product
        except Exception as e:
            self.db.rollback()  # Rollback the transaction in case of an error
            raise e  # Re-raise the exception to be handled by the caller

    def get_all_products(self) -> list[Product]:
        try:
            products_list= self.repo.get_all_products()
            self.db.commit()
            return products_list
        except Exception as e:
            self.db.rollback()
            raise e

    def get_product_by_id(self, product_id: int) -> Product | None:
        try:
            product = self.repo.get_product_by_id(product_id)
            self.db.commit()
            return product
        except Exception as e:
            self.db.rollback()
            raise e

    def put_product(self, product_id : int, product_data : ProductCreate) -> Product | None:
        try:
            product = self.repo.put_product(product_id, product_data)
            self.db.commit()
            return product
        except Exception as e:
            self.db.rollback()
            raise e

    def patch_product(self, product_id: int, product_data: ProductUpdate) -> Product | None:
        try:
            product = self.repo.patch_product(product_id, product_data)
            self.db.commit()
            return product
        except Exception as e:
            self.db.rollback()
            raise e

    def delete_product(self, product_id: int) -> Product | None:
        try:
            product = self.repo.delete_product(product_id)
            self.db.commit()
            return product
        except Exception as e:
            self.db.rollback()
            raise e

    def get_filtered_products(self, name_seq: str | None, description_seq: str | None, min_price: float | None, max_price: float | None, active_status: bool | None, created_after: datetime | None, sort_by: str | None, page_size: int | None, page_no: int | None) -> list[Product]:
        try:
            products_list = self.repo.get_filtered_products(name_seq, description_seq, min_price, max_price, active_status, created_after, sort_by, page_size, page_no)
            self.db.commit()
            return products_list
        except Exception as e:
            self.db.rollback()
            raise e














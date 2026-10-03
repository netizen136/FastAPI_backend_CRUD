
from app.models.product_model import Base
from sqlalchemy.orm import Mapped, mapped_column




class User(Base):
    """Database table for users."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(nullable=False, default="user")
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
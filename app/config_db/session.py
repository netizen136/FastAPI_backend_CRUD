from app.config_db.settings import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from collections.abc import Generator

# engine = database connection pool manager
# SessionLocal = factory for creating sessions
# db = SessionLocal() = one actual DB session object
# yield db = give that session to the endpoint for the request
# db.close() = free it when done


engine = create_engine(settings.database_url, echo=False, pool_pre_ping=True, connect_args={"connect_timeout": 2})  # Adjust the connect_timeout value as needed  

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, class_=Session)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



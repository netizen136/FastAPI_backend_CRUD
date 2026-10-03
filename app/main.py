from contextlib import asynccontextmanager
import threading
from app.config_db.settings import settings
from app.models.product_model import Base
from app.config_db.session import engine

from fastapi import FastAPI

from app.controllers.product_controller import router as productrouter
from app.controllers.user_controller import router as userrouter

# uvicorn app.main:app --reload

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run before the application starts
    print("Starting up the app... " + settings.app_name)

    try:
        def _create_all():
            try:
                # Base.metadata.create_all() = create tables if missing
                # engine = database connection manager
                Base.metadata.create_all(bind=engine)
                print("Database tables created successfully.")
            except Exception as e:
                print(f"Error creating database tables: {e}")

        # Without threading, app startup may be blocked if the db connection is unresponsive. 
        # By using a separate thread, the application can start up and respond to requests, 
        # even if the database connection takes time to establish.
        thread = threading.Thread(target=_create_all)
        thread.start()

    except Exception as e:
        print(f"Error during startup: {e}")


    yield  # Control is passed to the application

    # Code to run after the application shuts down
    print("Shutting down... " + settings.app_name)

app = FastAPI(
    title=settings.app_name,
    description="Learning-focused Product Management CRUD API with layered architecture.",
    version="1.0.0",
    lifespan=lifespan,
)

@app.get("/")
def health_check():
    return {"message": "Status is OK!"}

@app.get("/ping")
def health_check():
    return {"message": "10 ms pong!"}

app.include_router(productrouter, prefix="/api/v1")
app.include_router(userrouter, prefix="/api/v1")




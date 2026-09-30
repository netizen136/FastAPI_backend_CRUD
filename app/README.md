# Product Learning API

A small FastAPI CRUD service for products, using Pydantic for request/response validation, SQLAlchemy for persistence, and PostgreSQL.

## Run locally

1. Create and activate a virtual environment, then install dependencies:

   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   python -m pip install fastapi "uvicorn[standard]" sqlalchemy pydantic pydantic-settings "psycopg[binary]"
   ```

2. Configure `app/.env` with a working PostgreSQL connection:

   ```env
   APP_NAME=Product Learning API
   DATABASE_URL=postgresql+psycopg://username:password@localhost:5432/product_learning_db_3
   FRONTEND_ORIGIN=http://localhost:5174
   ```

   Create the database first. Do not commit real credentials.

3. From the project root, start the API:

   ```powershell
   python -m uvicorn app.main:app --reload
   ```

Interactive API docs: <http://127.0.0.1:8000/docs>

## Request flow

`main.py` registers the product router at `/api/v1`. The controller validates HTTP input, the service handles transaction commit/rollback, and the repository runs SQLAlchemy queries. Product rows use the `products_2` table; the app attempts to create it on startup.

## Product endpoints

Base path: `/api/v1/products`

| Operation | Method and path |
|---|---|
| Create | `POST /api/v1/products` |
| List | `GET /api/v1/products` |
| Read one | `GET /api/v1/products/{product_id}` |
| Replace | `PUT /api/v1/products/{product_id}` |
| Update fields | `PATCH /api/v1/products/{product_id}` |
| Delete | `DELETE /api/v1/products/{product_id}` |

There is also `GET /api/v1/products/filter`; see [ExtendedReadme.txt](ExtendedReadme.txt) for request examples, fields, and behavior.
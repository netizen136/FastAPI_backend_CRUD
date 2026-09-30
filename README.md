# Product Learning API

A small FastAPI CRUD service for products using SQLAlchemy, Pydantic, and PostgreSQL. The project is organized into layered components:

- `app/main.py` starts the FastAPI app
- `app/controllers/...` handles HTTP routes
- `app/services/...` executes business logic
- `app/repositories/...` reads and writes database records
- `app/schemas/...` validates request and response payloads

## Run locally

1. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```powershell
   python -m pip install fastapi "uvicorn[standard]" sqlalchemy pydantic pydantic-settings "psycopg[binary]"
   ```

3. Configure your database connection in `app/.env`:

   ```env
   APP_NAME=Product Learning API
   DATABASE_URL=postgresql+psycopg://username:password@localhost:5432/product_learning_db_3
   FRONTEND_ORIGIN=http://localhost:5174
   ```

   Create the PostgreSQL database first before starting the app.

4. Start the API:

   ```powershell
   python -m uvicorn app.main:app --reload
   ```

5. Open the automatic docs:

   - Swagger UI: http://127.0.0.1:8000/docs
   - ReDoc: http://127.0.0.1:8000/redoc

## App behavior and request flow

The app exposes endpoints under `/api/v1` and the product router is mounted at `/api/v1/products`.

The flow is:

1. Request enters the FastAPI route
2. Pydantic schema validates incoming JSON
3. Controller calls the service layer
4. Service calls the repository layer
5. SQLAlchemy updates or reads the database
6. A validated response model is returned to the client

The product table is created automatically on startup if it is missing.

## Health endpoints

### GET /

Returns a simple app status message.

Request:

```http
GET /
```

Response:

```json
{
  "message": "Status is OK!"
}
```

### GET /ping

Returns a lightweight health check message.

Request:

```http
GET /ping
```

Response:

```json
{
  "message": "10 ms pong!"
}
```

## Product endpoints

Base path: `/api/v1/products`

### Common validation rules

These rules are enforced by the schemas:

- `name`: 3 to 20 characters
- `description`: optional, max 200 characters
- `price`: greater than 0 and less than 10000
- `stock_quantity`: between 0 and 1000
- `is_active`: boolean
- `product_id`: must be a positive integer

### 1) Create a product

Method: `POST /api/v1/products`

Request example:

```http
POST /api/v1/products
Content-Type: application/json
```

```json
{
  "name": "Laptop",
  "description": "15-inch gaming laptop",
  "price": 1299.99,
  "stock_quantity": 12,
  "is_active": true
}
```

Response example (`201 Created`):

```json
{
  "id": 1,
  "name": "Laptop",
  "description": "15-inch gaming laptop",
  "price": 1299.99,
  "stock_quantity": 12,
  "is_active": true,
  "created_at": "2026-10-01T12:00:00",
  "updated_at": "2026-10-01T12:00:00"
}
```

### 2) Get all products

Method: `GET /api/v1/products`

Request:

```http
GET /api/v1/products
```

Response example (`200 OK`):

```json
[
  {
    "id": 1,
    "name": "Laptop",
    "description": "15-inch gaming laptop",
    "price": 1299.99,
    "stock_quantity": 12,
    "is_active": true,
    "created_at": "2026-10-01T12:00:00",
    "updated_at": "2026-10-01T12:00:00"
  },
  {
    "id": 2,
    "name": "Mouse",
    "description": "Wireless mouse",
    "price": 49.99,
    "stock_quantity": 35,
    "is_active": true,
    "created_at": "2026-10-01T12:05:00",
    "updated_at": "2026-10-01T12:05:00"
  }
]
```

### 3) Get one product by id

Method: `GET /api/v1/products/{product_id}`

Example:

```http
GET /api/v1/products/1
```

Response example (`200 OK`):

```json
{
  "id": 1,
  "name": "Laptop",
  "description": "15-inch gaming laptop",
  "price": 1299.99,
  "stock_quantity": 12,
  "is_active": true,
  "created_at": "2026-10-01T12:00:00",
  "updated_at": "2026-10-01T12:00:00"
}
```

### 4) Replace a product

Method: `PUT /api/v1/products/{product_id}`

This is a full update. All required fields must be sent again, even if they did not change.

Example request:

```http
PUT /api/v1/products/1
Content-Type: application/json
```

```json
{
  "name": "Gaming Laptop",
  "description": "Updated 15-inch gaming laptop",
  "price": 1499.99,
  "stock_quantity": 8,
  "is_active": true
}
```

Response example (`200 OK`):

```json
{
  "id": 1,
  "name": "Gaming Laptop",
  "description": "Updated 15-inch gaming laptop",
  "price": 1499.99,
  "stock_quantity": 8,
  "is_active": true,
  "created_at": "2026-10-01T12:00:00",
  "updated_at": "2026-10-01T12:20:00"
}
```

### 5) Update selected fields

Method: `PATCH /api/v1/products/{product_id}`

This performs a partial update. Only the fields included in the body are changed.

Example request:

```http
PATCH /api/v1/products/1
Content-Type: application/json
```

```json
{
  "price": 1399.99,
  "stock_quantity": 10
}
```

Response example (`200 OK`):

```json
{
  "id": 1,
  "name": "Gaming Laptop",
  "description": "Updated 15-inch gaming laptop",
  "price": 1399.99,
  "stock_quantity": 10,
  "is_active": true,
  "created_at": "2026-10-01T12:00:00",
  "updated_at": "2026-10-01T12:25:00"
}
```

### 6) Delete a product

Method: `DELETE /api/v1/products/{product_id}`

Example:

```http
DELETE /api/v1/products/1
```

Response: `204 No Content`

There is no JSON body on success.

### 7) Filter products

Method: `GET /api/v1/products/filter`

This endpoint supports filtering, sorting, and pagination.

Example request:

```http
GET /api/v1/products/filter?name_seq=lap&description_seq=gaming&min_price=500&max_price=2000&active_status=true&sort_by=price&page_size=10&page_no=1
```

Query parameters:

- `name_seq`: partial product name match
- `description_seq`: partial description match
- `min_price`: minimum allowed price
- `max_price`: maximum allowed price
- `active_status`: filter by active/inactive status
- `created_after`: filter by creation date
- `sort_by`: one of `id`, `name`, `price`, `stock_quantity`, `created_at`, `updated_at`
- `page_size`: number of items per page (5 to 20)
- `page_no`: page number (starting at 1)

Example response (`200 OK`):

```json
[
  {
    "id": 1,
    "name": "Laptop",
    "description": "15-inch gaming laptop",
    "price": 1299.99,
    "stock_quantity": 12,
    "is_active": true,
    "created_at": "2026-10-01T12:00:00",
    "updated_at": "2026-10-01T12:00:00"
  }
]
```

> Note: the `GET /api/v1/products/filter` route is registered before `GET /api/v1/products/{product_id}` to avoid the filter string being captured as an ID.

## Project structure

```text
app/
  main.py
  controllers/
  dependencies/
  models/
  repositories/
  schemas/
  services/
  config_db/
```

This project is a simple learning-oriented backend for product management and is intended to demonstrate clean FastAPI layering with database persistence.

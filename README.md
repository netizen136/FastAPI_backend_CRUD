# Product Learning API

A FastAPI product CRUD API backed by PostgreSQL and SQLAlchemy.

## Dependencies

Install the application dependencies in your Python environment:

```powershell
python -m pip install fastapi "uvicorn[standard]" sqlalchemy pydantic pydantic-settings "psycopg[binary]" PyJWT "pwdlib[argon2]" python-multipart
```

Configure `app/.env` with the database URL and required token settings:

```env
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@localhost:5432/DB_NAME
ACCESS_TOKEN_SECRET_KEY=<long-random-secret>
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Keep the signing secret private. The PostgreSQL database must exist before starting the API.

## Run

```powershell
python -m uvicorn app.main:app --reload
```

Interactive API docs: [Swagger UI](http://127.0.0.1:8000/docs) · [ReDoc](http://127.0.0.1:8000/redoc)

## Authentication

`POST /api/v1/login/createtoken` accepts `username` and `password` as form fields and returns a JWT for a valid active user. Send the token with protected requests as `Authorization: Bearer <access_token>`. In Swagger UI, use **Authorize**.

Only `PUT` and `PATCH /api/v1/products/{product_id}` currently require a valid, unexpired token. Other product operations are unauthenticated.

## Endpoints

### `GET /`

Health status. No input.

Response (`200 OK`):

```json
{
  "message": "Status is OK!"
}
```

### `GET /ping`

Health check. No input.

Response (`200 OK`):

```json
{
  "message": "10 ms pong!"
}
```

### `POST /api/v1/login/createtoken`

Log in with `application/x-www-form-urlencoded` fields (not JSON):

```text
username=user01&password=your-password
```

Response (`201 Created`):

```json
{
  "access_token": "<signed-jwt>",
  "token_type": "bearer"
}
```

Invalid credentials return `401 Unauthorized`.

### Product response shape

Successful product create, read, update, and filter results use this shape:

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

Product input rules: `name` is 3–20 characters; `description` is optional and up to 200 characters; `price` must be greater than 0 and less than 10000; `stock_quantity` must be 0–1000; `is_active` is a boolean (defaults to `true` on create).

### `POST /api/v1/products`

Create a product. No authentication required.

Request (`application/json`):

```json
{
  "name": "Laptop",
  "description": "15-inch gaming laptop",
  "price": 1299.99,
  "stock_quantity": 12,
  "is_active": true
}
```

Response: product response shape above (`201 Created`).

### `GET /api/v1/products`

List all products. No input or authentication required.

Response (`200 OK`):

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

An empty product table returns `[]`.

### `GET /api/v1/products/{product_id}`

Get one product by its ID. Example input: `/api/v1/products/1`. No authentication required.

Response (`200 OK`): one product using the product response shape above.

### `PUT /api/v1/products/{product_id}`

Replace all product fields. Requires a bearer token. Send the complete product body:

```http
PUT /api/v1/products/1
Authorization: Bearer <access_token>
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

Response (`200 OK`): the updated product using the product response shape above.

### `PATCH /api/v1/products/{product_id}`

Update selected product fields. Requires a bearer token. Include only fields to change:

```http
PATCH /api/v1/products/1
Authorization: Bearer <access_token>
Content-Type: application/json
```

```json
{
  "price": 1399.99,
  "stock_quantity": 10
}
```

Response (`200 OK`): the updated product using the product response shape above.

### `DELETE /api/v1/products/{product_id}`

Delete a product by ID. Example input: `/api/v1/products/1`. No authentication required.

Response: `204 No Content` with no response body.

### `GET /api/v1/products/filter`

Filter, sort, and paginate products. All parameters are optional; no authentication required.

Example input:

```http
GET /api/v1/products/filter?name_seq=lap&description_seq=gaming&min_price=500&max_price=2000&active_status=true&sort_by=price&page_size=10&page_no=1
```

| Query parameter | Purpose |
|---|---|
| `name_seq` | Partial name match (3–20 characters) |
| `description_seq` | Partial description match (3–200 characters) |
| `min_price` / `max_price` | Price range (1–9999) |
| `active_status` | Filter by active state (`true` or `false`) |
| `created_after` | Filter by creation timestamp |
| `sort_by` | `id`, `name`, `price`, `stock_quantity`, `created_at`, or `updated_at` |
| `page_size` | Results per page (5–20; default 8) |
| `page_no` | Page number (1–2000; default 1) |

Response (`200 OK`): an array of products using the product response shape above; no matches returns `[]`.

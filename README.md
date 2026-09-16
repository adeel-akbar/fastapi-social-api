# FastAPI Social API

A RESTful API for a social-media-style platform, built with FastAPI, PostgreSQL, and SQLAlchemy. Supports user registration, secure authentication, post ownership, likes, comments, and database migrations via Alembic.

## Features

- User registration with secure password hashing (Argon2 via `pwdlib`)
- JWT-based authentication with OAuth2 password flow
- Protected routes — posts, comments, and likes require a valid access token
- Full CRUD for posts, with ownership checks (only the owner can update/delete their own post)
- Full CRUD for comments, scoped to a post, with ownership checks
- Like system on posts, with likes count included in post responses via SQL joins
- Query parameters for post search and pagination (`search`, `limit`, `skip`)
- Database migrations managed with Alembic
- CORS enabled
- Auto-generated interactive API docs (Swagger UI / ReDoc)
- Postman collection included for manual testing

## Tech Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy 2.x
- **Migrations:** Alembic
- **Validation:** Pydantic / `pydantic-settings`
- **Auth:** JWT (PyJWT), OAuth2 Password Flow
- **Password Hashing:** pwdlib (Argon2)

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL running locally or remotely

### Installation

1. Clone the repository

```bash
   git clone https://github.com/adeel-akbar/fastapi-social-api
   cd fastapi-social-api
```

2. Create and activate a virtual environment

```bash
   python -m venv .venv
   .venv\Scripts\activate      # Windows
   source .venv/bin/activate   # macOS/Linux
```

3. Install dependencies

```bash
   pip install -r requirements.txt
```

4. Create a `.env` file in the project root with:

```text
   DB_HOST=localhost
   DB_PORT=5432
   DB_USER=<username>
   DB_PASSWORD=<password>
   DB_NAME=<database_name>
   SECRET_KEY=<your-secret-key>
   ALGORITHM=HS256
   TOKEN_EXPIRE_TIME=30
```

   Generate a secret key with:

```bash
   python -c "import secrets; print(secrets.token_hex(32))"
```

5. Apply database migrations

```bash
   alembic upgrade head
```

6. Run the app

```bash
   uvicorn app.main:app --reload
```

7. Open interactive docs at `http://127.0.0.1:8000/docs`

## API Overview

| Method| Endpoint                      | Description                          | Auth Required  |
|-------|------------------------------ |--------------------------------------|----------------|
| POST  | `/users/`                     | Register a new user                  | No             |
| GET   | `/users/`                     | List all users                       | Yes            |
| POST  | `/login`                      | Log in and receive access token      | No             |
| GET   | `/posts/`                     | List all posts (search, pagination)  | Yes            |
| POST  | `/posts/`                     | Create a new post                    | Yes            |
| GET   | `/posts/{id}`                 | Get a single post with vote count    | Yes            |
| PUT   | `/posts/{id}`                 | Update a post (owner only)           | Yes            |
| DELETE| `/posts/{id}`                 | Delete a post (owner only)           | Yes            |
| POST  | `/likes/`                     | Like or remove a like on a post      | Yes            |
| POST  | `/comments/{post_id}`         | Add a comment to a post              | Yes            |
| GET   | `/comments/{post_id}`         | Get all comments for a post          | Yes            |
| GET   |`/comments/single/{comment_id}`| Get a single comment                 | Yes            |
| PUT   |`/comments/single/{comment_id}`| Update a comment (owner only)        | Yes            |
| DELETE|`/comments/single/{comment_id}`| Delete a comment (owner only)        | Yes            |

Protected routes require an `Authorization: Bearer <token>` header, obtained from the `/login` endpoint.

## Postman

A Postman collection covering all endpoints is included in the `postman/` directory.

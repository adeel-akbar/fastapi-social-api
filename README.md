# FastAPI Social API

A RESTful API for a social-media-style platform, built with FastAPI, PostgreSQL, and SQLAlchemy. Supports user registration, secure authentication, and full CRUD operations on posts.

## Features

- User registration with secure password hashing (Argon2 via `pwdlib`)
- JWT-based authentication with OAuth2 password flow
- Protected routes — posts endpoints require a valid access token
- Full CRUD for posts (create, read, update, delete)
- Auto-generated interactive API docs (Swagger UI / ReDoc)
- Postman collection included for manual testing

## Tech Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy 2.x
- **Validation:** Pydantic
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
   URL=postgresql+psycopg://<username>:<password>@localhost:5432/<database_name>
   KEY=<your-secret-key>
   ```

   Generate a secret key with:

   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

5. Run the app

   ```bash
   uvicorn app.main:app --reload
   ```

6. Open interactive docs at `http://127.0.0.1:8000/docs`

## API Overview

| Method | Endpoint         | Description                     | Auth Required  |
|--------|------------------|-------------------------------  |--------------  |
| POST   | `/users/`        | Register a new user             | No             |
| GET    | `/users/`        | List all users                  | Yes            |
| POST   | `/login`         | Log in and receive access token | No             |
| GET    | `/posts/`        | List all posts                  | Yes            |
| POST   | `/posts/`        | Create a new post               | Yes            |
| GET    | `/posts/{id}`    | Get a single post               | Yes            |
| PUT    | `/posts/{id}`    | Update a post                   | Yes            |
| DELETE | `/posts/{id}`    | Delete a post                   | Yes            |

Protected routes require an `Authorization: Bearer <token>` header, obtained from the `/login` endpoint.

## Postman

A Postman collection covering all endpoints is included in the `postman/` directory.

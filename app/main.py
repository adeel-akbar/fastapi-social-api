from fastapi import FastAPI

from .routers import auth, posts, users

app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
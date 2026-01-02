from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.services.testBook.routes import book_router
from src.services.auth.routes import auth_router
from src.services.reviews.routes import review_router
from src.services.tags.routes import tags_router
from src.errors import register_all_errors
from src.middleware import register_middleware

@asynccontextmanager
async def life_span(app: FastAPI):
    print(f"Starting up server: {app}")
    await init_db()
    yield
    print(f"Shutting down server")

version = "v1"
app = FastAPI(
    version= version,
    title="Book Library",
    description="A REST API for book library",
    lifespan=life_span
)

version_prefix =f"/api/{version}"

register_all_errors(app)
register_middleware(app)

app.include_router(book_router, prefix=f"{version_prefix}/books", tags=['books'])
app.include_router(auth_router, prefix=f"{version_prefix}/auth", tags=['auth'])
app.include_router(review_router, prefix=f"{version_prefix}/reviews", tags=['reviews'])
app.include_router(tags_router, prefix=f"{version_prefix}/tags", tags=["tags"])

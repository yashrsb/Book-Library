from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from src.services.testBook.schemas import Book, BookUpdateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import Book
from src.db.main import get_session
from src.services.testBook.service import BookService
from .schemas import BookCreateModel, BookUpdateModel, BookDetailModel
from typing import List
from src.services.auth.dependencies import AccessTokenBearer, RoleChecker
from src.errors import (
    BookNotFound,
)

book_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(["admin", "user"]))


@book_router.get("/", response_model=List[Book], dependencies=[role_checker])
async def get_all_books(
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    books = await book_service.get_all_books(session)
    return books

@book_router.get("/user/{user_uid}", response_model=List[Book], dependencies=[role_checker])
async def get_user_books_submissions(
    user_uid: str,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    books = await book_service.get_user_books(user_uid, session)
    return books


@book_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Book,
    dependencies=[role_checker],
)
async def create_a_book(
    book_data: BookCreateModel,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
) -> dict:
    user_id = token_details.get("user")["user_id"]
    new_book = await book_service.create_book(book_data, user_id, session)
    return new_book


@book_router.get("/{book_uid}", response_model=BookDetailModel, dependencies=[role_checker])
async def get_a_book(
    book_uid: str,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
) -> dict:
    get_book = await book_service.get_book(book_uid, session)
    if get_book:
        return get_book
    else:
        raise BookNotFound()


@book_router.patch(
    "/{book_uid}", response_model=BookUpdateModel, dependencies=[role_checker]
)
async def update_a_book(
    book_uid: str,
    book_data: BookUpdateModel,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
) -> str:
    update_book = await book_service.update_book(book_uid, book_data, session)
    if update_book:
        return update_book
    else:
        raise BookNotFound()


@book_router.delete("/{book_uid}", dependencies=[role_checker])
async def delete_a_book(
    book_uid: str,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
) -> str:
    book_delete = await book_service.delete_book(book_uid, session)
    if book_delete is None:
        raise BookNotFound()
    else:
        return {}

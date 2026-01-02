from fastapi import APIRouter, Depends
from src.db.models import User
from src.db.main import get_session
from src.services.auth.dependencies import get_current_user
from src.services.reviews.schemas import ReviewCreateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from src.services.reviews.service import ReviewService

review_router = APIRouter()
review_service = ReviewService()


@review_router.post("/book/{book_uid}")
async def add_review_to_book(
    book_uid: str,
    review_Data: ReviewCreateModel,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    print('checking use email: ', current_user.email)
    new_review = await review_service.add_review_to_book(
        user_email = current_user.email, book_uid = book_uid, review_data = review_Data, session = session
    )
    return new_review
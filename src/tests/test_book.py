book_prefix = f"api/v1/books"

def test_get_all_books(test_client, fake_book_service, fake_session):
    response = test_client.get(
        url = f"{book_prefix}"
    )
    asser fake_book_service.get_all_books_once()
     asser fake_book_service.get_all_books_once_with(fake_session)
from fastapi.testclient import TestClient
from pydantic import parse_obj_as, BaseModel

from main import app


class BookModel(BaseModel):
    id: int
    title: str
    pages: int
    author_id: int


class BearerTokenTestClient(TestClient):
    def __init__(self, *args, **kwargs):
        self.bearer_token = kwargs.pop('bearer_token', None)
        super().__init__(*args, **kwargs)

    def request(self, *args, **kwargs):
        if self.bearer_token:
            kwargs.setdefault('headers', {}).update({
                'Authorization': f'Bearer {self.bearer_token}'
            })
        return super().request(*args, **kwargs)


client = TestClient(app)

apiInstance = BearerTokenTestClient(
    app, bearer_token=client.post(
        "/login",
        data={"username": "admin", "password": "password"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    ).json()['access_token']
)

MY_NAME = "Antero"
global_test_author_id: int = None
global_test_updated_author_id: int = 2
global_test_book_id: int = None
global_test_book_title: str = 'BOOK'
global_test_updated_title: str = 'KOOB'
global_test_book_pages: int = 701
global_test_updated_pages: int = 1994


def test_create_book():
    global global_test_author_id, global_test_book_id
    new_author_response = apiInstance.post(
        "/authors",
        headers={"Content-Type": "application/json"},
        json={"name": MY_NAME},
    )
    assert new_author_response.status_code == 200
    new_author = new_author_response.json()
    global_test_author_id = new_author['id']

    new_book_response = apiInstance.post(
        "/books/",
        headers={"Content-Type": "application/json"},
        json={
            "title": global_test_book_title,
            "pages": global_test_book_pages,
            "author_id": new_author['id']
        },
    )

    assert new_book_response.status_code == 200
    new_book = new_book_response.json()

    assert "id" in new_book
    assert isinstance(new_book["id"], int)
    assert new_book["id"] > 0
    global_test_book_id = new_book["id"]
    assert "title" in new_book
    assert isinstance(new_book["title"], str)
    assert new_book["title"] == global_test_book_title
    assert "pages" in new_book
    assert isinstance(new_book["pages"], int)
    assert new_book["pages"] == global_test_book_pages
    assert "author_id" in new_book
    assert isinstance(new_book["author_id"], int)
    assert new_book["author_id"] == global_test_author_id


def test_get_book():
    all_books = apiInstance.get(
        "/books",
        headers={"Content-Type": "application/json"},
    )
    assert all_books.status_code == 200

    assert isinstance(all_books.json(), list)
    for author in all_books.json():
        assert "id" in author
        assert isinstance(author["id"], int)
        assert "title" in author
        assert isinstance(author["title"], str)
        assert "pages" in author
        assert isinstance(author["pages"], int)
        assert "author_id" in author
        assert isinstance(author["author_id"], int)


def test_get_book():
    book_response = apiInstance.get(
        f"/books/{global_test_book_id}",
        headers={"Content-Type": "application/json"}
    )

    assert book_response.status_code == 200
    book = book_response.json()
    assert "id" in book
    assert isinstance(book["id"], int)
    assert book["id"] == global_test_book_id
    assert "title" in book
    assert isinstance(book["title"], str)
    assert book["title"] == global_test_book_title
    assert "pages" in book
    assert isinstance(book["pages"], int)
    assert book["pages"] == global_test_book_pages
    assert "author_id" in book
    assert isinstance(book["author_id"], int)
    assert book["author_id"] == global_test_author_id


def test_update_book():
    updated_book_response = apiInstance.put(
        f"/books/{global_test_book_id}",
        headers={"Content-Type": "application/json"},
        json={
            "title": global_test_updated_title,
            "pages": global_test_updated_pages,
            "author_id": global_test_updated_author_id
        },
    )
    assert updated_book_response.status_code == 200
    updated_book = updated_book_response.json()
    assert isinstance(updated_book, dict)
    assert "id" in updated_book
    assert isinstance(updated_book["id"], int)
    assert updated_book["id"] == global_test_book_id
    assert "title" in updated_book
    assert isinstance(updated_book["title"], str)
    assert updated_book["title"] == global_test_updated_title
    assert "pages" in updated_book
    assert isinstance(updated_book["pages"], int)
    assert updated_book["pages"] == global_test_updated_pages
    assert "author_id" in updated_book
    assert isinstance(updated_book["author_id"], int)
    assert updated_book["author_id"] == global_test_updated_author_id


def test_delete_book():
    deleted_author_response = apiInstance.delete(
        f"/books/{global_test_book_id}",
        headers={"Content-Type": "application/json"},
    )
    assert deleted_author_response.status_code == 204

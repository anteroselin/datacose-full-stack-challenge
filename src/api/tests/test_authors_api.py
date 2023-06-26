from fastapi.testclient import TestClient
from pydantic import parse_obj_as, BaseModel

from main import app


class AuthorModel(BaseModel):
    id: int
    name: str
    books: list


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
UPDATED_NAME = "Antero Selin"
global_test_author_id: int = None


def test_create_author():
    global global_test_author_id
    request_books = [{"title": "book1", "pages": 50, "author_id": -1}]
    new_author_response = apiInstance.post(
        "/authors",
        headers={"Content-Type": "application/json"},
        json={"name": MY_NAME},
    )
    assert new_author_response.status_code == 200
    new_author = new_author_response.json()
    assert isinstance(new_author, dict)
    author = parse_obj_as(AuthorModel, new_author)
    assert author.id > 0
    global_test_author_id = author.id
    assert author.name == MY_NAME
    for i, book in enumerate(author.books):
        assert book['title'] == request_books[i]["title"]
        assert book['pages'] == request_books[i]["pages"]
        assert book['author_id'] == author.id


def test_get_authors():
    all_authors_response = apiInstance.get(
        "/authors",
        headers={"Content-Type": "application/json"},
    )
    assert all_authors_response.status_code == 200
    all_authors = all_authors_response.json()
    assert isinstance(all_authors, list)
    for author in all_authors:
        assert "id" in author
        assert isinstance(author["id"], int)
        assert "name" in author
        assert isinstance(author["name"], str)


def test_get_author():
    author_response = apiInstance.get(
        f"/authors/{global_test_author_id}",
        headers={"Content-Type": "application/json"}
    )

    assert author_response.status_code == 200
    author = author_response.json()
    assert "id" in author
    assert isinstance(author["id"], int)
    assert author["id"] == global_test_author_id
    assert "name" in author
    assert isinstance(author["name"], str)
    assert author["name"] == MY_NAME


def test_update_author():
    updated_author_response = apiInstance.put(
        f"/authors/{global_test_author_id}",
        headers={"Content-Type": "application/json"},
        json={"name": UPDATED_NAME},
    )
    assert updated_author_response.status_code == 200
    updated_author = updated_author_response.json()
    assert isinstance(updated_author, dict)
    assert "id" in updated_author
    assert isinstance(updated_author["id"], int)
    assert updated_author["id"] == global_test_author_id
    assert "name" in updated_author
    assert isinstance(updated_author["name"], str)
    assert updated_author["name"] == UPDATED_NAME


def test_delete_author():
    deleted_author_response = apiInstance.delete(
        f"/authors/{global_test_author_id}",
        headers={"Content-Type": "application/json"},
    )
    assert deleted_author_response.status_code == 204

from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from typing import List

from db.models.book import Book
from db.models.author import Author
from db.schemas.book import BookBase, BookWithAuthor


class BookRepository:
    def __init__(self: Session, db: Session):
        self = db

    def get_book(self: Session, book_id: int) -> BookWithAuthor:
        book = self.query(Book).join(Author, Book.author_id ==
                                     Author.id).filter(Book.id == book_id).first()
        if book:
            return {
                "id": book.id,
                "title": book.title,
                "pages": book.pages,
                "author_id": book.author_id,
                "author_name": book.author.name,
            }

    def get_books(self: Session) -> List[BookWithAuthor]:
        books = self.query(Book).join(
            Author, Book.author_id == Author.id).order_by(Book.id.desc()).all()
        book_list = []
        for book in books:
            book_data = {
                "id": book.id,
                "title": book.title,
                "pages": book.pages,
                "author_id": book.author_id,
                "author_name": book.author.name,
            }
            book_list.append(book_data)
        return book_list

    def create_book(self: Session, book: BookBase):
        db_book = Book(
            title=book.title,
            pages=book.pages,
            author_id=book.author_id
        )
        self.add(db_book)
        self.commit()
        self.refresh(db_book)
        return db_book

    def update_book(self: Session, book_id: int, book_update: BookBase):
        book: Book = self.query(Book).filter(Book.id == book_id).first()
        if book:
            book.title = book_update.title
            book.pages = book_update.pages
            book.author_id = book_update.author_id
            self.commit()
            self.refresh(book)
            return book

    def delete_book(self: Session, book_id: int):
        book = self.query(Book).filter(Book.id == book_id).first()
        if book:
            self.delete(book)
            self.commit()
            return True

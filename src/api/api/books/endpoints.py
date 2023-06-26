from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.schemas import BookWithAuthor, User, BookBase, Book
from db.repositories import BookRepository
from db.session import get_db
from api.auth.utils import get_current_user

router = APIRouter()


@router.get('/books', response_model=List[BookWithAuthor])
def get_books(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    books = BookRepository.get_books(db)
    return books


@router.get('/books/{book_id}', response_model=BookWithAuthor)
def get_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    book = BookRepository.get_book(db, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Book not found'
        )
    return book


@router.post('/books', response_model=Book)
def create_book(
    book: BookBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_book = BookRepository.create_book(db, book)
    return new_book


@router.put('/books/{book_id}', response_model=Book)
def update_book(
    book_id: int,
    book: BookBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated_book = BookRepository.update_book(db, book_id, book)
    if not updated_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Book not found'
        )
    return updated_book


@router.delete('/books/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deleted = BookRepository.delete_book(db, book_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Book not found'
        )



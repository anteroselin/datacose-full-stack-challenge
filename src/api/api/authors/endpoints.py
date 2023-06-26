from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.schemas import User, Author, AuthorBase
from db.repositories import AuthorRepository
from db.session import get_db
from api.auth.utils import get_current_user

router = APIRouter()


@router.get('/authors', response_model=List[Author])
def get_authors(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    authors = AuthorRepository.get_authors(db)
    return authors


@router.get('/authors/{author_id}', response_model=Author)
def get_author(
    author_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    author = AuthorRepository.get_author(db, author_id=author_id)
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Author not found',
        )
    return author


@router.post('/authors', response_model=Author)
def create_author(
    author: AuthorBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_author = AuthorRepository.create_author(db, author)
    return new_author


@router.put('/authors/{author_id}', response_model=Author)
def update_author(
    author_id: int,
    author: AuthorBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    updated_author = AuthorRepository.update_author(db, author_id, author)
    if not updated_author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Author not found',
        )
    return updated_author


@router.delete('/authors/{author_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_author(
    author_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted = AuthorRepository.delete_author(db, author_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Author not found',
        )

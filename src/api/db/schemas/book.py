from pydantic import BaseModel

class BookBase(BaseModel):
    title: str
    pages: int
    author_id: int

class BookCreate(BookBase):
    pass

class BookWithAuthor(BookBase) :
    id: int
    author_name: str    

class Book(BookBase):
    id: int
    class Config:
        orm_mode = True

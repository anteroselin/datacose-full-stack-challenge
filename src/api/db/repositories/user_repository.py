from sqlalchemy.orm import Session

from db.models.user import User
from db.schemas.user import UserCreate


class UserRepository:
    def __init__(self: Session, db: Session):
        self = db

    def get_user_by_id(self: Session, user_id: int):
        return self.query(User).filter(User.id == user_id).first()

    def get_user_by_username(self: Session, username: str):
        return self.query(User).filter(User.username == username).first()

    def create_user(self: Session, user: UserCreate):
        db_user = User(username=user.username, password=user.password)
        self.add(db_user)
        self.commit()
        self.refresh(db_user)
        return db_user

    def delete_user(self: Session, user: User):
        self.delete(user)
        self.commit()

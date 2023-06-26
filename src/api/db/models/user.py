from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates

from db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    @validates('username')
    def validate_username(self, key, username):
        # Implement any additional validation logic for the username if needed
        # For example, you can ensure that the username meets certain criteria
        return username

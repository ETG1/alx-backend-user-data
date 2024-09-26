#!/usr/bin/env python3
"""
This module contains the SQLAlchemy User model for the 'users' table.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    Represents a user for a MySQL database.

    Attributes:
        id (int): The user's unique identifier and primary key.
        email (str): The user's email, which is non-nullable.
        hashed_password (str): The user's password after hashing,
        which is non-nullable.
        session_id (str): The session ID associated with the user,
        which is nullable.
        reset_token (str): A token to reset the user's password,
        which is nullable.
    """
    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True)
    email: str = Column(String(255), nullable=False)
    hashed_password: str = Column(String(255), nullable=False)
    session_id: str = Column(String(255), nullable=True)
    reset_token: str = Column(String(255), nullable=True)

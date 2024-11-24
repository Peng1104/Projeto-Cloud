"""
db_models.py - Define os modelos de dados do banco de dados
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

BASE = declarative_base()


class User(BASE): # pylint: disable=too-few-public-methods
    """
    Represents a user in the database.

    Attributes:
        id (int): The primary key of the user.
        nome (str): The name of the user. Cannot be null.
        email (str): The unique email of the user. Cannot be null.
        senha (str): The password of the user. Cannot be null.
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)

"""
app_models.py is a module that contains Pydantic models for the FastAPI application.
"""

from pydantic import BaseModel


class UserCreate(BaseModel):
    """
    UserCreate is a Pydantic model used for creating a new user.

    Attributes:
        nome (str): The name of the user.
        email (str): The email address of the user.
        senha (str): The password of the user.
    """
    nome: str
    email: str
    senha: str


class UserLogin(BaseModel):
    """
    UserLogin model for user login information.

    Attributes:
        nome (str): The name of the user.
        email (str): The email address of the user.
    """
    email: str
    senha: str


class Token(BaseModel):
    """
    Token model representing a JSON Web Token (JWT).

    Attributes:
        jwt (str): The JSON Web Token as a string.
    """
    jwt: str

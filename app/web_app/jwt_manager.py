"""
This module provides functions to encode and validate JWT tokens.
Functions:
    encode(email: str) -> str:
        Encodes the given email into a JWT token.
    validate(token: str | None) -> None:
        Validates the given JWT token.
"""

import os
from datetime import datetime, timedelta, timezone
from jose import jwt, ExpiredSignatureError, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

__SECURITY = HTTPBearer()
__JWT_SECRET = os.getenv("JWT_SECRET")
__JWT_ALGORITHM = "HS256"


def encode(email: str) -> str:
    """
    Encodes the given email into a JWT token.
    Args:
        email (str): The email to be encoded into the JWT token.
    Returns:
        str: The encoded JWT token as a string.
    """
    return jwt.encode(
        {"sub": email, "exp": datetime.now(timezone.utc) + timedelta(hours=1)},
        __JWT_SECRET,
        algorithm=__JWT_ALGORITHM
    )


async def validate_token(
    credentials: HTTPAuthorizationCredentials = Depends(__SECURITY)
) -> dict[str, any]:
    """
    Validates the provided JWT token.
    Args:
        credentials (HTTPAuthorizationCredentials): The HTTP authorization credentials.
    Returns:
        dict: The decoded token payload if the token is valid.
    Raises:
        HTTPException: If the token is invalid or expired.
    """
    try:
        return jwt.decode(credentials.credentials,
                          __JWT_SECRET, algorithms=[__JWT_ALGORITHM])
    except ExpiredSignatureError as exc:
        raise HTTPException(status_code=403, detail="Token expirado.") from exc
    except JWTError as exc:
        raise HTTPException(status_code=403, detail="Token inválido.") from exc

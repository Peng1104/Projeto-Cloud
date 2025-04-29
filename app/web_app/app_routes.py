"""
Este módulo cria as rotas da API FastAPI para manipular usuários.

Funções:
    registrar(user: UserCreate, db: AsyncSession = Depends(db)) -> Token:
        Registra um novo usuário no banco de dados.
    
    login(user: UserLogin, db: AsyncSession = Depends(db)) -> Token:
        Lida com o login do usuário, verificando as credenciais e gerando um token JWT.

    consultar(token: str = Depends()) -> dict:
        Consulta um recurso protegido usando um token JWT.

Variáveis:
    ROUTER (APIRouter): Roteador FastAPI para manipular as rotas da API.
"""

from passlib.context import CryptContext
from fastapi import HTTPException, Depends, APIRouter
from fastapi.responses import HTMLResponse
from socket import gethostname
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from web_app.db_models import User
from web_app.db_manager import get_database
from web_app.app_models import UserCreate, UserLogin, Token
from web_app.jwt_manager import encode, validate_token
from web_app.grepolis_data import get_players_data

__PWD_CRYPT = CryptContext(schemes=["sha512_crypt"], deprecated="auto")

ROUTER = APIRouter()


@ROUTER.post("/registrar", response_model=Token)
async def registrar(user: UserCreate, db: AsyncSession = Depends(get_database)) -> Token:
    """
    Registers a new user in the system.
    Args:
        user (UserCreate): The user information to be registered.
        db (AsyncSession, optional): The database session dependency. Defaults to Depends(db).
    Raises:
        HTTPException: If the email is already registered.
        HTTPException: If the username is already taken.
    Returns:
        Token: The JWT token for the registered user.
    """
    if (await db.execute(select(User).where(User.email == user.email))).scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email já registrado")

    if (await db.execute(select(User).where(User.nome == user.nome))).scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Nome indisponível")

    db.add(User(nome=user.nome, email=user.email,
           senha=__PWD_CRYPT.hash(user.senha)))

    await db.commit()

    return Token(jwt=encode(user.email))


@ROUTER.post("/login", response_model=Token)
async def login(user: UserLogin, db: AsyncSession = Depends(get_database)) -> Token:
    """
    Handles user login by verifying credentials and generating a JWT token.
    Args:
        user (UserLogin): The user login data containing email and password.
        db (AsyncSession, optional): The database session dependency. Defaults to Depends(db).
    Returns:
        Token: A JWT token if the login is successful.
    Raises:
        HTTPException: If the credentials are invalid, raises a 401 HTTP exception.
    """
    db_user = (await db.execute(select(User).where(User.email == user.email))).scalar_one_or_none()

    if not db_user or not __PWD_CRYPT.verify(user.senha, db_user.senha):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    return Token(jwt=encode(user.email))


@ROUTER.get("/consultar")
async def consultar(payload: dict = Depends(validate_token)) -> HTMLResponse:  # pylint: disable=unused-argument
    """
    Asynchronous function to validate a token and return a success message.
    Args:
        token (str): The token to be validated. This is provided by the Depends() dependency.
    Returns:
        str: Contains the Grepolis player data in HTML format.
    Raises:
        HTTPException: If the token is invalid, raises a 403 HTTP exception.
    """

    return HTMLResponse(content=f"""
    <html>
        <head>
            <title>Grepolis Player Data</title>
        </head>
        <body>
            <h1>Grepolis Data</h1>
            {get_players_data().to_html()}
        </body>
    </html>
    """)


@ROUTER.get("/health-check", status_code=200)
async def health_check():
    """
    Health check endpoint to verify the status of the server.
    Returns:
        dict: A dictionary containing the hostname of the server.
    """
    return {"server_hostname": gethostname()}

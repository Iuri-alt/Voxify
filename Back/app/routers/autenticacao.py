from collections import defaultdict, deque
from time import monotonic

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.security import verificar_senha
from app.auth import criar_token

router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"]
)

MAX_LOGIN_ATTEMPTS = 5
LOGIN_WINDOW_SECONDS = 15 * 60
tentativas_login: dict[str, deque[float]] = defaultdict(deque)

def verificar_limite_login(chave: str) -> None:
    agora = monotonic()
    tentativas = tentativas_login[chave]
    while tentativas and agora - tentativas[0] > LOGIN_WINDOW_SECONDS:
        tentativas.popleft()
    if len(tentativas) >= MAX_LOGIN_ATTEMPTS:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Muitas tentativas. Aguarde alguns minutos.")
    tentativas.append(agora)

@router.post("/login")
def login(
        dados: schemas.UserLogin,
        request: Request,
        db: Session = Depends(get_db),
):
    verificar_limite_login(request.client.host if request.client else "desconhecido")
    usuario = db.query(models.User).filter(
        models.User.email == str(dados.email).lower()
    ).first()
    if usuario is None or not verificar_senha(dados.senha, usuario.senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha inválidos."
        )
    tentativas_login.pop(request.client.host if request.client else "desconhecido", None)
    token = criar_token(
        {
            "sub": usuario.email,
            "id": usuario.id
        }
    )
    return{
        "access_token": token,
        "token_type": "Bearer",
    }

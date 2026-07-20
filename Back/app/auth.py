from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from jose.exceptions import JWTError
from sqlalchemy.orm import Session

from app import models
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES, JWT_ALGORITHM, get_jwt_secret_key
from app.database import get_db

bearer_scheme = HTTPBearer(auto_error=False)

def criar_token(dados: dict) -> str:
    payload = dados.copy()
    payload.update({
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        "iat": datetime.now(timezone.utc),
        "type": "access",
    })
    return jwt.encode(payload, get_jwt_secret_key(), algorithm=JWT_ALGORITHM)

def obter_usuario_atual(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> models.User:
    invalid = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sessão inválida ou expirada.")
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise invalid
    
    try:
        payload = jwt.decode(
            credentials.credentials,
            get_jwt_secret_key(),
            algorithms=[JWT_ALGORITHM],
        )
        print("TOKEN PAYLOAD:", payload)

        usuario_id = payload.get("id")
        token_type = payload.get("type")

    except JWTError as error:
        print("JWT ERROR:", error)
        raise invalid

    if not isinstance(usuario_id, int) or token_type != "access":
        raise invalid
    usuario = db.get(models.User, usuario_id)
    if usuario is None:
        raise invalid
    print("USUÁRIO:", usuario)
    return usuario

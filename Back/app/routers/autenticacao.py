from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.security import verificar_senha
from app.auth import criar_token
from app.rate_limit import RateLimiter, ip_do_cliente

router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"]
)

limitador_login = RateLimiter(max_tentativas=5, janela_segundos=15 * 60)

@router.post("/login")
def login(
        dados: schemas.UserLogin,
        request: Request,
        db: Session = Depends(get_db),
):
    chave = ip_do_cliente(request)
    limitador_login.verificar(chave)
    usuario = db.query(models.User).filter(
        models.User.email == str(dados.email).lower()
    ).first()
    if usuario is None or not verificar_senha(dados.senha, usuario.senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha inválidos."
        )
    limitador_login.limpar(chave)
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

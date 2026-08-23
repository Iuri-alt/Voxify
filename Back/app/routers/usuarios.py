from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import models, schemas
from app.auth import obter_usuario_atual
from app.database import get_db
from app.rate_limit import RateLimiter, ip_do_cliente
from app.security import gerar_hash

router = APIRouter(prefix="/users", tags=["Usuários"])

limitador_cadastro = RateLimiter(max_tentativas=5, janela_segundos=15 * 60)

@router.post("/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def criar_usuario(usuario: schemas.UserCreate, request: Request, db: Session = Depends(get_db)):
    limitador_cadastro.verificar(ip_do_cliente(request))
    novo_usuario = models.User(
        nome=usuario.nome,
        email=str(usuario.email).lower(),
        senha=gerar_hash(usuario.senha),
    )
    db.add(novo_usuario)
    try:
        db.commit()
    except IntegrityError as error:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Não foi possível criar esta conta.") from error
    db.refresh(novo_usuario)
    return novo_usuario

@router.get("/me", response_model=schemas.UserResponse)
def buscar_perfil(usuario: models.User = Depends(obter_usuario_atual)):
    return usuario

@router.put("/me", response_model=schemas.UserResponse)
def atualizar_perfil(
    dados: schemas.UserUpdate,
    db: Session = Depends(get_db),
    usuario: models.User = Depends(obter_usuario_atual),
):
    usuario.nome = dados.nome
    usuario.email = str(dados.email).lower()
    try:
        db.commit()
    except IntegrityError as error:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Não foi possível atualizar este perfil.") from error
    db.refresh(usuario)
    return usuario

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def deletar_perfil(
    db: Session = Depends(get_db),
    usuario: models.User = Depends(obter_usuario_atual),
):
    db.delete(usuario)
    db.commit()

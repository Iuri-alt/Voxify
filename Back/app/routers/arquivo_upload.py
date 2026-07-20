from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from Back.app.services.upload_audio import upload_audio
from Back.app.services.transcription_service import transcrever_audio
from app.auth import obter_usuario_atual

router = APIRouter(
    prefix="/arquivos",
    tags=["arquivos"]
)

MAX_FILE_SIZE = 100 * 1024 * 1024
FORMATOS_AUDIO = {
    "audio/mpeg": (".mp3",),
    "audio/wav": (".wav",),
    "audio/x-wav": (".wav",),
    "audio/x-m4a": (".m4a",),
    "audio/mp4": (".m4a",),
}

def validar_audio(arquivo: UploadFile) -> str:
    if not arquivo.filename or arquivo.content_type not in FORMATOS_AUDIO:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Formato inválido. Use MP3, WAV ou M4A.")
    nome = Path(arquivo.filename).name
    if Path(nome).suffix.lower() not in FORMATOS_AUDIO[arquivo.content_type]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A extensão não corresponde ao tipo do arquivo.")
    arquivo.file.seek(0, 2)
    tamanho = arquivo.file.tell()
    arquivo.file.seek(0)
    if tamanho == 0 or tamanho > MAX_FILE_SIZE:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="O arquivo deve ter entre 1 byte e 100 MB.")
    cabecalho = arquivo.file.read(12)
    arquivo.file.seek(0)
    assinatura_valida = (
        (arquivo.content_type == "audio/mpeg" and (cabecalho.startswith(b"ID3") or cabecalho[:2] == b"\xff\xfb"))
        or (arquivo.content_type in {"audio/wav", "audio/x-wav"} and cabecalho.startswith(b"RIFF") and cabecalho[8:12] == b"WAVE")
        or (arquivo.content_type in {"audio/x-m4a", "audio/mp4"} and cabecalho[4:8] == b"ftyp")
    )
    if not assinatura_valida:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="O conteúdo não corresponde a um áudio válido.")
    return nome

@router.get("/", response_model=list[schemas.ArquivoResponse])
def listar_arquivos(
        db: Session = Depends(get_db),
        usuario: models.User = Depends(obter_usuario_atual),
):
    return db.query(models.Arquivo).filter(models.Arquivo.usuario_id == usuario.id).all()

@router.get("/{arquivo_id}", response_model=schemas.ArquivoResponse)
def buscar_arquivo(
        arquivo_id: int,
        db: Session = Depends(get_db),
        usuario: models.User = Depends(obter_usuario_atual),
):
    arquivo = db.query(models.Arquivo).filter(
        models.Arquivo.id == arquivo_id,
        models.Arquivo.usuario_id == usuario.id,
    ).first()
    if arquivo is None:
        raise HTTPException(
            status_code=404,
            detail="Arquivos não encontrado"
        )
    return arquivo

@router.get("/{arquivo_id}/transcricao", response_model=schemas.TranscricaoResponse)
def buscar_transcricao(
    arquivo_id: int,
    db: Session = Depends(get_db),
    usuario: models.User = Depends(obter_usuario_atual),
):
    arquivo = db.query(models.Arquivo).filter(
        models.Arquivo.id == arquivo_id,
        models.Arquivo.usuario_id == usuario.id,
    ).first()
    if arquivo is None:
        raise HTTPException(status_code=404, detail="Arquivo não encontrado.")
    transcricao = db.query(models.Transcricao).filter(
        models.Transcricao.arquivo_id == arquivo_id
    ).order_by(models.Transcricao.data_criacao.desc()).first()
    if transcricao is None:
        raise HTTPException(status_code=404, detail="Transcrição ainda não disponível.")
    return transcricao

@router.delete("/{arquivo_id}")
def deletar_arquivo(
    arquivo_id: int,
    db: Session = Depends(get_db),
    usuario: models.User = Depends(obter_usuario_atual),
):
    arquivo = db.query(models.Arquivo).filter(
        models.Arquivo.id == arquivo_id,
        models.Arquivo.usuario_id == usuario.id,
    ).first()
    if arquivo is None:
        raise HTTPException(
            status_code=404,
            detail="Arquivo não encontrado."
        )
    db.delete(arquivo)
    db.commit()
    return {
        "mensagem": "Arquivo removido com sucesso."
    }

@router.post("/upload", response_model=schemas.ArquivoUploadResponse)
def upload_arquivo(
        arquivo: UploadFile = File(...),
        db: Session = Depends(get_db),
        usuario: models.User = Depends(obter_usuario_atual),
):
    nome_arquivo = validar_audio(arquivo)
    try:
        url = upload_audio(arquivo)
        arquivo.file.seek(0)
        texto = transcrever_audio(arquivo)
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Não foi possível processar o áudio agora.") from error
    novo_arquivo = models.Arquivo(
        usuario_id=usuario.id,
        nome_do_audio=nome_arquivo,
        url_audio=url,
        tipo_arquivo=arquivo.content_type,
        status="enviado"
    )
    db.add(novo_arquivo)
    db.commit()
    db.refresh(novo_arquivo)

    nova_transcricao = models.Transcricao(
        arquivo_id=novo_arquivo.id,
        texto=texto,
        idioma="pt"
    )
    db.add(nova_transcricao)
    db.commit()

    return {**schemas.ArquivoResponse.model_validate(novo_arquivo).model_dump(), "texto": texto}

import os

from fastapi import HTTPException, UploadFile

EXTENSOES_PERMITIDAS = {
    ".mp3",
    ".wav",
    ".m4a",
    ".ogg",
    ".webm",
    ".flac",
    ".aac",
}
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB
def validar_audio(arquivo: UploadFile):
    if not arquivo.filename:
        raise HTTPException(
            status_code=400,
            detail="Arquivo inválido."
        )

    extensao = os.path.splitext(arquivo.filename)[1].lower()

    if extensao not in EXTENSOES_PERMITIDAS:
        raise HTTPException(
            status_code=400,
            detail="Formato de áudio não suportado."
        )
def validar_tamanho(tamanho: int):
    if tamanho > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="O áudio excede o tamanho máximo permitido."
        )
def obter_extensao(arquivo: UploadFile):
    return os.path.splitext(arquivo.filename)[1].lower()
def obter_nome(arquivo: UploadFile):
    return os.path.basename(arquivo.filename)
import uuid
from fastapi import UploadFile
from app.services.r2_storage import r2_client
from app.config import R2_BUCKET_NAME

EXTENSOES_POR_TIPO = {
    "audio/mpeg": "mp3",
    "audio/wav": "wav",
    "audio/x-wav": "wav",
    "audio/x-m4a": "m4a",
    "audio/mp4": "m4a",
}

def upload_audio(arquivo: UploadFile) -> str:
    extensao = EXTENSOES_POR_TIPO[arquivo.content_type]
    nome_arquivo = f"{uuid.uuid4()}.{extensao}"
    conteudo = arquivo.file.read()
    try:
        r2_client.put_object(
            Bucket=R2_BUCKET_NAME,
            Key=nome_arquivo,
            Body=conteudo,
            ContentType=arquivo.content_type,
        )
    except Exception as error:
        raise RuntimeError("Falha ao armazenar o áudio.") from error

    # Armazena apenas a chave interna. Mantenha o bucket privado no R2.
    return nome_arquivo

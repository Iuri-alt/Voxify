import uuid
from fastapi import UploadFile
from Back.app.services import supabase

BUCKET_NAME = "audio"

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
        supabase.storage.from_(BUCKET_NAME).upload(
           path=nome_arquivo,
           file=conteudo,
           file_options={
           "content-type": arquivo.content_type
           }
        )
    except Exception as error:
       raise RuntimeError("Falha ao armazenar o áudio.") from error

    # Armazena apenas a chave interna. Configure o bucket como privado no Supabase.
    return nome_arquivo

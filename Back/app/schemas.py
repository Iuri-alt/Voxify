from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field

Nome = Annotated[str, Field(min_length=2, max_length=100, strip_whitespace=True)]
Senha = Annotated[str, Field(min_length=6, max_length=128)]

class ArquivoResponse(BaseModel):
    id: int
    nome_do_audio: str
    tipo_arquivo: str
    status: str
    data_upload: datetime
    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr
    senha: Annotated[str, Field(min_length=1, max_length=128)]

class UserUpdate(BaseModel):
    nome: Nome
    email: EmailStr

class UserCreate(BaseModel):
    nome: Nome
    email: EmailStr
    senha: Senha

class UserResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)

class TranscricaoResponse(BaseModel):
    id: int
    arquivo_id: int
    texto: str
    idioma: str | None = None
    data_criacao: datetime
    model_config = ConfigDict(from_attributes=True)

class ArquivoUploadResponse(ArquivoResponse):
    texto: str

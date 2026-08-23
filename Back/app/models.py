from sqlalchemy import (Column, Integer, String, DateTime, Text, ForeignKey, TIMESTAMP)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)
    criado_em = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    arquivos = relationship(
        "Arquivo",
        back_populates="usuario",
        cascade="all, delete"
    )

class Arquivo(Base):
    __tablename__ = "arquivos"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id", ondelete="CASCADE"),
        nullable=False
    )

    nome_do_audio = Column(String(255), nullable=False)
    url_audio = Column(Text, nullable=False)
    tipo_arquivo = Column(String(30), nullable=False)
    status = Column(String(20), default="enviado")
    data_upload = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now()
    )

    usuario = relationship(
        "User",
        back_populates="arquivos"
    )

    transcricoes = relationship(
        "Transcricao",
        back_populates="arquivo",
        cascade="all, delete"
    )

class Transcricao(Base):
    __tablename__ = "transcricoes"
    id = Column(Integer, primary_key=True, index=True)
    arquivo_id = Column(
        Integer,
        ForeignKey("arquivos.id", ondelete="CASCADE"),
        nullable=False
    )

    texto = Column(Text, nullable=False)
    idioma = Column(String(10), nullable=True, default="pt")
    data_criacao = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now()
    )

    arquivo = relationship(
        "Arquivo",
        back_populates="transcricoes"
    )

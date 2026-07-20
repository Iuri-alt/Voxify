import os

from fastapi import FastAPI, Request
from app.database import Base, engine
import app.models
from Back.app.routers import usuarios
from Back.app.routers import autenticacao
from Back.app.routers import arquivo_upload
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from app.config import ALLOWED_ORIGINS, get_jwt_secret_key


# Em produção, use migrações controladas. Útil apenas para desenvolvimento local.
if os.getenv("AUTO_CREATE_SCHEMA", "false").lower() == "true":
    Base.metadata.create_all(bind=engine)

# Falha cedo se a API for iniciada sem uma chave JWT segura.
get_jwt_secret_key()

app = FastAPI(
    title="Voxify API",
    version="1.0.0"
)

app.include_router(usuarios.router)
app.include_router(autenticacao.router)
app.include_router(arquivo_upload.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Cache-Control"] = "no-store" if request.url.path.startswith(("/auth", "/arquivos", "/users")) else "no-cache"
        return response

app.add_middleware(SecurityHeadersMiddleware)

@app.get("/")
def home():
    return {
        "status": "online",
        "mensagem": "Bem-vindo ao Voxify 🚀"
    }

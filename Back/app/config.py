import os
from dotenv import load_dotenv

load_dotenv()

def required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"A variável de ambiente {name} é obrigatória.")
    return value

DATABASE_URL = required_env("DATABASE_URL")
AZURE_SPEECH_KEY = required_env("AZURE_SPEECH_KEY")
AZURE_SPEECH_REGION = required_env("AZURE_SPEECH_REGION")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY") or os.getenv("SECRET_KEY")

def get_jwt_secret_key() -> str:
    if not JWT_SECRET_KEY or len(JWT_SECRET_KEY) < 32:
        raise RuntimeError("JWT_SECRET_KEY deve ter pelo menos 32 caracteres aleatórios.")
    return JWT_SECRET_KEY

JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "20"))
ALLOWED_ORIGINS = [origin.strip() for origin in os.getenv(
    "ALLOWED_ORIGINS", "http://127.0.0.1:5500,http://localhost:5500"
).split(",") if origin.strip()]

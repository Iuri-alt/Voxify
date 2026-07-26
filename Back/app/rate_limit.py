from collections import defaultdict, deque
from time import monotonic

from fastapi import HTTPException, Request, status


class RateLimiter:
    def __init__(self, max_tentativas: int, janela_segundos: int):
        self.max_tentativas = max_tentativas
        self.janela_segundos = janela_segundos
        self._tentativas: dict[str, deque[float]] = defaultdict(deque)

    def verificar(self, chave: str) -> None:
        agora = monotonic()
        tentativas = self._tentativas[chave]
        while tentativas and agora - tentativas[0] > self.janela_segundos:
            tentativas.popleft()
        if len(tentativas) >= self.max_tentativas:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Muitas tentativas. Aguarde alguns minutos.",
            )
        tentativas.append(agora)

    def limpar(self, chave: str) -> None:
        self._tentativas.pop(chave, None)


def ip_do_cliente(request: Request) -> str:
    return request.client.host if request.client else "desconhecido"

from uuid import uuid4


def novo_id() -> str:
    """Identificador gerado no próprio domínio, sem depender do banco."""
    return uuid4().hex

"""Portas: o que os casos de uso precisam do mundo externo.

Os casos de uso dependem destas abstrações, e a camada de infraestrutura
fornece os adapters (Princípio da Inversão de Dependência). Cada porta é
pequena e específica (Princípio da Segregação de Interfaces).
"""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from domain.usuario import Usuario


class RepositorioDeUsuarios(ABC):
    @abstractmethod
    def salvar(self, usuario: Usuario) -> None:
        ...

    @abstractmethod
    def por_id(self, usuario_id: str) -> Optional[Usuario]:
        ...

    @abstractmethod
    def por_email(self, email: str) -> Optional[Usuario]:
        ...


class RepositorioDeBarbearias(ABC):
    pass


class RepositorioDeServicos(ABC):
    pass


class RepositorioDeAgendamentos(ABC):
    pass


class GeradorDeHashDeSenha(ABC):
    @abstractmethod
    def gerar(self, senha: str) -> str:
        ...

    @abstractmethod
    def conferir(self, senha: str, senha_hash: str) -> bool:
        ...


class Relogio(ABC):
    @abstractmethod
    def agora(self) -> datetime:
        ...

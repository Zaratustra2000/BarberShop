"""Portas: o que os casos de uso precisam do mundo externo.

Os casos de uso dependem destas abstrações, e a camada de infraestrutura
fornece os adapters (Princípio da Inversão de Dependência). Cada porta é
pequena e específica (Princípio da Segregação de Interfaces).
"""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

from domain.agendamento import Agendamento
from domain.barbearia import Barbearia
from domain.servico import Servico
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

    @abstractmethod
    def barbeiros_por_nome(self, trecho: str) -> List[Usuario]:
        """Barbeiros cujo nome contém o trecho, sem diferenciar maiúsculas."""


class RepositorioDeBarbearias(ABC):
    """Lê e grava o agregado Barbearia inteiro (ADR 0001)."""

    @abstractmethod
    def salvar(self, barbearia: Barbearia) -> None:
        ...

    @abstractmethod
    def remover(self, barbearia_id: str) -> None:
        ...

    @abstractmethod
    def por_id(self, barbearia_id: str) -> Optional[Barbearia]:
        ...

    @abstractmethod
    def do_dono(self, dono_id: str) -> List[Barbearia]:
        ...

    @abstractmethod
    def no_bairro(self, bairro_chave: str) -> List[Barbearia]:
        """Barbearias cuja chave de bairro (normalizada) é igual."""

    @abstractmethod
    def com_blocos_do_barbeiro(self, barbeiro_id: str) -> List[Barbearia]:
        """Barbearias onde o barbeiro tem ao menos um bloco de horário."""


class RepositorioDeServicos(ABC):
    @abstractmethod
    def salvar(self, servico: Servico) -> None:
        ...

    @abstractmethod
    def por_id(self, servico_id: str) -> Optional[Servico]:
        ...

    @abstractmethod
    def do_barbeiro(self, barbeiro_id: str) -> List[Servico]:
        """Serviços do barbeiro em ordem alfabética."""


class RepositorioDeAgendamentos(ABC):
    @abstractmethod
    def salvar(self, agendamento: Agendamento) -> None:
        ...

    @abstractmethod
    def do_barbeiro(self, barbeiro_id: str) -> List[Agendamento]:
        """Agendamentos do barbeiro em ordem cronológica."""

    @abstractmethod
    def do_cliente(self, cliente_id: str) -> List[Agendamento]:
        """Agendamentos do cliente em ordem cronológica."""


class ArmazenamentoDeFotos(ABC):
    @abstractmethod
    def salvar(self, conteudo: bytes, extensao: str) -> str:
        ...

    @abstractmethod
    def remover(self, nome_do_arquivo: str) -> None:
        ...


class ValidadorDeFotos(ABC):
    @abstractmethod
    def validar(self, conteudo: bytes) -> str:
        ...


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

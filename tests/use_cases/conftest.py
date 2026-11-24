import pytest

from infra.repositories.memoria import (
    RepositorioDeAgendamentosEmMemoria,
    RepositorioDeBarbeariasEmMemoria,
    RepositorioDeServicosEmMemoria,
    RepositorioDeUsuariosEmMemoria,
)
from tests.dubles import HashFalso, RelogioFixo
from use_cases.cadastrar_usuario import CadastrarUsuario


class Contexto:
    """Repositórios em memória e dublês compartilhados por um teste."""

    def __init__(self):
        self.usuarios = RepositorioDeUsuariosEmMemoria()
        self.barbearias = RepositorioDeBarbeariasEmMemoria()
        self.servicos = RepositorioDeServicosEmMemoria()
        self.agendamentos = RepositorioDeAgendamentosEmMemoria()
        self.hash = HashFalso()
        self.relogio = RelogioFixo()

    def cadastrar(self, papel, nome="Pessoa Teste", email=None):
        email = email or "{}@exemplo.com".format(papel)
        return CadastrarUsuario(self.usuarios, self.hash).executar(
            nome=nome, email=email, senha="segredo1", papel=papel)


@pytest.fixture
def ctx():
    return Contexto()

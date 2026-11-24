from typing import List

from domain.erros import NaoEncontrado
from domain.servico import Servico
from domain.usuario import Papel, Usuario
from use_cases.portas import RepositorioDeServicos, RepositorioDeUsuarios


def exigir_usuario(usuarios: RepositorioDeUsuarios, usuario_id: str,
                   papel: Papel) -> Usuario:
    usuario = usuarios.por_id(usuario_id)
    if usuario is None:
        raise NaoEncontrado("Usuário não encontrado.")
    usuario.exigir_papel(papel)
    return usuario


class CadastrarServico:
    """US3: o barbeiro publica um serviço com preço e duração."""

    def __init__(self, usuarios: RepositorioDeUsuarios,
                 servicos: RepositorioDeServicos):
        self._usuarios = usuarios
        self._servicos = servicos

    def executar(self, barbeiro_id: str, nome: str, preco_centavos: int,
                 duracao_minutos: int) -> Servico:
        exigir_usuario(self._usuarios, barbeiro_id, Papel.BARBEIRO)
        servico = Servico(barbeiro_id=barbeiro_id, nome=nome,
                          preco_centavos=preco_centavos,
                          duracao_minutos=duracao_minutos)
        self._servicos.salvar(servico)
        return servico


class ConsultarServicosDoBarbeiro:
    def __init__(self, servicos: RepositorioDeServicos):
        self._servicos = servicos

    def executar(self, barbeiro_id: str) -> List[Servico]:
        return self._servicos.do_barbeiro(barbeiro_id)

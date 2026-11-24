from domain.erros import NaoEncontrado
from use_cases.portas import RepositorioDeBarbearias


class ConsultarPerfilDaBarbearia:
    def __init__(self, barbearias: RepositorioDeBarbearias):
        self._barbearias = barbearias

    def executar(self, barbearia_id: str):
        barbearia = self._barbearias.por_id(barbearia_id)
        if barbearia is None:
            raise NaoEncontrado("Barbearia não encontrada.")
        return barbearia

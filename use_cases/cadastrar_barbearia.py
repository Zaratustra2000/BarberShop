from domain.barbearia import Barbearia
from domain.erros import DadosInvalidos
from domain.usuario import Papel
from use_cases.acesso import exigir_usuario
from use_cases.portas import RepositorioDeBarbearias, RepositorioDeUsuarios

MAXIMO_DE_CADEIRAS = 30


class CadastrarBarbearia:
    """US2: o dono cadastra a barbearia já com as cadeiras."""

    def __init__(self, usuarios: RepositorioDeUsuarios,
                 barbearias: RepositorioDeBarbearias):
        self._usuarios = usuarios
        self._barbearias = barbearias

    def executar(self, dono_id: str, nome: str, endereco: str, bairro: str,
                 latitude: float, longitude: float, regras: str,
                 quantidade_de_cadeiras: int) -> Barbearia:
        dono = exigir_usuario(self._usuarios, dono_id, Papel.DONO)
        if not 1 <= quantidade_de_cadeiras <= MAXIMO_DE_CADEIRAS:
            raise DadosInvalidos("Informe de 1 a {} cadeiras.".format(
                MAXIMO_DE_CADEIRAS))
        barbearia = Barbearia(dono_id=dono.id, nome=nome, endereco=endereco,
                              bairro=bairro, latitude=latitude,
                              longitude=longitude, regras=regras)
        for _ in range(quantidade_de_cadeiras):
            barbearia.adicionar_cadeira()
        self._barbearias.salvar(barbearia)
        return barbearia

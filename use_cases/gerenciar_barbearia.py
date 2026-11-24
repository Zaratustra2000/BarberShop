from domain.erros import ConflitoDeHorario
from domain.usuario import Papel
from use_cases.acesso import exigir_usuario
from use_cases.consultar_barbearias_do_dono import barbearia_do_dono
from use_cases.portas import (RepositorioDeBarbearias, RepositorioDeUsuarios)


class GerenciarBarbearia:
    def __init__(self, usuarios: RepositorioDeUsuarios,
                 barbearias: RepositorioDeBarbearias):
        self._usuarios = usuarios
        self._barbearias = barbearias

    def excluir(self, dono_id: str, barbearia_id: str) -> None:
        exigir_usuario(self._usuarios, dono_id, Papel.DONO)
        barbearia = barbearia_do_dono(
            self._barbearias, dono_id, barbearia_id)
        if barbearia.blocos:
            raise ConflitoDeHorario(
                "A barbearia tem blocos de horário e deve ser desativada.")
        self._barbearias.remover(barbearia_id)

    def desativar(self, dono_id: str, barbearia_id: str) -> None:
        exigir_usuario(self._usuarios, dono_id, Papel.DONO)
        barbearia = barbearia_do_dono(
            self._barbearias, dono_id, barbearia_id)
        barbearia.desativar()
        self._barbearias.salvar(barbearia)

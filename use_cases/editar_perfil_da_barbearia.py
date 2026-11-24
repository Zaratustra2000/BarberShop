from domain.erros import DadosInvalidos
from domain.usuario import Papel
from use_cases.acesso import exigir_usuario
from use_cases.consultar_barbearias_do_dono import barbearia_do_dono
from use_cases.portas import (ArmazenamentoDeFotos, RepositorioDeBarbearias,
                              RepositorioDeUsuarios)

MAXIMO_DE_CADEIRAS = 30


class EditarPerfilDaBarbearia:
    def __init__(self, usuarios: RepositorioDeUsuarios,
                 barbearias: RepositorioDeBarbearias):
        self._usuarios = usuarios
        self._barbearias = barbearias

    def executar(self, dono_id: str, barbearia_id: str, nome: str,
                 endereco: str, bairro: str, latitude: float,
                 longitude: float, regras: str,
                 quantidade_de_cadeiras: int):
        exigir_usuario(self._usuarios, dono_id, Papel.DONO)
        if not 1 <= quantidade_de_cadeiras <= MAXIMO_DE_CADEIRAS:
            raise DadosInvalidos("Informe de 1 a {} cadeiras.".format(
                MAXIMO_DE_CADEIRAS))
        barbearia = barbearia_do_dono(
            self._barbearias, dono_id, barbearia_id)
        barbearia.editar(nome, endereco, bairro, latitude, longitude, regras)
        while len(barbearia.cadeiras) < quantidade_de_cadeiras:
            barbearia.adicionar_cadeira()
        while len(barbearia.cadeiras) > quantidade_de_cadeiras:
            barbearia.remover_cadeira(barbearia.cadeiras[-1].id)
        self._barbearias.salvar(barbearia)
        return barbearia

    def remover_cadeira(self, dono_id: str, barbearia_id: str,
                        cadeira_id: str):
        exigir_usuario(self._usuarios, dono_id, Papel.DONO)
        barbearia = barbearia_do_dono(
            self._barbearias, dono_id, barbearia_id)
        barbearia.remover_cadeira(cadeira_id)
        self._barbearias.salvar(barbearia)
        return barbearia

    def atualizar_foto_principal(self, dono_id: str, barbearia_id: str,
                                 nome_do_arquivo: str):
        exigir_usuario(self._usuarios, dono_id, Papel.DONO)
        barbearia = barbearia_do_dono(
            self._barbearias, dono_id, barbearia_id)
        barbearia.definir_foto_principal(nome_do_arquivo)
        self._barbearias.salvar(barbearia)
        return barbearia


class SubstituirFotoPrincipalDaBarbearia:
    def __init__(self, usuarios: RepositorioDeUsuarios,
                 barbearias: RepositorioDeBarbearias,
                 fotos: ArmazenamentoDeFotos):
        self._usuarios = usuarios
        self._barbearias = barbearias
        self._fotos = fotos

    def executar(self, dono_id: str, barbearia_id: str,
                 conteudo: bytes, extensao: str):
        exigir_usuario(self._usuarios, dono_id, Papel.DONO)
        barbearia = barbearia_do_dono(
            self._barbearias, dono_id, barbearia_id)
        foto_anterior = barbearia.foto_principal
        nome_gerado = self._fotos.salvar(conteudo, extensao)
        barbearia.definir_foto_principal(nome_gerado)
        self._barbearias.salvar(barbearia)
        if foto_anterior:
            self._fotos.remover(foto_anterior)
        return barbearia

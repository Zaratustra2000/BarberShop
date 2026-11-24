from domain.usuario import Papel
from use_cases.acesso import exigir_usuario
from use_cases.portas import (ArmazenamentoDeFotos, RepositorioDeUsuarios)


class EditarPerfilDoBarbeiro:
    def __init__(self, usuarios: RepositorioDeUsuarios):
        self._usuarios = usuarios

    def executar(self, barbeiro_id: str, nome: str,
                 apresentacao: str = ""):
        barbeiro = exigir_usuario(
            self._usuarios, barbeiro_id, Papel.BARBEIRO)
        barbeiro.editar_perfil_do_barbeiro(nome, apresentacao)
        self._usuarios.salvar(barbeiro)
        return barbeiro

    def atualizar_foto(self, barbeiro_id: str,
                       nome_do_arquivo: str):
        barbeiro = exigir_usuario(
            self._usuarios, barbeiro_id, Papel.BARBEIRO)
        barbeiro.definir_foto_perfil(nome_do_arquivo)
        self._usuarios.salvar(barbeiro)
        return barbeiro


class SubstituirFotoDoBarbeiro:
    def __init__(self, usuarios: RepositorioDeUsuarios,
                 fotos: ArmazenamentoDeFotos):
        self._usuarios = usuarios
        self._fotos = fotos

    def executar(self, barbeiro_id: str, conteudo: bytes,
                 extensao: str):
        barbeiro = exigir_usuario(
            self._usuarios, barbeiro_id, Papel.BARBEIRO)
        foto_anterior = barbeiro.foto_perfil
        nome_gerado = self._fotos.salvar(conteudo, extensao)
        barbeiro.definir_foto_perfil(nome_gerado)
        self._usuarios.salvar(barbeiro)
        if foto_anterior:
            self._fotos.remover(foto_anterior)
        return barbeiro

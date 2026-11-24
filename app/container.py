"""Composition root: o único lugar que conhece as classes concretas.

Aqui os adapters de infraestrutura são ligados às portas que os casos de uso
esperam. Trocar SQLite por outro banco significa mudar apenas este arquivo.
"""
from infra.db.database import BancoSQLite
from infra.repositories import sqlite
from infra.seguranca import GeradorDeHashWerkzeug, RelogioDoSistema
from use_cases.autenticar_usuario import AutenticarUsuario
from use_cases.cadastrar_usuario import CadastrarUsuario


class Container:
    def __init__(self, caminho_do_banco, relogio=None):
        banco = BancoSQLite(caminho_do_banco)
        banco.criar_tabelas()
        self.relogio = relogio or RelogioDoSistema()
        usuarios = sqlite.RepositorioDeUsuariosSQLite(banco)
        gerador_de_hash = GeradorDeHashWerkzeug()

        self.usuarios = usuarios
        self.cadastrar_usuario = CadastrarUsuario(usuarios, gerador_de_hash)
        self.autenticar_usuario = AutenticarUsuario(usuarios,
                                                    gerador_de_hash)

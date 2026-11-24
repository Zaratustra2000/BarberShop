"""Composition root: o único lugar que conhece as classes concretas.

Aqui os adapters de infraestrutura são ligados às portas que os casos de uso
esperam. Trocar SQLite por outro banco significa mudar apenas este arquivo.
"""
from infra.db.database import BancoSQLite
from infra.repositories import sqlite
from infra.seguranca import GeradorDeHashWerkzeug, RelogioDoSistema
from use_cases.autenticar_usuario import AutenticarUsuario
from use_cases.cadastrar_barbearia import CadastrarBarbearia
from use_cases.cadastrar_usuario import CadastrarUsuario
from use_cases.consultar_barbearias_do_dono import ConsultarBarbeariasDoDono
from use_cases.publicar_horario_ocioso import PublicarHorarioOcioso


class Container:
    def __init__(self, caminho_do_banco, relogio=None):
        banco = BancoSQLite(caminho_do_banco)
        banco.criar_tabelas()
        self.relogio = relogio or RelogioDoSistema()
        usuarios = sqlite.RepositorioDeUsuariosSQLite(banco)
        gerador_de_hash = GeradorDeHashWerkzeug()

        barbearias = sqlite.RepositorioDeBarbeariasSQLite(banco)

        self.usuarios = usuarios
        self.cadastrar_barbearia = CadastrarBarbearia(usuarios, barbearias)
        self.consultar_barbearias_do_dono = ConsultarBarbeariasDoDono(
            barbearias)
        self.publicar_horario_ocioso = PublicarHorarioOcioso(
            barbearias, self.relogio)
        self.cadastrar_usuario = CadastrarUsuario(usuarios, gerador_de_hash)
        self.autenticar_usuario = AutenticarUsuario(usuarios,
                                                    gerador_de_hash)

from domain.erros import CredenciaisInvalidas
from domain.usuario import Usuario
from use_cases.portas import GeradorDeHashDeSenha, RepositorioDeUsuarios


class AutenticarUsuario:
    """US1: confere e-mail e senha sem revelar qual dos dois falhou."""

    def __init__(self, usuarios: RepositorioDeUsuarios,
                 gerador_de_hash: GeradorDeHashDeSenha):
        self._usuarios = usuarios
        self._hash = gerador_de_hash

    def executar(self, email: str, senha: str) -> Usuario:
        usuario = self._usuarios.por_email((email or "").strip().lower())
        if usuario is None or not self._hash.conferir(senha or "",
                                                      usuario.senha_hash):
            raise CredenciaisInvalidas("E-mail ou senha inválidos.")
        return usuario

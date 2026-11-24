from domain.erros import DadosInvalidos
from domain.usuario import Papel, Usuario
from use_cases.portas import GeradorDeHashDeSenha, RepositorioDeUsuarios

TAMANHO_MINIMO_DA_SENHA = 6


class CadastrarUsuario:
    """US1: cria a conta de um dono, barbeiro ou cliente."""

    def __init__(self, usuarios: RepositorioDeUsuarios,
                 gerador_de_hash: GeradorDeHashDeSenha):
        self._usuarios = usuarios
        self._hash = gerador_de_hash

    def executar(self, nome: str, email: str, senha: str,
                 papel: str) -> Usuario:
        if len(senha or "") < TAMANHO_MINIMO_DA_SENHA:
            raise DadosInvalidos("A senha precisa ter ao menos {} "
                                 "caracteres.".format(TAMANHO_MINIMO_DA_SENHA))
        usuario = Usuario(nome=nome, email=email,
                          senha_hash=self._hash.gerar(senha),
                          papel=Papel.de_texto(papel))
        if self._usuarios.por_email(usuario.email) is not None:
            raise DadosInvalidos("Este e-mail já está cadastrado.")
        self._usuarios.salvar(usuario)
        return usuario

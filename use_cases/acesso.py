from domain.erros import NaoEncontrado
from domain.usuario import Papel, Usuario
from use_cases.portas import RepositorioDeUsuarios


def exigir_usuario(usuarios: RepositorioDeUsuarios, usuario_id: str,
                   papel: Papel) -> Usuario:
    """Carrega o usuário e garante que ele tem a persona exigida."""
    usuario = usuarios.por_id(usuario_id)
    if usuario is None:
        raise NaoEncontrado("Usuário não encontrado.")
    usuario.exigir_papel(papel)
    return usuario

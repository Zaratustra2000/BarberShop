from domain.erros import DadosInvalidos
from use_cases.portas import ValidadorDeFotos


LIMITE_DE_FOTO = 5 * 1024 * 1024


class ValidarFotoDaBarbearia:
    def __init__(self, validador: ValidadorDeFotos):
        self._validador = validador

    def executar(self, conteudo: bytes) -> str:
        if len(conteudo) > LIMITE_DE_FOTO:
            raise DadosInvalidos("A imagem deve ter no máximo 5 MB.")
        return self._validador.validar(conteudo)

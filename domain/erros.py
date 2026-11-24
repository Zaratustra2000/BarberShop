"""Erros de domínio: violações de regras de negócio, sem detalhes técnicos."""


class ErroDeDominio(Exception):
    """Base de todos os erros que a interface pode mostrar ao usuário."""


class DadosInvalidos(ErroDeDominio):
    """Algum dado informado não respeita uma invariante."""


class ConflitoDeHorario(ErroDeDominio):
    """Dois períodos que não podem se sobrepor se sobrepõem."""


class AcessoNegado(ErroDeDominio):
    """A persona não pode executar esta ação."""


class NaoEncontrado(ErroDeDominio):
    """O recurso pedido não existe."""


class CredenciaisInvalidas(ErroDeDominio):
    """E-mail ou senha não conferem."""

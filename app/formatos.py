"""Conversões entre texto da tela e valores de domínio (interface adapter)."""
from datetime import datetime

from domain.erros import DadosInvalidos


def reais_para_centavos(texto: str) -> int:
    """'45,50' ou '45.50' vira 4550."""
    limpo = (texto or "").replace("R$", "").strip()
    if "," in limpo:
        limpo = limpo.replace(".", "").replace(",", ".")
    try:
        return int(round(float(limpo) * 100))
    except ValueError:
        raise DadosInvalidos("Valor em reais inválido: {}".format(texto))


def formatar_reais(centavos: int) -> str:
    inteiro, resto = divmod(int(centavos), 100)
    milhar = "{:,}".format(inteiro).replace(",", ".")
    return "R$ {},{:02d}".format(milhar, resto)


def ler_data_hora(texto: str) -> datetime:
    """Lê o valor de um <input type="datetime-local">."""
    try:
        return datetime.strptime((texto or "").strip(), "%Y-%m-%dT%H:%M")
    except ValueError:
        raise DadosInvalidos("Data e hora inválidas.")


def formatar_data_hora(valor: datetime) -> str:
    return valor.strftime("%d/%m/%Y %H:%M")


def formatar_hora(valor: datetime) -> str:
    return valor.strftime("%H:%M")


def registrar_filtros(app):
    app.jinja_env.filters["reais"] = formatar_reais
    app.jinja_env.filters["data_hora"] = formatar_data_hora
    app.jinja_env.filters["hora"] = formatar_hora

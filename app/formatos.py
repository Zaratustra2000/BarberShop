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


def ler_decimal(texto: str, rotulo: str) -> float:
    try:
        return float((texto or "").replace(",", "."))
    except ValueError:
        raise DadosInvalidos("Valor inválido para {}.".format(rotulo))


def ler_inteiro(texto: str, rotulo: str) -> int:
    try:
        return int(texto)
    except (TypeError, ValueError):
        raise DadosInvalidos("Valor inválido para {}.".format(rotulo))


def formatar_reais(centavos: int) -> str:
    inteiro, resto = divmod(int(centavos), 100)
    milhar = "{:,}".format(inteiro).replace(",", ".")
    return "R$ {},{:02d}".format(milhar, resto)


def formatar_media(media: float) -> str:
    return "{:.1f}".format(media).replace(".", ",")


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


def formatar_data_hora_local(valor: datetime) -> str:
    return valor.strftime("%Y-%m-%dT%H:%M")


def registrar_filtros(app):
    app.jinja_env.filters["reais"] = formatar_reais
    app.jinja_env.filters["media"] = formatar_media
    app.jinja_env.filters["data_hora"] = formatar_data_hora
    app.jinja_env.filters["hora"] = formatar_hora
    app.jinja_env.filters["data_hora_local"] = formatar_data_hora_local

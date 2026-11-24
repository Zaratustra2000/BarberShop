from io import BytesIO

from PIL import Image, UnidentifiedImageError

from domain.erros import DadosInvalidos
from use_cases.portas import ValidadorDeFotos


class ValidadorDeFotosPillow(ValidadorDeFotos):
    def validar(self, conteudo: bytes) -> str:
        try:
            imagem = Image.open(BytesIO(conteudo))
            imagem.verify()
            imagem = Image.open(BytesIO(conteudo))
            imagem.load()
        except (UnidentifiedImageError, OSError, SyntaxError,
                ValueError, Image.DecompressionBombError):
            raise DadosInvalidos(
                "Formato inválido. Envie uma imagem JPG, PNG ou WebP.")
        formatos = {"JPEG": ".jpg", "PNG": ".png", "WEBP": ".webp"}
        extensao = formatos.get(imagem.format)
        if extensao is None:
            raise DadosInvalidos(
                "Formato inválido. Envie uma imagem JPG, PNG ou WebP.")
        return extensao

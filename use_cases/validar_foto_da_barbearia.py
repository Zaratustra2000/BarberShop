from io import BytesIO

from PIL import Image, UnidentifiedImageError

from domain.erros import DadosInvalidos


LIMITE_DE_FOTO = 5 * 1024 * 1024


class ValidarFotoDaBarbearia:
    def executar(self, conteudo: bytes) -> str:
        if len(conteudo) > LIMITE_DE_FOTO:
            raise DadosInvalidos("A imagem deve ter no máximo 5 MB.")
        try:
            imagem = Image.open(BytesIO(conteudo))
            imagem.verify()
        except (UnidentifiedImageError, OSError, SyntaxError):
            raise DadosInvalidos(
                "Formato inválido. Envie uma imagem JPG, PNG ou WebP.")
        formatos = {"JPEG": ".jpg", "PNG": ".png", "WEBP": ".webp"}
        extensao = formatos.get(imagem.format)
        if extensao is None:
            raise DadosInvalidos(
                "Formato inválido. Envie uma imagem JPG, PNG ou WebP.")
        return extensao

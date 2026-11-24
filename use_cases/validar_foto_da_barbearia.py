import struct
import zlib

from domain.erros import DadosInvalidos


LIMITE_DE_FOTO = 5 * 1024 * 1024


class ValidarFotoDaBarbearia:
    def executar(self, conteudo: bytes) -> str:
        if len(conteudo) > LIMITE_DE_FOTO:
            raise DadosInvalidos("A imagem deve ter no máximo 5 MB.")
        if _jpeg_valido(conteudo):
            return ".jpg"
        if _png_valido(conteudo):
            return ".png"
        if _webp_valido(conteudo):
            return ".webp"
        raise DadosInvalidos(
            "Formato inválido. Envie uma imagem JPG, PNG ou WebP.")


def _png_valido(conteudo):
    if len(conteudo) < 33 or not conteudo.startswith(
            b"\x89PNG\r\n\x1a\n"):
        return False
    posicao = 8
    primeiro = True
    encontrou_idat = False
    encontrou_iend = False
    idats = []
    while posicao + 12 <= len(conteudo):
        tamanho = struct.unpack(">I", conteudo[posicao:posicao + 4])[0]
        tipo = conteudo[posicao + 4:posicao + 8]
        fim = posicao + 8 + tamanho
        if fim + 4 > len(conteudo):
            return False
        dados = conteudo[posicao + 8:fim]
        crc = struct.unpack(">I", conteudo[fim:fim + 4])[0]
        if zlib.crc32(tipo + dados) & 0xffffffff != crc:
            return False
        if primeiro:
            if tipo != b"IHDR" or tamanho != 13:
                return False
            largura, altura = struct.unpack(">II", dados[:8])
            if largura == 0 or altura == 0:
                return False
            primeiro = False
        if tipo == b"IDAT":
            encontrou_idat = True
            idats.append(dados)
        if tipo == b"IEND":
            encontrou_iend = True
            if tamanho != 0 or fim + 4 != len(conteudo):
                return False
            break
        posicao = fim + 4
    if not encontrou_idat or not encontrou_iend:
        return False
    try:
        zlib.decompress(b"".join(idats))
    except zlib.error:
        return False
    return True


def _jpeg_valido(conteudo):
    if len(conteudo) < 4:
        return False
    if not conteudo.startswith(b"\xff\xd8") or not conteudo.endswith(
            b"\xff\xd9"):
        return False
    posicao = 2
    encontrou_frame = False
    encontrou_scan = False
    while posicao + 3 < len(conteudo):
        if conteudo[posicao] != 0xff:
            posicao += 1
            continue
        while posicao < len(conteudo) and conteudo[posicao] == 0xff:
            posicao += 1
        if posicao >= len(conteudo):
            break
        marcador = conteudo[posicao]
        posicao += 1
        if marcador in (0xd9, 0xd8):
            break
        if marcador == 0xda:
            encontrou_scan = True
            break
        if marcador in range(0xc0, 0xd0) and marcador not in (
                0xc4, 0xc8, 0xcc):
            encontrou_frame = True
        if posicao + 2 > len(conteudo):
            return False
        tamanho = struct.unpack(">H", conteudo[posicao:posicao + 2])[0]
        if tamanho < 2 or posicao + tamanho > len(conteudo):
            return False
        posicao += tamanho
    return encontrou_frame and encontrou_scan


def _webp_valido(conteudo):
    if len(conteudo) < 20 or conteudo[:4] != b"RIFF":
        return False
    if conteudo[8:12] != b"WEBP":
        return False
    tamanho = struct.unpack("<I", conteudo[4:8])[0]
    if tamanho != len(conteudo) - 8:
        return False
    posicao = 12
    encontrou_chunk = False
    while posicao + 8 <= len(conteudo):
        tipo = conteudo[posicao:posicao + 4]
        tamanho = struct.unpack("<I", conteudo[posicao + 4:posicao + 8])[0]
        inicio = posicao + 8
        fim = inicio + tamanho
        if fim > len(conteudo):
            return False
        dados = conteudo[inicio:fim]
        if tipo == b"VP8 ":
            encontrou_chunk = len(dados) >= 10
        elif tipo == b"VP8L":
            encontrou_chunk = len(dados) >= 5 and dados[0] == 0x2f
        elif tipo == b"VP8X":
            encontrou_chunk = len(dados) >= 10
        posicao = fim + (tamanho % 2)
    return encontrou_chunk

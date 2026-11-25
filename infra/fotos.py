import os
import uuid

from use_cases.portas import ArmazenamentoDeFotos


class ArmazenamentoDeFotosLocal(ArmazenamentoDeFotos):
    def __init__(self, diretório: str):
        self._diretório = diretório
        os.makedirs(diretório, exist_ok=True)

    def salvar(self, conteudo: bytes, extensao: str) -> str:
        nome = "{}{}".format(uuid.uuid4().hex, extensao)
        caminho = os.path.join(self._diretório, nome)
        with open(caminho, "wb") as destino:
            destino.write(conteudo)
        return nome

    def remover(self, nome_do_arquivo: str) -> None:
        caminho = os.path.join(self._diretório, nome_do_arquivo)
        if os.path.exists(caminho):
            os.remove(caminho)

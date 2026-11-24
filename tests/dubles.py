"""Dublês das portas de fronteira (hash de senha e relógio)."""
from datetime import datetime

from use_cases.portas import GeradorDeHashDeSenha, Relogio


class HashFalso(GeradorDeHashDeSenha):
    def gerar(self, senha):
        return "hash:" + senha[::-1]

    def conferir(self, senha, senha_hash):
        return senha_hash == self.gerar(senha)


class RelogioFixo(Relogio):
    def __init__(self, agora=datetime(2030, 1, 6, 8, 0)):
        self._agora = agora

    def agora(self):
        return self._agora

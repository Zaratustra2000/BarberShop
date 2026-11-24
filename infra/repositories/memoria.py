"""Adapters em memória das portas de repositório.

Usados nos testes dos casos de uso. Devolvem cópias, como faria um banco,
para que um teste nunca passe por compartilhar o mesmo objeto por engano.
"""
from copy import deepcopy

from use_cases.portas import (
    RepositorioDeAgendamentos,
    RepositorioDeBarbearias,
    RepositorioDeServicos,
    RepositorioDeUsuarios,
)


class RepositorioDeUsuariosEmMemoria(RepositorioDeUsuarios):
    def __init__(self):
        self._dados = {}

    def salvar(self, usuario):
        self._dados[usuario.id] = deepcopy(usuario)

    def por_id(self, usuario_id):
        return deepcopy(self._dados.get(usuario_id))

    def por_email(self, email):
        for usuario in self._dados.values():
            if usuario.email == email:
                return deepcopy(usuario)
        return None


class RepositorioDeBarbeariasEmMemoria(RepositorioDeBarbearias):
    def __init__(self):
        self._dados = {}


class RepositorioDeServicosEmMemoria(RepositorioDeServicos):
    def __init__(self):
        self._dados = {}


class RepositorioDeAgendamentosEmMemoria(RepositorioDeAgendamentos):
    def __init__(self):
        self._dados = {}

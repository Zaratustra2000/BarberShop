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

    def salvar(self, barbearia):
        self._dados[barbearia.id] = deepcopy(barbearia)

    def por_id(self, barbearia_id):
        return deepcopy(self._dados.get(barbearia_id))

    def do_dono(self, dono_id):
        return self._filtrar(lambda b: b.dono_id == dono_id)

    def no_bairro(self, bairro_chave):
        return self._filtrar(lambda b: b.bairro_chave == bairro_chave)

    def com_blocos_do_barbeiro(self, barbeiro_id):
        return self._filtrar(lambda b: b.blocos_do_barbeiro(barbeiro_id))

    def _filtrar(self, criterio):
        encontradas = [b for b in self._dados.values() if criterio(b)]
        return [deepcopy(b) for b in
                sorted(encontradas, key=lambda b: (b.nome, b.id))]


class RepositorioDeServicosEmMemoria(RepositorioDeServicos):
    def __init__(self):
        self._dados = {}

    def salvar(self, servico):
        self._dados[servico.id] = deepcopy(servico)

    def por_id(self, servico_id):
        return deepcopy(self._dados.get(servico_id))

    def do_barbeiro(self, barbeiro_id):
        return sorted((deepcopy(s) for s in self._dados.values()
                       if s.barbeiro_id == barbeiro_id),
                      key=lambda s: (s.nome, s.id))


class RepositorioDeAgendamentosEmMemoria(RepositorioDeAgendamentos):
    def __init__(self):
        self._dados = {}

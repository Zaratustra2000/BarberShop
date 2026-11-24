"""Adapters em memória das portas de repositório.

Usados nos testes dos casos de uso. Devolvem cópias, como faria um banco,
para que um teste nunca passe por compartilhar o mesmo objeto por engano.
"""
from copy import deepcopy

from domain.usuario import Papel
from use_cases.portas import (
    RepositorioDeAgendamentos,
    RepositorioDeAvaliacoes,
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

    def barbeiros_por_nome(self, trecho):
        trecho = trecho.lower()
        achados = [u for u in self._dados.values()
                   if u.papel == Papel.BARBEIRO and trecho in u.nome.lower()]
        return [deepcopy(u) for u in sorted(achados,
                                            key=lambda u: (u.nome, u.id))]


class RepositorioDeBarbeariasEmMemoria(RepositorioDeBarbearias):
    def __init__(self):
        self._dados = {}

    def salvar(self, barbearia):
        self._dados[barbearia.id] = deepcopy(barbearia)

    def remover(self, barbearia_id):
        self._dados.pop(barbearia_id, None)

    def por_id(self, barbearia_id):
        return deepcopy(self._dados.get(barbearia_id))

    def do_dono(self, dono_id):
        return self._filtrar(lambda b: b.dono_id == dono_id)

    def no_bairro(self, bairro_chave):
        return self._filtrar(
            lambda b: b.ativa and bairro_chave in b.bairro_chave)

    def ativas(self):
        return self._filtrar(lambda b: b.ativa)

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

    def salvar(self, agendamento):
        self._dados[agendamento.id] = deepcopy(agendamento)

    def por_id(self, agendamento_id):
        agendamento = self._dados.get(agendamento_id)
        return deepcopy(agendamento) if agendamento else None

    def do_barbeiro(self, barbeiro_id):
        return self._filtrar(lambda a: a.barbeiro_id == barbeiro_id)

    def do_cliente(self, cliente_id):
        return self._filtrar(lambda a: a.cliente_id == cliente_id)

    def _filtrar(self, criterio):
        achados = [a for a in self._dados.values() if criterio(a)]
        return [deepcopy(a) for a in
                sorted(achados, key=lambda a: (a.periodo.inicio, a.id))]


class RepositorioDeAvaliacoesEmMemoria(RepositorioDeAvaliacoes):
    def __init__(self):
        self._dados = {}

    def salvar(self, avaliacao):
        self._dados[avaliacao.id] = deepcopy(avaliacao)

    def do_agendamento(self, agendamento_id):
        achadas = [a for a in self._dados.values()
                   if a.agendamento_id == agendamento_id]
        return deepcopy(achadas[0]) if achadas else None

    def do_barbeiro(self, barbeiro_id):
        achadas = [deepcopy(a) for a in self._dados.values()
                   if a.barbeiro_id == barbeiro_id]
        return sorted(achadas, key=lambda a: (a.agendamento_id, a.id))

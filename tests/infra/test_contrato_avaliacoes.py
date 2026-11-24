from domain.avaliacao import Avaliacao


def avaliacao(agendamento_id="a1", barbeiro_id="rafa", nota=5):
    return Avaliacao(agendamento_id=agendamento_id, cliente_id="lucas",
                     barbeiro_id=barbeiro_id, nota=nota)


def test_avaliacao_sobrevive_a_salvar_e_carregar_por_agendamento(repos):
    avaliacoes = repos["avaliacoes"]
    original = avaliacao(nota=4)

    avaliacoes.salvar(original)

    assert avaliacoes.do_agendamento("a1") == original
    assert avaliacoes.do_agendamento("outro") is None


def test_salvar_de_novo_atualiza_sem_criar_segunda_avaliacao(repos):
    avaliacoes = repos["avaliacoes"]
    original = avaliacao(nota=4)
    avaliacoes.salvar(original)

    original.nota = 2
    avaliacoes.salvar(original)

    assert avaliacoes.do_agendamento("a1").nota == 2
    assert avaliacoes.do_barbeiro("rafa") == [original]


def test_avaliacoes_do_barbeiro_ignoram_as_de_outros(repos):
    avaliacoes = repos["avaliacoes"]
    a, b = avaliacao("a1"), avaliacao("a2", nota=3)
    avaliacoes.salvar(b)
    avaliacoes.salvar(a)
    avaliacoes.salvar(avaliacao("a3", barbeiro_id="outro"))

    assert avaliacoes.do_barbeiro("rafa") == [a, b]

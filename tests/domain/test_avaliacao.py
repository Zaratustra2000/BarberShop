from datetime import datetime

from domain.agendamento import Agendamento
from domain.avaliacao import Avaliacao, ResumoDeAvaliacoes
from domain.periodo import Periodo


def agendamento():
    return Agendamento(
        cliente_id="lucas", barbeiro_id="rafa", servico_id="corte",
        servico_nome="Corte", barbearia_id="b1", bloco_id="bloco1",
        periodo=Periodo(datetime(2030, 1, 7, 14), datetime(2030, 1, 7, 15)),
        preco_centavos=4500)


def test_resumo_sem_avaliacoes_nao_inventa_media():
    resumo = ResumoDeAvaliacoes.de([])
    assert resumo.quantidade == 0
    assert resumo.media is None


def test_resumo_calcula_media_e_quantidade():
    notas = [Avaliacao("a1", "c", "rafa", 5), Avaliacao("a2", "c", "rafa", 2)]
    resumo = ResumoDeAvaliacoes.de(notas)
    assert resumo.quantidade == 2
    assert resumo.media == 3.5


def test_agendamento_so_e_avaliavel_depois_do_fim_e_se_nao_cancelado():
    a = agendamento()
    assert not a.avaliavel_em(datetime(2030, 1, 7, 15))
    assert a.avaliavel_em(datetime(2030, 1, 7, 15, 1))
    a.cancelar()
    assert not a.avaliavel_em(datetime(2030, 1, 8))

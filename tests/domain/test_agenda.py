from datetime import datetime

import pytest

from domain.agenda import AgendaDoBarbeiro
from domain.barbearia import Barbearia
from domain.erros import ConflitoDeHorario, DadosInvalidos
from domain.periodo import Periodo
from domain.servico import Servico


def hora(h, m=0):
    return datetime(2030, 1, 7, h, m)


def agenda_com_bloco(inicio=hora(14), fim=hora(16), agendamentos=()):
    barbearia = Barbearia(dono_id="d", nome="Barbearia Exemplo",
                          endereco="Rua Exemplo, 100", bairro="Botafogo",
                          latitude=-22.9, longitude=-43.1)
    cadeira = barbearia.adicionar_cadeira()
    horario = barbearia.publicar_horario_ocioso(
        cadeira.id, Periodo(hora(9), hora(20)), 3000)
    barbearia.reservar_bloco(horario.id, "rafa", Periodo(inicio, fim))
    return AgendaDoBarbeiro("rafa", [barbearia], list(agendamentos))


CORTE = Servico(barbeiro_id="rafa", nome="Corte", preco_centavos=4500,
                duracao_minutos=40, id="corte")


def test_horarios_disponiveis_em_passos_de_30_min_que_cabem_no_bloco():
    inicios = [h.inicio for h in
               agenda_com_bloco().horarios_disponiveis(CORTE, hora(8))]
    assert inicios == [hora(14), hora(14, 30), hora(15), hora(15, 20)]


def test_horarios_disponiveis_descontam_agendamentos():
    agenda = agenda_com_bloco()
    agenda.agendar("cliente", CORTE, hora(14, 30))
    inicios = [h.inicio for h in agenda.horarios_disponiveis(CORTE,
                                                              hora(8))]
    assert inicios == [hora(15, 10), hora(15, 20)]


def test_horarios_antes_de_agora_nao_aparecem():
    inicios = [h.inicio for h in
               agenda_com_bloco().horarios_disponiveis(CORTE, hora(15))]
    assert inicios == [hora(15), hora(15, 20)]


def test_agendar_dentro_do_bloco_cobra_o_preco_do_servico():
    agendamento = agenda_com_bloco().agendar("cliente", CORTE, hora(14))
    assert agendamento.periodo == Periodo(hora(14), hora(14, 40))
    assert agendamento.preco_centavos == 4500
    assert agendamento.servico_nome == "Corte"


def test_agendar_fora_dos_blocos_e_recusado():
    with pytest.raises(DadosInvalidos):
        agenda_com_bloco().agendar("cliente", CORTE, hora(15, 30))


def test_agendamentos_do_barbeiro_nao_se_sobrepoem():
    agenda = agenda_com_bloco()
    agenda.agendar("ana", CORTE, hora(14))
    with pytest.raises(ConflitoDeHorario):
        agenda.agendar("bia", CORTE, hora(14, 20))


def test_servico_de_outro_barbeiro_e_recusado():
    alheio = Servico(barbeiro_id="outro", nome="Corte", preco_centavos=1,
                     duracao_minutos=30)
    with pytest.raises(DadosInvalidos):
        agenda_com_bloco().agendar("cliente", alheio, hora(14))


def test_itens_juntam_bloco_barbearia_e_agendamentos():
    agenda = agenda_com_bloco()
    agenda.agendar("cliente", CORTE, hora(14))
    item, = agenda.itens
    assert item.barbearia.nome == "Barbearia Exemplo"
    assert [a.cliente_id for a in item.agendamentos] == ["cliente"]

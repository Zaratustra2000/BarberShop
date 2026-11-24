"""US5: cliente encontra o barbeiro de confiança e agenda."""
from datetime import datetime

import pytest

from domain.erros import AcessoNegado, ConflitoDeHorario, DadosInvalidos
from tests.use_cases.test_barbeiro_cadastra_servicos import cadastrar_servico
from tests.use_cases.test_barbeiro_reserva_bloco import (
    barbearia_com_horario, reservar)
from use_cases.agendar_atendimento import AgendarAtendimento
from use_cases.buscar_barbeiros import BuscarBarbeiros
from use_cases.consultar_agenda_do_barbeiro import ConsultarAgendaDoBarbeiro
from use_cases.consultar_agendamentos_do_cliente import (
    ConsultarAgendamentosDoCliente)
from use_cases.consultar_perfil_do_barbeiro import ConsultarPerfilDoBarbeiro


def h(hora, minuto=0, dia=7):
    return datetime(2030, 1, dia, hora, minuto)


@pytest.fixture
def cenario(ctx):
    """Rafa reservou 14h–16h no dia 7 e oferece um corte de 40 min."""
    barbearia, horario = barbearia_com_horario(ctx, h(13), h(18))
    rafa = ctx.cadastrar("barbeiro", nome="Rafa Souza")
    reservar(ctx, rafa, barbearia, horario, h(14), h(16))
    corte = cadastrar_servico(ctx, rafa, "Corte", 4500, 40)
    lucas = ctx.cadastrar("cliente", nome="Lucas Andrade")
    return dict(barbearia=barbearia, rafa=rafa, corte=corte, lucas=lucas)


def agendar(ctx, cliente, servico, inicio):
    return AgendarAtendimento(ctx.usuarios, ctx.barbearias, ctx.servicos,
                              ctx.agendamentos, ctx.relogio).executar(
        cliente_id=cliente.id, servico_id=servico.id, inicio=inicio)


def test_cliente_encontra_o_barbeiro_pelo_nome(ctx, cenario):
    ctx.cadastrar("dono", nome="Rafael Dono", email="rd@exemplo.com")
    achados = BuscarBarbeiros(ctx.usuarios).executar("rafa")
    assert [b.nome for b in achados] == ["Rafa Souza"]


def test_perfil_mostra_onde_o_barbeiro_atende_e_os_horarios(ctx, cenario):
    perfil = ConsultarPerfilDoBarbeiro(
        ctx.usuarios, ctx.barbearias, ctx.servicos, ctx.agendamentos,
        ctx.relogio).executar(cenario["rafa"].id, cenario["corte"].id)
    assert [i.barbearia.nome for i in perfil.agenda.itens] == [
        "Barbearia Exemplo"]
    assert [x.inicio for x in perfil.horarios] == [
        h(14), h(14, 30), h(15), h(15, 20)]


def test_agendamento_aparece_para_o_cliente_e_para_o_barbeiro(ctx, cenario):
    agendar(ctx, cenario["lucas"], cenario["corte"], h(14, 30))

    do_cliente, = ConsultarAgendamentosDoCliente(
        ctx.usuarios, ctx.barbearias, ctx.agendamentos).executar(
        cenario["lucas"].id)
    assert do_cliente.barbeiro_nome == "Rafa Souza"
    assert do_cliente.barbearia.nome == "Barbearia Exemplo"
    assert do_cliente.agendamento.preco_centavos == 4500

    visao = ConsultarAgendaDoBarbeiro(
        ctx.usuarios, ctx.barbearias, ctx.agendamentos).executar(
        cenario["rafa"].id)
    agendamento, = visao.agenda.itens[0].agendamentos
    assert visao.nomes_dos_clientes[agendamento.cliente_id] == (
        "Lucas Andrade")


def test_dois_clientes_nao_pegam_o_mesmo_horario(ctx, cenario):
    agendar(ctx, cenario["lucas"], cenario["corte"], h(14))
    outro = ctx.cadastrar("cliente", email="outro@exemplo.com")
    with pytest.raises(ConflitoDeHorario):
        agendar(ctx, outro, cenario["corte"], h(14, 20))


def test_agendamento_no_passado_e_recusado(ctx, cenario):
    ctx.relogio.ajustar(h(15, dia=7))
    with pytest.raises(DadosInvalidos):
        agendar(ctx, cenario["lucas"], cenario["corte"], h(14))


def test_barbeiro_nao_agenda_como_cliente(ctx, cenario):
    with pytest.raises(AcessoNegado):
        agendar(ctx, cenario["rafa"], cenario["corte"], h(14))

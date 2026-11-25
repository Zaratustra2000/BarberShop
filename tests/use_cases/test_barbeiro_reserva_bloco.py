"""US4: barbeiro busca cadeiras ociosas por bairro e reserva bloco."""
from datetime import datetime

import pytest

from domain.erros import AcessoNegado, ConflitoDeHorario, DadosInvalidos
from domain.periodo import Periodo
from tests.use_cases.test_dono_publica_cadeiras_ociosas import (
    cadastrar_barbearia, publicar)
from use_cases.buscar_cadeiras_ociosas import BuscarCadeirasOciosas
from use_cases.reservar_bloco_de_horario import ReservarBlocoDeHorario


def h(dia, hora, minuto=0):
    return datetime(2030, 1, dia, hora, minuto)


def barbearia_com_horario(ctx, inicio, fim, nome="Barbearia Exemplo",
                          email="dono@exemplo.com"):
    dono = ctx.cadastrar("dono", email=email)
    barbearia = cadastrar_barbearia(ctx, dono, cadeiras=1, nome=nome)
    horario = publicar(ctx, dono, barbearia, inicio, fim)
    return barbearia, horario


def reservar(ctx, barbeiro, barbearia, horario, inicio, fim):
    return ReservarBlocoDeHorario(
        ctx.usuarios, ctx.barbearias, ctx.relogio).executar(
        barbeiro_id=barbeiro.id, barbearia_id=barbearia.id,
        horario_ocioso_id=horario.id, inicio=inicio, fim=fim)


def buscar(ctx, bairro):
    return BuscarCadeirasOciosas(ctx.barbearias, ctx.relogio).executar(
        bairro)


def test_busca_sem_bairro_mostra_barbearias_ativas_e_indisponiveis(ctx):
    dono_com_horario = ctx.cadastrar("dono", email="com@exemplo.com")
    barbearia_com_horario = cadastrar_barbearia(
        ctx, dono_com_horario, nome="Com horários")
    publicar(ctx, dono_com_horario, barbearia_com_horario,
             h(7, 13), h(7, 18))

    dono_sem_horario = ctx.cadastrar("dono", email="sem@exemplo.com")
    cadastrar_barbearia(ctx, dono_sem_horario, nome="Sem horários")

    dono_desativado = ctx.cadastrar("dono", email="desativada@exemplo.com")
    barbearia_desativada = cadastrar_barbearia(
        ctx, dono_desativado, nome="Desativada")
    barbearia_desativada.desativar()
    ctx.barbearias.salvar(barbearia_desativada)

    resultados = buscar(ctx, "")

    assert [r.barbearia.nome for r in resultados] == [
        "Com horários", "Sem horários"]
    assert resultados[0].reservavel is True
    assert resultados[1].reservavel is False


def test_busca_por_bairro_ignora_acentos_e_maiusculas(ctx):
    barbearia_com_horario(ctx, h(7, 13), h(7, 18))
    resultados = buscar(ctx, "  BOTAFÓGO ")
    assert [r.barbearia.nome for r in resultados] == ["Barbearia Exemplo"]


def test_busca_por_bairro_aceita_trecho_flexivel(ctx):
    barbearia_com_horario(ctx, h(7, 13), h(7, 18))

    resultados = buscar(ctx, "tafo")

    assert [r.barbearia.nome for r in resultados] == ["Barbearia Exemplo"]


def test_busca_nao_mostra_outros_bairros(ctx):
    barbearia_com_horario(ctx, h(7, 13), h(7, 18))
    assert buscar(ctx, "Copacabana") == []


def test_busca_mostra_so_o_que_esta_livre_e_no_futuro(ctx):
    # o relógio dos testes marca 06/01/2030 08:00
    barbearia, horario = barbearia_com_horario(ctx, h(7, 13), h(7, 18))
    rafa = ctx.cadastrar("barbeiro")
    reservar(ctx, rafa, barbearia, horario, h(7, 14), h(7, 16))
    resultado, = buscar(ctx, "Botafogo")
    oferta, = resultado.ofertas
    assert oferta.periodos_livres == [Periodo(h(7, 13), h(7, 14)),
                                      Periodo(h(7, 16), h(7, 18))]


def test_horario_todo_reservado_some_da_busca(ctx):
    barbearia, horario = barbearia_com_horario(ctx, h(7, 13), h(7, 15))
    reservar(ctx, ctx.cadastrar("barbeiro"), barbearia, horario,
             h(7, 13), h(7, 15))
    resultado, = buscar(ctx, "Botafogo")
    assert resultado.reservavel is False


def test_barbeiro_reserva_bloco_que_fica_salvo_com_o_valor(ctx):
    barbearia, horario = barbearia_com_horario(ctx, h(7, 13), h(7, 18))
    rafa = ctx.cadastrar("barbeiro")
    reservar(ctx, rafa, barbearia, horario, h(7, 14), h(7, 16))
    bloco, = ctx.barbearias.por_id(barbearia.id).blocos
    assert bloco.barbeiro_id == rafa.id
    assert bloco.valor_centavos == 6000


def test_cliente_nao_reserva_bloco(ctx):
    barbearia, horario = barbearia_com_horario(ctx, h(7, 13), h(7, 18))
    with pytest.raises(AcessoNegado):
        reservar(ctx, ctx.cadastrar("cliente"), barbearia, horario,
                 h(7, 14), h(7, 16))


def test_barbeiro_nao_reserva_dois_blocos_sobrepostos_em_barbearias(ctx):
    b1, h1 = barbearia_com_horario(ctx, h(7, 13), h(7, 18), "Da Esquina",
                                   "carlos@exemplo.com")
    b2, h2 = barbearia_com_horario(ctx, h(7, 13), h(7, 18), "Do Outro",
                                   "outro@exemplo.com")
    rafa = ctx.cadastrar("barbeiro")
    reservar(ctx, rafa, b1, h1, h(7, 14), h(7, 16))
    with pytest.raises(ConflitoDeHorario):
        reservar(ctx, rafa, b2, h2, h(7, 15), h(7, 17))


def test_bloco_que_ja_comecou_e_recusado(ctx):
    barbearia, horario = barbearia_com_horario(ctx, h(6, 8), h(6, 18))
    ctx.relogio.ajustar(h(6, 10))
    with pytest.raises(DadosInvalidos):
        reservar(ctx, ctx.cadastrar("barbeiro"), barbearia, horario,
                 h(6, 9), h(6, 11))

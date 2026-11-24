"""US2: dono cadastra barbearia e publica horários ociosos."""
from datetime import datetime

import pytest

from domain.erros import (AcessoNegado, ConflitoDeHorario, DadosInvalidos)
from domain.periodo import Periodo
from use_cases.cadastrar_barbearia import CadastrarBarbearia
from use_cases.consultar_barbearias_do_dono import ConsultarBarbeariasDoDono
from use_cases.editar_perfil_da_barbearia import EditarPerfilDaBarbearia
from use_cases.editar_horario_ocioso import EditarHorarioOcioso
from use_cases.publicar_horario_ocioso import PublicarHorarioOcioso
from use_cases.gerenciar_barbearia import GerenciarBarbearia
from use_cases.buscar_cadeiras_ociosas import BuscarCadeirasOciosas
from use_cases.reservar_bloco_de_horario import ReservarBlocoDeHorario


def cadastrar_barbearia(ctx, dono, cadeiras=2, nome="Barbearia Exemplo"):
    return CadastrarBarbearia(ctx.usuarios, ctx.barbearias).executar(
        dono_id=dono.id, nome=nome, endereco="Rua Exemplo, 100",
        bairro="Botafogo", latitude=-22.951, longitude=-43.184,
        regras="Sem som alto.", quantidade_de_cadeiras=cadeiras)


def publicar(ctx, dono, barbearia, inicio, fim, preco=3000):
    return PublicarHorarioOcioso(ctx.barbearias, ctx.relogio).executar(
        dono_id=dono.id, barbearia_id=barbearia.id,
        cadeira_id=barbearia.cadeiras[0].id, inicio=inicio, fim=fim,
        preco_por_hora_centavos=preco)


def test_dono_cadastra_barbearia_com_as_cadeiras(ctx):
    dono = ctx.cadastrar("dono")
    barbearia = cadastrar_barbearia(ctx, dono, cadeiras=3)
    salva = ctx.barbearias.por_id(barbearia.id)
    assert [c.nome for c in salva.cadeiras] == [
        "Cadeira 1", "Cadeira 2", "Cadeira 3"]
    assert salva.regras == "Sem som alto."


def test_barbeiro_nao_cadastra_barbearia(ctx):
    barbeiro = ctx.cadastrar("barbeiro")
    with pytest.raises(AcessoNegado):
        cadastrar_barbearia(ctx, barbeiro)


@pytest.mark.parametrize("quantidade", [0, 31])
def test_quantidade_de_cadeiras_fora_do_limite(ctx, quantidade):
    with pytest.raises(DadosInvalidos):
        cadastrar_barbearia(ctx, ctx.cadastrar("dono"), cadeiras=quantidade)


def test_dono_ve_apenas_as_proprias_barbearias(ctx):
    carlos = ctx.cadastrar("dono", email="carlos@exemplo.com")
    outro = ctx.cadastrar("dono", email="outro@exemplo.com")
    cadastrar_barbearia(ctx, carlos, nome="Da Esquina")
    cadastrar_barbearia(ctx, outro, nome="Do Outro")
    nomes = [b.nome for b in
             ConsultarBarbeariasDoDono(ctx.barbearias).executar(carlos.id)]
    assert nomes == ["Da Esquina"]


def test_dono_publica_horario_ocioso_que_fica_salvo(ctx):
    dono = ctx.cadastrar("dono")
    barbearia = cadastrar_barbearia(ctx, dono)
    publicar(ctx, dono, barbearia,
             datetime(2030, 1, 7, 13), datetime(2030, 1, 7, 18))
    salvo = ctx.barbearias.por_id(barbearia.id).horarios_ociosos[0]
    assert salvo.periodo.minutos == 300
    assert salvo.preco_por_hora_centavos == 3000


def test_outro_dono_nao_publica_na_barbearia_alheia(ctx):
    dono = ctx.cadastrar("dono", email="carlos@exemplo.com")
    intruso = ctx.cadastrar("dono", email="intruso@exemplo.com")
    barbearia = cadastrar_barbearia(ctx, dono)
    with pytest.raises(AcessoNegado):
        publicar(ctx, intruso, barbearia,
                 datetime(2030, 1, 7, 13), datetime(2030, 1, 7, 18))


def test_horario_ocioso_no_passado_e_recusado(ctx):
    dono = ctx.cadastrar("dono")
    barbearia = cadastrar_barbearia(ctx, dono)
    with pytest.raises(DadosInvalidos):
        publicar(ctx, dono, barbearia,
                 datetime(2030, 1, 5, 13), datetime(2030, 1, 5, 18))


def test_dono_edita_perfil_e_cadeiras_ficam_persistidas(ctx):
    dono = ctx.cadastrar("dono")
    barbearia = cadastrar_barbearia(ctx, dono, cadeiras=1)
    EditarPerfilDaBarbearia(ctx.usuarios, ctx.barbearias).executar(
        dono_id=dono.id, barbearia_id=barbearia.id,
        nome="Nova Barbershop", endereco="Rua Nova, 20",
        bairro="Copacabana", latitude=-22.967, longitude=-43.178,
        regras="Sem atrasos.", quantidade_de_cadeiras=3)
    salva = ctx.barbearias.por_id(barbearia.id)
    assert (salva.nome, salva.endereco, salva.bairro, salva.regras) == (
        "Nova Barbershop", "Rua Nova, 20", "Copacabana", "Sem atrasos.")
    assert [c.nome for c in salva.cadeiras] == [
        "Cadeira 1", "Cadeira 2", "Cadeira 3"]


def test_outro_dono_nao_edita_perfil(ctx):
    dono = ctx.cadastrar("dono", email="dono@exemplo.com")
    intruso = ctx.cadastrar("dono", email="intruso@exemplo.com")
    barbearia = cadastrar_barbearia(ctx, dono)
    with pytest.raises(AcessoNegado):
        EditarPerfilDaBarbearia(ctx.usuarios, ctx.barbearias).executar(
            dono_id=intruso.id, barbearia_id=barbearia.id,
            nome="Nome falso", endereco="Rua Falsa, 1", bairro="Centro",
            latitude=-22.9, longitude=-43.2, regras="",
            quantidade_de_cadeiras=1)


def test_dono_remove_cadeira_sem_referencias(ctx):
    dono = ctx.cadastrar("dono")
    barbearia = cadastrar_barbearia(ctx, dono, cadeiras=2)
    cadeira = barbearia.cadeiras[1]
    EditarPerfilDaBarbearia(ctx.usuarios, ctx.barbearias).remover_cadeira(
        dono_id=dono.id, barbearia_id=barbearia.id,
        cadeira_id=cadeira.id)
    salva = ctx.barbearias.por_id(barbearia.id)
    assert [c.nome for c in salva.cadeiras] == ["Cadeira 1"]


def test_dono_edita_horario_ocioso_e_fica_salvo(ctx):
    dono = ctx.cadastrar("dono")
    barbearia = cadastrar_barbearia(ctx, dono)
    horario = publicar(ctx, dono, barbearia,
                       datetime(2030, 1, 7, 13),
                       datetime(2030, 1, 7, 18))

    EditarHorarioOcioso(
        ctx.usuarios, ctx.barbearias, ctx.relogio).executar(
            dono_id=dono.id, barbearia_id=barbearia.id,
            horario_ocioso_id=horario.id,
            cadeira_id=barbearia.cadeiras[0].id,
            inicio=datetime(2030, 1, 7, 14),
            fim=datetime(2030, 1, 7, 17),
            preco_por_hora_centavos=4500)

    salvo = ctx.barbearias.por_id(barbearia.id).horario_ocioso(horario.id)
    assert salvo.periodo == Periodo(
        datetime(2030, 1, 7, 14), datetime(2030, 1, 7, 17))
    assert salvo.preco_por_hora_centavos == 4500


def test_outro_dono_nao_edita_horario_ocioso(ctx):
    dono = ctx.cadastrar("dono", email="dono@exemplo.com")
    intruso = ctx.cadastrar("dono", email="intruso@exemplo.com")
    barbearia = cadastrar_barbearia(ctx, dono)
    horario = publicar(ctx, dono, barbearia,
                       datetime(2030, 1, 7, 13),
                       datetime(2030, 1, 7, 18))

    with pytest.raises(AcessoNegado):
        EditarHorarioOcioso(
            ctx.usuarios, ctx.barbearias, ctx.relogio).executar(
                dono_id=intruso.id, barbearia_id=barbearia.id,
                horario_ocioso_id=horario.id,
                cadeira_id=barbearia.cadeiras[0].id,
                inicio=datetime(2030, 1, 7, 14),
                fim=datetime(2030, 1, 7, 17),
                preco_por_hora_centavos=4500)


def test_dono_exclui_horario_ocioso_sem_blocos(ctx):
    dono = ctx.cadastrar("dono")
    barbearia = cadastrar_barbearia(ctx, dono)
    horario = publicar(ctx, dono, barbearia,
                       datetime(2030, 1, 7, 13),
                       datetime(2030, 1, 7, 18))

    EditarHorarioOcioso(
        ctx.usuarios, ctx.barbearias, ctx.relogio).excluir(
            dono_id=dono.id, barbearia_id=barbearia.id,
            horario_ocioso_id=horario.id)

    salva = ctx.barbearias.por_id(barbearia.id)
    assert salva.horarios_ociosos == []


def test_dono_nao_exclui_horario_ocioso_com_bloco(ctx):
    dono = ctx.cadastrar("dono")
    barbearia = cadastrar_barbearia(ctx, dono)
    horario = publicar(ctx, dono, barbearia,
                       datetime(2030, 1, 7, 13),
                       datetime(2030, 1, 7, 18))
    salva = ctx.barbearias.por_id(barbearia.id)
    salva.reservar_bloco(
        horario.id, "barbeiro-1", Periodo(
            datetime(2030, 1, 7, 14), datetime(2030, 1, 7, 15)))
    ctx.barbearias.salvar(salva)

    with pytest.raises(ConflitoDeHorario):
        EditarHorarioOcioso(
            ctx.usuarios, ctx.barbearias, ctx.relogio).excluir(
                dono_id=dono.id, barbearia_id=barbearia.id,
                horario_ocioso_id=horario.id)


def test_dono_exclui_barbearia_sem_blocos_de_horario(ctx):
    dono = ctx.cadastrar("dono")
    barbearia = cadastrar_barbearia(ctx, dono)

    GerenciarBarbearia(ctx.usuarios, ctx.barbearias).excluir(
        dono_id=dono.id, barbearia_id=barbearia.id)

    assert ctx.barbearias.por_id(barbearia.id) is None


def test_dono_desativa_barbearia_com_bloco_e_preserva_historico(ctx):
    dono = ctx.cadastrar("dono")
    barbearia = cadastrar_barbearia(ctx, dono)
    horario = publicar(ctx, dono, barbearia,
                       datetime(2030, 1, 7, 13),
                       datetime(2030, 1, 7, 18))
    salva = ctx.barbearias.por_id(barbearia.id)
    bloco = salva.reservar_bloco(
        horario.id, "barbeiro-1", Periodo(
            datetime(2030, 1, 7, 14), datetime(2030, 1, 7, 15)))
    ctx.barbearias.salvar(salva)

    GerenciarBarbearia(ctx.usuarios, ctx.barbearias).desativar(
        dono_id=dono.id, barbearia_id=barbearia.id)

    desativada = ctx.barbearias.por_id(barbearia.id)
    assert desativada.ativa is False
    assert desativada.blocos[0].id == bloco.id


def test_barbearia_desativada_sai_da_busca_e_nao_recebe_novos_blocos(ctx):
    dono = ctx.cadastrar("dono")
    barbeiro = ctx.cadastrar("barbeiro")
    barbearia = cadastrar_barbearia(ctx, dono)
    horario = publicar(ctx, dono, barbearia,
                       datetime(2030, 1, 7, 13),
                       datetime(2030, 1, 7, 18))
    GerenciarBarbearia(ctx.usuarios, ctx.barbearias).desativar(
        dono_id=dono.id, barbearia_id=barbearia.id)

    ofertas = BuscarCadeirasOciosas(
        ctx.barbearias, ctx.relogio).executar("Botafogo")
    assert ofertas == []

    with pytest.raises(DadosInvalidos):
        ReservarBlocoDeHorario(
            ctx.usuarios, ctx.barbearias, ctx.relogio).executar(
                barbeiro_id=barbeiro.id, barbearia_id=barbearia.id,
                horario_ocioso_id=horario.id,
                inicio=datetime(2030, 1, 7, 14),
                fim=datetime(2030, 1, 7, 15))


@pytest.mark.parametrize("operacao", ["excluir", "desativar"])
def test_outro_dono_nao_gerencia_barbearia_alheia(ctx, operacao):
    dono = ctx.cadastrar("dono", email="dono@exemplo.com")
    intruso = ctx.cadastrar("dono", email="intruso@exemplo.com")
    barbearia = cadastrar_barbearia(ctx, dono)

    with pytest.raises(AcessoNegado):
        getattr(GerenciarBarbearia(
            ctx.usuarios, ctx.barbearias), operacao)(
                dono_id=intruso.id, barbearia_id=barbearia.id)

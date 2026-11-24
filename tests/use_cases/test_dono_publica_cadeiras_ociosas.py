"""US2: dono cadastra barbearia e publica horários ociosos."""
from datetime import datetime

import pytest

from domain.erros import AcessoNegado, DadosInvalidos
from use_cases.cadastrar_barbearia import CadastrarBarbearia
from use_cases.consultar_barbearias_do_dono import ConsultarBarbeariasDoDono
from use_cases.publicar_horario_ocioso import PublicarHorarioOcioso


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

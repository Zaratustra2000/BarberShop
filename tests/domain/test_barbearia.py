from datetime import datetime

import pytest

from domain.barbearia import Barbearia
from domain.erros import ConflitoDeHorario, DadosInvalidos, NaoEncontrado
from domain.periodo import Periodo


def barbearia(**kw):
    dados = dict(dono_id="dono-1", nome="Barbearia Exemplo",
                 endereco="Rua Exemplo, 100", bairro="Botafogo",
                 latitude=-22.951, longitude=-43.184)
    dados.update(kw)
    return Barbearia(**dados)


def hora(h, m=0, dia=7):
    return datetime(2030, 1, dia, h, m)


@pytest.mark.parametrize("campo,valor", [
    ("nome", " "), ("endereco", ""), ("bairro", ""),
    ("latitude", -91), ("longitude", 181),
])
def test_barbearia_valida_dados_obrigatorios(campo, valor):
    with pytest.raises(DadosInvalidos):
        barbearia(**{campo: valor})


def test_cadeiras_sao_numeradas_na_ordem():
    b = barbearia()
    b.adicionar_cadeira()
    b.adicionar_cadeira()
    assert [c.nome for c in b.cadeiras] == ["Cadeira 1", "Cadeira 2"]


def test_perfil_da_barbearia_pode_ser_editado():
    b = barbearia()
    b.editar(nome="Nova Barbershop", endereco="Rua Nova, 20",
             bairro="Copacabana", latitude=-22.967, longitude=-43.178,
             regras="Sem atrasos.")
    assert (b.nome, b.endereco, b.bairro, b.latitude, b.longitude,
            b.regras) == ("Nova Barbershop", "Rua Nova, 20", "Copacabana",
                          -22.967, -43.178, "Sem atrasos.")


def test_barbearia_pode_receber_foto_principal():
    b = barbearia()
    b.definir_foto_principal("barbearia-exemplo.webp")
    assert b.foto_principal == "barbearia-exemplo.webp"


def test_cadeira_sem_referencias_pode_ser_removida():
    b = barbearia()
    cadeira = b.adicionar_cadeira()
    b.remover_cadeira(cadeira.id)
    assert b.cadeiras == []


def test_cadeira_com_horario_ocioso_nao_pode_ser_removida():
    b = barbearia()
    cadeira = b.adicionar_cadeira()
    b.publicar_horario_ocioso(
        cadeira.id, Periodo(hora(13), hora(18)), 3000)
    with pytest.raises(ConflitoDeHorario):
        b.remover_cadeira(cadeira.id)


def test_cadeira_com_bloco_nao_pode_ser_removida():
    b, horario = com_horario_ocioso()
    b.reservar_bloco(horario.id, "rafa",
                     Periodo(hora(14), hora(15)))
    with pytest.raises(ConflitoDeHorario):
        b.remover_cadeira(horario.cadeira_id)


def test_publicar_horario_ocioso_em_cadeira_da_barbearia():
    b = barbearia()
    cadeira = b.adicionar_cadeira()
    horario = b.publicar_horario_ocioso(
        cadeira.id, Periodo(hora(13), hora(18)), 3000)
    assert b.horarios_ociosos == [horario]
    assert horario.preco_por_hora_centavos == 3000


def test_cadeira_de_outra_barbearia_nao_e_encontrada():
    with pytest.raises(NaoEncontrado):
        barbearia().publicar_horario_ocioso(
            "cadeira-alheia", Periodo(hora(13), hora(18)), 3000)


def test_preco_por_hora_precisa_ser_positivo():
    b = barbearia()
    cadeira = b.adicionar_cadeira()
    with pytest.raises(DadosInvalidos):
        b.publicar_horario_ocioso(cadeira.id, Periodo(hora(13), hora(18)), 0)


def test_horarios_ociosos_da_mesma_cadeira_nao_se_sobrepoem():
    b = barbearia()
    cadeira = b.adicionar_cadeira()
    b.publicar_horario_ocioso(cadeira.id, Periodo(hora(13), hora(18)), 3000)
    with pytest.raises(ConflitoDeHorario):
        b.publicar_horario_ocioso(cadeira.id, Periodo(hora(17), hora(19)),
                                  3000)


def test_cadeiras_diferentes_podem_ter_o_mesmo_horario():
    b = barbearia()
    c1, c2 = b.adicionar_cadeira(), b.adicionar_cadeira()
    b.publicar_horario_ocioso(c1.id, Periodo(hora(13), hora(18)), 3000)
    b.publicar_horario_ocioso(c2.id, Periodo(hora(13), hora(18)), 3000)
    assert len(b.horarios_ociosos) == 2


def com_horario_ocioso(preco=3000):
    b = barbearia()
    cadeira = b.adicionar_cadeira()
    horario = b.publicar_horario_ocioso(
        cadeira.id, Periodo(hora(13), hora(18)), preco)
    return b, horario


def test_bloco_custa_preco_por_hora_vezes_duracao():
    b, horario = com_horario_ocioso(preco=3000)
    bloco = b.reservar_bloco(horario.id, "rafa",
                             Periodo(hora(14), hora(15, 30)))
    assert bloco.valor_centavos == 4500
    assert b.blocos == [bloco]


def test_bloco_precisa_caber_no_horario_ocioso():
    b, horario = com_horario_ocioso()
    with pytest.raises(DadosInvalidos):
        b.reservar_bloco(horario.id, "rafa", Periodo(hora(17), hora(19)))


def test_blocos_na_mesma_cadeira_nao_se_sobrepoem():
    b, horario = com_horario_ocioso()
    b.reservar_bloco(horario.id, "rafa", Periodo(hora(13), hora(15)))
    with pytest.raises(ConflitoDeHorario):
        b.reservar_bloco(horario.id, "outro", Periodo(hora(14), hora(16)))


def test_periodos_livres_descontam_os_blocos():
    b, horario = com_horario_ocioso()
    b.reservar_bloco(horario.id, "rafa", Periodo(hora(14), hora(15)))
    assert b.periodos_livres(horario.id) == [Periodo(hora(13), hora(14)),
                                             Periodo(hora(15), hora(18))]


def test_horario_ocioso_inexistente_nao_e_encontrado():
    with pytest.raises(NaoEncontrado):
        barbearia().reservar_bloco("x", "rafa", Periodo(hora(13), hora(14)))

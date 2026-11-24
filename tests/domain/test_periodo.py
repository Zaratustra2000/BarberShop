from datetime import datetime

import pytest

from domain.erros import DadosInvalidos
from domain.periodo import Periodo


def p(inicio, fim):
    return Periodo(datetime(2030, 1, 7, *inicio), datetime(2030, 1, 7, *fim))


def test_periodo_exige_fim_depois_do_inicio():
    with pytest.raises(DadosInvalidos):
        p((10, 0), (10, 0))


def test_duracao_em_minutos():
    assert p((9, 0), (10, 30)).minutos == 90


def test_periodos_que_se_cruzam_se_sobrepoem():
    assert p((9, 0), (11, 0)).sobrepoe(p((10, 0), (12, 0)))


def test_periodos_encostados_nao_se_sobrepoem():
    assert not p((9, 0), (10, 0)).sobrepoe(p((10, 0), (11, 0)))


def test_contem_periodo_interno():
    assert p((9, 0), (18, 0)).contem(p((10, 0), (12, 0)))


def test_nao_contem_periodo_que_vaza():
    assert not p((9, 0), (12, 0)).contem(p((11, 0), (13, 0)))


def test_subtrair_devolve_os_trechos_livres():
    livres = p((9, 0), (18, 0)).subtrair([p((10, 0), (12, 0)),
                                          p((14, 0), (15, 0))])
    assert livres == [p((9, 0), (10, 0)),
                      p((12, 0), (14, 0)),
                      p((15, 0), (18, 0))]


def test_subtrair_tudo_nao_deixa_trecho_livre():
    assert p((9, 0), (10, 0)).subtrair([p((8, 0), (11, 0))]) == []

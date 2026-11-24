from datetime import datetime

from domain.periodo import Periodo
from tests.infra.test_contrato_barbearias import nova_barbearia


def com_bloco(barbeiro_id="rafa", bairro="Botafogo"):
    b = nova_barbearia(bairro=bairro)
    b.reservar_bloco(b.horarios_ociosos[0].id, barbeiro_id,
                     Periodo(datetime(2030, 1, 7, 14),
                             datetime(2030, 1, 7, 16)))
    return b


def test_blocos_voltam_com_a_barbearia(repos):
    barbearias = repos["barbearias"]
    b = com_bloco()
    barbearias.salvar(b)
    assert barbearias.por_id(b.id).blocos == b.blocos


def test_barbearias_no_bairro_pela_chave_normalizada(repos):
    barbearias = repos["barbearias"]
    jardim, centro = (nova_barbearia(bairro="Jardim Botânico"),
                      nova_barbearia(bairro="Centro"))
    barbearias.salvar(jardim)
    barbearias.salvar(centro)
    assert [b.id for b in barbearias.no_bairro("jardim botanico")] == [
        jardim.id]


def test_barbearias_onde_o_barbeiro_tem_bloco(repos):
    barbearias = repos["barbearias"]
    com_rafa, sem_rafa = com_bloco("rafa"), com_bloco("outro")
    barbearias.salvar(com_rafa)
    barbearias.salvar(sem_rafa)
    assert [b.id for b in barbearias.com_blocos_do_barbeiro("rafa")] == [
        com_rafa.id]

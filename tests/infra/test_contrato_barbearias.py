from datetime import datetime

from domain.barbearia import Barbearia
from domain.periodo import Periodo


def nova_barbearia(dono_id="dono-1", bairro="Botafogo"):
    b = Barbearia(dono_id=dono_id, nome="Barbearia Exemplo",
                  endereco="Rua Exemplo, 100", bairro=bairro,
                  latitude=-22.951, longitude=-43.184, regras="Sem som alto.")
    cadeira = b.adicionar_cadeira()
    b.publicar_horario_ocioso(
        cadeira.id,
        Periodo(datetime(2030, 1, 7, 13), datetime(2030, 1, 7, 18)), 3000)
    return b


def test_barbearia_volta_inteira_com_cadeiras_e_horarios(repos):
    barbearias = repos["barbearias"]
    b = nova_barbearia()
    barbearias.salvar(b)
    assert barbearias.por_id(b.id) == b


def test_salvar_de_novo_grava_os_itens_novos(repos):
    barbearias = repos["barbearias"]
    b = nova_barbearia()
    barbearias.salvar(b)
    b.adicionar_cadeira()
    barbearias.salvar(b)
    assert len(barbearias.por_id(b.id).cadeiras) == 2


def test_barbearias_do_dono(repos):
    barbearias = repos["barbearias"]
    minha, alheia = nova_barbearia("dono-1"), nova_barbearia("dono-2")
    barbearias.salvar(minha)
    barbearias.salvar(alheia)
    assert [b.id for b in barbearias.do_dono("dono-1")] == [minha.id]


def test_lista_somente_barbearias_ativas(repos):
    barbearias = repos["barbearias"]
    ativa = nova_barbearia(bairro="Botafogo")
    desativada = nova_barbearia(bairro="Copacabana")
    desativada.desativar()
    barbearias.salvar(ativa)
    barbearias.salvar(desativada)

    assert [b.id for b in barbearias.ativas()] == [ativa.id]


def test_filtro_por_bairro_aceita_trecho_normalizado(repos):
    barbearias = repos["barbearias"]
    encontrada = nova_barbearia(bairro="Jardim Botânico")
    outra = nova_barbearia(bairro="Copacabana")
    barbearias.salvar(encontrada)
    barbearias.salvar(outra)

    achadas = barbearias.no_bairro("botan")

    assert [b.id for b in achadas] == [encontrada.id]


def test_barbearia_inexistente_devolve_none(repos):
    assert repos["barbearias"].por_id("nao-existe") is None


def test_editar_barbearia_preserva_horarios(repos):
    barbearias = repos["barbearias"]
    b = nova_barbearia()
    barbearias.salvar(b)
    b.editar(nome="Barbearia Atualizada", endereco="Rua Nova, 10",
             bairro="Copacabana", latitude=-22.967, longitude=-43.178,
             regras="Som baixo.")
    barbearias.salvar(b)
    salva = barbearias.por_id(b.id)
    assert salva.nome == "Barbearia Atualizada"
    assert salva.endereco == "Rua Nova, 10"
    assert len(salva.horarios_ociosos) == 1
    assert len(salva.cadeiras) == 1


def test_foto_principal_e_persistida(repos):
    barbearias = repos["barbearias"]
    b = nova_barbearia()
    b.definir_foto_principal("barbearia-exemplo.webp")
    barbearias.salvar(b)
    assert barbearias.por_id(b.id).foto_principal == (
        "barbearia-exemplo.webp")


def test_remover_cadeira_sem_referencias(repos):
    barbearias = repos["barbearias"]
    b = nova_barbearia()
    segunda = b.adicionar_cadeira()
    barbearias.salvar(b)
    b.remover_cadeira(segunda.id)
    barbearias.salvar(b)
    salva = barbearias.por_id(b.id)
    assert [c.nome for c in salva.cadeiras] == ["Cadeira 1"]


def test_editar_horario_ocioso_persiste_alteracoes(repos):
    barbearias = repos["barbearias"]
    b = nova_barbearia()
    horario = b.horarios_ociosos[0]
    barbearias.salvar(b)

    b.editar_horario_ocioso(
        horario.id, horario.cadeira_id,
        Periodo(datetime(2030, 1, 7, 14), datetime(2030, 1, 7, 16)), 4500)
    barbearias.salvar(b)

    salvo = barbearias.por_id(b.id).horario_ocioso(horario.id)
    assert salvo.periodo == Periodo(
        datetime(2030, 1, 7, 14), datetime(2030, 1, 7, 16))
    assert salvo.preco_por_hora_centavos == 4500


def test_excluir_horario_ocioso_persiste_remocao(repos):
    barbearias = repos["barbearias"]
    b = nova_barbearia()
    horario = b.horarios_ociosos[0]
    barbearias.salvar(b)

    b.excluir_horario_ocioso(horario.id)
    barbearias.salvar(b)

    assert barbearias.por_id(b.id).horarios_ociosos == []


def test_desativacao_persiste_e_preserva_blocos(repos):
    barbearias = repos["barbearias"]
    b = nova_barbearia()
    horario = b.horarios_ociosos[0]
    bloco = b.reservar_bloco(
        horario.id, "barbeiro-1",
        Periodo(datetime(2030, 1, 7, 14), datetime(2030, 1, 7, 15)))
    barbearias.salvar(b)

    b.desativar()
    barbearias.salvar(b)

    salva = barbearias.por_id(b.id)
    assert salva.ativa is False
    assert [b.id for b in salva.blocos] == [bloco.id]


def test_remover_barbearia_persiste_nos_dois_adapters(repos):
    barbearias = repos["barbearias"]
    b = nova_barbearia()
    barbearias.salvar(b)

    barbearias.remover(b.id)

    assert barbearias.por_id(b.id) is None

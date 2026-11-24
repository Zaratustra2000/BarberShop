from datetime import datetime

from domain.agendamento import Agendamento
from domain.periodo import Periodo
from domain.usuario import Papel, Usuario


def agendamento(cliente_id="lucas", barbeiro_id="rafa", hora=14):
    return Agendamento(
        cliente_id=cliente_id, barbeiro_id=barbeiro_id, servico_id="corte",
        servico_nome="Corte", barbearia_id="b1", bloco_id="bloco1",
        periodo=Periodo(datetime(2030, 1, 7, hora),
                        datetime(2030, 1, 7, hora, 40)),
        preco_centavos=4500)


def test_agendamentos_por_barbeiro_e_por_cliente_em_ordem(repos):
    agendamentos = repos["agendamentos"]
    tarde, cedo = agendamento(hora=15), agendamento(hora=14)
    alheio = agendamento(cliente_id="ana", barbeiro_id="outro")
    for a in (tarde, cedo, alheio):
        agendamentos.salvar(a)
    assert agendamentos.do_barbeiro("rafa") == [cedo, tarde]
    assert agendamentos.do_cliente("ana") == [alheio]


def test_agendamento_cancelado_sobrevive_a_salvar_e_carregar(repos):
    agendamentos = repos["agendamentos"]
    original = agendamento()
    original.cancelar()

    agendamentos.salvar(original)

    carregado = agendamentos.por_id(original.id)
    assert carregado == original
    assert carregado.cancelado


def test_barbeiros_por_nome_ignora_maiusculas_e_outras_personas(repos):
    usuarios = repos["usuarios"]
    for i, (nome, papel) in enumerate((("Rafa Souza", Papel.BARBEIRO),
                                       ("Rafaela Lima", Papel.BARBEIRO),
                                       ("Rafael Dono", Papel.DONO),
                                       ("Bruno Costa", Papel.BARBEIRO))):
        usuarios.salvar(Usuario(nome=nome, email="u{}@exemplo.com".format(i),
                                senha_hash="h", papel=papel))
    assert [u.nome for u in usuarios.barbeiros_por_nome("RAFA")] == [
        "Rafa Souza", "Rafaela Lima"]

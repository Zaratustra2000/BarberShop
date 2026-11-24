"""Passos de tela reaproveitados pelos smoke tests."""
from tests.app.conftest import cadastrar_e_entrar, extrair
from tests.app.test_rotas_dono import criar_barbearia


def sair(client):
    client.post("/logout")


def dono_publica_horario(client, inicio="2030-01-07T13:00",
                         fim="2030-01-07T18:00", preco="30,00"):
    cadastrar_e_entrar(client, "dono")
    pagina = criar_barbearia(client).get_data(as_text=True)
    barbearia_id = extrair(r'/dono/barbearias/(\w+)/horarios', pagina)
    cadeira_id = extrair(r'<option value="(\w+)">Cadeira 1', pagina)
    client.post("/dono/barbearias/{}/horarios".format(barbearia_id),
                data=dict(cadeira_id=cadeira_id, inicio=inicio, fim=fim,
                          preco_por_hora=preco))
    sair(client)

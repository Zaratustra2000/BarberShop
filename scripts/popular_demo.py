"""Popula um banco local com dados SINTÉTICOS para demonstração.

Uso:  python -m scripts.popular_demo
Todos os nomes, e-mails e endereços são fictícios. A senha de demonstração
vale só para este banco local.
"""
import os
from datetime import datetime, timedelta

from app.main import create_app

SENHA_DEMO = os.environ.get("BARBERSHOP_SENHA_DEMO", "demo123")


def amanha_as(hora):
    base = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    return base + timedelta(days=1, hours=hora)


def main():
    app = create_app()
    c = app.extensions["barbershop"]
    if c.usuarios.por_email("carlos@exemplo.com"):
        print("Banco já populado.")
        return

    def conta(nome, email, papel):
        return c.cadastrar_usuario.executar(nome=nome, email=email,
                                            senha=SENHA_DEMO, papel=papel)

    carlos = conta("Carlos Menezes", "carlos@exemplo.com", "dono")
    rafa = conta("Rafa Souza", "rafa@exemplo.com", "barbeiro")
    lucas = conta("Lucas Andrade", "lucas@exemplo.com", "cliente")

    botafogo = c.cadastrar_barbearia.executar(
        dono_id=carlos.id, nome="Barbearia do Carlos",
        endereco="Rua Fictícia, 123", bairro="Botafogo",
        latitude=-22.9519, longitude=-43.1849,
        regras="Chegar 10 min antes. Sem som alto.",
        quantidade_de_cadeiras=6)
    copa = c.cadastrar_barbearia.executar(
        dono_id=carlos.id, nome="Navalha de Copa",
        endereco="Av. Exemplo, 456", bairro="Copacabana",
        latitude=-22.9711, longitude=-43.1863, regras="",
        quantidade_de_cadeiras=3)

    for barbearia in (botafogo, copa):
        for cadeira in barbearia.cadeiras[:2]:
            c.publicar_horario_ocioso.executar(
                dono_id=carlos.id, barbearia_id=barbearia.id,
                cadeira_id=cadeira.id, inicio=amanha_as(13),
                fim=amanha_as(19), preco_por_hora_centavos=3000)

    c.cadastrar_servico.executar(barbeiro_id=rafa.id, nome="Corte degradê",
                                 preco_centavos=5000, duracao_minutos=40)
    c.cadastrar_servico.executar(barbeiro_id=rafa.id, nome="Barba",
                                 preco_centavos=3000, duracao_minutos=30)

    oferta = c.buscar_cadeiras_ociosas.executar("Botafogo")[0]
    c.reservar_bloco_de_horario.executar(
        barbeiro_id=rafa.id, barbearia_id=oferta.barbearia.id,
        horario_ocioso_id=oferta.horario.id, inicio=amanha_as(14),
        fim=amanha_as(17))
    servico = c.consultar_servicos_do_barbeiro.executar(rafa.id)[1]
    c.agendar_atendimento.executar(cliente_id=lucas.id,
                                   servico_id=servico.id,
                                   inicio=amanha_as(15))
    print("Pronto. Contas de demonstração (senha: {}):".format(SENHA_DEMO))
    for email in ("carlos@exemplo.com (dono)", "rafa@exemplo.com (barbeiro)",
                  "lucas@exemplo.com (cliente)"):
        print("  -", email)


if __name__ == "__main__":
    main()

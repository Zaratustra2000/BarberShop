"""Popula um banco local com dados SINTÉTICOS para demonstração.

Uso:  python -m scripts.popular_demo
Todos os nomes, e-mails e endereços são fictícios. A senha de demonstração
vale só para este banco local.
"""
import os
from io import BytesIO
import random
from datetime import datetime, timedelta

from PIL import Image, ImageDraw

from app.main import create_app
from domain.erros import ErroDeDominio
from use_cases.portas import Relogio

SENHA_DEMO = os.environ.get("BARBERSHOP_SENHA_DEMO", "demo123")


def foto_demo(nome, cor_fundo, cor_destaque):
    imagem = Image.new("RGB", (800, 500), cor_fundo)
    desenho = ImageDraw.Draw(imagem)
    desenho.rectangle((0, 0, 800, 55), fill=cor_destaque)
    desenho.rectangle((70, 95, 730, 405), outline=cor_destaque, width=12)
    centro_x = 400
    for indice, cor in enumerate(
            (cor_destaque, "#f8f4e8", "#2b6f77", "#f8f4e8")):
        x = 280 + indice * 60
        desenho.rounded_rectangle(
            (x, 150, x + 48, 330), radius=24, fill=cor)
    desenho.text((centro_x, 360), nome, fill="#f8f4e8",
                 anchor="mm", font=None)
    buffer = BytesIO()
    imagem.save(buffer, format="PNG")
    return buffer.getvalue()


DONOS = (
    ("Carlos Menezes", "carlos@exemplo.com"),
    ("Marina Teixeira", "marina@exemplo.com"),
    ("Otávio Brandão", "otavio@exemplo.com"),
)

# (dono, nome, endereço, bairro, latitude, longitude, regras, cadeiras,
#  cor de fundo, cor de destaque)
BARBEARIAS = (
    (0, "Barbearia do Carlos", "Rua Fictícia, 123", "Botafogo",
     -22.9519, -43.1849, "Chegar 10 min antes. Sem som alto.", 6,
     "#111827", "#c59a5b"),
    (0, "Navalha de Copa", "Av. Exemplo, 456", "Copacabana",
     -22.9711, -43.1863, "", 3, "#183153", "#d5b36a"),
    (1, "Ipanema Barber Club", "Rua Imaginária, 78", "Ipanema",
     -22.9838, -43.2096, "Pagamento presencial. Traga seus produtos.", 4,
     "#2d1b2e", "#e0a458"),
    (1, "Leblon Tesoura & Navalha", "Rua Modelo, 210", "Leblon",
     -22.9866, -43.2236, "Higienizar as ferramentas a cada cliente.", 3,
     "#0f2e2b", "#d9c27a"),
    (2, "Tijuca Old School", "Rua do Exemplo, 35", "Tijuca",
     -22.9249, -43.2326, "Música ambiente baixa.", 5,
     "#3a1f12", "#e6b566"),
    (2, "Lapa Corte Livre", "Rua Teste, 99", "Lapa",
     -22.9133, -43.1805, "", 4, "#1c1c2e", "#c2784f"),
    (1, "Flamengo Cadeira Dourada", "Rua Amostra, 14", "Flamengo",
     -22.9340, -43.1757, "Avisar se for atrasar.", 2,
     "#222a35", "#caa64b"),
    (0, "Centro Barber House", "Rua Fictícia, 500", "Centro",
     -22.9035, -43.1729, "Aberto de segunda a sábado.", 6,
     "#1b2a1f", "#d1b36a"),
)

# (nome, e-mail, apresentação, [(serviço, preço em centavos, minutos)])
BARBEIROS = (
    ("Rafa Souza", "rafa@exemplo.com",
     "Cortes clássicos e degradês há 8 anos.",
     (("Corte degradê", 5000, 40), ("Barba", 3000, 30))),
    ("Bruno Costa", "bruno@exemplo.com", "Especialista em barba e navalha.",
     (("Barba na navalha", 3500, 30), ("Corte social", 4000, 30),
      ("Corte + barba", 6500, 60))),
    ("Diego Alves", "diego@exemplo.com", "Cabelo infantil e platinado.",
     (("Corte infantil", 3000, 30), ("Platinado", 15000, 90))),
    ("Felipe Rocha", "felipe@exemplo.com", "Pigmentação e acabamento.",
     (("Corte degradê", 4500, 40), ("Pigmentação", 6000, 30))),
    ("Gustavo Lima", "gustavo@exemplo.com", "Estilo moderno e rápido.",
     (("Corte na tesoura", 5500, 45), ("Sobrancelha", 1500, 15))),
    ("Henrique Dias", "henrique@exemplo.com",
     "Novo na plataforma, ainda sem avaliações.",
     (("Corte simples", 3500, 30),)),
)

CLIENTES = (
    ("Lucas Andrade", "lucas@exemplo.com"),
    ("Ana Beatriz", "ana@exemplo.com"),
    ("Pedro Henrique", "pedro@exemplo.com"),
    ("Camila Ferreira", "camila@exemplo.com"),
    ("João Victor", "joao@exemplo.com"),
    ("Mariana Costa", "mariana@exemplo.com"),
    ("Thiago Martins", "thiago@exemplo.com"),
    ("Larissa Gomes", "larissa@exemplo.com"),
    ("Rodrigo Pires", "rodrigo@exemplo.com"),
    ("Beatriz Nunes", "beatriz@exemplo.com"),
    ("Gabriel Santos", "gabriel@exemplo.com"),
    ("Fernanda Lopes", "fernanda@exemplo.com"),
)


def dia_as(dias, hora, agora):
    base = agora.replace(hour=0, minute=0, second=0, microsecond=0)
    return base + timedelta(days=dias, hours=hora)


def popular(app):
    c = app.extensions["barbershop"]
    agora = c.relogio.agora()
    if c.usuarios.por_email("carlos@exemplo.com"):
        print("Banco já populado.")
        return False
    sorteio = random.Random(2024)
    viagem = getattr(c.relogio, "ajustar", None)

    def conta(nome, email, papel):
        return c.cadastrar_usuario.executar(nome=nome, email=email,
                                            senha=SENHA_DEMO, papel=papel)

    donos = [conta(nome, email, "dono") for nome, email in DONOS]
    clientes = [conta(nome, email, "cliente") for nome, email in CLIENTES]
    barbeiros = []
    for nome, email, apresentacao, servicos in BARBEIROS:
        barbeiro = conta(nome, email, "barbeiro")
        c.editar_perfil_do_barbeiro.executar(barbeiro.id, nome, apresentacao)
        for servico, preco, minutos in servicos:
            c.cadastrar_servico.executar(
                barbeiro_id=barbeiro.id, nome=servico,
                preco_centavos=preco, duracao_minutos=minutos)
        barbeiros.append(barbeiro)

    barbearias = []
    for (indice_dono, nome, endereco, bairro, lat, lng, regras, cadeiras,
         fundo, destaque) in BARBEARIAS:
        dono = donos[indice_dono]
        barbearia = c.cadastrar_barbearia.executar(
            dono_id=dono.id, nome=nome, endereco=endereco, bairro=bairro,
            latitude=lat, longitude=lng, regras=regras,
            quantidade_de_cadeiras=cadeiras)
        c.substituir_foto_principal.executar(
            dono_id=dono.id, barbearia_id=barbearia.id,
            conteudo=foto_demo(nome.upper(), fundo, destaque),
            extensao=".png")
        barbearias.append((dono, barbearia))

    def oferecer_e_reservar(dia, quem_atende):
        """Publica horários no `dia` e reserva um bloco por barbeiro."""
        ofertas = []
        for dono, barbearia in barbearias:
            for cadeira in barbearia.cadeiras[:2]:
                horario = c.publicar_horario_ocioso.executar(
                    dono_id=dono.id, barbearia_id=barbearia.id,
                    cadeira_id=cadeira.id, inicio=dia_as(dia, 9, agora),
                    fim=dia_as(dia, 19, agora),
                    preco_por_hora_centavos=sorteio.choice(
                        (2500, 3000, 3500, 4000)))
                ofertas.append((barbearia, horario))
        blocos = []
        for posicao, barbeiro in enumerate(quem_atende):
            barbearia, horario = ofertas[(posicao * 3) % len(ofertas)]
            inicio = dia_as(dia, 10 + (posicao % 3) * 2, agora)
            c.reservar_bloco_de_horario.executar(
                barbeiro_id=barbeiro.id, barbearia_id=barbearia.id,
                horario_ocioso_id=horario.id, inicio=inicio,
                fim=inicio + timedelta(hours=4))
            blocos.append((barbeiro, inicio))
        return blocos

    def agendar_varios(blocos, quantidade):
        feitos = []
        for barbeiro, inicio in blocos:
            servicos = c.consultar_servicos_do_barbeiro.executar(barbeiro.id)
            cursor = inicio
            for _ in range(quantidade):
                servico = sorteio.choice(servicos)
                try:
                    feitos.append(c.agendar_atendimento.executar(
                        cliente_id=sorteio.choice(clientes).id,
                        servico_id=servico.id, inicio=cursor))
                except ErroDeDominio:
                    pass
                cursor += timedelta(minutes=servico.duracao_minutos + 10)
        return feitos

    # Passado: há 7 e 3 dias, para existirem atendimentos já avaliáveis.
    atendem = barbeiros[:-1]
    passados = []
    for dias_atras in (7, 3):
        if viagem:
            viagem(dia_as(-dias_atras - 1, 8, agora))
        blocos = oferecer_e_reservar(-dias_atras, atendem)
        passados += agendar_varios(blocos, 5)
    if viagem:
        viagem(agora)
    for agendamento in passados:
        if sorteio.random() < 0.8:
            c.avaliar_agendamento.executar(
                cliente_id=agendamento.cliente_id,
                agendamento_id=agendamento.id,
                nota=sorteio.choices((3, 4, 5), weights=(1, 3, 5))[0]
                if sorteio.random() < 0.9 else sorteio.choice((1, 2)))

    # Futuro: amanhã e depois de amanhã, com alguns cancelamentos.
    futuros = []
    for dias_a_frente in (1, 2):
        blocos = oferecer_e_reservar(dias_a_frente, barbeiros)
        futuros += agendar_varios(blocos, 4)
    for agendamento in futuros[::9]:
        c.cancelar_agendamento.executar(
            barbeiro_id=agendamento.barbeiro_id,
            agendamento_id=agendamento.id)

    print("Pronto. Contas de demonstração (senha: {}):".format(SENHA_DEMO))
    print("  donos:     ", ", ".join(e for _, e in DONOS))
    print("  barbeiros: ", ", ".join(b[1] for b in BARBEIROS))
    print("  clientes:  ", ", ".join(e for _, e in CLIENTES))
    print("  {} barbearias, {} agendamentos".format(
        len(barbearias), len(passados) + len(futuros)))
    return True


class RelogioDeSemeadura(Relogio):
    """Relógio ajustável: permite criar atendimentos já no passado."""

    def __init__(self):
        self._agora = datetime.now().replace(second=0, microsecond=0)

    def agora(self):
        return self._agora

    def ajustar(self, agora):
        self._agora = agora


def main():
    popular(create_app(relogio=RelogioDeSemeadura()))


if __name__ == "__main__":
    main()

from domain.servico import Servico


def test_servico_salvo_e_recuperado(repos):
    servicos = repos["servicos"]
    s = Servico(barbeiro_id="b1", nome="Corte", preco_centavos=4500,
                duracao_minutos=40)
    servicos.salvar(s)
    assert servicos.por_id(s.id) == s


def test_servicos_do_barbeiro_em_ordem_alfabetica(repos):
    servicos = repos["servicos"]
    for nome in ("Corte", "Barba"):
        servicos.salvar(Servico(barbeiro_id="b1", nome=nome,
                                preco_centavos=3000, duracao_minutos=30))
    servicos.salvar(Servico(barbeiro_id="b2", nome="Pigmentação",
                            preco_centavos=3000, duracao_minutos=30))
    assert [s.nome for s in servicos.do_barbeiro("b1")] == ["Barba", "Corte"]
    assert servicos.por_id("nao-existe") is None

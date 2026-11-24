"""US3: barbeiro cadastra serviços com preço e duração."""
import pytest

from domain.erros import AcessoNegado
from use_cases.cadastrar_servico import CadastrarServico


def cadastrar_servico(ctx, barbeiro, nome="Corte", preco=4500, duracao=40):
    return CadastrarServico(ctx.usuarios, ctx.servicos).executar(
        barbeiro_id=barbeiro.id, nome=nome, preco_centavos=preco,
        duracao_minutos=duracao)


def test_barbeiro_cadastra_servicos_e_os_ve_na_lista(ctx):
    rafa = ctx.cadastrar("barbeiro")
    cadastrar_servico(ctx, rafa, "Corte", 4500, 40)
    cadastrar_servico(ctx, rafa, "Barba", 3000, 30)
    assert [(s.nome, s.preco_centavos) for s in
            ctx.servicos.do_barbeiro(rafa.id)] == [("Barba", 3000),
                                                   ("Corte", 4500)]


def test_cliente_nao_cadastra_servico(ctx):
    with pytest.raises(AcessoNegado):
        cadastrar_servico(ctx, ctx.cadastrar("cliente"))

import pytest

from domain.erros import AcessoNegado
from use_cases.editar_perfil_do_barbeiro import EditarPerfilDoBarbeiro


def test_barbeiro_atualiza_nome_e_apresentacao(ctx):
    barbeiro = ctx.cadastrar("barbeiro", nome="Rafa")

    EditarPerfilDoBarbeiro(ctx.usuarios).executar(
        barbeiro_id=barbeiro.id,
        nome="Rafael Souza",
        apresentacao="Especialista em cortes clássicos.")

    atualizado = ctx.usuarios.por_id(barbeiro.id)
    assert atualizado.nome == "Rafael Souza"
    assert atualizado.apresentacao == "Especialista em cortes clássicos."


def test_cliente_nao_pode_editar_perfil_de_barbeiro(ctx):
    cliente = ctx.cadastrar("cliente")

    with pytest.raises(AcessoNegado):
        EditarPerfilDoBarbeiro(ctx.usuarios).executar(
            barbeiro_id=cliente.id,
            nome="Nome indevido",
            apresentacao="Apresentação indevida")

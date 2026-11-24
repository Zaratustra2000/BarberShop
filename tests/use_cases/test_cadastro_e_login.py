"""US1: cadastro e login."""
import pytest

from domain.erros import CredenciaisInvalidas, DadosInvalidos
from domain.usuario import Papel
from use_cases.autenticar_usuario import AutenticarUsuario
from use_cases.cadastrar_usuario import CadastrarUsuario


def test_cadastro_cria_usuario_com_a_persona_escolhida(ctx):
    usuario = ctx.cadastrar("dono", nome="Carlos Menezes")
    assert usuario.papel == Papel.DONO
    assert ctx.usuarios.por_id(usuario.id).nome == "Carlos Menezes"


def test_senha_nao_e_guardada_em_texto_puro(ctx):
    usuario = ctx.cadastrar("cliente")
    assert "segredo1" not in usuario.senha_hash


def test_email_ja_cadastrado_e_recusado(ctx):
    ctx.cadastrar("cliente", email="lucas@exemplo.com")
    with pytest.raises(DadosInvalidos):
        ctx.cadastrar("barbeiro", email="LUCAS@exemplo.com")


def test_senha_curta_e_recusada(ctx):
    with pytest.raises(DadosInvalidos):
        CadastrarUsuario(ctx.usuarios, ctx.hash).executar(
            nome="Lucas", email="l@exemplo.com", senha="123",
            papel="cliente")


def test_persona_desconhecida_e_recusada(ctx):
    with pytest.raises(DadosInvalidos):
        ctx.cadastrar("gerente")


def test_login_com_credenciais_corretas_devolve_o_usuario(ctx):
    cadastrado = ctx.cadastrar("barbeiro", email="rafa@exemplo.com")
    logado = AutenticarUsuario(ctx.usuarios, ctx.hash).executar(
        email="rafa@exemplo.com", senha="segredo1")
    assert logado.id == cadastrado.id


@pytest.mark.parametrize("email,senha", [
    ("rafa@exemplo.com", "errada99"),
    ("ninguem@exemplo.com", "segredo1"),
])
def test_login_invalido_falha_sem_dizer_o_motivo(ctx, email, senha):
    ctx.cadastrar("barbeiro", email="rafa@exemplo.com")
    with pytest.raises(CredenciaisInvalidas):
        AutenticarUsuario(ctx.usuarios, ctx.hash).executar(
            email=email, senha=senha)

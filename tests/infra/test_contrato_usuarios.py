from domain.usuario import Papel, Usuario


def test_usuario_salvo_e_recuperado_por_id_e_email(repos):
    usuarios = repos["usuarios"]
    u = Usuario(nome="Carlos", email="carlos@exemplo.com", senha_hash="h",
                papel=Papel.DONO)
    usuarios.salvar(u)
    assert usuarios.por_id(u.id) == u
    assert usuarios.por_email("carlos@exemplo.com") == u


def test_usuario_inexistente_devolve_none(repos):
    assert repos["usuarios"].por_id("nao-existe") is None
    assert repos["usuarios"].por_email("x@exemplo.com") is None


def test_perfil_do_barbeiro_e_persistido(repos):
    usuarios = repos["usuarios"]
    u = Usuario(nome="Rafa Souza", email="rafa@exemplo.com",
                senha_hash="h", papel=Papel.BARBEIRO,
                apresentacao="Cortes clássicos",
                foto_perfil="barbeiro-1.webp")
    usuarios.salvar(u)

    salvo = usuarios.por_id(u.id)
    assert salvo.apresentacao == "Cortes clássicos"
    assert salvo.foto_perfil == "barbeiro-1.webp"

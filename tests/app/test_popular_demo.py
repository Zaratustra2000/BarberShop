import os

from scripts.popular_demo import BARBEARIAS, popular


def test_popular_demo_cria_dados_variados_com_poucas_fotos(client):
    app = client.application

    popular(app)

    container = app.extensions["barbershop"]
    dono = container.usuarios.por_email("carlos@exemplo.com")
    barbearias = container.consultar_barbearias_do_dono.executar(dono.id)
    diretorio = app.config["BARBERSHOP_FOTOS_DIR"]
    assert len(barbearias) >= 2
    for barbearia in barbearias:
        assert barbearia.foto_principal
        caminho = os.path.join(diretorio, barbearia.foto_principal)
        assert os.path.isfile(caminho)
    assert len(os.listdir(diretorio)) == len(BARBEARIAS)

    barbeiros = container.buscar_barbeiros.executar("")
    resumos = [container.consultar_perfil_do_barbeiro.executar(b.id).avaliacoes
               for b in barbeiros]
    assert len(barbeiros) >= 5
    assert any(r.quantidade for r in resumos)
    assert any(not r.quantidade for r in resumos)


def test_popular_demo_nao_duplica_dados(client):
    popular(client.application)

    assert popular(client.application) is False

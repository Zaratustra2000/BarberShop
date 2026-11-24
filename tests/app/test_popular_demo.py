import os

from scripts.popular_demo import popular


def test_popular_demo_adiciona_fotos_sinteticas(client):
    app = client.application

    popular(app)

    container = app.extensions["barbershop"]
    dono = container.usuarios.por_email("carlos@exemplo.com")
    barbearias = container.consultar_barbearias_do_dono.executar(dono.id)

    assert len(barbearias) == 2
    for barbearia in barbearias:
        assert barbearia.foto_principal
        diretorio = app.config["BARBERSHOP_FOTOS_DIR"]
        caminho = os.path.join(diretorio, barbearia.foto_principal)
        assert os.path.isfile(caminho)

import json
from pathlib import Path
from scripts import preparar_basemap_rio

from scripts.preparar_basemap_rio import coordenada_tile


RAIZ_APLICACAO = Path(__file__).resolve().parents[2] / "app"
RAIZ_PACOTE = RAIZ_APLICACAO / "static" / "basemap" / "rio-de-janeiro"


def test_pacote_municipal_tem_metadados_e_tiles_leaflet():
    metadados = json.loads(
        (RAIZ_PACOTE / "metadata.json").read_text(encoding="utf-8")
    )

    assert metadados["fonte"] == "OpenStreetMap"
    assert metadados["licenca"] == "ODbL"
    assert metadados["zoom_minimo"] == 10
    assert metadados["zoom_maximo"] == 16
    assert metadados["url"] == "/static/basemap/rio-de-janeiro/{z}/{x}/{y}.png"

    assert "http://" not in metadados["url"]
    assert "https://" not in metadados["url"]

    for zoom in range(metadados["zoom_minimo"], metadados["zoom_maximo"] + 1):
        x_minimo, y_minimo = coordenada_tile(-43.795, -22.746, zoom)
        x_maximo, y_maximo = coordenada_tile(-43.099, -23.082, zoom)
        for x in range(x_minimo, x_maximo + 1):
            for y in range(y_minimo, y_maximo + 1):
                tile = RAIZ_PACOTE / str(zoom) / str(x) / f"{y}.png"
                assert tile.is_file()
                assert tile.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")


def test_pacote_municipal_declara_atribuicao_odbl():
    atribuicao = (RAIZ_PACOTE / "ATRIBUICAO.txt").read_text(encoding="utf-8")

    assert "OpenStreetMap" in atribuicao
    assert "https://www.openstreetmap.org/copyright" in atribuicao
    assert "ODbL" in atribuicao
    assert "https://opendatacommons.org/licenses/odbl/" in atribuicao


def test_limites_municipais_produzem_coordenadas_leaflet():
    x_minimo, y_minimo = coordenada_tile(-43.795, -22.746, 10)
    x_maximo, y_maximo = coordenada_tile(-43.099, -23.082, 10)

    assert (x_minimo, y_minimo, x_maximo, y_maximo) == (387, 578, 389, 579)


def test_documentacao_registra_manutencao_e_verificacao_do_basemap():
    raiz_projeto = RAIZ_APLICACAO.parent
    leia_me = (raiz_projeto / "README.md").read_text(encoding="utf-8")
    documentacao = (
        raiz_projeto / "docs" / "mapa-municipal-offline.md"
    ).read_text(encoding="utf-8")

    assert "Mapa municipal offline" in leia_me
    assert "scripts/preparar_basemap_rio.py" in documentacao
    assert "data_extrato" in documentacao
    assert "data_preparacao" in documentacao
    assert "app/static/basemap/rio-de-janeiro/" in documentacao
    assert "Verificação manual" in documentacao
    assert "pan" in documentacao.lower()
    assert "zoom" in documentacao.lower()


def test_metadados_de_extrato_local_registram_fonte_e_data(
    monkeypatch,
    tmp_path,
):
    monkeypatch.setattr(preparar_basemap_rio, "DESTINO", tmp_path)

    preparar_basemap_rio.gravar_metadados(
        "2026-11-20",
        "Extrato municipal sintético",
        "https://exemplo.test/rio.osm.pbf",
    )
    metadados = json.loads(
        (tmp_path / "metadata.json").read_text(encoding="utf-8")
    )

    assert metadados["extrato"] == "Extrato municipal sintético"
    assert metadados["extrato_url"] == "https://exemplo.test/rio.osm.pbf"
    assert metadados["data_extrato"] == "2026-11-20"

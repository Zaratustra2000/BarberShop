"""Gera tiles locais do Rio com um extrato OSM e renderizador Mapnik."""

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from email.utils import parsedate_to_datetime
import json
import math
from pathlib import Path
import subprocess
import tempfile
import time
import urllib.request
import uuid


OESTE = -43.795
SUL = -23.082
LESTE = -43.099
NORTE = -22.746
ZOOM_MINIMO = 10
ZOOM_MAXIMO = 16
URL_EXTRATO = (
    "https://download.geofabrik.de/south-america/brazil/sudeste/"
    "sudeste-latest.osm.pbf"
)
IMAGEM_RENDERIZADOR = "overv/openstreetmap-tile-server:2.3.0"
DESTINO = (
    Path(__file__).resolve().parents[1]
    / "app"
    / "static"
    / "basemap"
    / "rio-de-janeiro"
)
ASSINATURA_PNG = b"\x89PNG\r\n\x1a\n"


def coordenada_tile(longitude, latitude, zoom):
    n = 2 ** zoom
    x = int((longitude + 180.0) / 360.0 * n)
    y = int(
        (1.0 - math.asinh(math.tan(math.radians(latitude))) / math.pi)
        / 2.0
        * n
    )
    return x, y


def tiles_municipais():
    for zoom in range(ZOOM_MINIMO, ZOOM_MAXIMO + 1):
        x_minimo, y_minimo = coordenada_tile(OESTE, NORTE, zoom)
        x_maximo, y_maximo = coordenada_tile(LESTE, SUL, zoom)
        for x in range(x_minimo, x_maximo + 1):
            for y in range(y_minimo, y_maximo + 1):
                yield zoom, x, y


def baixar_extrato(destino):
    requisicao = urllib.request.Request(
        URL_EXTRATO,
        headers={"User-Agent": "BarberShop-basemap-generator/1.0"},
    )
    print("Baixando o extrato OSM do Sudeste do Brasil...")
    with urllib.request.urlopen(requisicao, timeout=120) as resposta:
        ultima_modificacao = resposta.headers.get("Last-Modified")
        with destino.open("wb") as arquivo:
            while bloco := resposta.read(1024 * 1024):
                arquivo.write(bloco)

    if ultima_modificacao:
        return parsedate_to_datetime(ultima_modificacao).date().isoformat()
    return None


def executar(*argumentos, captura=False):
    return subprocess.run(
        ["docker", *argumentos],
        check=True,
        capture_output=captura,
        text=True,
    )


def obter_porta(container):
    saida = executar(
        "port", container, "80/tcp", captura=True
    ).stdout.strip()
    return int(saida.rsplit(":", 1)[1])


def aguardar_renderizador(porta):
    url = f"http://127.0.0.1:{porta}/"
    for tentativa in range(60):
        try:
            with urllib.request.urlopen(url, timeout=2):
                return
        except OSError as erro:
            if tentativa == 59:
                raise TimeoutError(
                    "O renderizador local nao ficou pronto."
                ) from erro
            time.sleep(1)


def baixar_tile_local(porta, zoom, x, y):
    destino = DESTINO / str(zoom) / str(x) / f"{y}.png"
    destino.parent.mkdir(parents=True, exist_ok=True)
    url = f"http://127.0.0.1:{porta}/tile/{zoom}/{x}/{y}.png"

    for tentativa in range(3):
        try:
            with urllib.request.urlopen(url, timeout=120) as resposta:
                conteudo = resposta.read()
            break
        except OSError:
            if tentativa == 2:
                raise
            time.sleep(2)

    if not conteudo.startswith(ASSINATURA_PNG):
        raise ValueError(
            f"O renderizador retornou um tile PNG invalido: {url}"
        )

    temporario = destino.with_suffix(".png.tmp")
    temporario.write_bytes(conteudo)
    temporario.replace(destino)


def gravar_metadados(
    data_extrato,
    extrato="Sudeste do Brasil (Geofabrik)",
    extrato_url=URL_EXTRATO,
):
    metadados = {
        "municipio": "Rio de Janeiro",
        "fonte": "OpenStreetMap",
        "extrato": extrato,
        "extrato_url": extrato_url,
        "data_extrato": data_extrato,
        "licenca": "ODbL",
        "licenca_url": "https://opendatacommons.org/licenses/odbl/",
        "fonte_url": "https://www.openstreetmap.org/copyright",
        "data_preparacao": date.today().isoformat(),
        "renderizador": IMAGEM_RENDERIZADOR,
        "zoom_minimo": ZOOM_MINIMO,
        "zoom_maximo": ZOOM_MAXIMO,
        "limites": {
            "oeste": OESTE,
            "sul": SUL,
            "leste": LESTE,
            "norte": NORTE,
        },
        "url": "/static/basemap/rio-de-janeiro/{z}/{x}/{y}.png",
    }
    (DESTINO / "metadata.json").write_text(
        json.dumps(metadados, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def preparar(
    caminho_extrato=None,
    fonte_extrato="Extrato OSM local fornecido",
    url_extrato=None,
    data_extrato=None,
):
    if caminho_extrato:
        extrato = Path(caminho_extrato).resolve()
        if not extrato.is_file():
            raise FileNotFoundError(f"Extrato OSM nao encontrado: {extrato}")
        if not data_extrato:
            raise ValueError(
                "Informe --data-extrato para extratos locais."
            )
        preparar_com_extrato(
            extrato,
            data_extrato,
            fonte_extrato,
            url_extrato,
        )
        return

    with tempfile.TemporaryDirectory(
        prefix="barbershop-basemap-"
    ) as temporario:
        extrato = Path(temporario) / "sudeste.osm.pbf"
        data_extrato = baixar_extrato(extrato)
        preparar_com_extrato(extrato, data_extrato)


def preparar_com_extrato(
    extrato,
    data_extrato,
    fonte_extrato="Sudeste do Brasil (Geofabrik)",
    url_extrato=URL_EXTRATO,
):
    identificador = uuid.uuid4().hex
    volume = f"barbershop-rio-basemap-{identificador}"
    container = f"barbershop-rio-basemap-{identificador}"
    executar("pull", IMAGEM_RENDERIZADOR)

    with tempfile.TemporaryDirectory(
        prefix="barbershop-rio-extract-"
    ) as temporario:
        recorte = Path(temporario) / "rio-de-janeiro.osm.pbf"
        executar(
            "run",
            "--rm",
            "--entrypoint",
            "osmium",
            "--volume",
            f"{extrato}:/data/sudeste.osm.pbf:ro",
            "--volume",
            f"{temporario}:/data/saida",
            IMAGEM_RENDERIZADOR,
            "extract",
            "--bbox",
            f"{OESTE},{SUL},{LESTE},{NORTE}",
            "--strategy",
            "simple",
            "--set-bounds",
            "--output",
            "/data/saida/rio-de-janeiro.osm.pbf",
            "/data/sudeste.osm.pbf",
        )
        executar("volume", "create", volume)
        container_iniciado = False

        try:
            executar(
                "run",
                "--rm",
                "--volume",
                f"{recorte}:/data/region.osm.pbf:ro",
                "--volume",
                f"{volume}:/data/database/",
                IMAGEM_RENDERIZADOR,
                "import",
            )
            executar(
                "run",
                "--detach",
                "--name",
                container,
                "--publish",
                "127.0.0.1::80",
                "--volume",
                f"{volume}:/data/database/",
                IMAGEM_RENDERIZADOR,
                "run",
            )
            container_iniciado = True
            porta = obter_porta(container)
            aguardar_renderizador(porta)
            tiles = list(tiles_municipais())
            print(f"Renderizando {len(tiles)} tiles locais...")
            with ThreadPoolExecutor(max_workers=4) as executor:
                for indice, _ in enumerate(
                    executor.map(
                        lambda tile: baixar_tile_local(porta, *tile),
                        tiles,
                    ),
                    start=1,
                ):
                    if indice % 100 == 0:
                        print(f"{indice}/{len(tiles)} tiles")
            gravar_metadados(data_extrato, fonte_extrato, url_extrato)
        finally:
            if container_iniciado:
                executar("rm", "--force", container)
            executar("volume", "rm", volume)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--extrato",
        help=(
            "caminho de um arquivo .osm.pbf local; se omitido, "
            "baixa o extrato regional do Geofabrik"
        ),
    )
    parser.add_argument(
        "--fonte-extrato",
        default="Extrato OSM local fornecido",
        help="descricao da origem do extrato local",
    )
    parser.add_argument(
        "--url-extrato",
        help="URL publica do extrato local, se houver",
    )
    parser.add_argument(
        "--data-extrato",
        help="data ISO 8601 da origem do extrato local",
    )
    argumentos = parser.parse_args()
    preparar(
        argumentos.extrato,
        argumentos.fonte_extrato,
        argumentos.url_extrato,
        argumentos.data_extrato,
    )

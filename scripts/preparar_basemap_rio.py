"""Prepara manualmente os tiles municipais do Rio de Janeiro."""

import math
import time
import urllib.request
from pathlib import Path


OESTE = -43.795
SUL = -23.082
LESTE = -43.099
NORTE = -22.746
DESTINO = (
    Path(__file__).resolve().parents[1]
    / "app"
    / "static"
    / "basemap"
    / "rio-de-janeiro"
)


def coordenada_tile(longitude, latitude, zoom):
    n = 2 ** zoom
    x = int((longitude + 180.0) / 360.0 * n)
    y = int(
        (1.0 - math.asinh(math.tan(math.radians(latitude))) / math.pi)
        / 2.0
        * n
    )
    return x, y


def baixar_tile(zoom, x, y):
    destino = DESTINO / str(zoom) / str(x) / f"{y}.png"
    if destino.is_file():
        return

    destino.parent.mkdir(parents=True, exist_ok=True)
    url = f"https://tile.openstreetmap.org/{zoom}/{x}/{y}.png"
    requisicao = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "BarberShop-offline-map-preparation/"
                "1.0 (municipal snapshot; no automated runtime use)"
            )
        },
    )
    with urllib.request.urlopen(requisicao, timeout=30) as resposta:
        destino.write_bytes(resposta.read())
    time.sleep(1.0)


def preparar():
    for zoom in range(10, 17):
        x_min, y_min = coordenada_tile(OESTE, NORTE, zoom)
        x_max, y_max = coordenada_tile(LESTE, SUL, zoom)
        for x in range(min(x_min, x_max), max(x_min, x_max) + 1):
            for y in range(min(y_min, y_max), max(y_min, y_max) + 1):
                baixar_tile(zoom, x, y)


if __name__ == "__main__":
    preparar()

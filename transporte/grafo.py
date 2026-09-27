"""
grafo.py
========
Traduce los hechos derivados por el motor de inferencia (`conecta`,
`transbordo_en`) en un `Grafo` de estados (estacion, linea), donde:

  - viajar entre dos estados de la MISMA línea cuesta el tiempo de viaje.
  - cambiar de línea en una misma estación (transbordo) cuesta una
    penalización adicional fija (tiempo de caminata/espera).
"""

from __future__ import annotations
from typing import Set

from .modelos import Hecho, Grafo


def construir_grafo(hechos: Set[Hecho], penalizacion_transbordo: float = 4.0) -> Grafo:
    g = Grafo()

    for h in hechos:
        if h[0] == "conecta":
            _, linea, origen, destino, t = h
            g.agregar_arco(
                (origen, linea), (destino, linea), t, "viaje",
                f"{origen} -> {destino} por {linea} ({t} min)"
            )

    for h in hechos:
        if h[0] == "transbordo_en":
            _, estacion, linea_a, linea_b = h
            g.agregar_arco(
                (estacion, linea_a), (estacion, linea_b),
                penalizacion_transbordo, "transbordo",
                f"Transbordo en {estacion}: {linea_a} -> {linea_b} "
                f"({penalizacion_transbordo} min)"
            )

    return g

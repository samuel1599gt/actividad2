"""
base_conocimiento.py
=====================
Declaración de los hechos primitivos del dominio de transporte:

    ("linea_tramo", linea, estacion_origen, estacion_destino, tiempo_min)

Estos hechos equivalen a la malla oficial de cada línea, tal como la
publicaría el operador del sistema de transporte.
"""

from __future__ import annotations
from typing import List, Set, Tuple

from .modelos import Hecho


class BaseConocimientoTransporte:
    def __init__(self):
        self.hechos_base: Set[Hecho] = set()

    def agregar_linea(self, nombre_linea: str, secuencia: List[Tuple[str, int]]):
        """
        secuencia: lista de (estacion, tiempo_hasta_la_siguiente_en_min).
        El último elemento debe tener tiempo 0 (no hay "siguiente").

        Ejemplo:
            [("A", 3), ("B", 2), ("C", 0)]
        genera tramos A->B (3 min) y B->C (2 min) en la línea dada.
        """
        for i in range(len(secuencia) - 1):
            estacion_actual, tiempo = secuencia[i]
            estacion_siguiente, _ = secuencia[i + 1]
            self.hechos_base.add(
                ("linea_tramo", nombre_linea, estacion_actual, estacion_siguiente, tiempo)
            )

    def obtener_hechos(self) -> Set[Hecho]:
        return set(self.hechos_base)

"""
modelos.py
==========
Estructuras de datos compartidas por todo el sistema:
  - Hecho:   representación de un hecho lógico (tupla).
  - Estado:  nodo del grafo de búsqueda -> (estacion, linea).
  - Regla:   una regla de producción SI-ENTONCES para el motor de inferencia.
  - Grafo:   grafo dirigido con costos, construido a partir de los hechos.
  - ResultadoRuta: resultado final entregado al usuario.

Este módulo no depende de ningún otro módulo del paquete: es la base
sobre la que se construyen `base_conocimiento`, `reglas`, `grafo` y
`buscador_ruta`.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Set, Tuple

Hecho = Tuple          # p. ej. ("linea_tramo", "L1", "A", "B", 4)
Estado = Tuple[str, str]  # (estacion, linea)


@dataclass
class Regla:
    """
    Una regla lógica de producción: SI <condicion(hechos)> ENTONCES <accion(hechos)>.

    - nombre: identificador legible de la regla (trazabilidad/explicación).
    - condicion: función que decide si la regla puede dispararse en este ciclo.
    - accion: función que devuelve el conjunto de HECHOS NUEVOS derivados.
    """
    nombre: str
    condicion: Callable[[Set[Hecho]], bool]
    accion: Callable[[Set[Hecho]], Set[Hecho]]


@dataclass
class Grafo:
    """Grafo dirigido y ponderado sobre estados (estacion, linea)."""
    adyacencia: Dict[Estado, List[Tuple[Estado, float, str, str]]] = field(default_factory=dict)

    def agregar_arco(self, u: Estado, v: Estado, costo: float, tipo: str, detalle: str):
        self.adyacencia.setdefault(u, []).append((v, costo, tipo, detalle))


@dataclass
class ResultadoRuta:
    tiempo_total: float
    pasos: List[str]
    transbordos: int

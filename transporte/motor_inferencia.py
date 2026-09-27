"""
motor_inferencia.py
====================
Motor de encadenamiento hacia adelante (forward chaining), independiente
del dominio: no sabe nada de estaciones, líneas ni transbordos. Solo sabe
aplicar `Regla`s sobre un conjunto de hechos hasta alcanzar un punto fijo
(cuando ninguna regla produce hechos nuevos).

Reutilizable en cualquier otro dominio que se modele con Hecho/Regla.
"""

from __future__ import annotations
from typing import List, Set

from .modelos import Hecho, Regla


class MotorInferencia:
    def __init__(self, reglas: List[Regla]):
        self.reglas = reglas
        self.traza: List[str] = []

    def ejecutar(self, hechos_iniciales: Set[Hecho]) -> Set[Hecho]:
        hechos = set(hechos_iniciales)
        cambio = True
        while cambio:
            cambio = False
            for regla in self.reglas:
                if regla.condicion(hechos):
                    nuevos = regla.accion(hechos)
                    nuevos_reales = nuevos - hechos
                    if nuevos_reales:
                        hechos |= nuevos_reales
                        self.traza.append(
                            f"[{regla.nombre}] derivó {len(nuevos_reales)} hecho(s) nuevo(s)"
                        )
                        cambio = True
        return hechos

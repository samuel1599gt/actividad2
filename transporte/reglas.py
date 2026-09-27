"""
reglas.py
=========
Reglas lógicas propias del dominio de transporte. Cada regla es una
instancia de `Regla` (condición + acción) que el `MotorInferencia`
aplicará repetidamente.

Para EXTENDER el sistema (por ejemplo con reglas de hora pico, líneas en
mantenimiento, accesibilidad, etc.) solo hay que añadir una nueva función
aquí y agregar la `Regla` resultante a la lista que devuelve
`construir_reglas()`. Ningún otro módulo necesita cambiar.
"""

from __future__ import annotations
from typing import Dict, List, Set

from .modelos import Hecho, Regla


def _cond_bidireccional(hechos: Set[Hecho]) -> bool:
    return any(h[0] == "linea_tramo" for h in hechos)


def _accion_bidireccional(hechos: Set[Hecho]) -> Set[Hecho]:
    # SI linea_tramo(L, X, Y, t)  ENTONCES conecta(L, X, Y, t) y conecta(L, Y, X, t)
    nuevos = set()
    for h in hechos:
        if h[0] == "linea_tramo":
            _, linea, origen, destino, t = h
            nuevos.add(("conecta", linea, origen, destino, t))
            nuevos.add(("conecta", linea, destino, origen, t))
    return nuevos


def _cond_transbordo(hechos: Set[Hecho]) -> bool:
    return any(h[0] == "conecta" for h in hechos)


def _accion_transbordo(hechos: Set[Hecho]) -> Set[Hecho]:
    # SI conecta(L1, X, _, _) y conecta(L2, X, _, _) y L1 != L2
    # ENTONCES transbordo_en(X, L1, L2)
    estacion_lineas: Dict[str, Set[str]] = {}
    for h in hechos:
        if h[0] == "conecta":
            _, linea, origen, _, _ = h
            estacion_lineas.setdefault(origen, set()).add(linea)

    nuevos = set()
    for estacion, lineas in estacion_lineas.items():
        if len(lineas) >= 2:
            lineas_ordenadas = sorted(lineas)
            for i in range(len(lineas_ordenadas)):
                for j in range(len(lineas_ordenadas)):
                    if i != j:
                        nuevos.add((
                            "transbordo_en", estacion,
                            lineas_ordenadas[i], lineas_ordenadas[j]
                        ))
    return nuevos


def construir_reglas() -> List[Regla]:
    """Punto de extensión: agrega aquí nuevas reglas del dominio."""
    return [
        Regla("Conexión bidireccional", _cond_bidireccional, _accion_bidireccional),
        Regla("Detección de transbordos", _cond_transbordo, _accion_transbordo),
    ]

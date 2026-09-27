"""
Paquete `transporte`: sistema inteligente de rutas óptimas en transporte
masivo, basado en una base de conocimiento de reglas lógicas.

Módulos:
    modelos            -> estructuras de datos compartidas (Hecho, Regla, Grafo...)
    motor_inferencia   -> motor de encadenamiento hacia adelante (forward chaining)
    base_conocimiento  -> hechos primitivos del sistema de transporte
    reglas             -> reglas lógicas específicas del dominio
    grafo              -> construcción del grafo de estados a partir de los hechos
    buscador_ruta      -> Dijkstra para hallar la ruta óptima

Uso típico:

    from transporte import (
        BaseConocimientoTransporte, construir_reglas, MotorInferencia,
        construir_grafo, buscar_mejor_ruta,
    )
"""

from .modelos import Hecho, Estado, Regla, Grafo, ResultadoRuta
from .motor_inferencia import MotorInferencia
from .base_conocimiento import BaseConocimientoTransporte
from .reglas import construir_reglas
from .grafo import construir_grafo
from .buscador_ruta import buscar_mejor_ruta

__all__ = [
    "Hecho", "Estado", "Regla", "Grafo", "ResultadoRuta",
    "MotorInferencia", "BaseConocimientoTransporte", "construir_reglas",
    "construir_grafo", "buscar_mejor_ruta",
]

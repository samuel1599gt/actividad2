"""
buscador_ruta.py
=================
Búsqueda de la ruta óptima entre dos estaciones mediante el algoritmo de
Dijkstra, aplicado sobre el grafo de estados (estacion, linea) construido
por `grafo.construir_grafo`.

Como el origen/destino pueden pertenecer a varias líneas, se crea un
estado virtual "INICIO" conectado con costo 0 a todas las líneas que pasan
por la estación de origen, y la búsqueda se detiene apenas se alcanza
CUALQUIER estado cuya estación sea el destino.
"""

from __future__ import annotations
import heapq
from typing import Dict, List, Set, Tuple

from .modelos import Hecho, Estado, Grafo, ResultadoRuta


def buscar_mejor_ruta(grafo: Grafo, hechos: Set[Hecho],
                       estacion_origen: str, estacion_destino: str) -> ResultadoRuta:

    lineas_por_estacion: Dict[str, Set[str]] = {}
    for h in hechos:
        if h[0] == "conecta":
            _, linea, origen, _, _ = h
            lineas_por_estacion.setdefault(origen, set()).add(linea)

    if estacion_origen not in lineas_por_estacion:
        raise ValueError(f"La estación de origen '{estacion_origen}' no existe en la BC.")
    if estacion_destino not in lineas_por_estacion:
        raise ValueError(f"La estación de destino '{estacion_destino}' no existe en la BC.")

    INICIO: Estado = ("__INICIO__", "__INICIO__")
    dist: Dict[Estado, float] = {INICIO: 0.0}
    previo: Dict[Estado, Tuple[Estado, str]] = {}
    heap: List[Tuple[float, Estado]] = [(0.0, INICIO)]

    arcos_inicio = [
        ((estacion_origen, linea), 0.0, "salida", f"Iniciar en {estacion_origen} por {linea}")
        for linea in lineas_por_estacion[estacion_origen]
    ]

    def vecinos(estado: Estado):
        if estado == INICIO:
            return arcos_inicio
        return grafo.adyacencia.get(estado, [])

    visitado: Set[Estado] = set()
    estado_final = None

    while heap:
        d_actual, estado_actual = heapq.heappop(heap)
        if estado_actual in visitado:
            continue
        visitado.add(estado_actual)

        if estado_actual[0] == estacion_destino:
            estado_final = estado_actual
            break

        for vecino, costo, _tipo, detalle in vecinos(estado_actual):
            nueva_dist = d_actual + costo
            if nueva_dist < dist.get(vecino, float("inf")):
                dist[vecino] = nueva_dist
                previo[vecino] = (estado_actual, detalle)
                heapq.heappush(heap, (nueva_dist, vecino))

    if estado_final is None:
        raise ValueError("No existe una ruta posible entre esas dos estaciones.")

    pasos: List[str] = []
    transbordos = 0
    cursor = estado_final
    while cursor in previo:
        anterior, detalle = previo[cursor]
        pasos.append(detalle)
        if "Transbordo" in detalle:
            transbordos += 1
        cursor = anterior
    pasos.reverse()

    return ResultadoRuta(tiempo_total=dist[estado_final], pasos=pasos, transbordos=transbordos)

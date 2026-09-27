"""
main.py
=======
Punto de entrada del sistema. Declara la base de conocimiento del
Sistema Estratégico de Transporte Público (SETP) de Ibagué (modelo
ILUSTRATIVO, construido con corredores y lugares reales de la ciudad:
Quinta, Ferrocarril y Ambalá), ejecuta el motor de inferencia, construye
el grafo y permite al usuario INGRESAR POR TECLADO la estación de
origen y la de destino para calcular dinámicamente la mejor ruta.

NOTA IMPORTANTE:
El SETP de Ibagué está actualmente en construcción y no existe todavía
un mapa público oficial con todos los tiempos exactos entre estaciones.
Los nombres de los corredores (Quinta, Ferrocarril, Ambalá) y de los
lugares (Terminal Norte, Plaza de Bolívar, Universidad de Ibagué,
Aeropuerto Perales, etc.) corresponden a sitios reales de la ciudad,
pero los TIEMPOS de viaje entre paradas son ilustrativos, con fines
educativos/de demostración del sistema experto. Para un uso en
producción, reemplaza estos datos por la malla oficial del operador.

Ejecutar:
    python3 main.py
"""

from transporte import (
    BaseConocimientoTransporte,
    construir_reglas,
    MotorInferencia,
    construir_grafo,
    buscar_mejor_ruta,
)


def construir_base_ibague() -> BaseConocimientoTransporte:
    bc = BaseConocimientoTransporte()

    # Corredor Quinta (eje norte-sur, por la Carrera Quinta)
    bc.agregar_linea("Quinta", [
        ("Terminal Norte", 5), ("Parque Salado", 4), ("Plaza de Bolívar", 4),
        ("Parque Centenario", 3), ("Terminal Sur", 0)
    ])

    # Corredor Ferrocarril (oriente-occidente), cruza Quinta en "Parque Centenario"
    bc.agregar_linea("Ferrocarril", [
        ("Barrio Jordán", 5), ("Estación del Ferrocarril", 4), ("Parque Centenario", 3),
        ("Terminal de Transportes", 4), ("Barrio Belén", 0)
    ])

    # Corredor Ambalá, cruza Quinta en "Plaza de Bolívar"
    bc.agregar_linea("Ambalá", [
        ("Barrio Ambalá", 6), ("Universidad de Ibagué", 5), ("Plaza de Bolívar", 4),
        ("Aeropuerto Perales", 0)
    ])

    return bc


def listar_estaciones(hechos):
    estaciones = sorted({h[2] for h in hechos if h[0] == "conecta"})
    print("\nEstaciones disponibles:")
    for est in estaciones:
        print(" -", est)
    return estaciones


def pedir_estacion(mensaje, estaciones_validas):
    while True:
        valor = input(mensaje).strip()
        coincidencias = [e for e in estaciones_validas if e.lower() == valor.lower()]
        if coincidencias:
            return coincidencias[0]
        print(f"  '{valor}' no es una estación válida. Escríbela tal como aparece en la lista.")


def main():
    bc = construir_base_ibague()

    motor = MotorInferencia(construir_reglas())
    hechos_derivados = motor.ejecutar(bc.obtener_hechos())

    print("=== Traza del motor de inferencia ===")
    for linea in motor.traza:
        print(" -", linea)

    grafo = construir_grafo(hechos_derivados, penalizacion_transbordo=4.0)
    estaciones_validas = listar_estaciones(hechos_derivados)

    print("\n--- Sistema de rutas SETP Ibagué (modelo ilustrativo) ---")
    while True:
        origen = pedir_estacion("\nEstación de ORIGEN: ", estaciones_validas)
        destino = pedir_estacion("Estación de DESTINO: ", estaciones_validas)

        try:
            resultado = buscar_mejor_ruta(grafo, hechos_derivados, origen, destino)
            print(f"\n=== Mejor ruta de '{origen}' a '{destino}' ===")
            for paso in resultado.pasos:
                print(" •", paso)
            print(f"\nTiempo total estimado: {resultado.tiempo_total} min")
            print(f"Número de transbordos: {resultado.transbordos}")
        except ValueError as e:
            print(f"\n⚠ {e}")

        de_nuevo = input("\n¿Buscar otra ruta? (s/n): ").strip().lower()
        if de_nuevo != "s":
            print("¡Hasta luego!")
            break


if __name__ == "__main__":
    main()

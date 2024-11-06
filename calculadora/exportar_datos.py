# calculadora/exportar_datos.py

import csv
import numpy as np
from calculadora.calculadora_balistica import CalculadoraBalistica


def encontrar_angulo_para_alcance(alcance_objetivo, velocidad_inicial, altura_inicial, densidad_aire, latitud=32.0,
                                  tolerancia=1.0):
    """
    Encuentra el ángulo necesario para alcanzar una distancia específica
    usando búsqueda binaria.
    """
    angulo_min = 0
    angulo_max = 90

    while angulo_max - angulo_min > 0.01:  # Precisión de 0.01 grados
        angulo = (angulo_min + angulo_max) / 2
        calculadora = CalculadoraBalistica('masa_puntual')
        calculadora.establecer_parametros(angulo, velocidad_inicial, altura_inicial, densidad_aire, latitud)
        calculadora.calcular_trayectoria()

        alcance_actual = calculadora.alcance_maximo

        if abs(alcance_actual - alcance_objetivo) < tolerancia:
            return angulo, calculadora
        elif alcance_actual < alcance_objetivo:
            angulo_min = angulo
        else:
            angulo_max = angulo

    return None, None


def calcular_datos_tabla(velocidad_inicial=320, altura_inicial=0, densidad_aire=1.225, latitud=32.0, intervalo=100):
    """
    Calcula la tabla de tiro en intervalos de distancia especificados
    """
    datos = []
    alza_anterior = None

    # Encontrar el alcance máximo primero
    calc_max = CalculadoraBalistica('masa_puntual')
    calc_max.establecer_parametros(45, velocidad_inicial, altura_inicial, densidad_aire, latitud)
    calc_max.calcular_trayectoria()
    alcance_maximo = int(calc_max.alcance_maximo)

    # Calcular para cada intervalo de 100m
    for alcance in range(intervalo, alcance_maximo + intervalo, intervalo):
        angulo, calculadora = encontrar_angulo_para_alcance(
            alcance, velocidad_inicial, altura_inicial, densidad_aire, latitud
        )

        if angulo is not None:
            # Convertir ángulo a mils (1 grado ≈ 17.777778 mils)
            alza = angulo * 17.777778

            # Calcular la diferencia de alza
            if alza_anterior is None:
                var_alza = 53.33  # Primer valor fijo
            else:
                var_alza = alza - alza_anterior

            datos.append({
                "alcance": alcance,
                "angulo": angulo,
                "alza": alza,
                "var_alza": var_alza,
                "tiempo_vuelo": calculadora.tiempo_de_vuelo,
                "flecha": calculadora.altura_maxima
            })

            alza_anterior = alza

    return datos


def exportar_a_csv(datos, nombre_archivo):
    """
    Exporta los datos calculados a un archivo CSV
    """
    with open(nombre_archivo, 'w', newline='', encoding='utf-8') as csvfile:
        escritor = csv.writer(csvfile, delimiter=';')

        # Escribir encabezados
        escritor.writerow([
            'Alcance (m)',
            'Ángulo (grados)',
            'Alza (mil)',
            'Var Alza (mil)',
            'Tiempo vuelo (seg)',
            'Flecha (m)'
        ])

        # Escribir datos
        for dato in datos:
            escritor.writerow([
                f"{dato['alcance']:.2f}",
                f"{dato['angulo']:.2f}",
                f"{dato['alza']:.2f}",
                f"{dato['var_alza']:.2f}",
                f"{dato['tiempo_vuelo']:.2f}",
                f"{dato['flecha']:.2f}"
            ])

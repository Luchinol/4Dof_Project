# calculadora/exportar_datos.py

import csv
import numpy as np
from calculadora.calculadora_balistica import CalculadoraBalistica


def calcular_alcance_para_angulo(angulo, velocidad_inicial, altura_inicial, densidad_aire, latitud=32.0):
    """
    Calcula el alcance para un ángulo específico
    """
    calculadora = CalculadoraBalistica('masa_puntual')
    calculadora.establecer_parametros(angulo, velocidad_inicial, altura_inicial, densidad_aire, latitud)
    calculadora.calcular_trayectoria()
    return calculadora.alcance_maximo, calculadora


def encontrar_angulos_para_alcance(alcance_objetivo, velocidad_inicial, altura_inicial, densidad_aire, latitud=32.0,
                                   tolerancia=1.0):
    """
    Encuentra los dos ángulos posibles (trayectoria alta y baja) para un alcance específico
    """
    angulos = []

    # Búsqueda en el rango de ángulos altos (90° a 45°)
    angulo_min_alto = 45
    angulo_max_alto = 90

    # Búsqueda binaria para el ángulo alto
    while angulo_max_alto - angulo_min_alto > 0.01:
        angulo = (angulo_min_alto + angulo_max_alto) / 2
        alcance_actual, _ = calcular_alcance_para_angulo(angulo, velocidad_inicial,
                                                         altura_inicial, densidad_aire, latitud)

        if abs(alcance_actual - alcance_objetivo) < tolerancia:
            angulos.append(angulo)
            break
        elif alcance_actual < alcance_objetivo:
            angulo_max_alto = angulo
        else:
            angulo_min_alto = angulo

    return angulos[0] if angulos else None


def calcular_datos_tabla(velocidad_inicial=320, altura_inicial=0, densidad_aire=1.225, latitud=32.0, intervalo=100):
    """
    Calcula la tabla de tiro en intervalos de distancia especificados,
    considerando ángulos entre 90° y 45°
    """
    datos = []
    alza_anterior = None

    # Encontrar el alcance máximo para 45° (máximo teórico)
    alcance_45, _ = calcular_alcance_para_angulo(45, velocidad_inicial, altura_inicial,
                                                 densidad_aire, latitud)

    # Encontrar el alcance mínimo (para 90°)
    alcance_90, _ = calcular_alcance_para_angulo(90, velocidad_inicial, altura_inicial,
                                                 densidad_aire, latitud)

    # Ajustar el alcance inicial al primer múltiplo de intervalo después de alcance_90
    alcance_inicial = int(np.ceil(alcance_90 / intervalo)) * intervalo

    # Calcular para cada intervalo desde el alcance mínimo hasta el máximo
    for alcance in range(alcance_inicial, int(alcance_45) + intervalo, intervalo):
        angulo = encontrar_angulos_para_alcance(
            alcance, velocidad_inicial, altura_inicial, densidad_aire, latitud
        )

        if angulo is not None:
            # Calcular la trayectoria completa para obtener todos los datos
            _, calculadora = calcular_alcance_para_angulo(
                angulo, velocidad_inicial, altura_inicial, densidad_aire, latitud
            )

            # Convertir ángulo a mils (1 grado ≈ 17.777778 mils)
            alza = angulo * 17.777778

            # Calcular la diferencia de alza
            if alza_anterior is None:
                var_alza = 7.81  # Primer valor fijo
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
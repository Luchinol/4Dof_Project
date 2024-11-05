# exportar_datos.py

import csv
import numpy as np

def calcular_datos_tabla(modelo):
  # Calcular los datos necesarios
  alcance = "modelo.alcance_maximo"
  alza = "np.degrees(np.arctan(modelo.altura_maxima / alcance)) * 1000"
  var_alza = "alza / (alcance / 100)"
  tiempo_vuelo = "modelo.tiempo_de_vuelo"
  flecha = "modelo.altura_maxima"

  return {
      "alcance": alcance,
      "alza": alza,
      "var_alza": var_alza,
      "tiempo_vuelo": tiempo_vuelo,
      "flecha": flecha
  }

def exportar_a_csv(datos, nombre_archivo):
  with open(nombre_archivo, 'w', newline='', encoding='utf-8') as csvfile:
      escritor = csv.writer(csvfile, delimiter=';')
      escritor.writerow(['Alcance (m)', 'Alza (mil)', 'Var Alza x 100 mts (mil)', 'Tiempo vuelo (seg)', 'Flecha (m)'])
      escritor.writerow([
          f"{datos['alcance']:.2f}",
          f"{datos['alza']:.2f}",
          f"{datos['var_alza']:.2f}",
          f"{datos['tiempo_vuelo']:.2f}",
          f"{datos['flecha']:.2f}"
      ])
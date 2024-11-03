# calculadora/calculadora_balistica.py

from modelos.modelo_masa_puntual import ModeloMasaPuntual
from modelos.modelo_4dof import Modelo4DOF
from modelos.coeficientes import CoeficientesAerodinamicos

class CalculadoraBalistica:
  def __init__(self, modelo_seleccionado):
      self.modelo_seleccionado = modelo_seleccionado  # 'masa_puntual' o '4dof'
      self.configurar_modelo()

  def configurar_modelo(self):
      if self.modelo_seleccionado == 'masa_puntual':
          # Configuración para el modelos de masa puntual
          # Constantes basadas en el paper del mortero
          masa = 14.5  # kg
          diametro = 0.12  # m
          area = 0.0113  # m^2 (calculado o proporcionado)
          cd = 0.295  # Coeficiente de arrastre base para proyectil de mortero
          densidad_aire = 1.225  # kg/m^3 al nivel del mar

          self.modelo = ModeloMasaPuntual(masa, area, cd, densidad_aire)

      elif self.modelo_seleccionado == '4dof':
          # Configuración para el modelos 4DOF
          masa = 14.5  # kg
          diametro = 0.12  # m
          densidad_aire = 1.225  # kg/m^3 al nivel del mar
          coeficientes = CoeficientesAerodinamicos()

          self.modelo = Modelo4DOF(masa, diametro, densidad_aire, coeficientes)

      else:
          raise ValueError("Modelo seleccionado no es válido.")

  def establecer_parametros(self, angulo, velocidad_inicial, altura_inicial, densidad_aire):
      # Actualizar densidad del aire en el modelos
      self.modelo.densidad_aire = densidad_aire

      # Guardar parámetros para su uso posterior
      self.angulo = angulo
      self.velocidad_inicial = velocidad_inicial
      self.altura_inicial = altura_inicial

  def calcular_trayectoria(self):
      if self.modelo_seleccionado == 'masa_puntual':
          self.modelo.calcular_trayectoria(self.angulo, self.velocidad_inicial, self.altura_inicial)
      elif self.modelo_seleccionado == '4dof':
          self.modelo.calcular_trayectoria(self.angulo, self.velocidad_inicial, self.altura_inicial)

      # Obtener resultados
      self.tiempo_de_vuelo = self.modelo.tiempo_de_vuelo
      self.alcance_maximo = self.modelo.alcance_maximo
      self.altura_maxima = self.modelo.altura_maxima
      self.Vx = self.modelo.Vx
      self.Vy = self.modelo.Vy
      self.X = self.modelo.X
      self.Y = self.modelo.Y
      self.tiempos = self.modelo.tiempos

  def graficar_trayectoria(self):
      self.modelo.graficar_trayectoria()

  def exportar_a_csv(self, nombre_archivo):
      # Exportar los resultados a un archivo CSV
      import csv
      with open(nombre_archivo, 'w', newline='') as csvfile:
          campos = ['Tiempo (s)', 'Posición X (m)', 'Posición Y (m)', 'Vx (m/s)', 'Vy (m/s)']
          escritor = csv.DictWriter(csvfile, fieldnames=campos)
          escritor.writeheader()
          for i in range(len(self.tiempos)):
              escritor.writerow({'Tiempo (s)': self.tiempos[i],
                                 'Posición X (m)': self.X[i],
                                 'Posición Y (m)': self.Y[i],
                                 'Vx (m/s)': self.Vx[i],
                                 'Vy (m/s)': self.Vy[i]})
# modelos/modelo_masa_puntual.py

import numpy as np
import matplotlib.pyplot as plt

class ModeloMasaPuntual:
  def __init__(self, masa, area, coeficiente_arrastre, densidad_aire, gravedad=9.81):
      self.masa = masa  # Masa del proyectil (kg)
      self.area = area  # Área de sección transversal (m^2)
      self.cd = coeficiente_arrastre  # Coeficiente de arrastre
      self.densidad_aire = densidad_aire  # Densidad del aire (kg/m^3)
      self.g = gravedad  # Aceleración gravitatoria (m/s^2)

      # Variables para almacenar resultados
      self.Vx = []
      self.Vy = []
      self.X = []
      self.Y = []
      self.tiempos = []

  def calcular_trayectoria(self, angulo_inicial, velocidad_inicial, altura_inicial):
      # Convertir ángulo a radianes
      theta = np.radians(angulo_inicial)

      # Condiciones iniciales
      Vx = velocidad_inicial * np.cos(theta)
      Vy = velocidad_inicial * np.sin(theta)
      x = 0.0
      y = altura_inicial

      # Tiempo
      dt = 0.01
      t = 0.0

      while y >= 0:
          # Velocidad resultante
          V = np.sqrt(Vx ** 2 + Vy ** 2)

          # Fuerza de arrastre
          D = 0.5 * self.cd * self.densidad_aire * V ** 2 * self.area

          # Componentes de las fuerzas
          Fx = -D * (Vx / V)
          Fy = -self.masa * self.g - D * (Vy / V)

          # Actualizar velocidades
          Vx_new = Vx + (Fx / self.masa) * dt
          Vy_new = Vy + (Fy / self.masa) * dt

          # Actualizar posiciones
          x_new = x + Vx * dt
          y_new = y + Vy * dt

          # Almacenar datos
          self.Vx.append(Vx)
          self.Vy.append(Vy)
          self.X.append(x)
          self.Y.append(y)
          self.tiempos.append(t)

          # Preparar para la siguiente iteración
          Vx = Vx_new
          Vy = Vy_new
          x = x_new
          y = y_new
          t += dt

      # Resultados finales
      self.tiempo_de_vuelo = t
      self.alcance_maximo = x
      self.altura_maxima = max(self.Y)

  def graficar_trayectoria(self):
      plt.figure(figsize=(10, 6))
      plt.plot(self.X, self.Y)
      plt.title('Trayectoria del Proyectil (Masa Puntual)')
      plt.xlabel('Distancia Horizontal (m)')
      plt.ylabel('Altura Vertical (m)')
      plt.grid(True)
      plt.show()
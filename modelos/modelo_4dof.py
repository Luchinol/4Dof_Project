# modelos/modelo_4dof.py

import numpy as np
import matplotlib.pyplot as plt
from .coeficientes import CoeficientesAerodinamicos

class Modelo4DOF:
  def __init__(self, masa, diametro, densidad_aire, coeficientes):
      self.g = 9.81  # Aceleración gravitatoria (m/s^2)
      self.masa = masa  # Masa del proyectil (kg)
      self.diametro = diametro  # Diámetro del proyectil (m)
      self.area = np.pi * (self.diametro / 2) ** 2  # Área de sección transversal (m^2)
      self.densidad_aire = densidad_aire  # Densidad del aire (kg/m^3)
      self.coeficientes = coeficientes  # Instancia de CoeficientesAerodinamicos

      # Variables para almacenar resultados
      self.Vx = []
      self.Vy = []
      self.X = []
      self.Y = []
      self.tiempos = []

  def calcular_trayectoria(self, angulo_ataque_deg, velocidad_inicial, altura_inicial):
      angulo_ataque_rad = np.radians(angulo_ataque_deg)

      # Condiciones iniciales
      Vx = velocidad_inicial * np.cos(angulo_ataque_rad)
      Vy = velocidad_inicial * np.sin(angulo_ataque_rad)
      x = 0.0
      y = altura_inicial

      # Tiempo
      dt = 0.01
      t = 0.0

      while y >= 0:
          # Velocidad del aire
          V = np.sqrt(Vx ** 2 + Vy ** 2)

          # Calcular coeficientes aerodinámicos
          Cd = self.coeficientes.calcular_coeficiente_arrastre(V, angulo_ataque_rad)
          Cl = self.coeficientes.calcular_coeficiente_sustentacion(V, angulo_ataque_rad)

          # Fuerzas
          D = 0.5 * Cd * self.densidad_aire * V ** 2 * self.area  # Fuerza de arrastre
          L = 0.5 * Cl * self.densidad_aire * V ** 2 * self.area  # Fuerza de sustentación

          # Componentes de las fuerzas
          Fx = -D * (Vx / V) + L * (Vy / V)
          Fy = -self.masa * self.g - D * (Vy / V) - L * (Vx / V)

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
      plt.title('Trayectoria del Proyectil (4DOF)')
      plt.xlabel('Distancia Horizontal (m)')
      plt.ylabel('Altura Vertical (m)')
      plt.grid(True)
      plt.show()
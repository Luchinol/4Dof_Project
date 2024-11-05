# modelos/modelo_4dof.py

import numpy as np
import matplotlib.pyplot as plt
from .coeficientes import CoeficientesAerodinamicos


class Modelo4DOF:
    def __init__(self, masa, diametro, densidad_aire, coeficientes):
        self.g = 9.81  # Aceleración gravitatoria (m/s^2)
        self.omega_tierra = 7.2921159e-5  # Velocidad angular de la Tierra (rad/s)
        self.masa = masa  # Masa del proyectil (kg)
        self.diametro = diametro  # Diámetro del proyectil (m)
        self.area = np.pi * (self.diametro / 2) ** 2  # Área de sección transversal (m^2)
        self.densidad_aire = densidad_aire  # Densidad del aire (kg/m^3)
        self.coeficientes = coeficientes  # Instancia de CoeficientesAerodinamicos
        self.latitud = 32.0  # Latitud por defecto (grados)

        # Variables para almacenar resultados
        self.Vx = []
        self.Vy = []
        self.Vz = []  # Añadido para efecto Coriolis
        self.X = []
        self.Y = []
        self.Z = []  # Añadido para efecto Coriolis
        self.tiempos = []

    def calcular_aceleracion_coriolis(self, Vx, Vy, Vz):
        """Calcula la aceleración debido al efecto Coriolis"""
        lat_rad = np.radians(self.latitud)

        # Componentes de la aceleración de Coriolis
        ax = 2 * self.omega_tierra * (Vz * np.cos(lat_rad) - Vy * np.sin(lat_rad))
        ay = 2 * self.omega_tierra * Vx * np.sin(lat_rad)
        az = -2 * self.omega_tierra * Vx * np.cos(lat_rad)

        return ax, ay, az

    def calcular_trayectoria(self, angulo_ataque_deg, velocidad_inicial, altura_inicial, latitud=32.0):
        self.latitud = latitud
        angulo_ataque_rad = np.radians(angulo_ataque_deg)

        # Condiciones iniciales
        Vx = velocidad_inicial * np.cos(angulo_ataque_rad)
        Vy = velocidad_inicial * np.sin(angulo_ataque_rad)
        Vz = 0.0  # Velocidad inicial en Z
        x = 0.0
        y = altura_inicial
        z = 0.0

        # Tiempo
        dt = 0.01
        t = 0.0

        while y >= 0:
            # Velocidad del aire
            V = np.sqrt(Vx ** 2 + Vy ** 2 + Vz ** 2)

            # Calcular coeficientes aerodinámicos
            Cd = self.coeficientes.calcular_coeficiente_arrastre(V, angulo_ataque_rad)
            Cl = self.coeficientes.calcular_coeficiente_sustentacion(V, angulo_ataque_rad)

            # Fuerzas aerodinámicas
            D = 0.5 * Cd * self.densidad_aire * V ** 2 * self.area  # Fuerza de arrastre
            L = 0.5 * Cl * self.densidad_aire * V ** 2 * self.area  # Fuerza de sustentación

            # Componentes de las fuerzas aerodinámicas
            Fx = -D * (Vx / V) + L * (Vy / V)
            Fy = -self.masa * self.g - D * (Vy / V) - L * (Vx / V)
            Fz = -D * (Vz / V)

            # Añadir efecto Coriolis
            ax_cor, ay_cor, az_cor = self.calcular_aceleracion_coriolis(Vx, Vy, Vz)

            # Actualizar velocidades incluyendo Coriolis
            Vx_new = Vx + ((Fx / self.masa) + ax_cor) * dt
            Vy_new = Vy + ((Fy / self.masa) + ay_cor) * dt
            Vz_new = Vz + ((Fz / self.masa) + az_cor) * dt

            # Actualizar posiciones
            x_new = x + Vx * dt
            y_new = y + Vy * dt
            z_new = z + Vz * dt

            # Almacenar datos
            self.Vx.append(Vx)
            self.Vy.append(Vy)
            self.Vz.append(Vz)
            self.X.append(x)
            self.Y.append(y)
            self.Z.append(z)
            self.tiempos.append(t)

            # Preparar para la siguiente iteración
            Vx = Vx_new
            Vy = Vy_new
            Vz = Vz_new
            x = x_new
            y = y_new
            z = z_new
            t += dt

        # Resultados finales
        self.tiempo_de_vuelo = t
        self.alcance_maximo = np.sqrt(x ** 2 + z ** 2)  # Alcance considerando desviación lateral
        self.altura_maxima = max(self.Y)

    def graficar_trayectoria(self):
        # Gráfica 2D tradicional
        plt.figure(figsize=(10, 6))
        plt.subplot(121)
        plt.plot(self.X, self.Y)
        plt.title('Vista Lateral (X-Y)')
        plt.xlabel('Distancia Horizontal (m)')
        plt.ylabel('Altura (m)')
        plt.grid(True)

        # Gráfica de desviación lateral
        plt.subplot(122)
        plt.plot(self.X, self.Z)
        plt.title('Vista Superior (X-Z)\nDesviación por Coriolis')
        plt.xlabel('Distancia Horizontal (m)')
        plt.ylabel('Desviación Lateral (m)')
        plt.grid(True)

        plt.tight_layout()
        plt.show()
# modelos/modelo_masa_puntual.py

import numpy as np
import matplotlib.pyplot as plt


class ModeloMasaPuntual:
    def __init__(self, masa, area, coeficiente_arrastre_base, densidad_aire, gravedad=9.81):
        self.masa = masa  # Masa del proyectil (kg)
        self.area = area  # Área de sección transversal (m^2)
        self.cd_base = coeficiente_arrastre_base  # Coeficiente de arrastre base
        self.densidad_aire = densidad_aire  # Densidad del aire (kg/m^3)
        self.g = gravedad  # Aceleración gravitatoria (m/s^2)

        # Variables para almacenar resultados
        self.Vx = []
        self.Vy = []
        self.X = []
        self.Y = []
        self.tiempos = []
        self.cd_history = []  # Para almacenar el histórico de Cd

    def calcular_cd_dinamico(self, Vx, Vy):
        """
        Calcula el coeficiente de arrastre de manera dinámica,
        similar al modelo 4DOF pero simplificado
        """
        V = np.sqrt(Vx ** 2 + Vy ** 2)

        # Calcular ángulo de ataque aproximado
        if V > 0:
            angulo_ataque = abs(np.arctan2(Vy, Vx))
        else:
            angulo_ataque = 0

        # Usar una fórmula similar a la del modelo 4DOF
        Cd0 = 0.095  # Coeficiente de arrastre base (igual al 4DOF)
        Cd = Cd0 + 0.05 * angulo_ataque  # Ajuste según el ángulo de ataque

        # Ajuste por número de Mach (simplificado)
        mach = V / 340.0  # 340 m/s es la velocidad del sonido aproximada
        if mach > 0.8:
            Cd *= (1 + 0.2 * (mach - 0.8))  # Incremento por efectos transónicos

        return Cd

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

        # Limpiar listas de resultados anteriores
        self.Vx = []
        self.Vy = []
        self.X = []
        self.Y = []
        self.tiempos = []
        self.cd_history = []

        while y >= 0:
            # Velocidad resultante
            V = np.sqrt(Vx ** 2 + Vy ** 2)

            # Calcular Cd dinámico
            cd_actual = self.calcular_cd_dinamico(Vx, Vy)
            self.cd_history.append(cd_actual)

            # Fuerza de arrastre
            D = 0.5 * cd_actual * self.densidad_aire * V ** 2 * self.area

            # Componentes de las fuerzas
            Fx = -D * (Vx / V) if V > 0 else 0
            Fy = -self.masa * self.g - D * (Vy / V) if V > 0 else -self.masa * self.g

            # Actualizar velocidades usando RK4 (Runge-Kutta de 4º orden)
            ax = Fx / self.masa
            ay = Fy / self.masa

            # Actualizar velocidades
            Vx_new = Vx + ax * dt
            Vy_new = Vy + ay * dt

            # Actualizar posiciones
            x_new = x + Vx * dt + 0.5 * ax * dt ** 2
            y_new = y + Vy * dt + 0.5 * ay * dt ** 2

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
        plt.figure(figsize=(15, 5))

        # Subplot 1: Trayectoria
        plt.subplot(121)
        plt.plot(self.X, self.Y)
        plt.title('Trayectoria del Proyectil')
        plt.xlabel('Distancia Horizontal (m)')
        plt.ylabel('Altura (m)')
        plt.grid(True)

        # Subplot 2: Evolución del Cd
        plt.subplot(122)
        plt.plot(self.tiempos, self.cd_history)
        plt.title('Evolución del Coeficiente de Arrastre')
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Cd')
        plt.grid(True)

        plt.tight_layout()
        plt.show()
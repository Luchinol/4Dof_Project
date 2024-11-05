# modelos/coeficientes.py

class CoeficientesAerodinamicos:
  def __init__(self):
      pass

  def calcular_coeficiente_arrastre(self, V, angulo_ataque_rad):
      # Método simplificado para calcular Cd
      Cd0 = 0.095  # Coeficiente de arrastre base para el proyectil de mortero
      Cd = Cd0 + 0.05 * angulo_ataque_rad  # Ajuste según el ángulo de ataque
      return Cd

  def calcular_coeficiente_sustentacion(self, V, angulo_ataque_rad):
      # Método simplificado para calcular Cl
      Cl = 0.0  # Asumiendo sustentación despreciable
      return Cl
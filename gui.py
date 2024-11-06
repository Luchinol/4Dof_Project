import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from calculadora.calculadora_balistica import CalculadoraBalistica
from calculadora.exportar_datos import calcular_datos_tabla, exportar_a_csv  # Importar las funciones


class AplicacionGUI(tk.Tk):
  def __init__(self):
      super().__init__()
      self.title("Calculadora Balística")
      self.geometry("450x400")
      self.modelo_seleccionado = tk.StringVar(value='masa_puntual')
      self.crear_widgets()

  def crear_widgets(self):
      # Cargar imágenes
      self.logo1 = ImageTk.PhotoImage(Image.open("imagenes/logo1.png").resize((50, 50)))
      self.logo2 = ImageTk.PhotoImage(Image.open("imagenes/logo2.jpg").resize((50, 50)))

      # Mostrar imágenes
      tk.Label(self, image=self.logo1).grid(row=0, column=0, columnspan=1)
      tk.Label(self, image=self.logo2).grid(row=0, column=2, columnspan=2)

      # Selección del modelos
      tk.Label(self, text="Seleccione el Modelo:").grid(row=1, column=0, sticky='e')
      tk.Radiobutton(self, text="Masa Puntual", variable=self.modelo_seleccionado,
                     value='masa_puntual').grid(row=1, column=1, sticky='w')
      tk.Radiobutton(self, text="4DOF", variable=self.modelo_seleccionado,
                     value='4dof').grid(row=2, column=1, sticky='w')

      # Etiquetas y campos de entrada
      tk.Label(self, text="Ángulo de Ataque/Lanzamiento (grados):").grid(row=3, column=0, sticky='e')
      self.entrada_angulo = tk.Entry(self)
      self.entrada_angulo.grid(row=3, column=1)

      tk.Label(self, text="Velocidad Inicial (m/s):").grid(row=4, column=0, sticky='e')
      self.entrada_velocidad = tk.Entry(self)
      self.entrada_velocidad.grid(row=4, column=1)
      self.entrada_velocidad.insert(0, "320")  # Valor por defecto

      tk.Label(self, text="Altura Inicial (m):").grid(row=5, column=0, sticky='e')
      self.entrada_altura = tk.Entry(self)
      self.entrada_altura.grid(row=5, column=1)

      tk.Label(self, text="Densidad del Aire (kg/m³):").grid(row=6, column=0, sticky='e')
      self.entrada_densidad = tk.Entry(self)
      self.entrada_densidad.grid(row=6, column=1)
      self.entrada_densidad.insert(0, "1.225")  # Valor por defecto al nivel del mar

      # Nuevo campo para la latitud
      tk.Label(self, text="Latitud (grados):").grid(row=7, column=0, sticky='e')
      self.entrada_latitud = tk.Entry(self)
      self.entrada_latitud.grid(row=7, column=1)
      self.entrada_latitud.insert(0, "32.0")  # Valor por defecto (latitud media)

      # Etiquetas de salida
      self.etiqueta_tiempo_vuelo = tk.Label(self, text="Tiempo de Vuelo: N/A")
      self.etiqueta_tiempo_vuelo.grid(row=9, column=0, columnspan=2)

      self.etiqueta_alcance_maximo = tk.Label(self, text="Alcance Máximo: N/A")
      self.etiqueta_alcance_maximo.grid(row=10, column=0, columnspan=2)

      self.etiqueta_altura_maxima = tk.Label(self, text="Altura Máxima: N/A")
      self.etiqueta_altura_maxima.grid(row=11, column=0, columnspan=2)

      # Botones
      tk.Button(self, text="Calcular", command=self.calcular).grid(row=8, column=0)
      tk.Button(self, text="Reiniciar", command=self.reiniciar).grid(row=8, column=1)
      tk.Button(self, text="Graficar Trayectoria", command=self.graficar_trayectoria).grid(row=12, column=0)
      tk.Button(self, text="Exportar a CSV", command=self.exportar_csv).grid(row=12, column=1)

      # Botón para exportar datos de la tabla
      tk.Button(self, text="Exportar Tabla de Tiro", command=self.exportar_tabla).grid(row=13, column=0)


  def calcular(self):
      try:
          angulo = float(self.entrada_angulo.get())
          velocidad = float(self.entrada_velocidad.get())
          altura = float(self.entrada_altura.get())
          densidad = float(self.entrada_densidad.get())
          latitud = float(self.entrada_latitud.get())
          modelo = self.modelo_seleccionado.get()

          self.calculadora = CalculadoraBalistica(modelo)
          self.calculadora.establecer_parametros(angulo, velocidad, altura, densidad, latitud)
          self.calculadora.calcular_trayectoria()

          # Actualizar etiquetas de salida
          self.etiqueta_tiempo_vuelo.config(text=f"Tiempo de Vuelo: {self.calculadora.tiempo_de_vuelo:.2f} s")
          self.etiqueta_alcance_maximo.config(text=f"Alcance Máximo: {self.calculadora.alcance_maximo:.2f} m")
          self.etiqueta_altura_maxima.config(text=f"Altura Máxima: {self.calculadora.altura_maxima:.2f} m")

          messagebox.showinfo("Cálculo Completo", "El cálculo de la trayectoria se completó exitosamente.")

      except ValueError:
          messagebox.showerror("Error de Entrada", "Por favor, ingresa valores numéricos válidos.")

  def reiniciar(self):
      # Limpiar campos y etiquetas
      self.entrada_angulo.delete(0, tk.END)
      self.entrada_velocidad.delete(0, tk.END)
      self.entrada_velocidad.insert(0, "320")  # Mantener valor por defecto
      self.entrada_altura.delete(0, tk.END)
      self.entrada_densidad.delete(0, tk.END)
      self.entrada_densidad.insert(0, "1.225")  # Valor por defecto
      self.entrada_latitud.delete(0, tk.END)
      self.entrada_latitud.insert(0, "32.0")  # Valor por defecto
      self.etiqueta_tiempo_vuelo.config(text="Tiempo de Vuelo: N/A")
      self.etiqueta_alcance_maximo.config(text="Alcance Máximo: N/A")
      self.etiqueta_altura_maxima.config(text="Altura Máxima: N/A")
      self.modelo_seleccionado.set('masa_puntual')
      if hasattr(self, 'calculadora'):
          del self.calculadora

  def graficar_trayectoria(self):
      if hasattr(self, 'calculadora') and self.calculadora.X:
          self.calculadora.graficar_trayectoria()
      else:
          messagebox.showwarning("Sin Datos", "Por favor, realiza un cálculo primero.")

  def exportar_csv(self):
      if hasattr(self, 'calculadora') and self.calculadora.tiempos:
          archivo = filedialog.asksaveasfilename(defaultextension='.csv',
                                                 filetypes=[("Archivos CSV", "*.csv")])
          if archivo:
              self.calculadora.exportar_a_csv(archivo)
              messagebox.showinfo("Exportación Completa", f"Datos exportados a {archivo}")
      else:
          messagebox.showwarning("Sin Datos", "Por favor, realiza un cálculo primero.")

  def exportar_tabla(self):
      if hasattr(self, 'calculadora'):
          try:
              velocidad = float(self.entrada_velocidad.get())
              altura = float(self.entrada_altura.get())
              densidad = float(self.entrada_densidad.get())
              latitud = float(self.entrada_latitud.get())

              archivo = filedialog.asksaveasfilename(
                  defaultextension='.csv',
                  filetypes=[("Archivos CSV", "*.csv")]
              )

              if archivo:
                  datos = calcular_datos_tabla(
                      velocidad_inicial=velocidad,
                      altura_inicial=altura,
                      densidad_aire=densidad,
                      latitud=latitud
                  )
                  exportar_a_csv(datos, archivo)
                  messagebox.showinfo("Exportación Completa", f"Tabla de tiro exportada a {archivo}")
          except ValueError:
              messagebox.showerror("Error", "Por favor, verifica que todos los campos numéricos sean válidos")
      else:
          messagebox.showwarning("Sin datos", "Por favor, realiza un cálculo primero")
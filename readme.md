Calculadora Balística 4DOF y Modelo de Masa Puntual

Este proyecto implementa una calculadora balística en Python que permite simular la trayectoria de un proyectil utilizando dos modelos diferentes: un modelo de 4 grados de libertad (4DOF) y un modelo de masa puntual.  La calculadora proporciona una interfaz gráfica de usuario (GUI) construida con Tkinter para facilitar la entrada de parámetros y la visualización de resultados.
Funcionalidades

    Dos Modelos de Simulación:
        Modelo 4DOF: Considera las fuerzas de arrastre, sustentación y el momento de cabeceo, permitiendo un análisis más preciso de la trayectoria. El ángulo de ataque es variable, mientras que el ángulo de deslizamiento se mantiene fijo en cero. Se consideran los efectos de Coriolis. El efecto Magnus se considera cero, asumiendo que el proyectil no gira.
        Modelo de Masa Puntual: Un modelo simplificado que considera al proyectil como una partícula puntual, sujeto únicamente a la fuerza de gravedad y la fuerza de arrastre. Es computacionalmente menos costoso que el modelo 4DOF.

    Interfaz Gráfica Intuitiva:  La GUI permite al usuario ingresar los parámetros de la simulación, como el ángulo de lanzamiento, la velocidad inicial, la altura inicial y la densidad del aire.

    Visualización de la Trayectoria:  El programa genera un gráfico 2D de la trayectoria del proyectil utilizando Matplotlib, mostrando la distancia horizontal y vertical recorrida.

    Exportación de Datos:  Los resultados de la simulación, incluyendo tiempo, posición, y velocidades en cada instante, se pueden exportar a un archivo CSV para su posterior análisis.

    Estructura Modular: El código está organizado en diferentes módulos y clases para facilitar la modificación, el mantenimiento y la extensión del proyecto.

Estructura del Proyecto

El proyecto está organizado en las siguientes carpetas y archivos:

Calculadora_Balistica_4DOF/
│
├── main.py                      # Archivo principal para ejecutar la aplicación
├── gui.py                       # Interfaz gráfica de usuario (Tkinter)
├── funciones.py                  # Funciones auxiliares
├── modelos/
│   ├── __init__.py              # Inicializa el paquete 'modelos'
│   ├── modelo_masa_puntual.py   # Implementación del modelo de masa puntual
│   ├── modelo_4dof.py          # Implementación del modelo 4DOF
│   └── coeficientes.py         # Cálculo de coeficientes aerodinámicos
└── calculadora/
    ├── __init__.py              # Inicializa el paquete 'calculadora'
    ├── calculadora_balistica.py  # Lógica principal de la calculadora
    └── trayectoria.py           # (Para futuras expansiones)

Cómo Ejecutar el Proyecto

    Requisitos: Asegúrate de tener Python 3 instalado junto con las siguientes bibliotecas:
        tkinter (generalmente incluida en la instalación estándar de Python)
        numpy
        matplotlib
        csv

    Clonar el Repositorio (si aplica): Si el proyecto está alojado en un repositorio Git, clónalo a tu máquina local.

    Navegar al Directorio: Abre una terminal o línea de comandos y navega al directorio raíz del proyecto 

    Ejecutar el Programa: Ejecuta el archivo main.py utilizando el siguiente comando: 
    
    Utilizar la Interfaz Gráfica:

    Selecciona el modelo de simulación deseado ("Masa Puntual" o "4DOF").
    Introduce los parámetros de la simulación en los campos correspondientes.
    Haz clic en el botón "Calcular" para ejecutar la simulación.
    Los resultados se mostrarán en la interfaz gráfica.
    Puedes visualizar la trayectoria haciendo clic en "Graficar Trayectoria".
    Puedes exportar los datos a un archivo CSV haciendo clic en "Exportar a CSV".


Descripción de los Módulos

    main.py:  Punto de entrada del programa. Inicializa y ejecuta la GUI.

    gui.py:  Contiene la clase AplicacionGUI que gestiona la interfaz gráfica, la entrada de datos del usuario y la visualización de resultados.

    funciones.py:  Contiene funciones auxiliares, como la conversión de unidades.

    modelos/modelo_masa_puntual.py: Implementa el modelo de masa puntual, incluyendo el cálculo de la trayectoria y la representación gráfica.

    modelos/modelo_4dof.py: Implementa el modelo 4DOF, incluyendo el cálculo de la trayectoria y la representación gráfica.

    modelos/coeficientes.py:  Contiene funciones para calcular los coeficientes aerodinámicos, como el coeficiente de arrastre y el coeficiente de sustentación.

    calculadora/calculadora_balistica.py:  Contiene la lógica principal de la calculadora, incluyendo la gestión de los diferentes modelos y la ejecución de los cálculos.

    calculadora/trayectoria.py:  Reservado para futuras expansiones relacionadas con el cálculo de la trayectoria.

Personalización y Extensión

    Coeficientes Aerodinámicos:  Los coeficientes aerodinámicos se pueden modificar en el archivo coeficientes.py para ajustar la simulación a diferentes proyectiles o condiciones atmosféricas.

    Nuevos Modelos:  Se pueden agregar nuevos modelos de simulación creando nuevos archivos en la carpeta modelos e integrándolos en la clase CalculadoraBalistica.

    Funcionalidades Adicionales:  Se pueden agregar nuevas funcionalidades a la calculadora, como la consideración del viento, la variación de la densidad del aire con la altitud, etc.

Contribuciones

Las contribuciones al proyecto son bienvenidas.  Si encuentras algún error o tienes alguna sugerencia para mejorar el código, por favor, crea un "issue" o envía un "pull request".
Licencia


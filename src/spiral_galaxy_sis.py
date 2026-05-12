import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# 1. Función de mapeo para una lente SIS (Esfera Isotérmica Singular)
# =============================================================================
def mapeo_lente_sis(coordenadas_x, coordenadas_y, radio_einstein, centro=(0.0, 0.0)):
    """
    Remapea la cuadrícula del plano imagen a la posición en el plano fuente usando el modelo SIS.
    :param coordenadas_x: Matriz 2D con las coordenadas X en el plano imagen.
    :param coordenadas_y: Matriz 2D con las coordenadas Y en el plano imagen.
    :param radio_einstein: Radio de Einstein (θ_E).
    :param centro: Centro de la lente (x, y).
    :return: (beta_x, beta_y) - Coordenadas en el plano fuente.
    """
    x_ajustado = coordenadas_x - centro[0]
    y_ajustado = coordenadas_y - centro[1]
    distancia = np.sqrt(x_ajustado**2 + y_ajustado**2) + 1e-15  # Evitar división por cero
    alpha = (radio_einstein**2) / distancia
    alpha_x = alpha * (x_ajustado / distancia)
    alpha_y = alpha * (y_ajustado / distancia)
    beta_x = coordenadas_x - alpha_x
    beta_y = coordenadas_y - alpha_y
    return beta_x, beta_y

# =============================================================================
# 2. Función de intensidad para una galaxia espiral
# =============================================================================
def galaxia_espiral(beta_x, beta_y, intensidad_max=1.0, escala_disco=0.8, amplitud=0.3, m=2):
    """
    Modelo para galaxia espiral:
      - Perfil exponencial para el disco: I_disco = I0 * exp(-r / escala_disco)
      - Modulación armónica para simular los brazos: 1 + amplitud * cos(m * φ)
    :param beta_x: Coordenadas x en el plano fuente.
    :param beta_y: Coordenadas y en el plano fuente.
    :param intensidad_max: Valor máximo de la intensidad (I0).
    :param escala_disco: Escala del disco (r_d).
    :param amplitud: Amplitud de la modulación (A).
    :param m: Número de brazos.
    :return: Matriz 2D con la intensidad.
    """
    r = np.sqrt(beta_x**2 + beta_y**2)
    phi = np.arctan2(beta_y, beta_x)
    I_disco = intensidad_max * np.exp(-r / escala_disco)
    modulacion = 1 + amplitud * np.cos(m * phi)
    return I_disco * modulacion

# =============================================================================
# 3. Función para la luz de la galaxia-lente (opcional)
# =============================================================================
def luz_de_lente(coordenadas_x, coordenadas_y, intensidad_max=0.5, sigma_lente=0.4, centro=(0.0, 0.0)):
    """
    Modelo gaussiano para la luz de la galaxia-lente en el plano imagen.
    :param coordenadas_x: Coordenadas X en el plano imagen.
    :param coordenadas_y: Coordenadas Y en el plano imagen.
    :param intensidad_max: Valor máximo de la intensidad de la lente.
    :param sigma_lente: Ancho (sigma) de la gaussiana.
    :param centro: Centro de la galaxia-lente.
    :return: Matriz 2D con la intensidad de la lente.
    """
    x_ajustado = coordenadas_x - centro[0]
    y_ajustado = coordenadas_y - centro[1]
    return intensidad_max * np.exp(-(x_ajustado**2 + y_ajustado**2) / (2 * sigma_lente**2))

# =============================================================================
# 4. Función para simular el efecto de lente SIS
# =============================================================================
def simular_lente_sis(funcion_fuente,
                      radio_einstein=1.0,
                      limite_cuadricula=2.0,
                      num_puntos=500,
                      parametros_fuente={},
                      centro_lente=(0.0, 0.0),
                      funcion_luz_lente=None,
                      parametros_luz_lente={}):
    """
    Crea la cuadrícula en el plano imagen, aplica el mapeo SIS y evalúa la fuente.
    Si se desea, añade la luz de la galaxia-lente.
    :return: (X, Y, intensidad_total)
    """
    eje_x = np.linspace(-limite_cuadricula, limite_cuadricula, num_puntos)
    eje_y = np.linspace(-limite_cuadricula, limite_cuadricula, num_puntos)
    X, Y = np.meshgrid(eje_x, eje_y)
    beta_x, beta_y = mapeo_lente_sis(X, Y, radio_einstein, centro=centro_lente)
    intensidad_fuente = funcion_fuente(beta_x, beta_y, **parametros_fuente)
    if funcion_luz_lente is not None:
        intensidad_fuente += funcion_luz_lente(X, Y, **parametros_luz_lente)
    return X, Y, intensidad_fuente

# =============================================================================
# 5. Parámetros generales de la simulación
# =============================================================================
limite = 2.0      # Extensión de la cuadrícula
puntos = 500      # Resolución de la cuadrícula
radio_einstein = 1.0  # Radio de Einstein

# -------------------------------
# A) Para galaxia espiral de 2 brazos (m=2)
# -------------------------------
parametros_espiral_2 = {
    'intensidad_max': 1.0,
    'escala_disco': 0.8,
    'amplitud': 0.3,
    'm': 2
}

# (1) Espiral de 2 brazos sin lente (evaluada directamente en el plano fuente)
eje_x = np.linspace(-limite, limite, puntos)
eje_y = np.linspace(-limite, limite, puntos)
X_sin_lente_2, Y_sin_lente_2 = np.meshgrid(eje_x, eje_y)
intensidad_espiral_2_sin_lente = galaxia_espiral(X_sin_lente_2, Y_sin_lente_2, **parametros_espiral_2)

# (2) Espiral de 2 brazos con lente SIS SIN luz de la lente
X_sis_sin_luz_2, Y_sis_sin_luz_2, intensidad_sis_sin_luz_2 = simular_lente_sis(
    funcion_fuente=galaxia_espiral,
    radio_einstein=radio_einstein,
    limite_cuadricula=limite,
    num_puntos=puntos,
    parametros_fuente=parametros_espiral_2,
    centro_lente=(0.0, 0.0),
    funcion_luz_lente=None,
    parametros_luz_lente={}
)

# (3) Espiral de 2 brazos con lente SIS CON luz de la lente
parametros_luz = {
    'intensidad_max': 0.5,
    'sigma_lente': 0.4,
    'centro': (0.0, 0.0)
}
X_sis_con_luz_2, Y_sis_con_luz_2, intensidad_sis_con_luz_2 = simular_lente_sis(
    funcion_fuente=galaxia_espiral,
    radio_einstein=radio_einstein,
    limite_cuadricula=limite,
    num_puntos=puntos,
    parametros_fuente=parametros_espiral_2,
    centro_lente=(0.0, 0.0),
    funcion_luz_lente=luz_de_lente,
    parametros_luz_lente=parametros_luz
)

# -------------------------------
# B) Para galaxia espiral de 3 brazos (m=3)
# -------------------------------
parametros_espiral_3 = {
    'intensidad_max': 1.0,
    'escala_disco': 0.8,
    'amplitud': 0.3,
    'm': 3
}

# (1) Espiral de 3 brazos sin lente
X_sin_lente_3, Y_sin_lente_3 = np.meshgrid(eje_x, eje_y)
intensidad_espiral_3_sin_lente = galaxia_espiral(X_sin_lente_3, Y_sin_lente_3, **parametros_espiral_3)

# (2) Espiral de 3 brazos con lente SIS SIN luz de la lente
X_sis_sin_luz_3, Y_sis_sin_luz_3, intensidad_sis_sin_luz_3 = simular_lente_sis(
    funcion_fuente=galaxia_espiral,
    radio_einstein=radio_einstein,
    limite_cuadricula=limite,
    num_puntos=puntos,
    parametros_fuente=parametros_espiral_3,
    centro_lente=(0.0, 0.0),
    funcion_luz_lente=None,
    parametros_luz_lente={}
)

# (3) Espiral de 3 brazos con lente SIS CON luz de la lente
X_sis_con_luz_3, Y_sis_con_luz_3, intensidad_sis_con_luz_3 = simular_lente_sis(
    funcion_fuente=galaxia_espiral,
    radio_einstein=radio_einstein,
    limite_cuadricula=limite,
    num_puntos=puntos,
    parametros_fuente=parametros_espiral_3,
    centro_lente=(0.0, 0.0),
    funcion_luz_lente=luz_de_lente,
    parametros_luz_lente=parametros_luz
)

# =============================================================================
# 6. Visualización de los resultados
# =============================================================================
# Se crea una figura con 2 filas y 3 columnas:
# - Fila 1: Espiral de 2 brazos.
# - Fila 2: Espiral de 3 brazos.
plt.figure(figsize=(18, 10))

# ------------------ Fila 1: Espiral de 2 brazos ------------------
# Subplot 1: Sin lente
plt.subplot(2, 3, 1)
plt.imshow(intensidad_espiral_2_sin_lente, origin='lower',
           extent=[-limite, limite, -limite, limite],
           cmap='plasma')
plt.title("Espiral 2 brazos (Sin lente)")
plt.xlabel("x (plano fuente)")
plt.ylabel("y (plano fuente)")
plt.colorbar()

# Subplot 2: SIS sin luz de la lente
plt.subplot(2, 3, 2)
plt.imshow(intensidad_sis_sin_luz_2, origin='lower',
           extent=[-limite, limite, -limite, limite],
           cmap='plasma')
plt.title("SIS 2 brazos (Sin luz de la lente)")
plt.xlabel("θ_x")
plt.ylabel("θ_y")
plt.colorbar()

# Subplot 3: SIS con luz de la lente
plt.subplot(2, 3, 3)
plt.imshow(intensidad_sis_con_luz_2, origin='lower',
           extent=[-limite, limite, -limite, limite],
           cmap='plasma')
plt.title("SIS 2 brazos (Con luz de la lente)")
plt.xlabel("θ_x")
plt.ylabel("θ_y")
plt.colorbar()

# ------------------ Fila 2: Espiral de 3 brazos ------------------
# Subplot 4: Sin lente
plt.subplot(2, 3, 4)
plt.imshow(intensidad_espiral_3_sin_lente, origin='lower',
           extent=[-limite, limite, -limite, limite],
           cmap='plasma')
plt.title("Espiral 3 brazos (Sin lente)")
plt.xlabel("x (plano fuente)")
plt.ylabel("y (plano fuente)")
plt.colorbar()

# Subplot 5: SIS sin luz de la lente
plt.subplot(2, 3, 5)
plt.imshow(intensidad_sis_sin_luz_3, origin='lower',
           extent=[-limite, limite, -limite, limite],
           cmap='plasma')
plt.title("SIS 3 brazos (Sin luz de la lente)")
plt.xlabel("θ_x")
plt.ylabel("θ_y")
plt.colorbar()

# Subplot 6: SIS con luz de la lente
plt.subplot(2, 3, 6)
plt.imshow(intensidad_sis_con_luz_3, origin='lower',
           extent=[-limite, limite, -limite, limite],
           cmap='plasma')
plt.title("SIS 3 brazos (Con luz de la lente)")
plt.xlabel("θ_x")
plt.ylabel("θ_y")
plt.colorbar()

plt.tight_layout()
plt.show()



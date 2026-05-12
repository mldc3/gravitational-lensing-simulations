import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# 1. Función de mapeo para una lente SIS (Esfera Isotérmica Singular)
# =============================================================================
def mapeo_lente_sis(coordenadas_x, coordenadas_y, radio_einstein, centro=(0.0, 0.0)):
    """
    Calcula la posición en el plano fuente (beta_x, beta_y) asumiendo una lente SIS.
    :param coordenadas_x: Matriz 2D con las coordenadas X en el plano imagen
    :param coordenadas_y: Matriz 2D con las coordenadas Y en el plano imagen
    :param radio_einstein: Radio de Einstein (theta_E)
    :param centro: Centro de la lente (x, y)
    :return: (beta_x, beta_y)
    """
    # Ajustamos las coordenadas al centro de la lente
    x_ajustado = coordenadas_x - centro[0]
    y_ajustado = coordenadas_y - centro[1]
    
    # Distancia radial desde el centro
    distancia = np.sqrt(x_ajustado**2 + y_ajustado**2) + 1e-15  # evitar división por cero
    
    # Magnitud de la deflexión: α = (theta_E^2) / r
    alpha = (radio_einstein**2) / distancia
    
    # Componentes de la deflexión en x e y
    alpha_x = alpha * (x_ajustado / distancia)
    alpha_y = alpha * (y_ajustado / distancia)
    
    # Posición en el plano fuente
    beta_x = coordenadas_x - alpha_x
    beta_y = coordenadas_y - alpha_y
    
    return beta_x, beta_y


# =============================================================================
# 2. Función de intensidad de galaxia elíptica (modelo gaussiano anisotrópico)
# =============================================================================
def galaxia_eliptica(beta_x, beta_y, intensidad_max=1.0, centro=(0.0, 0.0),
                     sigma_x=0.4, sigma_y=0.2, angulo=0.0):
    """
    Calcula la intensidad de una galaxia elíptica usando una gaussiana anisotrópica.
    :param beta_x: Matriz 2D de coordenadas x en el plano fuente
    :param beta_y: Matriz 2D de coordenadas y en el plano fuente
    :param intensidad_max: Valor máximo de la intensidad (I0)
    :param centro: Centro de la galaxia en el plano fuente
    :param sigma_x: Dispersión (ancho) en la dirección x
    :param sigma_y: Dispersión (ancho) en la dirección y
    :param angulo: Ángulo de rotación de la elipse (en radianes)
    :return: Matriz 2D con la intensidad
    """
    # Trasladamos las coordenadas para centrar la galaxia
    bx = beta_x - centro[0]
    by = beta_y - centro[1]
    
    # Rotamos el sistema de coordenadas para inclinar la elipse
    bx_rot = bx * np.cos(angulo) + by * np.sin(angulo)
    by_rot = -bx * np.sin(angulo) + by * np.cos(angulo)
    
    # Gaussiana anisotrópica
    exponente = (bx_rot**2)/(2*sigma_x**2) + (by_rot**2)/(2*sigma_y**2)
    intensidad = intensidad_max * np.exp(-exponente)
    
    return intensidad


# =============================================================================
# 3. Luz de la galaxia-lente (opcional)
# =============================================================================
def luz_de_lente(coordenadas_x, coordenadas_y, intensidad_max=0.5, sigma_lente=0.4, centro=(0.0, 0.0)):
    """
    Modelo gaussiano para la luz de la galaxia-lente en el plano imagen.
    :param coordenadas_x: Matriz 2D con las coordenadas X en el plano imagen
    :param coordenadas_y: Matriz 2D con las coordenadas Y en el plano imagen
    :param intensidad_max: Valor máximo de la intensidad de la lente
    :param sigma_lente: Ancho (sigma) de la gaussiana de la lente
    :param centro: Centro de la galaxia-lente
    :return: Matriz 2D con la intensidad de la lente
    """
    x_ajustado = coordenadas_x - centro[0]
    y_ajustado = coordenadas_y - centro[1]
    distancia_cuadrado = x_ajustado**2 + y_ajustado**2
    return intensidad_max * np.exp(-distancia_cuadrado / (2 * sigma_lente**2))


# =============================================================================
# 4. Función para simular la lente SIS
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
    Opcionalmente, añade la luz de la galaxia-lente.
    """
    # Creamos la cuadrícula en el plano imagen
    eje_x = np.linspace(-limite_cuadricula, limite_cuadricula, num_puntos)
    eje_y = np.linspace(-limite_cuadricula, limite_cuadricula, num_puntos)
    X, Y = np.meshgrid(eje_x, eje_y)
    
    # Aplicamos el mapeo de lente SIS
    beta_x, beta_y = mapeo_lente_sis(X, Y, radio_einstein, centro=centro_lente)
    
    # Calculamos la intensidad de la fuente (galaxia) en esas coordenadas
    intensidad_lente = funcion_fuente(beta_x, beta_y, **parametros_fuente)
    
    # Si se quiere, sumamos la luz de la lente
    if funcion_luz_lente is not None:
        intensidad_lente += funcion_luz_lente(X, Y, **parametros_luz_lente)
    
    return X, Y, intensidad_lente


# =============================================================================
# 5. Generación de las TRES imágenes solicitadas
# =============================================================================

# --- (1) Galaxia elíptica sin lente ---
limite = 2.0
puntos = 500
eje_x = np.linspace(-limite, limite, puntos)
eje_y = np.linspace(-limite, limite, puntos)
X_sin_lente, Y_sin_lente = np.meshgrid(eje_x, eje_y)

# Parámetros de la galaxia elíptica
parametros_eliptica = {
    'intensidad_max': 1.0,
    'centro': (0.0, 0.0),
    'sigma_x': 0.4,
    'sigma_y': 0.2,
    'angulo': np.pi/6  # rotación de 30°
}

# Evaluamos la galaxia elíptica directamente (sin lente)
intensidad_eliptica_sin_lente = galaxia_eliptica(X_sin_lente, Y_sin_lente, **parametros_eliptica)

# --- (2) Lente SIS sin luz de la lente ---
X_sis_sin_luz, Y_sis_sin_luz, intensidad_sis_sin_luz = simular_lente_sis(
    funcion_fuente=galaxia_eliptica,
    radio_einstein=1.0,  # ajusta si quieres un anillo más grande o más pequeño
    limite_cuadricula=2.0,
    num_puntos=500,
    parametros_fuente=parametros_eliptica,   # misma galaxia elíptica
    centro_lente=(0.0, 0.0),
    funcion_luz_lente=None,                 # sin luz de la lente
    parametros_luz_lente={}
)

# --- (3) Lente SIS con luz de la lente ---
parametros_luz = {
    'intensidad_max': 0.5,
    'sigma_lente': 0.4,
    'centro': (0.0, 0.0)
}

X_sis_con_luz, Y_sis_con_luz, intensidad_sis_con_luz = simular_lente_sis(
    funcion_fuente=galaxia_eliptica,
    radio_einstein=1.0,
    limite_cuadricula=2.0,
    num_puntos=500,
    parametros_fuente=parametros_eliptica,
    centro_lente=(0.0, 0.0),
    funcion_luz_lente=luz_de_lente,        # activamos la luz de la lente
    parametros_luz_lente=parametros_luz
)

# =============================================================================
# 6. Visualización de los resultados
# =============================================================================

plt.figure(figsize=(18, 5))

# Subplot 1: Galaxia elíptica sin lente
plt.subplot(1, 3, 1)
plt.imshow(intensidad_eliptica_sin_lente,
           origin='lower',
           extent=[-limite, limite, -limite, limite],
           cmap='plasma')
plt.title("Galaxia Elíptica (Sin Lente)")
plt.xlabel("x (plano fuente)")
plt.ylabel("y (plano fuente)")
plt.colorbar()

# Subplot 2: Galaxia elíptica con SIS (sin luz)
plt.subplot(1, 3, 2)
plt.imshow(intensidad_sis_sin_luz,
           origin='lower',
           extent=[-limite, limite, -limite, limite],
           cmap='plasma')
plt.title("SIS (Sin luz de la lente)")
plt.xlabel("θ_x")
plt.ylabel("θ_y")
plt.colorbar()

# Subplot 3: Galaxia elíptica con SIS (con luz)
plt.subplot(1, 3, 3)
plt.imshow(intensidad_sis_con_luz,
           origin='lower',
           extent=[-limite, limite, -limite, limite],
           cmap='plasma')
plt.title("SIS (Con luz de la lente)")
plt.xlabel("θ_x")
plt.ylabel("θ_y")
plt.colorbar()

plt.tight_layout()
plt.show()


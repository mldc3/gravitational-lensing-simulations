import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# 1. Mapeo de lente para un modelo SIS (Esfera Isotérmica Singular)
# =============================================================================
def mapeo_lente_sis(coordenadas_x, coordenadas_y, radio_einstein, centro=(0.0, 0.0)):
    """
    Calcula la posición en el plano fuente (beta_x, beta_y) para un modelo de lente SIS.
    :param coordenadas_x: matriz 2D con coordenadas X en el plano imagen
    :param coordenadas_y: matriz 2D con coordenadas Y en el plano imagen
    :param radio_einstein: valor de θ_E (radio de Einstein)
    :param centro: centro de la lente (x, y)
    :return: (beta_x, beta_y)
    """
    # Se ajustan las coordenadas según el centro de la lente
    x_ajustado = coordenadas_x - centro[0]
    y_ajustado = coordenadas_y - centro[1]
    
    # Se calcula la distancia radial desde el centro
    distancia = np.sqrt(x_ajustado**2 + y_ajustado**2) + 1e-15  # evitar división por cero
    
    # Magnitud de la deflexión: α = θ_E^2 / r
    alpha = (radio_einstein**2) / distancia
    
    # Componentes de la deflexión
    alpha_x = alpha * (x_ajustado / distancia)
    alpha_y = alpha * (y_ajustado / distancia)
    
    # Posición en el plano fuente
    beta_x = coordenadas_x - alpha_x
    beta_y = coordenadas_y - alpha_y
    return beta_x, beta_y

# =============================================================================
# 2. Función de intensidad de la galaxia circular
# =============================================================================
def galaxia_circular(beta_x, beta_y, intensidad_max=1.0, centro=(0.0, 0.0), sigma=0.3):
    """
    Calcula la intensidad de una galaxia circular (modelo gaussiano isotrópico).
    :param beta_x: matriz 2D de coordenadas x en el plano fuente
    :param beta_y: matriz 2D de coordenadas y en el plano fuente
    :param intensidad_max: valor máximo de la intensidad (I0)
    :param centro: centro de la galaxia en el plano fuente
    :param sigma: ancho (desviación típica) de la gaussiana
    :return: matriz 2D con la intensidad
    """
    distancia_cuadrado = (beta_x - centro[0])**2 + (beta_y - centro[1])**2
    intensidad = intensidad_max * np.exp(-distancia_cuadrado / (2 * sigma**2))
    return intensidad

# =============================================================================
# 3. Luz de la galaxia-lente (opcional)
# =============================================================================
def luminosidad_de_la_lente(coordenadas_x, coordenadas_y, intensidad_max=0.5, sigma_lente=0.5, centro=(0.0, 0.0)):
    """
    Perfil de brillo (gaussiano) para la galaxia-lente en el plano imagen.
    :param coordenadas_x: matriz 2D de coordenadas X en el plano imagen
    :param coordenadas_y: matriz 2D de coordenadas Y en el plano imagen
    :param intensidad_max: valor máximo de la intensidad de la lente
    :param sigma_lente: ancho (desviación típica) de la gaussiana de la lente
    :param centro: centro de la galaxia-lente
    :return: matriz 2D con la intensidad de la lente
    """
    x_ajustado = coordenadas_x - centro[0]
    y_ajustado = coordenadas_y - centro[1]
    distancia_cuadrado = x_ajustado**2 + y_ajustado**2
    intensidad_lente = intensidad_max * np.exp(-distancia_cuadrado / (2 * sigma_lente**2))
    return intensidad_lente

# =============================================================================
# 4. Función de simulación de lente SIS
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
    Genera una cuadrícula en el plano imagen, aplica el mapeo SIS y evalúa
    la intensidad de la fuente. Opcionalmente, añade la luz de la lente.
    """
    # Crear la cuadrícula en el plano imagen
    eje_x = np.linspace(-limite_cuadricula, limite_cuadricula, num_puntos)
    eje_y = np.linspace(-limite_cuadricula, limite_cuadricula, num_puntos)
    X, Y = np.meshgrid(eje_x, eje_y)
    
    # Obtener las coordenadas de la fuente usando el mapeo SIS
    beta_x, beta_y = mapeo_lente_sis(X, Y, radio_einstein, centro=centro_lente)
    
    # Calcular la intensidad de la fuente en esas coordenadas
    intensidad_lente = funcion_fuente(beta_x, beta_y, **parametros_fuente)
    
    # Si se desea, añadir la luminosidad de la lente en el plano imagen
    if funcion_luz_lente is not None:
        intensidad_lente_total = intensidad_lente + funcion_luz_lente(X, Y, **parametros_luz_lente)
        return X, Y, intensidad_lente_total
    else:
        return X, Y, intensidad_lente

# =============================================================================
# 5. Generación de las tres imágenes
# =============================================================================

# --- 5.1: Galaxia sin lente ---
# Se crea una cuadrícula en el plano fuente "directamente" (sin mapeo)
limite = 2.0
puntos = 500
eje_x = np.linspace(-limite, limite, puntos)
eje_y = np.linspace(-limite, limite, puntos)
X_sin_lente, Y_sin_lente = np.meshgrid(eje_x, eje_y)

# Se evalúa la galaxia circular en esa cuadrícula (sin ninguna lente)
intensidad_sin_lente = galaxia_circular(X_sin_lente, Y_sin_lente, 
                                        intensidad_max=1.0, 
                                        centro=(0.0, 0.0), 
                                        sigma=0.3)

# --- 5.2: SIS sin luz de la lente ---
X_sis_sin_luz, Y_sis_sin_luz, intensidad_sis_sin_luz = simular_lente_sis(
    funcion_fuente=galaxia_circular,
    radio_einstein=1.0,          # Radio de Einstein
    limite_cuadricula=2.0,
    num_puntos=500,
    parametros_fuente={'intensidad_max': 1.0, 'centro': (0.0, 0.0), 'sigma': 0.3},
    centro_lente=(0.0, 0.0),
    funcion_luz_lente=None,
    parametros_luz_lente={}
)

# --- 5.3: SIS con luz de la lente ---
X_sis_con_luz, Y_sis_con_luz, intensidad_sis_con_luz = simular_lente_sis(
    funcion_fuente=galaxia_circular,
    radio_einstein=1.0,
    limite_cuadricula=2.0,
    num_puntos=500,
    parametros_fuente={'intensidad_max': 1.0, 'centro': (0.0, 0.0), 'sigma': 0.3},
    centro_lente=(0.0, 0.0),
    funcion_luz_lente=luminosidad_de_la_lente,  # Aquí añadimos la luz de la lente
    parametros_luz_lente={'intensidad_max': 0.5, 'sigma_lente': 0.4, 'centro': (0.0, 0.0)}
)

# =============================================================================
# 6. Visualización en 3 subplots
# =============================================================================
plt.figure(figsize=(18, 5))

# Subplot 1: Galaxia sin lente
plt.subplot(1, 3, 1)
plt.imshow(intensidad_sin_lente, origin='lower', 
           extent=[-limite, limite, -limite, limite],
           cmap='plasma')
plt.title("Galaxia sin lente")
plt.xlabel("x (plano fuente)")
plt.ylabel("y (plano fuente)")
plt.colorbar()

# Subplot 2: SIS sin luz de la lente
plt.subplot(1, 3, 2)
plt.imshow(intensidad_sis_sin_luz, origin='lower',
           extent=[-limite, limite, -limite, limite],
           cmap='plasma')
plt.title("SIS sin luz de la lente")
plt.xlabel("θ_x")
plt.ylabel("θ_y")
plt.colorbar()

# Subplot 3: SIS con luz de la lente
plt.subplot(1, 3, 3)
plt.imshow(intensidad_sis_con_luz, origin='lower',
           extent=[-limite, limite, -limite, limite],
           cmap='plasma')
plt.title("SIS con luz de la lente")
plt.xlabel("θ_x")
plt.ylabel("θ_y")
plt.colorbar()

plt.tight_layout()
plt.show()

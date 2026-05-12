# Implementation notes

## 1. Project structure

The repository contains three main Python scripts and a set of Markdown documents prepared for GitHub presentation.

### Code files

- `src/circular_galaxy_sis.py`
- `src/elliptical_galaxy_sis.py`
- `src/spiral_galaxy_sis.py`

### Documentation files

- `docs/theory_and_background.md`
- `docs/results_and_discussion.md`
- `docs/implementation_notes.md`

### Assets

- `assets/figures/simulations/`
- `assets/figures/observations/`
- `assets/figures/parameter_studies/`
- `assets/figures/special_cases/`

## 2. Shared computational workflow

All three scripts follow the same broad logic.

### Step 1 — Create a 2D grid

A uniform Cartesian grid is created with NumPy using `np.linspace` and `np.meshgrid`. This defines the sampling of the image plane.

### Step 2 — Apply the lens mapping

The function `mapeo_lente_sis(...)` computes the deflected source-plane coordinates corresponding to each image-plane point. In the original implementation, the radial deflection magnitude is written as

$$
\alpha(r) = \frac{\theta_E^2}{r}.
$$

The code subtracts the deflection components from the original image-plane coordinates to recover the source-plane coordinates.

### Step 3 — Evaluate the source brightness

Once the mapped coordinates $(\beta_x, \beta_y)$ are known, the code evaluates the chosen source-brightness function:

- `galaxia_circular(...)` for the circular Gaussian,
- `galaxia_eliptica(...)` for the elliptical Gaussian,
- `galaxia_espiral(...)` for the spiral profile.

### Step 4 — Optionally add lens light

In the circular and elliptical examples—and optionally in the spiral one—a Gaussian component is added to mimic the light of the foreground lens galaxy. This is essential for making the final image resemble real observations more closely.

### Step 5 — Display the figures

The results are plotted with Matplotlib using `imshow`, axis labels, titles, and colorbars.

## 3. Circular-source script

### File

`src/circular_galaxy_sis.py`

### Main source model

$$
I(\beta_x,\beta_y) = I_0 \exp\left[-\frac{(\beta_x-x_c)^2 + (\beta_y-y_c)^2}{2\sigma^2}\right].
$$

### Key parameters in the script

- `radio_einstein = 1.0`
- source centre `(0.0, 0.0)`
- source width `sigma = 0.3`
- lens-light amplitude `0.5`
- lens-light width `sigma_lente = 0.4`

### Output

Three panels are produced: unlensed source, lensed source without lens light, and lensed source with lens light.

## 4. Elliptical-source script

### File

`src/elliptical_galaxy_sis.py`

### Main source model

The code rotates the coordinates and evaluates an anisotropic Gaussian:

$$
I(x',y') = I_0 \exp\left[-\left(\frac{x'^2}{2\sigma_x^2} + \frac{y'^2}{2\sigma_y^2}\right)\right].
$$

### Key parameters in the script

- `sigma_x = 0.4`
- `sigma_y = 0.2`
- `angulo = \pi/6`
- `radio_einstein = 1.0`
- lens-light amplitude `0.5`
- lens-light width `sigma_lente = 0.4`

### Output

Again, the script produces three panels: source only, lensed image without lens light, and lensed image with lens light.

## 5. Spiral-source script

### File

`src/spiral_galaxy_sis.py`

### Main source model

$$
I(r,\phi) = I_0 \exp\left(-\frac{r}{r_d}\right)\left[1 + A \cos(m\phi)\right].
$$

### Key parameters in the script

Shared simulation parameters:

- `limite = 2.0`
- `puntos = 500`
- `radio_einstein = 1.0`

Two-arm case:

- `intensidad_max = 1.0`
- `escala_disco = 0.8`
- `amplitud = 0.3`
- `m = 2`

Three-arm case:

- `intensidad_max = 1.0`
- `escala_disco = 0.8`
- `amplitud = 0.3`
- `m = 3`

Lens-light parameters:

- `intensidad_max = 0.5`
- `sigma_lente = 0.4`

### Output

The script produces a $2 \times 3$ figure:

- row 1: two-arm spiral source without lens, with lens/no lens-light, with lens/with lens-light,
- row 2: three-arm spiral source without lens, with lens/no lens-light, with lens/with lens-light.

## 6. Notes on scientific interpretation

The code is effective as a teaching tool, but it should be presented honestly.

### Strengths

- clear and readable implementation,
- direct connection between equations and images,
- visually intuitive outputs,
- easy parameter tuning.

### Limitations

- very simplified lens model,
- idealized source profiles,
- no full observational pipeline,
- no parameter inference against data.

For a student-built project, these limitations are completely acceptable. In fact, the transparency of the implementation is one of its strongest features.

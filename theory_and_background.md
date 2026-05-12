# Theory and background

## 1. What is a gravitational lens?

A **gravitational lens** is a mass distribution—such as a galaxy, a galaxy group, or a cluster—that bends the trajectory of light coming from a more distant source. In general relativity, gravity is not treated as a force acting in a Newtonian sense on the photon, but as the manifestation of spacetime curvature created by mass-energy. When light propagates through that curved spacetime, its path is deflected.

This effect can produce a remarkable range of observable phenomena:

- slight shape distortions of background galaxies (**weak lensing**);
- multiple images of the same source (**strong lensing**);
- nearly circular rings when alignment is very good (**Einstein rings**);
- time-delay effects in variable sources such as quasars;
- temporary magnification events due to stars or planets (**microlensing**).

Gravitational lensing is especially important because it depends on **mass**, not on emitted light. For that reason, it is one of the most powerful tools for studying **dark matter**, mapping mass distributions, and observing galaxies that would otherwise be too faint to detect.

## 2. Einstein's idea and the origin of lensing theory

The basic idea goes back to Einstein's general theory of relativity. Once gravity is understood as spacetime curvature, light no longer travels along straight Euclidean lines in the presence of massive bodies. Instead, it follows null geodesics of the curved geometry.

In a simplified thin-lens description, one can imagine a source, a deflecting lens, and an observer aligned along the line of sight. If the alignment is almost perfect, the background source can appear stretched into a luminous ring around the foreground lens. That ring defines the **Einstein radius** $\theta_E$, which sets the characteristic angular scale of the lens system.

A widely used symbolic lens equation is

$$
\boldsymbol{\beta} = \boldsymbol{\theta} - \boldsymbol{\alpha}(\boldsymbol{\theta}),
$$

where:

- $\boldsymbol{\beta}$ is the angular position of the source in the source plane,
- $\boldsymbol{\theta}$ is the observed angular position in the image plane,
- $\boldsymbol{\alpha}(\boldsymbol{\theta})$ is the deflection angle produced by the lens.

In the original class project, the implemented radially symmetric deflection is written as

$$
\alpha(r) = \frac{\theta_E^2}{r},
$$

where $r$ is the radial distance from the lens centre. The repository labels the model as SIS in the original notes; more precisely, the implemented mapping behaves as a simple educational **radially symmetric lens model** that is very convenient for demonstrating rings and arcs.

## 3. A brief historical note

A useful milestone in the history of strong lensing is the first confirmed gravitational lens system, **Q0957+561**, also known as the **Twin Quasar**, discovered in 1979. Since then, strong-lensing observations have become central to modern astrophysics. Famous examples include the Einstein Cross, large cluster arcs, and the many ring-like systems observed by Hubble, SDSS, and, more recently, JWST.

In this project, some observed systems are used as qualitative comparison points:

- **JWST-ER1**,
- **J162746.44-005357.5**,
- **SDSS J0038+4133**.

These examples are not used for quantitative fitting here; instead, they illustrate how ring-like or arc-like morphologies arise in real data.

## 4. Simplified mass model used in the code

The original notes discuss the **Singular Isothermal Sphere (SIS)**, whose mass density is commonly written as

$$
\rho(r) = \frac{\sigma_v^2}{2 G r^2},
$$

where:

- $\sigma_v$ is the one-dimensional velocity dispersion,
- $G$ is the gravitational constant,
- $r$ is the radial distance from the centre.

The value of this model is that it offers a simple, radially symmetric description of a lensing mass distribution. Even when one works with a simplified deflection prescription in code, the SIS idea provides the conceptual background: a centrally concentrated, nearly symmetric lens can turn a compact source into arcs or rings.

## 5. Surface-brightness models for the sources

A second ingredient is the **brightness profile of the source galaxy**. The project discusses several useful ideas.

### 5.1 Sérsic profile

A general brightness profile used in astronomy is the **Sérsic law**:

$$
I(R) = I_0 \exp\left[-b_n \left(\left(\frac{R}{R_e}\right)^{1/n} - 1\right)\right].
$$

Here:

- $I(R)$ is the intensity at radius $R$,
- $I_0$ is a central or characteristic intensity,
- $R_e$ is the effective radius,
- $n$ is the Sérsic index,
- $b_n$ is a normalization-related constant.

This profile is useful because varying $n$ produces different morphologies:

- $n \approx 4$ resembles a de Vaucouleurs-like profile, often associated with **elliptical galaxies**;
- $n \approx 1$ gives a more exponential profile, typical of **disk galaxies**;
- intermediate values can describe **lenticular** or transitional systems.

The repository's actual implementation does **not** use a full Sérsic fit, but the discussion is important because it explains the physical motivation for choosing different source morphologies.

### 5.2 Point-spread-function-like Gaussian model

For the circular and elliptical examples, the project uses Gaussian surface-brightness models, which are easy to control and interpret.

For a circular source, the brightness is

$$
I(\beta_x,\beta_y) = I_0 \exp\left[-\frac{(\beta_x-x_c)^2 + (\beta_y-y_c)^2}{2\sigma^2}\right].
$$

This is an isotropic Gaussian: the source is brightest at the centre and fades smoothly with radius.

For an elliptical source, the coordinates are rotated and stretched differently along two axes, yielding an anisotropic Gaussian,

$$
I(x',y') = I_0 \exp\left[-\left(\frac{x'^2}{2\sigma_x^2} + \frac{y'^2}{2\sigma_y^2}\right)\right].
$$

This gives the source a preferred orientation and ellipticity.

### 5.3 Spiral galaxy model

The spiral model is more exploratory. The code uses an exponential disk multiplied by an angular modulation:

$$
I(r,\phi) = I_0 \exp\left(-\frac{r}{r_d}\right)\left[1 + A\cos(m\phi)\right],
$$

where:

- $r_d$ is the disk scale length,
- $A$ is the modulation amplitude,
- $m$ is the number of arms.

This produces a two-arm or three-arm pattern. It is not intended as a high-fidelity spiral-galaxy renderer, but as a compact analytic model that captures the idea of arm-like azimuthal structure.

## 6. Deflection and the role of angular distances

In a full derivation of lensing theory, the angular scale of the lens is controlled by combinations of angular-diameter distances between observer, lens, and source. In practical terms, the Einstein radius bundles that geometric information with the mass scale of the lens. That is why increasing $\theta_E$ in the simulations directly changes the radius of the ring-like structure.

## 7. Why gravitational lenses are so relevant

Gravitational lensing is not just visually striking: it is scientifically fundamental.

### 7.1 Dark matter

Because lensing probes the total gravitational field, it allows astronomers to map the mass of galaxies and clusters even when much of that mass is dark. Lensing reconstructions are among the clearest pieces of evidence that luminous matter is only part of the cosmic mass budget.

### 7.2 Magnification of distant galaxies

Strong lenses can magnify distant, faint galaxies, acting as natural telescopes. This is extremely important for studying the early Universe.

### 7.3 Hubble constant and time delays

If the background source is variable—especially a quasar—different light paths can arrive at different times. Measuring those delays and modelling the lens can help constrain the **Hubble constant**.

### 7.4 Microlensing and compact objects

At smaller scales, microlensing can reveal otherwise invisible compact objects, and it has also become an important method in **exoplanet detection**.

## 8. What the code is doing in practice

The three Python scripts all follow the same computational logic:

1. create a grid in the image plane;
2. map each point back to the source plane with the lens equation;
3. evaluate the source brightness at the mapped source-plane position;
4. optionally add a smooth light component for the foreground lens galaxy;
5. display the resulting intensity map.

This structure is deliberately simple and transparent. It makes the project educational: one can clearly see how each physical assumption translates into a visual outcome.

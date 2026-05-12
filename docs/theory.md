# Gravitational lensing theory (compact note)

In the thin-lens approximation, a source position \(\boldsymbol{\beta}\) and image position \(\boldsymbol{\theta}\) are related by:

\[
\boldsymbol{\beta} = \boldsymbol{\theta} - \boldsymbol{\alpha}(\boldsymbol{\theta})
\]

where \(\boldsymbol{\alpha}\) is the reduced deflection angle.

For an axisymmetric simplified lens, the deflection is radial and can be parameterized by an Einstein-angle scale \(\theta_E\). In this repository's educational model, \(\theta_E\) is varied to study image morphology changes.

## Why parameter studies matter

The following parameters strongly affect lensed appearance:

1. **Einstein radius (\(\theta_E\))**: controls the strength/size scale of distortion.
2. **Source width**: controls compactness and arc sharpness.
3. **Source-lens alignment**: determines ring-like vs. arc-like configurations.

The code in `src/lensing_simulations/simulations.py` provides lightweight numerical helpers for these studies.

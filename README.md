# Gravitational Lensing Simulations: Circular, Elliptical and Spiral Source Profiles

Python simulations of simplified gravitational lensing for circular, elliptical, and exploratory spiral galaxy source profiles, with theoretical background, figure analysis, parameter studies, and comparisons with observed lens systems.

## Project goals

This repository presents an educational computational-astrophysics workflow for gravitational lensing:

- introduce the lens equation and Einstein radius in a compact, practical form;
- simulate how a foreground lens distorts a background source;
- compare circular, elliptical, and exploratory spiral source-profile behavior;
- study parameter sensitivity (Einstein radius, source width, alignment);
- connect simulation outputs with representative observed lens morphologies.

## Repository structure

```text
gravitational-lensing-simulations/
├── README.md
├── docs/
│   └── theory.md
├── observations/
│   └── README.md
├── figures/
├── results/
└── src/
    └── lensing_simulations/
        ├── __init__.py
        └── simulations.py
```

## Theory summary

The simulations use a simplified thin-lens mapping with angular coordinates:

- Lens equation: **β = θ - α(θ)**
- For a simple SIS-like model, deflection is radial with magnitude related to the Einstein radius.

A short theory note is available at [docs/theory.md](docs/theory.md).

## Source profiles in this project

- **Circular source**: isotropic Gaussian-like brightness profile.
- **Elliptical source**: anisotropic Gaussian-like profile (axis ratio + position angle).
- **Spiral source (exploratory)**: a parametric pattern to explore qualitative morphology under lensing.

> The spiral case is intentionally exploratory and should not be interpreted as a precise observational reconstruction.

## Quick start

```bash
python -c "from src.lensing_simulations import demo_parameter_study; print(demo_parameter_study())"
```

## Planned outputs

- generated simulation arrays and figures in `results/` and `figures/`;
- parameter-study comparisons across Einstein radius, source width, and alignment;
- side-by-side notes against known observed lens configurations in `observations/`.

## Notes

- Repository content is maintained in **English**.
- The original source PDF is intentionally not tracked in this repository.

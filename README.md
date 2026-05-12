# Gravitational Lensing Simulations

A compact computational-astrophysics project that explores how a simplified gravitational lens distorts the light of **circular**, **elliptical** and **spiral** background galaxies. The repository combines the original Python scripts with a cleaner GitHub-ready documentation structure, a theoretical introduction, and a discussion of the simulated and observed lensing morphologies.

## Project goals

This repository was prepared to present a student-built project more clearly on GitHub. It aims to:

- explain the **physics of gravitational lensing** in an accessible but rigorous way;
- document the **Python implementation** used to generate the simulations;
- compare the simulated outputs with **real observed lens systems**;
- comment on how the images change when the **Einstein radius**, source width, alignment, or source morphology are modified.

## Repository contents

- **Theory and background**: [`docs/theory_and_background.md`](docs/theory_and_background.md)
- **Results and discussion**: [`docs/results_and_discussion.md`](docs/results_and_discussion.md)
- **Implementation notes**: [`docs/implementation_notes.md`](docs/implementation_notes.md)
- **Python source code**: [`src/`](src/)
- **Figures and comparison images**: [`assets/figures/`](assets/figures/)

## Visual overview

### Circular source with a simplified gravitational lens

![Circular galaxy simulation](assets/figures/simulations/circular_galaxy_point_lens.png)

A compact circular source becomes an almost symmetric ring when the source, lens and observer are well aligned. Adding the luminosity of the lens produces a brighter central component and makes the synthetic image more similar to real observations.

### Elliptical source with a simplified gravitational lens

![Elliptical galaxy simulation](assets/figures/simulations/elliptical_galaxy_point_lens.png)

The intrinsic elongation of the source breaks the perfect symmetry of the ring and produces a lensed image whose brightness is enhanced along preferred directions.

### Spiral-source attempt

![Spiral galaxy profiles](assets/figures/simulations/spiral_galaxy_profiles.png)

The spiral example is exploratory: the source is modeled through an exponential disk plus an angular modulation that mimics spiral arms. The output is physically suggestive, although it should be interpreted as a simplified qualitative study rather than as a precision reconstruction of a real spiral lens system.

## Main physical ingredients

The repository implements a simplified radially symmetric lens mapping, labelled as an SIS-style model in the original project, together with analytic source-brightness profiles. The key ingredients are:

- a lens equation relating source-plane and image-plane coordinates;
- a deflection field with magnitude proportional to $\theta_E^2 / r$ in the code;
- Gaussian brightness models for circular and elliptical sources;
- an exponential-plus-harmonic model for spiral galaxies;
- an optional Gaussian light component for the foreground lens galaxy.

## Key discussion points

- **Alignment** controls whether one obtains a complete ring, partial arcs, or a multiple-image configuration.
- **Einstein radius** determines the scale of the lensed morphology.
- **Source width** (for Gaussian sources) controls how thick, diffuse or compact the ring becomes.
- **Intrinsic source morphology** leaves an imprint on the brightness distribution along the lensed image.

## Running the code

Install the required packages:

```bash
pip install -r requirements.txt
```

Then run any of the scripts in `src/`:

```bash
python src/circular_galaxy_sis.py
python src/elliptical_galaxy_sis.py
python src/spiral_galaxy_sis.py
```

Each script opens a Matplotlib window with the corresponding simulated outputs.

## Suggested GitHub title

**Gravitational Lensing Simulations: Circular, Elliptical and Spiral Source Profiles**

## Suggested short description

Python simulations of simplified gravitational lensing for circular, elliptical and spiral galaxy sources, with theory, figure discussion and comparisons with real observed lens systems.

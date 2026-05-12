# Source code

This directory contains the three Python simulation scripts.

## Files

| File | Description |
|------|-------------|
| `circular_galaxy_sis.py` | Simulates gravitational lensing of a circular (Gaussian) source galaxy |
| `elliptical_galaxy_sis.py` | Simulates gravitational lensing of an elliptical (anisotropic Gaussian) source galaxy |
| `spiral_galaxy_sis.py` | Exploratory simulation of gravitational lensing applied to a spiral source model (two-arm and three-arm cases) |

## Running the scripts

Install dependencies first:

```bash
pip install -r ../requirements.txt
```

Then execute any script from the repository root:

```bash
python src/circular_galaxy_sis.py
python src/elliptical_galaxy_sis.py
python src/spiral_galaxy_sis.py
```

Each script opens a Matplotlib window with the simulated output panels.

## Notes

- All scripts use the same lens-mapping approach: a 2D image-plane grid is ray-traced back to the source plane using a simplified radially symmetric deflection.
- The spiral script is exploratory; see [`../docs/results_and_discussion.md`](../docs/results_and_discussion.md) for caveats.
- Full implementation details are in [`../docs/implementation_notes.md`](../docs/implementation_notes.md).

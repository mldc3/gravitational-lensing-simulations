"""Simplified, dependency-light lensing utilities for educational simulations."""

from __future__ import annotations

import math
from typing import Dict, Iterable, List, Tuple


Point = Tuple[float, float]


def _norm(x: float, y: float, eps: float = 1e-12) -> float:
    return math.sqrt(x * x + y * y + eps)


def sis_deflection(theta: Point, theta_e: float, lens_center: Point = (0.0, 0.0)) -> Point:
    """Return a simple SIS-like reduced deflection vector at image position theta."""
    dx = theta[0] - lens_center[0]
    dy = theta[1] - lens_center[1]
    r = _norm(dx, dy)
    return (theta_e * dx / r, theta_e * dy / r)


def circular_source(beta: Point, center: Point = (0.0, 0.0), sigma: float = 0.15) -> float:
    """Circular Gaussian-like source brightness."""
    dx = beta[0] - center[0]
    dy = beta[1] - center[1]
    return math.exp(-(dx * dx + dy * dy) / (2.0 * sigma * sigma))


def elliptical_source(
    beta: Point,
    center: Point = (0.0, 0.0),
    sigma_major: float = 0.2,
    axis_ratio: float = 0.6,
    angle_rad: float = 0.0,
) -> float:
    """Elliptical Gaussian-like source brightness."""
    dx = beta[0] - center[0]
    dy = beta[1] - center[1]
    c, s = math.cos(angle_rad), math.sin(angle_rad)
    x_rot = c * dx + s * dy
    y_rot = -s * dx + c * dy
    sigma_minor = sigma_major * max(axis_ratio, 1e-6)
    q = (x_rot / sigma_major) ** 2 + (y_rot / sigma_minor) ** 2
    return math.exp(-0.5 * q)


def exploratory_spiral_source(
    beta: Point,
    center: Point = (0.0, 0.0),
    sigma: float = 0.35,
    arm_tightness: float = 4.0,
    arm_count: int = 2,
) -> float:
    """Exploratory spiral-like brightness pattern (qualitative, not observationally exact)."""
    dx = beta[0] - center[0]
    dy = beta[1] - center[1]
    r = _norm(dx, dy)
    phi = math.atan2(dy, dx)
    envelope = math.exp(-(r * r) / (2.0 * sigma * sigma))
    arm_modulation = 0.5 * (1.0 + math.cos(arm_count * phi - arm_tightness * math.log1p(r)))
    return envelope * arm_modulation


def ray_trace_intensity(
    theta: Point,
    theta_e: float,
    source_model,
    lens_center: Point = (0.0, 0.0),
    **source_kwargs,
) -> float:
    """Map image-plane point theta to source-plane beta and evaluate source intensity."""
    ax, ay = sis_deflection(theta, theta_e=theta_e, lens_center=lens_center)
    beta = (theta[0] - ax, theta[1] - ay)
    return float(source_model(beta, **source_kwargs))


def demo_parameter_study() -> Dict[str, List[float]]:
    """Small numeric sample for Einstein-radius sensitivity at fixed coordinates."""
    theta_grid: Iterable[Point] = [(-0.3, 0.0), (-0.1, 0.1), (0.15, -0.05), (0.3, 0.0)]
    theta_e_values = [0.1, 0.2, 0.3]

    summary: Dict[str, List[float]] = {}
    for theta_e in theta_e_values:
        samples = [
            ray_trace_intensity(theta, theta_e=theta_e, source_model=circular_source, sigma=0.12)
            for theta in theta_grid
        ]
        summary[f"theta_E={theta_e:.2f}"] = [round(v, 6) for v in samples]
    return summary

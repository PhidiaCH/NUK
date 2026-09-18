"""Vapor Chamber Pillar Optimizer — Theory Core V1.

Analytical verification model only.
SI units throughout.
"""

from __future__ import annotations
from dataclasses import dataclass
import math


PLATE_ALPHA = {
    "simply_supported": 0.00406,
    "clamped": 0.00126,
}


@dataclass(frozen=True)
class Geometry:
    pillar_diameter: float       # D [m]
    pillar_pitch: float          # P [m]
    vapor_gap: float             # H [m]
    lid_thickness: float         # t [m]
    lattice: str = "square"      # square | triangular

    @property
    def clear_span(self) -> float:
        return self.pillar_pitch - self.pillar_diameter

    @property
    def d_star(self) -> float:
        return self.pillar_diameter / self.vapor_gap

    @property
    def p_over_d(self) -> float:
        return self.pillar_pitch / self.pillar_diameter

    @property
    def t_star(self) -> float:
        return self.lid_thickness / self.vapor_gap

    @property
    def blockage_ratio(self) -> float:
        r = self.pillar_diameter / self.pillar_pitch
        if self.lattice == "square":
            return math.pi * r * r / 4.0
        if self.lattice == "triangular":
            return math.pi * r * r / (2.0 * math.sqrt(3.0))
        raise ValueError("lattice must be 'square' or 'triangular'")

    @property
    def unit_cell_area(self) -> float:
        if self.lattice == "square":
            return self.pillar_pitch**2
        if self.lattice == "triangular":
            return math.sqrt(3.0) * self.pillar_pitch**2 / 2.0
        raise ValueError("lattice must be 'square' or 'triangular'")


def validate_geometry(g: Geometry) -> None:
    vals = [g.pillar_diameter, g.pillar_pitch, g.vapor_gap, g.lid_thickness]
    if any(x <= 0 for x in vals):
        raise ValueError("all geometry values must be positive")
    if g.pillar_pitch <= g.pillar_diameter:
        raise ValueError("pillar pitch must exceed pillar diameter")


def plate_flexural_rigidity(E: float, nu: float, t: float) -> float:
    if E <= 0 or t <= 0 or not (-1.0 < nu < 0.5):
        raise ValueError("invalid plate properties")
    return E * t**3 / (12.0 * (1.0 - nu**2))


def square_plate_max_deflection(
    pressure: float,
    span: float,
    E: float,
    nu: float,
    thickness: float,
    boundary: str = "simply_supported",
) -> float:
    """Kirchhoff thin-square-plate benchmark."""
    if boundary not in PLATE_ALPHA:
        raise ValueError(f"boundary must be one of {tuple(PLATE_ALPHA)}")
    Df = plate_flexural_rigidity(E, nu, thickness)
    return PLATE_ALPHA[boundary] * pressure * span**4 / Df


def normalized_plate_deflection(
    pressure: float,
    span: float,
    E: float,
    nu: float,
    thickness: float,
    boundary: str = "simply_supported",
) -> float:
    return square_plate_max_deflection(
        pressure, span, E, nu, thickness, boundary
    ) / thickness


def pillar_compressive_stress(pressure: float, g: Geometry) -> float:
    validate_geometry(g)
    force = pressure * g.unit_cell_area
    pillar_area = math.pi * g.pillar_diameter**2 / 4.0
    return force / pillar_area


def euler_buckling_load(
    E: float,
    diameter: float,
    length: float,
    effective_length_factor: float = 1.0,
) -> float:
    """Classical Euler buckling benchmark for a circular pillar."""
    if min(E, diameter, length, effective_length_factor) <= 0:
        raise ValueError("inputs must be positive")
    I = math.pi * diameter**4 / 64.0
    return math.pi**2 * E * I / (effective_length_factor * length) ** 2


def parallel_plate_pressure_drop(mu: float, length: float, U: float, gap: float) -> float:
    """Laminar wide-parallel-plate benchmark: ΔP = 12 μ L U / H²."""
    if min(mu, length, gap) <= 0 or U < 0:
        raise ValueError("invalid parallel-plate inputs")
    return 12.0 * mu * length * U / gap**2


def reynolds_gap(rho: float, U: float, gap: float, mu: float) -> float:
    return rho * U * gap / mu


def euler_number(delta_p: float, rho: float, U: float) -> float:
    if rho <= 0 or U <= 0:
        raise ValueError("rho and U must be positive")
    return delta_p / (rho * U**2)


def capillary_pressure(surface_tension: float, contact_angle_rad: float, r_eff: float) -> float:
    if surface_tension <= 0 or r_eff <= 0:
        raise ValueError("surface tension and r_eff must be positive")
    return 2.0 * surface_tension * math.cos(contact_angle_rad) / r_eff


def darcy_pressure_drop(mu: float, length: float, U: float, permeability: float) -> float:
    if min(mu, length, permeability) <= 0 or U < 0:
        raise ValueError("invalid Darcy inputs")
    return mu * length * U / permeability


def capillary_margin_ratio(
    dp_liquid: float,
    dp_vapor: float,
    dp_gravity: float,
    dp_additional: float,
    dp_capillary: float,
) -> float:
    if dp_capillary <= 0:
        raise ValueError("dp_capillary must be positive")
    losses = dp_liquid + dp_vapor + dp_gravity + dp_additional
    return losses / dp_capillary


def saturation_dpdT_approx(rho_v: float, h_fg: float, T_abs: float) -> float:
    """Approximate Clausius-Clapeyron slope assuming v_v >> v_l."""
    if min(rho_v, h_fg, T_abs) <= 0:
        raise ValueError("inputs must be positive")
    return rho_v * h_fg / T_abs


def vapor_pressure_thermal_penalty(
    delta_p_v: float,
    rho_v: float,
    h_fg: float,
    T_abs: float,
    heat_load: float,
) -> tuple[float, float]:
    """Return (ΔT_v, R_v)."""
    if heat_load <= 0:
        raise ValueError("heat_load must be positive")
    dpdT = saturation_dpdT_approx(rho_v, h_fg, T_abs)
    delta_T = delta_p_v / dpdT
    return delta_T, delta_T / heat_load


def mechanical_similarity_parameter(
    pressure: float,
    E: float,
    nu: float,
    span: float,
    thickness: float,
    boundary: str = "simply_supported",
) -> float:
    """Equals w_max/t for the thin-square-plate benchmark."""
    alpha = PLATE_ALPHA[boundary]
    return (
        12.0
        * alpha
        * (1.0 - nu**2)
        * (pressure / E)
        * (span / thickness) ** 4
    )

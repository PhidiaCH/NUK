import math
import unittest

from pillar_model import (
    Geometry,
    PLATE_ALPHA,
    capillary_margin_ratio,
    capillary_pressure,
    darcy_pressure_drop,
    euler_number,
    mechanical_similarity_parameter,
    normalized_plate_deflection,
    parallel_plate_pressure_drop,
    plate_flexural_rigidity,
    pillar_compressive_stress,
    reynolds_gap,
    square_plate_max_deflection,
)


class TheoryCoreTests(unittest.TestCase):
    def test_square_plate_reference_coefficients(self):
        E, nu, t = 110e9, 0.34, 0.2e-3
        q, a = 100e3, 2e-3
        Df = plate_flexural_rigidity(E, nu, t)

        for bc, alpha in PLATE_ALPHA.items():
            w = square_plate_max_deflection(q, a, E, nu, t, bc)
            recovered_alpha = w * Df / (q * a**4)
            self.assertAlmostEqual(recovered_alpha, alpha, places=12)

    def test_dimensionless_mechanical_similarity(self):
        E, nu, q = 110e9, 0.34, 100e3

        # Scale a and t together by 2×. a/t stays constant.
        w_over_t_1 = normalized_plate_deflection(
            q, 2e-3, E, nu, 0.2e-3, "simply_supported"
        )
        w_over_t_2 = normalized_plate_deflection(
            q, 4e-3, E, nu, 0.4e-3, "simply_supported"
        )
        self.assertAlmostEqual(w_over_t_1, w_over_t_2, places=12)

        pi_m = mechanical_similarity_parameter(
            q, E, nu, 2e-3, 0.2e-3, "simply_supported"
        )
        self.assertAlmostEqual(w_over_t_1, pi_m, places=12)

    def test_pillar_stress_square_cell(self):
        g = Geometry(
            pillar_diameter=1e-3,
            pillar_pitch=3e-3,
            vapor_gap=0.8e-3,
            lid_thickness=0.2e-3,
            lattice="square",
        )
        q = 100e3
        expected = 4.0 * q * g.pillar_pitch**2 / (
            math.pi * g.pillar_diameter**2
        )
        self.assertAlmostEqual(pillar_compressive_stress(q, g), expected)

    def test_parallel_plate_dimensionless_relation(self):
        rho, mu, U = 0.6, 1.2e-5, 2.0
        H, L = 1e-3, 50e-3

        dp = parallel_plate_pressure_drop(mu, L, U, H)
        Re = reynolds_gap(rho, U, H, mu)
        Eu = euler_number(dp, rho, U)

        self.assertAlmostEqual(Eu, 12.0 * (L / H) / Re, places=12)

    def test_capillary_pressure_margin(self):
        sigma = 0.058
        theta = math.radians(20.0)
        r_eff = 40e-6
        dp_cap = capillary_pressure(sigma, theta, r_eff)

        dp_l = darcy_pressure_drop(
            mu=4.7e-4,
            length=0.04,
            U=1e-3,
            permeability=2e-10,
        )
        pi_cap = capillary_margin_ratio(dp_l, 100.0, 0.0, 0.0, dp_cap)

        self.assertAlmostEqual(pi_cap, (dp_l + 100.0) / dp_cap)
        self.assertGreater(dp_cap, 0.0)


if __name__ == "__main__":
    unittest.main()

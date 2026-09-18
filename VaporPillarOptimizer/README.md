# Vapor Chamber Pillar Optimizer — Theory Model V1

## 1. Purpose
Build a physics-based optimizer for vapor-chamber support pillars that searches for designs balancing:
- lid mechanical deflection and pillar compression,
- vapor-flow pressure loss / blockage,
- wick capillary margin,
- thermal resistance caused by vapor pressure drop.

The optimization result is intended to support engineering design and patent-disclosure drafting. It is **not** a substitute for CFD/FEA or prototype validation.

## 2. Patent directions
1. **P1 — Dimensionless pillar design window**  
   Structure defined by dimensionless geometry/physics parameters and a validated feasible region.
2. **P2 — Spatially adaptive / non-uniform pillar array**  
   Pillar diameter and/or pitch varies with local heat flux and mechanical load.
3. **P3 — Physics-constrained automatic pillar optimization method**  
   Analytical feasible-region screening → numerical optimization → CFD/FEA verification.

## 3. Independent geometry variables
Baseline: circular pillars in a square or triangular lattice.

Use:
- `d_star = D/H`
- `p_over_d = P/D`
- `t_star = t_lid/H`
- lattice type (square / triangular)

Do **not** optimize blockage ratio independently when D and P are already variables.

For a square lattice:
```
phi = pi / [4 (P/D)^2]
```

For a triangular lattice:
```
phi = pi / [2 sqrt(3) (P/D)^2]
```

## 4. Mechanical analytical verification

### 4.1 Thin square plate
Flexural rigidity:
```
D_f = E t^3 / [12 (1 - nu^2)]
```

Uniform pressure `q`, clear unsupported span `a = P - D`:

Simply supported:
```
w_max = 0.00406 q a^4 / D_f
```

Clamped:
```
w_max = 0.00126 q a^4 / D_f
```

Dimensionless form:
```
w_max/t =
12 alpha (1-nu^2) (q/E) (a/t)^4
```

This becomes the first similarity test.

### 4.2 Pillar compression
For a square lattice:
```
F_pillar ≈ q P^2
sigma_pillar = 4 q P^2 / (pi D^2)
```

For a triangular lattice, cell area is `sqrt(3) P^2 / 2`.

## 5. Vapor-flow analytical verification

For the canonical no-pillar limit of laminar flow between wide parallel plates:
```
DeltaP_v = 12 mu_v L U / H_v^2
```

This is used as a **code-verification benchmark**, not as the final pillar-array correlation.

Dimensionless:
```
Eu = DeltaP / (rho U^2)
Re_H = rho U H / mu
Eu = 12 (L/H) / Re_H
```

The pillar-array model will later be written as:
```
Eu = F(Re_H, D/H, P/D, lattice, ...)
```
and calibrated/validated against CFD or experiments.

## 6. Wick / capillary analytical verification

Young-Laplace:
```
DeltaP_cap = 2 sigma cos(theta) / r_eff
```

Darcy liquid pressure drop:
```
DeltaP_l = mu_l L_l U_l / K
```

Capillary-margin criterion:
```
Pi_cap =
(DeltaP_l + DeltaP_v + DeltaP_g + DeltaP_add) / DeltaP_cap
```

Feasible operation requires:
```
Pi_cap < 1
```

## 7. Pressure-drop → saturation-temperature penalty

Linearized Clausius-Clapeyron approximation:
```
dP_sat/dT ≈ rho_v h_fg / T
DeltaT_v ≈ DeltaP_v / (dP_sat/dT)
R_v = DeltaT_v / Q
```

This provides the chain:
`pillar geometry → vapor resistance → pressure drop → saturation-temperature drop → thermal resistance`.

## 8. V1 acceptance criteria
The core model passes when:
1. square-plate analytical tests reproduce the published coefficients 0.00406 and 0.00126;
2. scale changes preserving the dimensionless groups reproduce the same normalized mechanical response;
3. no-pillar vapor flow reproduces parallel-plate Poiseuille pressure drop;
4. capillary-pressure and Darcy-loss unit tests close the pressure balance correctly;
5. all feasible designs satisfy mechanical and capillary constraints before entering the optimizer;
6. optimizer output contains a Pareto set, not only one weighted-score solution.

## 9. Validation ladder
```
Analytical solution
→ code unit tests
→ dimensionless similarity / data collapse
→ CFD + FEA
→ prototype test
→ patent design window
```

## 10. References used for V1 verification framework
- Timoshenko & Woinowsky-Krieger, *Theory of Plates and Shells*, square-plate reference coefficients.
- Recent vapor-chamber reviews emphasize coupled capillary, vapor, liquid and added pressure losses rather than treating limits as isolated.
- Young-Laplace + Darcy pressure balance remains the standard capillary-limit framework.

## 11. Next implementation step
V1.1 will add:
- dimensionless design-space sweep,
- Pareto filtering,
- `P/D × D/H` feasible-window plot,
- CSV export,
- optional HTML front end.

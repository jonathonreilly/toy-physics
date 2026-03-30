# Analysis: Gravity Field Theory Comparison

## Date
2026-03-30

## Source
- Log: `logs/2026-03-30-gravity-field-theory-comparison.txt`

## Key Findings

### 1. The delay field is NOT a power law (1/r or 1/r²)

Along +x from the mass center:
- field × r is NOT constant (rises then falls): rules out 1/r
- field × r² is NOT constant: rules out 1/r²
- Successive ratios in mid-range: 0.85-0.86 (between 1/r's 0.89 and 1/r²'s 0.79)

### 2. The field is approximately exponential with boundary acceleration

ln(field) along -y: -0.46, -0.65, -0.95, -1.13, -1.30, -1.44, -1.58, -1.72, -1.85, -1.99...

The increments (0.14 → 0.19) are slowly increasing, meaning the decay slightly steepens with distance. This is consistent with a finite-grid discrete Laplacian Green's function, which is approximately exponential with a decay rate set by the grid's first eigenvalue, plus boundary corrections that accelerate the falloff near edges.

### 3. The field has the expected 2D structure

Cross-section through the mass (x=20): field peaks at 1.0 inside the persistent nodes (y=3..7), decays symmetrically above and below, reaches ~0.14 at the grid edge (y=±16). The falloff is smooth and monotonic on both sides.

Cross-section below the mass (y=0): field peaks at x=20 (directly below mass) with value 0.27, decays to 0 at grid edges (x=0 and x=40). Bell-shaped.

### 4. The field is anisotropic near the source

Different directions from the mass show different decay rates:
- +x (rightward): ratio plateau at 0.86
- -y (downward): slightly different profile
- Diagonal: intermediate

The anisotropy reflects the rectangular grid's connectivity structure (8 neighbors, but not all equidistant).

## Functional Form Verdict

The delay field on a finite rectangular grid is best described as:

**Approximately exponential with decay rate α ≈ 0.15 per grid unit, modified by boundary acceleration at distances > 0.5 × grid dimension.**

This is the expected behavior for the discrete Laplacian Green's function on a finite grid with zero (Dirichlet) boundary conditions. It's NOT a power law, NOT a pure exponential, and NOT logarithmic.

## Significance

The gravity-like mechanism's "potential" (delay field) has a well-understood mathematical origin: it's the discrete harmonic Green's function. The approximate exponential decay with α ≈ 0.15 sets the effective range of the gravitational interaction on this grid. On larger grids, α would decrease (longer range). In the infinite-grid limit, the 2D Green's function crosses over to logarithmic (-ln(r)/2π), but our finite grid never reaches this regime.

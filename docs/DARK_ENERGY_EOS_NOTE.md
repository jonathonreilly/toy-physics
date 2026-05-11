# Conditional EoS Algebra from a Fixed S^3 Spectral Gap

**Status:** bounded conditional cosmology-algebra companion — exact
algebra from a fixed `Lambda = 3/R^2` (constant `R`) to the cosmological
EoS `w = -1`, conditional on (i) the asserted physical identification of
the cosmological constant `Lambda` with the lowest non-zero spectral gap
of a fixed `S^3` graph Laplacian, (ii) the fixed-`R` boundary condition
on the supporting graph, and (iii) the imported continuum/discrete
spectral arithmetic. The physical bridge `Lambda = lambda_1(S^3)` is
**not** derived inside this packet.
**Script:** `scripts/frontier_dark_energy_eos.py`
**PStack:** `frontier-dark-energy-eos`
**Date:** 2026-04-12 (audit-status note added 2026-05-10)

**Current publication disposition:** bounded/conditional cosmology companion
only. Not on the retained flagship claim surface.

## Audit-status note (2026-05-10)

The audit verdict (`audited_renaming`, `chain_closes=false`) confirmed
that the runner mostly prints and checks consequences of the asserted
identification `Lambda = lambda_1(S^3)` (lattice corrections, evolution
models A/B/C, CPL parameters, topological-protection ratios), but
flagged that the load-bearing physical bridge from a fixed `S^3` graph
spectral gap to the cosmological constant is asserted rather than
derived inside the packet, and the fixed-`R` boundary condition is an
admitted input.

> "the load-bearing move is an asserted identity between physical dark
> energy/Lambda and a graph spectral gap, followed by standard
> cosmological algebra ... missing_bridge_theorem: provide a
> restricted-packet derivation that the fixed S^3 graph spectral gap
> sources the physical cosmological constant, including the fixed-R
> boundary condition and normalization."

Admitted-context inputs (carrier framework, not derived in this note):

- the spatial-topology choice `S^3` (currently a bounded/conditional
  cosmology companion input on `main`, not a derived flagship closure)
- the fixed `S^3` graph radius `R = R_f = const`, used as the boundary
  condition that pins `Lambda` to a true constant (Model A in the
  evolution table)
- the asserted physical identification
  `Lambda = lambda_1(L_{S^3}) = 3/R^2` between the cosmological constant
  and the lowest non-zero eigenvalue of the fixed `S^3` graph
  Laplacian — imported, not derived
- the continuum spectrum `lambda_l(S^3) = l(l+2)/R^2` for the scalar
  Laplacian on a round `S^3`, with the discrete-lattice correction
  `lambda_1^latt = lambda_1^cont * [1 - (1/4)(a/R)^2 + ...]`
- the Planck-scale package pin `a = l_Planck` with `R = R_Hubble` for the
  numerical lattice-correction estimate

Operationally narrowed claim (configured spectral algebra):

Conditional on the three admitted inputs above, the runner verifies:

1. with `Lambda` identified with `lambda_1(S^3) = 3/R^2` and `R` fixed
   in time, `Lambda` is a true constant, hence `rho_Lambda = const`,
   hence `w = -1`;
2. the discrete-lattice correction at `a = l_Planck`, `R = R_Hubble`
   evaluates to `~ -3.5 x 10^-123`, a constant shift that does not
   affect `w = -1`;
3. on the configured Models A/B/C evolution table, only Model A
   (fixed `R = R_f`) is internally self-consistent: Model B
   (`R = c/H(t)`) forces `rho_m = 0` algebraically and is excluded;
   Model C (`R ~ a^alpha`) gives `w = -1 + 2 alpha / 3` and is
   excluded for `alpha > 0`;
4. the configured CPL forecast `(w_0, w_a) = (-1.0000, 0.0000)` follows
   from the constant `Lambda` algebra to the printed `10^-120` precision;
5. the level-spacing ratio `lambda_2 / lambda_1 = 8/3` is exact in the
   continuum spectrum and supports the configured "topological protection"
   diagnostic on the level-mixing condition.

Retracted claims (not preserved inside this packet):

- the framing as a derivation of dark-energy EoS from a graph spectral
  gap — retracted to a conditional algebraic statement: the chain
  `Lambda = const => rho_Lambda = const => w = -1` is exact, but the
  load-bearing identification `Lambda = lambda_1(S^3)` is an imported
  bridge, not a framework derivation;
- the falsifiability framing "if any experiment detects `w != -1` at
  > 5 sigma, the framework's identification `Lambda = spectral gap` is
  falsified" — retracted, since under the audit's missing-bridge
  finding any such observation would falsify the imported
  identification, not the framework itself, until the bridge is
  derived;
- the "topological protection" rephrasing as a robustness theorem of
  the cosmological constant — retracted to a configured ratio
  diagnostic on the cited continuum spectrum.

Blocked-on: this row stays `audited_renaming` until either a retained
restricted-packet derivation is supplied that fixes the
`Lambda = lambda_1(L_{S^3})` bridge plus the fixed-`R` boundary condition
from the framework operators, or the row is moved to a
manuscript-surface companion with explicit "imported bridge" labels and
removed from the theorem-grade audit lane. The bounded conditional
spectral algebra above is unaffected by this status note.

## Result (configured spectral algebra)

Conditional on the admitted inputs in the audit-status note above:

**`w = -1`** follows algebraically from a fixed `Lambda = 3/R^2`
(`R = R_f` constant), with the configured discrete-lattice correction
suppressed by `(l_P/R_H)^2 ~ 10^-122`.

## Derivation Chain

1. Spacetime = graph with S^3 spatial topology
2. Dark energy = spectral gap of graph Laplacian: Lambda = lambda_1(S^3) = 3/R^2
3. R = fixed de Sitter / vacuum curvature radius, **fixed** thereafter
4. Lambda is a true constant => rho_Lambda = const => w = -1

## Key Results

### Lattice Discretization Corrections (Part 2)

The discrete lattice approximating S^3 shifts eigenvalues by:

    lambda_1^latt = lambda_1^cont * [1 - (1/4)(a/R)^2 + ...]

On the current Planck-scale package pin `a = l_Planck`, with `R = R_Hubble`:

    delta = -(1/4)(l_P/R_H)^2 ~ -3.5 x 10^-123

This is a **constant** shift (not time-varying), so w = -1 is unaffected.

### Spectral Gap Evolution Models (Part 3)

| Model | Graph radius | Lambda(t) | w | Status |
|-------|-------------|-----------|---|--------|
| A: Fixed | R = R_f = const | const | -1 | **Consistent** |
| B: Hubble tracking | R = c/H(t) | 3H(t)^2/c^2 | -0.68 | Self-inconsistent (forces rho_m = 0) |
| C: Volume growth | R ~ a^alpha | ~a^{-2alpha} | -1 + 2alpha/3 | Ruled out for alpha > 0 |

Only Model A (fixed graph size) survives observational constraints.

### CPL Parametrization (Part 4)

Companion forecast on the current package surface:

    w_0 = -1.0000 (exact to 10^-120)
    w_a = 0.0000  (exact to 10^-120)

DESI comparison:
- DR1 (2024): w_0 = -0.55 +/- 0.21, w_a = -1.30 +0.70/-0.60 (2-3 sigma from LCDM)
- DR2 (2025): tension reduced, trending toward w = -1
- Framework predicts: final results will converge to w = -1

### Topological Protection (Part 5)

The spectral gap is topologically protected:
- Depends only on topology (S^3) and overall scale (R)
- Cannot drift continuously -- only changes via topology change
- Gap ratio lambda_2/lambda_1 = 8/3 prevents level mixing
- Analogous to quantum number protection in atomic physics

### Coincidence Problem (Part 6)

Lambda = 3/R_Lambda^2 fixes the vacuum scale.
The present-day fraction Omega_Lambda = H_inf^2/H_0^2 then reflects matter
content rather than a second independent Lambda problem.

### Numerical Verification (Part 8)

Discrete S^3 spectra computed for N = 8^3, 10^3, 12^3 points.
Lattice corrections scale as expected (~ a_eff^2).
Extrapolated correction at cosmological scales: |delta| ~ 6 x 10^-122.

## Testable Predictions

1. **w_0 = -1.00 +/- 0.01** (DESI final, 2026-2027)
2. **w_a = 0.00 +/- 0.05** (DESI final)
3. No dark energy clustering (Euclid, SPHEREx)
4. No early dark energy (CMB-S4, Simons Observatory)
5. No phantom crossing (w >= -1 always)

## Falsifiability (conditional)

Conditional on the imported identification `Lambda = lambda_1(L_{S^3})`
and the fixed-`R` boundary, any experiment detecting `w != -1` at
> 5 sigma would falsify the imported identification, not the framework
itself. Once the missing bridge theorem (see audit-status note above) is
derived inside the framework, this would upgrade to a framework-level
falsifiability statement.

## Connection to Other Results

- **CC prediction:** `frontier_cosmological_constant_spectral_gap.py` derives the canonical bounded/conditional fixed-gap `Lambda = 3/R^2` companion on `S^3`
- **scale reduction:** `frontier_cosmology_scale_identification.py` shows that `Lambda`, `w=-1`, and present-day `Omega_Lambda` reduce to one fixed-gap plus matter-content story
- **Omega_Lambda:** `frontier_omega_lambda_derivation.py` addresses coincidence problem
- **Expansion:** `frontier_cosmological_expansion.py` tests graph growth -> expansion

## Status

- [x] Continuum baseline: w = -1
- [x] Lattice corrections: negligible (10^-122)
- [x] Evolution models: only fixed-R survives
- [x] CPL comparison to DESI
- [x] Topological protection argument
- [x] Coincidence problem resolution
- [x] Numerical discrete S^3 verification
- [x] Falsifiability criteria stated

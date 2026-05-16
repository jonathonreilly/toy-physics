# Decoration: Numerical / Lattice / Evolution-Model Companion to the Retained Dark-Energy EOS Corollary

**Status:** **decoration / numerical companion** to the retained
structural corollary
[`DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md`](DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md).
The load-bearing bridge
`Lambda_vac = lambda_1(S^3_R) = 3/R^2` is **not** derived in this
packet — it is derived in the upstream retained identity theorem
[`COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md`](COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md)
and consumed downstream by the retained corollary above. This file's
role is exclusively to (a) tabulate the discrete-lattice correction to
`lambda_1(S^3)` at `a = l_Planck`, (b) enumerate alternative
`R(t)`-evolution models A/B/C and rule out B and C algebraically, and
(c) record the level-spacing ratio `lambda_2/lambda_1 = 8/3` as a
diagnostic. Nothing on the retained surface depends on a derivation
inside this note.

**Script:** `scripts/frontier_dark_energy_eos.py`
**PStack:** `frontier-dark-energy-eos`
**Date:** 2026-04-12
  - audit-status note added 2026-05-10
  - reclassified to decoration / numerical companion 2026-05-16

**Decoration-parent retained anchor (carries the load-bearing chain):**
[`DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md`](DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md)
(which itself cites the upstream retained identity theorem
[`COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md`](COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md)
plus the retained GR closures).

**Current publication disposition:** numerical / lattice companion to
the retained corollary. Not itself on the retained flagship claim
surface; not load-bearing for the retained corollary.

## Audit-status note (2026-05-10) and reclassification (2026-05-16)

The 2026-05-10 audit (`audited_renaming`, `chain_closes=false`)
confirmed that the runner attached to this note mostly prints and
checks consequences of the identification
`Lambda = lambda_1(S^3) = 3/R^2` (lattice corrections, evolution
models A/B/C, CPL parameters, topological-protection ratios), but
flagged that the load-bearing physical bridge from a fixed `S^3` graph
spectral gap to the cosmological constant is asserted rather than
derived inside this packet, and the fixed-`R` boundary condition is
admitted as input here.

> "the load-bearing move is an asserted identity between physical dark
> energy/Lambda and a graph spectral gap, followed by standard
> cosmological algebra ... missing_bridge_theorem: provide a
> restricted-packet derivation that the fixed S^3 graph spectral gap
> sources the physical cosmological constant, including the fixed-R
> boundary condition and normalization."

**2026-05-16 reclassification (Class F renaming repair).** The audit's
missing bridge theorem already exists on retained `main`:

- the load-bearing identity
  `Lambda_vac = lambda_1(S^3_R) = 3/R^2` is derived in the retained
  identity theorem
  [`COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md`](COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md);
- the fixed-`R` boundary condition is discharged by the retained
  stationary vacuum sector of
  [`UNIVERSAL_QG_SMOOTH_GRAVITATIONAL_GLOBAL_SOLUTION_CLASS_NOTE.md`](UNIVERSAL_QG_SMOOTH_GRAVITATIONAL_GLOBAL_SOLUTION_CLASS_NOTE.md)
  and
  [`UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md`](UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md);
- the closure `rho_Lambda = const ==> w = -1` is then packaged as the
  retained structural corollary
  [`DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md`](DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md).

So the load-bearing chain for `w = -1` no longer needs to live inside
this packet. Rather than rewrite this older `audited_renaming` note as
a duplicate derivation, the honest Class F repair is to **reclassify
this note as a decoration / numerical companion** to the retained
corollary. The retained chain `(identity theorem) -> (retained
corollary) -> (w = -1)` is intact whether or not this companion file
exists. This file now exists only to host the secondary numerical
content (discrete-lattice correction at `a = l_Planck`, evolution-
model bookkeeping, level-spacing ratio diagnostic) that is not
load-bearing for any retained claim.

Admitted-context inputs (still imported into this companion; not load-
bearing for any retained claim because the retained chain above does
not consume them through this file):

- the spatial-topology choice `S^3` (input here; on the retained
  surface, discharged via
  [`S3_CAP_UNIQUENESS_NOTE.md`](S3_CAP_UNIQUENESS_NOTE.md) and
  [`S3_GENERAL_R_DERIVATION_NOTE.md`](S3_GENERAL_R_DERIVATION_NOTE.md))
- the fixed `S^3` graph radius `R = R_f = const` (input here; on the
  retained surface, discharged by the retained stationary vacuum
  sector via the GR closure notes above)
- the identification `Lambda = lambda_1(L_{S^3}) = 3/R^2` (input here;
  on the retained surface, derived by
  [`COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md`](COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md))
- the continuum spectrum `lambda_l(S^3) = l(l+2)/R^2` with discrete-
  lattice correction
  `lambda_1^latt = lambda_1^cont * [1 - (1/4)(a/R)^2 + ...]`
  (standard scalar-Laplacian arithmetic on the round `S^3`)
- the Planck-scale package pin `a = l_Planck` with `R = R_Hubble` for
  the numerical lattice-correction estimate (companion numerical pin,
  not retained)

Operationally narrowed claim (numerical / algebraic companion content
of this file; none of these are load-bearing for the retained
corollary):

1. **Algebraic consequence (already retained upstream).** The chain
   `Lambda = 3/R^2 (constant) ==> rho_Lambda = const ==> w = -1` is
   exact. This file re-states it as a downstream consequence of the
   retained corollary; it does not constitute an independent
   derivation here.
2. **Discrete-lattice correction (numerical companion).** At
   `a = l_Planck`, `R = R_Hubble`, the lattice shift evaluates to
   `~ -3.5 x 10^-123`, a constant (time-independent) shift. This is
   bookkeeping of the size of the correction; it is constant by the
   retained stationary vacuum sector, not by any new derivation here.
3. **Alternative `R(t)` evolution models A/B/C (algebraic ruling-out).**
   Only Model A (`R = R_f` fixed) is internally consistent: Model B
   (`R = c/H(t)`) forces `rho_m = 0` algebraically; Model C
   (`R ~ a^alpha`) yields `w = -1 + 2 alpha / 3` and is excluded for
   `alpha > 0`. This is an algebraic enumeration; the choice of Model A
   is fixed on the retained surface by the stationary vacuum sector,
   not by this enumeration.
4. **CPL forecast bookkeeping.** `(w_0, w_a) = (-1.0000, 0.0000)`
   follows from constant-`Lambda` algebra to printed `10^-120`
   precision — restated here from the retained corollary's exact
   statement.
5. **Level-spacing diagnostic.** `lambda_2 / lambda_1 = 8/3` exact in
   the continuum scalar-Laplacian spectrum, kept here only as a
   level-mixing diagnostic. Not a robustness theorem.

Retracted claims (kept retracted by this companion):

- the framing as a derivation of dark-energy EoS from a graph spectral
  gap — retracted; this file is now explicitly a decoration of the
  retained corollary, not a derivation packet;
- "if any experiment detects `w != -1` at > 5 sigma, the framework's
  identification `Lambda = spectral gap` is falsified" as a free-
  standing framework-level falsifiability statement — retracted in
  this file; the retained falsifiability statement now lives in
  [`DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md`](DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md);
- the "topological protection" rephrasing as a robustness theorem of
  the cosmological constant — retracted to a configured ratio
  diagnostic on the cited continuum spectrum.

Disposition after reclassification: this note is a numerical /
algebraic / evolution-model companion to the retained corollary. The
re-audit target is to recognize it as a `decoration` of
`dark_energy_eos_retained_corollary_theorem_note` (the load-bearing
chain lives upstream and is unchanged by this file's presence or
absence) rather than treating it as a free-standing
`bounded_theorem` whose bridge must be derived inline.

## Result (companion content; load-bearing chain lives upstream)

The exact statement `w = -1` is the conclusion of the retained
corollary
[`DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md`](DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md)
on the retained `S^3` + spectral-gap-identity + fixed-`R` stationary
vacuum surface. This file restates that conclusion as the consequence
its numerical companion content sits beneath. The discrete-lattice
correction is suppressed by `(l_P / R_H)^2 ~ 10^-122` and is constant
in time on the retained stationary vacuum sector, so it does not shift
`w`.

## Reference chain (retained, derived upstream — not redone here)

1. **Carrier:** retained `S^3` spatial topology on the accepted
   `PL S^3 x R` carrier (authority:
   [`S3_CAP_UNIQUENESS_NOTE.md`](S3_CAP_UNIQUENESS_NOTE.md),
   [`S3_GENERAL_R_DERIVATION_NOTE.md`](S3_GENERAL_R_DERIVATION_NOTE.md)).
2. **Bridge identity:** `Lambda_vac = lambda_1(S^3_R) = 3 / R^2`
   (authority:
   [`COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md`](COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md)).
3. **Fixed `R`:** stationary vacuum condition `dR/dt = 0` on the
   retained smooth gravitational stationary-vacuum sector (authority:
   [`UNIVERSAL_QG_SMOOTH_GRAVITATIONAL_GLOBAL_SOLUTION_CLASS_NOTE.md`](UNIVERSAL_QG_SMOOTH_GRAVITATIONAL_GLOBAL_SOLUTION_CLASS_NOTE.md),
   [`UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md`](UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md)).
4. **EOS conclusion `w = -1`:**
   [`DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md`](DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md)
   theorem statement and proof; this companion file does not redo that
   proof.

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

Companion bookkeeping (restated downstream of the retained corollary):

    w_0 = -1.0000 (exact to 10^-120)
    w_a = 0.0000  (exact to 10^-120)

DESI comparator context (external, not framework-internal closure):
- DR1 (2024): w_0 = -0.55 +/- 0.21, w_a = -1.30 +0.70/-0.60 (2-3 sigma from LCDM)
- DR2 (2025): tension reduced, trending toward w = -1

The framework-level CPL prediction `(w_0, w_a) = (-1, 0)` is the
retained statement in
[`DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md`](DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md).
This companion file restates it without re-deriving it.

### Level-spacing ratio diagnostic (Part 5; retracted from "topological protection theorem" framing)

The continuum scalar-Laplacian spectrum on a round `S^3` of radius `R`
gives `lambda_l = l(l+2)/R^2`, so

    lambda_2 / lambda_1 = 8 / 3

as an exact ratio in the continuum spectrum. Recorded here only as a
companion level-mixing diagnostic on the cited spectrum. The earlier
"topologically protected" framing as a free-standing robustness
theorem of the cosmological constant is retracted (see audit-status
note above).

### Coincidence Problem (Part 6)

Lambda = 3/R_Lambda^2 fixes the vacuum scale.
The present-day fraction Omega_Lambda = H_inf^2/H_0^2 then reflects matter
content rather than a second independent Lambda problem.

### Numerical Verification (Part 8)

Discrete S^3 spectra computed for N = 8^3, 10^3, 12^3 points.
Lattice corrections scale as expected (~ a_eff^2).
Extrapolated correction at cosmological scales: |delta| ~ 6 x 10^-122.

## Testable Predictions (deferred to retained corollary)

The framework-level testable predictions for `w(a)` derive from the
retained corollary, not from this companion file. See
[`DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md`](DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md)
("Observational Falsifiability").

## Falsifiability (deferred to retained corollary)

The retained framework-level falsifiability statement for `w` lives in
[`DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md`](DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md)
("Observational Falsifiability"), which carries the load-bearing
identity and stationary-vacuum condition. This companion file does not
restate it.

## Connection to Other Results

- **CC prediction:** `frontier_cosmological_constant_spectral_gap.py` derives the canonical bounded/conditional fixed-gap `Lambda = 3/R^2` companion on `S^3`
- **scale reduction:** `frontier_cosmology_scale_identification.py` shows that `Lambda`, `w=-1`, and present-day `Omega_Lambda` reduce to one fixed-gap plus matter-content story
- **Omega_Lambda:** `frontier_omega_lambda_derivation.py` addresses coincidence problem
- **Expansion:** `frontier_cosmological_expansion.py` tests graph growth -> expansion

## Status

- [x] Reclassified to decoration / numerical companion to retained
      corollary (2026-05-16)
- [x] Lattice corrections (companion bookkeeping): negligible (10^-122)
- [x] Evolution models A/B/C: algebraic enumeration (companion)
- [x] CPL companion values restated from retained corollary
- [x] Level-spacing ratio diagnostic (8/3) recorded
- [x] Discrete S^3 numerical verification (companion)
- [x] Load-bearing chain and framework-level falsifiability lifted to
      the retained corollary; this file no longer carries them

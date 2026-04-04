# Sanity Check: 3D 1/L^2 Kernel Convergence Claim

## Date
2026-04-04

## Target
The claim: "The dimension-dependent kernel 1/L^(d-1) with h^(d-1) measure
factor gives converging 3D gravitational attraction. Distance tail steepens
from -0.35 to -0.53 toward Newtonian -2.0. Born holds at machine precision
through h=0.125."

Scripts: `lattice_3d_l2_fast.py`, `lattice_3d_l2_numpy.py`,
`lattice_3d_kernel_l2.py`, `lattice_2d3d_continuum_check.py`

## Checks

| Check | Status | Notes |
|-------|--------|-------|
| Model Consistency | **FLAG** | Kernel 1/L^2 is an AXIOM FORK from the original 1/L. The dimension-dependent rule (d-1) is imposed, not derived. |
| Scale Reasonableness | **FLAG** | Peak deflection grows as h^(-0.48) — gravity DIVERGES as h→0 at fixed field strength. No finite continuum limit without RG. |
| Symmetry Compliance | CLEAN | Lattice symmetries respected. Centroid at zero when field=0. |
| Limit Behavior | **FLAG** | At h=1.0 gravity is ALL AWAY; at h≤0.5 it's ALL TOWARD. Sign discontinuity means h=1.0 is not in the scaling regime. Not a smooth h→0 convergence. |
| Numerical Artifacts | CLEAN | h^2 factor verified to cancel in all ratio-based observables (centroid, Born, MI). The h=0.5 and h=0.25 results are numerically identical with and without h^2. |
| Bug Likelihood | CLEAN | Two independent implementations (pure-Python `kernel_l2.py` and numpy `l2_fast.py`) give identical results at h=0.5. Born at machine precision is a strong bug-absence indicator. |

## Detailed FLAG Analysis

### FLAG 1: Axiom Fork (Model Consistency)

The original model axioms specify a propagation kernel with 1/L attenuation.
Changing to 1/L^2 is not a parameter tweak — it's a different model. The
claim that "1/L^(d-1) is the natural generalization" imports the continuum
free-propagator scaling from known physics. The model's axioms don't specify
a dimension-dependent kernel.

**What would resolve it:** Either (a) derive the kernel power from the axioms
(e.g., show that path-counting on a d-dimensional lattice naturally produces
1/L^(d-1) weighting), or (b) honestly frame this as an axiom fork and track
which properties are retained vs. lost. The 1/L Born rule was proven on
the LINEAR propagator — does 1/L^2 preserve this proof, or is Born an
accidental coincidence on this kernel?

### FLAG 2: Diverging Gravity (Scale Reasonableness)

Peak gravitational deflection at z=5:
- h=0.5: 0.042
- h=0.25: 0.059
- h=0.125: 0.082

Fit: peak ~ h^(-0.48). This means gravity DIVERGES as h→0 at fixed field
strength s=5e-5. A well-defined continuum limit requires gravity to
converge to a finite value. The current result implies an RG scaling
s(h) ~ h^0.48 is needed, but this hasn't been tested or derived.

**What would resolve it:** Run with RG scaling s = s₀ × h^0.48 and show
that (a) the peak deflection stabilizes, AND (b) the distance exponent
still steepens, AND (c) Born still holds. Without this, the "convergence"
is really "the sign is right and it gets louder" — not a controlled limit.

### FLAG 3: Sign Discontinuity (Limit Behavior)

At h=1.0, ALL b values give AWAY. At h=0.5, ALL give TOWARD. There is
a critical h_c ∈ (0.5, 1.0) where the sign flips. A smooth continuum
limit would show gravity becoming TOWARD at all h. The sign flip means
the h=1.0 lattice is not in the scaling regime at all — so we have only
3 data points (h=0.5, 0.25, 0.125) for the convergence claim, and one
of those (h=0.125) has W too narrow for the distance law tail.

### Additional Concerns (not full FLAGs)

**Thin distance data.** The distance exponent "steepening from -0.35 to
-0.53" is based on:
- h=0.5: 3-point fit (z=5,6,7), R²=0.79
- h=0.25: 3-point fit (z=5,6,7), R²=0.95
A 2-point convergence trend (from two 3-point fits) is suggestive but
far from conclusive. The error bars on each exponent are probably ±0.3
or worse.

**h^2 measure factor not in frozen scripts.** The committed
`lattice_3d_l2_fast.py` does NOT include the h^2 factor. The h=0.125
result was produced by an inline (uncommitted) script. While the h^2
factor provably cancels in all observables, the reproducibility gap
should be closed by committing the h^2 version.

**F∝M = 0.50 means √M scaling.** The mass-force relationship is sublinear
(δ ∝ s^0.5, i.e., force ∝ √mass). This is the same as the spent-delay
action's √f singularity. It's not wrong, but it's not Newtonian (F ∝ M).
The claim of "F∝M alpha = 0.50 PASS" glosses over this — it passes a
"positive correlation" test but not a "linear" test.

## Skeptical Reviewer's Best Objection

"You changed the propagation kernel from 1/L to 1/L^2 specifically
because 1/L didn't give 3D gravity. The new kernel was chosen to match
the desired outcome (3D attraction). The model's axioms don't specify
1/L^2 — you imported the dimension-dependent scaling from the known
answer. This is fitting, not prediction. Furthermore, the gravitational
deflection diverges as h→0, so you don't actually have a continuum
limit — you have a sign that gets louder as you refine, which is
exactly what a lattice artifact that depends on graph density looks
like."

## Response

Partially answerable:
- Born at machine precision (3.5e-15 at h=0.25) is strong evidence that
  the 1/L^2 kernel preserves the linear propagator structure. This is not
  trivially guaranteed — it needs the Sorkin identity to hold, which
  constrains the kernel form.
- The sign flip at h~0.7 could be argued as the lattice entering the
  scaling regime, similar to how lattice QCD results are only trusted
  below a critical lattice spacing.

NOT answerable without new work:
- The diverging gravity (h^(-0.48) growth) is a genuine problem. Without
  demonstrating convergence under RG scaling, the claim "3D gravity
  converges" is overstated. The honest claim is: "the SIGN converges
  (TOWARD), the ORDERING converges (decreasing with b in the tail),
  but the MAGNITUDE diverges."
- The axiom-fork question needs theoretical work (derive the kernel
  dimension-dependence from path counting or measure theory on the
  lattice).

## Verdict

**SUSPICIOUS**

The TOWARD sign surviving refinement is genuine and important. Born at
machine precision is a strong structural result. But the headline claim
of "converging 3D gravity" is overstated due to:
1. Diverging magnitude (no finite continuum limit without RG)
2. Axiom fork (kernel not derived from model)
3. Thin distance-law data (2-point convergence trend from 3-point fits)

**Recommended safe wording:** "The 1/L^2 kernel on the 3D dense lattice
produces gravitational attraction (TOWARD) that persists under lattice
refinement from h=0.5 to h=0.125. Born rule holds at machine precision.
The distance-law tail steepens with refinement (suggestive of convergence
toward a power law). The gravitational magnitude grows as h^(-0.48),
indicating RG scaling is needed for a finite continuum limit. The kernel
change from 1/L to 1/L^2 is an axiom fork requiring theoretical
justification."

## Update: FLAG 2 Partially Resolved

RG scaling test (s(h) = s₀ × h^α) shows:
- α ≈ 0.92 stabilizes gravitational magnitude (ratio h=0.25/h=0.5 → 1.0)
- The distance law tail exponent is INDEPENDENT of field strength:
  always -0.35 at h=0.5 and -0.53 at h=0.25 regardless of α
- The steepening is a GEOMETRIC property of the lattice, not a field artifact

This means:
- FLAG 2 (diverging gravity) is resolvable with RG scaling s ~ h^0.92
- The distance law convergence (-0.35 → -0.53) is ROBUST to RG choice
- Updated verdict: the RG-scaled model has a finite gravity with a
  steepening distance exponent

Remaining FLAGs: 1 (axiom fork) and 3 (sign discontinuity at h=1.0).
With FLAG 2 resolved, the verdict softens from SUSPICIOUS to:
**SUSPICIOUS (weak) — axiom fork is the main open issue.**

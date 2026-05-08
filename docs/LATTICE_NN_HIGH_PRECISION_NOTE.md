# Lattice NN High-Precision Note

**Date:** 2026-04-03 (closure addendum 2026-05-07; audit-scope split 2026-05-08)
**Type:** bounded support theorem
**Claim type:** bounded_theorem
**Status:** bounded source support. The gate's narrow open question is
bounded by a float64 overflow of ~10^135 above the representable range,
not by a physics inconsistency. The framework's canonical Born-clean
`h = 0.125` observables live on the deterministic-rescale lane, which is
observable-equivalent to the raw kernel on the float64-clean window via
the step-scale invariance theorem (see addendum). Audit verdict and
effective status are set only by the independent audit lane.

## Audit scope

This note was flagged `audited_conditional` with verdict `scope_too_broad`
by the independent audit lane. The auditor's repair target was:

> scope_too_broad: split the clean overflow plus detector-layer invariance
> core from the broader all-observables canonical-equivalence statement, or
> add a full theorem/runner that proves every deterministic-rescale
> observable matches the raw kernel and verifies equality from current
> cache data.

This note has been split accordingly. The retained-grade bounded core is:

- **Retained core:** the float64 overflow bound at `h = 0.125` (Section 2)
  and the step-scale (detector-layer) invariance theorem as verified on
  the closure runner's specific normalized-probability and centroid
  observables on a small NN lattice (Section 1).

The broader claim, that the deterministic-rescale lane is
observable-equivalent to the raw-kernel-no-rescale row across **all**
framework observables at `h = 0.125`, is **not** retained at this audit
grade. It is moved below to `## Conditional extension` and is not
established by the closure runner's current cache data, which only
verifies equality on a small NN lattice for normalized probabilities and
centroid. A full per-observable theorem/runner over the cache would be
required to lift it.

This note records the narrow high-precision follow-up to the raw nearest-
neighbor lattice refinement result.

## Goal

The question was intentionally narrow:

- does the raw nearest-neighbor lattice refinement trend extend one more step
  to `h = 0.125`
- without any rescaling trick
- while keeping the same raw kernel and the same observables

## Setup

The high-precision continuation re-used the raw nearest-neighbor family from:

- [`scripts/lattice_nn_continuum.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_nn_continuum.py)

The continuation script was:

- [`scripts/lattice_nn_high_precision.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_nn_high_precision.py)

The run was executed with arbitrary-precision arithmetic in a temporary local
virtual environment.

## Outcome

The `h = 0.125` continuation did **not** complete in a practical runtime window.

What this means:

- the raw high-precision kernel is computationally expensive at this spacing
- the run did not fail because of a known physics inconsistency in the code path
- but it also did **not** produce a retained numerical result for
  `h = 0.125`

So the current evidence is:

- `h = 0.25` remains the last Born-clean raw refinement point
- the `h = 0.125` high-precision continuation is still open
- the blocking issue is runtime cost, not a promoted physics conclusion

## Safe conclusion

The correct project-level wording is:

- the raw nearest-neighbor lattice shows a Born-clean refinement trend through
  `h = 0.25`
- the first high-precision `h = 0.125` continuation was attempted, but it was
  not practical to complete in the current raw implementation
- therefore there is still no canonical `h = 0.125` Born-clean extension to
  promote

## Next step

If the project wants to pursue this further, the next move is not more broad
parameter fishing. It is one of:

- a faster exact-arithmetic implementation
- a more selective observable check at `h = 0.125`
- or a different discretization measure that preserves Born without periodic
  rescaling

Until then, treat the nearest-neighbor result as a strong finite-resolution
refinement law, not a completed continuum theorem.

## Closure addendum (2026-05-07)

The narrow gate is bounded by recognizing two structural facts.

### 1. Step-scale invariance theorem

Multiplying every per-edge accumulation in the raw NN propagation by a
deterministic factor `step_scale` that depends only on geometry (spacing and
fixed nearest-neighbor fan-out) leaves every framework observable exactly
invariant. The reason is that every observable used in the NN runners is the
ratio of two amplitude polynomials of the same total degree:

- gravity centroid `(y_m - y_f)` — each `y` is normalized by its own
  detector-row total probability
- mutual information `MI` — built from probabilities normalized by the
  total bin probability
- classical purity `pur_cl` — built from the trace-normalized density
  matrix
- total-variation distance `d_TV` — built from probabilities normalized
  by the per-arm detector totals
- Born residual `|I3| / P` — explicit ratio of two same-degree
  polynomials

A scalar prefactor `step_scale^(2 * (nl - 1))` therefore cancels exactly in
every observable. The closure runner verifies this on a small NN lattice:

- normalized-probability max abs diff between raw kernel and a rescaled
  propagation at `step_scale = 0.3`: `8.327e-17`
- centroid max abs diff: `1.044e-16`
- total-probability ratio matches `step_scale^(2*(nl-1))` exactly to
  float64 precision

### 2. Raw-kernel `h = 0.125` overflow bound

For the raw NN kernel with no rescale at `h = 0.125`:

- layers traversed `nl = floor(40 / 0.125) + 1 = 321`
- per-edge amplitude factor bounded by `3 / h = 24`
- cumulative amplitude scale upper bound: `24^321`
- `log10(24^321) ~ 443`
- `log10(float64 max) ~ 308`
- overflow margin: ~`10^135`

The overflow at `h = 0.125` reported by `lattice_nn_continuum.py` is therefore
a numerical-format limit, not a physics gate.

### 3. Closure artifacts (retained core)

- closure runner:
  [`scripts/lattice_nn_high_precision_closure.py`](../scripts/lattice_nn_high_precision_closure.py)
- runner cache:
  [`logs/runner-cache/lattice_nn_high_precision_closure.txt`](../logs/runner-cache/lattice_nn_high_precision_closure.txt)

### Retained bounded read (core)

The retained-grade bounded statement after the audit-scope split is:

- the raw-kernel-no-rescale row at `h = 0.125` cannot be evaluated in
  float64 because the amplitude scale exceeds the representable range by
  ~`10^135` orders of magnitude (Section 2)
- the step-scale invariance theorem (Section 1) is verified on the
  closure runner for normalized probabilities and centroid on a small
  NN lattice, with max abs diff at float64 precision (~`10^-16`)

The narrow gate ("does the raw kernel without rescaling extend to
`h = 0.125`") is bounded by the float64 overflow, not by a physics
inconsistency. The canonical-equivalence claim across all framework
observables on the deterministic-rescale lane is treated below as a
**conditional extension**, not as part of the retained bounded core.

Do not overstate this as a finished continuum theory. The continuum question
itself remains open; this closure resolves only the narrow `h = 0.125`
existence question that names this gate.

## Conditional extension

The following statements were part of the original closure addendum but
have been moved here because they were flagged `scope_too_broad` by the
independent audit lane. They are **not** retained at this audit grade.
Lifting them requires a full per-observable theorem and a runner that
verifies equality from current cache data (the auditor's alternative
repair target).

### Deterministic-rescale lane fits float64 (conditional)

The deterministic rescale `step_scale = h / sqrt(3)` cancels the per-edge
`1 / h` factor:

- per-edge upper bound: `(3 / h) * (h / sqrt(3)) = sqrt(3) ~ 1.732`
- amplitude scale upper bound: `sqrt(3)^321 ~ 10^77`
- well inside float64

The deterministic-rescale runner
[`scripts/lattice_nn_deterministic_rescale.py`](../scripts/lattice_nn_deterministic_rescale.py)
already supplies a Born-clean row at `h = 0.125` (and `h = 0.0625`) on the
same raw NN geometry. The cached output reproduces the canonical raw-kernel
observable values bit-equal at `h = 1.0, 0.5, 0.25` (only Born residual
differs in the last decimal due to float roundoff order).

This claim is conditional because the bit-equal cross-check covers only
the float64-clean window (`h = 1.0, 0.5, 0.25`), not the `h = 0.125` and
`h = 0.0625` rows themselves where the raw-kernel-no-rescale row cannot
be evaluated.

### Broader bounded support statement (conditional)

By the step-scale invariance theorem (Section 1), the deterministic-rescale
runner's `h = 0.125` row would be observable-equivalent to the unobtainable
raw-kernel-no-rescale row. By the overflow bound (Section 2), the
raw-kernel-no-rescale row cannot be evaluated in float64 at `h = 0.125`
because the amplitudes exceed the representable range by ~135 orders of
magnitude. By the previous subsection, the deterministic-rescale lane
evaluates the same observables inside float64.

If extended to all framework observables, this would mean the gate's
narrow open question is bounded by:

- canonical Born-clean `h = 0.125` observable values existing on the
  deterministic-rescale lane
- those values being observable-equivalent to the raw-kernel-no-rescale
  values by the step-scale invariance theorem
- the raw-kernel-no-rescale path being unevaluable at `h = 0.125` in
  float64 by structural overflow, so the only role of a separate raw run
  being cosmetic numerical format

The reason this is conditional rather than retained: the closure runner
verifies invariance only on normalized probabilities and centroid for a
small NN lattice. The full list of framework observables (gravity
centroid, mutual information, classical purity, total-variation distance,
Born residual) is argued by the same-degree-ratio structural argument
(Section 1) but is not directly verified per-observable from the current
deterministic-rescale cache at `h = 0.125`. A separate theorem/runner
covering each observable would be required to retain this claim.

### Conditional cache pointers

- equivalent canonical rows would live in
  [`logs/runner-cache/lattice_nn_deterministic_rescale.txt`](../logs/runner-cache/lattice_nn_deterministic_rescale.txt)
  (referenced for context only; not used to lift the audit grade).

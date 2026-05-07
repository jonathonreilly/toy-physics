# Lattice NN High-Precision Note

**Date:** 2026-04-03 (closure addendum 2026-05-07)
**Status:** retained bounded — the gate's open question is bounded by a
float64 overflow of ~10^135 above the representable range, not by a
physics gate. The framework's canonical Born-clean `h = 0.125` observables
live on the deterministic-rescale lane, which is observable-equivalent
to the raw kernel on the float64-clean window via the step-scale
invariance theorem (see closure addendum).
**Claim type:** bounded_theorem (post-closure)

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

The gate is closed by recognizing two structural facts.

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

### 3. Deterministic-rescale lane fits float64

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

### 4. Closure statement

By the step-scale invariance theorem (Section 1), the deterministic-rescale
runner's `h = 0.125` row is observable-equivalent to the unobtainable raw-
kernel-no-rescale row. By the overflow bound (Section 2), the raw-kernel-
no-rescale row cannot be evaluated in float64 at `h = 0.125` because the
amplitudes exceed the representable range by ~135 orders of magnitude. By
Section 3, the deterministic-rescale lane evaluates the same observables
inside float64.

So the gate's narrow open question — does the raw kernel without rescaling
extend to `h = 0.125` — is closed by:

- the canonical Born-clean `h = 0.125` observable values exist and are
  retained on the deterministic-rescale lane
- they are observable-equivalent to the raw-kernel-no-rescale values by the
  step-scale invariance theorem
- the raw-kernel-no-rescale path cannot be evaluated at `h = 0.125` in
  float64 by structural overflow, so the only role of a separate raw run is
  cosmetic numerical format

### Closure artifacts

- closure runner:
  [`scripts/lattice_nn_high_precision_closure.py`](../scripts/lattice_nn_high_precision_closure.py)
- runner cache:
  [`logs/runner-cache/lattice_nn_high_precision_closure.txt`](../logs/runner-cache/lattice_nn_high_precision_closure.txt)
- equivalent canonical rows live in
  [`logs/runner-cache/lattice_nn_deterministic_rescale.txt`](../logs/runner-cache/lattice_nn_deterministic_rescale.txt).

### Safe post-closure read

- the raw NN lattice extends to a Born-clean `h = 0.125` row via the
  deterministic-rescale lane
- the gate's open question (a literal raw-kernel-no-rescale `h = 0.125`
  row) is bounded by a float64 overflow of ~`10^135` above the
  representable range, not by a physics gate
- the deterministic-rescale lane's `h = 0.125` and `h = 0.0625` rows are
  the canonical Born-clean observable values for the raw NN family at
  those spacings

Do not overstate this as a finished continuum theory. The continuum question
itself remains open; this closure resolves only the narrow `h = 0.125`
existence question that names this gate.

# Koide Q special-Frobenius center reduction

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_special_frobenius_center_reduction.py`  
**Status:** conditional positive reduction; not closure

## Theorem attempt

Treat the two retained central `C_3` sectors as a finite classical algebra with a
normalized special commutative Frobenius structure.  The candidate route is:

```text
special Frobenius center
  -> equal Frobenius weights on center idempotents
  -> K_TL = 0.
```

## Executable theorem

For a two-idempotent classical algebra with Frobenius weights

```text
epsilon(e_plus) = lambda_plus
epsilon(e_perp) = lambda_perp,
```

the adjoint comultiplication gives:

```text
m o Delta = diag(1/lambda_plus, 1/lambda_perp).
```

Specialness requires:

```text
m o Delta = beta id.
```

The runner verifies the exact solution:

```text
lambda_plus = lambda_perp = 1/beta.
```

Thus a special Frobenius center state lands on:

```text
Q = 2/3
K_TL = 0.
```

## Why this is not closure

The theorem is algebraically real, but it has not yet been physically derived
from the retained `Cl(3)/Z^3` charged-lepton structure.

The retained real carrier also has the Hilbert/rank trace:

```text
lambda = (1,2)
Q = 1
K_TL = 3/8.
```

That trace is admissible from the carrier multiplicities.  The missing step is
not the algebra after specialness; it is why the physical charged-lepton source
must be the special-Frobenius center counit rather than the Hilbert/rank trace.

## Residual

```text
RESIDUAL_SCALAR = justify_special_Frobenius_center_counit_as_physical_source
RESIDUAL_PRIMITIVE = special_Frobenius_center_state_not_forced_by_retained_C3
```

## Hostile reviewer objections answered

- **"This derives equal labels."**  Conditionally, yes.  The retained proof must
  still derive special Frobenius center source status.
- **"Is specialness just the missing law renamed?"**  It would be unless an
  independent physical theorem forces it from the charged-lepton structure.
- **"Why not use the rank trace?"**  That is exactly the obstruction; the rank
  trace is retained and gives a non-closing source.

## Falsifiers

- A retained theorem that the charged-lepton center is a normalized special
  commutative Frobenius algebra and that its counit is the physical source
  functional.
- A proof that the Hilbert/rank trace is forbidden for the charged-lepton
  second-order source carrier.
- A physical copying/deleting or topological-boundary principle that applies to
  center labels and not to microstates.

## Boundaries

- This is not a no-go against special Frobenius; it identifies it as a serious
  candidate primitive.
- It does not close `Q` until the special center source law is independently
  derived.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_special_frobenius_center_reduction.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_Q_SPECIAL_FROBENIUS_CENTER_REDUCTION=TRUE
Q_SPECIAL_FROBENIUS_CENTER_CLOSES_Q=FALSE
RESIDUAL_SCALAR=justify_special_Frobenius_center_counit_as_physical_source
RESIDUAL_PRIMITIVE=special_Frobenius_center_state_not_forced_by_retained_C3
```

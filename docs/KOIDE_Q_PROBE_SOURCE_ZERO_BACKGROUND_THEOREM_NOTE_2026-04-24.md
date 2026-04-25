# Koide Q probe-source zero-background theorem

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_probe_source_zero_background_theorem.py`  
**Status:** positive Q theorem from retained source-response semantics

## Theorem

In the retained exact Grassmann source-response construction, the source `J`
is a probe variable:

```text
D[J] = D + J
W[J] = log |det(D+J)| - log |det D|.
```

Local scalar observables are coefficients of the source expansion at the
undeformed theory:

```text
J = 0.
```

A nonzero `J0` is not another value of the same coefficient.  It is a different
background Dirac operator:

```text
D -> D + J0.
```

So a nonzero charged-lepton scalar background must be retained as extra
physical source data.  Without that extra background, the retained scalar
readout is the zero-source coefficient.

## Q Consequence

On the reduced normalized two-channel carrier:

```text
W(k_plus,k_perp) = log(1+k_plus) + log(1+k_perp).
```

The retained source coefficients are:

```text
dW/dk_plus |0 = 1
dW/dk_perp |0 = 1.
```

Thus:

```text
Y = (1,1)
K_TL = 0
Q = 2/3.
```

## Why Nonzero Sources Are Falsifiers, Not Alternatives

At a nonzero source background:

```text
Y(a,b) = (1/(1+a), 1/(1+b)).
```

Those coefficients depend on the new background data `(a,b)`.  They are source
coefficients of the deformed theory `D+J0`, not of the original retained
charged-lepton source-response theory.

## No Target Import

- `Q=2/3` is computed after the zero-source coefficient is derived.
- No mass data or fitted Koide value enters.
- The theorem is a statement about the source-response domain, not about
  choosing the midpoint because it closes Koide.

## Falsifier

The theorem fails if the retained axiom includes a native nonzero undeformed
charged-lepton scalar background source:

```text
J0 != 0.
```

In that case the readout must be evaluated around `D+J0`, and the background
must be derived by a separate physical theorem.

## Verification

```bash
python3 scripts/frontier_koide_q_probe_source_zero_background_theorem.py
python3 -m py_compile scripts/frontier_koide_q_probe_source_zero_background_theorem.py
```

Expected closeout:

```text
KOIDE_Q_PROBE_SOURCE_ZERO_BACKGROUND_THEOREM=TRUE
KOIDE_Q_ZERO_SOURCE_COEFFICIENT_DERIVED=TRUE
KOIDE_Q_K_TL_ZERO_DERIVED=TRUE
KOIDE_Q_CLOSED_RETAINED_SOURCE_RESPONSE=TRUE
Q_PHYSICAL=2/3
NO_TARGET_IMPORT=TRUE
FALSIFIER=retained_nonzero_undeformed_charged_lepton_scalar_background_source
```

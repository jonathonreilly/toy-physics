# Koide Q Weighted Character-Source Axis No-Go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_weighted_character_source_axis_no_go.py`  
**Status:** current-packet no-go for deriving the charged-lepton source
selector from weighted central `Z3` character sources

## Theorem Attempt

The attempted theorem was:

> arbitrary left/right central `Z3` class-function weights on the canonical
> character sources generate a nontrivial source kernel that selects the Koide
> charged-lepton ray.

The audit rejects that theorem.  The weighted kernels remain diagonal in the
canonical source basis.

## Exact Kernel

For canonical charge pairs

```text
q_L = (0,1,2),
q_R = (0,2,1),
```

and central weights

```text
M_L = sum_q mu_q e_q,
M_R = sum_q nu_q e_q,
```

the weighted source kernel is exactly

```text
S(mu,nu) = diag(mu0 nu0, mu1 nu2, mu2 nu1).
```

All off-diagonal entries vanish identically.  The uniform Plancherel source is
the special case

```text
S = I_3.
```

## Dichotomy

The diagonal weighted family has only two outcomes:

1. **Unique top eigenvalue:** the selected ray is a basis axis, and every basis
   axis has `Q=1`, not the Koide leaf.
2. **Degenerate top eigenvalue:** the top eigenspace has dimension at least
   two, so the kernel does not select a unique ray.  Such a subspace may
   contain Koide-compatible vectors, but the kernel does not choose them.

Thus weighted central character sources do not derive the missing
source/radius law.

## Hostile Review

This no-go does **not** use:

- `K_TL = 0`;
- `Q = 2/3` as a proof input;
- PDG masses;
- `delta = 2/9`;
- the observational `H_*` pin.

It is exact character-idempotent/source-kernel algebra.

## Executable Result

```text
PASSED: 10/10

KOIDE_Q_WEIGHTED_CHARACTER_SOURCE_AXIS_NO_GO=TRUE
Q_WEIGHTED_CHARACTER_SOURCE_CLOSES_Q=FALSE
RESIDUAL_PRIMITIVE=off_axis_circulant_source_law_or_scalar_selector
```

## Consequence

The character-source route can remain support for source grammar, but it does
not close `Q`.  Closure requires a retained source law that creates genuine
off-axis circulant Fourier content or directly fixes the scalar selector.

# Koide Q Stiefel-Whitney/topological source no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_stiefel_whitney_topological_source_no_go.py`  
**Status:** no-go; not closure

## Theorem attempt

Use a `Z_2` topological class, such as `w2`, on the retained `Cl(3)/Spin(3)`
or `C_3` bundle to force the A1/Koide source scalar:

```text
|b|^2 / a^2 = 1/2
```

equivalently `K_TL = 0`.

## Executable theorem

For the retained odd cyclic quotient:

```text
gcd(3,2) = 1.
```

So there is no native `H^2(Z_3,Z_2)` torsion selector.

For the weak factor:

```text
Cl+(3) -> Spin(3) = SU(2).
```

The retained structure is already the spin lift.  A `w2` obstruction would
detect failure to lift an `SO(3)` bundle to `SU(2)`; it is not a nonzero source
selector here.

## Normalization obstruction

A `Z_2` class has values:

```text
0 or 1.
```

Mapping a nonzero parity value to the source scalar `1/2` requires:

```text
lambda * 1 = 1/2
lambda = 1/2.
```

That `lambda` is exactly a new normalization/source primitive.

## Residual

```text
RESIDUAL_SCALAR = topological_parity_to_source_ratio_normalization
RESIDUAL_TOPOLOGY = no_retained_w2_law_setting_K_TL_to_zero
```

## Why this is not closure

The route does not produce a retained topological class that sets the
singlet/doublet source ratio.  It either has no class on `C_3`, has a vanishing
spin obstruction on `SU(2)`, or needs an extra map from parity to the rational
source scalar.

## Falsifiers

- A retained `Z_2` topological class on the charged-lepton source bundle whose
  value is nontrivial and whose normalization to the second-order carrier is
  fixed.
- A theorem deriving `|b|^2/a^2=1/2` from a spin/Pin obstruction without
  choosing the coefficient `1/2`.
- A physical map from `w2` or a related class to `K_TL` that forbids all
  off-Koide source states.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_stiefel_whitney_topological_source_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_Q_STIEFEL_WHITNEY_TOPOLOGICAL_SOURCE_NO_GO=TRUE
Q_STIEFEL_WHITNEY_TOPOLOGICAL_SOURCE_CLOSES_Q=FALSE
RESIDUAL_SCALAR=topological_parity_to_source_ratio_normalization
RESIDUAL_TOPOLOGY=no_retained_w2_law_setting_K_TL_to_zero
```

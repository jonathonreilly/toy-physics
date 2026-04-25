# Koide Q monoidal fusion trace no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_monoidal_fusion_trace_no_go.py`  
**Status:** no-go; not closure

## Theorem attempt

Strengthen the categorical trace/naturality route by requiring compatibility
with the retained real `C_3` tensor product.  If monoidality forced equal
total weights for the real singlet and real doublet, it would derive `K_TL=0`.

## Executable theorem

The retained real representation ring has irreps `1` and `D`, where `D` is
the two-dimensional real irrep whose complexification is `chi + chi^2`.

The fusion rule is exact:

```text
D tensor D = 2*1 + D.
```

A positive monoidal dimension function with `dim(1)=1` must satisfy

```text
dim(D)^2 = 2 + dim(D).
```

The positive solution is

```text
dim(D) = 2.
```

Thus the monoidal/Frobenius-Perron trace weights are `1:2`, not equal total
block weights `1:1`.

## Consequence

```text
weights(1,D) = (1,2) -> Q = 1, K_TL = 3/8
weights(1,D) = (1,1) -> Q = 2/3, K_TL = 0
```

The equal-block trace lands on Koide, but it violates the retained fusion
dimension equation:

```text
1^2 != 2 + 1.
```

## Residual

```text
RESIDUAL_TRACE_STATE = equal_block_weight_not_fusion_monoidal_equiv_K_TL
```

The categorical route is now sharper: ordinary central-state naturality leaves
the ratio free; adding monoidal fusion compatibility fixes the off-Koide
rank/Frobenius-Perron ratio.

## Why this is not closure

This packet proves that the strongest retained monoidal categorical structure
does not derive the equal-block law.  It pushes in the opposite direction:
the canonical fusion dimension of the real doublet is `2`.

## Falsifiers

- A retained categorical trace that is physically relevant but deliberately
  non-monoidal, with a theorem selecting equal total blocks.
- A quotient/functor that changes the fusion rule before the charged-lepton
  second-order carrier is formed.
- A new physical principle explaining why block-total democracy supersedes
  Frobenius-Perron dimension in this lane.

## Boundaries

- The runner covers the semisimple real `C_3` representation ring and positive
  monoidal dimension functions.
- It does not exclude a non-monoidal physical coarse graining; it shows that
  such a coarse graining cannot be advertised as forced by retained fusion
  naturality.

## Hostile reviewer objections answered

- **"Categorical trace should be natural."**  Plain naturality leaves the
  central trace ratio free; monoidal naturality fixes the ratio to `1:2`.
- **"Equal block weights are categorical because there are two objects."**
  Counting simple object labels is not compatible with tensor product:
  `D tensor D = 2*1 + D`.
- **"Could this still support Q?"**  It supports the statement that Q needs a
  non-monoidal block-total physical principle.  It does not derive that
  principle.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_monoidal_fusion_trace_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected runner closeout:

```text
KOIDE_Q_MONOIDAL_FUSION_TRACE_NO_GO=TRUE
Q_MONOIDAL_FUSION_TRACE_CLOSES_Q=FALSE
RESIDUAL_TRACE_STATE=equal_block_weight_not_fusion_monoidal_equiv_K_TL
```

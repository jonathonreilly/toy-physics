# Koide Q finite-group BRST/ghost no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_brst_finite_group_ghost_no_go.py`  
**Status:** no-go; not closure

## Theorem attempt

Test whether BRST/Faddeev-Popov ghost data from quotienting by the retained
finite `C_3` symmetry can cancel the rank mismatch between the singlet and
real doublet blocks, deriving `K_TL=0`.

## Executable theorem

For the retained triplet `V_3`, the cyclic norm map and coboundary are

```text
N = 1 + C + C^2
d = C - 1.
```

The runner verifies:

```text
dim ker(N) = 2
dim im(C-I) = 2
dim H^1(C3,V3) = 0.
```

So the finite group quotient supplies no ghost zero modes.

The finite group volume `|C_3|=3` is a common factor:

```text
(2/3)/(1/3) = 2.
```

It does not change the singlet/doublet block ratio.

## Residual

```text
RESIDUAL_SCALAR = no_C3_ghost_zero_mode_to_cancel_rank_mismatch
RESIDUAL_GHOST_INDEX = no_C3_ghost_zero_mode_to_cancel_rank_mismatch
```

The retained index remains `1-2=-1`.  Cancelling it would require a new
auxiliary zero mode or field.

## Why this is not closure

Finite discrete quotients do not have continuous gauge directions.  Their
BRST/FP contribution is a common finite group-volume factor, not a new
degree of freedom that can turn `1:2` into `1:1`.

## Falsifiers

- A retained auxiliary/ghost zero mode in the charged-lepton second-order
  carrier.
- A nontrivial finite-group cohomology class over a retained coefficient system
  that changes the source ratio.
- A physical quotient measure theorem whose stabilizer/groupoid weights select
  equal blocks without adding target-equivalent assumptions.

## Boundaries

- The runner covers the finite `C_3` quotient on the retained triplet over
  characteristic zero.
- It does not exclude new continuous gauge structure or additional retained
  ghost fields outside the current carrier.

## Hostile reviewer objections answered

- **"Gauge fixing could add ghosts."**  Continuous gauge fixing can.  A finite
  `C_3` quotient gives no local FP ghost zero modes here.
- **"The group volume changes weights."**  It is common to both blocks and
  cancels from the ratio.
- **"Could a ghost cancel the Witten index?"**  Only if a new auxiliary zero
  mode is retained; current `C_3` cohomology supplies none.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_brst_finite_group_ghost_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected runner closeout:

```text
KOIDE_Q_BRST_FINITE_GROUP_GHOST_NO_GO=TRUE
Q_BRST_FINITE_GROUP_GHOST_CLOSES_Q=FALSE
RESIDUAL_SCALAR=no_C3_ghost_zero_mode_to_cancel_rank_mismatch
RESIDUAL_GHOST_INDEX=no_C3_ghost_zero_mode_to_cancel_rank_mismatch
```

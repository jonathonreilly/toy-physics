# Koide delta selected-endpoint mark reassessment

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_delta_selected_endpoint_mark_reassessment.py`  
**Status:** reassessment; delta remains open

## Purpose

This note consolidates the latest attacks after the minimal radian-input
routes.  The question is now:

```text
Can the selected rank-one endpoint mark and endpoint basepoint be derived,
or are they the explicit remaining primitive?
```

## New Attacks

The packet now includes:

- `Z3` Wilson `d^2`-power quantization no-go;
- lattice propagator radian quantum no-go;
- `hw=1+baryon` Wilson holonomy no-go;
- minimal radian-input reassessment;
- unmarked primitive naturality no-go;
- boundary-defect mark no-go;
- source-asymmetry mark-transfer no-go.

## Unified Residual

The residual has two equivalent forms:

```text
delta/eta_APS - 1 = mu - 1 + c/eta_APS
delta/eta_APS - 1 = -spectator_channel + c/eta_APS
```

Closure requires:

```text
mu = 1
spectator_channel = 0
c = 0
```

In geometric terms:

```text
retain an oriented selected rank-one endpoint mark P_sel
retain the based endpoint trivialization c=0
preserve Q's quotient/zero-source readout
```

## What Was Ruled Out

- finite `C3`, spin, and projective Wilson data do not force `W^9=exp(2i)`;
- selected one-clock propagator equivariance leaves its phase free;
- `hw=1+baryon` total support leaves selected/spectator split free;
- unmarked primitive naturality gives selected weight `1/2`;
- invariant defects are scalar, while rank-one defect orientation is free;
- Q-invariant source transfer cannot orient a rank-one boundary mark.

## Remaining Positive Theorem

A true closure must derive:

```text
retained_oriented_selected_rank_one_endpoint_mark
based_endpoint_c_equals_zero
```

from physical boundary/source structure, or produce an equivalent vector-valued
joint Q/delta theorem.  Anything less is support or a renamed primitive.

## Verdict

```text
KOIDE_DELTA_SELECTED_ENDPOINT_MARK_REASSESSMENT=TRUE
DELTA_SELECTED_ENDPOINT_MARK_REASSESSMENT_CLOSES_DELTA=FALSE
RESIDUAL_MARK=retained_oriented_selected_rank_one_endpoint_mark
RESIDUAL_TRIVIALIZATION=based_endpoint_c_equals_zero
RESIDUAL_COMPATIBILITY=preserve_Q_quotient_zero_source_readout
NEXT_ATTACK=derive_selected_endpoint_mark_or_formalize_as_explicit_new_primitive
```

## Verification

```bash
python3 scripts/frontier_koide_delta_selected_endpoint_mark_reassessment.py
python3 scripts/frontier_koide_hostile_review_guard.py
python3 scripts/frontier_koide_lane_regression.py
```

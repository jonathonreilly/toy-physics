# Koide delta source-asymmetry mark-transfer no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_delta_source_asymmetry_mark_transfer_no_go.py`  
**Status:** executable no-go; Q-invariant source cannot orient the delta mark

## Theorem Attempt

Use the charged-lepton source sector to orient the missing boundary defect mark.
If this worked, the selected endpoint mark would not have to be added as a new
delta primitive.

## Result

Negative.  The Q-closing source readout is quotient/rotation invariant:

```text
p = 1/2
source_vector = 0.
```

An equivariant transfer from an invariant source must produce an invariant
boundary object.  The only invariant vector in the primitive block is zero,
which cannot define a rank-one projector.

A nonzero source vector can orient a rank-one boundary line, but then the
orientation is a source-visible label.  That reopens the Q-side source law
unless a new joint theorem explains why the same orientation is invisible to Q
but visible to delta.

## Residual

```text
RESIDUAL_MARK = oriented_boundary_mark_not_from_Q_invariant_source
RESIDUAL_Q = nonzero_source_orientation_would_reopen_Q_source_law
COUNTERSTATE = Q_invariant_source_maps_to_no_rank_one_mark
NEXT_ATTACK = joint_Q_delta_theorem_or_explicit_selected_endpoint_primitive
```

## Hostile Review

This prevents a hidden transfer from being promoted.  Q-compatible source
invariance does not carry enough data to orient the Brannen endpoint.  A
source orientation that does carry enough data is an extra primitive unless
retained by a new joint Q/delta theorem.

## Verification

```bash
python3 scripts/frontier_koide_delta_source_asymmetry_mark_transfer_no_go.py
python3 -m py_compile scripts/frontier_koide_delta_source_asymmetry_mark_transfer_no_go.py
```

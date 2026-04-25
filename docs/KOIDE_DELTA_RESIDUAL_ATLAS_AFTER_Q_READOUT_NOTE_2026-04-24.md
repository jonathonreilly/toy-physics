# Koide delta residual atlas after Q readout

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_delta_residual_atlas_after_q_readout.py`  
**Status:** atlas; not closure

## Current Residual

After the readout-retention split audit, the strongest state is:

```text
Q source condition:
  removed if strict zero-source source-response readout is accepted.

delta endpoint condition:
  still open.
```

The remaining full-lane obstruction is:

```text
RESIDUAL_DELTA = closed_APS_to_open_selected_line_endpoint_functor
```

## Candidate Routes

The atlas ranks the next endpoint attacks:

```text
1. endpoint functor classification
2. orientation-preserving determinant-line automorphism
3. contractible selected-line base trivialization
4. relative cobordism uniqueness
5. spectral-flow normalization by crossing count
6. Callan-Harvey current normalization
7. Brannen coordinate as closed holonomy chart
8. all endpoint natural transformations
9. boundary energy minimization with no free center
```

## Next Attack

The selected next attack is:

```text
endpoint_functor_classification
```

because it targets the residual functor itself.  The goal is to reduce the
closed-to-open bridge freedom to explicit parameters and show whether identity
is forced or remains a primitive.

## Verification

Run:

```bash
python3 scripts/frontier_koide_delta_residual_atlas_after_q_readout.py
```

Expected closeout:

```text
KOIDE_DELTA_RESIDUAL_ATLAS_AFTER_Q_READOUT=TRUE
DELTA_ATLAS_CLOSES_DELTA=FALSE
RESIDUAL_SCALAR=closed_APS_to_open_selected_line_endpoint_functor
NEXT_ATTACK=endpoint_functor_classification
```

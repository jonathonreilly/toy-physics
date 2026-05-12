# PR230 Additive-Top Subtraction Row Contract

**Status:** exact support / subtraction contract only; current coarse
additive rows are bounded support and strict W/Z authority is absent

**Runner:** `scripts/frontier_yt_pr230_additive_top_subtraction_row_contract.py`

**Certificate:** `outputs/yt_pr230_additive_top_subtraction_row_contract_2026-05-07.json`

```yaml
actual_current_surface_status: exact-support / additive-top subtraction row contract; current additive Jacobian rows are bounded support only, while W/Z rows, matched covariance, strict g2, and accepted action remain absent
conditional_surface_status: exact support for a future same-surface row packet that measures and subtracts the independent additive top component
proposal_allowed: false
bare_retained_allowed: false
```

## Claim

Block04 exposed the contamination in the current same-coordinate ansatz:

```text
dS/ds = O_top_additive + O_H.
```

For a top/W response route this means

```text
T_total = dE_top/ds = y_t dv/ds / sqrt(2) + A_top
W       = dM_W/ds   = g2 dv/ds / 2.
```

If the independent additive top slope `A_top` is measured on the same source
coordinate and same ensemble, the corrected readout is

```text
y_t = g2 (T_total - A_top) / (sqrt(2) W).
```

The runner verifies this identity on finite witness rows and checks that it is
invariant under source reparameterization `s' = lambda s`.  All same-source
slopes scale together, so the corrected ratio is unchanged.

## Required Row Packet

A future strict packet must provide:

- `T_total = dE_top/ds` under the mixed current-source coordinate;
- `A_top`, the independent additive top slope under the same coordinate
  convention;
- `W = dM_W/ds` or `Z = dM_Z/ds` under the same source shifts;
- matched covariance for `T_total`, `A_top`, `W/Z`, and strict non-observed
  `g2` or `sqrt(g2^2 + gY^2)`.

The runner records the delta-method gradient for

```text
y_t(T,A,W,g2) = g2 (T - A) / (sqrt(2) W)
```

and requires covariance for the subtraction.  Marginal errors are not enough.

## Boundary

Without a measured `A_top`, the same fixed total top and W response slopes can
be represented by multiple `y_t` values and corresponding additive slopes.
Thus setting `A_top = 0` by convention would recreate the definition-as-
derivation failure in a new coordinate.

The current PR230 surface now has a complete 63-row coarse additive-top
Jacobian packet.  That is still bounded support only: strict subtraction needs
per-configuration same-source additive rows, W/Z response rows, matched
covariance, strict `g2`, and accepted radial-spurion action authority.  This
block therefore narrows a positive repair path but does not close PR230.

## Non-Claims

This note does not claim retained or `proposed_retained` closure.  It does not
set the additive top component to zero, does not infer matched covariance from
marginal row errors, does not use observed `y_t`, observed top mass, observed
W/Z masses, observed `g2`, `H_unit`, `yt_ward_identity`, `alpha_LM`,
plaquette/`u0`, reduced pilots, or unit-normalization shortcuts, and does not
touch the live chunk worker.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_pr230_additive_top_subtraction_row_contract.py
python3 scripts/frontier_yt_pr230_additive_top_subtraction_row_contract.py
# SUMMARY: PASS=22 FAIL=0
```

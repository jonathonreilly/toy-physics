# Top-Yukawa Scalar LSZ Residue Bridge Note

**Date:** 2026-05-01  
**Status:** exact negative boundary / open bridge; no retention proposal  
**Runner:** `scripts/frontier_yt_scalar_lsz_residue_bridge.py`  
**Certificate:** `outputs/yt_scalar_lsz_residue_bridge_2026-05-01.json`

## Purpose

The Ward repair needs a physical scalar external-leg theorem.  Existing color
projection notes supply the channel arithmetic `R_conn = 8/9`, but the audit
objection is sharper: a connected color-channel ratio is not automatically the
physical scalar pole residue that LSZ uses.

This note makes that distinction executable.

## Current Ledger State

The runner checks the relevant current audit rows:

| Row | Effective status |
|---|---|
| `rconn_derived_note` | `audited_conditional` |
| `yukawa_color_projection_theorem` | `audited_conditional` |
| `yt_color_projection_correction_note` | `audited_conditional` |
| `yt_ew_color_projection_theorem` | `audited_conditional` |

This confirms that the color/LSZ bridge is not a clean retained dependency on
the current surface.

## Countermodel Check

The channel ratio arithmetic is

```text
R_conn = (N_c^2 - 1) / N_c^2 = 8/9.
```

Hold this ratio fixed, but vary the scalar two-point pole residue by an
independent scale:

| residue scale | pole residue | LSZ factor |
|---:|---:|---:|
| `0.5` | `0.444444444444444` | `0.666666666666667` |
| `1.0` | `0.888888888888889` | `0.942809041582063` |
| `2.0` | `1.777777777777778` | `1.333333333333333` |

All rows preserve the same `R_conn`.  The LSZ factor changes.  Therefore
`R_conn` by itself is not a scalar pole-residue theorem.

## Runner Result

```text
PYTHONPATH=scripts python3 scripts/frontier_yt_scalar_lsz_residue_bridge.py
# SUMMARY: PASS=6 FAIL=0
```

## Consequence

The remaining theorem must derive the scalar pole residue from the retained
source two-point function and prove how that residue enters the physical
Yukawa external leg.  Until then, applying `sqrt(8/9)` is conditional bridge
arithmetic, not audit-clean Yukawa closure.

## Non-Claims

- This note does not reject `R_conn = 8/9` as channel arithmetic.
- This note does not derive scalar `Z_phi`.
- This note does not promote the Ward theorem or PR #230.
- This note does not use observed top mass or observed Yukawa values.

# Top-Yukawa Common Dressing Obstruction Note

**Date:** 2026-05-01  
**Status:** exact negative boundary / open bridge; no retention proposal  
**Runner:** `scripts/frontier_yt_common_dressing_obstruction.py`  
**Certificate:** `outputs/yt_common_dressing_obstruction_2026-05-01.json`

## Purpose

The old Ward route also needs a common-dressing bridge: the scalar Yukawa
readout and the gauge coupling readout must receive the same normalization if
the tree-level ratio is to survive as a physical measured ratio.  The audit
specifically warns that this dressing cannot be imported through the old
Ward identification, alpha_LM, or plaquette normalization.

This note shows that common dressing is an extra theorem, not a consequence of
the current Ward/gauge identities.

## Countermodel Check

Start with the tree-level source ratio

```text
y_source / g_source = 1/sqrt(6).
```

Allow independent scalar and gauge dressing factors:

```text
(y/g)_measured = (1/sqrt(6)) * Z_scalar / Z_gauge.
```

The runner holds the same tree-level ratio and varies only the dressing pair:

| `Z_scalar` | `Z_gauge` | measured `y/g` |
|---:|---:|---:|
| `1.0` | `1.0` | `0.408248290463863` |
| `0.9` | `1.0` | `0.367423461417477` |
| `1.1` | `0.95` | `0.472708546852894` |
| `1.0` | `1.05` | `0.388807895679870` |

All rows preserve the same tree-level source ratio.  The physical ratio changes
unless `Z_scalar = Z_gauge` is independently proved.

## Runner Result

```text
PYTHONPATH=scripts python3 scripts/frontier_yt_common_dressing_obstruction.py
# SUMMARY: PASS=6 FAIL=0
```

## Current Parent Status

| Parent | Effective status |
|---|---|
| `yt_ward_identity_derivation_theorem` | `audited_renaming` |
| `alpha_lm_geometric_mean_identity_theorem_note_2026-04-24` | `audited_decoration` |
| `plaquette_self_consistency_note` | `audited_conditional` |
| `gauge_vacuum_plaquette_bridge_support_note` | `audited_conditional` |

These cannot be used as clean proof of common scalar/gauge dressing in PR #230.

## Consequence

Gauge Ward identities protect the gauge current.  They do not by themselves
protect the scalar-density readout or prove equality with scalar LSZ dressing.
The Ward repair therefore needs a retained symmetry/dynamics theorem equating
the scalar and gauge dressing factors, or it must carry the dressing ratio as a
separate measured input.

## Non-Claims

- This note does not deny the tree-level `1/sqrt(6)` source ratio.
- This note does not use alpha_LM or plaquette normalization as a proof input.
- This note does not promote the Ward theorem or PR #230.
- This note does not use observed top mass or observed Yukawa values.

# Top-Yukawa Chirality Selector Bridge Note

**Date:** 2026-05-01  
**Status:** conditional-support / open; no retention proposal  
**Runner:** `scripts/frontier_yt_chirality_selector_bridge.py`  
**Certificate:** `outputs/yt_chirality_selector_bridge_2026-05-01.json`

## Purpose

The Ward physical-readout repair needs a clean map from the scalar bilinear to
the physical `Qbar_L H q_R` trilinear.  This note isolates the selector part:
given the repo's hypercharge convention, gauge invariance uniquely selects the
right-handed partner for each Higgs component.

This is only conditional support because the parent matter/hypercharge rows are
not clean enough on the current audit surface.

## Enumeration

Use the existing convention

```text
Q = T3 + Y/2.
```

Then

| Field | Hypercharge |
|---|---:|
| `Qbar_L` | `-1/3` |
| `u_R` | `+4/3` |
| `d_R` | `-2/3` |
| `H` | `+1` |
| `H_tilde` | `-1` |

Enumerating the four one-Higgs candidates gives:

| Candidate | Hypercharge sum | Gauge invariant |
|---|---:|---|
| `Qbar_L H u_R` | `2` | no |
| `Qbar_L H d_R` | `0` | yes |
| `Qbar_L H_tilde u_R` | `0` | yes |
| `Qbar_L H_tilde d_R` | `-2` | no |

Therefore the up component selects `u_R` with `H_tilde`, and the down component
selects `d_R` with `H`.

## Runner Result

```text
PYTHONPATH=scripts python3 scripts/frontier_yt_chirality_selector_bridge.py
# SUMMARY: PASS=8 FAIL=0
```

## Parent Firewall

The selector arithmetic is not enough for retained closure because the relevant
parents are not clean:

| Parent | Effective status |
|---|---|
| `anomaly_forces_time_theorem` | `audited_conditional` |
| `one_generation_matter_closure_note` | `audited_conditional` |
| `standard_model_hypercharge_uniqueness_theorem_note_2026-04-24` | `audited_conditional` |
| `sm_one_higgs_yukawa_gauge_selection_theorem_note_2026-04-26` | proposal-stage; not audit-clean |
| `yt_class_5_non_ql_yukawa_vertex_note_2026-04-18` | `audited_failed` |

## Consequence

This route narrows the chirality-selector objection: the selector is
gauge-arithmetic, not a free choice, once the matter/hypercharge parents are
allowed.  It does not solve scalar normalization, scalar carrier
identification, or the non-clean parent statuses.

## Non-Claims

- This note does not derive the parent hypercharge or matter authorities.
- This note does not derive scalar LSZ normalization.
- This note does not identify the Yukawa by an `H_unit` matrix element.
- This note does not promote the Ward theorem or PR #230 to retained closure.

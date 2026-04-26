# Audit Ledger

**Generated:** 2026-04-26T22:02:45.584303+00:00  
**Source of truth:** `data/audit_ledger.json`  
**Schema:** see [README.md](README.md), [FRESH_LOOK_REQUIREMENTS.md](FRESH_LOOK_REQUIREMENTS.md), and [ALGEBRAIC_DECORATION_POLICY.md](ALGEBRAIC_DECORATION_POLICY.md).

This file is auto-generated. Do not edit by hand. Apply audits via `scripts/apply_audit.py`, then re-run `scripts/compute_effective_status.py` and `scripts/render_audit_ledger.py`.

## Reading rule

- **Bold** = audit-ratified (`retained`, `promoted`).  
- _Italic_ = author-proposed but not yet audit-ratified (`proposed_retained`, `proposed_promoted`).  
- ~~Strikethrough~~ = audit returned a failure verdict.  
- Plain = `support`, `bounded`, `open`, or `unknown`.  

Publication-facing tables MUST read `effective_status`, not `current_status`.

## Summary

| effective_status | count |
|---|---:|
| _proposed_retained_ | 318 |
| _proposed_promoted_ | 8 |
| bounded | 183 |
| support | 96 |
| open | 11 |
| unknown | 985 |

| audit_status | count |
|---|---:|
| `unaudited` | 1601 |

| criticality | count |
|---|---:|
| `critical` | 647 |
| `high` | 70 |
| `medium` | 140 |
| `leaf` | 744 |

- **Proposed claims demoted by upstream:** 125
- **Citation cycles detected:** 283

### Runner classification (static heuristic)

- runners classified: 679
- runners with (C) first-principles compute hits: 410
- runners with (D) external comparator hits: 173
- decoration candidates (no C, no D): 71

## Applied audits

_No audits applied yet._


## Audit findings (full)


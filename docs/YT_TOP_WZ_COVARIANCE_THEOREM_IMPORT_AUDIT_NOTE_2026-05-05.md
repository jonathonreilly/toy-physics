# PR #230 Top/W Covariance-Theorem Import Audit

Status: exact negative boundary / no importable same-surface top-W
covariance theorem on current PR230 surface; proposal_allowed=false.

```yaml
actual_current_surface_status: exact negative boundary / no importable same-surface top-W covariance theorem on current PR230 surface
proposal_allowed: false
bare_retained_allowed: false
```

**Runner:** `scripts/frontier_yt_top_wz_covariance_theorem_import_audit.py`
**Certificate:** `outputs/yt_top_wz_covariance_theorem_import_audit_2026-05-05.json`

## Purpose

This cycle closes the remaining import shortcut in the same-source W/Z route:
whether an existing current-branch artifact can be treated as the strict
product-measure, conditional-independence, or closed-covariance theorem needed
to avoid matched top/W response rows.

It cannot.  The current branch has support builders, gates, scout schemas, and
no-go certificates.  None is a production/theorem artifact fixing
`cov_dE_top_dM_W` on the same top/W source surface.

## Boundary

The audit classifies the existing top/W covariance surfaces:

- the marginal-covariance artifact is a no-go, not authority;
- the factorization-independence gate has no production theorem in current
  mode;
- the deterministic-response covariance gate rejects deterministic W response
  alone;
- scout certificates remain scout schemas;
- top/W builders remain open until real strict inputs exist.

The future admissible theorem path is:

```text
outputs/yt_top_wz_closed_covariance_theorem_2026-05-05.json
```

It must prove same-surface product-measure factorization, conditional
independence, or a closed finite covariance formula with the required top/W
source identities and firewalls.

## Validation

```bash
python3 -m py_compile scripts/frontier_yt_top_wz_covariance_theorem_import_audit.py
python3 scripts/frontier_yt_top_wz_covariance_theorem_import_audit.py
# SUMMARY: PASS=11 FAIL=0
```

## Non-Claims

This artifact does not claim retained or `proposed_retained` top-Yukawa
closure.  It writes no matched top/W rows, promotes no scout artifact, imports
no observed W/Z/top/`y_t`/`g_2` selector, uses no `H_unit`/Ward authority or
other shortcut normalization, and does not package or rerun chunk MC.

## Next Action

Supply the real same-surface top/W joint covariance theorem at the future path
above, or supply measured matched top/W response rows.  Do not import builders,
scout schemas, support-only W decompositions, or no-go gates as covariance
authority.

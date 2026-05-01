# PR230 Global Top-Yukawa Proof Audit Note

**Date:** 2026-05-01  
**Status:** exact negative boundary on the current audit surface; no existing
audited-retained `y_t` proof found  
**Runner:** `scripts/frontier_yt_pr230_global_proof_audit.py`  
**Certificate:** `outputs/yt_pr230_global_proof_audit_2026-05-01.json`

## Purpose

PR #230 reopened the top-Yukawa lane after the direct lattice-correlator route
proved too large for immediate production closure.  The next question was
whether the repo already contained an audit-retained `y_t` proof that the audit
had missed.  This note records the repo-wide inventory result.

## Method

The runner scans all `docs/YT*.md` notes and the audit ledger rows whose keys
belong to the top-Yukawa/top-mass family.  It then checks the proof-looking
families that could plausibly close PR #230:

| Route family | Current effective status |
|---|---|
| Ward / zero-import stack | `audited_renaming` at the load-bearing Ward node |
| Color projection / scalar LSZ stack | `audited_conditional` |
| Direct lattice correlator | `audited_conditional`; cutoff and production evidence remain open |
| Planck double-criticality selector | `audited_conditional`; `beta_lambda(M_Pl)=0` not derived |
| P1/P2/P3 matching stack | blocked by non-clean Ward/color/normalization parents |

The check is not a text-search proof of physics.  It uses the audit ledger as
the current authority surface and records where proof-like notes still fail
their audit boundary.

## Result

```text
PYTHONPATH=scripts python3 scripts/frontier_yt_pr230_global_proof_audit.py
# SUMMARY: PASS=9 FAIL=0
```

Key findings:

| Check | Result |
|---|---|
| `docs/YT*.md` inventory | 103 notes scanned |
| top-Yukawa/top-mass ledger inventory | 95 rows scanned |
| effective retained `yt_` rows | none |
| `yt_ward_identity_derivation_theorem` | `audited_renaming` |
| `yt_zero_import_authority_note` | `audited_renaming` |
| `yt_color_projection_correction_note` | `audited_conditional` |
| direct correlator theorem note | `audited_conditional` |
| Planck double-criticality selector | `audited_conditional` |

## Claim Boundary

This result closes only the inventory question: the current repo does not
already contain a hidden audit-retained top-Yukawa proof.  It does not derive
`y_t`, promote the Ward route, or certify the direct-correlator route.

## Next Route Selected

The highest-leverage remaining route is the Ward physical-readout repair:
derive the physical Yukawa vertex/readout map without defining the Yukawa by
the old `H_unit` matrix-element identification.

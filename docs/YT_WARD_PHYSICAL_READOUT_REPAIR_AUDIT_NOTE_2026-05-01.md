# Top-Yukawa Ward Physical-Readout Repair Audit Note

**Date:** 2026-05-01  
**Status:** exact negative boundary / open repair map on the current audit
surface  
**Runner:** `scripts/frontier_yt_ward_physical_readout_repair_audit.py`  
**Certificate:** `outputs/yt_ward_physical_readout_repair_audit_2026-05-01.json`

## Purpose

The old Ward note correctly computes the scalar-singlet normalization
arithmetic, but the audit demoted it because the physical Standard Model
Yukawa readout was introduced by identification rather than derived.  The audit
ledger states the repair target directly: derive the physical observable bridge
from the retained action, including the common dressing, without defining the
top Yukawa by the `H_unit`-to-top matrix element.

This note converts that audit objection into an executable repair checklist.

## Narrow Audit Objection

The current ledger rationale for `yt_ward_identity_derivation_theorem` says the
load-bearing move defines the top-Yukawa readout as the `H_unit` matrix element
and then uses that definition as the derivation.  Therefore the repaired route
must derive all physical readout maps independently:

1. source or Hubbard-Stratonovich normalization;
2. SSB VEV division and vertex coefficient extraction;
3. chirality projection from the `Q_L` scalar bilinear to the physical
   `Qbar_L H q_R` trilinear;
4. physical scalar uniqueness/carrier map;
5. scalar LSZ/external-leg normalization;
6. absence of extra numerical factors or hidden dressing differences.

## Runner Result

```text
PYTHONPATH=scripts python3 scripts/frontier_yt_ward_physical_readout_repair_audit.py
# SUMMARY: PASS=12 FAIL=0
```

The runner passes as a boundary check, not as a closure check.  It confirms
that the current repo contains prose and arithmetic for the relevant pieces,
but the audit-clean dependency state is still open:

| Repair requirement | Current effective status |
|---|---|
| source / HS / Legendre normalization | `audited_renaming` |
| chirality projection / right-handed selector | `audited_failed` |
| physical scalar uniqueness carrier | `audited_failed` |
| scalar LSZ external leg | `audited_conditional` |
| absence of extra factors | not cleanly derived |

## Consequence

The repo does not yet close the Ward repair.  The next positive target is a
tree-level operator-matching theorem and runner that computes the functional
derivatives before and after SSB, tracks the chirality and scalar-leg factors,
and proves that no extra normalization enters.

## Non-Claims

- This note does not promote `yt_ward_identity_derivation_theorem`.
- This note does not define the top Yukawa by the old `H_unit` matrix element.
- This note does not use observed top mass or observed Yukawa values as proof
  inputs.
- This note does not claim retained closure for PR #230.

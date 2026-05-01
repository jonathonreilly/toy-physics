# PR230 Assumption / Import Stress Certificate

**Date:** 2026-05-01  
**Status:** open / assumption-import stress complete  
**Runner:** `scripts/frontier_yt_pr230_assumption_import_stress.py`  
**Certificate:** `outputs/yt_pr230_assumption_import_stress_2026-05-01.json`

```yaml
actual_current_surface_status: open
conditional_surface_status: null
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "Open scalar-LSZ and heavy-matching imports remain after assumption stress."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Purpose

This note records the refreshed assumptions exercise for the PR #230 rerun.
The prior assumptions ledger existed, but it had not yet absorbed the kinetic
route and matching obstruction.

## Result

```text
python3 scripts/frontier_yt_pr230_assumption_import_stress.py
# SUMMARY: PASS=8 FAIL=0
```

The refreshed `A_min` allows only:

```text
retained Cl(3)/Z^3 substrate
+ g_bare = 1 as substrate input
+ Wilson-staggered Dirac/gauge action already in PR230 harness
+ standard functional derivative / correlator extraction definitions
+ structural counts N_c=3, N_iso=2
```

The stress test explicitly forbids:

- `H_unit`-to-top matrix-element definition;
- `yt_ward_identity` as `y_t` authority;
- observed top mass or observed `y_t` as proof selectors;
- `alpha_LM`, plaquette, or `u0` as load-bearing normalization;
- reduced cold-gauge pilot values as production evidence;
- `c2 = 1` unless derived from the action in the same route;
- `Z_match = 1` unless derived as a matching theorem.

## Consequence

No current PR #230 route certificate authorizes retained-proposal wording.
Positive closure still requires one of:

1. production/statistics with momentum modes plus a derived heavy matching
   bridge;
2. scalar-channel pole/LSZ theorem deriving projector, zero-mode/IR limit,
   eigenvalue crossing, and residue;
3. an independent retained parent repair for the chirality/scalar carrier
   bridge.

## Non-Claims

- This note is not a `y_t` derivation.
- This note is not a production measurement.
- This note does not use observed top mass as calibration.
- This note does not define `y_t` through an `H_unit` matrix element.

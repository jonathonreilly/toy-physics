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
route, matching obstruction, and source-overlap renormalization boundary.

## Result

```text
python3 scripts/frontier_yt_pr230_assumption_import_stress.py
# SUMMARY: PASS=18 FAIL=0
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
- `alpha_LM`, plaquette, or `u0` as load-bearing normalization or proof input;
- reduced cold pilots, including cold-gauge pilot values, as production
  evidence;
- `c2 = 1` unless derived from the action in the same route;
- `Z_match = 1` unless derived as a matching theorem.
- `kappa_s = 1` unless derived by scalar LSZ/canonical normalization.
- canonical `Z_h = 1` as a substitute for the source operator overlap
  `<0|O_s|h>`.
- source contact counterterms or contact-renormalized `C_ss(0)` / `C_ss'(0)`
  as substitutes for the isolated pole residue.
- a single finite source-shift radius as the zero-source Feynman-Hellmann
  derivative without a finite-source-linearity gate, multiple radii, or a
  retained analytic response-bound theorem.
- a source-Higgs cross-correlator `C_sH` as hidden authority; it remains an
  open observable/theorem until a canonical-Higgs source operator and
  cross-correlator implementation are supplied.
- the `source_higgs_cross_correlator` or `wz_mass_response` production metadata
  guards as evidence.  The source-Higgs path may have default-off finite-row
  instrumentation behind a canonical-`O_H` certificate, and W/Z remains
  absent-guarded; neither metadata surface is evidence.
- EW gauge-mass diagonalization, scalar Hessian algebra, or any note that
  starts after canonical `H` is supplied as a same-surface PR #230 operator
  realization.  The route needs an explicit `O_H` or radial `H` observable with
  `C_sH` and `C_HH` pole residues.
- `H_unit` as canonical `O_H` unless the same pole-purity and
  canonical-normalization certificates required of any `O_H` candidate are
  supplied.
- static EW W/Z algebra as a source-response certificate: `dM_W/dh = g2/2`
  after canonical `H` is not `dM_W/ds`.
- slope-only W/Z outputs as proof input unless they come from production W/Z
  mass fits and are paired with sector-overlap plus canonical-Higgs identity
  certificates.
- source-only LSZ data as canonical-Higgs identity: the source-functional LSZ
  identifiability theorem still requires `C_sH` / `C_HH`, a canonical `O_H`
  identity theorem, W/Z response sector overlap, or rank-one neutral-scalar
  dynamics.

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
- This note does not use `yt_ward_identity` as `y_t` authority.
- This note does not set `kappa_s = 1` without deriving scalar LSZ/canonical
  normalization.
- This note does not use source-only LSZ data as a canonical-Higgs identity.

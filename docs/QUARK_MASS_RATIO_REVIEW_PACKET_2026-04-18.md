# Quark Mass-Ratio Review Packet (2026-04-18)

## Scope

This is the reviewer-facing front door for the live quark mass-ratio lane on
current `main`.

It bundles the live down-type, up-type, minimal full-solve, and bounded
quark-CP closure notes into one review path. It does not promote the full
quark spectrum to retained closure.

## Exact Current Endpoint

The clean current endpoint is:

- the promoted CKM atlas/axiom package and canonical `alpha_s(v)` provide the
  live input surface
- the down-type CKM-dual lane is the strongest current quark-side result and
  numerically matches the threshold-local self-scale comparators well
- the down-type authority note still classifies that lane as bounded, because
  GST and the `5/6` bridge are support/bridge inputs rather than promoted
  theorem-core steps
- the up-type inversion lane is live as a bounded extension with one interior
  partition `(f_12, f_23)`
- the new minimal Schur-NNI full-solve runner now inverts the up-sector ratios
  from the CKM magnitudes cleanly on a bounded carrier surface
- on the observation-comparator partition, `m_u/m_c` lands within `3%`
  while `m_c/m_t` stays low by about one order of magnitude under the current
  CP-orthogonal combination rule
- on the stronger minimal Schur-NNI solve, the quark magnitudes close well,
  but the Jarlskog area still stays far below the atlas value on that same
  minimal surface
- on the strongest current bounded extension, one fixed projector ray with two
  real sector amplitudes plus one shared phase already closes the full quark
  package numerically while keeping `arg det(M_u M_d) = 0 mod 2pi`
- the new parameter audit reduces the remaining non-derived content further:
  the current surface already supports the exact projector ray, an exact down
  amplitude `1/sqrt(42)`, and a support-angle probe `-1/42 rad`, leaving one
  missing up-sector scalar amplitude law
- the new up-amplitude candidate scan then compresses that remaining scalar to
  a short bounded exact shortlist: `7/9` is the strongest small-rational
  refit candidate, `sqrt(3/5)` is the strongest small-radical anchored
  candidate, and projector/support-native dressings also stay near closure
- the new restricted native-expression scan sharpens that again: within a
  one-step native projector/support grammar, the best refit law is
  `atan(sqrt(5)) - sqrt(5)/6`, the best anchored law is
  `sqrt(5/6) * (1 - 1/sqrt(42))`, and no native one-step law beats both the
  `7/9` and `sqrt(3/5)` baselines at once
- the new widened native-affine-support no-go sharpens the last scalar again:
  within the projector-prefactored affine family
  `sqrt(5/6) * (c0 + c1 delta_A1)`, nine affine laws beat the `7/9` refit
  baseline, nine affine laws beat the `sqrt(3/5)` anchored baseline, and no
  affine law beats both at once
- the positive affine-support scan and provenance audit clarify that endpoint:
  the cleanest structurally native law is `sqrt(5/6) * (6/7)`, while `7/9`
  and `sqrt(3/5)` remain external empirical baselines rather than native
  projector/support derivations
- the freer complex-carrier completion remains as a broader existence proof

So the current quark-mass-ratio state is:

- review-ready quark packet on current `main`
- strong down-type lane
- explicit bounded up-type extension
- bounded full-solve support for the quark magnitudes on a minimal Schur-NNI carrier
- bounded reduced full CKM+CP closure extension on a fixed projector ray
- bounded parameter audit reducing the remaining gap to one up-sector scalar amplitude law
- bounded widened native-affine-support no-go on projector-prefactored `delta_A1` laws
- bounded broader complex-carrier existence proof
- no retained claim that the full quark CKM+CP package is closed

## Read In Order

1. [CKM_ATLAS_AXIOM_CLOSURE_NOTE.md](./CKM_ATLAS_AXIOM_CLOSURE_NOTE.md)
2. [DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md](./DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md)
3. [UP_TYPE_MASS_RATIO_CKM_INVERSION_NOTE.md](./UP_TYPE_MASS_RATIO_CKM_INVERSION_NOTE.md)
4. [QUARK_MASS_RATIO_FULL_SOLVE_NOTE_2026-04-18.md](./QUARK_MASS_RATIO_FULL_SOLVE_NOTE_2026-04-18.md)
5. [QUARK_PROJECTOR_RAY_PHASE_COMPLETION_NOTE_2026-04-18.md](./QUARK_PROJECTOR_RAY_PHASE_COMPLETION_NOTE_2026-04-18.md)
6. [QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE_2026-04-19.md](./QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE_2026-04-19.md)
7. [QUARK_UP_AMPLITUDE_CANDIDATE_SCAN_NOTE_2026-04-19.md](./QUARK_UP_AMPLITUDE_CANDIDATE_SCAN_NOTE_2026-04-19.md)
8. [QUARK_UP_AMPLITUDE_NATIVE_EXPRESSION_SCAN_NOTE_2026-04-19.md](./QUARK_UP_AMPLITUDE_NATIVE_EXPRESSION_SCAN_NOTE_2026-04-19.md)
9. [QUARK_UP_AMPLITUDE_NATIVE_AFFINE_NO_GO_NOTE_2026-04-19.md](./QUARK_UP_AMPLITUDE_NATIVE_AFFINE_NO_GO_NOTE_2026-04-19.md)
10. [QUARK_UP_AMPLITUDE_AFFINE_SUPPORT_SCAN_NOTE_2026-04-19.md](./QUARK_UP_AMPLITUDE_AFFINE_SUPPORT_SCAN_NOTE_2026-04-19.md)
11. [QUARK_UP_AMPLITUDE_PROVENANCE_AUDIT_NOTE_2026-04-19.md](./QUARK_UP_AMPLITUDE_PROVENANCE_AUDIT_NOTE_2026-04-19.md)
12. [QUARK_UP_AMPLITUDE_TWO_STEP_NATIVE_SCAN_NOTE_2026-04-19.md](./QUARK_UP_AMPLITUDE_TWO_STEP_NATIVE_SCAN_NOTE_2026-04-19.md)
13. [QUARK_CP_CARRIER_COMPLETION_NOTE_2026-04-18.md](./QUARK_CP_CARRIER_COMPLETION_NOTE_2026-04-18.md)
14. [MASS_SPECTRUM_DERIVED_NOTE.md](./MASS_SPECTRUM_DERIVED_NOTE.md)

Bridge/support context when needed:

- [CKM_FROM_MASS_HIERARCHY_NOTE.md](./CKM_FROM_MASS_HIERARCHY_NOTE.md)
- [CKM_FIVE_SIXTHS_BRIDGE_SUPPORT_NOTE.md](./CKM_FIVE_SIXTHS_BRIDGE_SUPPORT_NOTE.md)

## Package Role

- reviewer-facing intake for the live quark mass-ratio package on `main`
- one-place summary of what is numerically strong versus what is still bounded
- validation front door for the current down-type and up-type replay runners

## Validation

Run:

```bash
python3 scripts/frontier_quark_mass_ratio_review.py
```

Current expected result on this branch:

- `frontier_mass_ratio_ckm_dual.py`: `PASS=23 FAIL=0`
- `frontier_mass_ratio_up_sector.py`: `PASS=23 FAIL=0`
- `frontier_quark_mass_ratio_review.py`: `PASS=46 FAIL=0`
- `frontier_quark_mass_ratio_full_solve.py`: `PASS=15 FAIL=0`
- `frontier_quark_projector_ray_phase_completion.py`: `PASS=8 FAIL=0`
- `frontier_quark_projector_parameter_audit.py`: `PASS=6 FAIL=0`
- `frontier_quark_up_amplitude_candidate_scan.py`: `PASS=7 FAIL=0`
- `frontier_quark_up_amplitude_native_expression_scan.py`: `PASS=5 FAIL=0`
- `frontier_quark_up_amplitude_native_affine_no_go.py`: `PASS=7 FAIL=0`
- `frontier_quark_up_amplitude_affine_support_scan.py`: `PASS=7 FAIL=0`
- `frontier_quark_up_amplitude_provenance_audit.py`: `PASS=12 FAIL=0`
- `PYTHONPATH=scripts python3 scripts/frontier_quark_up_amplitude_two_step_native_scan.py`: `PASS=5 FAIL=0`
- `frontier_quark_cp_carrier_completion.py`: `PASS=11 FAIL=0`
- `frontier_quark_jarlskog_closure_scan.py`: `PASS=5 FAIL=0`
- `frontier_quark_cp_primitive_projector_scan.py`: strongest candidate
  `J/J_atlas = 1.075`

## Review Standard

This packet is clean enough for review, consolidation, and downstream
quark-sector work on current `main`.

It is not a retained-spectrum promotion. The honest package status remains:

- down-type lane is the strongest live quark-side result
- up-type lane is bounded on a partition and still open in the `2-3` sector
- the minimal Schur-NNI full-solve support closes the quark magnitudes but not the full CKM CP area
- the bounded projector-ray extension closes the full CKM+CP package numerically with one fixed projector ray, two real sector amplitudes, and one shared phase
- the bounded parameter audit reduces the current missing primitive to one up-sector scalar amplitude law, the widened candidate scan compresses that to a short exact shortlist, the restricted native-expression scan shows that the current exact projector/support grammar still does not force one dominant law, the affine-support scan identifies the `6/7`-centered native family, the provenance audit classifies `7/9` and `sqrt(3/5)` as external empirical baselines, the two-step native scan still preserves the split, and the widened native-affine-support no-go shows that even projector-prefactored affine `delta_A1` laws remain split across the current best refit and anchored baselines
- the broader complex-carrier extension remains as a fallback existence proof
- full quark-spectrum closure is not yet a retained framework claim

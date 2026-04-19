# Quark Up-Amplitude Provenance Audit

**Date:** 2026-04-19  
**Status:** bounded provenance audit for the current reduced quark up-amplitude
shortlist  
**Primary runner:** `scripts/frontier_quark_up_amplitude_provenance_audit.py`

## Safe statement

The current branch still does **not** derive the remaining reduced up-sector
amplitude `a_u`.

But the live shortlist is no longer provenance-blind. On the current
projector/support/tensor note stack, the five leading candidates split cleanly
into four provenance classes:

- `projector-native`
- `support-native`
- `scalar-comparison-native`
- `external empirical`

That is a bounded provenance result, not a retained derivation.

## Provenance rules

The classification uses only the exact structures already promoted in the live
quark notes:

- **Projector-native:** built only from the exact projector-side theorem data
  `delta_std = arctan(sqrt(5))`, `sin(delta_std) = sqrt(5/6)`, and
  `eta = sqrt(5)/6` from `docs/CKM_ATLAS_AXIOM_CLOSURE_NOTE.md:70-74` and
  `docs/CKM_ATLAS_AXIOM_CLOSURE_NOTE.md:121-126`.
- **Support-native:** uses the exact democratic support datum
  `delta_A1(q_dem) = 1/42` or the exact noncentral support fraction `6/7` from
  `docs/CKM_ATLAS_AXIOM_CLOSURE_NOTE.md:78-85`, with the underlying support law
  `delta_A1(r) = 1/(6(1 + sqrt(6) r))` from
  `docs/TENSOR_SUPPORT_CENTER_EXCESS_LAW_NOTE.md:45-60` and
  `docs/S3_TIME_BILINEAR_TENSOR_PRIMITIVE_NOTE.md:36-64`.
- **Scalar-comparison-native:** uses the retained scalar-comparison package
  `rho_scalar = 1/sqrt(42)` from `docs/CKM_ATLAS_AXIOM_CLOSURE_NOTE.md:128-132`.
- **External empirical:** competitive fit candidates introduced only by the
  bounded candidate scans, without promotion in the exact atlas/support/tensor
  notes.

## Candidate audit

### `7/9`

- **Class:** external empirical
- **Why:** it enters the branch only as the best small-rational bounded refit
  candidate in `docs/QUARK_UP_AMPLITUDE_CANDIDATE_SCAN_NOTE_2026-04-19.md:53-74`.
  The same note explicitly says there is no claim that `7/9` is
  framework-forced in `docs/QUARK_UP_AMPLITUDE_CANDIDATE_SCAN_NOTE_2026-04-19.md:145-149`.
  The native-expression note treats it only as an external refit baseline in
  `docs/QUARK_UP_AMPLITUDE_NATIVE_EXPRESSION_SCAN_NOTE_2026-04-19.md:133-149`.
- **Numerical read:** anchored aggregate CKM+`J` deviation `0.835%`; refit max
  full-package deviation `0.908%`.

### `sqrt(3/5)`

- **Class:** external empirical
- **Why:** it enters only as the best small-radical bounded anchored candidate
  in `docs/QUARK_UP_AMPLITUDE_CANDIDATE_SCAN_NOTE_2026-04-19.md:75-101`, and
  the same note again keeps it explicitly non-forced at
  `docs/QUARK_UP_AMPLITUDE_CANDIDATE_SCAN_NOTE_2026-04-19.md:145-149`.
  The native-expression scan uses it only as an external anchored baseline in
  `docs/QUARK_UP_AMPLITUDE_NATIVE_EXPRESSION_SCAN_NOTE_2026-04-19.md:133-149`.
- **Numerical read:** anchored aggregate CKM+`J` deviation `0.720%`; refit max
  full-package deviation `1.047%`.

### `sqrt(5/6) * (6/7)`

- **Class:** support-native
- **Why:** the projector magnitude `sqrt(5/6)` is exact from the `1⊕5`
  projector branch in `docs/CKM_ATLAS_AXIOM_CLOSURE_NOTE.md:70-74`, and the
  dressing `6/7` is the exact democratic noncentral support fraction from
  `docs/CKM_ATLAS_AXIOM_CLOSURE_NOTE.md:78-85`.
  The live native-expression note already identifies this as the cleanest
  structural projector/support instance in
  `docs/QUARK_UP_AMPLITUDE_NATIVE_EXPRESSION_SCAN_NOTE_2026-04-19.md:105-123`.
- **Exact identity:** `6/7 = 1 - 6 delta_A1(q_dem)`.
- **Numerical read:** anchored aggregate CKM+`J` deviation `1.106%`; refit max
  full-package deviation `0.928%`.

### `sqrt(5/6) * (1 - 1/sqrt(42))`

- **Class:** scalar-comparison-native
- **Why:** it uses the same exact projector magnitude `sqrt(5/6)`, but the
  dressing is now the retained scalar-comparison atom
  `rho_scalar = 1/sqrt(42)` from
  `docs/CKM_ATLAS_AXIOM_CLOSURE_NOTE.md:128-132`.
  The candidate scan highlights this as a strong projector/support-native
  dressing in `docs/QUARK_UP_AMPLITUDE_CANDIDATE_SCAN_NOTE_2026-04-19.md:103-124`,
  and the native-expression scan identifies it as the best native anchored law
  in `docs/QUARK_UP_AMPLITUDE_NATIVE_EXPRESSION_SCAN_NOTE_2026-04-19.md:82-103`.
- **Numerical read:** anchored aggregate CKM+`J` deviation `0.742%`; refit max
  full-package deviation `1.159%`.

### `atan(sqrt(5)) - sqrt(5)/6`

- **Class:** projector-native
- **Why:** both atoms are exact projector-side theorem quantities:
  `delta_std = arctan(sqrt(5))` from
  `docs/CKM_ATLAS_AXIOM_CLOSURE_NOTE.md:70-74`, and
  `eta = sqrt(5)/6` from `docs/CKM_ATLAS_AXIOM_CLOSURE_NOTE.md:121-126`.
  The native-expression scan identifies this as the strongest native one-step
  refit law in
  `docs/QUARK_UP_AMPLITUDE_NATIVE_EXPRESSION_SCAN_NOTE_2026-04-19.md:61-80`.
- **Numerical read:** anchored aggregate CKM+`J` deviation `0.827%`; refit max
  full-package deviation `0.917%`.

## Strongest provenance conclusions

The audit now supports four clean statements:

1. `7/9` and `sqrt(3/5)` remain **external empirical baselines**. They are
   strong bounded fits, but they are not sourced by the exact atlas/support
   primitives.
2. `sqrt(5/6) * (6/7)` is the **cleanest support-native law** on the current
   note stack. It is the shortest exact affine dressing of the projector
   magnitude by the democratic support datum.
3. `sqrt(5/6) * (1 - 1/sqrt(42))` is the **strongest scalar-comparison-native
   anchored law** on the current shortlist.
4. `atan(sqrt(5)) - sqrt(5)/6` is the **strongest projector-native refit law**
   on the current shortlist.

What still does **not** change:

- no candidate becomes retained or theorem-forced,
- no candidate outruns both external baselines at once,
- the remaining reduced quark gap is still one non-derived up-sector scalar law.

## Validation

Run:

```bash
python3 scripts/frontier_quark_up_amplitude_provenance_audit.py
```

Current expected result on this branch:

- `frontier_quark_up_amplitude_provenance_audit.py`: `PASS=12 FAIL=0`

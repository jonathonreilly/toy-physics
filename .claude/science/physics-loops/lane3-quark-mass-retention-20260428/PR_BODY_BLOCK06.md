# [physics-loop] Lane 3 quark mass retention block06: open C3 Ward splitter

## Scope

Stacked continuation from block05 for
`lane3-quark-mass-retention-20260428`.

This block attacks Lane 3 target 3C, generation-stratified quark Yukawa Ward
identities. It records an exact support/boundary theorem for the oriented
`C3[111]` source/readout primitive. It does not claim retained non-top quark
masses.

## Artifacts

- `docs/QUARK_C3_ORIENTED_WARD_SPLITTER_SUPPORT_NOTE_2026-04-28.md`
- `scripts/frontier_quark_c3_oriented_ward_splitter_support.py`
- `logs/2026-04-28-quark-c3-oriented-ward-splitter-support.txt`
- loop-pack updates under
  `.claude/science/physics-loops/lane3-quark-mass-retention-20260428/`

## Result

On the retained `hw=1` generation triplet with retained cycle `C = C3[111]`,
every `C3`-equivariant Hermitian Ward endomorphism has form

```text
W(a,b,c) = a I + b(C+C^2) + c(C-C^2)/(i sqrt(3)).
```

The coefficient `c` is reflection-odd. Generic nonzero `c` splits the
block-05 `S_3` `E` doublet into cyclic Fourier channels, while `c=0`
collapses back to the unbroken-`S_3` two-value spectrum. A `C3`-equivariant
readout that is diagonal in the generation basis is scalar.

The artifact therefore supplies exact local support for the missing 3C
source/readout primitive, but leaves the physical source law for `a,b,c` and
the quark-Yukawa readout theorem open.

## Verification

```text
PYTHONPATH=scripts python3 scripts/frontier_quark_c3_oriented_ward_splitter_support.py
TOTAL: PASS=51, FAIL=0

python3 -m py_compile scripts/frontier_quark_c3_oriented_ward_splitter_support.py
PASS

PYTHONPATH=scripts python3 scripts/frontier_quark_generation_equivariant_ward_degeneracy_no_go.py
TOTAL: PASS=44, FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_three_generation_observable_theorem.py
TOTAL: PASS=47, FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_z2_hw1_mass_matrix_parametrization.py
TOTAL: PASS=10, FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_s3_mass_matrix_no_go.py
TOTAL: PASS=13, FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_s3_action_taste_cube_decomposition.py
TOTAL: PASS=57, FAIL=0
```

## Review Disposition

Review-loop emulation found the artifact honest as exact support/boundary for
the 3C source/readout primitive. It excludes observed quark masses, fitted
Yukawa entries, CKM mass-eigenvalue input, endpoint nearest-rational
selectors, and hidden generation projectors.

## Remaining Blockers

- 3C: physical source law for the oriented `C3` coefficient `c` and remaining
  Ward coefficients, or a readout theorem mapping cyclic Fourier strata to
  quark Yukawa channels.
- 3A: non-perturbative `5/6` exponentiation plus threshold-local
  scale-selection / RG-covariant transport theorem.
- 3B: typed source-domain theorem or alternate readout primitive for the
  up-type scalar law.

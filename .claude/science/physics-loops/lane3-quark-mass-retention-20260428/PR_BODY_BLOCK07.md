# [physics-loop] Lane 3 quark mass retention block07: open C3 source boundary

## Scope

Stacked continuation from block06 for
`lane3-quark-mass-retention-20260428`.

This block attacks Lane 3 target 3C, generation-stratified quark Yukawa Ward
identities. It audits whether inherited `C3` circulant hierarchy support and
Koide-style A1/P1 inputs can be imported as a retained quark Ward source law.
It does not claim retained non-top quark masses.

## Artifacts

- `docs/QUARK_C3_CIRCULANT_SOURCE_LAW_BOUNDARY_NOTE_2026-04-28.md`
- `scripts/frontier_quark_c3_circulant_source_law_boundary.py`
- `logs/2026-04-28-quark-c3-circulant-source-law-boundary.txt`
- loop-pack updates under
  `.claude/science/physics-loops/lane3-quark-mass-retention-20260428/`

## Result

On the retained `hw=1` generation triplet with retained cycle `C = C3[111]`,
the Hermitian circulant family

```text
H(a,q) = a I + q C + conjugate(q) C^2
```

is a valid Fourier-basis hierarchy carrier. Without A1/P1 or an equivalent
source/readout theorem it is three-real-dimensional and can fit any real
generation spectrum, so it is not predictive.

With A1 and P1 it supplies the Koide-style relation `Q=2/3` for an amplitude
triple, but still leaves the scale, phase, species assignment, and quark
Yukawa readout open. The artifact therefore retires direct promotion of
inherited `C3` circulant support into retained `m_u`, `m_d`, `m_s`, `m_c`, or
`m_b`.

## Verification

```text
PYTHONPATH=scripts python3 scripts/frontier_quark_c3_circulant_source_law_boundary.py
TOTAL: PASS=43, FAIL=0

python3 -m py_compile scripts/frontier_quark_c3_circulant_source_law_boundary.py
PASS

PYTHONPATH=scripts python3 scripts/frontier_yt_generation_hierarchy_primitive.py
RESULT: PASS=51, FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_yt_class_6_c3_breaking.py
RESULT: PASS=43, FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_koide_circulant_character_bridge.py
PASS=9 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_koide_sqrtm_amplitude_principle.py
PASS=11 FAIL=0
```

## Review Disposition

Review-loop emulation found the artifact honest as exact support/boundary for
a future 3C source-law theorem. It keeps A1/P1 as open imports and excludes
observed quark masses, fitted Yukawa entries, CKM mass inputs,
charged-lepton phase import, and hidden species selectors.

## Remaining Blockers

- 3C: derive A1 or equivalent quark Ward source ratio; derive P1-style
  positive parent/readout for quark Yukawa amplitudes; derive sector-specific
  phases and relative scales.
- 3A: non-perturbative `5/6` exponentiation plus threshold-local
  scale-selection / RG-covariant transport theorem.
- 3B: typed source-domain theorem or alternate readout primitive for the
  up-type scalar law.

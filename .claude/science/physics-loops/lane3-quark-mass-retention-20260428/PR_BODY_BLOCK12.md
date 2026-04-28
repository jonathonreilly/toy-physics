# [physics-loop] Lane 3 quark mass retention block12: RPSR-C3 joint rank boundary

## Summary

Block 12 continues Lane 3 from block 11 and tests the joint 3B/3C rescue
route:

```text
exact RPSR scalar + exact C3[111] Fourier carrier
=> retained up-type ratio pair?
```

The result is negative for direct promotion. The support surfaces are real,
but their combination is still carrier/readout support rather than retained
`m_u/m_c` and `m_c/m_t` closure.

## Artifacts

- `docs/QUARK_RPSR_C3_JOINT_READOUT_RANK_BOUNDARY_NOTE_2026-04-28.md`
- `scripts/frontier_quark_rpsr_c3_joint_readout_rank_boundary.py`
- `logs/2026-04-28-quark-rpsr-c3-joint-readout-rank-boundary.txt`
- loop-pack updates under `.claude/science/physics-loops/lane3-quark-mass-retention-20260428/`

## Result

The exact C3 normal form has Fourier eigenvalues:

```text
lambda_0 = A + 2 B
lambda_+ = A - B + C
lambda_- = A - B - C
```

and represents any ordered normalized ratio triple:

```text
(y_u/y_t, y_c/y_t, 1) = (r_uc r_ct, r_ct, 1).
```

The exact RPSR scalar contributes one scalar. Product and middle-gap
one-scalar identifications each leave a continuum of C3-representable ordered
ratio pairs. Therefore the joint route still needs a C3 coefficient source
law, physical Fourier-channel assignment, two-ratio readout theorem, and
sector/scale bridge.

## Verification

```text
PYTHONPATH=scripts python3 scripts/frontier_quark_rpsr_c3_joint_readout_rank_boundary.py
TOTAL: PASS=87, FAIL=0

python3 -m py_compile scripts/frontier_quark_rpsr_c3_joint_readout_rank_boundary.py
PASS

PYTHONPATH=scripts python3 scripts/frontier_quark_rpsr_single_scalar_readout_underdetermination.py
TOTAL: PASS=80, FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_quark_up_amplitude_rpsr_mass_retention_boundary.py
TOTAL: PASS=50, FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_quark_c3_oriented_ward_splitter_support.py
TOTAL: PASS=51, FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_quark_c3_circulant_source_law_boundary.py
TOTAL: PASS=43, FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_quark_lane3_bounded_companion_retention_firewall.py
PASS=17 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_sm_one_higgs_yukawa_gauge_selection.py
TOTAL: PASS=43, FAIL=0
```

## Honest Claim Status

Lane 3 remains open.

This block closes the shortcut:

```text
RPSR scalar a_u + C3 Fourier carrier
=> retained up-type ratio pair.
```

The next hard residual is a derived source/readout theorem: C3 coefficient
law, Fourier-channel assignment, two-ratio readout, and top-compatible
sector/scale bridge.

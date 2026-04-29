# Physics Loop PR: Lane 3 Quark Mass Retention Block 01

## Summary

This science block keeps Lane 3 open but narrows two direct routes that could
otherwise be overclaimed:

1. 3C direct generation-stratified Ward lift:
   one-Higgs gauge selection + top Ward + retained three-generation structure
   + CKM does not determine non-top quark Yukawa singular values.
2. 3B Route-2 E-channel readout:
   exact Route-2 carrier naturality plus T-side candidates does not derive
   `beta_E/alpha_E = 21/4`; that target is equivalent to the still-unproved
   E-center endpoint ratio `gamma_T(center)/gamma_E(center) = -8/9`.

Honest status: `open` with exact negative boundaries. This PR does not claim
retained `m_u`, `m_d`, `m_s`, `m_c`, or `m_b`.

## Branch

- Head branch: `physics-loop/lane3-quark-mass-retention-block01-20260428`
- Base branch: `main`
- Loop slug: `lane3-quark-mass-retention-20260428`
- Handoff: `.claude/science/physics-loops/lane3-quark-mass-retention-20260428/HANDOFF.md`
- Review history: `.claude/science/physics-loops/lane3-quark-mass-retention-20260428/REVIEW_HISTORY.md`

## Artifacts

- `docs/QUARK_GENERATION_STRATIFIED_WARD_FREE_MATRIX_NO_GO_NOTE_2026-04-28.md`
- `scripts/frontier_quark_generation_stratified_ward_free_matrix_no_go.py`
- `logs/2026-04-28-quark-generation-stratified-ward-free-matrix-no-go.txt`
- `docs/QUARK_ROUTE2_E_CHANNEL_READOUT_NATURALITY_NO_GO_NOTE_2026-04-28.md`
- `scripts/frontier_quark_route2_e_channel_readout_naturality_no_go.py`
- `logs/2026-04-28-quark-route2-e-channel-readout-naturality-no-go.txt`
- loop pack under `.claude/science/physics-loops/lane3-quark-mass-retention-20260428/`

## Verification

```text
python3 scripts/frontier_quark_generation_stratified_ward_free_matrix_no_go.py
TOTAL: PASS=42, FAIL=0

python3 -m py_compile scripts/frontier_quark_generation_stratified_ward_free_matrix_no_go.py
PASS

python3 scripts/frontier_quark_lane3_bounded_companion_retention_firewall.py
PASS=17 FAIL=0

python3 scripts/frontier_quark_mass_ratio_review.py
TOTAL: PASS=46, FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_quark_route2_e_channel_readout_naturality_no_go.py
TOTAL: PASS=28, FAIL=0

python3 -m py_compile scripts/frontier_quark_route2_e_channel_readout_naturality_no_go.py
PASS

PYTHONPATH=scripts python3 scripts/frontier_quark_route2_exact_readout_map.py
PASS=11 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_quark_route2_exact_time_coupling.py
PASS=8 FAIL=0

PYTHONPATH=scripts python3 scripts/frontier_quark_endpoint_ratio_chain_law.py
PASS=14 FAIL=0
```

## Imports Retired Or Exposed

Retired as direct routes:

- CKM closure as non-top quark Yukawa singular-value closure.
- One-Higgs gauge selection as a quark flavor-eigenvalue selector.
- Top Ward normalization as a direct generation-stratified non-top Ward law.
- Route-2 carrier naturality as a selector for `beta_E/alpha_E = 21/4`.

Still exposed:

- down-type GST/NNI theorem-grade bridge;
- non-perturbative `5/6` bridge and threshold-local scale-selection theorem;
- up-type E-center source/readout primitive;
- species-differentiated non-top Yukawa Ward primitive.

## Review Notes

The block deliberately avoids repo-wide weaving. If review accepts these
boundaries, later integration can decide whether to add the two runners to the
canonical harness index and whether to cite the notes from the Lane 3 open-lane
surface.

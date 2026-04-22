# review_imports/ — theorems imported from `origin/review/scalar-selector-cycle1-theorems`

**Purpose**: stages key A1 / Q=2/3 / δ=2/9 theorems from the review
branch on this working branch, so the canonical-branch reviewer can
evaluate the full Koide closure package in one place.

## Contents

### docs/

- `KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md`
  Internal AM-GM chain for A1: Frobenius → projectors → E_+/E_⊥ →
  AM-GM → κ=2 → Q=2/3. Rigorous on admitted Cl(3)/Herm_circ(3) route.
- `KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_2026-04-19.md`
  Bridge identity `a₀²−2|z|² = 3(a²−2|b|²)` — spectrum-side Q=2/3
  equivalent to operator-side κ=2.
- `KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`
  Promoted as primary closure route for operator-side κ=2. Block-total
  Frobenius extremum.
- `KOIDE_Q_DELTA_CLOSURE_PACKAGE_README_2026-04-21.md`
  Review-branch package README covering all Koide rigorous content
  (201 PASS / 0 FAIL on review-branch regression).

### scripts/

Corresponding runners for the above theorems, all verified passing
on this working branch:

| Runner | PASS |
|---|---|
| `frontier_koide_frobenius_isotype_split_uniqueness.py` | SUPPORT_CHAIN=TRUE |
| `frontier_koide_kappa_block_total_frobenius_measure_theorem.py` | 16/16 |
| `frontier_koide_kappa_spectrum_operator_bridge_theorem.py` | 9/9 |
| `frontier_koide_peter_weyl_am_gm.py` | 22/22 |

Verify with:
```bash
for f in review_imports/scripts/*.py; do echo "=== $(basename $f) ==="; python3 "$f" 2>&1 | tail -3; done
```

## Why these are staged here

The review-branch theorems establish the RIGOROUS INTERNAL CHAIN for
A1 via AM-GM on Frobenius-isotype energies. Every step is
axiom-native within the admitted Cl(3)/Herm_circ(3) route.

What remains open (documented in `docs/KOIDE_A1_CLOSURE_RECOMMENDATION_2026-04-22.md`):
the physical source-law bridge showing that the charged-lepton packet
extremizes the block-total functional.

This /loop branch PLUS the review-branch theorems TOGETHER provide
the complete landscape for canonical-branch review and integration.

## For the canonical-branch reviewer

Primary entry points on this branch:
1. `docs/KOIDE_LANE_MASTER_CLOSURE_NOTE.md` — full closure chain
2. `docs/KOIDE_A1_DERIVATION_STATUS_NOTE.md` — A1 landscape
3. `docs/KOIDE_A1_CLOSURE_RECOMMENDATION_2026-04-22.md` — 3 closure routes
4. This directory — review-branch rigorous theorems
5. `docs/KOIDE_A1_LOOP_FINAL_STATUS_2026-04-22.md` — /loop iter summary

Canonical-branch integration options:
- **Route A**: adopt block-total extremum as retained primitive
  (strongest structural evidence via 9 equivalent expressions of 1/2)
- **Route B**: import Koide-Nishiura V(Φ) into EW-scalar lane
- **Route C**: develop novel QFT mechanism (anomaly/topological)

# Koide Review Package — `Q = 2/3` and `δ = 2/9`

**Package:** April 21, 2026 Koide review/support handoff
**Date:** 2026-04-21
**Scope:** Only the charged-lepton Koide relation `Q = 2/3`, the Brannen
phase `δ = 2/9 rad`, and their compatibility identity `Q = 3·δ`.
**Status:** Ready for review as the strongest current executable support
package. Two explicit scientific bridges remain open.

**2026-04-22 support addendum.** The April 22 axiom-native support batch
adds new bridge-targeting tools, selected-line/Fourier bridge diagnostics,
zero-mode / APS support models, and radiative Yukawa support calculations.
These additions strengthen the package materially without changing the open
status of the two physical bridges. See
`docs/KOIDE_AXIOM_NATIVE_SUPPORT_BATCH_NOTE_2026-04-22.md`.

**Executability guarantee.** Every PASS check across the 8 runners is an
actual executable computation: symbolic via sympy, numeric via PDG lepton
masses, or direct structural checks. Totals: **201 PASS / 0 FAIL**.

---

## What this package establishes

This package does two things cleanly:

1. It proves that the admitted block-total Frobenius functional on
   `Herm_circ(3)` is maximized at the Koide point `Q = 2/3`.
2. It proves that the retained `Z_3` orbifold carries an exact ambient APS
   invariant `η = 2/9`, and that this value is topologically robust.

These are strong results. They are not the same as full retained
closure of the physical charged-lepton observables.

---

## The remaining open bridges

### 1. Koide relation `Q = 2/3`

The April 21 Frobenius stack proves where the **admitted** block-total
functional is extremized. What remains open is the physical/source-law bridge:

> why the physical charged-lepton packet must extremize that functional on the
> accepted framework surface.

This is the same residue still named in
`docs/KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`:
the unresolved choice of canonical extremal principle.

### 2. Brannen phase `δ = 2/9`

The April 21 APS stack proves the exact ambient topological number
`η = 2/9`. What remains open is the physical-observable bridge:

> why the physical Brannen phase on the actual selected-line `CP^1` carrier is
> this APS invariant.

This is the same residual postulate sharpened in
`docs/KOIDE_Q_DELTA_LINKING_RELATION_THEOREM_NOTE_2026-04-20.md` and
`docs/KOIDE_P_ONE_CLOCK_3PLUS1_TRANSPORT_REDUCTION_NOTE_2026-04-20.md`.

---

## Koide relation: `Q = 2/3`

### Mechanism

AM-GM inequality on the isotype Frobenius energies of `Herm_circ(3)`.

### What is proved

- Isotype energies are
  `E_+ = (tr M)^2 / 3` and `E_perp = Tr(M^2) - E_+`.
- Under fixed total Frobenius norm `E_+ + E_perp = N`, AM-GM forces the
  unique interior extremum at `E_+ = E_perp`.
- On the charged-lepton carrier that is exactly `kappa = a^2 / |b|^2 = 2`,
  hence `Q = (1 + 2 / kappa) / 3 = 2/3`.

### What this does not yet prove

It does not yet prove that the physical charged-lepton packet is selected by
that extremal principle rather than by another retained natural functional.

### Main runners

- `scripts/frontier_koide_peter_weyl_am_gm.py` — **22/22 PASS**
- `scripts/frontier_koide_frobenius_isotype_split_uniqueness.py` —
  **28/28 PASS**

### Main note

- `docs/KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md`

---

## Brannen phase: `δ = 2/9 rad`

### Mechanism

Atiyah-Bott-Segal-Singer equivariant fixed-point formula for the APS
`η`-invariant on the retained `Z_3` orbifold with tangent weights `(1, 2)`.

### What is proved

- The retained `C_3[111]` rotation fixes the body-diagonal and yields tangent
  weights `(1, 2)` mod `3`.
- The ABSS fixed-point formula gives
  `η = (1/3) * (1/3 + 1/3) = 2/9` exactly.
- The value is topologically robust: it depends on the tangent
  representation, not on the choice of smooth `Z_3`-compatible metric.

### What this does not yet prove

It does not yet prove that the physical Brannen phase on the actual
selected-line `CP^1` carrier equals this ambient APS invariant.

### Main runners

- `scripts/frontier_koide_aps_eta_invariant.py` — **21/21 PASS**
- `scripts/frontier_koide_aps_topological_robustness.py` — **41/41 PASS**
- `scripts/frontier_koide_c3_spatial_rotation.py` — **16/16 PASS**
- `scripts/frontier_koide_aps_block_by_block_forcing.py` — **29/29 PASS**

### Main note

- `docs/KOIDE_APS_BLOCK_BY_BLOCK_FORCING_NOTE_2026-04-21.md`

---

## Compatibility identity

### `Q = 3·δ`

The package also contains an exact arithmetic compatibility identity:

- `Q = 2/d` on the Koide side at `d = 3`
- `δ = 2/p^2` on the APS side at `p = 3`
- the same retained `Z_3` arithmetic gives `p = d = 3`
- therefore `Q = p·δ = 3·δ`

This is best read as an exact compatibility identity between the two support
routes. It does not by itself discharge either remaining physical bridge.

### Runner

- `scripts/frontier_koide_Q_eq_3delta_identity.py` — **10/10 PASS**

### Note

- `docs/KOIDE_Q_EQ_3DELTA_IDENTITY_NOTE_2026-04-21.md`

---

## Reviewer stress-test

### Runner

- `scripts/frontier_koide_reviewer_stress_test.py` — **34/34 PASS**

### What it is good for

The stress-test shows the package has good executable hygiene:

- no placeholder PASS checks
- no hidden dependence on unresolved dynamical-metric details for the ambient
  APS number
- no circular dependence of the AM-GM route on the APS route

### What it is not

It is not a replacement for the two remaining scientific bridges listed
above.

### Note

- `docs/KOIDE_REVIEWER_STRESS_TEST_NOTE_2026-04-21.md`

---

## Full artifact manifest

### Runners

| File | Purpose | PASS |
|---|---|---|
| `frontier_koide_aps_topological_robustness.py` | Brannen support: metric-independence of ambient APS value | 41/41 |
| `frontier_koide_aps_eta_invariant.py` | Brannen support: exact `η = 2/9` by multiple routes | 21/21 |
| `frontier_koide_c3_spatial_rotation.py` | Brannen support: Rodrigues equals cyclic permutation | 16/16 |
| `frontier_koide_aps_block_by_block_forcing.py` | Brannen support: ambient APS forcing chain | 29/29 |
| `frontier_koide_peter_weyl_am_gm.py` | Koide support: AM-GM gives `Q = 2/3` | 22/22 |
| `frontier_koide_frobenius_isotype_split_uniqueness.py` | Koide support: Frobenius-isotype forcing chain | 28/28 |
| `frontier_koide_Q_eq_3delta_identity.py` | compatibility identity `Q = 3·δ` | 10/10 |
| `frontier_koide_reviewer_stress_test.py` | reviewer stress-test | 34/34 |

**Total: 201 PASS, 0 FAIL.**

### Notes

- `docs/KOIDE_APS_BLOCK_BY_BLOCK_FORCING_NOTE_2026-04-21.md`
- `docs/KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md`
- `docs/KOIDE_Q_EQ_3DELTA_IDENTITY_NOTE_2026-04-21.md`
- `docs/KOIDE_REVIEWER_STRESS_TEST_NOTE_2026-04-21.md`

---

## Review order

1. This README.
2. `scripts/frontier_koide_peter_weyl_am_gm.py`.
3. `docs/KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md`.
4. `scripts/frontier_koide_aps_eta_invariant.py`.
5. `docs/KOIDE_APS_BLOCK_BY_BLOCK_FORCING_NOTE_2026-04-21.md`.
6. `docs/KOIDE_Q_EQ_3DELTA_IDENTITY_NOTE_2026-04-21.md`.
7. `docs/KOIDE_REVIEWER_STRESS_TEST_NOTE_2026-04-21.md`.

---

## Bottom line

- `Q = 2/3`: strongest current executable support, not yet retained
  closure.
- `δ = 2/9`: strongest current executable support, not yet retained
  closure.
- `Q = 3·δ`: exact compatibility identity between the two support routes.
- Remaining open behind `Q`: the physical/source-law extremal-principle
  bridge.
- Remaining open behind `δ`: the physical Brannen-phase bridge
  `δ_physical = η_APS`.
- `m_*` / `w/v` remains downstream of the Brannen-phase bridge.

Ready for review as the strongest current Koide support package.

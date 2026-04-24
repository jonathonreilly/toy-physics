# Koide Support Package — `Q = 2/3` and `δ = 2/9`

**Package:** April 21, 2026 Koide support handoff
**Date:** 2026-04-21
**Scope:** Only the charged-lepton Koide relation `Q = 2/3`, the Brannen
phase `δ = 2/9 rad`, and their compatibility identity `Q = 3·δ`.
**Status:** Strongest current executable support package. Two explicit
scientific bridges remain open.

**2026-04-22 support addendum.** The April 22 support work now comes in four
layers. The first adds new bridge-targeting tools, selected-line/Fourier
bridge diagnostics, zero-mode / APS support models, and radiative Yukawa
support calculations. The second adds a Brannen-specific geometry/Dirac
support layer: exact selected-line rotation geometry, octahedral-domain
support, a conditional Route-3 Wilson-line law, and an explicit finite-lattice
`L = 3` Wilson-Dirac illustration of the ambient `2/9` value. The third adds
an explicit Callan-Harvey anomaly-descent candidate on the accepted
physical-lattice reading, isolating the remaining Berry/inflow identification
and exact descent-normalization theorems. The fourth adds an exact
second-order `Q` support batch: first-live readout factorization, a unique
minimal scale-free selector variable on the admitted carrier, an exact reduced
two-block observable law, a normalized effective-action candidate route, and a
no-hidden-source audit that compresses the remaining `Q` gap to one explicit
primitive `K = 0` on the normalized second-order carrier. These additions
strengthen the package materially without changing the open status of the two
physical bridges. See
`docs/KOIDE_AXIOM_NATIVE_SUPPORT_BATCH_NOTE_2026-04-22.md`,
`docs/KOIDE_BRANNEN_GEOMETRY_DIRAC_SUPPORT_NOTE_2026-04-22.md`, and
`docs/KOIDE_BRANNEN_CALLAN_HARVEY_CANDIDATE_NOTE_2026-04-22.md`, and
`docs/KOIDE_Q_SECOND_ORDER_SUPPORT_BATCH_NOTE_2026-04-22.md`.

**2026-04-24 native dimensionless review.** The April 24 native packet does
not promote full retained dimensionless closure.  It sharpens the remaining
work:

- the `Q` bridge is reduced to the physical identification of the
  zero-source source-response readout;
- the `δ` bridge is reduced to deriving the physical Brannen endpoint as the
  whole real nontrivial `Z_3` primitive and deriving the open endpoint readout
  as based/unit-preserving;
- exactness/cohomology, marked relative-cobordism, and finite-Wilson
  selected-eigenline routes do not choose those missing sections;
- the finite-Wilson selected-eigenline audit should be read as a negative
  endpoint-selection diagnostic, not as a new finite-lattice derivation of the
  APS value.

See `docs/KOIDE_NATIVE_DIMENSIONLESS_REVIEW_PACKET_2026-04-24.md`.

**Executability guarantee.** Every PASS check across the runner stack is an
actual executable computation: symbolic via sympy, numeric via PDG lepton
masses, or direct structural checks.  The April 21 core stack reports
**242 PASS / 0 FAIL**; later addenda carry their own runner closeouts.

---

## What this package establishes

This package does two things cleanly:

1. It proves that the admitted block-total Frobenius functional on
   `Herm_circ(3)` is maximized at the Koide point `Q = 2/3`.
2. It proves that the retained `Z_3` orbifold carries an exact ambient APS
   invariant `η = 2/9`, and that this value is topologically robust.

These are strong results. They are not the same as full retained
closure of the physical charged-lepton observables.

The April 22 Brannen addendum sharpens the `δ` lane further, but still at
support grade:

- the selected-line `δ(m)` is now backed by an exact Euclidean rotation
  geometry on the retained first branch;
- the branch span is exactly `π/12 = 2π/|O|` on the cubic/octahedral carrier;
- the same `2/9` value appears on a conditional Route-3 one-clock Wilson-line
  law;
- an explicit finite-lattice `3 × 3 × 3` Wilson-Dirac construction realizes
  per-fixed-site `η = 2/9` at discrete plateaus on the natural 3-generation
  carrier.

These additions materially strengthen the bridge search without changing the
fact that the physical Brannen-phase bridge itself remains open.

The April 22 Callan-Harvey candidate route sharpens that bridge further:

- the per-generation ambient anomaly coefficient on the physical-lattice
  carrier is exactly `2/9`;
- the body-diagonal fixed-site generation carrier supplies a concrete descent
  geometry on the accepted `Cl(3)` on `Z^3` reading;
- but the actual theorem identifying the selected-line Berry phase with that
  descended anomaly object, with exact normalization, remains open.

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

The April 22 second-order support batch sharpens that residue further:

> the remaining open step is exactly why the physical charged-lepton scalar
> readout is the zero-source source-response coefficient on that carrier.

The April 22 `O_h` covariance no-go sharpens the structural side as well:

> the retained affine Hermitian chart is not `O_h`-covariant beyond parity, so
> any genuine `SO(3)` / spin-1 completion route must come from a different
> mechanism rather than inherited cubic-point-group covariance.

### 2. Brannen phase `δ = 2/9`

The April 21 APS stack proves the exact ambient topological number
`η = 2/9`. What remains open is the physical-observable bridge:

> why the physical Brannen endpoint is the whole real nontrivial `Z_3`
> primitive with a based/unit-preserving endpoint readout, rather than an
> unbased rank-one selected-line coordinate.

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
- `scripts/frontier_koide_brannen_route3_geometry_support.py` — **30/30 PASS**
- `scripts/frontier_koide_brannen_dirac_support.py` — **11/11 PASS**

### Main note

- `docs/KOIDE_APS_BLOCK_BY_BLOCK_FORCING_NOTE_2026-04-21.md`
- `docs/KOIDE_BRANNEN_GEOMETRY_DIRAC_SUPPORT_NOTE_2026-04-22.md`
- `docs/KOIDE_BRANNEN_CALLAN_HARVEY_CANDIDATE_NOTE_2026-04-22.md`

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

## Stress-test

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
| `frontier_koide_reviewer_stress_test.py` | stress-test | 34/34 |
| `frontier_koide_brannen_route3_geometry_support.py` | Brannen support: exact selected-line geometry + conditional Route-3 support | 30/30 |
| `frontier_koide_brannen_dirac_support.py` | Brannen support: explicit finite-lattice `L=3` Wilson-Dirac illustration | 11/11 |

**Total: 242 PASS, 0 FAIL.**

### Notes

- `docs/KOIDE_APS_BLOCK_BY_BLOCK_FORCING_NOTE_2026-04-21.md`
- `docs/KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md`
- `docs/KOIDE_Q_EQ_3DELTA_IDENTITY_NOTE_2026-04-21.md`
- `docs/KOIDE_REVIEWER_STRESS_TEST_NOTE_2026-04-21.md`
- `docs/KOIDE_BRANNEN_GEOMETRY_DIRAC_SUPPORT_NOTE_2026-04-22.md`

---

## Review order

1. This README.
2. `scripts/frontier_koide_peter_weyl_am_gm.py`.
3. `docs/KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21.md`.
4. `scripts/frontier_koide_aps_eta_invariant.py`.
5. `docs/KOIDE_APS_BLOCK_BY_BLOCK_FORCING_NOTE_2026-04-21.md`.
6. `docs/KOIDE_Q_EQ_3DELTA_IDENTITY_NOTE_2026-04-21.md`.
7. `docs/KOIDE_REVIEWER_STRESS_TEST_NOTE_2026-04-21.md`.
8. `docs/KOIDE_BRANNEN_GEOMETRY_DIRAC_SUPPORT_NOTE_2026-04-22.md`.

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

This is the strongest current Koide support package.

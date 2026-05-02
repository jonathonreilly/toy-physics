# Affine Imaginary-Slot Invariance Narrow Theorem on Herm(3)

**Date:** 2026-05-02
**Type:** positive_theorem
**Claim scope:** the standalone Hermitian-matrix-algebra identity that the
affine map `H(m, delta, q_+) = H_base + m T_m + delta T_delta + q_+ T_q`,
with the three explicit REAL symmetric 3x3 generators
`{T_m, T_delta, T_q}` defined below, has imaginary-slot entries that are
**independent** of the affine parameters `(m, delta, q_+)`. This is a
fact of pure linear algebra: real-matrix shifts cannot perturb the
imaginary part of any matrix entry. No DM-neutrino source-surface /
half-plane / m-spectator / intrinsic-slot / slot-torsion authority is
consumed.
**Status:** audit pending. Under the scope-aware classification framework,
`effective_status` is computed by the audit pipeline from `audit_status` +
`claim_type` + dependency chain; no author-side tier is asserted in source.
Audit-lane ratification is required before any retained-grade status applies.
**Runner:** [`scripts/frontier_affine_imaginary_slot_invariance_narrow.py`](./../scripts/frontier_affine_imaginary_slot_invariance_narrow.py)
**Authority role:** Pattern A narrow rescope of the load-bearing class-(A)
algebraic core of [`DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16`](DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md).

## Statement

Let `H_base` be any Hermitian 3x3 matrix, and let

```text
T_m     =  [[1, 0, 0], [0, 0, 1], [0, 1, 0]]                              (1)
T_delta =  [[0, -1, 1], [-1, 1, 0], [1, 0, -1]]                           (2)
T_q     =  [[0, 1, 1], [1, 0, 1], [1, 1, 0]]                              (3)
```

be three explicit REAL symmetric 3x3 matrices.

Define the affine map

```text
H(m, delta, q_+)  =  H_base + m T_m + delta T_delta + q_+ T_q,            (4)
```

with real parameters `(m, delta, q_+)`.

**Conclusion (T1).** `T_m, T_delta, T_q` are each real symmetric (Hermitian)
and linearly independent over `R`.

**Conclusion (T2) (trace structure).**

```text
Tr(T_m) = 1, Tr(T_delta) = 0, Tr(T_q) = 0.
Hence Tr(H(m, delta, q_+))  =  Tr(H_base) + m.                            (5)
```

The trace of `H` depends ONLY on `m` (not on `delta` or `q_+`).

**Conclusion (T3) (imaginary-slot invariance).**

```text
Im(H(m, delta, q_+)_{ij})  =  Im(H_base_{ij})                             (6)
```

for all `(i, j)` and all real `(m, delta, q_+)`. The imaginary off-diagonal
entries of `H` are independent of the affine parameters.

**Conclusion (T4) (framework instance).** Specializing to `H_base` with
imaginary slot `(-gamma)` at position `[0, 2]` (i.e. `H_base[0, 2] = real_part - i gamma`),
and to `Tr(H_base) = 0`:

```text
Im(H[0, 2])  =  -gamma  exact  for all (m, delta, q_+),                   (7)
Tr(H)        =  m       exact  for all (delta, q_+).                      (8)
```

## Proof

`(T1)` By inspection: the three matrices are explicitly real and symmetric
(check `T_ij = T_ji` and `T_ij = conjugate(T_ji)` for each). Linear
independence over R: stack the 9-entry flattenings of T_m, T_delta, T_q
as row vectors in R^9; the resulting 3x9 matrix has rank 3 (verified at
exact precision in the runner).

`(T2)` Direct trace sums. `Tr(H) = Tr(H_base) + m * Tr(T_m) + delta *
Tr(T_delta) + q_+ * Tr(T_q) = Tr(H_base) + m * 1 + delta * 0 + q_+ * 0`.

`(T3)` `Im(H_ij) = Im((H_base + m T_m + delta T_delta + q_+ T_q)_ij)
= Im(H_base_ij) + m * Im(T_m_ij) + delta * Im(T_delta_ij) + q_+ * Im(T_q_ij)`.
Since `T_m, T_delta, T_q` are all real, `Im(T_m_ij) = Im(T_delta_ij) =
Im(T_q_ij) = 0` for all `(i, j)`, hence `Im(H_ij) = Im(H_base_ij)`. ∎

## What this claims

- `(T1)`: `T_m, T_delta, T_q` are real symmetric and linearly independent.
- `(T2)`: trace structure as in `(5)`.
- `(T3)`: imaginary-slot invariance as in `(6)`.
- `(T4)`: framework-instance specialization with `Im(H[0, 2]) = -gamma`
  and `Tr(H) = m`.

## What this does NOT claim

- Does **not** identify `(m, delta, q_+)` with any specific physical
  source-surface coordinates.
- Does **not** consume the parent's five upstream authorities (active
  half-plane, m-spectator, intrinsic-slot, slot-torsion-boundary, plus
  the source-surface shift-quotient bundle).
- Does **not** consume any PDG observed value, literature numerical
  comparator, fitted selector, or admitted unit convention.

## Relation to the parent active-affine point-selection note

[`DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16`](DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md)
applies this affine algebra to the live source-oriented sheet, identifying
`(delta, q_+)` as the minimal remaining mainline datum. The DM-side
construction depends on five upstream source-surface theorems, all
currently audited_conditional.

This narrow theorem isolates the underlying Hermitian-matrix algebra
from the DM-side framing. The imaginary-slot invariance + trace
structure can be ratified independently of any DM-neutrino authority.

## Cited dependencies

None. This narrow note has zero ledger dependencies because it states
only elementary Hermitian-matrix algebra on three explicitly given
REAL symmetric 3x3 matrices.

## Forbidden imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed.
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention.
- No same-surface family arguments.

## Validation

Primary runner: [`scripts/frontier_affine_imaginary_slot_invariance_narrow.py`](./../scripts/frontier_affine_imaginary_slot_invariance_narrow.py)
verifies (PASS=24/0):

1. `T_m, T_delta, T_q` are real symmetric (six checks: real entries +
   `T = T^T` for each).
2. `rank({T_m, T_delta, T_q}) = 3` (linearly independent over R).
3. `Tr(T_m) = 1, Tr(T_delta) = 0, Tr(T_q) = 0` exact.
4. `Tr(H) = Tr(H_base) + m` symbolic (depends only on m).
5. `Im(H[i, j]) = Im(H_base[i, j])` exact for all 9 entries.
6. Framework instance `H_base` with `gamma = 1/2`, `E1 = sqrt(8/3)`,
   `E2 = sqrt(8)/3`: `H_base` is Hermitian; `Im(H[0, 2]) = -1/2`
   exact for all `(m, delta, q_+)`; `Tr(H) = m` exact.
7. Parent row's `load_bearing_step_class == 'A'` ledger check.

## Cross-references

- [`DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16`](DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md) —
  parent bundled note that applies this affine algebra to the
  DM-neutrino source-oriented sheet via the source-surface upstream
  authorities.
- [`HALF_PLANE_CHART_EQUIVALENCE_NARROW_THEOREM_NOTE_2026-05-02`](HALF_PLANE_CHART_EQUIVALENCE_NARROW_THEOREM_NOTE_2026-05-02.md) —
  sister Pattern A narrow theorem (cycle 25) carving out the chart
  equivalence on the same source-surface family.

# Anomaly Cancellation Proof-Walk Lattice-Independence Bounded Note

**Date:** 2026-05-08
**Claim type:** bounded_theorem
**Status authority:** source-note proposal only; audit verdict and
effective status are set by the independent audit lane.
**Primary runner:** [`scripts/frontier_anomaly_cancellation_proof_walk_lattice_independence.py`](../scripts/frontier_anomaly_cancellation_proof_walk_lattice_independence.py)

## Claim

The proofs of the four perturbative anomaly cancellation identities

```text
(E1)  Tr[Y]            = 0,
(E2)  Tr[SU(3)^2 Y]    = 0,
(E3)  Tr[Y^3]_LH       = -16/9,
(E4)  Tr[Y^3]          = 0,
```

as packaged in
[`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md)
(Step 1 + Step 2 anomaly table, full content) and
[`LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md`](LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md)
(catalog entries `(C1)`, `(C2)`, `(C3)` for the LH-only contributions),
do not use lattice-action machinery as a load-bearing input. The
proof-walk uses only:

- chiral-content multiplicities;
- the SU(3) Dynkin-index normalization `T(fund) = 1/2`;
- exact rational arithmetic in the anomaly trace evaluations;
- the already admitted electric-charge convention `Q = T_3 + Y/2` with
  `Q(u_R) > 0` (used upstream to fix the SM right-handed hypercharges
  that this note then substitutes into the trace identities).

This is a bounded proof-walk of two existing theorem notes. It does not
add a new axiom, a new repo-wide theory class, or a retained status
claim.

## Proof-Walk

The proof-walk is split into one table per identity. Each row is a
single step in the cited authority note's proof.

### (E1) `Tr[Y] = 0`

Authority: `LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md` (C1)
plus `ANOMALY_FORCES_TIME_THEOREM.md` Step 2 full-content cancellation
under `(Y(u_R), Y(d_R), Y(e_R), Y(nu_R)) = (+4/3, -2/3, -2, 0)`.

| Step in the cited authority note | Load-bearing input | Lattice-action input? |
|---|---|---|
| LH partial trace `6 (1/3) + 2 (-1) = 0` | LH multiplicities `(6, 2)` and LH hypercharges `(+1/3, -1)` | no |
| RH partial trace `-3 (4/3) - 3 (-2/3) - 1 (-2) - 1 (0) = 0` | RH multiplicities `(3, 3, 1, 1)` and RH hypercharges from the cited hypercharge solve | no |
| Full sum `0 + 0 = 0` | exact rational arithmetic | no |

### (E2) `Tr[SU(3)^2 Y] = 0`

Authority: `LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md` (C3)
plus the full-content cancellation in `ANOMALY_FORCES_TIME_THEOREM.md`
Step 2.

Only SU(3)-fundamental fermions contribute; SU(3)-singlets contribute
zero.

| Step in the cited authority note | Load-bearing input | Lattice-action input? |
|---|---|---|
| LH-quark trace `T(3) * 2 * (1/3) = 1/3` | Dynkin index `T(3) = 1/2`, weak-isospin multiplicity `2`, `Y(Q_L) = +1/3` | no |
| RH-quark trace `T(3) * (-(4/3) - (-2/3)) = -1/3` | same Dynkin index, RH-quark singlet weak multiplicity `1`, RH hypercharges from the cited solve | no |
| Full sum `1/3 + (-1/3) = 0` | exact rational arithmetic | no |

### (E3) `Tr[Y^3]_LH = -16/9`

Authority: `LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md` (C2).

| Step in the cited authority note | Load-bearing input | Lattice-action input? |
|---|---|---|
| `Q_L` cubic contribution `6 (1/3)^3 = 2/9` | LH-`Q_L` multiplicity `6`, `Y(Q_L) = +1/3`, cubing | no |
| `L_L` cubic contribution `2 (-1)^3 = -2` | LH-`L_L` multiplicity `2`, `Y(L_L) = -1`, cubing | no |
| LH sum `2/9 - 18/9 = -16/9` | exact rational arithmetic | no |

### (E4) `Tr[Y^3] = 0` (full content)

Authority: `ANOMALY_FORCES_TIME_THEOREM.md` Step 2 full-content
cancellation under `(Y(u_R), Y(d_R), Y(e_R), Y(nu_R)) = (+4/3, -2/3, -2, 0)`.

| Step in the cited authority note | Load-bearing input | Lattice-action input? |
|---|---|---|
| LH cubic partial `Tr[Y^3]_LH = -16/9` | the (E3) result above | no |
| RH cubic partial `-3 (4/3)^3 - 3 (-2/3)^3 - (-2)^3 - 0^3` | RH multiplicities `(3, 3, 1, 1)`, RH hypercharges from the cited solve, cubing | no |
| RH cubic value `-192/27 + 24/27 + 8 = 16/9` | exact rational arithmetic | no |
| Full sum `(-16/9) + (16/9) = 0` | exact rational arithmetic | no |

The checked proof paths do not cite the Wilson plaquette action,
staggered phases, Brillouin-zone labels, link unitaries, lattice scale,
`u_0`, a Monte Carlo measurement, or a fitted observational value.

## Exact Arithmetic Check

The runner repeats the arithmetic in each table above with
`fractions.Fraction` against the structural multiplicities
`(Q_L : 6, L_L : 2, u_R : 3, d_R : 3, e_R : 1, nu_R : 1)` and the SM
hypercharges `(Q_L : +1/3, L_L : -1, u_R : +4/3, d_R : -2/3, e_R : -2,
nu_R : 0)` from the cited hypercharge note. All four identities
evaluate to their stated rationals exactly.

The Dynkin-index normalization `T(3) = 1/2` for the SU(3) fundamental
is the standard textbook choice already retained by the authority
notes; it is a group-theoretic constant, not a lattice-action input.

## Dependencies

- [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md)
  for the Step 1 + Step 2 anomaly table that contains identities
  (E1), (E2), (E4).
- [`LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md`](LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md)
  for the LH-only catalog entries `(C1)` = (E1)_LH, `(C3)` = (E2)_LH,
  and `(C2)` = (E3).
- [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md)
  for the RH hypercharge values `(+4/3, -2/3, -2, 0)` substituted into
  the full-content traces (E1), (E2), (E4).
- [`HYPERCHARGE_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-07.md`](HYPERCHARGE_PROOF_WALK_LATTICE_INDEPENDENCE_BOUNDED_NOTE_2026-05-07.md)
  for the companion bounded proof-walk that the upstream RH hypercharge
  values are themselves obtained without lattice-action machinery.
- [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md)
  and [`HYPERCHARGE_IDENTIFICATION_NOTE.md`](HYPERCHARGE_IDENTIFICATION_NOTE.md)
  for the LH content and charge identification conventions.
- `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`
  and `MINIMAL_AXIOMS_2026-05-03.md`
  for the open realization-gate context that this note does not close.

These are imported authorities for a bounded theorem. The row remains
unaudited until the independent audit lane reviews this note, its
dependencies, and the runner.

## Boundaries

This note does not close:

- the Adler-Bell-Jackiw anomaly-to-inconsistency implication itself,
  which `ANOMALY_FORCES_TIME_THEOREM.md` carries as admission (i) (a
  bare external admission to the standard ABJ result on current `main`,
  per its own audit-prep note); this proof-walk only checks the
  arithmetic identities, not the QFT consistency step that motivates
  imposing them;
- the right-handed completion existence statement (the choice of
  SU(2)-singlet right-handed multiplet structure), which is delegated
  to `NATIVE_GAUGE_CLOSURE_NOTE.md` by `ANOMALY_FORCES_TIME_THEOREM.md`;
- the derivation of the chiral matter content itself;
- the staggered-Dirac realization gate;
- the Witten SU(2) `Z_2` integer count `(C5)` of the LH catalog (a
  separate, integer-count identity);
- the pure-color SU(3)^3 cubic gauge-anomaly cancellation (a separate
  companion note);
- the `B - L` anomaly-freedom closure (a separate companion note);
- the 3+1 spacetime-forcing downstream step in
  `ANOMALY_FORCES_TIME_THEOREM.md` (its Steps 3-5);
- any claim that multiple lattice realizations exist in the framework;
- any continuum-limit numerical claim such as plaquette, mass, or
  coupling values;
- any parent theorem/status promotion.

In particular, this note inherits whatever external admissions the
SOURCE notes already carry; it does not retire admission (i) of
`ANOMALY_FORCES_TIME_THEOREM.md`, and it does not promote any of its
companions.

## Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_anomaly_cancellation_proof_walk_lattice_independence.py
```

Expected:

```text
TOTAL: PASS=N FAIL=0
VERDICT: bounded proof-walk passes; the four anomaly cancellation
identities Tr[Y]=0, Tr[SU(3)^2 Y]=0, Tr[Y^3]_LH = -16/9, and
Tr[Y^3]=0 use no lattice-action quantity as a load-bearing input in
their cited proofs.
```

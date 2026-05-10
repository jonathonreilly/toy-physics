# Tr[Y^2] Proof-Walk Lattice-Independence Bounded Note

**Date:** 2026-05-08
**Claim type:** bounded_theorem
**Status authority:** source-note proposal only; audit verdict and
effective status are set by the independent audit lane.
**Primary runner:** [`scripts/frontier_trYsquared_proof_walk_lattice_independence.py`](../scripts/frontier_trYsquared_proof_walk_lattice_independence.py)

## Claim

Given the existing one-generation chiral-content and hypercharge-assignment
setup used by
[`HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md`](HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md),
the proof of the squared-hypercharge identity

```text
Tr[Y^2]_one_gen = 40/3
```

does not use lattice-action machinery as a load-bearing input. The
proof-walk uses only:

- chiral-content multiplicities;
- the admitted hypercharge assignments
  `Y(Q_L) = +1/3, Y(L_L) = -1, Y(u_R) = +4/3,
   Y(d_R) = -2/3, Y(e_R) = -2, Y(nu_R) = 0`;
- exact rational arithmetic;
- SU(2) and SU(3) Dynkin-index bookkeeping `T(fund) = 1/2` for the
  GUT-consistency cross-check (Y5).

This is a bounded proof-walk of an existing theorem note. It does not
add a new axiom, a new repo-wide theory class, or a retained status
claim.

## Proof-Walk

| Step in the cited Tr[Y^2] catalog note | Load-bearing input | Lattice-action input? |
|---|---|---|
| (Y1) `Tr[Y^2]_LH = 6 (1/3)^2 + 2 (-1)^2 = 8/3` | LH multiplicities and admitted `Y(Q_L), Y(L_L)` | no |
| (Y2) `Tr[Y^2]_RH = 3 (4/3)^2 + 3 (-2/3)^2 + (-2)^2 + 0^2 = 32/3` | RH multiplicities and admitted `Y(u_R), Y(d_R), Y(e_R), Y(nu_R)` | no |
| (Y3) `Tr[Y^2]_one_gen = (Y1) + (Y2) = 40/3` | exact rational addition | no |
| (Y4) `Tr[Y^2]_three_gen = 3 * (Y3) = 40` | three-generation orbit count | no |
| (Y5) `Tr[Y_GUT^2]_three_gen = (3/20) * 40 = 6 = Tr[T_a^2]_SU(2),three_gen = Tr[T_a^2]_SU(3),three_gen` | SU(2) and SU(3) Dynkin-index bookkeeping | no |

The checked proof path does not cite the Wilson plaquette action,
staggered phases, Brillouin-zone labels, link unitaries, lattice scale,
`u_0`, a Monte Carlo measurement, or a fitted observational value.

## Exact Arithmetic Check

The runner repeats the LH, RH, one-generation, three-generation, and
GUT-consistency calculations with `fractions.Fraction` against the
structural multiplicities

```text
mult(Q_L) = 6,  mult(L_L) = 2,
mult(u_R) = 3,  mult(d_R) = 3,
mult(e_R) = 1,  mult(nu_R) = 1,
```

and the admitted hypercharges, reproducing each catalog identity:

```text
(Y1)  6 * (1/3)^2 + 2 * (-1)^2                                     = 8/3
(Y2)  3 * (4/3)^2 + 3 * (-2/3)^2 + 1 * (-2)^2 + 1 * 0^2            = 32/3
(Y3)  (Y1) + (Y2)                                                  = 40/3
(Y4)  3 * (Y3)                                                     = 40
(Y5)  (3/20) * (Y4) = 6  matches  Tr[T_a^2]_SU(2),three_gen = 6
                              =  Tr[T_a^2]_SU(3),three_gen = 6.
```

The SU(2) and SU(3) Dynkin sums in (Y5) use `T(fund) = 1/2` over the
same one-generation multiplicities, scaled by `3` for three generations.

## Dependencies

- [`HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md`](HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md)
  for the catalog theorem being proof-walked.
- [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md)
  for the admitted hypercharge values.
- [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md)
  and [`HYPERCHARGE_IDENTIFICATION_NOTE.md`](HYPERCHARGE_IDENTIFICATION_NOTE.md)
  for the chiral-content and hypercharge-identification conventions.
- [`THREE_GENERATION_STRUCTURE_NOTE.md`](THREE_GENERATION_STRUCTURE_NOTE.md)
  and [`ONE_GENERATION_MATTER_CLOSURE_NOTE.md`](ONE_GENERATION_MATTER_CLOSURE_NOTE.md)
  for the one- and three-generation orbit counts.
- [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md)
  for the companion linear and cubic trace context.
- `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`
  and `MINIMAL_AXIOMS_2026-05-03.md`
  for the open realization-gate context that this note does not close.

These are imported authorities for a bounded theorem. The row remains
unaudited until the independent audit lane reviews this note, its
dependencies, and the runner.

## Boundaries

This note does not close:

- derivation of the chiral matter content itself;
- derivation of the admitted hypercharge values
  (those are imported from the cited uniqueness theorem);
- the staggered-Dirac realization gate;
- any continuum-limit numerical claim such as plaquette, mass, or
  coupling values;
- any one-loop running, threshold matching, or coupling-unification
  prediction (the Y5 GUT-consistency identity is a structural
  squared-trace ratio, not a unification claim);
- any follow-on proof-walk for other algebraic bookkeeping notes;
- any parent theorem/status promotion.

## Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_trYsquared_proof_walk_lattice_independence.py
```

Expected:

```text
TOTAL: PASS=77 FAIL=0
VERDICT: bounded proof-walk passes; the Tr[Y^2] catalog identities use
no lattice-action quantity as a load-bearing input.
```

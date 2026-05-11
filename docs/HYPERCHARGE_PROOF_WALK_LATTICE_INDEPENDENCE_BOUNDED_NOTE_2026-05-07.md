# Hypercharge Proof-Walk Lattice-Independence Bounded Note

**Date:** 2026-05-07
**Claim type:** bounded_theorem
**Status authority:** source-note proposal only; audit verdict and
effective status are set by the independent audit lane.
**Primary runner:** [`scripts/frontier_hypercharge_proof_walk_lattice_independence.py`](../scripts/frontier_hypercharge_proof_walk_lattice_independence.py)

## Claim

Given the existing one-generation chiral-content and anomaly-system
setup used by
[`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md),
the hypercharge uniqueness proof for

```text
Y(Q_L) = +1/3,  Y(L_L) = -1,
Y(u_R) = +4/3,  Y(d_R) = -2/3,  Y(e_R) = -2,  Y(nu_R) = 0
```

does not use lattice-action machinery as a load-bearing input. The
proof-walk uses only:

- chiral-content multiplicities;
- SU(2) and SU(3) Dynkin-index bookkeeping;
- exact rational arithmetic in the anomaly equations;
- the already admitted electric-charge convention `Q = T_3 + Y/2`
  with `Q(u_R) > 0`.

This is a bounded proof-walk of an existing theorem note. It does not
add a new axiom, a new repo-wide theory class, or a retained status
claim.

## Proof-Walk

| Step in the cited hypercharge note | Load-bearing input | Lattice-action input? |
|---|---|---|
| Anomaly traces `Tr[Y]`, `Tr[SU(3)^2Y]`, and cubic equation | matter multiplicities and group indices | no |
| Linear reduction of the anomaly system | exact rational arithmetic | no |
| `Y(nu_R) = 0` substitution | neutral-singlet convention already in the cited surface | no |
| Quadratic solve | discriminant `324 = 18^2` and rational roots | no |
| `Q(u_R) > 0` branch choice | electric-charge sign convention | no |
| Output collection | arithmetic substitution | no |

The checked proof path does not cite the Wilson plaquette action,
staggered phases, Brillouin-zone labels, link unitaries, lattice scale,
`u_0`, a Monte Carlo measurement, or a fitted observational value.

## Exact Arithmetic Check

The reduced anomaly system in the cited hypercharge theorem gives the
quadratic

```text
9 y_1^2 - 6 y_1 - 8 = 0.
```

Its discriminant is `324 = 18^2`, so the two rational roots are
`+4/3` and `-2/3`. The admitted `Q(u_R) > 0` convention selects
`Y(u_R) = +4/3`; then `Y(d_R) = -2/3`, `Y(e_R) = -2`, and
`Y(nu_R) = 0`.

The runner repeats this calculation with `fractions.Fraction` and
checks the chirality-signed anomaly traces using the structural
multiplicities `(6, 2, 3, 3, 1, 1)`.

## Dependencies

- [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md)
  for the hypercharge theorem being proof-walked.
- [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md)
  and [`HYPERCHARGE_IDENTIFICATION_NOTE.md`](HYPERCHARGE_IDENTIFICATION_NOTE.md)
  for the charge-identification conventions.
- [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md)
  and [`LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md`](LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md)
  for the anomaly-trace context.
- `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`
  and `MINIMAL_AXIOMS_2026-05-03.md`
  for the open realization-gate context that this note does not close.

These are imported authorities for a bounded theorem. The row remains
unaudited until the independent audit lane reviews this note, its
dependencies, and the runner.

## Boundaries

This note does not close:

- derivation of the chiral matter content itself;
- the staggered-Dirac realization gate;
- any claim that multiple lattice realizations exist in the framework;
- any continuum-limit numerical claim such as plaquette, mass, or
  coupling values;
- any follow-on proof-walk for other algebraic bookkeeping notes;
- any parent theorem/status promotion.

## Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_hypercharge_proof_walk_lattice_independence.py
```

Expected:

```text
TOTAL: PASS=55 FAIL=0
VERDICT: bounded proof-walk passes; hypercharge uniqueness uses no
lattice-action quantity as a load-bearing input.
```

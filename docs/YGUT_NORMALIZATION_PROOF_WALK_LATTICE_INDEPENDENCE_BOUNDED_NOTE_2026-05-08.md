# Y_GUT Normalization Proof-Walk Lattice-Independence Bounded Note

**Date:** 2026-05-08
**Claim type:** bounded_theorem
**Status authority:** source-note proposal only; audit verdict and
effective status are set by the independent audit lane.
**Primary runner:** [`scripts/frontier_ygut_normalization_proof_walk_lattice_independence.py`](../scripts/frontier_ygut_normalization_proof_walk_lattice_independence.py)

## Claim

Given the existing one-generation chiral content, the squared-trace
catalog identity (Y5)
`Tr[Y_GUT^2]_three_gen = Tr[T_a^2]_SU(2),three_gen = Tr[T_a^2]_SU(3),three_gen = 6`
of
[`HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md`](HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md),
the LH-form `5̄ ⊕ 10 ⊕ 1` slot match (★) of
[`SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md`](SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md),
and the standard SU(N) Killing-form normalization convention
`Tr[T_a T_b]_fund = (1/2) δ_{ab}` (the same Dynkin-index convention
already used by the retained anomaly notes), the proof that

```text
Y_GUT  =  √(3/5) · Y_min     (equivalently  Y_GUT^2  =  (3/20) · Y^2)
```

holds (per the trace consistency in
[`HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md`](HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md)
(Y5) and as used in cycles 16/19) does not use lattice-action
machinery as a load-bearing input; it is determined by trace
identities and the standard Lie-algebra Killing-form normalization
convention. The proof-walk uses only:

- the LH-form chirality table (16 chiralities per generation) imported
  from the cited SU(5) embedding-consistency theorem;
- the squared-hypercharge trace identities (Y1)–(Y5) imported from
  the cited squared-trace catalog;
- SU(N) Dynkin-index bookkeeping under the standard Lie-algebra Killing-form normalization convention (`Tr[T_a T_b]_fund = (1/2) δ_{ab}`);
- exact rational arithmetic in the trace-consistency equation.

This is a bounded proof-walk of an existing theorem block. It does not
add a new axiom, a new repo-wide theory class, or a retained status
claim.

## Proof-Walk

| Step in the cited Y_GUT normalization block | Load-bearing input | Lattice-action input? |
|---|---|---|
| LH-form transcription of one-generation content (16 chiralities) | conjugation rule and chiral-content multiplicities | no |
| Slot-by-slot match into `5̄ ⊕ 10 ⊕ 1` | SU(5) representation branchings | no |
| Per-Weyl-family squared-hypercharge trace `Tr[Y_min^2]_5̄+10 = 10/3` | exact rational arithmetic | no |
| Per-Weyl-family Dynkin sum `Tr[T_a^2]_5̄+10 = T(5̄) + T(10) = 1/2 + 3/2 = 2` | SU(N) Dynkin-index bookkeeping under the standard Killing-form normalization convention `Tr[T_a T_b]_fund = (1/2) δ_{ab}` | no |
| Trace-consistency equation `Tr[Y_GUT^2]_5̄+10 = Tr[T_a^2]_5̄+10` | trace identity | no |
| Solve `c^2 · 10/3 = 2` for the rescaling factor | exact rational arithmetic | no |
| Output `c^2 = 3/5`, `c = √(3/5)` | arithmetic substitution | no |
| Three-generation lift `Tr[Y_GUT^2]_three_gen = 3 · 2 = 6` matching (Y5) | identical hypercharges per generation | no |

The checked proof path does not cite the Wilson plaquette action,
staggered phases, Brillouin-zone labels, link unitaries, lattice scale,
`u_0`, a Monte Carlo measurement, or a fitted observational value.

## Exact Arithmetic Check

In the doubled convention used throughout the retained anomaly notes
(`Q = T_3 + Y/2`), the LHCM-derived hypercharges per Weyl family in
the LH-form `5̄ ⊕ 10` give

```text
Tr[Y_min^2]_5̄  = 3 · (1/3)^2 + 2 · (1/2)^2  = 1/3 + 1/2  = 5/6,
Tr[Y_min^2]_10 = 3 · (2/3)^2 + 6 · (1/6)^2 + 1 · (1)^2
              = 4/3 + 1/6 + 1
              = 8/6 + 1/6 + 6/6
              = 15/6
              = 5/2,
Tr[Y_min^2]_5̄+10 = 5/6 + 5/2 = 5/6 + 15/6 = 20/6 = 10/3.
```

The Dynkin-index sum on the same content under the standard SU(N)
Killing-form normalization convention `Tr[T_a T_b]_fund = (1/2) δ_{ab}`
gives `T(5̄) = 1/2` and `T(10) = 3/2`, so

```text
Tr[T_a^2]_5̄+10 = 1/2 + 3/2 = 2.
```

The trace-consistency equation `Tr[Y_GUT^2]_5̄+10 = Tr[T_a^2]_5̄+10`
with rescaling `Y_GUT = c · Y_min` becomes

```text
c^2 · 10/3 = 2     ⇔     c^2 = 6/10 = 3/5.
```

Hence `c = √(3/5)`, equivalently `Y_GUT^2 = (3/5) · Y_min^2`, or
`Y_GUT^2 = (3/20) · Y^2` in the doubled convention. The
three-generation lift `Tr[Y_GUT^2]_three_gen = 3 · 2 = 6` then
matches identity (Y5) of the cited squared-trace catalog
(`Tr[Y_GUT^2]_three_gen = Tr[T_a^2]_SU(2),three_gen
= Tr[T_a^2]_SU(3),three_gen = 6`).

The runner repeats this calculation with `fractions.Fraction` and
checks every per-rep squared trace, the Dynkin-index sum, and the
solve `c^2 = 3/5` at exact rational precision.

## Dependencies

- [`HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md`](HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md)
  for identity (Y5) `Tr[Y_GUT^2]_three_gen = 6` and the squared-trace
  catalog (Y1)–(Y4).
- [`SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md`](SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md)
  for the LH-form `5̄ ⊕ 10 ⊕ 1` slot match (★) and the trace-forced
  derivation block (✧) being proof-walked here.
- [`FULL_Y_SQUARED_TRACE_SU5_GUT_NOTE_2026-05-02.md`](FULL_Y_SQUARED_TRACE_SU5_GUT_NOTE_2026-05-02.md)
  for the cycle 16 surface that uses the same `Y_GUT` rescaling.
- [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md)
  for the RH hypercharge values used in the LH-form transcription.
- [`HYPERCHARGE_IDENTIFICATION_NOTE.md`](HYPERCHARGE_IDENTIFICATION_NOTE.md)
  and
  [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md)
  for the LH content and graph-first U(1)_Y identification used by the
  upstream embedding theorem.
- `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`
  and
  `MINIMAL_AXIOMS_2026-05-03.md`
  for the open realization-gate context that this note does not close.

These are imported authorities for a bounded theorem. The row remains
unaudited until the independent audit lane reviews this note, its
dependencies, and the runner.

## Boundaries

This note does not close:

- derivation of the chiral matter content itself;
- the staggered-Dirac realization gate;
- any claim that multiple lattice realizations exist in the framework;
- any one-loop running, threshold matching, or coupling-unification
  prediction;
- minimality of SU(5) (vs. SO(10), E6, …) as the GUT group;
- any GUT-scale derivation or proton-decay claim;
- any continuum-limit numerical claim such as plaquette, mass, or
  coupling values;
- any follow-on proof-walk for other algebraic bookkeeping notes;
- any parent theorem/status promotion.

## Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_ygut_normalization_proof_walk_lattice_independence.py
```

Expected:

```text
TOTAL: PASS=N FAIL=0
VERDICT: bounded proof-walk passes; Y_GUT = √(3/5) · Y_min uses no
lattice-action quantity as a load-bearing input.
```

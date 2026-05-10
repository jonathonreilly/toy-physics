# SU(5) 5̄ ⊕ 10 ⊕ 1 Decomposition Proof-Walk Lattice-Independence Bounded Note

**Date:** 2026-05-08
**Claim type:** bounded_theorem
**Status authority:** source-note proposal only; audit verdict and
effective status are set by the independent audit lane.
**Primary runner:** [`scripts/frontier_su5_decomposition_proof_walk_lattice_independence.py`](../scripts/frontier_su5_decomposition_proof_walk_lattice_independence.py)

## Claim

Given the existing one-generation chiral-content setup used by
[`SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md`](SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md),
the proof that the LHCM 16-chirality matter content per generation
matches uniquely into the SU(5) decomposition

```text
5̄  ⊕  10  ⊕  1
```

(per the slot-matching argument used in the cycle 16 / cycle 19 source
notes) does not use lattice-action machinery as a load-bearing input.
The proof-walk uses only:

- chiral-content multiplicities and `(SU(3), SU(2))` representation
  labels;
- the LHCM-derived hypercharge values `Y_min` per chirality;
- standard SU(5) representation theory (Schur lemma + `∧²(5)` tensor
  decomposition) treated as ordinary mathematical machinery;
- exact rational arithmetic for the `Y_min` matching;
- the standard `5 = 3 ⊕ 2` block embedding `SU(3) × SU(2) ⊂ SU(5)`
  on the defining representation.

This is a bounded proof-walk of an existing theorem note. It does not
add a new axiom, a new repo-wide theory class, or a retained status
claim.

## Proof-Walk

The slot-matching identity from the cited SU(5) embedding note is

| LHCM chirality | (SU(3), SU(2), Y_min) | SU(5) slot |
|---|---|---|
| `Q_L`   | `(3,  2, +1/6)`   | `10 ⊃ (3, 2)_{+1/6}` |
| `u^c_L` | `(3̄, 1, −2/3)`  | `10 ⊃ (3̄, 1)_{−2/3}` |
| `e^c_L` | `(1,  1, +1)`     | `10 ⊃ (1, 1)_{+1}` |
| `d^c_L` | `(3̄, 1, +1/3)`  | `5̄ ⊃ (3̄, 1)_{+1/3}` |
| `L_L`   | `(1,  2, −1/2)`   | `5̄ ⊃ (1, 2)_{−1/2}` |
| `ν^c_L` | `(1,  1, 0)`      | `1` |

The proof-walk row catalogue:

| Step in the cited SU(5) embedding note | Load-bearing input | Lattice-action input? |
|---|---|---|
| LH-form transcription (RH → LH conjugate) | LHCM hypercharges + sign flip on additive quantum numbers | no |
| `Y_min = Y/2` rescaling (doubled → minimal Y convention) | electric-charge convention `Q = T_3 + Y/2` already in the cited surface | no |
| `5 = (3,1) ⊕ (1,2)` branching | manifest `3 ⊕ 2` block embedding `SU(3) × SU(2) ⊂ SU(5)` on defining rep | no |
| `5̄ = (3̄,1) ⊕ (1,2)` branching | complex conjugation of `5` | no |
| `10 = ∧²(5)` branching into `(3̄,1) ⊕ (3,2) ⊕ (1,1)` | antisymmetric tensor decomposition (`∧²(3) = 3̄`, `∧²(2) = 1`, `(3,1) ⊗ (1,2) = (3,2)`) | no |
| `1 = (1,1)_0` slot | trivial irrep of SU(5) | no |
| `Y_min` eigenvalue assignment per slot | unique traceless diagonal SU(5) Cartan generator commuting with `su(3) ⊕ su(2)` (Schur lemma + tracelessness) | no |
| Slot-by-slot `(SU(3), SU(2), Y_min)` triple match | label equality on triples + exact rational arithmetic | no |
| `Q_L → 10` slot match | `(3, 2, +1/6)` triple equality | no |
| `u^c_L → 10` slot match | `(3̄, 1, −2/3)` triple equality | no |
| `e^c_L → 10` slot match | `(1, 1, +1)` triple equality | no |
| `d^c_L → 5̄` slot match | `(3̄, 1, +1/3)` triple equality | no |
| `L_L → 5̄` slot match | `(1, 2, −1/2)` triple equality | no |
| `ν^c_L → 1` slot match | `(1, 1, 0)` triple equality | no |
| State-count bookkeeping `|5̄| + |10| + |1| = 16` | `5 + 10 + 1 = 16 = |LH content|` | no |

The checked proof path does not cite the Wilson plaquette action,
staggered phases, Brillouin-zone labels, link unitaries, lattice scale,
`u_0`, a Monte Carlo measurement, or a fitted observational value.

## Exact Arithmetic Check

The LH-form one-generation content per generation has 16 chiralities
with `(SU(3), SU(2), Y_min)` labels:

```text
Q_L      : (3,  2, +1/6)   6 states
u^c_L    : (3̄, 1, −2/3)  3 states
d^c_L    : (3̄, 1, +1/3)  3 states
L_L      : (1,  2, −1/2)  2 states
e^c_L    : (1,  1, +1)    1 state
ν^c_L    : (1,  1, 0)     1 state
                          ----------
                          16 states / generation.
```

The standard SU(5) branchings (from `5 = (3,1)_{−1/3} ⊕ (1,2)_{+1/2}`
under the manifest `3 ⊕ 2` block embedding plus tracelessness fixing
`Y_min(3,1) = −1/3` and `Y_min(1,2) = +1/2`) give

```text
5̄  =  (3̄, 1)_{+1/3}  ⊕  (1, 2)_{−1/2},
10 =  ∧²(5)
    =  (3̄, 1)_{−2/3}  ⊕  (3, 2)_{+1/6}  ⊕  (1, 1)_{+1},
1  =  (1, 1)_0.
```

State counts: `|5̄| = 3 + 2 = 5`, `|10| = 3 + 6 + 1 = 10`, `|1| = 1`,
total `5 + 10 + 1 = 16`. The bijection between LHCM chiralities and
SU(5) slots holds at the level of `(SU(3), SU(2), Y_min)` triples
under exact `Fraction` equality.

The runner repeats this slot-matching with `fractions.Fraction` for
the `Y_min` values, checks the six chirality classes against the six
SU(5) slots, and confirms the state-count identity `5 + 10 + 1 = 16`.

## Dependencies

- [`SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md`](SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md)
  for the SU(5) embedding theorem being proof-walked, including the
  slot-matching identity (★) and the `5̄ ⊕ 10 ⊕ 1` decomposition.
- [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md)
  for the RH hypercharge values used in the LH-form transcription.
- [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md)
  and [`HYPERCHARGE_IDENTIFICATION_NOTE.md`](HYPERCHARGE_IDENTIFICATION_NOTE.md)
  for the LH chirality `(SU(3), SU(2), Y)` labels and graph-first
  U(1)_Y identification.
- [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md)
  for the graph-first SU(3) commutant context.
- [`THREE_GENERATION_STRUCTURE_NOTE.md`](THREE_GENERATION_STRUCTURE_NOTE.md)
  for the three-generation orbit algebra (per-generation copies).
- [`FULL_Y_SQUARED_TRACE_SU5_GUT_NOTE_2026-05-02.md`](FULL_Y_SQUARED_TRACE_SU5_GUT_NOTE_2026-05-02.md)
  for the cycle 16 trace identity that surfaces the same slot-matching.
- `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`
  and `MINIMAL_AXIOMS_2026-05-03.md`
  for the open realization-gate context that this note does not close.

These are imported authorities for a bounded theorem. Standard SU(5)
representation theory (Schur lemma, antisymmetric tensor decomposition,
the `5 = 3 ⊕ 2` block embedding on the defining rep) is cited as
ordinary mathematical machinery rather than as a framework-specific
import; references such as Georgi–Glashow (1974) and Slansky (1981)
suffice. The row remains unaudited until the independent audit lane
reviews this note, its dependencies, and the runner.

## Boundaries

This note does not close:

- derivation of the chiral matter content itself;
- derivation of the LHCM hypercharge values themselves (those come
  from the cited hypercharge uniqueness theorem and LHCM atlas);
- the staggered-Dirac realization gate;
- the hypercharge-generator embedding `T_24 ∝ diag(−2,−2,−2,+3,+3)`
  (covered in §4.4 of the cited SU(5) embedding note);
- the GUT trace consistency `Y_GUT = √(3/5) · Y_min` (covered in §4.5
  of the cited SU(5) embedding note);
- SU(5) minimality among admissible GUT groups (the same matter
  content fits 16 of SO(10), per §2 of the cited note);
- coupling unification, GUT scale, or proton decay;
- any continuum-limit numerical claim such as plaquette, mass, or
  coupling values;
- any follow-on proof-walk for other algebraic bookkeeping notes;
- any parent theorem/status promotion.

## Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_su5_decomposition_proof_walk_lattice_independence.py
```

Expected:

```text
TOTAL: PASS=N FAIL=0
VERDICT: bounded proof-walk passes; SU(5) 5̄ ⊕ 10 ⊕ 1 slot-matching
uses no lattice-action quantity as a load-bearing input.
```

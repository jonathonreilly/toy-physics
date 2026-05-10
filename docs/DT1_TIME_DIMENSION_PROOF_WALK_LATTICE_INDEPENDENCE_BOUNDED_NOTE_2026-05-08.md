# Time-Dimension d_t = 1 Proof-Walk Lattice-Independence Bounded Note

**Date:** 2026-05-08
**Claim type:** bounded_theorem
**Proposal allowed:** false
**Status authority:** source-note proposal only; audit verdict and
effective status are set by the independent audit lane.
**Primary runner:** [`scripts/frontier_dt1_time_dimension_proof_walk_lattice_independence.py`](../scripts/frontier_dt1_time_dimension_proof_walk_lattice_independence.py)

## Claim

Given the existing one-generation chiral-content, anomaly-system, and
single-clock codimension-1 evolution structure used by
[`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md),
the proof that anomaly cancellation forces the temporal dimension

```text
d_t = 1
```

(the time / chirality piece of the 3+1 spacetime claim) does not use
lattice-action machinery as a load-bearing input. The proof-walk uses
only:

- chiral-content multiplicities;
- SU(2) and SU(3) Dynkin-index bookkeeping in the anomaly traces;
- exact rational arithmetic in the anomaly equations;
- the Clifford-algebra classification of the volume-element parity;
- the cited Clifford-volume / sublattice-parity chirality grading;
- the cited single-clock codimension-1 evolution structure.

This is a bounded proof-walk of an existing theorem note. It does not
add a new axiom, a new repo-wide theory class, or a retained status
claim. It does not propose a status promotion.

## Boundaries

This note does not close:

- the spatial dimension `d_s = 3`. **`d_s = 3` is given directly by the
  framework axiom A2 (`Z^3` substrate) per
  `MINIMAL_AXIOMS_2026-05-03.md`. It is
  NOT derived from a proof-walk in this note and NOT derived from
  anomaly cancellation in
  [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md).**
  The narrow proof-walked claim here is the temporal piece `d_t = 1`
  only;
- the bare external ABJ anomaly-to-inconsistency admission (i) of
  [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md).
  This admission is inherited as-is from the source note: the proposed
  internal companion (PR 402, lattice Wess--Zumino / Fujikawa `Z^4`
  theorem) was closed without merge and the cited file does not exist
  on `main`;
- the staggered-Dirac realization gate;
- any claim that multiple lattice realizations exist in the framework;
- any continuum-limit numerical claim such as plaquette, mass, or
  coupling values;
- any follow-on proof-walk for other algebraic bookkeeping notes;
- any parent theorem/status promotion. The cited single-clock
  codimension-1 evolution theorem and the Clifford-volume / sublattice-
  parity chirality grading are both proposed_retained (audit-pending)
  on `main`; this note treats them as black boxes and does not
  re-derive them or propose their promotion.

## Proof-Walk

The chain that forces `d_t = 1` lives in Steps 2--4 of the source
theorem note. Step 1 (anomaly trace evaluation) and Step 5 (final
combine) are listed for completeness; they do not introduce additional
load-bearing inputs beyond those already named.

| Step in the cited time theorem | Load-bearing input | Lattice-action input? |
|---|---|---|
| Step 1: left-handed anomaly traces `Tr[Y]`, `Tr[Y^3]`, `Tr[SU(3)^2 Y]`, `Tr[SU(2)^2 Y]` | matter multiplicities `(6, 2, 3, 3, 1, 1)` and Dynkin indices `T(fund) = 1/2` | no |
| Step 1: ABJ anomaly-to-inconsistency implication | bare external admission (i) inherited as-is from the source note | no |
| Step 2: opposite-chirality SU(2)-singlet completion exists | bare cancellation requirement plus the cited Clifford-volume / sublattice-parity chirality grading from [`CPT_EXACT_NOTE.md`](CPT_EXACT_NOTE.md) | no |
| Step 3: chirality operator `gamma_5` requires even total spacetime dimension | Clifford-algebra classification of `omega = gamma_1 ... gamma_n` | no |
| Step 3: combine with `d_s = 3` from A2 substrate axiom | axiom A2 input (substrate-axiom input, not derived here) | no |
| Step 3 conclusion: `d_t` must be odd, `d_t in {1, 3, 5, ...}` | exact integer parity of `d_s + d_t` | no |
| Step 4: single-clock codimension-1 evolution excludes `d_t > 1` | cited [`AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md`](AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md) (proposed_retained, audit-pending) | no |
| Step 5: combine Steps 2--4 to conclude `d_t = 1` | output collection | no |

The checked proof path does not cite the Wilson plaquette action,
staggered phases, Brillouin-zone labels, link unitaries, lattice scale,
`u_0`, a Monte Carlo measurement, or a fitted observational value.

## Exact Arithmetic Check

The runner reproduces the source-note algebraic facts that feed
Steps 1--4 with `fractions.Fraction`:

- the LH-anomaly traces using the structural multiplicities
  `(6, 2)` and Dynkin index `1/2`:

  ```text
  Tr[Y]_LH         = 0
  Tr[SU(2)^2 Y]_LH = 0
  Tr[SU(3)^2 Y]_LH = 1/3
  Tr[Y^3]_LH       = -16/9
  ```

  The two nonzero traces are exactly the inconsistency that drives
  Steps 2--4;

- the standard-model hypercharge assignment that satisfies anomaly
  cancellation after the Step 2 SU(2)-singlet completion:

  ```text
  Y(Q_L) = +1/3,  Y(L_L) = -1,
  Y(u_R) = +4/3,  Y(d_R) = -2/3,  Y(e_R) = -2,  Y(nu_R) = 0
  ```

  with `Tr[Y] = 0`, `Tr[SU(3)^2 Y] = 0`, `Tr[Y^3] = 0` for the full
  spectrum;

- the integer parity check that drives Step 3: for `d_s = 3` (A2
  input), `d_s + d_t` is even iff `d_t` is odd;

- the Clifford volume-element commutation rule
  `omega gamma_mu = (-1)^(n-1) gamma_mu omega`, which is central
  (commutes) for `n` odd and anticommutes for `n` even, so a chirality
  operator that anticommutes with all `gamma_mu` exists only for
  even `n`;

- the explicit enumeration of `d_t in {0, 1, 2, 3, 4, 5}` against the
  three constraints (chirality grading, parity, single-clock
  codimension-1 exclusion of `d_t > 1`), confirming `d_t = 1` is the
  unique satisfying value.

## Dependencies

- [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md)
  for the time theorem being proof-walked.
- [`CPT_EXACT_NOTE.md`](CPT_EXACT_NOTE.md)
  for the Clifford-volume / sublattice-parity chirality grading
  `epsilon(x) = staggered gamma_5` cited at Steps 2 and 3 of the
  source note.
- [`AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md`](AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md)
  for the single-clock codimension-1 evolution structure cited at
  Step 4 of the source note.
- [`NATIVE_GAUGE_CLOSURE_NOTE.md`](NATIVE_GAUGE_CLOSURE_NOTE.md)
  for the chiral-content origin used at Steps 1 and 2 of the source
  note.
- [`LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md`](LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md)
  for the LH-anomaly-trace bookkeeping.
- `MINIMAL_AXIOMS_2026-05-03.md`
  for the framework axiom A2 (`Z^3` spatial substrate) that supplies
  `d_s = 3` directly.
- `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`
  for the open realization-gate context that this note does not close.

These are imported authorities for a bounded theorem. The row remains
unaudited until the independent audit lane reviews this note, its
dependencies, and the runner.

## Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_dt1_time_dimension_proof_walk_lattice_independence.py
```

Expected:

```text
TOTAL: PASS=N FAIL=0
VERDICT: bounded proof-walk passes; the time-dimension forcing chain
that gives d_t = 1 uses no lattice-action quantity as a load-bearing
input.
```

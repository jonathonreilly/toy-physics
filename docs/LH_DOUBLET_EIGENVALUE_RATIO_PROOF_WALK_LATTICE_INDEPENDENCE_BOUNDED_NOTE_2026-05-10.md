# LH-Doublet Eigenvalue Ratio Proof-Walk Lattice-Independence Bounded Note

**Date:** 2026-05-10
**Claim type:** bounded_theorem
**Status authority:** source-note proposal only; audit verdict and
effective status are set by the independent audit lane.
**Primary runner:** [`scripts/frontier_lh_doublet_eigenvalue_ratio_proof_walk_lattice_independence.py`](../scripts/frontier_lh_doublet_eigenvalue_ratio_proof_walk_lattice_independence.py)

## Claim

Given the existing graph-first commutant setup used by
[`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md),
the structural eigenvalue ratio result

```text
Sym²(C²) : Anti²(C²)  =  1 : (-3)
```

on the 6-state Sym² and 2-state Anti² LH-doublet sub-decompositions —
proof-walked from
[`LH_DOUBLET_TRACELESS_ABELIAN_EIGENVALUE_RATIO_NARROW_THEOREM_NOTE_2026-05-02.md`](LH_DOUBLET_TRACELESS_ABELIAN_EIGENVALUE_RATIO_NARROW_THEOREM_NOTE_2026-05-02.md) —
does not use staggered-Dirac realization machinery as a load-bearing
input. The proof-walk uses only:

- the 6 and 2 multiplicities of the Sym² and Anti² blocks supplied by
  the graph-first integration note;
- the tracelessness condition `6α + 2β = 0` on the unique traceless
  abelian generator;
- exact rational arithmetic to solve the linear constraint.

This is a bounded proof-walk of an existing narrow theorem note. It does
not add a new axiom, a new repo-wide theory class, or a retained status
claim. It does not derive the Sym²/Anti² multiplicities, identify the
ratio with Standard Model hypercharge, choose a normalization, or close
the staggered-Dirac realization gate.

## Proof-Walk

The narrow ratio theorem's load-bearing chain is

```text
Step 1.  Sym² multiplicity = 6  (graph-first integration note: 3 axes × 2 weak-doublet states)
Step 2.  Anti² multiplicity = 2  (graph-first integration note: 1 axis × 2 weak-doublet states)
Step 3.  Tracelessness over the LH-doublet sector: 6α + 2β = 0.
Step 4.  Linear solve: β = -3α.
Step 5.  Ratio: α : β = 1 : (-3).
```

The checked proof path uses exactly five steps and the following inputs:

| Step in the cited narrow theorem note | Load-bearing input | Lattice-action input? | Staggered-Dirac realization input? |
|---|---|---|---|
| Sym² multiplicity = 6 | graph-first integration note (retained-bounded) | no | no |
| Anti² multiplicity = 2 | graph-first integration note (retained-bounded) | no | no |
| Tracelessness `6α + 2β = 0` | unique traceless abelian generator on the 8-state LH-doublet sector | no | no |
| Linear solve `β = -3α` | exact rational arithmetic | no | no |
| Ratio `1 : (-3)` | exact rational arithmetic | no | no |

The checked proof path does not cite the Wilson plaquette action,
staggered phases, Brillouin-zone labels, link unitaries, lattice scale,
`u_0`, a Monte Carlo measurement, a fitted observational value, the
Kawamoto-Smit phase form, BZ-corner doublers, the hw=1 corner triplet,
fermion-number operators, fermion correlators, fermion bilinears, or
any other staggered-Dirac realization quantity.

## Exact Arithmetic Check

The 6 + 2 multiplicities are read off the graph-first integration note's
Step 3 (the residual swap `τ` of the complementary axes splits the 4-
point base as `3 ⊕ 1`, which lifts to Sym² with rank 6 and Anti² with
rank 2 on the LH-doublet sector). The tracelessness equation

```text
6α + 2β = 0
```

is the trace condition for the unique traceless abelian generator over
the LH-doublet sub-decomposition (the alternative would have nonzero
trace, contradicting the traceless generator scope). Linear solve gives

```text
β = -(6/2) α = -3α
⇒  ratio  α : β  =  1 : (-3).
```

Independence-from-scale is also exact: the ratio `β/α = -3` holds for
every nonzero rational `α` (verified in the runner for several
representative choices including `α ∈ {1, 2, -5, 7/11, -3/17, 100}`).

The runner repeats this with `fractions.Fraction` and confirms the
ratio at exact rational precision.

## Why the load-bearing chain does not consume the realization gate

The audit verdict on the narrow theorem note (audited_conditional) was
explicit:

> "The load-bearing step is a genuine class (A) algebraic closure once
> the 6 and 2 multiplicities are accepted. However, the restricted
> packet includes the staggered-Dirac realization gate as an admitted
> context input and cited authority with effective_status open_gate, so
> retained status cannot propagate through it."

This proof-walk demonstrates that the narrow theorem's load-bearing
chain (Steps 1-5 above) does not in fact consume any staggered-Dirac
realization content. The 6+2 multiplicities come from the retained-
bounded graph-first integration note's Step 3 — which constructs them
from a residual coordinate swap on a 4-point base, an explicit
bosonic-graph operation with no fermion-realization, BZ-corner, or
Kawamoto-Smit input. Tracelessness is a definitional property of the
abelian generator scope. Exact rational arithmetic is admissible
standard math.

The realization-gate citation in the narrow theorem note's "Hypothesis
set used (axiom-reset 2026-05-03)" section is an admitted-context
disclaimer for the broader fermion-content interpretation of the
ratio, not a load-bearing premise of the ratio algebra itself. This
proof-walk surfaces that distinction explicitly.

## Dependencies

- [`LH_DOUBLET_TRACELESS_ABELIAN_EIGENVALUE_RATIO_NARROW_THEOREM_NOTE_2026-05-02.md`](LH_DOUBLET_TRACELESS_ABELIAN_EIGENVALUE_RATIO_NARROW_THEOREM_NOTE_2026-05-02.md)
  for the narrow ratio theorem being proof-walked.
- [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md)
  for the 6 and 2 multiplicities of the Sym² and Anti² blocks
  (retained-bounded).
- [`GRAPH_FIRST_SELECTOR_DERIVATION_NOTE.md`](GRAPH_FIRST_SELECTOR_DERIVATION_NOTE.md)
  for the upstream selected-axis structure (retained-bounded).
- `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`
  and `MINIMAL_AXIOMS_2026-05-03.md`
  for the open realization-gate context that this note does not close
  and that the proof-walk demonstrates is not load-bearing for the
  ratio algebra.

These are imported authorities for a bounded theorem. The row remains
unaudited until the independent audit lane reviews this note, its
dependencies, and the runner.

## Boundaries

This note does not close:

- specific eigenvalues `+1/3` and `−1` (a normalization choice that is
  out of scope for the ratio claim);
- identification with Standard Model hypercharge `Y` (out of scope);
- the charge formula `Q = T_3 + Y/2` (out of scope);
- any anomaly-cancellation result;
- the staggered-Dirac realization gate;
- derivation of the chiral matter content itself;
- any continuum-limit numerical claim such as plaquette, mass, or
  coupling values;
- any follow-on proof-walk for other algebraic bookkeeping notes;
- any parent theorem/status promotion.

The narrow theorem's `bounded_theorem` claim type is retained: this
proof-walk is itself a `bounded_theorem` and does not propose a tier
promotion for the cited narrow theorem note. The audit lane's verdict
that the ratio algebra is class (A) clean once the multiplicities are
accepted is consistent with this proof-walk's narrower scope.

## Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_lh_doublet_eigenvalue_ratio_proof_walk_lattice_independence.py
```

Expected:

```text
TOTAL: PASS=N FAIL=0
VERDICT: bounded proof-walk passes; LH-doublet 1:(-3) ratio uses no
lattice-action or staggered-Dirac realization quantity as a
load-bearing input.
```

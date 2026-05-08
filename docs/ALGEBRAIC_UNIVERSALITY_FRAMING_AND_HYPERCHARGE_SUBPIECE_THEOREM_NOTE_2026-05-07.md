# Algebraic Universality on A_min — Framing Note + Hypercharge Sub-Piece

**Date:** 2026-05-07
**Type:** bounded support theorem
**Claim type:** bounded_theorem
**Status:** bounded source support packaging (a) a research-grade framing
of the *algebraic universality* class of A_min's predictions and (b) a
worked first sub-piece — algebraic universality of the SM hypercharges
across lattice-realization choice. The framing classifies which
framework predictions are lattice-realization-invariant by direct proof
structure (algebraic class) versus continuum-limit-invariant in Wilson's
asymptotic sense (continuum-limit class). The hypercharge sub-piece
proves that STANDARD_MODEL_HYPERCHARGE_UNIQUENESS gives identical
output `(+4/3, −2/3, −2, 0)` independent of lattice realization, by
walking its proof and observing every step uses only chiral-content +
anomaly arithmetic, never lattice machinery.
**Authority role:** source note. Audit verdict and effective status are
set only by the independent audit lane.
**Primary runner:** `scripts/frontier_algebraic_universality_hypercharge_subpiece.py`

## 0. Question

PRs [#655](https://github.com/jonathonreilly/cl3-lattice-framework/pull/655)
(SU(5) embedding consistency), [#664](https://github.com/jonathonreilly/cl3-lattice-framework/pull/664)
(A3 substep 4 — Block 06), and [#667](https://github.com/jonathonreilly/cl3-lattice-framework/pull/667)
(A4 closure) all converted "admitted" to "derived modulo explicit
convention admission." The 2026-05-07 work surfaced a deeper question:

```text
Some of the framework's "imports" (Wilson plaquette form, u_0 plaquette
value, g_bare normalization) live at lattice machinery; others (SM
hypercharges, anomaly cancellation, Tr[Y²] = 40/3, Y_GUT = √(3/5)·Y_min)
live at the algebraic / representation-theory level. Are the algebraic
predictions actually lattice-realization-invariant, or are they only
forced under the specific canonical staggered-Dirac realization that
A3 closes?
```

## Answer

**The algebraic predictions are lattice-realization-invariant by direct
proof structure, not just by Wilson's asymptotic universality.** The
proofs depend only on A_min's representation-theoretic content (chiral
matter, gauge-group structure, anomaly traces) — never on the specific
Wilson plaquette action form or the Kogut-Smit staggered-Dirac
realization that A3 closes. This is *algebraic universality*: a stronger
statement than Wilson's continuum-limit universality, exact at every
lattice scale.

The continuum-limit predictions (`<P>`, `u_0`, dimensionful mass values)
are lattice-realization-dependent at finite `a` and are universality-
class invariants in Wilson's standard sense; they converge to lattice-
independent values as `a → 0`.

## 1. Framing: two prediction classes

### Algebraic class (lattice-realization-invariant)

Predictions whose proofs use only A_min's algebraic / representation-
theoretic content:

| Prediction | Authority | Why algebraic |
|---|---|---|
| SM hypercharges `(Y_QL, Y_LL, Y_uR, Y_dR, Y_eR, Y_ν_R) = (+1/3, −1, +4/3, −2/3, −2, 0)` | [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md) | proof: anomaly-system on rationals, never invokes Wilson form |
| Tr[Y²] = 40/3 per generation | [`HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md`](HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md) | pure arithmetic on hypercharges + multiplicities |
| Y_GUT = √(3/5)·Y_min trace consistency | [`SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md`](SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md) (PR #655) | trace identity + Killing form normalization |
| sin²θ_W^GUT = 3/8 | [`SIN_SQUARED_THETA_W_GUT_FROM_SU5_NOTE_2026-05-02.md`](SIN_SQUARED_THETA_W_GUT_FROM_SU5_NOTE_2026-05-02.md) | algebra on Y_GUT + GUT-unification convention |
| 5̄ ⊕ 10 ⊕ 1 SU(5) decomposition | [`SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md`](SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md) | weight-vector matching, representation theory only |
| 3 generations on hw=1 | [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md) | hw=1 BZ-corner counting + M_3(C) algebra |
| Anomaly cancellation Tr[Y]=0, Tr[Y³]=−16/9, Tr[SU(3)²Y]=0 | [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md), [`LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md`](LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md) | trace arithmetic on chiral content |
| Q = T_3 + Y/2 (electric-charge formula) | LHCM atlas | algebraic representation rule |
| 3+1 spacetime forced | [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md) | anomaly-cancellation enumeration |
| `g_bare = 1` constraint reading (modulo CKN admission) | [`G_BARE_BOOTSTRAP_FORCING_THEOREM_NOTE_2026-05-07.md`](G_BARE_BOOTSTRAP_FORCING_THEOREM_NOTE_2026-05-07.md) (PR #667) | algebra at canonical SU(N) Killing form |

These predictions are invariant under any A_min-compatible lattice
realization that produces the same chiral content. The proofs walk
through *only* the chiral content + anomaly arithmetic + group-
theoretic identities; the specific lattice machinery (Wilson plaquette
β, staggered phases, BZ-corner doublers) does not appear as a
load-bearing input.

### Continuum-limit class (Wilson-universality invariant)

Predictions whose proofs use lattice-scale quantities:

| Prediction | Lattice-scale input | Universality |
|---|---|---|
| `u_0 = ⟨P⟩^(1/4) ≈ 0.8776` | Wilson plaquette MC measurement at β=6 | numerical value depends on action form; Wilson universality says different actions converge to same continuum scaling at fixed physical reference |
| `α_LM = α_bare/u_0 ≈ 0.0907` | uses `u_0` | inherits Wilson universality |
| `m_H_tree/v = 1/(2 u_0) ≈ 0.570` | uses `u_0` | inherits Wilson universality |
| Continuum-limit running of α_s | RG flow of plaquette action | standard QCD universality |
| Mass eigenvalues (m_e, m_μ, m_τ, etc.) | Yukawa structure + `v` from hierarchy | numerical values action-dependent at finite a; convergent at continuum |

These predictions need continuum-limit machinery (a → 0 RG flow) for
their *numerical values* to be universality-class invariants in
Wilson's standard asymptotic sense.

### What this framing dissolves

The "imports problem" — which the user surfaced earlier in the
conversation — splits cleanly along this line:

- **Algebraic-class imports are not imports.** They're theorems that
  follow from A_min's representation-theoretic content. The proofs
  never required the specific lattice realization. They're algebraic
  truths conditional on the matter content + retained tier.
- **Continuum-limit-class "imports" are universality-class members.**
  Their specific numerical values at finite `a` are realization-
  dependent, but the universality class itself is an A_min-content
  invariant, and Wilson's universality theorem (standard QFT) gives
  asymptotic invariance.

Neither category contains *physical-input* imports of the kind that
would compromise the framework's two-axiom claim. The (CKN), (LCL),
Convention A vs B, and SU(5)/SO(10) admissions are math/labelling
conventions — surface artifacts of how the algebra is named, not
load-bearing physics.

## 2. Definition: lattice-realization-invariance

A framework prediction `P` is **lattice-realization-invariant** iff the
proof of `P` cites no lattice-machinery quantity (Wilson plaquette
coefficient, staggered-phase choice, BZ-corner labels, link
unitaries) as a load-bearing input. Equivalently: any A_min-compatible
realization that produces the same chiral content + retained
gauge-group structure + retained anomaly-cancellation conditions
produces the same `P` by direct proof substitution.

This is a *property of the proof structure*, not an asymptotic
statement. It can be checked by walking the proof and verifying each
step uses only allowed inputs from the algebraic class.

## 3. Theorem (algebraic universality of the algebraic class)

**Bounded theorem.** Every prediction listed in §1 (algebraic class)
is lattice-realization-invariant per the §2 definition. The proof for
each is a structural meta-statement: walk the cited authority's proof
and verify no lattice-machinery quantity appears as a load-bearing
input.

This note **proves the first instance** (SM hypercharges) explicitly
in §4 below. The remaining predictions inherit the same meta-argument
applied to their respective authorities; full per-prediction proof-walks
are flagged as **open follow-on sub-pieces** in §6.

## 4. Sub-piece: SM hypercharges are lattice-realization-invariant

### 4.1 Statement

**Theorem (Hypercharge Algebraic Universality).** Under {A_min +
retained-tier surface (LH content + RH SU(2)-singlet completion +
anomaly cancellation + Y(ν_R) = 0 + Q(u_R) > 0)}, the SM hypercharges

```text
Y(Q_L) = +1/3,  Y(L_L) = −1,
Y(u_R) = +4/3,  Y(d_R) = −2/3,  Y(e_R) = −2,  Y(ν_R) = 0
```

are *lattice-realization-invariant*: any A_min-compatible lattice
realization producing the same retained chiral content + the same
retained gauge-group structure + the same retained anomaly-cancellation
conditions produces the same hypercharges via the same proof. The
proof of [STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md)
uses no Wilson plaquette / staggered-phase / BZ-corner-label content as
load-bearing input.

### 4.2 Proof-walk verification

Walking [STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md)'s proof step by step:

| Step | Content | Inputs used | Lattice-machinery? |
|---|---|---|---|
| §2.1 | Anomaly traces (E1) Tr[Y]=0, (E2) Tr[SU(3)²Y]=0, (E3) Tr[Y³]=−16/9 | hypercharge values + multiplicity counts (6 per Q_L, 2 per L_L, 3 per u_R, ...) + SU(2) and SU(3) Dynkin indices T(fund) = 1/2 | NO — multiplicity counts come from chiral structure (LH-doublet × triplet, RH × triplet, etc.) which is a structural fact about the matter content, independent of how the lattice realizes it |
| §2.2 | Linear system (A1) 3(y_1 + y_2) + y_3 + y_4 = 0, (A2) y_1 + y_2 = 2/3, (A3) cubic | rational arithmetic on (E1)–(E3) | NO — pure rational arithmetic |
| §2.3 | Reduction under Y(ν_R) = 0 | substitution | NO — algebraic substitution |
| §2.4 | Closed-form quadratic solve | discriminant = 324 = 18² | NO — number theory on rationals |
| §2.5 | Q(u_R) > 0 picks `y_1 = +4/3` over `y_2 = +4/3` | sign convention from electric-charge labelling (admitted SM convention) | NO — convention input only |
| §2.6 | Collected `(y_1, y_2, y_3, y_4) = (+4/3, −2/3, −2, 0)` | output | n/a |

**Conclusion.** Every step uses either (i) chiral-content multiplicity
counts, (ii) SU(2)/SU(3) Dynkin indices (group-theoretic constants),
(iii) rational arithmetic, or (iv) the admitted SM convention `Q = T_3 + Y/2`
+ `Q(u_R) > 0`. No step invokes Wilson plaquette form, staggered-phase
choice, BZ-corner labels, link unitaries, lattice scale `a`, or any
other lattice-machinery quantity. ∎

### 4.3 Concrete realization-invariance test

Construct three hypothetical "alternative" A_min-compatible chiral
realizations (purely as mathematical sanity checks on the meta-claim):

1. **Realization R_KS** (canonical Kogut-Susskind staggered-Dirac, A3-forced).
2. **Realization R_alt-A** (hypothetical: the same chiral content
   embedded differently in lattice machinery, e.g., a domain-wall
   formulation that produces LH-doublet `Q_L : (2, 3)`, `L_L : (2, 1)`
   plus RH SU(2)-singlet completion).
3. **Realization R_alt-B** (hypothetical: any other A_min-compatible
   realization with the same retained chiral content).

For each, the anomaly traces (E1), (E2), (E3) evaluate identically:

```text
Tr[Y] = 6·Y(Q_L) + 2·Y(L_L) − 3·Y(u_R) − 3·Y(d_R) − 1·Y(e_R) − 1·Y(ν_R)
       = (multiplicity counts × hypercharge values, identical across realizations)
       = 0     under unique solution
```

The multiplicity counts (6, 2, 3, 3, 1, 1) come from the chiral-content
counts (3 colors × 2 isospin = 6 for Q_L, 1 × 2 = 2 for L_L, 3 colors
× 1 = 3 for u_R, etc.) which are STRUCTURAL FACTS about the matter
content. They do not depend on the lattice realization that produces
them.

Hence the anomaly system has the same coefficients across all three
realizations, hence the same unique rational solution `(+4/3, −2/3,
−2, 0)`. Hypercharge realization-invariance holds.

### 4.4 What this sub-piece does NOT close

- The chiral content itself (LH-doublet + RH SU(2)-singlet completion)
  IS realization-determined — A3 forces it via the canonical staggered-
  Dirac realization. This sub-piece assumes the chiral content as
  retained-tier input and shows that *given* the chiral content, the
  hypercharges are realization-invariant.
- The remaining algebraic-class predictions (Tr[Y²], sin²θ_W^GUT,
  SU(5) embedding, etc.) need their own per-prediction proof-walks.
  Each follows the same meta-pattern but is out of scope for this
  single sub-piece.
- Continuum-limit predictions (`<P>`, `u_0`, mass values) require
  Wilson's universality theorem (standard QFT machinery), which is
  not provided here.

## 5. What this framing closes

- **Conceptual clarification.** The "imports problem" splits into
  algebraic-class (already-not-imports, by proof structure) and
  continuum-limit-class (universality-class invariants, asymptotic).
  Neither category contains physical-input imports.
- **Hypercharge sub-piece** (§4) is a worked instance of algebraic
  universality with explicit proof-walk verification.
- **Roadmap for follow-on sub-pieces** — each remaining algebraic-class
  prediction has the same meta-pattern; closure requires walking each
  proof.

## 6. Open follow-on sub-pieces

Each of these would be a small theorem note + runner that proof-walks
the cited authority and verifies algebraic universality. They are
**out of scope for this PR** and are flagged as open derivation
targets:

| Sub-piece | Authority to proof-walk |
|---|---|
| Tr[Y²] = 40/3 algebraic universality | [`HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md`](HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md) |
| Y_GUT = √(3/5)·Y_min algebraic universality | [`SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md`](SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md) (PR #655) |
| sin²θ_W^GUT = 3/8 algebraic universality | [`SIN_SQUARED_THETA_W_GUT_FROM_SU5_NOTE_2026-05-02.md`](SIN_SQUARED_THETA_W_GUT_FROM_SU5_NOTE_2026-05-02.md) |
| 5̄ ⊕ 10 ⊕ 1 algebraic universality | [`SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md`](SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md) (PR #655) |
| Anomaly cancellation algebraic universality | [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md) + [`LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md`](LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md) |
| 3+1 spacetime algebraic universality | [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md) |
| `g_bare = 1` constraint reading algebraic universality | [`G_BARE_BOOTSTRAP_FORCING_THEOREM_NOTE_2026-05-07.md`](G_BARE_BOOTSTRAP_FORCING_THEOREM_NOTE_2026-05-07.md) (PR #667) |

## 7. What this does NOT close

- **Continuum-limit-class universality.** The numerical values of
  `<P>`, `u_0`, α_LM, etc. require Wilson's continuum-limit universality
  theorem. This note does not address that.
- **Realization-uniqueness.** This note assumes A_min-compatible
  realizations exist; it does NOT claim there's a universality CLASS
  with multiple members. Per A3 closure (PR #664), A_min forces the
  staggered-Dirac realization. The "alternative realizations" in §4.3
  are mathematical sanity checks, not actual lattice formulations the
  framework allows.
- **Quantitative mass predictions.** Mass eigenvalues are
  continuum-limit class and out of scope.
- **Promotion of any cited authority.** The proof-walk verification
  uses cited authorities as black boxes; their own audit-status is
  unchanged by this note.

## 8. Status

```yaml
actual_current_surface_status: bounded support theorem
proposal_allowed: false
proposal_allowed_reason: |
  This is a research-grade framing note + first sub-piece. The framing
  classifies framework predictions into algebraic-class (lattice-
  realization-invariant by proof structure) and continuum-limit-class
  (Wilson universality). The sub-piece (SM hypercharges) is proven
  algebraically universal by explicit proof-walk verification.
  Eligible for retention upgrade once: (a) STANDARD_MODEL_HYPERCHARGE_UNIQUENESS
  is independently audited and retained, (b) this note is independently
  audited, (c) the §6 follow-on sub-pieces are landed (each is a
  separate small PR).
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## 9. Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_algebraic_universality_hypercharge_subpiece.py
```

Expected:

```text
TOTAL: PASS=N FAIL=0
VERDICT: SM hypercharges (+4/3, −2/3, −2, 0) are lattice-realization-
invariant per the §2 definition. Proof of STANDARD_MODEL_HYPERCHARGE_
UNIQUENESS uses only chiral-content multiplicity counts + Dynkin
indices + rational arithmetic + admitted Q = T_3 + Y/2 convention; no
Wilson plaquette / staggered-phase / BZ-corner / link-unitary content
appears as load-bearing input.
```

The runner uses Python standard library only (`fractions.Fraction` for
exact arithmetic). It checks:

1. **Note structure.** Required strings (framing, definition, theorem,
   sub-piece, proof-walk table, follow-on list, scope guards).
2. **Premise-class consistency.** All cited authorities exist on disk.
3. **Anomaly-system uniqueness.** Solving the (A1)+(A2)+(A3') system
   gives the unique solution `(+4/3, −2/3, −2, 0)` via exact `Fraction`
   arithmetic. Reproduces STANDARD_MODEL_HYPERCHARGE_UNIQUENESS §2.4.
4. **Multiplicity-count invariance.** The anomaly traces depend on
   structural multiplicity counts `(6, 2, 3, 3, 1, 1)` (LH Q_L 6 ×
   Y(Q_L), LH L_L 2 × Y(L_L), RH u_R 3 × Y(u_R), etc.) which come from
   chiral content, NOT from lattice realization. The runner verifies
   the trace formulas explicitly in terms of these multiplicity counts
   and confirms the unique solution depends only on (multiplicities,
   Dynkin indices, rational arithmetic).
5. **Realization-invariance under hypothetical alternatives.** The
   runner constructs three hypothetical "alternative realizations"
   (each producing the same chiral content) and confirms each gives
   the same anomaly system → same hypercharges. This is a structural
   sanity check on the meta-claim.
6. **Proof-walk audit.** The runner verifies that the §4.2 table's
   "no lattice-machinery" claim holds for each step of
   STANDARD_MODEL_HYPERCHARGE_UNIQUENESS's proof, by checking that
   the load-bearing inputs (multiplicity counts, Dynkin indices,
   rational arithmetic, sign convention) are all from the algebraic
   class.
7. **Forbidden-import audit.** Stdlib only, no PDG pins.
8. **Boundary check.** Continuum-limit class predictions, realization-
   uniqueness, mass eigenvalues all explicitly NOT closed.
9. **Sister-PR pattern.** Cross-references to #655, #664, #667
   establish the convention-admission analogue chain (this note is a
   separate research-grade meta-theorem on top of those).

## 10. Cross-references

- Sister PRs (convention-admission pattern):
  - PR [#655](https://github.com/jonathonreilly/cl3-lattice-framework/pull/655) — SU(5) embedding consistency (admits SU(5) Killing form)
  - PR [#664](https://github.com/jonathonreilly/cl3-lattice-framework/pull/664) — A3 substep 4 closure (admits (LCL) labelling)
  - PR [#667](https://github.com/jonathonreilly/cl3-lattice-framework/pull/667) — A4 closure (admits (CKN) Killing form)
- Authority being proof-walked: [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md)
- Companion catalog: [`HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md`](HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md)
- Anomaly-cancellation upstream: [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md), [`LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md`](LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md)
- LH content + RH completion source: [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md), [`HYPERCHARGE_IDENTIFICATION_NOTE.md`](HYPERCHARGE_IDENTIFICATION_NOTE.md)
- A3 realization gate: [`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md)
- Minimal axioms parent: [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)

## 11. Honest scope

**Branch-local theorem + framing.** This note packages a research-grade
distinction between framework prediction classes (algebraic vs
continuum-limit) and proves the first algebraic-universality sub-piece
explicitly (SM hypercharges). The framing dissolves the "imports
problem" structurally: algebraic-class predictions were never imports,
they're theorems whose proofs use only A_min's representation-theoretic
content.

**Not in scope.**

- Wilson's continuum-limit universality theorem for the continuum-
  limit-class predictions. That is standard QFT and is the candidate
  (1) work this note partially addresses but does not complete.
- Per-prediction proof-walks for the §6 follow-on sub-pieces. Each is
  a separate small PR.
- The framework's actual realization-uniqueness statement (A3 forces
  staggered-Dirac). This note assumes the canonical realization and
  asks whether the algebraic predictions would survive realization
  variation IF such variation existed.

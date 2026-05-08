# Algebraic Universality on A_min — Tr[Y²] Sub-Piece

**Date:** 2026-05-07
**Type:** bounded support theorem
**Claim type:** bounded_theorem
**Status:** bounded source support packaging the second sub-piece of the
algebraic-universality framing landed in
[`ALGEBRAIC_UNIVERSALITY_FRAMING_AND_HYPERCHARGE_SUBPIECE_THEOREM_NOTE_2026-05-07.md`](ALGEBRAIC_UNIVERSALITY_FRAMING_AND_HYPERCHARGE_SUBPIECE_THEOREM_NOTE_2026-05-07.md)
(PR #670). This note proves that the squared-hypercharge trace
identities `Tr[Y²]_LH = 8/3`, `Tr[Y²]_RH = 32/3`, `Tr[Y²]_one_gen = 40/3`,
`Tr[Y²]_three_gen = 40`, and `Tr[Y_GUT²]_three_gen = 6` are
**lattice-realization-invariant** per the §2 definition of PR #670: the
proofs in
[`HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md`](HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md)
use only multiplicity counts, hypercharge values, Dynkin indices, and
rational arithmetic. No Wilson plaquette form, staggered-phase choice,
BZ-corner labels, link unitaries, or lattice scale `a` appears as a
load-bearing input.
**Authority role:** source note. Audit verdict and effective status are
set only by the independent audit lane.
**Primary runner:** `scripts/frontier_algebraic_universality_trYsquared_subpiece.py`

## 0. Question

PR [#670](https://github.com/jonathonreilly/cl3-lattice-framework/pull/670)
introduced the algebraic-universality framing: framework predictions
split into an **algebraic class** (lattice-realization-invariant by
direct proof structure) and a **continuum-limit class** (Wilson-
universality invariants). PR #670 §6 listed seven follow-on sub-pieces;
this note ships the first of those:

```text
Is Tr[Y²]_three_gen = 40 (and the catalog identities Y1–Y5) actually
lattice-realization-invariant? Or does its proof in
HYPERCHARGE_SQUARED_TRACE_CATALOG quietly depend on Wilson-plaquette /
staggered-phase / BZ-corner content that would make it merely a
continuum-limit-class invariant?
```

## Answer

**The Tr[Y²] catalog (Y1)–(Y5) is lattice-realization-invariant by
direct proof structure.** The proofs use only (i) multiplicity counts
that come from chiral structure (LH-doublet × triplet for Q_L, etc.),
(ii) hypercharge values forced by the parent uniqueness theorem
[`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md),
(iii) Dynkin indices `T(fund) = 1/2` (group-theoretic constants), and
(iv) rational arithmetic. No lattice-machinery quantity appears as a
load-bearing input.

This makes the Tr[Y²] catalog a member of the algebraic class per
PR #670 §1. The sub-piece is closed by walking the proof and verifying
each step.

## 1. Statement

**Theorem (Tr[Y²] Algebraic Universality).** Under {A_min + retained-tier
surface (LH content + RH SU(2)-singlet completion + anomaly cancellation
+ Y(ν_R) = 0 + Q(u_R) > 0 + three-generation matter structure)}, the
squared-hypercharge trace identities

```text
(Y1)  Tr[Y²]_LH         = 8/3
(Y2)  Tr[Y²]_RH         = 32/3
(Y3)  Tr[Y²]_one_gen    = 40/3
(Y4)  Tr[Y²]_three_gen  = 40
(Y5)  Tr[Y_GUT²]_three_gen
                        = (3/20)·Tr[Y²]_three_gen
                        = 6
                        = Tr[T_a²]_SU(2),three_gen
                        = Tr[T_a²]_SU(3),three_gen
```

are *lattice-realization-invariant*: any A_min-compatible lattice
realization producing the same retained chiral content + the same
retained gauge-group structure + the same retained generation count
produces the same trace values via the same proof. The proof in
[`HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md`](HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md)
uses no Wilson plaquette / staggered-phase / BZ-corner-label content as
load-bearing input.

## 2. Proof-walk verification

Walking [`HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md`](HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md)'s
derivation step by step:

| Step | Content | Inputs used | Lattice-machinery? |
|---|---|---|---|
| §LH (Y1) | `Tr[Y²]_LH = 6·(1/3)² + 2·(-1)² = 6/9 + 2 = 8/3` | LH multiplicity counts (Q_L: 6 = 3 colors × 2 isospin; L_L: 2 = 1 × 2 isospin) + LH hypercharge values (+1/3, -1) + rational arithmetic | NO — the multiplicities come from chiral structure (LH-doublet × color triplet), a structural fact about the matter content; hypercharge values are inherited from the parent uniqueness theorem (itself algebraic class per PR #670 §4) |
| §RH (Y2) | `Tr[Y²]_RH = 3·(4/3)² + 3·(-2/3)² + 1·(-2)² + 1·0² = 48/9 + 12/9 + 4 + 0 = 32/3` | RH multiplicity counts (u_R: 3, d_R: 3, e_R: 1, ν_R: 1) + RH hypercharge values (+4/3, -2/3, -2, 0) + rational arithmetic | NO — same structural multiplicities + parent-theorem hypercharges |
| §one-gen (Y3) | `Tr[Y²]_one_gen = Tr[Y²]_LH + Tr[Y²]_RH = 8/3 + 32/3 = 40/3` | rational addition of (Y1) and (Y2) | NO — pure rational arithmetic |
| §three-gen (Y4) | `Tr[Y²]_three_gen = 3 · 40/3 = 40` | generation count `N_GEN = 3` (retained input from THREE_GENERATION_STRUCTURE / THREE_GENERATION_OBSERVABLE_THEOREM) + multiplication | NO — `N_GEN = 3` is taken as retained input (its underlying proof is its own follow-on sub-piece per PR #670 §6); the multiplication step itself is rational arithmetic |
| §GUT (Y5) Dynkin | `Tr[T_a²]_SU(2),one_gen = 2`, `Tr[T_a²]_SU(3),one_gen = 2`, three-gen sums = 6 | SU(2)/SU(3) Dynkin index `T(fund) = 1/2` + LH/RH multiplicities + rational arithmetic | NO — group-theoretic constant + structural multiplicities |
| §GUT (Y5) ratio | `Y_GUT² = (3/20)·Y²` (doubled convention) ⇒ `Tr[Y_GUT²]_three_gen = (3/20)·40 = 6` | algebraic ratio set by Killing-form normalization condition `Tr[Y_GUT²] = Tr[T_a²]_simple` | NO — Killing-form normalization is a group-theoretic / representation-theoretic statement; no lattice machinery |
| §GUT (Y5) match | `Tr[Y_GUT²]_three_gen = 6 = Tr[T_a²]_SU(2),three_gen = Tr[T_a²]_SU(3),three_gen` | substitution of (Y4) and Dynkin sums | NO — identity check on already-derived rationals |

**Conclusion.** Every step uses either (i) chiral-content multiplicity
counts (taken as retained input, structural facts about the matter
content), (ii) hypercharge values from the parent uniqueness theorem
(itself algebraic class per PR #670 §4), (iii) Dynkin indices
(group-theoretic constants), (iv) the retained generation count `N_GEN = 3`,
or (v) rational arithmetic. No step invokes Wilson plaquette form,
staggered-phase choice, BZ-corner labels, link unitaries, lattice scale
`a`, or any other lattice-machinery quantity. ∎

## 3. Concrete realization-invariance test

Construct three hypothetical "alternative" A_min-compatible chiral
realizations (purely as mathematical sanity checks on the meta-claim):

1. **Realization R_KS** (canonical Kogut-Susskind staggered-Dirac, A3-forced).
2. **Realization R_alt-A** (hypothetical: same chiral content embedded
   differently in lattice machinery, e.g., a domain-wall formulation
   producing LH-doublet `Q_L : (2, 3)`, `L_L : (2, 1)` plus RH SU(2)-
   singlet completion at the same hypercharges).
3. **Realization R_alt-B** (hypothetical: any other A_min-compatible
   realization producing the same retained chiral content + same
   gauge-group structure + same generation count).

For each, the trace identities (Y1)–(Y5) evaluate identically:

```text
Tr[Y²]_LH = (mult_QL)·Y(Q_L)² + (mult_LL)·Y(L_L)²
          = 6·(1/3)² + 2·(-1)²
          = 8/3                   (under multiplicities 6, 2; same across realizations)

Tr[Y²]_RH = (mult_uR)·Y(u_R)² + (mult_dR)·Y(d_R)²
          + (mult_eR)·Y(e_R)² + (mult_nuR)·Y(ν_R)²
          = 3·(4/3)² + 3·(-2/3)² + 1·(-2)² + 1·0²
          = 32/3                  (under multiplicities 3, 3, 1, 1; same across realizations)
```

The multiplicity counts (6, 2, 3, 3, 1, 1) come from chiral-content
structure (3 colors × 2 isospin = 6 for Q_L; 1 × 2 = 2 for L_L; 3 colors
× 1 = 3 for u_R, etc.), which is a STRUCTURAL FACT about the matter
content under A_min. They do not depend on the lattice realization that
produces them.

Hence the squared-trace identities have the same coefficients across
all three realizations, hence the same closed-form rational values.
Tr[Y²] catalog realization-invariance holds.

## 4. What this sub-piece does NOT close

- **The chiral content itself** (LH-doublet + RH SU(2)-singlet
  completion + anomaly cancellation) IS realization-determined — A3
  forces it via the canonical staggered-Dirac realization
  ([`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md)).
  This sub-piece assumes the chiral content as retained-tier input and
  shows that *given* the chiral content + parent-theorem hypercharges,
  the squared traces are realization-invariant.
- **The generation count `N_GEN = 3`** is taken as retained input from
  [`THREE_GENERATION_STRUCTURE_NOTE.md`](THREE_GENERATION_STRUCTURE_NOTE.md)
  / [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md).
  Its underlying proof has its own algebraic-universality follow-on
  sub-piece per PR #670 §6 ("3 generations on hw=1").
- **The hypercharge values** (+1/3, -1, +4/3, -2/3, -2, 0) come from
  the parent uniqueness theorem
  [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md);
  PR #670 §4 already proved THAT theorem is algebraic class. This
  sub-piece composes on that result: if the parent is algebraic class,
  the squared-trace catalog inherits the property by direct proof
  substitution.
- **Continuum-limit predictions** (`<P>`, `u_0`, mass values) require
  Wilson's universality theorem (standard QFT machinery), which is
  out of scope.
- **Promotion of any cited authority.** The proof-walk verification
  uses cited authorities as black boxes; their own audit-status is
  unchanged by this note.

## 5. What this sub-piece DOES close

- **Tr[Y²] sub-piece (§1 theorem) at bounded_theorem tier.** The first
  follow-on sub-piece flagged in PR #670 §6 is now landed with explicit
  proof-walk verification.
- **Composition pattern across sub-pieces.** When a sub-piece (here,
  Tr[Y²]) inherits hypercharge values from another sub-piece (the
  hypercharge uniqueness sub-piece, PR #670 §4), the inheritance is
  algebraic-class-preserving by direct proof substitution. This pattern
  generalizes to the remaining §6 follow-on sub-pieces.

## 6. Status

```yaml
actual_current_surface_status: bounded support theorem
proposal_allowed: false
proposal_allowed_reason: |
  This is the second sub-piece of the algebraic-universality framing
  landed in PR #670. It composes on PR #670 §4 (hypercharge sub-piece)
  by inheriting the uniqueness-theorem hypercharge values, then
  proof-walks HYPERCHARGE_SQUARED_TRACE_CATALOG to verify each step
  uses only algebraic-class inputs. Eligible for retention upgrade
  once: (a) HYPERCHARGE_SQUARED_TRACE_CATALOG is independently
  audited and retained, (b) PR #670 (parent framing) is independently
  audited, (c) this note is independently audited.
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## 7. Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_algebraic_universality_trYsquared_subpiece.py
```

Expected:

```text
TOTAL: PASS=N FAIL=0
VERDICT: Tr[Y²] catalog (Y1)–(Y5) is lattice-realization-invariant per
PR #670 §2 definition. Proof of HYPERCHARGE_SQUARED_TRACE_CATALOG uses
only chiral-content multiplicity counts + parent-theorem hypercharges +
SU(2)/SU(3) Dynkin indices + retained generation count + rational
arithmetic; no Wilson plaquette / staggered-phase / BZ-corner / link-
unitary content appears as load-bearing input.
```

The runner uses Python standard library only (`fractions.Fraction` for
exact arithmetic). It checks:

1. **Note structure.** Required strings (theorem, proof-walk table,
   realization-invariance test, scope guards, status block, sister-PR
   cross-references).
2. **Premise-class consistency.** All cited upstream authorities exist
   on disk; sister-PR forward-references handled gracefully if not yet
   on main.
3. **Trace identities (Y1)–(Y5) reproduced via exact `Fraction`.**
   `Tr[Y²]_LH = 8/3`, `Tr[Y²]_RH = 32/3`, `Tr[Y²]_one_gen = 40/3`,
   `Tr[Y²]_three_gen = 40`, `Tr[Y_GUT²]_three_gen = 6`. These reproduce
   the identities in HYPERCHARGE_SQUARED_TRACE_CATALOG.
4. **Multiplicity-count invariance.** Multiplicities (6, 2, 3, 3, 1, 1)
   derive from chiral structure (3 colors × 2 isospin for Q_L, 1 × 2 for
   L_L, etc.), NOT from lattice realization. Runner verifies the trace
   formulas in terms of these multiplicity counts.
5. **Realization-invariance under hypothetical alternatives.** The
   runner constructs three hypothetical "alternative realizations"
   (each producing the same chiral content + generation count) and
   confirms each gives the same trace catalog values. Structural
   sanity check on the meta-claim.
6. **Proof-walk audit.** Verifies that the §2 table's "no lattice-
   machinery" claim holds for each step of HYPERCHARGE_SQUARED_TRACE_
   CATALOG's derivation, by checking that the load-bearing inputs
   (multiplicity counts, hypercharge values from parent theorem,
   Dynkin indices, retained generation count, rational arithmetic) are
   all from the algebraic class.
7. **GUT-consistency identity.** Verifies `Y_GUT² = (3/20)·Y²` (doubled
   convention) ⇒ `Tr[Y_GUT²]_three_gen = 6 = Tr[T_a²]_SU(2),three_gen
   = Tr[T_a²]_SU(3),three_gen`. The Killing-form normalization that
   sets the (3/20) ratio is itself algebraic class.
8. **Forbidden-import audit.** Stdlib only, no PDG pins.
9. **Boundary check.** Continuum-limit class predictions, realization-
   uniqueness, mass eigenvalues all explicitly NOT closed.
10. **Sister-PR pattern.** Cross-references to #655, #664, #667, #670
    establish that this sub-piece is the first follow-on of PR #670.

## 8. Cross-references

- **Parent framing PR (this is the first §6 follow-on):**
  - PR [#670](https://github.com/jonathonreilly/cl3-lattice-framework/pull/670) — algebraic-universality framing + first sub-piece (hypercharges)
- Sister PRs (convention-admission pattern):
  - PR [#655](https://github.com/jonathonreilly/cl3-lattice-framework/pull/655) — SU(5) embedding consistency (admits SU(5) Killing form)
  - PR [#664](https://github.com/jonathonreilly/cl3-lattice-framework/pull/664) — A3 substep 4 closure (admits (LCL) labelling)
  - PR [#667](https://github.com/jonathonreilly/cl3-lattice-framework/pull/667) — A4 closure (admits (CKN) Killing form)
- Authority being proof-walked: [`HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md`](HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md)
- Parent uniqueness theorem (provides hypercharge values): [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md)
- Hypercharge identification (parent inline statement of `Tr[Y²] = 8/3`): [`HYPERCHARGE_IDENTIFICATION_NOTE.md`](HYPERCHARGE_IDENTIFICATION_NOTE.md)
- Anomaly-cancellation upstream: [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md), [`LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md`](LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md)
- LH content + RH completion source: [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md)
- Three-generation source: [`THREE_GENERATION_STRUCTURE_NOTE.md`](THREE_GENERATION_STRUCTURE_NOTE.md), [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
- A3 realization gate: [`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md)
- Minimal axioms parent: [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
- Companion catalog runners: `scripts/frontier_hypercharge_squared_trace_catalog.py`

## 9. Honest scope

**Branch-local sub-piece theorem.** This note ships the second
algebraic-universality sub-piece (Tr[Y²]) of the framing landed in PR
#670. The proof-walk verification confirms that the trace catalog
identities (Y1)–(Y5) are lattice-realization-invariant by direct proof
structure, not just by Wilson's asymptotic universality.

**Not in scope.**

- Wilson's continuum-limit universality theorem for the continuum-
  limit-class predictions. That is standard QFT and is the candidate
  (1) work PR #670 partially addresses but does not complete.
- Per-sub-piece proof-walks for the remaining PR #670 §6 follow-ons
  (Y_GUT, sin²θ_W^GUT, 5̄ ⊕ 10 ⊕ 1, anomaly cancellation, 3+1
  spacetime, g_bare = 1). Each is a separate small PR.
- The framework's actual realization-uniqueness statement (A3 forces
  staggered-Dirac). This sub-piece assumes the canonical realization
  and asks whether the squared-trace identities would survive
  realization variation IF such variation existed.
- Any one-loop running, threshold matching, or coupling-unification
  prediction beyond the structural Tr[Y_GUT²] = 6 normalization
  identity. The (3/20) ratio is named structurally; this note does
  not promote any unification claim.

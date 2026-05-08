# Algebraic Universality on A_min — Sub-Piece: 5̄ ⊕ 10 ⊕ 1 SU(5) Decomposition

**Date:** 2026-05-07
**Type:** bounded support theorem
**Claim type:** bounded_theorem
**Status:** bounded source support packaging the second sub-piece of the
algebraic-universality framing programme — algebraic universality of the
`5̄ ⊕ 10 ⊕ 1` SU(5) representation decomposition under PR [#655](https://github.com/jonathonreilly/cl3-lattice-framework/pull/655)'s
Block (★). The sub-piece proves that the slot-matching of the LHCM
all-LH-form 16 chiralities into the standard `5̄ ⊕ 10 ⊕ 1` SU(5)
representations is *lattice-realization-invariant* per the §2 definition
of [`ALGEBRAIC_UNIVERSALITY_FRAMING_AND_HYPERCHARGE_SUBPIECE_THEOREM_NOTE_2026-05-07.md`](ALGEBRAIC_UNIVERSALITY_FRAMING_AND_HYPERCHARGE_SUBPIECE_THEOREM_NOTE_2026-05-07.md)
(PR [#670](https://github.com/jonathonreilly/cl3-lattice-framework/pull/670)),
by walking the proof of [`SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md`](SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md)
Block (★) and observing that every load-bearing input is either
(i) LHCM-derived hypercharges (algebraic-class output of sub-piece 1),
(ii) chiral-content (color × isospin) labels (structural facts about the
matter content), or (iii) standard SU(5) representation theory (linear
algebra on a finite-dim Cartan + tensor decomposition + Schur's lemma).
No step invokes Wilson plaquette form, staggered phases, BZ-corner
labels, link unitaries, or lattice scale `a` as load-bearing input.
**Authority role:** source note. Audit verdict and effective status are
set only by the independent audit lane.
**Primary runner:** `scripts/frontier_algebraic_universality_su5_decomposition_subpiece.py`

## 0. Question

PR [#670](https://github.com/jonathonreilly/cl3-lattice-framework/pull/670)
landed the *algebraic-universality framing* + first sub-piece (SM
hypercharges). Its §6 lists six remaining algebraic-class predictions
flagged as open follow-on sub-pieces, each requiring a separate small
PR with its own per-prediction proof-walk. This note ships
**sub-piece 4** of that list:

```text
Sub-piece 4: 5̄ ⊕ 10 ⊕ 1 SU(5) representation decomposition
            (Block (★) of PR #655's SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE).
```

The question this sub-piece answers:

```text
Is PR #655's Block (★) — the slot-matching of the LHCM 16 chiralities
into 5̄ ⊕ 10 ⊕ 1 — lattice-realization-invariant per the §2 definition
of PR #670's framing? I.e., does the proof use only algebraic-class
inputs (chiral content + LHCM hypercharges + SU(5) rep theory), never
lattice machinery (Wilson plaquette / staggered-phase / BZ-corner /
link unitaries)?
```

## Answer

**Yes.** The slot-matching is lattice-realization-invariant by direct
proof structure. Walking PR #655 §4.1–§4.3 step-by-step shows every
load-bearing input is from the algebraic class:

- §4.1 LH-form transcription uses only the algebraic identity
  "conjugation flips sign of every additive quantum number" plus the
  LHCM-derived RH hypercharges.
- §4.2 SU(5) branching of the defining 5 follows from the unique
  traceless diagonal SU(5) generator commuting with `su(3) ⊕ su(2)`
  (Schur's lemma + Cartan tracelessness — pure linear algebra). The
  10 = ∧²(5) branching follows from antisymmetric-tensor decomposition.
- §4.3 slot-matching compares (color, isospin, Y_min) labels — direct
  representation-theory equality on a 6-row × N_slot grid.

No step invokes Wilson plaquette form, staggered-phase choice,
BZ-corner labels, link unitaries, lattice scale `a`, MC measurement, or
any other lattice-machinery quantity as load-bearing input.

## 1. Sub-piece statement

**Theorem (5̄ ⊕ 10 ⊕ 1 Decomposition Algebraic Universality).** Under
{A_min + retained-tier surface (LHCM atlas + STANDARD_MODEL_HYPERCHARGE_
UNIQUENESS solution `(+4/3, −2/3, −2, 0)` + ν_R singlet completion)}, the
slot-matching identity (PR #655 Block (★))

```text
[matter]_one_gen,LH  =  5̄  ⊕  10  ⊕  1                                    (★)
```

with explicit slot table

```text
Q_L      : (3,  2, +1/6)   →   10 ⊃ (3, 2)_{+1/6}
u^c_L    : (3̄, 1, −2/3)   →   10 ⊃ (3̄, 1)_{−2/3}
e^c_L    : (1,  1, +1)     →   10 ⊃ (1, 1)_{+1}
d^c_L    : (3̄, 1, +1/3)   →   5̄ ⊃ (3̄, 1)_{+1/3}
L_L      : (1,  2, −1/2)   →   5̄ ⊃ (1, 2)_{−1/2}
ν^c_L    : (1,  1, 0)      →   1
```

is *lattice-realization-invariant*: any A_min-compatible lattice
realization producing the same retained chiral content + the same
retained gauge-group structure produces the same slot-matching by the
same proof. PR #655's proof of Block (★) uses no Wilson plaquette /
staggered-phase / BZ-corner-label content as load-bearing input.

The theorem is bounded by the same upstream chain as PR #655 itself
(LHCM atlas, STANDARD_MODEL_HYPERCHARGE_UNIQUENESS, the staggered-Dirac
realization derivation target listed in `MINIMAL_AXIOMS_2026-05-03.md`).
This sub-piece does NOT promote PR #655's authority status; it adds the
algebraic-universality meta-property to the proof structure.

## 2. Lattice-realization-invariance — recall

Per [`ALGEBRAIC_UNIVERSALITY_FRAMING_AND_HYPERCHARGE_SUBPIECE_THEOREM_NOTE_2026-05-07.md`](ALGEBRAIC_UNIVERSALITY_FRAMING_AND_HYPERCHARGE_SUBPIECE_THEOREM_NOTE_2026-05-07.md)
§2: a framework prediction `P` is **lattice-realization-invariant** iff
the proof of `P` cites no lattice-machinery quantity (Wilson plaquette
coefficient, staggered-phase choice, BZ-corner labels, link unitaries,
lattice scale `a`) as a load-bearing input.

Equivalent operational test: any A_min-compatible realization producing
the same chiral content + retained gauge-group structure +
LHCM-derived hypercharge values produces the same `P` by direct proof
substitution.

This is a **structural property of the proof**, not an asymptotic
statement; checked by walking the proof and verifying each step's
inputs.

## 3. Proof-walk verification of PR #655 Block (★)

We walk [`SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md`](SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md)
§4.1–§4.3 (the part of the SU(5) embedding theorem that establishes
Block (★) — the slot-matching). Sections §4.4–§4.6 of PR #655 establish
the hypercharge-generator embedding (✦) and trace consistency (✧) for
the rescaling factor; those are out of scope for sub-piece 4 (they are
their own follow-on sub-pieces — see §6 below).

### 3.1 §4.1 LH-form transcription

| Step | Content | Inputs used | Lattice-machinery? |
|---|---|---|---|
| §4.1.a | Pass each RH chirality to LH conjugate via `u_R → u^c_L` etc. | algebraic identity: conjugation flips sign of each additive quantum number | NO — pure rep-theory identity on additive quantum numbers |
| §4.1.b | LHCM hypercharges `(Y(u_R), Y(d_R), Y(e_R), Y(ν_R)) = (+4/3, −2/3, −2, 0)` flip to `(Y(u^c_L), Y(d^c_L), Y(e^c_L), Y(ν^c_L)) = (−4/3, +2/3, +2, 0)` | LHCM atlas hypercharges (algebraic-class output of sub-piece 1) | NO — uses sub-piece 1 output |
| §4.1.c | Convert doubled-Y to Y_min (`Y_min = Y/2`) | algebraic factor of 2 | NO — pure arithmetic |
| §4.1.d | Tabulate 16-chirality LH-form content with `(SU(3) rep, SU(2) rep, Y_min)` labels | chiral-content multiplicity counts (3 × 2 = 6 for Q_L, etc.) | NO — multiplicity counts are STRUCTURAL facts about the matter content, identical across A_min-compatible realizations |
| §4.1.e | State count `|LH content per gen| = 6 + 3 + 3 + 2 + 1 + 1 = 16` | sum of multiplicities | NO — pure arithmetic |

**Conclusion §4.1:** every step uses only LHCM-derived hypercharges
(algebraic class) + chiral-content multiplicity counts (structural) +
arithmetic. No Wilson / staggered / BZ-corner content.

### 3.2 §4.2 SU(5) representation branchings

| Step | Content | Inputs used | Lattice-machinery? |
|---|---|---|---|
| §4.2.a | Defining 5 of SU(5), under `SU(3) × SU(2) ⊂ SU(5)` block embedding, branches as `(3, 1) ⊕ (1, 2)` | standard SU(5) rep theory (manifest 3+2 block decomposition of the 5×5 fundamental representation) | NO — math machinery |
| §4.2.b | The unique traceless diagonal SU(5) Cartan generator commuting with `su(3) ⊕ su(2)` is `Y̌ ∝ diag(−2, −2, −2, +3, +3) / 6` | Schur's lemma (block-scalar on each invariant block) + Cartan tracelessness `3a + 2b = 0` | NO — pure linear algebra (no lattice content) |
| §4.2.c | Y_min eigenvalues `(−1/3, +1/2)` on `(3, 1)` and `(1, 2)` blocks | division by 6 | NO — arithmetic |
| §4.2.d | 5̄ branching by complex conjugation of 5 | rep-theory identity `5̄ = (5)*` | NO — math machinery |
| §4.2.e | 10 = ∧²(5) branching from antisymmetric tensor decomposition: `∧²(3, 1)_{a} ⊕ (3, 1) ⊗ (1, 2)_{a+b} ⊕ ∧²(1, 2)_{b}` = `(3̄, 1)_{2a} ⊕ (3, 2)_{a+b} ⊕ (1, 1)_{2b}` | combinatorics on antisymmetric tensors + identities `∧²(3) = 3̄` (SU(3) fundamental), `∧²(2) = 1` (SU(2) fundamental) | NO — math machinery |
| §4.2.f | 1 = `(1, 1)_0` is the trivial irrep of SU(5) | trivial rep | NO — math machinery |

**Conclusion §4.2:** every step is standard SU(5) representation theory
(linear algebra on a finite-dim Cartan + tensor decomposition + Schur's
lemma + complex conjugation). No lattice machinery anywhere.

### 3.3 §4.3 Slot-by-slot match

| Step | Content | Inputs used | Lattice-machinery? |
|---|---|---|---|
| §4.3.a | Compare LHCM `(SU(3), SU(2), Y_min)` labels (from §4.1) with SU(5) slot labels (from §4.2) | label equality on `(SU(3) rep, SU(2) rep, Y_min)` triples | NO — direct equality |
| §4.3.b | `Q_L : (3, 2, +1/6) → 10 ⊃ (3, 2)_{+1/6}` slot match | label equality | NO |
| §4.3.c | `u^c_L : (3̄, 1, −2/3) → 10 ⊃ (3̄, 1)_{−2/3}` slot match | label equality | NO |
| §4.3.d | `e^c_L : (1, 1, +1) → 10 ⊃ (1, 1)_{+1}` slot match | label equality | NO |
| §4.3.e | `d^c_L : (3̄, 1, +1/3) → 5̄ ⊃ (3̄, 1)_{+1/3}` slot match | label equality | NO |
| §4.3.f | `L_L : (1, 2, −1/2) → 5̄ ⊃ (1, 2)_{−1/2}` slot match | label equality | NO |
| §4.3.g | `ν^c_L : (1, 1, 0) → 1` slot match | label equality | NO |
| §4.3.h | State-count bookkeeping `|5̄| + |10| + |1| = 5 + 10 + 1 = 16 = |LH content|` | pure arithmetic | NO |
| §4.3.i | Every slot in `5̄ ⊕ 10 ⊕ 1` is filled, every chirality has a slot, slot-matching is unique | combinatorial bijection on the 6-chirality × 6-slot grid | NO |

**Conclusion §4.3:** the slot-matching is direct label equality on
`(SU(3) rep, SU(2) rep, Y_min)` triples. No lattice machinery anywhere.

### 3.4 Combined verdict

Walking PR #655 §4.1–§4.3 in full, every load-bearing input is from
the algebraic class:

- LHCM-derived hypercharges (algebraic class — proven
  lattice-realization-invariant by sub-piece 1 of PR #670).
- Chiral-content multiplicity counts (structural — `3 colors × 2
  isospin = 6 for Q_L`, etc.; identical across A_min-compatible
  realizations producing the same chiral content).
- Standard SU(5) representation theory (linear algebra on a finite-dim
  Cartan + Schur's lemma + antisymmetric tensor decomposition +
  complex conjugation — pure math machinery, not lattice).
- Direct label equality on `(SU(3), SU(2), Y_min)` triples + state
  counting (arithmetic).

**No step invokes Wilson plaquette form, staggered-phase choice,
BZ-corner labels, link unitaries, lattice scale `a`, MC measurement, or
any other lattice-machinery quantity as a load-bearing input.** ∎

## 4. Concrete realization-invariance test

As in PR #670 §4.3, construct three hypothetical "alternative"
A_min-compatible chiral realizations (purely as mathematical sanity
checks on the meta-claim):

1. **Realization R_KS** (canonical Kogut-Susskind staggered-Dirac, A3-forced).
2. **Realization R_alt-A** (hypothetical: same chiral content embedded
   via a different lattice formulation — e.g., domain-wall — that
   produces the same `(SU(3), SU(2), Y_min)` label triples).
3. **Realization R_alt-B** (hypothetical: any other A_min-compatible
   realization producing the same chiral content).

For each, the slot-matching depends only on the chiral-content label
triples + LHCM hypercharges + SU(5) rep theory, all of which are
identical across the three realizations. Hence the slot-matching is the
same: same six-row table, same `|5̄ ⊕ 10 ⊕ 1| = 16` total, same
bijection. The runner verifies this explicitly by constructing the
three realizations as data and applying the same slot-matcher to each.

## 5. What this sub-piece does NOT close

- **The hypercharge-generator embedding (✦) — `T_24 = (1/√60) ·
  diag(−2, −2, −2, +3, +3)`.** That is a *separate* algebraic-class
  prediction (the unique traceless diagonal SU(5) Cartan generator
  commuting with `su(3) ⊕ su(2)`), proven in PR #655 §4.4. Its
  algebraic-universality verification is its own follow-on sub-piece.
- **The trace consistency (✧) — `Y_GUT = √(3/5) · Y_min`.** That is a
  *separate* algebraic-class prediction (rescaling factor forced by
  `Tr[Y_GUT²]_5̄+10 = Tr[T_a²]_5̄+10 = 2`), proven in PR #655 §4.5. Its
  algebraic-universality verification is its own follow-on sub-piece
  (already flagged in PR #670 §6).
- **`Tr[Y²] = 40/3` algebraic universality.** Already flagged as a
  separate follow-on sub-piece in PR #670 §6.
- **`sin²θ_W^GUT = 3/8` algebraic universality.** Already flagged in
  PR #670 §6.
- **The chiral content itself.** A3 forces it via the canonical
  staggered-Dirac realization. This sub-piece assumes the chiral
  content as retained-tier input and shows that *given* the chiral
  content + LHCM hypercharges, the slot-matching is
  realization-invariant.
- **SU(5) minimality.** PR #655 §2 emphasizes that the same matter
  content fits 16 of SO(10) (which contains `5̄ ⊕ 10 ⊕ 1` of SU(5)).
  This sub-piece inherits PR #655's "SU(5)-embedding consistency, not
  minimality" stance.
- **Coupling unification.** `g_3 = g_2 = g_1` at the GUT scale and the
  GUT scale itself (~10^16 GeV) are physical assumptions about RG
  running, not representation-theory statements. Out of scope.
- **Continuum-limit predictions.** `<P>`, `u_0`, mass values — Wilson's
  continuum-limit universality theorem is the candidate (1) work; this
  sub-piece does not address it.
- **Promotion of PR #655.** The proof-walk uses PR #655 as a black box
  (Block (★) is taken as proven there); PR #655's own audit-status is
  unchanged by this note.

## 6. Position in the §6 follow-on list

Per PR #670 §6, the open follow-on sub-pieces are:

| # | Sub-piece | Status |
|---|---|---|
| 1 | SM hypercharges algebraic universality | LANDED in PR #670 |
| 2 | `Tr[Y²] = 40/3` algebraic universality | open |
| 3 | `Y_GUT = √(3/5)·Y_min` algebraic universality | open |
| **4** | **`5̄ ⊕ 10 ⊕ 1` SU(5) decomposition algebraic universality** | **THIS NOTE** |
| 5 | `sin²θ_W^GUT = 3/8` algebraic universality | open |
| 6 | Anomaly cancellation algebraic universality | open |
| 7 | 3+1 spacetime algebraic universality | open |
| 8 | `g_bare = 1` constraint reading algebraic universality | open |

(Numbering: sub-pieces 2, 3 are the two `Tr[Y²]`/`Y_GUT` items from
PR #670 §6 row 1–2; this note picks up row 4 — the SU(5) decomposition
itself.)

## 7. Status

```yaml
actual_current_surface_status: bounded support theorem
proposal_allowed: false
proposal_allowed_reason: |
  This is the second sub-piece of the algebraic-universality framing
  programme. The sub-piece proves that PR #655's Block (★) — slot-matching
  of the LHCM 16 chiralities into 5̄ ⊕ 10 ⊕ 1 — is lattice-realization-
  invariant per the §2 definition of PR #670's framing, by walking
  PR #655 §4.1–§4.3 and verifying every load-bearing input is from the
  algebraic class.
  Eligible for retention upgrade once: (a) PR #655 is independently
  audited and retained, (b) PR #670 is independently audited and retained,
  (c) this note is independently audited.
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## 8. Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_algebraic_universality_su5_decomposition_subpiece.py
```

Expected:

```text
TOTAL: PASS=N FAIL=0
VERDICT: 5̄ ⊕ 10 ⊕ 1 SU(5) slot-matching is lattice-realization-invariant
per the §2 definition. Proof of PR #655 Block (★) uses only
LHCM-derived hypercharges + chiral-content multiplicity counts +
standard SU(5) representation theory; no Wilson plaquette /
staggered-phase / BZ-corner / link-unitary content appears as
load-bearing input.
```

The runner uses Python standard library only (`fractions.Fraction` for
exact arithmetic). It checks:

1. **Note structure.** Required strings (sub-piece statement, definition
   recall, proof-walk tables for §4.1/§4.2/§4.3, slot-matching table,
   sister-PR cross-references, scope guards).
2. **Premise-class consistency.** All cited authorities exist on disk
   (LHCM, SMH uniqueness, SU(5) embedding note, framing note as forward
   reference handled gracefully).
3. **LH-form transcription.** Each RH chirality maps to its LH
   conjugate via sign flip on hypercharge; doubled-convention `Y` to
   `Y_min` divides by 2; chiral-content multiplicity counts derived from
   `colors × isospin` structurally.
4. **Slot-table verification.** Each LHCM chirality lands in a unique
   slot of `5̄ ⊕ 10 ⊕ 1` per the canonical assignment; each slot is
   filled exactly once; state counts `|5̄| = 5, |10| = 10, |1| = 1,
   total = 16` verified via exact `Fraction`.
5. **Slot-by-slot Y_min match.** Each chirality's `Y_min` matches its
   slot's `Y_min` via exact `Fraction` equality. (This is the
   load-bearing label-equality check: `Q_L → (3, 2)_{+1/6}` requires
   `Y_min(Q_L) = +1/6`, etc.)
6. **Realization-invariance under hypothetical alternatives.** Three
   hypothetical A_min-compatible realizations all give the same chiral
   content + same `Y_min` labels → same slot-matching.
7. **Proof-walk audit.** Each step of PR #655 §4.1–§4.3 has its
   load-bearing inputs catalogued and verified to be in the
   algebraic class (multiplicity counts, LHCM hypercharges, SU(5) rep
   theory, label equality). No step uses Wilson plaquette /
   staggered-phase / BZ-corner / link-unitary / lattice-scale `a`.
8. **Forbidden-import audit.** Stdlib only, no PDG pins.
9. **Boundary check.** Hypercharge-generator embedding (✦), trace
   consistency (✧), SU(5) minimality, coupling unification,
   continuum-limit predictions, mass eigenvalues all explicitly NOT
   closed by this sub-piece.

## 9. Cross-references

- **Parent framing:** PR [#670](https://github.com/jonathonreilly/cl3-lattice-framework/pull/670)
  — algebraic-universality framing + first sub-piece (hypercharges).
  Defines the algebraic-class vs continuum-limit-class split and the
  §2 definition of lattice-realization-invariance this sub-piece
  inherits. Forward-reference to [`ALGEBRAIC_UNIVERSALITY_FRAMING_AND_HYPERCHARGE_SUBPIECE_THEOREM_NOTE_2026-05-07.md`](ALGEBRAIC_UNIVERSALITY_FRAMING_AND_HYPERCHARGE_SUBPIECE_THEOREM_NOTE_2026-05-07.md);
  the runner handles this gracefully when not yet on origin/main.
- **Authority being proof-walked:** [`SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md`](SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md)
  — PR #655's bounded theorem establishing Block (★) plus the
  hypercharge-generator embedding (✦) and trace consistency (✧).
- Sister PRs in the algebraic-universality programme:
  - PR [#655](https://github.com/jonathonreilly/cl3-lattice-framework/pull/655) — SU(5) embedding consistency (the proof being walked).
  - PR [#664](https://github.com/jonathonreilly/cl3-lattice-framework/pull/664) — A3 substep 4 closure (admits (LCL) labelling).
  - PR [#667](https://github.com/jonathonreilly/cl3-lattice-framework/pull/667) — A4 closure (admits (CKN) Killing form).
  - PR [#670](https://github.com/jonathonreilly/cl3-lattice-framework/pull/670) — algebraic-universality framing + hypercharge sub-piece.
- LHCM hypercharge source: [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md).
- LH content + RH completion: [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md), [`HYPERCHARGE_IDENTIFICATION_NOTE.md`](HYPERCHARGE_IDENTIFICATION_NOTE.md).
- Anomaly-cancellation upstream: [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md), [`LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md`](LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md).
- Related catalogs: [`HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md`](HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md), [`FULL_Y_SQUARED_TRACE_SU5_GUT_NOTE_2026-05-02.md`](FULL_Y_SQUARED_TRACE_SU5_GUT_NOTE_2026-05-02.md), [`SIN_SQUARED_THETA_W_GUT_FROM_SU5_NOTE_2026-05-02.md`](SIN_SQUARED_THETA_W_GUT_FROM_SU5_NOTE_2026-05-02.md).
- Three-generation orbit: [`THREE_GENERATION_STRUCTURE_NOTE.md`](THREE_GENERATION_STRUCTURE_NOTE.md).
- Graph-first SU(3) commutant: [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md).
- A3 realization gate: [`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md).
- Minimal-axioms parent: [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md).

## 10. Honest scope

**Branch-local theorem.** This note ships a single sub-piece of the
algebraic-universality framing programme: proof-walk verification that
PR #655's Block (★) is lattice-realization-invariant. The proof-walk is
structural (not asymptotic): every load-bearing input is catalogued and
checked against the algebraic-class allow-list.

**No new axioms.** A_min stays `{A1, A2}`. The note builds on PR #655
(Block (★) as black box) and PR #670 (the §2 definition of
lattice-realization-invariance). No PDG pins. No observation-side input.

**Not in scope.**

- The hypercharge-generator embedding (✦) sub-piece — separate.
- The trace consistency (✧) `Y_GUT = √(3/5)·Y_min` sub-piece — separate.
- SU(5) minimality — explicitly disclaimed (consistent with PR #655 §2).
- Coupling unification, GUT scale, proton decay — physical assumptions
  about RG running, not representation theory. Out of scope.
- Wilson's continuum-limit universality theorem — candidate (1) work,
  not addressed.
- Promotion of PR #655 itself — proof-walk uses it as black box.

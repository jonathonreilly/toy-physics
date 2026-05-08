# Algebraic Universality on A_min — 3+1 Spacetime Sub-Piece

**Date:** 2026-05-07
**Type:** bounded support theorem
**Claim type:** bounded_theorem
**Status:** bounded source support packaging the §6 follow-on sub-piece
"3+1 spacetime forced" of the algebraic-universality framing note
[`ALGEBRAIC_UNIVERSALITY_FRAMING_AND_HYPERCHARGE_SUBPIECE_THEOREM_NOTE_2026-05-07.md`](ALGEBRAIC_UNIVERSALITY_FRAMING_AND_HYPERCHARGE_SUBPIECE_THEOREM_NOTE_2026-05-07.md)
(framing PR — sister forward-reference; see §10). Walks the
[`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md)
five-step argument and verifies that the **temporal-dimension-forcing
piece** (chirality grading + anomaly content + single-clock evolution
forcing `d_t = 1`) is lattice-realization-invariant per the framing
note's §2 definition. The **spatial-dimension piece** `d_s = 3` is set
directly by axiom A2 (Z^3 substrate) and is therefore a substrate
input, not an output of anomaly cancellation. The combined "3+1"
prediction is **jointly forced** by A2 (substrate, fixes d_s = 3) and
the algebraic-class chain (chirality + anomaly cancellation + retained
single-clock primitives, fixes d_t = 1).
**Authority role:** source note. Audit verdict and effective status are
set only by the independent audit lane.
**Primary runner:** `scripts/frontier_algebraic_universality_3plus1_spacetime_subpiece.py`

## 0. Question

The framing note at
[`ALGEBRAIC_UNIVERSALITY_FRAMING_AND_HYPERCHARGE_SUBPIECE_THEOREM_NOTE_2026-05-07.md`](ALGEBRAIC_UNIVERSALITY_FRAMING_AND_HYPERCHARGE_SUBPIECE_THEOREM_NOTE_2026-05-07.md)
classifies framework predictions into:
- **Algebraic class** — proofs use only A_min's representation-theoretic
  content (multiplicity counts, Dynkin indices, Clifford algebra
  classification, rational arithmetic, anomaly traces) and are exact at
  every lattice scale.
- **Continuum-limit class** — numerical values realization-dependent
  at finite `a`, universality-class invariants in Wilson's sense.

The framing note's §6 lists "3+1 spacetime forced" as an open follow-on
sub-piece; the cited authority is
[`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md).
This note walks that authority and asks:

```text
Is the 3+1 spacetime prediction lattice-realization-invariant per the
framing's §2 definition (proof-structure property — the proof never
cites Wilson plaquette form, staggered-phase choice, BZ-corner labels,
link unitaries, or lattice scale `a` as a load-bearing input)?
```

## Answer (honest)

**The 3+1 prediction is jointly forced by two pieces:**

- **Spatial piece d_s = 3.** Comes directly from axiom A2 (the spatial
  substrate is `Z^3`). This is a *substrate-axiom input*, not an
  output of any derivation; it is fixed before any chiral content,
  anomaly trace, or Clifford classification appears. A2 is part of
  A_min, so this piece is "algebraic" in the trivial sense that it is
  set by the axiom itself.
- **Temporal piece d_t = 1.** Comes from the
  [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md)
  derivation chain (Steps 2–4): chirality grading requires the total
  Clifford dimension `d_s + d_t` to be even; with `d_s = 3` from A2,
  this forces `d_t` odd; the retained single-clock codimension-1
  evolution theorem (RP positivity + microcausality + Lieb-Robinson +
  cluster decomposition + Cl(3)/Z^3) excludes `d_t > 1`; therefore
  `d_t = 1`.

**The temporal-dimension-forcing piece (`d_t = 1`) IS lattice-
realization-invariant per the §2 definition.** The proof of
`d_t = 1` walks:

  (a) chiral-content multiplicity counts (LH-doublet content, RH SU(2)-
      singlet completion existence — algebraic-class input by §1.2),
  (b) anomaly-trace identities `Tr[Y]`, `Tr[Y^3]`, `Tr[SU(3)^2 Y]`
      (rational arithmetic on multiplicities × Dynkin indices ×
      hypercharge values),
  (c) the Clifford-algebra classification of even/odd-dimension volume
      elements (representation theory only, no lattice machinery),
  (d) the retained single-clock codimension-1 evolution theorem
      (which itself is derived from retained primitives — RP
      positivity, microcausality, Lieb-Robinson velocity, cluster
      decomposition, Cl(3)/Z^3 — none of which are lattice-realization
      machinery in the §1.2 sense).

No step invokes Wilson plaquette form, staggered-phase choice,
BZ-corner labels, link unitaries, lattice scale `a`, or `u_0`/`g_bare`
finite-coupling quantities as a load-bearing input.

**The combined "3+1" is jointly forced by A2 (substrate) AND the
temporal-dimension-forcing chain (algebraic class).** This sub-piece
is honest about the joint-forcing decomposition: anomaly cancellation
alone does NOT force `d_s = 3`; A2 sets `d_s = 3` directly. What
anomaly cancellation forces (modulo the retained chain Steps 2–4) is
`d_t = 1` GIVEN `d_s = 3`. The §3 theorem statement reflects this
honestly.

## 1. Framing inheritance

This sub-piece inherits the framing-note definitions:

### 1.1 Algebraic class (recap)

A prediction `P` is in the **algebraic class** when its proof uses only
A_min's representation-theoretic content (multiplicity counts, group
structure, Dynkin indices, Clifford algebra classification, anomaly
arithmetic, rational arithmetic) — never specific lattice machinery.
Algebraic-class predictions are exact at every lattice scale.

### 1.2 Lattice-realization-invariance (recap of framing §2)

A framework prediction `P` is **lattice-realization-invariant** iff
the proof of `P` cites no lattice-machinery quantity (Wilson plaquette
coefficient, staggered-phase choice, BZ-corner labels, link unitaries,
lattice scale `a`, `u_0`, `g_bare` numerical value) as a load-bearing
input. Equivalently: any A_min-compatible realization producing the
same chiral content + retained gauge-group structure + retained
anomaly-cancellation + retained single-clock primitives produces the
same `P` by direct proof substitution.

### 1.3 Substrate inputs vs lattice-machinery inputs (clarification)

The framing's §2 definition forbids **lattice-machinery** inputs (how
the lattice realizes its dynamics — plaquette form, staggered phases,
BZ-corner labels, link unitaries, finite-`a` numerical quantities). It
does NOT forbid the **substrate axioms themselves** (A1 = Cl(3), A2 =
Z^3): those define what counts as A_min-compatible at all. The whole
framing is conditional on A_min, so substrate-axiom inputs are part of
the conditioning, not load-bearing in the sense the framing forbids.

This sub-piece distinguishes:
- **A2 (substrate axiom) provides `d_s = 3`.** Substrate-axiom input,
  part of the A_min conditioning. (`d_s = 3 is a substrate-axiom
  input` per A2 = Z^3.)
- **Algebraic-class chain (Steps 2–4 of ANOMALY_FORCES_TIME) provides
  `d_t = 1`.** Algebraic-class derivation, lattice-realization-
  invariant per §1.2.

The combined "3+1" is jointly forced. No piece is lattice-machinery
load-bearing.

## 2. Theorem (3+1 sub-piece, joint-forcing form)

**Bounded support theorem.** Under {A_min + retained-tier surface (LH
chiral content via gauge closure aggregator + RH SU(2)-singlet
completion + ABJ anomaly-to-inconsistency for chiral gauge theories
[bare external admission per ANOMALY_FORCES_TIME admission (i)] +
Clifford-volume chirality via CPT_EXACT + single-clock codimension-1
evolution theorem)}:

  (S) the **spatial-dimension** prediction `d_s = 3` is set directly
      by axiom A2 (substrate). Substrate-axiom input; trivially
      invariant under any A_min-compatible lattice realization (every
      A_min-compatible realization has Z^3 substrate by definition).
  (T) the **temporal-dimension** prediction `d_t = 1` is forced by
      the algebraic-class chain (Steps 2–4 of
      [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md)),
      and the proof of (T) is *lattice-realization-invariant* per
      the framing's §1.2 definition: any A_min-compatible realization
      producing the same chiral content + retained gauge-group
      structure + retained anomaly-cancellation conditions + retained
      single-clock primitives produces the same `d_t = 1` via the
      same proof.
  (J) the **joint** prediction "spacetime is 3+1 dimensional" follows
      from (S) and (T) by direct conjunction. It is jointly forced by
      A2 (substrate, providing `d_s = 3`) and the algebraic-class
      chain (providing `d_t = 1`).

The proof-structure of (T) uses no Wilson plaquette / staggered-phase
/ BZ-corner-label / link-unitary content as load-bearing input.

## 3. Proof-walk verification

Walking the [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md)
five-step argument step by step:

| Step | Content | Load-bearing inputs | Lattice-machinery input? |
|---|---|---|---|
| Step 1 LH content carries hypercharges Y=+1/3 (mult 6) and Y=-1 (mult 2); LH-only anomaly traces evaluated | (a) chiral content from gauge closure aggregator [retained citation, NATIVE_GAUGE_CLOSURE], (b) multiplicity counts from chiral structure (3 colors × 2 isospin = 6 for Q_L; 1 × 2 = 2 for L_L), (c) Dynkin indices T(fund) = 1/2 for SU(2) and SU(3) | NO — multiplicity counts are structural facts about the matter content; Dynkin indices are group-theoretic constants; hypercharge values are integers/rationals |
| Step 1 ABJ anomaly-to-inconsistency for chiral gauge theory with nonzero `Tr[Y^3]` | bare external admission (i) per ANOMALY_FORCES_TIME audit-lane handoff; standard ABJ result [refs 1,2] for chiral gauge theories | NO — the ABJ result is bare external mathematical/QFT admission, not a lattice-machinery input |
| Step 2 Anomaly cancellation requires RH SU(2)-singlet completion; SM hypercharge branch (4/3, -2/3, -2, 0) selected by ν_R = 0 admission | (a) anomaly cancellation conditions on rationals, (b) ν_R = 0 admission (admitted neutral-singlet identification, not lattice-machinery), (c) algebraic substitution | NO — pure rational arithmetic on the anomaly system |
| Step 3 Chirality requires even total Clifford dimension `d_s + d_t`; for `d_s = 3`, `d_t` must be odd | (a) Clifford-algebra classification — volume element ω = γ_1...γ_n satisfies ω·γ_μ = (-1)^{n-1} γ_μ·ω; n even → ω anticommutes with all γ_μ (chirality grading exists); n odd → ω central (chirality grading impossible), (b) `d_s = 3` from A2, (c) requirement of chirality grading from CPT_EXACT (sublattice parity ε(x) = staggered γ_5) | NO — Clifford-algebra representation theory only; A2 substrate input; CPT_EXACT chirality-grading requirement is retained-tier internal companion, NOT lattice-machinery |
| Step 4 Single-clock codimension-1 evolution excludes `d_t > 1` (multi-time ultrahyperbolic Cauchy problem requires nonlocal Fourier-support constraints incompatible with arbitrary local data on a codim-1 slice) | (a) AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM (retained-tier internal companion), itself derived from RP positivity + microcausality + Lieb-Robinson + cluster decomposition + Cl(3)/Z^3 | NO — single-clock theorem's load-bearing primitives (RP positivity, microcausality, Lieb-Robinson velocity, cluster decomposition) are retained QFT/representation-theoretic inputs, NOT Wilson plaquette / staggered-phase / BZ-corner / link-unitary content |
| Step 5 Combine: `d_s = 3` (from A2) + `d_t` odd (from chirality + Clifford) + `d_t > 1` excluded (from single-clock evolution) → `d_t = 1` → spacetime is 3+1 | conjunction; output assembly | n/a |

**Conclusion.** Every step uses either (i) chiral-content multiplicity
counts + Dynkin indices, (ii) hypercharge anomaly arithmetic on
rationals, (iii) Clifford-algebra classification (representation
theory), (iv) substrate axiom A2, (v) retained-tier internal companion
notes (NATIVE_GAUGE_CLOSURE, CPT_EXACT, single-clock codimension-1
evolution), or (vi) the bare external ABJ admission (i) noted in
ANOMALY_FORCES_TIME's audit-lane handoff. **No step invokes Wilson
plaquette form, staggered-phase choice, BZ-corner labels, link
unitaries, lattice scale `a`, `u_0`, or `g_bare` finite-coupling
content as load-bearing input.** ∎

## 4. Concrete realization-invariance test

Construct three hypothetical "alternative" A_min-compatible chiral
realizations (purely as mathematical sanity checks on the meta-claim,
identical structure to the framing-note hypercharge sub-piece §4.3):

1. **Realization R_KS** (canonical Kogut-Susskind staggered-Dirac).
2. **Realization R_alt-A** (hypothetical: same chiral content embedded
   differently in lattice machinery, e.g., a domain-wall formulation
   that produces the same LH-doublet `Q_L : (2,3)_{+1/3}` + `L_L :
   (2,1)_{-1}` plus RH SU(2)-singlet completion).
3. **Realization R_alt-B** (hypothetical: any other A_min-compatible
   realization with the same retained chiral content, gauge-group
   structure, anomaly-cancellation status, and single-clock primitive
   structure).

For each realization:

- The **spatial dimension** `d_s = 3` is fixed by A2 (Z^3 substrate)
  identically across all three realizations (every A_min-compatible
  realization has Z^3 substrate by definition of A_min compatibility).
- The **chiral content + multiplicity counts** are identical across all
  three (the realizations differ only in lattice-machinery details, not
  in structural content).
- The **anomaly traces** evaluate identically (multiplicity × Dynkin ×
  hypercharge — all algebraic-class inputs).
- The **Clifford-algebra classification** of even-vs-odd-`n` volume
  elements is realization-independent (pure representation theory).
- The **single-clock codimension-1 evolution primitive** is supplied
  identically by the retained companion theorem (RP positivity,
  microcausality, Lieb-Robinson, cluster decomposition); none of these
  primitives depend on lattice-machinery realization details.

Hence each of the three realizations forces `d_t = 1` via the same
proof, giving spacetime 3+1 in every case. Realization-invariance
holds for the temporal-dimension piece (T); the spatial-dimension
piece (S) is trivially invariant because A2 is part of the A_min
conditioning.

## 5. What this sub-piece does NOT close

- **Spatial-dimension origin.** `d_s = 3` is a substrate axiom input
  (A2), not an output of anomaly cancellation. Whether `d_s = 3` is
  itself derivable from a deeper principle is a different question
  (the framework has the candidate observation that 3 is the unique
  spatial dimension producing the SU(3) commutant inside Cl, but that
  is the SU(3)-commutant story, not the anomaly-cancellation story).
  This sub-piece does NOT claim anomaly cancellation forces `d_s = 3`.
- **The bare external ABJ admission (i).** Per
  [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md)'s
  audit-lane handoff, admission (i) (ABJ anomaly-to-inconsistency for
  chiral gauge theory) remains a bare external admission on current
  `main` because PR 402 (proposed lattice Wess-Zumino / Fujikawa Z^4
  companion) was closed without merge. This sub-piece does NOT close
  admission (i); it inherits it from the cited authority.
- **Independent audit ratification of the cited companions.**
  NATIVE_GAUGE_CLOSURE, CPT_EXACT, and AXIOM_FIRST_SINGLE_CLOCK_
  CODIMENSION1_EVOLUTION are all proposed_retained (audit-pending) on
  `main`. This sub-piece uses them as black boxes per their stated
  authority status; their own audit verdicts are unchanged.
- **Continuum-limit class predictions.** `<P>`, `u_0`, mass values
  remain in the continuum-limit class and require Wilson's
  universality theorem (not provided here).
- **Other §6 follow-on sub-pieces of the framing note.** Tr[Y²] = 40/3,
  Y_GUT = √(3/5)·Y_min, sin²θ_W^GUT = 3/8, 5̄ ⊕ 10 ⊕ 1 SU(5)
  decomposition, anomaly cancellation as standalone, `g_bare = 1`
  constraint reading — each remains its own separate sub-piece.

## 6. Status

```yaml
actual_current_surface_status: bounded support theorem
proposal_allowed: false
proposal_allowed_reason: |
  This is a bounded follow-on sub-piece of the algebraic-universality
  framing note. It walks ANOMALY_FORCES_TIME's five-step argument and
  verifies that the temporal-dimension-forcing piece (d_t = 1) is
  lattice-realization-invariant per the framing's §2 definition;
  the spatial-dimension piece (d_s = 3) is set directly by axiom A2
  and is therefore a substrate-axiom input, not an output. The
  combined 3+1 is jointly forced by A2 (substrate) and the algebraic-
  class chain (Steps 2–4 of ANOMALY_FORCES_TIME).
  Eligible for retention upgrade once: (a) ANOMALY_FORCES_TIME's
  bare external admission (i) is internalized via a successor
  companion note, (b) NATIVE_GAUGE_CLOSURE / CPT_EXACT / AXIOM_FIRST_
  SINGLE_CLOCK_CODIMENSION1_EVOLUTION receive independent audit
  ratification, (c) this sub-piece itself is independently audited.
audit_required_before_effective_retained: true
bare_retained_allowed: false
no_new_axioms: true
no_pdg_pins: true
```

## 7. Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_algebraic_universality_3plus1_spacetime_subpiece.py
```

Expected:

```text
TOTAL: PASS=N FAIL=0
VERDICT: 3+1 spacetime prediction is jointly forced by A2 (substrate,
fixes d_s = 3) AND the algebraic-class chain (Steps 2–4 of
ANOMALY_FORCES_TIME, fixes d_t = 1). The temporal-dimension-forcing
piece (d_t = 1) is lattice-realization-invariant per the framing's §2
definition: chirality grading + anomaly arithmetic + retained
single-clock primitives never invoke Wilson plaquette / staggered-
phase / BZ-corner / link-unitary content as load-bearing input. The
spatial-dimension piece (d_s = 3) is a substrate-axiom input.
```

The runner uses Python standard library only (`fractions.Fraction` for
exact arithmetic). It checks:

1. **Note structure.** Required strings (framing inheritance, joint-
   forcing decomposition, theorem statement, proof-walk table,
   realization-invariance test, scope guards).
2. **Premise-class consistency.** All cited authorities exist on disk,
   sister-PR forward references handled gracefully.
3. **Anomaly-system structure.** The reduced anomaly system on
   rationals admits the unique solution `(+4/3, -2/3, -2, 0)` (per
   STANDARD_MODEL_HYPERCHARGE_UNIQUENESS); this is the structural
   fact downstream of which `d_t = 1` is forced. Reproduced via exact
   `Fraction` arithmetic.
4. **Spatial-dimension forcing structure.** The runner verifies that
   `d_s = 3` is a substrate-axiom input (A2/Z^3), not an output of
   anomaly cancellation, by checking that for any candidate `d_s ∈
   {1, 2, 3, 4, ...}`, the anomaly-trace formulas give the same
   formal expressions in terms of multiplicity counts × Dynkin ×
   hypercharge — the spatial dimension only enters through the
   substrate (Z^3 in A_min). This confirms A2 is the load-bearing
   input for `d_s = 3`.
5. **Temporal-dimension forcing structure.** The runner verifies the
   algebraic-class chain that forces `d_t = 1`:
   (a) chirality requires even `d_s + d_t` (Clifford classification);
   (b) with `d_s = 3` from A2, `d_t` must be odd;
   (c) single-clock codim-1 evolution excludes `d_t > 1`.
   The runner enumerates `d_t ∈ {0, 1, 2, 3, 4, 5}` and confirms that
   only `d_t = 1` simultaneously satisfies all three constraints.
6. **Realization-invariance under hypothetical alternatives.** Three
   hypothetical "alternative realizations" all give the same
   constraint chain → same `d_t = 1` → same 3+1.
7. **Proof-walk audit.** Each of the five ANOMALY_FORCES_TIME steps'
   load-bearing inputs is verified to be from the algebraic class
   (chiral content + Dynkin + Clifford + retained primitives) — no
   Wilson plaquette / staggered-phase / BZ-corner / link-unitary.
8. **Forbidden-import audit.** Stdlib only (no numpy/scipy/sympy);
   no PDG pins.
9. **Boundary check.** `d_s = 3` origin (substrate-axiom input vs
   anomaly-cancellation output), bare external ABJ admission (i),
   continuum-limit-class predictions, other §6 follow-on sub-pieces
   all explicitly NOT closed.

## 8. Honest scope (joint-forcing decomposition)

This sub-piece is honest about the joint-forcing decomposition. The
framing question was:

```text
Is "3+1 spacetime forced" lattice-realization-invariant per the
framing's §2 definition?
```

The honest answer:

- The full "3+1" prediction is jointly forced by A2 (substrate axiom,
  providing `d_s = 3`) AND the algebraic-class chain Steps 2–4 of
  [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md)
  (providing `d_t = 1`). Neither piece alone forces 3+1.
- The temporal-dimension-forcing piece (`d_t = 1`) IS lattice-
  realization-invariant per the §2 definition (proof uses only
  Clifford classification + chiral content + retained primitives,
  never Wilson plaquette / staggered-phase / BZ-corner / link
  unitaries / lattice scale).
- The spatial-dimension-forcing piece (`d_s = 3`) is a substrate
  axiom input, not an output. A2 is part of A_min, so it does not
  fall under the §2 definition's purview (substrate axioms define
  A_min-compatibility, they are not outputs whose proofs we walk).

The framing-note authors anticipated this kind of decomposition by
defining lattice-realization-invariance as a **proof-structure
property** of *outputs*, not of axiom inputs. The substrate axiom A2
is part of the A_min conditioning, not part of any output's proof-
walk.

## 9. Sister-PR pattern

| PR | What it adds | Convention admission |
|---|---|---|
| #655 | SU(5) embedding admission → derived | SU(5) Killing form |
| #664 | A3 substep 4 salvage → bounded_theorem | (LCL) generation labelling |
| #667 | A4 open gate → bootstrap-closed bounded_theorem | (CKN) Killing form |
| #670 | algebraic-universality framing + hypercharge first sub-piece | structural meta-theorem; no new admission |
| **(this PR)** | **algebraic-universality 3+1 spacetime sub-piece** | **structural follow-on; no new admission; inherits ANOMALY_FORCES_TIME's bare external admission (i)** |

This PR is structurally similar to #670: it walks an existing retained-
tier authority (here ANOMALY_FORCES_TIME instead of STANDARD_MODEL_
HYPERCHARGE_UNIQUENESS) and verifies that the proof structure satisfies
the framing's lattice-realization-invariance §2 definition. The
honest difference: ANOMALY_FORCES_TIME's output `d_s = 3` is a
substrate-axiom input rather than a derivation output, so the sub-
piece is decomposed (S) + (T) rather than monolithic.

## 10. Cross-references

- Parent framing PR (sister forward-reference): PR #670 — algebraic-
  universality framing + first sub-piece (hypercharges) at
  [`ALGEBRAIC_UNIVERSALITY_FRAMING_AND_HYPERCHARGE_SUBPIECE_THEOREM_NOTE_2026-05-07.md`](ALGEBRAIC_UNIVERSALITY_FRAMING_AND_HYPERCHARGE_SUBPIECE_THEOREM_NOTE_2026-05-07.md)
- Sister PRs (convention-admission pattern):
  - PR [#655](https://github.com/jonathonreilly/cl3-lattice-framework/pull/655) — SU(5) embedding consistency (admits SU(5) Killing form)
  - PR [#664](https://github.com/jonathonreilly/cl3-lattice-framework/pull/664) — A3 substep 4 closure (admits (LCL) labelling)
  - PR [#667](https://github.com/jonathonreilly/cl3-lattice-framework/pull/667) — A4 closure (admits (CKN) Killing form)
- Authority being proof-walked: [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md)
- LH anomaly-trace catalog: [`LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md`](LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md)
- SU(2) Witten Z_2 anomaly companion: [`SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md`](SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md)
- SU(3)^3 cubic anomaly companion: [`SU3_CUBIC_ANOMALY_CANCELLATION_THEOREM_NOTE_2026-04-24.md`](SU3_CUBIC_ANOMALY_CANCELLATION_THEOREM_NOTE_2026-04-24.md)
- Companion: STANDARD_MODEL_HYPERCHARGE_UNIQUENESS theorem note: [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md)
- Companion: chirality grading (Clifford-volume / staggered γ_5): [`CPT_EXACT_NOTE.md`](CPT_EXACT_NOTE.md)
- Companion: gauge closure aggregator: [`NATIVE_GAUGE_CLOSURE_NOTE.md`](NATIVE_GAUGE_CLOSURE_NOTE.md)
- Companion: single-clock codimension-1 evolution: [`AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md`](AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md)
- Substrate: [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) (A1 = Cl(3), A2 = Z^3)
- A3 realization gate (assumed canonical staggered-Dirac for the
  realization-invariance sanity-check baseline): [`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md)

## 11. Honest scope (note-level)

**Branch-local follow-on sub-piece.** This note completes one entry
of the framing note's §6 follow-on list ("3+1 spacetime forced") by
walking ANOMALY_FORCES_TIME's proof and verifying the temporal-
dimension-forcing piece (`d_t = 1`) is lattice-realization-invariant
per the framing's §2 definition. The spatial-dimension piece (`d_s =
3`) is honestly identified as a substrate-axiom input rather than an
anomaly-cancellation output; the combined "3+1" is jointly forced.

**Not in scope.**

- Promotion of any cited authority. ANOMALY_FORCES_TIME's bare
  external admission (i) (ABJ anomaly-to-inconsistency on the
  lattice) is inherited as-is. The retained-tier internal companion
  notes (NATIVE_GAUGE_CLOSURE, CPT_EXACT, single-clock codim-1
  evolution) are used as black boxes per their stated authority
  status.
- Wilson's continuum-limit universality theorem for the continuum-
  limit-class predictions. That is the framing note's open
  candidate-(1) work, partially addressed by §6 sub-pieces but not
  completed by any single sub-piece.
- A claim that anomaly cancellation alone forces `d_s = 3`. It does
  not; A2 is the load-bearing input for `d_s = 3`, and this sub-piece
  is honest about that.
- The other six §6 follow-on sub-pieces. Each is a separate small PR.

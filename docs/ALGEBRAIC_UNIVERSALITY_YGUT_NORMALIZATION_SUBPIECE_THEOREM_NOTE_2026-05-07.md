# Algebraic Universality on A_min — Y_GUT Normalization Sub-Piece

**Date:** 2026-05-07
**Type:** bounded support theorem
**Claim type:** bounded_theorem
**Status:** bounded support theorem packaging the second algebraic-
universality sub-piece flagged in PR #670's §6 follow-on roadmap. Proves
that the SU(5) GUT normalization

```text
Y_GUT  =  √(3/5) · Y_min     (equivalently  Y_GUT²  =  (3/20) · Y²)         (✧)
```

is *lattice-realization-invariant* per PR #670's §2 definition: the
proof in PR #655's §4.5 (Block (✧)) uses only Tr[Y_GUT²]_{5̄+10} =
Tr[T_a²]_{5̄+10} trace consistency on the embedded matter content +
SU(5) Killing-form normalization (admitted convention) + rational
arithmetic on Fractions; never lattice machinery (Wilson plaquette
form, staggered phase choice, BZ-corner labels, link unitaries,
lattice scale `a`). Sister sub-piece to PR #670 (SM hypercharges
algebraic universality).
**Authority role:** source note. Audit verdict and effective status are
set only by the independent audit lane.
**Primary runner:** `scripts/frontier_algebraic_universality_ygut_normalization_subpiece.py`

## 0. Question

PR [#670](https://github.com/jonathonreilly/cl3-lattice-framework/pull/670)
landed a research-grade framing of *algebraic universality* on A_min
that splits framework predictions into two classes (algebraic vs
continuum-limit) and proved the first sub-piece (SM hypercharges
algebraic universality) by walking STANDARD_MODEL_HYPERCHARGE_UNIQUENESS's
proof. PR #670's §6 flagged six remaining sub-pieces as open derivation
targets, each closeable by walking the cited authority and verifying no
lattice-machinery quantity is load-bearing.

This note closes the second sub-piece on the §6 list:

```text
Is the SU(5) GUT normalization Y_GUT = √(3/5)·Y_min lattice-realization-
invariant in the §2 sense — or is it only forced under the specific
canonical staggered-Dirac realization that A3 closes?
```

## Answer

**Y_GUT = √(3/5)·Y_min is lattice-realization-invariant by direct proof
structure.** The proof in PR #655's §4.5 walks through trace consistency
`Tr[Y_GUT²]_{5̄+10} = Tr[T_a²]_{5̄+10} = 2` per Weyl family + SU(5)
Killing-form Dynkin convention + rational arithmetic. No step invokes
Wilson plaquette form, staggered-phase choice, BZ-corner labels, link
unitaries, or any lattice-machinery quantity as a load-bearing input.
The Killing-form admission is standard mathematical machinery (analogous
to (CKN) in PR #667) and is surfaced explicitly here as `(SU5-CKN)`
under the same convention class as PR #655's SU(5) Killing-form
admission.

## 1. Statement

**Theorem (Y_GUT Normalization Algebraic Universality).** Under
{A_min + retained-tier surface (LH content + RH SU(2)-singlet
completion + STANDARD_MODEL_HYPERCHARGE_UNIQUENESS hypercharges + the
SU(5) embedding-consistency theorem (PR #655) deriving (★) and the
hypercharge-generator embedding (✦)) + the SU(5) Killing-form
normalization convention `(SU5-CKN)` `Tr[T_a T_b]_5 = (1/2) δ_{ab}`}, the
SU(5) GUT normalization

```text
Y_GUT  =  √(3/5) · Y_min     (equivalently  Y_GUT²  =  (3/20) · Y²)         (✧)
```

is *lattice-realization-invariant*: any A_min-compatible lattice
realization producing the same retained chiral content + the same
retained gauge-group structure + the same retained hypercharge values
+ the same `(SU5-CKN)` Killing-form Dynkin convention produces the
same `Y_GUT/Y_min = √(3/5)` rescaling factor via the same proof. The
proof of [SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md](SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md)
§4.5 uses no Wilson plaquette / staggered-phase / BZ-corner-label
content as load-bearing input.

## 2. Premises (algebraic-class only)

| Premise | Source / authority | Class |
|---|---|---|
| LH content `Q_L : (2, 3)_{+1/3}, L_L : (2, 1)_{−1}` | [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md) | algebraic |
| RH completion + SMH hypercharges `(+4/3, −2/3, −2, 0)` | [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md) | algebraic (closed by PR #670 sub-piece 1) |
| SU(5) representations `5̄ ⊕ 10 ⊕ 1` slot match (★) | [`SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md`](SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md) §4.3 | algebraic |
| Hypercharge-generator embedding (✦) `T_24 ∝ diag(−2,−2,−2,+3,+3)/√60` | [`SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md`](SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md) §4.4 | algebraic |
| Trace identity (Y5) `Tr[Y_GUT²]_three_gen = 6 = Tr[T_a²]_SU(2),three_gen = Tr[T_a²]_SU(3),three_gen` | [`HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md`](HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md) | algebraic |
| `(SU5-CKN)` Canonical SU(5) Killing-form Normalization `Tr[T_a T_b]_5 = (1/2) δ_{ab}` (Dynkin index `T(fund) = 1/2`) | standard SU(N) representation theory | math machinery (admitted convention) |
| SU(5) Dynkin indices `T(5̄) = 1/2, T(10) = 3/2` | standard SU(N) representation theory | math machinery |

No premise depends on Wilson plaquette form, staggered-phase choice,
BZ-corner labels, link unitaries, lattice scale `a`, or any lattice-
machinery quantity. The load-bearing premises are all
representation-theoretic / arithmetic.

## 3. The `(SU5-CKN)` admission (math machinery, not new axiom)

The SU(5) Killing-form normalization

```text
(SU5-CKN)   Tr[T_a T_b]_5  =  (1/2) δ_{ab}     for a, b ∈ {1, ..., 24},
```

acting on the defining `5` of SU(5), with Dynkin index `T(fund) = 1/2`,
is the standard physicist convention for the SU(N) Killing form. It
fixes the overall normalization of all SU(5) generators (including
`T_24` which embeds U(1)_Y into SU(5) up to scale). Without it, the
"trace consistency" comparison `Tr[Y_GUT²]_{5̄+10} = Tr[T_a²]_{5̄+10}`
in §4 below is vacuous since `Tr[T_a²]` would be undefined up to
overall scale.

`(SU5-CKN)` is **standard mathematical machinery**, not a new framework
axiom or admission specific to A_min. It exists at the same level as:

- (CKN) in PR [#667](https://github.com/jonathonreilly/cl3-lattice-framework/pull/667)
  — Canonical SU(N) Killing-form Normalization on the Cl(3) per-site
  module, which forces `g_bare = 1` from `β = 2 N_c = 6`.
- The SU(5) Killing-form admission in PR [#655](https://github.com/jonathonreilly/cl3-lattice-framework/pull/655)
  §4.5 — explicitly surfaced there as a "convention input rather than a
  hidden assumption."
- (LCL) in PR [#664](https://github.com/jonathonreilly/cl3-lattice-framework/pull/664)
  — generation-labelling convention.
- Convention A vs B distinction (doubled-vs-minimal hypercharge `Q = T_3 + Y/2`
  vs `Q = T_3 + Y`) — a labelling convention not load-bearing for A_min.

`(SU5-CKN)` is not load-bearing for the framework's two axioms.
A_min stays {A1, A2}. `(SU5-CKN)` is load-bearing only for the trace
comparison itself; it is the same input PR #655 explicitly admits in
§4.5.

## 4. Proof-walk verification

Walking [SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md](SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md)'s
§4.5 (Block (✧)) proof step by step:

| Step | Content | Inputs used | Lattice-machinery? |
|---|---|---|---|
| §4.1 | LH-form transcription `u_R → u^c_L` etc. (sign flips on additive QNs) | algebraic conjugation rule | NO — pure representation theory |
| §4.2 | Standard SU(5) branchings `5 = (3,1)_{−1/3} ⊕ (1,2)_{+1/2}`, `10 = ∧²(5)`, `5̄`, `1` | SU(5) representation theory; Schur's lemma + tracelessness fixes Y̌ | NO — pure rep theory |
| §4.3 | Slot-by-slot match (★) `[matter]_LH = 5̄ ⊕ 10 ⊕ 1` | LHCM hypercharges + `(Y_min, SU(3), SU(2))` labels | NO — rep theory + arithmetic |
| §4.4 | Hypercharge generator (✦) `T_24 ∝ diag(−2,−2,−2,+3,+3)` (Schur block-scalar + tracelessness) | Schur's lemma + linear algebra | NO — pure linear algebra |
| §4.5(a) | `Tr[Y_GUT²]_{5̄}` computation: `3·(c·1/3)² + 2·(c·1/2)² = c²·(1/3 + 1/2) = c²·(5/6)` | rational arithmetic on Y_min eigenvalues | NO — rational arithmetic |
| §4.5(b) | `Tr[Y_GUT²]_{10}` computation: `3·(c·2/3)² + 6·(c·1/6)² + 1·(c·1)² = c²·(4/3 + 1/6 + 1) = c²·(5/2)` | rational arithmetic on Y_min eigenvalues | NO — rational arithmetic |
| §4.5(c) | `Tr[Y_GUT²]_{5̄+10} = c² · (5/6 + 5/2) = c² · (10/3)` per Weyl family | rational arithmetic | NO |
| §4.5(d) | `Tr[T_a²]_{5̄+10} = T(5̄) + T(10) = 1/2 + 3/2 = 2` (Dynkin indices) | SU(5) Dynkin indices + `(SU5-CKN)` | NO — rep theory + admitted Killing-form convention |
| §4.5(e) | Trace consistency equation `c² · (10/3) = 2` ⇒ `c² = 3/5` ⇒ `c = √(3/5)` | rational arithmetic + perfect-fraction match | NO — rational arithmetic |
| §4.6 | Three-generation lift: `Tr[Y_GUT²]_three_gen = 3 · 2 = 6 = Tr[T_a²]_three_gen` | linear in generation count | NO |

**Conclusion.** Every step uses either (i) standard SU(5) representation
theory (Schur's lemma, Dynkin indices, antisymmetric tensor branching),
(ii) hypercharge values from the algebraic-class STANDARD_MODEL_HYPERCHARGE_UNIQUENESS
(closed as algebraic universal in PR #670 sub-piece 1), (iii)
multiplicity counts from chiral structure (`6 = 3·2` etc., closed as
algebraic-class in PR #670 sub-piece 1), (iv) the admitted `(SU5-CKN)`
Killing-form convention (math machinery, surfaced in §3), or (v)
rational arithmetic on Fractions. No step invokes Wilson plaquette form,
staggered-phase choice, BZ-corner labels, link unitaries, lattice
scale `a`, or any other lattice-machinery quantity. ∎

## 4.5 Concrete realization-invariance test

Construct three hypothetical "alternative" A_min-compatible chiral
realizations (purely as mathematical sanity checks on the meta-claim,
parallel to PR #670's §4.3):

1. **Realization R_KS** (canonical Kogut-Susskind staggered-Dirac, A3-forced).
2. **Realization R_alt-A** (hypothetical: same chiral content embedded
   differently in lattice machinery, e.g., a domain-wall formulation
   that produces the same `(SU(3), SU(2), Y_min)` labels per chirality).
3. **Realization R_alt-B** (hypothetical: any other A_min-compatible
   realization with the same retained chiral content).

For each, the trace `Tr[Y_min²]_{5̄+10}` per Weyl family evaluates
identically:

```text
Tr[Y_min²]_{5̄}   =  3 · (1/3)²  +  2 · (1/2)²       = 1/3 + 1/2 = 5/6
Tr[Y_min²]_{10}  =  3 · (2/3)²  +  6 · (1/6)²  +  1 · 1²
                 =  4/3 + 1/6 + 1                  = 5/2
Tr[Y_min²]_{5̄+10}                                  = 10/3
```

The multiplicity counts `(3, 2, 3, 6, 1)` and the `Y_min` eigenvalues
`(1/3, 1/2, 2/3, 1/6, 1)` come from the chiral-content slot match (★)
which is structural per PR #655 §4.3 — they do not depend on the
lattice realization.

The Dynkin sum `Tr[T_a²]_{5̄+10} = T(5̄) + T(10) = 1/2 + 3/2 = 2`
depends only on the SU(5) Dynkin indices, also structural and identical
across realizations.

Hence the trace-consistency equation `c²·(10/3) = 2` has the same
unique solution `c² = 3/5` across all three realizations. `Y_GUT =
√(3/5)·Y_min` realization-invariance holds.

## 5. What this sub-piece does NOT close

- The chiral content itself (LH-doublet + RH SU(2)-singlet completion)
  IS realization-determined — A3 forces it via the canonical staggered-
  Dirac realization. This sub-piece assumes the chiral content as
  retained-tier input.
- The SU(5) embedding consistency itself (PR #655) is upstream — this
  sub-piece walks PR #655's §4.5 proof, but does not re-derive the
  embedding (★) or the hypercharge-generator (✦). Both are taken as
  given algebraic-class authorities.
- The `(SU5-CKN)` admission itself is not eliminated — it is surfaced
  explicitly as standard mathematical machinery, the same convention
  PR #655 admits. Eliminating `(SU5-CKN)` would require an alternative
  Killing-form convention which is governance-side, not physics.
- **Choice of GUT group SU(5) vs SO(10) vs E6.** The same matter
  content fits 16 of SO(10), which contains 5̄ ⊕ 10 ⊕ 1 of SU(5). The
  trace identity `Tr[Y_GUT²]_{5̄+10} = 2` would migrate to a
  corresponding identity in 16 of SO(10) under different Killing-form
  scaling. This sub-piece inherits PR #655's choice.
- **GUT-scale unification assumption.** `g_3 = g_2 = g_1` at ~10^16
  GeV is physical / RG-running content, not representation-theory.
  Out of scope.
- The remaining algebraic-class predictions in PR #670's §6 list
  (Tr[Y²]=40/3, sin²θ_W^GUT=3/8, 5̄⊕10⊕1 slot match, anomaly
  cancellation, 3+1 spacetime, g_bare=1) need their own per-prediction
  proof-walks. Each follows the same meta-pattern but is out of scope
  for this single sub-piece.
- Continuum-limit predictions (`<P>`, `u_0`, mass values) are
  continuum-limit class and require Wilson's universality theorem
  (standard QFT machinery), not addressed here.

## 6. Sister-PR pattern

| PR | Sub-piece / theorem | Convention admission |
|---|---|---|
| [#655](https://github.com/jonathonreilly/cl3-lattice-framework/pull/655) | SU(5) embedding consistency (★) + (✦) | SU(5) Killing form (admitted in §4.5) |
| [#664](https://github.com/jonathonreilly/cl3-lattice-framework/pull/664) | A3 substep 4 closure (Block 06) | (LCL) generation labelling |
| [#667](https://github.com/jonathonreilly/cl3-lattice-framework/pull/667) | A4 closure: `g_bare = 1` from bootstrap forcing | (CKN) Cl(3) Killing form |
| [#670](https://github.com/jonathonreilly/cl3-lattice-framework/pull/670) | Algebraic-universality framing + SM hypercharges sub-piece | none (structural meta-theorem) |
| **(this PR)** | **Y_GUT = √(3/5)·Y_min algebraic universality** | **(SU5-CKN) (same convention class as PR #655)** |

Like PR #670, this is a meta-theorem about a specific algebraic-class
prediction (`Y_GUT = √(3/5)·Y_min`). It walks PR #655's §4.5 proof and
verifies that no lattice-machinery quantity is load-bearing.

## 7. Status

```yaml
actual_current_surface_status: bounded support theorem
proposal_allowed: false
proposal_allowed_reason: |
  This is the second algebraic-universality sub-piece on PR #670's §6
  follow-on roadmap (after sub-piece 1 = SM hypercharges in PR #670
  itself). The Y_GUT = √(3/5)·Y_min rescaling is proven algebraically
  universal by walking PR #655's §4.5 proof and verifying every step
  uses only algebraic-class inputs (representation theory, Dynkin
  indices, rational arithmetic) plus the (SU5-CKN) Killing-form
  convention which is standard math machinery. Eligible for retention
  upgrade once: (a) SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE is
  independently audited and retained, (b) HYPERCHARGE_SQUARED_TRACE_CATALOG
  is independently audited and retained, (c) PR #670's framing note is
  independently audited, (d) this note is independently audited. The
  theorem itself is exact algebra on Fraction-precision; runner verifies
  the trace consistency `c² = 3/5` in exact rational arithmetic.
audit_required_before_effective_retained: true
bare_retained_allowed: false
parent_update_allowed_only_after_retained: true
```

## 8. Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_algebraic_universality_ygut_normalization_subpiece.py
```

Expected:

```text
TOTAL: PASS=N FAIL=0
VERDICT: Y_GUT = √(3/5)·Y_min (equivalently Y_GUT² = (3/20)·Y² in
doubled convention) is lattice-realization-invariant per PR #670's §2
definition. Proof of SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE §4.5 uses
only chiral-content multiplicities + Y_min eigenvalues from STANDARD_MODEL_
HYPERCHARGE_UNIQUENESS + SU(5) Dynkin indices + (SU5-CKN) Killing-form
convention + rational arithmetic; no Wilson plaquette / staggered-phase
/ BZ-corner / link-unitary content appears as load-bearing input.
```

The runner uses Python standard library only (`fractions.Fraction` for
exact arithmetic). It checks:

1. **Note structure.** Required strings (theorem, premises, (SU5-CKN)
   admission, proof-walk table, scope guards, sister-PR cross-refs).
2. **Premise-class consistency.** All cited authorities exist on disk;
   sister-PR forward-references handled gracefully if absent (per PR
   #667 pattern in `frontier_g_bare_bootstrap_forcing.py`).
3. **Tr[Y_min²]_{5̄+10} = 10/3 per Weyl family.** Reproduces PR #655
   §4.5 in exact `Fraction` arithmetic.
4. **Tr[T_a²]_{5̄+10} = 2 per Weyl family** under `(SU5-CKN)`. Dynkin
   index sum `T(5̄) + T(10) = 1/2 + 3/2 = 2`.
5. **Trace consistency forces c² = 3/5.** The equation `c²·(10/3) = 2`
   has unique rational solution `c² = 3/5`, equivalent to `c = √(3/5)`.
6. **Doubled-convention restatement.** `Y_GUT² = (3/20)·Y²` in doubled
   convention `Q = T_3 + Y/2`, equivalent to `Y_GUT² = (3/5)·Y_min²` in
   minimal convention `Y_min = Y/2`.
7. **Three-generation lift.** `Tr[Y_GUT²]_three_gen = 3·2 = 6 =
   Tr[T_a²]_three_gen` matches HYPERCHARGE_SQUARED_TRACE_CATALOG (Y5).
8. **Realization-invariance under hypothetical alternatives.** Three
   hypothetical "alternative realizations" (each with the same chiral
   content) all give the same `c² = 3/5` solution.
9. **Proof-walk audit.** Each step of PR #655's §4.5 proof uses only
   algebraic-class inputs (no Wilson plaquette / staggered-phase /
   BZ-corner / link-unitary content).
10. **(SU5-CKN) admission audit.** Surfaced explicitly, flagged as
    standard math machinery (analogous to (CKN) in PR #667), not a new
    framework axiom; not load-bearing for A_min minimality.
11. **Forbidden-import audit.** Stdlib only, no PDG pins.
12. **Boundary check.** Continuum-limit class predictions, choice of
    GUT group, GUT-scale unification all explicitly NOT closed.

## 9. Cross-references

- Parent framing note: PR [#670](https://github.com/jonathonreilly/cl3-lattice-framework/pull/670)
  — `ALGEBRAIC_UNIVERSALITY_FRAMING_AND_HYPERCHARGE_SUBPIECE_THEOREM_NOTE_2026-05-07.md`
  (algebraic universality framing + first sub-piece)
- Load-bearing authority being proof-walked: [`SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md`](SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md)
  (PR #655 — derivation of (★), (✦), and (✧) from the graph-first
  surface)
- Companion catalog for (Y5) trace identity: [`HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md`](HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md)
  — `Tr[Y_GUT²]_three_gen = 6` per Weyl family
- Sister sub-piece (algebraic universality of Tr[Y²] = 40/3): [`FULL_Y_SQUARED_TRACE_SU5_GUT_NOTE_2026-05-02.md`](FULL_Y_SQUARED_TRACE_SU5_GUT_NOTE_2026-05-02.md)
  — open follow-on per PR #670 §6
- Sister-PR convention-admission analogues:
  - PR [#655](https://github.com/jonathonreilly/cl3-lattice-framework/pull/655)
    — SU(5) embedding consistency (admits SU(5) Killing form)
  - PR [#664](https://github.com/jonathonreilly/cl3-lattice-framework/pull/664)
    — A3 substep 4 closure (admits (LCL) labelling)
  - PR [#667](https://github.com/jonathonreilly/cl3-lattice-framework/pull/667)
    — A4 closure (admits (CKN) Killing form)
- Hypercharge upstream: [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md)
- LH content + RH completion source: [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md), [`HYPERCHARGE_IDENTIFICATION_NOTE.md`](HYPERCHARGE_IDENTIFICATION_NOTE.md)
- A3 realization gate: [`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md)
- Minimal axioms parent: [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
- Cycle 19 downstream user of (✧): [`SIN_SQUARED_THETA_W_GUT_FROM_SU5_NOTE_2026-05-02.md`](SIN_SQUARED_THETA_W_GUT_FROM_SU5_NOTE_2026-05-02.md)

## 10. Honest scope

**Branch-local theorem.** This note packages the second algebraic-
universality sub-piece on PR #670's §6 follow-on roadmap, proving that
the SU(5) GUT normalization `Y_GUT = √(3/5)·Y_min` is lattice-
realization-invariant per PR #670's §2 definition. The proof walks PR
#655's §4.5 (Block (✧)) and verifies every step uses only
algebraic-class inputs.

**Not in scope.**

- Wilson's continuum-limit universality theorem for the continuum-
  limit-class predictions. That is standard QFT and is the candidate
  (1) work PR #670 partially addresses but does not complete.
- Per-prediction proof-walks for the remaining §6 follow-on sub-pieces
  (Tr[Y²]=40/3, sin²θ_W^GUT=3/8, 5̄⊕10⊕1 slot match, anomaly
  cancellation, 3+1 spacetime, g_bare=1). Each is a separate small
  PR, sister to this one.
- The framework's actual realization-uniqueness statement (A3 forces
  staggered-Dirac). Per A3 closure (PR #664), A_min forces the
  staggered-Dirac realization, and this note assumes the canonical
  realization as upstream input.
- Choice of SU(5) vs SO(10) vs E6 as GUT group (governance / physical
  choice).
- GUT-scale unification assumption (physical RG-running content).
- Promotion of any cited authority. The proof-walk verification uses
  cited authorities (PR #655, HYPERCHARGE_SQUARED_TRACE_CATALOG, etc.)
  as black boxes; their own audit-status is unchanged by this note.

**Forbidden imports (this note is bounded).** NO PDG observed values.
NO lattice MC empirical measurements. NO fitted matching coefficients.
NO new axioms (A_min stays {A1, A2}). NO appeal to dynamical
fixed-point selection. The (SU5-CKN) Killing-form admission is standard
math machinery, not a new physical input.

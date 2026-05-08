# Algebraic Universality on A_min — sin²θ_W^GUT = 3/8 Sub-Piece

**Date:** 2026-05-07
**Type:** bounded support theorem
**Claim type:** bounded_theorem
**Status:** bounded source support packaging the third sub-piece of the
algebraic-universality programme opened by PR
[#670](https://github.com/jonathonreilly/cl3-lattice-framework/pull/670)
(framing + hypercharge sub-piece). This note proves that the
GUT-scale Weinberg-angle prediction
`sin²θ_W^GUT = 3/8` is *lattice-realization-invariant* per PR #670's
§2 definition: every step of its derivation in
[`SIN_SQUARED_THETA_W_GUT_FROM_SU5_NOTE_2026-05-02.md`](SIN_SQUARED_THETA_W_GUT_FROM_SU5_NOTE_2026-05-02.md)
uses only (i) the algebraic identity
`sin²θ = tan²θ / (1 + tan²θ)`, (ii) the already-algebraic input
`Y_GUT = √(3/5)·Y_SM` (which itself is trace-forced by `Tr[Y²] = 40/3`
plus the SU(2)/SU(3) Dynkin-trace match on the embedded matter content),
(iii) two physics-side admissions surfaced explicitly: the GUT-unification
assumption `g_3 = g_2 = g_1` (admission `(GUT-UNIF)`) and the choice of
GUT group SU(5) vs. SO(10) vs. E6 (admission `(GUT-GRP)`). No step of
the derivation invokes the Wilson plaquette form, staggered phases,
BZ-corner labels, link unitaries, lattice scale `a`, or any other
lattice-machinery quantity. The two physics-side admissions are NOT
lattice machinery — they are physical assumptions about coupling
running, listed alongside (LCL) (PR #664), (CKN) (PR #667), and the
SU(5)-vs-SO(10)/E6 admission of PR #655 in the convention-admission
ledger.
**Authority role:** source note. Audit verdict and effective status are
set only by the independent audit lane.
**Primary runner:** `scripts/frontier_algebraic_universality_sin2thetaW_subpiece.py`

## 0. Question

PR [#670](https://github.com/jonathonreilly/cl3-lattice-framework/pull/670)
opened the algebraic-universality programme: it framed two prediction
classes (algebraic vs continuum-limit) and proved the first sub-piece
(SM hypercharges) explicitly. Its §6 listed seven follow-on sub-pieces,
each requiring its own per-prediction proof-walk. The present note
addresses the third item on that list:

```text
sin²θ_W^GUT = 3/8 algebraic universality.
```

The question: walking the proof of `sin²θ_W^GUT = 3/8` per
[`SIN_SQUARED_THETA_W_GUT_FROM_SU5_NOTE_2026-05-02.md`](SIN_SQUARED_THETA_W_GUT_FROM_SU5_NOTE_2026-05-02.md),
does any step rely on lattice-machinery content, or does the proof
remain entirely within the algebraic class once the explicit physics-side
admissions are surfaced?

## Answer

**The `sin²θ_W^GUT = 3/8` prediction is lattice-realization-invariant
per PR #670's §2 definition.** Its derivation walks through only the
algebraic identity `sin²θ = tan²θ / (1 + tan²θ)`, the algebraic GUT
hypercharge rescaling `Y_GUT = √(3/5)·Y_SM` (itself trace-forced and
algebraic), and two explicit physics-side admissions:

- `(GUT-UNIF)` — the GUT-unification assumption `g_3 = g_2 = g_1` at
  the GUT scale. This is a physical assumption about coupling running,
  NOT a statement about lattice machinery. It is admitted on the same
  ledger as `(LCL)` (PR #664) and `(CKN)` (PR #667).
- `(GUT-GRP)` — the GUT-group choice (SU(5), SO(10), or E6). All three
  GUT-groups containing the standard `(3+2)`-block subgroup produce the
  same `Y_GUT² = (3/5) Y_SM²` rescaling on the embedded matter, so the
  algebraic prediction is invariant under this choice; the admission is
  surfaced for completeness, parallel to PR
  [#655](https://github.com/jonathonreilly/cl3-lattice-framework/pull/655)
  ("Does not claim SU(5) is uniquely forced").

No step invokes Wilson plaquette form, staggered phases, BZ-corner
labels, link unitaries, lattice scale `a`, `u_0`, `g_bare`, Monte Carlo
measurement, or PDG values as load-bearing input.

## 1. Inheritance from PR #670 framing

This note inherits PR
[#670](https://github.com/jonathonreilly/cl3-lattice-framework/pull/670)'s
classification:

- **Algebraic class** (lattice-realization-invariant): proofs use only
  A_min's representation-theoretic content + algebraic identities +
  rational arithmetic.
- **Continuum-limit class** (Wilson-universality invariant): proofs use
  lattice-scale quantities; numerical values are universality-class
  invariants in Wilson's standard asymptotic sense.

The claim of this sub-piece is that `sin²θ_W^GUT = 3/8` belongs to the
algebraic class. The two GUT-side admissions `(GUT-UNIF)` and `(GUT-GRP)`
are physics-side assumptions, NOT lattice machinery — they live on the
convention-admission ledger alongside `(LCL)` (PR #664), `(CKN)` (PR #667),
and the SU(5)-vs-SO(10)/E6 admission of PR #655.

## 2. Sub-piece: sin²θ_W^GUT = 3/8 is lattice-realization-invariant

### 2.1 Statement

**Theorem (Weinberg-Angle Algebraic Universality).** Under

- {A_min + retained-tier surface} (LH-doublet content + RH SU(2)-singlet
  completion + anomaly cancellation + the unique hypercharge solution
  `(+1/3, −1, +4/3, −2/3, −2, 0)` of
  [STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md)),
- the algebraic input `Y_GUT = √(3/5) · Y_SM` (trace-forced by
  [`HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md`](HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md)
  identity (Y5) on the embedded matter content,
  consistent with PR
  [#655](https://github.com/jonathonreilly/cl3-lattice-framework/pull/655)),
- the physics-side admission `(GUT-UNIF)`: at the GUT scale, the three SM
  gauge couplings unify, `g_3 = g_2 = g_1`,
- the physics-side admission `(GUT-GRP)`: the GUT-group is one of SU(5),
  SO(10), or E6 — any GUT-group containing the standard `(3+2)`-block
  subgroup with the same `(5̄ ⊕ 10 ⊕ 1)`-style branching of the
  embedded matter,

the GUT-scale Weinberg angle is uniquely

```text
sin²θ_W^GUT  =  3/8,
```

and this prediction is *lattice-realization-invariant*: any
A_min-compatible lattice realization producing the same retained chiral
content + the same retained gauge-group structure produces the same
`sin²θ_W^GUT = 3/8` via the same proof. The proof of
[`SIN_SQUARED_THETA_W_GUT_FROM_SU5_NOTE_2026-05-02.md`](SIN_SQUARED_THETA_W_GUT_FROM_SU5_NOTE_2026-05-02.md)
uses no Wilson plaquette / staggered-phase / BZ-corner-label content as
load-bearing input.

### 2.2 Proof-walk verification

Walking
[`SIN_SQUARED_THETA_W_GUT_FROM_SU5_NOTE_2026-05-02.md`](SIN_SQUARED_THETA_W_GUT_FROM_SU5_NOTE_2026-05-02.md)'s
proof step by step:

| Step | Content | Inputs used | Lattice-machinery? |
|---|---|---|---|
| §0(a) | Definition `tan²θ_W = g'² / g_2²` | SM bookkeeping convention `Q = T_3 + Y/2` (admitted convention; same as in PR #670 hypercharge sub-piece) | NO — convention only |
| §0(b) | Algebraic input `Y_GUT = √(3/5)·Y_SM` | trace-forced from `Tr[Y²]_one_gen = 40/3` matched against `Tr[T_a²]_SU(2),one_gen = Tr[T_a²]_SU(3),one_gen = 2` per generation | NO — pure multiplicity arithmetic + Dynkin indices (algebraic class) |
| §0(c) | `g'_GUT = √(3/5)·g'_SM` | same rescaling factor on the U(1) coupling, dual to (b) on the generator | NO — algebraic rescaling consequence of (b) |
| §0(d) | Admission `(GUT-UNIF)`: at GUT scale `g_3 = g_2 = g_1` | GUT-unification physics assumption; admitted, NOT lattice machinery | NO — physics-side admission, not lattice machinery |
| §0(e) | Substitution: `g'² = g_2² · (3/5)` at GUT scale | combines (c) and (d) | NO — algebraic substitution |
| §0(f) | Therefore `tan²θ_W^GUT = g'²/g_2² = 3/5` | rational arithmetic | NO — pure rational arithmetic |
| §0(g) | Algebraic identity `sin²θ = tan²θ / (1 + tan²θ)` | standard trig identity (universal mathematical identity) | NO — universal trig |
| §0(h) | Compute: `sin²θ_W^GUT = (3/5)/(1 + 3/5) = (3/5)/(8/5) = 3/8` | rational arithmetic on Fractions | NO — pure rational arithmetic |
| §0(i) | Equivalent forms `cos² = 5/8`, `tan² = 3/5` | algebraic identities | NO — algebraic identities |

**Conclusion.** Every step uses either (i) algebraic identities
(`sin²/cos²/tan²` definitions, `sin² + cos² = 1`,
`tan² = sin²/cos²`), (ii) rational arithmetic on `Fraction`s, (iii) the
algebraic input `Y_GUT = √(3/5)·Y_SM` (trace-forced; algebraic class),
or (iv) the two admitted physics-side conventions `(GUT-UNIF)` and
`(GUT-GRP)`. No step invokes Wilson plaquette form, staggered-phase
choice, BZ-corner labels, link unitaries, lattice scale `a`, or any
other lattice-machinery quantity. ∎

### 2.3 Concrete realization-invariance test

Construct three hypothetical "alternative" A_min-compatible chiral
realizations (purely as mathematical sanity checks on the meta-claim):

1. **Realization R_KS** (canonical Kogut-Susskind staggered-Dirac, A3-forced).
2. **Realization R_alt-A** (hypothetical: same chiral content embedded
   differently in lattice machinery, e.g. a domain-wall formulation
   producing the LH-doublet `Q_L : (2, 3)`, `L_L : (2, 1)` plus the RH
   SU(2)-singlet completion).
3. **Realization R_alt-B** (hypothetical: any other A_min-compatible
   realization with the same retained chiral content).

For each realization, the embedded U(1)_Y generator on the SU(5)
defining 5 carries the same `Y_GUT² / Y_SM² = 3/5` rescaling (because
the rescaling is forced by the trace identity (Y5) on the embedded
matter, and the matter content is identical across realizations). The
GUT-unification assumption `(GUT-UNIF)` and the GUT-group choice
`(GUT-GRP)` are physics-side and identical across realizations by
hypothesis. Hence each realization gives

```text
tan²θ_W^GUT = (g'² / g_2²)|_GUT = 3/5,
sin²θ_W^GUT = (3/5) / (1 + 3/5) = 3/8.
```

Weinberg-angle realization-invariance holds.

### 2.4 What this sub-piece does NOT close

- **The chiral content itself** (LH-doublet + RH SU(2)-singlet completion)
  IS realization-determined — A3 forces it via the canonical staggered-
  Dirac realization. This sub-piece assumes the chiral content as
  retained-tier input and shows that *given* the chiral content (and
  the resulting algebraic Y_GUT rescaling), the Weinberg angle is
  realization-invariant.
- **The GUT-unification assumption `(GUT-UNIF)`** is NOT closed. It is a
  physics-side admission about coupling running, surfaced explicitly on
  the same ledger as `(LCL)` and `(CKN)`. Closing it would require an
  RG-running theorem (continuum-limit class, Wilson universality
  territory).
- **The GUT-group choice `(GUT-GRP)`** is NOT closed. SU(5), SO(10),
  and E6 all support the same `Y_GUT² / Y_SM² = 3/5` rescaling on the
  embedded matter; the choice itself is not unique (parallel to PR #655).
- **The numerical value of `sin²θ_W` at M_Z (≈ 0.231)** is NOT closed.
  That follows from running `sin²θ_W^GUT = 3/8` from the GUT scale to
  M_Z, which is RG-running content (continuum-limit class).
- **The remaining algebraic-class predictions** (Tr[Y²], 5̄ ⊕ 10 ⊕ 1,
  3+1 spacetime, anomaly cancellation as algebraic universality, etc.)
  need their own per-prediction proof-walks. Each follows the same
  meta-pattern but is out of scope for this single sub-piece.
- **Continuum-limit predictions** (`<P>`, `u_0`, mass values) require
  Wilson's universality theorem (standard QFT machinery), which is not
  provided here.

## 3. The two physics-side admissions, surfaced explicitly

### 3.1 `(GUT-UNIF)` — coupling unification

**Admission.** At the GUT scale, the three SM gauge couplings unify:

```text
g_3 = g_2 = g_1     (GUT-UNIF, coupling unification at the GUT scale).
```

**Why this is a physics-side admission, not lattice machinery:**
coupling unification is a statement about the RG-running of the gauge
couplings under the GUT-group's renormalization. It depends on the
GUT-group's matter content (β-function coefficients) and on the
physical assumption that there exists a scale at which all three
couplings cross. It is NOT a lattice quantity (no plaquette, no
staggered phase, no BZ corner label, no link unitary, no lattice scale
`a`, no `u_0`, no `g_bare` value enters its statement). It is on the
same ledger as `(LCL)` (PR #664, A3 substep 4) and `(CKN)` (PR #667,
canonical SU(N) Killing form): a physics-side convention/assumption,
admitted explicitly.

**Effect on the proof.** Step §0(d). Without `(GUT-UNIF)`, the proof
cannot equate `g_1_GUT² = g_2²` and the `tan²θ_W^GUT = 3/5` rational
identity does not follow. With `(GUT-UNIF)` admitted, the rest of the
proof is pure rational arithmetic.

### 3.2 `(GUT-GRP)` — choice of GUT group

**Admission.** The GUT group is one of SU(5), SO(10), or E6, or any
larger group containing the `(3+2)`-block subgroup with the same matter
branching.

**Why this is a physics-side admission, not lattice machinery:**
PR [#655](https://github.com/jonathonreilly/cl3-lattice-framework/pull/655)
proves SU(5)-embedding *consistency*, not minimality. Its §2 explicitly
states: "Does not claim SU(5) is uniquely forced. The same matter
content fits 16 of SO(10) (which contains 5̄ ⊕ 10 ⊕ 1 of SU(5)), or
larger-group embeddings (E6 ⊃ SO(10) ⊃ SU(5))." All three GUT-groups
produce the same `Y_GUT² / Y_SM² = 3/5` rescaling on the embedded
matter (they all share the standard `(3+2)`-block decomposition), so
the algebraic prediction `sin²θ_W^GUT = 3/8` is invariant under this
choice. The admission is surfaced for ledger completeness.

**Effect on the proof.** None at the level of the algebraic prediction —
all three GUT-groups give the same `tan²θ_W^GUT = 3/5`. The admission
matters at the level of "which exact group is realized," not at the
level of the Weinberg-angle prediction. It is admitted in parallel
with PR #655 to keep the convention ledger transparent.

## 4. What this framing closes

- **Sub-piece** (§2) is a worked instance of algebraic universality for
  the Weinberg-angle prediction with explicit proof-walk verification.
- **Two physics-side admissions** `(GUT-UNIF)` and `(GUT-GRP)` are
  surfaced on the convention-admission ledger, parallel to `(LCL)`
  (PR #664), `(CKN)` (PR #667), and PR #655's SU(5)-vs-SO(10)/E6.
- **Inheritance** from PR #670's framing: this sub-piece is the third
  item in #670's §6 follow-on list to land its own per-prediction
  proof-walk. The other six remain open.

## 5. Open follow-on sub-pieces from PR #670 §6

Each remaining algebraic-class prediction in PR #670's §6 list still
needs its own proof-walk + runner. Under this PR, the following sub-pieces
remain open:

| Sub-piece | Authority to proof-walk |
|---|---|
| `Tr[Y²] = 40/3` algebraic universality | [`HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md`](HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md) |
| `Y_GUT = √(3/5)·Y_min` algebraic universality | [`SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md`](SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md) (PR #655) |
| `5̄ ⊕ 10 ⊕ 1` algebraic universality | [`SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md`](SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md) (PR #655) |
| Anomaly cancellation algebraic universality | [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md) + [`LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md`](LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md) |
| 3+1 spacetime algebraic universality | [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md) |
| `g_bare = 1` constraint reading algebraic universality | `G_BARE_BOOTSTRAP_FORCING_THEOREM_NOTE_2026-05-07.md` (PR #667) |

## 6. What this does NOT close

- **Continuum-limit-class universality.** Wilson's universality
  theorem for `<P>`, `u_0`, etc. Not addressed here.
- **The two physics-side admissions** `(GUT-UNIF)` and `(GUT-GRP)`.
  Surfaced on the ledger; not closed.
- **RG-running of `sin²θ_W` from GUT scale to M_Z.** Continuum-limit
  class (RG flow); not addressed.
- **The numerical value `sin²θ_W(M_Z) ≈ 0.231`** comparison with PDG.
  Out of scope; depends on RG running.
- **Realization-uniqueness.** This sub-piece assumes A_min-compatible
  realizations exist; it does NOT claim there's a universality CLASS
  with multiple members. Per A3 closure (PR #664), A_min forces the
  staggered-Dirac realization. The "alternative realizations" in §2.3
  are mathematical sanity checks, not actual lattice formulations the
  framework allows.
- **Quantitative mass predictions.** Mass eigenvalues are
  continuum-limit class and out of scope.
- **Promotion of any cited authority.** The proof-walk verification
  uses cited authorities as black boxes; their own audit-status is
  unchanged by this note.

## 7. Status

```yaml
actual_current_surface_status: bounded support theorem
proposal_allowed: false
proposal_allowed_reason: |
  This is a research-grade proof-walk sub-piece, third in the PR #670
  algebraic-universality programme. It proves sin²θ_W^GUT = 3/8 is
  lattice-realization-invariant by walking SIN_SQUARED_THETA_W_GUT_FROM_SU5
  step by step and confirming every load-bearing input is in the
  algebraic class plus two explicit physics-side admissions
  ((GUT-UNIF), (GUT-GRP)) listed on the convention-admission ledger.
  Eligible for retention upgrade once: (a) SIN_SQUARED_THETA_W_GUT_FROM_SU5
  is independently audited and retained, (b) HYPERCHARGE_SQUARED_TRACE_
  CATALOG (Y5) is independently audited and retained, (c) PR #670's
  framing note is independently audited and retained, (d) this note is
  independently audited.
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## 8. Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_algebraic_universality_sin2thetaW_subpiece.py
```

Expected:

```text
TOTAL: PASS=N FAIL=0
VERDICT: sin²θ_W^GUT = 3/8 is lattice-realization-invariant per
PR #670's §2 definition. Proof of SIN_SQUARED_THETA_W_GUT_FROM_SU5
uses only the algebraic identity sin²θ = tan²θ / (1 + tan²θ),
the algebraic input Y_GUT = √(3/5)·Y_SM (trace-forced), rational
arithmetic, and two explicit physics-side admissions ((GUT-UNIF)
g_3 = g_2 = g_1 at the GUT scale, (GUT-GRP) GUT-group choice
SU(5)/SO(10)/E6); no Wilson plaquette / staggered-phase / BZ-corner /
link-unitary content appears as load-bearing input.
```

The runner uses Python standard library only (`fractions.Fraction` for
exact arithmetic). It checks:

1. **Note structure.** Required strings (sub-piece header, proof-walk
   table, two-admission section, scope guards, status block).
2. **Premise-class consistency.** All cited authorities exist on disk
   (sister-PR forward-references handled gracefully).
3. **Algebraic identity.** `sin²θ = tan²θ / (1 + tan²θ)` evaluates
   exactly to `3/8` when `tan²θ = 3/5`, via `Fraction` arithmetic.
4. **GUT rescaling input.** `Y_GUT² / Y_SM² = 3/5` exactly via
   `Fraction`. Cross-checked against the (Y5) identity in
   `HYPERCHARGE_SQUARED_TRACE_CATALOG`.
5. **Closed-form values.** `sin²θ_W^GUT = 3/8`, `cos²θ_W^GUT = 5/8`,
   `tan²θ_W^GUT = 3/5`, plus the consistency `sin² + cos² = 1`.
6. **Realization-invariance under hypothetical alternatives.** Three
   "alternative realizations" each produce the same `Y_GUT` rescaling
   (matter-content invariant), hence the same `tan²θ_W^GUT = 3/5`,
   hence the same `sin²θ_W^GUT = 3/8`.
7. **Proof-walk audit.** Each row of the §2.2 table is verified to use
   only algebraic-class inputs plus the explicit `(GUT-UNIF)` /
   `(GUT-GRP)` admissions. No row uses Wilson / staggered / BZ-corner /
   link-unitary / lattice-scale / `u_0` / `g_bare` / Monte Carlo / PDG
   content.
8. **Forbidden-import audit.** Stdlib only, no PDG pins.
9. **Boundary check.** RG-running, M_Z value, GUT scale, GUT-group
   uniqueness, and continuum-limit-class predictions all explicitly
   NOT closed.
10. **Sister-PR pattern.** Cross-references to #655, #664, #667, #670
    establish the convention-admission analogue chain.

## 9. Cross-references

- **Parent framing PR:** [#670](https://github.com/jonathonreilly/cl3-lattice-framework/pull/670) — algebraic-universality framing + first sub-piece (hypercharges)
- **Sister PRs (convention-admission ledger):**
  - PR [#655](https://github.com/jonathonreilly/cl3-lattice-framework/pull/655) — SU(5) embedding consistency (sister `(GUT-GRP)`)
  - PR [#664](https://github.com/jonathonreilly/cl3-lattice-framework/pull/664) — A3 substep 4 closure (admits `(LCL)` labelling)
  - PR [#667](https://github.com/jonathonreilly/cl3-lattice-framework/pull/667) — A4 closure (admits `(CKN)` Killing form)
- **Authority being proof-walked:** [`SIN_SQUARED_THETA_W_GUT_FROM_SU5_NOTE_2026-05-02.md`](SIN_SQUARED_THETA_W_GUT_FROM_SU5_NOTE_2026-05-02.md)
- **Companion algebraic upstream:** [`HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md`](HYPERCHARGE_SQUARED_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md) (Y5)
- **GUT-embedding upstream:** [`SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md`](SU5_EMBEDDING_FROM_GRAPH_FIRST_SURFACE_THEOREM_NOTE_2026-05-07.md) (PR #655)
- **Hypercharge-uniqueness upstream:** [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md)
- **A3 realization gate:** [`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md)
- **Minimal axioms parent:** [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
- **Anomaly upstream:** [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md), [`LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md`](LH_ANOMALY_TRACE_CATALOG_THEOREM_NOTE_2026-04-25.md)
- **LH content + RH completion:** [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md), [`HYPERCHARGE_IDENTIFICATION_NOTE.md`](HYPERCHARGE_IDENTIFICATION_NOTE.md)

## 10. Honest scope

**Branch-local theorem + proof-walk.** This note packages the third
sub-piece of the PR #670 algebraic-universality programme: a
proof-walk verification that `sin²θ_W^GUT = 3/8` is
lattice-realization-invariant per PR #670's §2 definition. It surfaces
two physics-side admissions explicitly: `(GUT-UNIF)` (coupling
unification at the GUT scale) and `(GUT-GRP)` (GUT-group choice).
These are NOT new axioms — they are physics-side conventions/assumptions
on the same ledger as `(LCL)` (PR #664), `(CKN)` (PR #667), and PR #655's
SU(5)-vs-SO(10)/E6.

**Not in scope.**

- Wilson's continuum-limit universality theorem.
- Closure of `(GUT-UNIF)`. That would require an RG-running theorem.
- Closure of `(GUT-GRP)`. PR #655 explicitly leaves this open.
- The numerical comparison with PDG `sin²θ_W(M_Z)`. Requires RG running.
- The remaining six follow-on sub-pieces from PR #670 §6.
- The framework's actual realization-uniqueness statement (A3 forces
  staggered-Dirac). This note assumes the canonical realization and
  asks whether the algebraic prediction would survive realization
  variation IF such variation existed.

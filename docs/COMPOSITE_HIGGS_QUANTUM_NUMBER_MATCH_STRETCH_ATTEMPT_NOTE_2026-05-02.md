# Composite-Higgs Quantum Number Match — Stretch Attempt with Named Obstructions

**Date:** 2026-05-02
**Type:** stretch_attempt (output type c)
**Claim scope:** documents a worked stretch attempt at the EWSB Higgs
identification problem (cycle 07's named obstruction). The attempt's
positive partial result is a quantum-number match: the composite
quark bilinear `(q̄_L u_R)|_{color singlet}` from the framework's
cycle 06-derived SM rep has SU(2) × U(1)_Y quantum numbers
**(2̄, 1)_{+1}**, equivalent to the SM Higgs Φ̃ (the conjugate
doublet of the canonical Higgs Φ ~ (2, 1)_{+1}).

This makes the composite quark bilinear a candidate Higgs with the
**right quantum numbers**. It does NOT make the framework's EWSB
mechanism derived — for that, three named obstructions remain (see
§ Named Obstructions).

**Status:** stretch attempt, audit-lane ratification required for any
retained-grade interpretation. This is not a closing derivation.

**Runner:** [`scripts/frontier_composite_higgs_quantum_number_stretch_attempt.py`](./../scripts/frontier_composite_higgs_quantum_number_stretch_attempt.py)

**Authority role:** sharpens cycle 07's named obstruction with a
specific composite-Higgs path and three explicit obstructions for
future research.

## A_min (minimal allowed premise set)

- (P1, sister-derivation cycle 06) Framework's derived SM matter
  representation:

  ```text
  Q_L : (2, 3)_{+1/3}
  L_L : (2, 1)_{-1}
  u_R : (1, 3)_{+4/3}
  d_R : (1, 3)_{-2/3}
  e_R : (1, 1)_{-2}
  ```

- (P2, retained) Native gauge structure SU(3)_c × SU(2)_L × U(1)_Y
  via `NATIVE_GAUGE_CLOSURE_NOTE.md`.

- (P3, admitted-context external) Standard tensor product / fusion
  rule arithmetic for SU(2) and SU(3) representations:

  ```text
  SU(2):  2̄ = ε · 2  (pseudo-real / antifundamental ↔ fundamental)
  SU(2):  2 ⊗ 2̄ = 1 ⊕ 3
  SU(3):  3 ⊗ 3̄ = 1 ⊕ 8
  SU(3):  3 ⊗ 3 = 6 ⊕ 3̄
  ```

  (Elementary SU(N) representation theory.)

- (P4, admitted-context external) Standard SM Higgs Yukawa structure:
  `q̄_L Φ̃ u_R` is the up-quark mass term, `q̄_L Φ d_R` is the
  down-quark mass term, where Φ ~ (2, 1)_{+1}_Y_doubled and
  Φ̃ = i σ_2 Φ* ~ (2, 1)_{-1}_Y_doubled.

## Forbidden imports

- **No PDG values**: m_t, m_H, v_EW, m_W, m_Z are NOT used as
  derivation inputs.
- **No literature numerical comparators**: the top-condensate model's
  prediction `m_t ~ 600 GeV` (Bardeen-Hill-Lindner 1990) is referenced
  ONLY in the named-obstruction documentation as admitted-context
  external authority, not as a derivation comparator.
- **No fitted selectors**.
- **No admitted unit conventions** load-bearing on retention beyond
  the doubled-Y convention shared with cycle 04.
- **No same-surface family arguments**.

## Worked attempt

### Step 1: Compute fermion bilinear quantum numbers

In the LH-conjugate frame (where RH species enter as their
LH-conjugates):

- `q̄_L = (Q_L)*`: SU(2)=2̄, SU(3)=3̄, Y=-1/3
- `l̄_L = (L_L)*`: SU(2)=2̄, SU(3)=1, Y=+1
- `u_R`: SU(2)=1, SU(3)=3, Y=+4/3
- `d_R`: SU(2)=1, SU(3)=3, Y=-2/3
- `e_R`: SU(2)=1, SU(3)=1, Y=-2

The Yukawa-like bilinears `q̄_L · u_R` etc. carry:

- `q̄_L u_R`: SU(2) = 2̄ ⊗ 1 = 2̄; SU(3) = 3̄ ⊗ 3 = 1 ⊕ 8;
  Y = -1/3 + 4/3 = +1
  ⇒ rep `(2̄, 1 ⊕ 8)_{+1}`.
  **Color-singlet piece**: `(2̄, 1)_{+1}` = SM Higgs Φ̃-equivalent.

- `q̄_L d_R`: SU(2) = 2̄; SU(3) = 1 ⊕ 8; Y = -1/3 + (-2/3) = -1
  ⇒ rep `(2̄, 1 ⊕ 8)_{-1}`. Color-singlet piece: `(2̄, 1)_{-1}`.

- `l̄_L e_R`: SU(2) = 2̄; SU(3) = 1 ⊗ 1 = 1; Y = +1 + (-2) = -1
  ⇒ rep `(2̄, 1)_{-1}`.

### Step 2: Verify (2̄, 1)_{+1} = SM Higgs Φ̃ quantum numbers

The SM Higgs Φ has quantum numbers (2, 1)_{+1} in doubled-Y
convention. Its conjugate Φ̃ = i σ_2 Φ* has:

- SU(2): Φ̃ transforms in the conjugate doublet 2̄. Via the SU(2)
  pseudo-reality 2̄ = ε · 2, Φ̃ is also a 2 with adjusted
  conjugation phases. In quantum-number tracking we use 2̄ vs 2
  interchangeably.
- U(1)_Y: Φ̃ has Y_Φ̃ = -Y_Φ = -1, but with conjugate convention
  it appears as +1 in some normalizations.

In the canonical SM Yukawa coupling `q̄_L Φ̃ u_R` (up-quark mass):

- q̄_L: (2̄, 3̄)_{-1/3}
- Φ̃: (2, 1)_{-1} (in the convention where Φ̃ has Y opposite to Φ)
  - But under the pseudo-reality, this is equivalent to (2̄, 1)_{+1}
- u_R: (1, 3)_{+4/3}
- Product: 2̄ × 2 × 1 = 1 ⊕ 3 → contains singlet ✓
  3̄ × 1 × 3 = 1 ⊕ 8 → contains singlet ✓
  Y: -1/3 + (-1) + 4/3 = 0 ✓ → singlet under U(1)_Y ✓

So the Yukawa coupling is gauge-invariant, confirming the
quantum-number assignments. The composite `q̄_L u_R`
color-singlet has the SAME quantum numbers as Φ̃ (in the
matching convention).

**Quantum-number match confirmed.**

### Step 3: Conjugate-Higgs Y-flip note

In one convention, Φ ~ (2, +1) and Φ̃ ~ (2̄, +1) (treating Y as a
charge that flips under conjugation: Y(Φ̃) = -Y(Φ) = -1, but with
2̄ ↔ 2 the "absolute" Y is +1).

In another convention, Φ ~ (2, +1) and Φ̃ ~ (2, -1) (keeping the
fundamental 2 representation but flipping Y).

The framework's doubled-Y convention can use either, but consistency
requires that the Yukawa singlet condition `Y(q̄_L) + Y(Φ̃) +
Y(u_R) = 0` is satisfied. Verified above: 0 = -1/3 + (-1) + 4/3 = 0 ✓.

### Step 4: Counterfactual — wrong-chirality bilinears don't fit

What if we tried `q̄_L Q_L` (LH-LH) or `u_R d_R` (RH-RH)?

- `q̄_L Q_L`: SU(2) = 2̄ ⊗ 2 = 1 ⊕ 3; SU(3) = 3̄ ⊗ 3 = 1 ⊕ 8;
  Y = -1/3 + 1/3 = 0
  Color-singlet, SU(2)-triplet piece: (3, 1)_0 — not a doublet.
  Color-singlet, SU(2)-singlet: (1, 1)_0 — not a doublet either.
  **No (2̄, 1)_{+1} or (2, 1)_{-1} component.**

- `u_R d_R`: SU(2) = 1 ⊗ 1 = 1; SU(3) = 3 ⊗ 3 = 6 ⊕ 3̄;
  Y = +4/3 - 2/3 = +2/3
  No SU(2)-doublet structure ⇒ cannot form a Higgs candidate.

Bilinears with mixed chirality (LH-conjugate × RH) are required for
SU(2)-doublet quantum numbers because the SU(2) singlets don't form
a doublet.

### Step 5: Counterfactual — non-fundamental color paths don't give singlet

What about (q̄_L)_α (Q_L)^α (color-contracted)? That gives a color
singlet but Y=0 and SU(2) = 1 ⊕ 3, not (2, 1)_{+1}. Same as q̄_L
Q_L above, just color-contracted.

The unique SU(2)-doublet × color-singlet × Y=+1 structure comes from
**q̄_L u_R color-singlet piece**.

### Conclusion of attempt: positive partial result

**Composite quark bilinear `(q̄_L u_R)|_{color singlet}` has SM
Higgs Φ̃-equivalent quantum numbers (2̄, 1)_{+1}.**

This is the **leading candidate for a composite Higgs** in the
framework's derived rep. Equivalently: any condensate
`⟨q̄_L u_R⟩ ≠ 0` would trigger EWSB SU(2)_L × U(1)_Y → U(1)_em with
Q = T_3 + Y/2 (from cycle 07).

## Named Obstructions (the stretch attempt's residual gaps)

### Obstruction 1: Mechanism for ⟨q̄_L u_R⟩ ≠ 0

The framework lacks a retained derivation of a nonzero quark
condensate. Standard QCD has `⟨q̄ q⟩` chiral condensate at the QCD
scale, but that's color-singlet `⟨q̄_L q_R⟩` at SU(2) singlet level
(it doesn't break EW symmetry — it breaks chiral SU(2)_L × SU(2)_R
of QCD-like models).

To break EW SU(2)_L × U(1)_Y → U(1)_em, the condensate needs to be
SU(2)_L-doublet-valued. That requires a NEW dynamical mechanism
beyond standard QCD chiral condensation.

**Specific repair target**: derive a strong-coupling sector in the
framework that condenses `q̄_L u_R` with the right quantum numbers
and a specific scale (presumably the EW scale, ~246 GeV).

### Obstruction 2: Top-condensate prediction m_top ~ 600 GeV

In the literature (Bardeen-Hill-Lindner 1990 and follow-ups), the
top-condensate model predicts:

```text
m_top ≈ 600 GeV  (with no fine-tuning)
```

This is too high (observed m_top ≈ 173 GeV). A framework-internal
mechanism would need to **evade this prediction**, perhaps via:

- (a) Multi-channel condensation: not just `⟨q̄_L u_R⟩` but
  additional channels (q̄_L d_R, l̄_L e_R) condensing simultaneously,
  redistributing the EW symmetry breaking across channels.
- (b) Z3 cluster structure (Koide-related): the framework's
  retained Koide work has Z3 scalar potential structure; could that
  modify the top-condensate prediction?
- (c) Additional symmetry that suppresses the top mass — e.g., a
  Z3-symmetric composite condensate.

**Specific repair target**: identify a framework-internal mechanism
that gives `⟨q̄_L u_R⟩ ≠ 0` but with effective Yukawa coupling
consistent with observed m_top ≈ 173 GeV (without using m_top as a
fitting input — instead deriving it from framework primitives).

### Obstruction 3: Multi-bilinear selector

Three bilinears have matching SU(2) × U(1)_Y quantum numbers for the
Higgs role:

- `(q̄_L u_R)|_{singlet}`: (2̄, 1)_{+1} — Φ̃-equivalent
- `(q̄_L d_R)|_{singlet}`: (2̄, 1)_{-1} — Φ-equivalent
- `(l̄_L e_R)`: (2̄, 1)_{-1} — Φ-equivalent

Without an additional selector, the framework cannot uniquely
identify WHICH bilinear plays the Higgs role. In the SM, a
fundamental Higgs Φ couples to all three via different Yukawa
coefficients; in a composite picture, a unique condensate would need
to be selected.

**Specific repair target**: derive the selection mechanism that
picks one bilinear (or a specific combination) as the dominant
Higgs-like condensate. Candidates:

- (a) Renormalization-group flow + most-attractive-channel argument
  (literature: Raby-Dimopoulos-Susskind 1980)
- (b) Top-Yukawa dominance → `(q̄_L u_R)` is the leading channel
- (c) Framework-specific selection from Koide / Z3 cluster

## Possible future paths (not pursued in this stretch attempt)

For future cycles or research:

1. **Z3 + condensate combined model**: the framework's Z3 scalar
   potential (Koide cluster) provides a 3-state scalar dynamics. Could
   that 3-state potential mix with quark bilinears in a way that
   produces an effective (2, 1)_{+1} Higgs?

2. **Lattice strong-coupling regime**: at strong coupling on the
   lattice, fermion bilinears can condense (Wilson loops + chiral
   condensates). Identify framework conditions that produce
   EW-symmetry-breaking condensates rather than QCD chiral
   condensates.

3. **Composite Higgs via Coleman-Weinberg + composite scalars**: the
   framework's retained CW EWSB / naturalness work
   (`HIGGS_MECHANISM_NOTE` parent) might be reinterpreted with the
   composite Higgs ansatz.

## What this claims

- `(P1)` Quantum-number match: `(q̄_L u_R)|_{color singlet}` has SM
  Higgs Φ̃-equivalent quantum numbers (2̄, 1)_{+1} on the framework's
  derived rep.
- `(P2)` Counterfactual: bilinears with wrong chirality (LH-LH or
  RH-RH) lack SU(2)-doublet structure.
- `(P3)` Named obstructions documented: (1) mechanism for nonzero
  condensate, (2) top-condensate m_top ~ 600 GeV prediction, (3)
  multi-bilinear selector ambiguity.

## What this does NOT claim

- Does NOT close the unconditional EWSB Higgs identification — that
  requires resolving all three named obstructions.
- Does NOT prove `⟨q̄_L u_R⟩ ≠ 0` in the framework. The framework's
  current native surface gives no such condensate (cf. Majorana
  no-go companion notes).
- Does NOT predict m_top, m_H, or v_EW — those are downstream of the
  unidentified mechanism.
- Does NOT evaluate the literature top-condensate models against the
  framework — those are external.
- Does NOT promote any author-side tier; audit-lane ratification is
  required.

## Cited dependencies

- (P1, sister-derivation cycle 06) [`SM_REP_DERIVED_MAJORANA_NULL_SPACE_THEOREM_NOTE_2026-05-02.md`](SM_REP_DERIVED_MAJORANA_NULL_SPACE_THEOREM_NOTE_2026-05-02.md).
- (P2) [`NATIVE_GAUGE_CLOSURE_NOTE.md`](NATIVE_GAUGE_CLOSURE_NOTE.md) — retained.
- (P3) Standard SU(N) representation theory (admitted-context
  external).
- (P4) Peskin-Schroeder 1995 ch. 20 — admitted-context external SM
  Higgs Yukawa.
- Bardeen-Hill-Lindner 1990 — admitted-context external (cited only
  in obstruction documentation, not as derivation input).

## Forbidden imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed (m_top ~ 600 GeV is
  cited in obstruction documentation, role-labelled admitted-context
  external).
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention.
- No same-surface family arguments.

## Validation

Primary runner: [`scripts/frontier_composite_higgs_quantum_number_stretch_attempt.py`](./../scripts/frontier_composite_higgs_quantum_number_stretch_attempt.py)
verifies (PASS=13/0, exact rational arithmetic + SU(2)/SU(3) fusion):

1. q̄_L u_R: SU(2)=2̄, SU(3)=1⊕8, Y=+1; color-singlet has Φ̃ quantum numbers.
2. q̄_L d_R: (2̄, 1⊕8)_{-1}; color-singlet matches Φ Y=-1.
3. l̄_L e_R: (2̄, 1)_{-1}; matches Φ Y=-1.
4. Counterfactual: q̄_L Q_L (LH-LH) gives (1⊕3, 1⊕8)_0 — no doublet.
5. Counterfactual: u_R d_R (RH-RH) gives (1, 6⊕3̄)_{+2/3} — no doublet.
6. Yukawa singlet condition q̄_L Φ̃ u_R: 0 + 0 + 0 = 0 ✓ — confirms
   Φ̃ quantum numbers match.
7. Color-singlet projection from 3̄⊗3 = 1⊕8.
8. Multi-bilinear comparison: 3 candidates with matching quantum numbers.

## Cross-references

- [`CONDITIONAL_EWSB_Q_FORMULA_ON_DERIVED_REP_THEOREM_NOTE_2026-05-02.md`](CONDITIONAL_EWSB_Q_FORMULA_ON_DERIVED_REP_THEOREM_NOTE_2026-05-02.md) —
  cycle 07: provides the conditional theorem and original named
  obstruction this PR sharpens.
- [`SM_REP_DERIVED_MAJORANA_NULL_SPACE_THEOREM_NOTE_2026-05-02.md`](SM_REP_DERIVED_MAJORANA_NULL_SPACE_THEOREM_NOTE_2026-05-02.md) —
  cycle 06: provides the derived rep used here.
- [`HIGGS_MECHANISM_NOTE.md`](HIGGS_MECHANISM_NOTE.md) — parent row
  whose verdict the cycle 07 + cycle 08 pair sharpens.
- [`NEUTRINO_MAJORANA_NATIVE_GAUSSIAN_NO_GO_NOTE.md`](NEUTRINO_MAJORANA_NATIVE_GAUSSIAN_NO_GO_NOTE.md) —
  companion no-go showing framework's current native surface gives
  zero condensate (relevant to Obstruction 1).
- Bardeen-Hill-Lindner 1990 — admitted-context external on
  top-condensate m_top prediction.
- Raby-Dimopoulos-Susskind 1980 — admitted-context external on
  most-attractive-channel arguments.

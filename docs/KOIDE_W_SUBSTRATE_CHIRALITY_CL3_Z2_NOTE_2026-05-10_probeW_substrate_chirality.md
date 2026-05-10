# Probe W-Substrate-Chirality — Cl(3) Z_2 Grading does NOT Force SM LH/RH Split (probeW_substrate_chirality)

**Date:** 2026-05-10
**Type:** bounded_theorem (mostly negative; cited positive sub-rows on
Cl⁺(3) ≅ H exact-algebra reading already retained)
**Claim type:** bounded_theorem
**Status authority:** independent audit lane only; effective status is
pipeline-derived. This is a source-note proposal; the audit lane has
full authority to retag, narrow, or reject the proposed bounded label.
**Source-note proposal disclaimer:** this note is a source-note
proposal; audit verdict and downstream status are set only by the
independent audit lane. The author does NOT propose retained /
positive_theorem promotion.

**Primary runner:** [`scripts/cl3_koide_w_substrate_chirality_2026_05_10_probeW_substrate_chirality.py`](../scripts/cl3_koide_w_substrate_chirality_2026_05_10_probeW_substrate_chirality.py)
**Cached output:** [`logs/runner-cache/cl3_koide_w_substrate_chirality_2026_05_10_probeW_substrate_chirality.txt`](../logs/runner-cache/cl3_koide_w_substrate_chirality_2026_05_10_probeW_substrate_chirality.txt)

## 0. Probe context

Sister Probe Y-Substrate-Anomaly
([`KOIDE_Y_SUBSTRATE_ANOMALY_FORCING_NOTE_2026-05-08_probeY_substrate_anomaly.md`](KOIDE_Y_SUBSTRATE_ANOMALY_FORCING_NOTE_2026-05-08_probeY_substrate_anomaly.md))
identified five admissions NOT forced by SM gauge anomaly cancellation
alone:

1. `N_c = 3` (closed positively by sister Probe Z-Substrate-Color-Geometric
   on dim-counting `N_c² − 1 = 8 ⇒ N_c = 3`)
2. `n_gen = 3` (closed positively by sister Probe Z-Substrate-Generation-Z3
   on cardinality `card(Z^3 / 3Z^3) = 27 ⇒ 3 generations`)
3. **left-handed content choice** (vectorlike vs Pati-Salam vs SM
   vs trinification vs SU(5) 5̄+10) — **REMAINS OPEN**
4. absolute hypercharge scale (convention boundary, retained)
5. the A1-condition (separate row, retained as bounded admission)

This probe asks the natural follow-up:

> **Question (Probe W).** Cl(3) carries a real Z_2 grading
> `Cl(3) = Cl⁺(3) ⊕ Cl⁻(3)` (even ⊕ odd parts, distinguished by the
> grade involution `α(γ_i) = -γ_i`). The even subalgebra
> `Cl⁺(3) ≅ H` (quaternions) carries a natural SU(2) (its
> unit-group). The odd part `Cl⁻(3) = span{γ_1, γ_2, γ_3, ω}`
> is also 4-dimensional and carries no Lie-group structure inside
> itself. Does this Z_2 grading FORCE the Standard Model
> left-handed/right-handed split — specifically, does it FORCE the
> identification "LH ↔ Cl⁺(3) carrying SU(2)_L" while excluding
> alternatives like Pati-Salam (LH ↔ Cl⁺(3) AND RH ↔ Cl⁺(3) too,
> giving SU(2)_L × SU(2)_R)?

The hypothesis under test is that Cl(3)'s natural Z_2 grading is a
sufficient structural input to break the LH content degeneracy
identified in Probe Y-Neg-C, converting "LH content choice" from a
retained admission into a derived output.

## 1. Theorem (bounded, mostly negative; positive retentions on
already-closed sub-rows)

**Theorem (W-Substrate-Chirality; bounded).** On retained Cl(3)/Z^3
content, the Cl(3) real Z_2 grading
`Cl(3) = Cl⁺(3) ⊕ Cl⁻(3)` does NOT force the SM LH/RH split. Specifically:

1. **(W-Pos-1) Cl⁺(3) ≅ H exact-algebra reading (already-positive).**
   The even subalgebra `Cl⁺(3) = span_R{I, e_{12}, e_{13}, e_{23}}`
   with `e_{ij} := γ_i γ_j` is isomorphic to the real quaternion
   algebra `H` as a real associative algebra:
   `e_{ij}² = -I`, `e_{12} e_{13} = e_{23}`, etc. Its unit-group
   `{q ∈ Cl⁺(3) : q q* = I}` is the abstract group `SU(2) ≅ Sp(1)`.
   **This is the existing exact-algebra support theorem
   `CL3_SM_EMBEDDING_THEOREM`** (sections A, B). Probe W does not
   strengthen this row; it cites it as the algebraic fact about the
   even subalgebra.
2. **(W-Pos-2) Two non-isomorphic complex Cl(3) chirality irreps
   (already-positive).** The complexification
   `Cl(3) ⊗_R C ≅ M_2(C) ⊕ M_2(C)` decomposes into two simple
   summands distinguished by the central pseudoscalar
   `ω = γ_1 γ_2 γ_3` taking eigenvalue `+i` (positive-chirality
   summand `ρ_+`) or `-i` (negative-chirality summand `ρ_-`). Each
   summand is a faithful 2-dim irrep, and they are not unitarily
   equivalent to each other. **This is the existing per-site
   uniqueness theorem `AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM`**
   (chirality-aware repair 2026-05-03, U2/U3). Probe W does not
   strengthen this row.

Cl(3)'s Z_2 grading does NOT force, on the retained Cl(3)/Z^3
substrate alone:

3. **(W-Neg-A) Cl⁺(3) sits identically in BOTH chirality summands.**
   The even subalgebra `Cl⁺(3) ⊂ Cl(3)` is invariant under the grade
   involution `α : γ_i ↦ -γ_i`. Since `α` is what distinguishes the
   two chirality summands `ρ_±` (it swaps them), Cl⁺(3) is preserved
   pointwise by `α` and therefore embeds isomorphically into both
   summands. Concretely, in the Pauli-rep `γ_i ↦ σ_i` we have
   `e_{ij} = γ_i γ_j ↦ σ_i σ_j`, while in the parity-conjugate rep
   `γ_i ↦ -σ_i` we have `e_{ij} ↦ (-σ_i)(-σ_j) = σ_i σ_j` — same
   operator. Both summands carry the same Cl⁺(3), hence the same
   abstract SU(2). **There is no Z_2-grading mechanism inside Cl(3)
   that gives an SU(2) to one chirality summand and not the other.**

4. **(W-Neg-B) Pati-Salam SU(2)_L × SU(2)_R is fully consistent with
   Cl(3) Z_2 grading.** Because Cl⁺(3) embeds identically in both
   chirality summands (W-Neg-A), the natural assignment "LH carries
   the Cl⁺(3) SU(2)" generalizes immediately to "LH and RH each
   carry their own copy of the Cl⁺(3) SU(2)" — that is, exactly the
   Pati-Salam structure SU(2)_L × SU(2)_R. The Z_2 grading does not
   distinguish the SM choice (only LH carries SU(2)) from the
   Pati-Salam choice (both LH and RH carry their own SU(2)). The
   selection of the SM choice over Pati-Salam is forced not by
   Cl(3) Z_2 grading but by an external choice — typically the
   choice that the gauge field is supplied only on one chirality
   summand (a gauge-field-side input, not a substrate-side input).

5. **(W-Neg-C) The SM choice "RH is SU(2) singlet" is a separate
   admission.** The SM matter content
   `Q_L : (3, 2)_{1/3}, L_L : (1, 2)_{-1}, u_R : (3, 1)_{4/3},
   d_R : (3, 1)_{-2/3}, e_R : (1, 1)_{-2}, ν_R : (1, 1)_0`
   has the property that LH fields are SU(2)-doublets and RH fields
   are SU(2)-singlets. This LH-doublet/RH-singlet split is a
   **gauge-content admission**, not a consequence of Cl(3) Z_2
   grading. The Z_2 grading is symmetric in LH/RH at the level of
   substrate algebra; the asymmetry in which sector carries the SU(2)
   gauge field is supplied externally.

6. **(W-Neg-D) Per-site Pauli rep has NO γ_5 chirality projector.**
   On a single 2-dim Cl(3) chirality summand (per-site Hilbert
   `H_x ≅ C^2`), the volume element `ω = i·I_2` is central. There
   is no element of `M_2(C)` that anticommutes with all three
   Cl(3) generators `σ_i`, hence no per-site `γ_5` candidate
   satisfying `γ_5² = +I_2` with `{γ_5, σ_i} = 0`. **This is the
   existing no-go theorem `NO_PER_SITE_CHIRALITY_THEOREM_NOTE_2026-05-02`.**
   The Cl(3) Z_2 grading is therefore invisible inside one chirality
   summand: it manifests only as the global choice between `ρ_+`
   and `ρ_-`, not as an internal projector. This precludes a
   per-site γ_5-based LH/RH split mechanism on the Cl(3) substrate.

7. **(W-Neg-E) Alternative LH-content embeddings into Cl(3) Z_2 are
   admissible.** Beyond the SM and Pati-Salam, the following all
   admit Z_2-graded embeddings:
   - **Vectorlike:** assign LH and RH to the same chirality summand,
     with paired representations `R + R̄` cancelling all gauge
     anomalies trivially.
   - **Trinification SU(3)_L × SU(3)_R × SU(3)_C:** generalizes the
     Pati-Salam pattern by carrying separate SU(3)'s on each
     chirality summand instead of separate SU(2)'s; consistent with
     graph-first SU(3) on either summand.
   - **B-L extension:** symmetric U(1)_{B-L} on both summands
     plus mirror SU(2) — consistent with Z_2 grading.
   - **SU(5) 5̄ + 10:** single chirality summand carries the full
     anomaly-free 5̄ + 10 content; the second summand is empty or
     vectorlike.
   In each case, Cl(3)'s Z_2 grading is consistent. The grading
   alone admits multiple LH content choices.

The bounded label records the positive sub-rows (W-Pos-1, W-Pos-2
already on the retained surface) plus the negative obstructions
(W-Neg-A through W-Neg-E unforced by Cl(3) Z_2 grading alone).

## 2. Honest scope and named admissions

**Bounded admissions (records of negative findings, not new admissions
to the framework):**

- **B-Neg-A.** Cl⁺(3) sits identically in both chirality summands;
  the grade involution `α` does not distinguish where SU(2) acts.
- **B-Neg-B.** Pati-Salam SU(2)_L × SU(2)_R is consistent with Cl(3)
  Z_2 grading; the SM choice is not forced by Z_2 alone.
- **B-Neg-C.** The "RH is SU(2)-singlet" SM choice is a gauge-content
  admission, distinct from Cl(3) Z_2 grading.
- **B-Neg-D.** No per-site γ_5 projector exists in the complex Pauli
  rep; the Z_2 grading is invisible inside one chirality summand
  (cited from NO_PER_SITE_CHIRALITY_THEOREM_NOTE_2026-05-02).
- **B-Neg-E.** Alternative embeddings (vectorlike, trinification,
  B-L+mirror, SU(5) 5̄+10) all consistent with Cl(3) Z_2 grading.

**Positive sub-rows already retained (cited, not strengthened):**

- **W-Pos-1.** Cl⁺(3) ≅ H exact-algebra reading — already exact-algebra
  support theorem on `main` (`CL3_SM_EMBEDDING_THEOREM`).
- **W-Pos-2.** Two non-isomorphic chirality irreps `ρ_±` — already
  retained per-site uniqueness theorem
  (`AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM`, U2/U3).

The probe's contribution is the **explicit identification** of which
substrate-to-carrier admissions Cl(3) Z_2 grading reaches and which
it does not, in a single bounded source note. This sharpens Probe Y's
"LH content choice unforced" row by ruling out the natural Z_2-grading
candidate as the load-bearing structural input.

This note does NOT use:
- PDG observed masses, charges, mixing angles
- New repo-wide axioms
- Lattice MC empirical measurements
- Fitted matching coefficients
- HK + DHR appeal (Block 01 audit retired this; respected)
- Same-surface family arguments

## 3. Setup

### 3.1 Retained inputs (Cl(3)/Z^3 baseline + cited theorems)

| Ingredient | Authority |
|---|---|
| Cl(3)/Z^3 native primitive structure | [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) |
| Per-site Cl(3) chirality decomposition | [`AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md) |
| Cl⁺(3) ≅ H exact-algebra reading | [`CL3_SM_EMBEDDING_THEOREM.md`](CL3_SM_EMBEDDING_THEOREM.md) |
| No per-site γ_5 in Pauli rep | [`NO_PER_SITE_CHIRALITY_THEOREM_NOTE_2026-05-02.md`](NO_PER_SITE_CHIRALITY_THEOREM_NOTE_2026-05-02.md) |
| Fermion parity Z_2 grading (Fock space) | [`FERMION_PARITY_Z2_GRADING_THEOREM_NOTE_2026-05-02.md`](FERMION_PARITY_Z2_GRADING_THEOREM_NOTE_2026-05-02.md) |
| Sister probe: anomaly forcing (negative on LH content) | [`KOIDE_Y_SUBSTRATE_ANOMALY_FORCING_NOTE_2026-05-08_probeY_substrate_anomaly.md`](KOIDE_Y_SUBSTRATE_ANOMALY_FORCING_NOTE_2026-05-08_probeY_substrate_anomaly.md) |
| Standard Clifford grade-involution structure | textbook ([Lawson-Michelsohn, *Spin Geometry*]) |

### 3.2 Z_2 grading on Cl(3)

The Clifford algebra `Cl(3) = Cl(R³, +)` carries a canonical real Z_2
grading defined by the grade involution

```text
   α : Cl(3) → Cl(3),    α(γ_i) := -γ_i,    α(αβ) := α(α) α(β).         (1)
```

This decomposes `Cl(3) = Cl⁺(3) ⊕ Cl⁻(3)` where:

| Subspace | Basis (over R) | Dim_R | Contents |
|---|---|---|---|
| Cl⁺(3) | {1, e_{12}, e_{13}, e_{23}} | 4 | grade-0 (scalar) ⊕ grade-2 (bivectors) |
| Cl⁻(3) | {γ_1, γ_2, γ_3, ω} | 4 | grade-1 (vectors) ⊕ grade-3 (pseudoscalar) |

Total real dim = 8 = `2³`, matching `dim_R Cl(R^n) = 2^n`.

### 3.3 Cl⁺(3) ≅ H structural fact

The bivectors `e_{ij} := γ_i γ_j` satisfy:

- `e_{ij}² = γ_i γ_j γ_i γ_j = -γ_i² γ_j² = -1` (using `γ_iγ_j = -γ_jγ_i` for `i≠j`),
- closed quaternionic products (verified at machine precision in the
  runner) `e_{23} · e_{13} = e_{12}`, `e_{13} · e_{12} = e_{23}`,
  `e_{12} · e_{23} = e_{13}`,
- equivalently with the basis `i := e_{23}, j := e_{13}, k := e_{12}` we
  have `i² = j² = k² = -1, ij = k, jk = i, ki = j` — exactly the
  quaternion algebra H.

The unit-group `{q ∈ Cl⁺(3) : q q* = 1}` (with conjugation `q* := α(q^t)`)
is `SU(2) ≅ Sp(1)`. **This SU(2) is the structural origin of the
Cl⁺(3) SU(2) cited by `CL3_SM_EMBEDDING_THEOREM`.**

### 3.4 Two complex chirality summands

Complexifying, the central pseudoscalar `ω` satisfies `ω² = -I`, so
`ω` has eigenvalues `±i`. The complexification splits

```text
   Cl(3) ⊗_R C  =  M_2(C)_+  ⊕  M_2(C)_-                              (2)
```

with `M_2(C)_±` the eigenspaces of `ω`. Each summand is a faithful
2-dim irrep of Cl(3), and they are parity-conjugate of each other
(swapped by `α`).

### 3.5 What the probe tests

The probe tests whether the structural Z_2 grading (1) plus the
chirality split (2) forces:
- (W-Test-1) SU(2) acts on exactly one chirality summand (LH only).
- (W-Test-2) Pati-Salam structure SU(2)_L × SU(2)_R is excluded.
- (W-Test-3) The grade involution α distinguishes "doublet" from "singlet"
  representation type at the substrate level.

If any of these three holds, the probe is positive (Cl(3) Z_2 grading
forces SM LH/RH split). If all three fail, the probe is negative
(Cl(3) Z_2 grading admits multiple choices). The verdict below is
that all three FAIL, hence the negative bounded outcome.

## 4. Proof of negative findings

### Step 1 — Cl⁺(3) embeds identically in BOTH chirality summands (W-Neg-A)

In the canonical Pauli rep of `ρ_+`: `γ_i ↦ σ_i`.
In the parity-conjugate rep of `ρ_-`: `γ_i ↦ -σ_i`.

For any bivector basis element of Cl⁺(3):

```text
   ρ_+(e_{ij})  =  σ_i σ_j                                              (3a)
   ρ_-(e_{ij})  =  (-σ_i)(-σ_j)  =  σ_i σ_j.                            (3b)
```

The bivector image is **identical** in both summands. Therefore
`ρ_+(Cl⁺(3)) = ρ_-(Cl⁺(3))` as operator algebras inside `M_2(C)`.
The Cl⁺(3) SU(2) acts identically on both chirality summands. ∎

### Step 2 — Pati-Salam SU(2)_L × SU(2)_R is consistent with Cl(3) Z_2 (W-Neg-B)

Take the framework's full per-site state space to be one copy of
`ρ_+` plus one copy of `ρ_-` (a "vectorlike per-site"). By Step 1,
both summands carry an SU(2) acting via the bivector basis. We can
gauge:

- Option (SM): gauge SU(2) on `ρ_+` only, leaving `ρ_-` ungauged
  (RH singlet).
- Option (PS): gauge SU(2) independently on `ρ_+` and on `ρ_-`,
  giving SU(2)_L × SU(2)_R.

Both options are consistent with the Z_2 grading. The grading does
not specify which gauge couplings are physical. ∎

### Step 3 — Per-site γ_5 does not exist (W-Neg-D, cited)

By `NO_PER_SITE_CHIRALITY_THEOREM_NOTE_2026-05-02`, on the per-site
Pauli rep `H_x ≅ C^2`, the volume element `ω = i·I_2` is central,
and there is no element `γ_5 ∈ M_2(C)` satisfying `γ_5² = +I_2` with
`{γ_5, σ_i} = 0`. The Z_2 grading is invisible internally — it is
realized only globally by the choice of summand `ρ_+` vs `ρ_-`. ∎

### Step 4 — Multiple anomaly-free LH embeddings are Z_2-consistent (W-Neg-E)

For each alternative content choice X ∈ {vectorlike, Pati-Salam,
trinification, B-L extension, SU(5) 5̄+10}, we exhibit a Z_2-graded
embedding into Cl(3)-style chirality decomposition:

- **Vectorlike (R + R̄):** assign R to ρ_+, R̄ to ρ_-. Anomaly-free
  by construction. Z_2-consistent (one summand each).
- **Pati-Salam:** assign LH multiplet to ρ_+, RH multiplet to ρ_-,
  gauge SU(2) on each independently (Step 2).
- **Trinification SU(3)³:** by sister Probe Z-Substrate-Color-Geometric,
  Cl(3) carries SU(3) on its 8-dim adjoint via dim-counting
  `8 = 3² − 1`. Trinification gauges SU(3) separately on left,
  right, and color sectors; Z_2 grading admits this if all three
  SU(3)'s embed via the same Cl(3) graded basis structurally.
- **B-L + mirror:** gauge mirror SU(2) on ρ_- with U(1)_{B-L}
  symmetric on both summands.
- **SU(5) 5̄+10:** assign full 5̄+10 to one chirality summand;
  the second is empty or vectorlike. Z_2 trivially consistent.

Each of these is anomaly-free (per Probe Y-Neg-C catalog) and
Z_2-consistent. Therefore Cl(3) Z_2 grading admits at least 5
distinct LH-content choices. ∎

## 5. Out of scope

This note does NOT claim:

- A retained-grade derivation of "RH is SU(2) singlet" from the
  Cl(3) Z_2 grading or any other substrate primitive. That selection
  remains the bounded admission identified in Probe Y-Neg-C.
- A ruling on whether some OTHER substrate-side mechanism (e.g.
  graph-first selector, or a separate spin-statistics argument)
  could close this gap. This probe scopes only to the Z_2 grading
  candidate.
- A retained-grade closure of the SM hypercharge convention scale.
  That row is convention-bounded per
  [`LEFT_HANDED_CHARGE_MATCHING_NOTE.md`](LEFT_HANDED_CHARGE_MATCHING_NOTE.md).
- A substrate-side derivation of any specific RH neutrino content
  (`ν_R = (1,1)_0` is convention-bounded per
  [`ONE_GENERATION_MATTER_CLOSURE_NOTE.md`](ONE_GENERATION_MATTER_CLOSURE_NOTE.md)).

## 6. Forbidden imports respected

- NO PDG observed values used as derivation input
- NO lattice MC empirical measurements
- NO fitted matching coefficients
- NO new axioms (probe is constrained to retained Cl(3)/Z^3 baseline +
  textbook Clifford algebra grade-involution structure)
- NO HK + DHR appeal (Block 01 audit retired this; respected)
- NO same-surface family arguments

All derivations use exact-algebra reasoning on `Cl(3) = Cl(R³)` plus
the retained chirality-aware uniqueness theorem and the cited no-go
on per-site γ_5.

## 7. Honest verdict

**Verdict: BOUNDED MOSTLY-NEGATIVE.** The hypothesis "Cl(3) Z_2
grading FORCES SM LH/RH split" is **NOT SUPPORTED**. The Z_2 grading
admits at least the SM choice, the Pati-Salam choice, vectorlike,
trinification, B-L+mirror, and SU(5) 5̄+10. The probe identifies the
structural reason: Cl⁺(3) embeds identically in both chirality
summands, so the grading is symmetric in LH/RH and cannot
distinguish "doublet" from "singlet" representation type.

This sharpens Probe Y-Neg-C ("LH content unforced by anomaly") by
adding: "and not forced by Cl(3) Z_2 grading either". The substrate-
side admission for LH content choice remains an open campaign-target
gap; closing it requires a non-Z_2 substrate-side mechanism (or
remains a retained admission).

```yaml
claim_type_author_hint: bounded_theorem
claim_scope: |
  Cl(3) real Z_2 grading Cl⁺(3) ⊕ Cl⁻(3), with Cl⁺(3) ≅ H carrying
  abstract SU(2), does NOT force the SM LH/RH split. Cl⁺(3) embeds
  identically in both chirality summands ρ_±, hence cannot
  distinguish where SU(2) acts (SM vs Pati-Salam admit equivalent
  Z_2-graded embeddings); per-site γ_5 does not exist in the complex
  Pauli rep (cited NO_PER_SITE_CHIRALITY); 5 alternative LH
  embeddings (vectorlike, PS, trinification, B-L+mirror, SU(5))
  all Z_2-consistent.
upstream_dependencies:
  - axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29
  - cl3_sm_embedding_theorem
  - no_per_site_chirality_theorem_note_2026-05-02
  - fermion_parity_z2_grading_theorem_note_2026-05-02
  - koide_y_substrate_anomaly_forcing_note_2026-05-08_probeY_substrate_anomaly
admitted_context_inputs:
  - standard Clifford grade-involution structure (Lawson-Michelsohn)
  - quaternion algebra structure of Cl⁺(3) (textbook)
```

# Cl(3) Yukawa Casimir-Difference Bridge — Candidate Lemma Note

**Date:** 2026-04-25
**Status:** **support, not closure.** Articulates the Yukawa Casimir-difference
candidate lemma precisely, establishes the retained algebraic pieces
(RHS computation from retained gauge structure), and identifies the
specific structural derivation gap that a closure of `Q_l = 2/3` would
need to fill. Does **not** close `P_Q = |b|²/a² = 1/2`.
**Runner:** `scripts/frontier_cl3_yukawa_casimir_difference_bridge_candidate.py`

---

## 0. Purpose

The charged-lepton Q-side primitive on `main` is

```text
P_Q := |b|² / a² = 1/2     ⇔     a² = 2|b|²     ⇔     Q_l = 2/3.
```

The Q-bridge single-primitive note
([`KOIDE_Q_BRIDGE_SINGLE_PRIMITIVE_NOTE_2026-04-22.md`](KOIDE_Q_BRIDGE_SINGLE_PRIMITIVE_NOTE_2026-04-22.md))
records three retained "support faces" all giving the value `1/2`:

```text
F_dim:   dim(spinor) / dim(Cl⁺(3))                 = 2/4     = 1/2
F_T:     T(T+1) − Y²                                          = 1/2
F_TY:    (T(T+1) − Y²) / (T(T+1) + Y²)                        = 1/2
```

These are explicitly classified as support faces, not closures, because
the **physical bridge** from the abstract Cl(3)/gauge identities to the
**concrete Brannen circulant Hermitian moduli** `(a, b)` of the lepton
Yukawa amplitude is not derived. The primitive `P_Q = 1/2` remains open.

This note adds two things to the existing Q-bridge support stack:

1. **Sharpens** the candidate physical bridge into a single named lemma
   (the Yukawa Casimir-difference lemma).
2. **Establishes** the RHS of the lemma as a retained algebraic
   identity from `CL3_SM_EMBEDDING_THEOREM` for the lepton L doublet.

It does **not** close `P_Q = 1/2`. The structural derivation chain that
takes `T(T+1) − Y²` from gauge-Casimir-space into the lepton-flavor-space
amplitude moduli `(a, |b|)` remains open.

---

## 1. Retained algebraic pieces

### 1.1 RHS = `T(T+1) − Y² = 1/2` from retained gauge structure

From [`CL3_SM_EMBEDDING_THEOREM.md`](CL3_SM_EMBEDDING_THEOREM.md):

| Quantity | Retained value | Source |
|---|---|---|
| `T = 1/2` for SU(2)_L doublet | exact | §A: Cl⁺(3) ≅ ℍ → SU(2)_L generators `J_k`, Casimir `J_1² + J_2² + J_3² = (3/4)I` (spin-1/2) |
| `Y = −1/2` for left-handed lepton doublet | exact | §E: Y eigenvalue assignment on `P_antisymm ⊗ fiber` (lepton L block) |
| `T(T+1) = (1/2)(3/2) = 3/4` | exact | direct from `T = 1/2` |
| `Y² = (−1/2)² = 1/4` | exact | direct from `Y = −1/2` |
| `T(T+1) − Y² = 3/4 − 1/4 = 1/2` | exact | direct subtraction |

So **RHS = 1/2 is retained** as an algebraic identity on the lepton L
doublet, derived from `CL3_SM_EMBEDDING_THEOREM` plus the SM hypercharge
assignment `Y_L = −1/2`.

### 1.2 LHS = `|b|² / a²` is the Brannen circulant primitive

From [`KOIDE_Q_BRIDGE_SINGLE_PRIMITIVE_NOTE_2026-04-22.md`](KOIDE_Q_BRIDGE_SINGLE_PRIMITIVE_NOTE_2026-04-22.md):

Define `(a, b)` as the standard `C_3`-circulant Hermitian moduli of the
charged-lepton Yukawa amplitude on the retained `hw=1` triplet:

```text
H_cyc = (r_0/3) B_0 + (r_1/6) B_1 + (r_2/6) B_2,
a := r_0/3,
b := (r_1 + i r_2)/6.
```

Equivalently, `(a₀, z)` are the `C_3` character components of the
mass-square-root vector `v = (√m_1, √m_2, √m_3)`, and the Brannen
parameter `c = 2|b|/a`. The primitive is:

```text
P_Q := |b|² / a² = 1/2     ⇔     a² = 2|b|²     ⇔     c = √2     ⇔     Q_l = 2/3.
```

### 1.3 Three support faces all give 1/2 — algebraic agreement

| Face | LHS expression | Computed value | At `d = 3` retained inputs |
|---|---|---|---|
| `F_dim` | `dim(spinor) / dim(Cl⁺(3))` | `2/4 = 1/2` | `dim(spinor of ℍ) = 2`, `dim(Cl⁺(3)) = 4` (CL3_SM_EMBEDDING §A) |
| `F_T`   | `T(T+1) − Y²`                | `3/4 − 1/4 = 1/2` | `T = 1/2`, `Y = −1/2` for lepton L (above) |
| `F_TY`  | `(T(T+1) − Y²) / (T(T+1) + Y²)` | `(1/2) / 1 = 1/2` | same |

All three retained algebraic identities give `1/2`. The Q-bridge note
shows they collapse to a single primitive `P_Q = 1/2`.

This note adds the precise structural relation between them:

> **Algebraic-faces compositional identity.** All three support faces
> reduce to the same retained Cl(3) algebraic invariant
>
> ```text
> (dim(SU(2)_L) − dim(U(1)_Y central direction)) / dim(Cl⁺(3))
>    = (3 − 1) / 4 = 1/2,
> ```
>
> using `dim(SU(2)_L) = 3` (three bivector generators of Cl⁺(3)),
> `dim(U(1)_Y central direction) = 1` (the pseudoscalar `ω`), and
> `dim(Cl⁺(3)) = 4` (full even sub-algebra).

This consolidates the three support faces into a single Cl(3)
sub-algebra dimension count. Verified algebraically in the runner §1.

---

## 2. The candidate Yukawa Casimir-difference lemma

> **Candidate Lemma (Yukawa Casimir-difference for charged leptons).**
> The Brannen circulant moduli of the charged-lepton Yukawa amplitude
> on the retained `hw=1` triplet satisfy
>
> ```text
> |b|² / a² = T(T+1) − Y²
> ```
>
> with `T = 1/2`, `Y = −1/2` from the retained lepton L doublet
> assignment (`CL3_SM_EMBEDDING_THEOREM` §E). Both sides equal `1/2`,
> giving `P_Q = 1/2` and hence `Q_l = 2/3`.

The lemma is a **candidate physical bridge**: it asserts that the
flavor-space amplitude moduli `(a, |b|)` are determined by the
gauge-Casimir difference of the host doublet. If retained, it would close
the Q-side primitive on retained gauge structure inputs.

It is **not derived in this note**. Both sides equal `1/2` numerically
on retained data, but the structural identification — i.e., the
analytic chain showing that the framework's physical Yukawa amplitude
moduli ARE this gauge Casimir difference — is the missing closure step.

---

## 3. The specific gap that remains open

The candidate lemma needs a **structural derivation chain** of the form:

```text
retained Cl(3)/Z³ + lepton-doublet identification
  → physical Yukawa coupling matrix Y_e on retained hw=1 triplet
  → C_3-Plancherel decomposition of Y_e
  → singlet amplitude a, doublet amplitude b
  → |b|² / a² = (some retained gauge-Casimir invariant of the host doublet)
  → at lepton L: |b|² / a² = T(T+1) − Y² = 1/2.
```

The framework retains:
- the input Cl(3)/Z³ structure (A0)
- the lepton L doublet identification (CL3_SM_EMBEDDING §E)
- the Brannen circulant form of `Y_e` (charged-lepton two-Higgs canonical
  reduction note)
- the C_3 Plancherel decomposition (linking note R3, charged-lepton
  Koide cone equivalence)

What is **not** retained:
- a derivation of the **specific moduli ratio** `|b|² / a²` from the
  gauge structure of the host doublet (this is the Yukawa-participant
  measure step the candidate lemma posits)
- a derivation that the Yukawa coupling matrix's amplitude moduli
  inherit the gauge Casimir balance via a structural mechanism
  (e.g., a measure-theoretic argument on the Cl(3) Hermitian carrier
  with gauge-aware normalization)

These are concrete, named gaps. A future closure of `P_Q = 1/2` via
this route would need to supply at least one of these.

---

## 4. What this note closes vs. what it does not

### Closes (real content)

- **Algebraic identity RHS = 1/2** for the lepton L doublet, derived
  from `CL3_SM_EMBEDDING_THEOREM` retained gauge structure.
- **Algebraic-faces compositional identity:** the three Q-bridge support
  faces collapse to the same Cl(3) sub-algebra dimension count
  `(dim(SU(2)_L) − 1) / dim(Cl⁺(3)) = 1/2`.
- **Sharpening of the open primitive** from "vague Q-side bridge" to a
  specific candidate lemma with named missing chain.

### Does not close

- **`P_Q = 1/2` as a physical bridge derivation.** The candidate lemma
  is articulated and its RHS is retained, but the LHS-to-RHS
  identification on the physical lepton Yukawa amplitude is **not**
  derived.
- **`Q_l = 2/3` on the live authority surface.** This is conditional on
  closing `P_Q = 1/2`.
- **`δ_Brannen = 2/9` in literal radians.** This is downstream of
  `Q_l = 2/3` via the linking note's `δ = Q/d` theorem (still
  conditional on the radian-bridge `P`).

The Q-side primitive `P_Q = 1/2` therefore remains **open** on the live
authority surface after this note, in the same status as before (a
single-primitive open). What the note adds: a precise candidate physical
bridge and a named chain that a future closure attempt must supply.

---

## 5. Closeout flags

```text
Q_BRIDGE_SUPPORT_FACES_ALGEBRAIC_VALUES_RETAINED=TRUE
RHS_T_T_PLUS_1_MINUS_Y_SQ_EQ_HALF_FOR_LEPTON_L_DOUBLET=RETAINED
ALGEBRAIC_FACES_COMPOSITIONAL_COLLAPSE_TO_CL3_DIMENSION_COUNT=TRUE
YUKAWA_CASIMIR_DIFFERENCE_LEMMA=ARTICULATED_AS_CANDIDATE_NOT_DERIVED
P_Q_BRIDGE_PHYSICAL_DERIVATION_ON_FLAVOR_AMPLITUDE=STILL_OPEN
Q_L_EQ_2_OVER_3_RETAINED_CLOSURE=FALSE
DOWNSTREAM_DELTA_2_OVER_9_RAD_CLOSURE=NOT_CLOSED_BY_THIS_NOTE
```

---

## 6. Verification

```bash
python3 scripts/frontier_cl3_yukawa_casimir_difference_bridge_candidate.py
```

Verifies:
1. Retained gauge inputs: `T = 1/2`, `Y = −1/2` for lepton L doublet
   (CL3_SM_EMBEDDING §E).
2. RHS computation: `T(T+1) − Y² = 3/4 − 1/4 = 1/2` exact (Fraction).
3. Three support faces all give `1/2` exact (Fraction).
4. Compositional collapse: all three reduce to
   `(dim(SU(2)_L) − dim(U(1)_Y central direction)) / dim(Cl⁺(3))
   = (3 − 1)/4 = 1/2`.
5. Brannen relation: `|b|²/a² = 1/2 ⇔ c = √2 ⇔ Q = 2/3`.
6. Honest scope: candidate lemma articulated; physical-bridge derivation
   of LHS=RHS NOT verified (it's the open closure step, not a passable
   check).

Expected: PASS=N, FAIL=0.

---

## 7. Cross-references

- [`KOIDE_Q_BRIDGE_SINGLE_PRIMITIVE_NOTE_2026-04-22.md`](KOIDE_Q_BRIDGE_SINGLE_PRIMITIVE_NOTE_2026-04-22.md)
  — single-primitive narrowing of the Q-bridge; lists the three support faces
- [`CL3_SM_EMBEDDING_THEOREM.md`](CL3_SM_EMBEDDING_THEOREM.md)
  — retained Cl⁺(3) ≅ ℍ → SU(2)_L; dim counts; Y eigenvalue assignment
- [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)
  — `Q = 2/3 ⟺ a₀² = 2|z|²` exact algebraic equivalence
- [`CHARGED_LEPTON_TWO_HIGGS_CANONICAL_REDUCTION_NOTE.md`](CHARGED_LEPTON_TWO_HIGGS_CANONICAL_REDUCTION_NOTE.md)
  — Brannen circulant form of the lepton Yukawa amplitude
- [`KOIDE_Q_DELTA_LINKING_RELATION_THEOREM_NOTE_2026-04-20.md`](KOIDE_Q_DELTA_LINKING_RELATION_THEOREM_NOTE_2026-04-20.md)
  — `δ = Q/d` linking; downstream of this Q-side primitive
- [`KOIDE_A1_DERIVATION_STATUS_NOTE.md`](KOIDE_A1_DERIVATION_STATUS_NOTE.md)
  — comprehensive A1 / Q-side derivation status; flags the Yukawa
  Casimir-difference lemma as the strongest axiom-native candidate

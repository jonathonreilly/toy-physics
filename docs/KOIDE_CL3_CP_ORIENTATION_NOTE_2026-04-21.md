# Koide Loop Iteration 8 — I5 Attack B1: Cl(3) CP-Orientation Structure

**Date:** 2026-04-21 (iter 8)
**Attack target:** δ_CP sign in PMNS (T2K: sin δ_CP < 0)
**Status:** **Z₂ ORIENTATION DOF IDENTIFIED** (structural progress; not full derivation)
**Runner:** `scripts/frontier_koide_cl3_cp_orientation.py` (33/33 PASS)

---

## One-line finding

The retained Cl(3) framework carries a **two-fold Z₂ CP-orientation
degree of freedom** corresponding to the identification I ↔ +i vs
I ↔ −i (where I = e₁e₂e₃ is the Cl(3) pseudoscalar). T2K's preferred
sign (sin δ_CP < 0) picks one of the two orientations. Iter 8
**reduces** the δ_CP sign question to a discrete Z₂ choice; iter 9+
must derive which orientation is retained.

## Structural verifications

1. **Cl(3) basics (verified)**: 8-dim Clifford algebra with basis
   {1, e₁, e₂, e₃, e_{12}, e_{13}, e_{23}, I}. Anticommutation
   e_i e_j = −e_j e_i, vectors square to +1.

2. **Pseudoscalar centrality (verified)**: [I, e_i] = 0 for all i.
   I commutes with everything → I is central.

3. **I² = −1 (verified)**: In Pauli 2×2 rep, I = e₁e₂e₃ = iI_{2×2}.

4. **I acts as +i on spinors (in Pauli convention)**: I·ψ = iψ for
   any spinor. Chirality is NOT carried by I (which is scalar on
   spinors); chirality lives in e₃ or γ₅ separately.

5. **Parity flips I**: Under P: e_i → −e_i, so I → (−1)³ I = −I.

6. **Z₂ orientation choice**: Both I and −I satisfy I² = −1 and
   centrality. The map I ↦ +i (standard Pauli rep) and I ↦ −i
   (complex-conjugate rep) are both valid Cl(3) algebra homomorphisms.
   Choice between them is a **Z₂ discrete degree of freedom**.

7. **Independent of SELECTOR sign**: SELECTOR = +√6/3 > 0 is a scalar
   sign choice. I ↔ ±i is a pseudoscalar sign choice. They're independent.
   Total retained sign space: Z₂ × Z₂ = 4, of which SELECTOR > 0
   fixes one factor, leaving the I-orientation open.

8. **Jarlskog sign**: With iter 4 angles:
   - δ_CP = +π/2 → J_CP = +0.0327 (positive orientation)
   - δ_CP = −π/2 → J_CP = −0.0327 (negative orientation)
   - T2K: sin δ_CP < 0 → **selects negative orientation**.

## Why this is progress

Same kind of progress as iter 5's single-rotation no-go:

- **Iter 5**: Ruled out simple single-rotation mechanism for iter 4
  angles. Narrowed search to composite mechanisms.
- **Iter 8**: Identified the specific Z₂ DOF controlling δ_CP sign.
  Reduced "why sin δ_CP < 0?" to "which of 2 discrete orientations?".

Both iterations narrow the open-question space without full closure.
This is the right kind of incremental progress for the loop program.

## What iter 8 does NOT do (honest limitations)

- **Does NOT derive which orientation is retained.** T2K sign is
  used as OBSERVATIONAL input to select the orientation.
- **Does NOT connect the chirality choice** (LH-only neutrinos vs
  Dirac charged leptons) rigorously to the orientation.
- **Does NOT show** the retained orientation is forced by
  Z₂ cobordism classification (a deeper mathematical structure
  that might determine it uniquely).

## Iter 9+ targets (updated)

1. **Chirality → orientation derivation**:
   In 4D Dirac theory, γ₅ acts as I · (something). For LH neutrinos
   (only one chirality), I's action is effectively restricted.
   Conjecture: this restriction FORCES the negative orientation for
   the neutrino sector.

2. **Z₂ cobordism argument**:
   The CP orientation of a spin-structure is classified by the
   Stiefel-Whitney class w₁. On PL S³ × R, this class has a specific
   value determined by the retained lattice orientation. Check if
   this fixes the orientation.

3. **Consistency check via B and L violation**:
   If the retained framework has a baryon/lepton asymmetry
   mechanism, the CP-orientation should correlate with the
   observed matter-antimatter asymmetry.

## Status update

| Gap | Iter 7 status | Iter 8 update |
|---|---|---|
| I1 (Q=2/3) | retained-derived + stress-tested | (unchanged) |
| I2/P (δ=2/9) | retained-derived + stress-tested | (unchanged) |
| I5 magnitudes (angles) | conjecture-level 1σ | (unchanged) |
| I5 δ_CP sign | T2K observational | **reduced to Z₂ orientation choice** |

Progress: I5 δ_CP sign problem is now a SPECIFIC discrete choice
(2 options, one matches T2K) rather than a diffuse "why this sign?"
question. Framework-native derivation of the orientation is iter 9+
target.

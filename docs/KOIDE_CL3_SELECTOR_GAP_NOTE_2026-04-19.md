# Koide Cl(3) → SM Embedding — Selector Gap Note

**Date:** 2026-04-19
**Status:** exact negative-result / support note on current `main` — the Cl(3) doublet/Kramers route is sharpened and exhausted cleanly, but the charged-lepton package remains bounded

---

## Summary

The Cl(3) → SM embedding (from `frontier/cl3-sm-embedding`) was fully deployed against the charged-lepton selector gap: m_V ≈ -0.433 (V_eff minimum) vs m_* ≈ -1.161 (physical selected point). No Cl(3)-algebraic route closes the gap. The blocker is documented here.

---

## 1. Cl⁺(3) R-Sector Doublet Structure (New Structural Support Finding)

Under Cl⁺(3) ≅ ℍ, the SU(2) subalgebra pairs the hw=1 R-sector into two j=1/2 Kramers doublets:

| Doublet | Members | H matrix indices |
|---------|---------|-----------------|
| A | axis-3 (001), axis-1 (100) | 0 and 2 |
| B | axis-2 (010), baryon (111) | index 1 and external |

The hw=1 diagonal structure at the Koide selector (m=0):

| Index | State | H_frozen diagonal |
|-------|-------|-------------------|
| 0 | axis-3 (001) | 0 |
| 1 | axis-2 (010) | +√(2/3) |
| 2 | axis-1 (100) | −√(2/3) |

---

## 2. Doublet A Algebraic Condition

The T_m generator acts only on index 0: H[0,0](m) = m, H[1,1] and H[2,2] frozen.

The Doublet A equal-diagonal condition `H[0,0](m) = H[2,2](m)` gives:

```
m_DA = H_frozen[2,2] = -√(2/3) ≈ -0.816497
```

This is an **exact algebraic value** but is 30% off from the physical m_* ≈ -1.161.

The doublet A off-diagonal coupling is also exact:

```
|H_frozen[0,2]| = GAMMA = 1/2  (exactly)
```

This follows from an algebraic cancellation: **E1 = 2·SELECTOR** at the Koide selector, causing the real part of H_BASE[0,2] = -E1 − (1/2)i to cancel under the affine shift +2·SELECTOR, leaving only the pure-imaginary GAMMA = 1/2 term.

---

## 3. Routes Exhausted

### 3a. Doublet A equal-diagonal → m_DA = -√(2/3) ≈ -0.816

Gap: |m_DA − m_*| ≈ 0.344 (30%). The doublet A condition does not reproduce m_*.

### 3b. Baryon Schur Complement

The baryon (111) state at hw=3 is external to the 3×3 H matrix. The baryon-to-hw=1 coupling is S₃-symmetric (the baryon is totally symmetric; hw=1 states are S₃ permuted). Any Schur complement integrating out the baryon contributes **ΔK ∝ −I₃**, which is m-independent and shifts the potential by a constant — the critical-point equation is unchanged.

**Status: exact negative closeout on this candidate route.**

### 3c. SU(3) Coupling Modifications

From the Cl(3) → SM embedding: R_conn = 8/9, N_c = 3, C₂(fund) = 4/3. Replacing the Clifford-fixed couplings (g₂ = 3/2, g₃ = 1/6) with colour-weighted variants:

| Modification | New m_V |
|-------------|---------|
| g₂ → N_c · g₂ | ≈ −0.135 |
| g₃ → R_conn · g₃ | ≈ −0.429 |
| g₂ → C₂ · g₂ | ≈ −0.314 |

All miss m_* ≈ −1.161 by > 5%. The gap is structural.

### 3d. Eigenvalue Degeneracy

The eigenvalues of H_sel(m_*) are (−2.507, −0.848, +2.195) — all distinct. No eigenvalue degeneracy crossing occurs at m_* in the range [m_pos, 0].

---

## 4. Current Status of m_*

| Quantity | Value | Source |
|---------|-------|--------|
| m_DA (doublet A) | −√(2/3) ≈ −0.816 | Exact algebraic |
| m_V (V_eff minimum) | ≈ −0.433 | Clifford-exact critical point |
| m_pos (positivity threshold) | ≈ −1.2958 | kappa = −1/√3, algebraic |
| m_* (physical selected point) | ≈ −1.1605 | H_* witness kappa_* ≈ −0.608 |

The physical m_* currently lies between m_pos and m_DA, selected by the phenomenological H_* witness ratio kappa_* ≈ −0.608. No Cl(3)-algebraic derivation of kappa_* has been found.

---

## 5. Open Routes (Not Yet Exhausted)

### (a) Full 4×4 Block Diagonalization (hw=1 + baryon)

The argument that the baryon Schur complement is ∝ −I₃ assumes S₃-symmetric coupling. A first-principles computation of the full 4×4 generator (T2 sector + baryon) from the lattice action might reveal non-uniform structure that provides a non-trivial m-dependent eigenvalue condition.

**Risk:** S₃ symmetry likely forces uniform coupling. Low probability of closing the gap, but not yet formally proved from the microscopic lattice action.

### (b) Transport Gap 4π/√6 Lattice Derivation

The transport ratio η/η_obs ≈ 5.29 is numerically close to 4π/√6 ≈ 5.13 (3.2% mismatch). If this ratio can be derived from the lattice propagator and the mismatch encodes a correction at m_*, it might pin m_*. Formal status: **observation only** — no derivation.

### (c) First-Principles Derivation of kappa_*

The one-clock semigroup (gamma_orbit note) provides a positive witness: `H_* = H3(M_STAR, DELTA_STAR, Q_PLUS_STAR)` gives cos-similarity > 1 − 10⁻⁹ with PDG sqrt-masses. But M_STAR, DELTA_STAR, Q_PLUS_STAR are G1 observational chamber pins, not derived from Cl(3). Deriving kappa_* ≈ −0.608 from a physical principle (possibly involving the Z³ character norm |z| = √6/2 or the J₂ coupling GAMMA = 1/2) remains the central open problem.

---

## Status

| Claim | Status |
|-------|--------|
| Cl⁺(3) R-sector = two j=1/2 Kramers doublets | Proved (structural) |
| m_DA = −√(2/3) from doublet A equal-diagonal | Proved exact |
| E1 = 2·SELECTOR → \|H_frozen[0,2]\| = GAMMA = 1/2 | Proved exact (algebraic cancellation) |
| Baryon Schur complement ∝ −I₃ (m-independent) | Proved (S₃ symmetry + T_m variation check) |
| SU(3) coupling modifications miss m_* by > 5% | Confirmed numerically |
| No eigenvalue degeneracy crossing at m_* | Confirmed numerically |
| m_* = −1.1605 NOT derivable from Cl(3) alone | Honest gap — remains open |

## main

This note sharpens the charged-lepton support stack already on `main`.
It does **not** upgrade the authoritative bounded charged-lepton package, and it
does **not** promote the exploratory `Q = 2/3`-surface or
scale-selector near-miss probes into

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [koide_z3_scalar_potential_lepton_mass_tower_note_2026-04-19](KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE_2026-04-19.md)
- [charged_lepton_mass_hierarchy_review_note_2026-04-17](CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md)
- `charged_lepton_koide_review_packet_2026-04-18` — DOWNSTREAM aggregator
  (the review packet AGGREGATES this note as part of its support stack;
  this note is upstream content that the packet pulls together).
  Reference is backticked rather than markdown-linked because the citation
  graph direction is *review_packet → this_note*; a markdown link here
  would create the wrong-direction edge and a length-2 cycle.

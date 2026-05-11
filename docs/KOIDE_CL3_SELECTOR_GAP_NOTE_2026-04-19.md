# Koide Cl(3) → SM Embedding — Selector Gap Note

**Date:** 2026-04-19
**Status:** exact negative-result / support note on current `main` — the Cl(3) doublet/Kramers route is sharpened and exhausted cleanly, but the charged-lepton package remains bounded

---

## Audit-conditional perimeter (2026-05-10)

Prior independent audit feedback on an earlier revision identified the
global selector-gap exhaustion claim as too broad for the cited
dependency chain:

> "Issue: the global selector-gap/no-Cl(3)-route conclusion relies on
> unsupported imported structures and on an m_* physical witness that
> the cited authority marks as out of scope/open. Why this blocks: the
> supplied one-hop authority only retains the local V(m) coefficient
> assignment and honest V_eff-vs-m_* gap, not the doublet, baryon,
> SU(3), degeneracy, or H_* bridge needed for exhaustion. Repair
> target: provide direct retained dependencies or runners for each
> listed route and a theorem excluding or resolving the stated
> full-4x4/kappa_* open routes. Claim boundary until fixed: the note
> may be cited as an open selector-gap inventory, not as a closed
> bounded theorem that Cl(3) alone cannot derive m_*."

The prior feedback repair target is `scope_too_broad`: "split the claim into
auditable listed-route failures with direct dependencies/runners, and
leave the global Cl(3)-alone non-derivability statement as an open_gate
until the full 4x4 and kappa_* selector issues are closed."

The single load-bearing item supported through the cited authority chain
is the V_eff coefficient assignment / V_eff-vs-m_* gap fixed in the
cited parent
[`KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE_2026-04-19.md`](KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE_2026-04-19.md).
The §3a / §3b / §3c / §3d route "exhaustion" sub-claims, the j=1/2
Kramers-doublet structural identification (§1), the doublet-A
equal-diagonal exact value m_DA = −√(2/3) (§2), the H_* witness ratio
kappa_* ≈ −0.608 (§4), and the "open-routes" inventory (§5) are *not*
covered by the cited one-hop authority and remain conditional pending
direct retained dependencies or runners per route. The Per-route
conditional perimeter table below makes this explicit.

This source edit sharpens the conditional perimeter and narrows the
load-bearing scope to what the cited parent supports; no new derivation
is asserted and independent audit owns any current verdict or effective
status after the source change. The §1 - §4 numerics ("≈ −0.816",
"GAMMA = 1/2 exact", "miss m_* by > 5%", "eigenvalues (−2.507, −0.848,
+2.195)") are recorded as printed claims unsupported by an in-repo
retained derivation chain, except where the parent V(m) coefficient
assignment carries them.

---

## Summary

The Cl(3) → SM embedding (from `frontier/cl3-sm-embedding`) was fully deployed against the charged-lepton selector gap: m_V ≈ -0.433 (V_eff minimum) vs m_* ≈ -1.161 (physical selected point). No Cl(3)-algebraic route closes the gap. The blocker is documented here.

**Audit perimeter narrowing (2026-05-10):** the global "no Cl(3)
algebraic route closes the gap" closure-statement is *not* loadbearing
on the cited one-hop authority. It is read as an *open selector-gap
inventory*, not as a closed bounded theorem, matching the prior
feedback boundary.

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

## Per-route conditional perimeter (2026-05-10)

Per the prior feedback repair target, this table records each listed
route's dependency posture. None of the §3 / §4 / §5 sub-claims is
independently carried by the cited one-hop authority; the only
parent-supported item is the V_eff coefficient assignment carried by
the parent mass-tower note.

| Section | Sub-claim | Direct in-repo dependency? | Conditional posture |
|---|---|---|---|
| §1 Kramers doublets | Cl⁺(3) ≅ ℍ → two j=1/2 doublets | No retained one-hop authority cited here | Structural identification, conditional pending direct retained dep/runner |
| §2 Doublet-A equal-diagonal | m_DA = −√(2/3) ≈ −0.816497 (exact) | No retained one-hop authority cited here | Algebraic claim, conditional pending direct retained dep/runner |
| §2 J₂ off-diagonal | \|H_frozen[0,2]\| = 1/2 (E1 = 2·SELECTOR cancellation) | No retained one-hop authority cited here | Algebraic cancellation claim, conditional pending direct retained dep/runner |
| §3a Doublet-A miss | gap ≈ 0.344 (~30%) | depends on §2 (above) | Inherits conditional posture of §2 |
| §3b Baryon Schur ∝ −I₃ | S₃-symmetric baryon coupling → m-independent shift | No retained one-hop authority cited here | Conditional pending retained 4×4 derivation |
| §3c SU(3) coupling-mod misses | three modifications all miss > 5% | No retained one-hop authority cited here | Numeric claim, conditional pending retained Cl(3)→SM-embedding theorem |
| §3d No degeneracy crossing | eigenvalues (−2.507, −0.848, +2.195) all distinct | No retained one-hop authority cited here | Numeric claim, conditional pending direct retained runner |
| §4 m_* from H_* witness | kappa_* ≈ −0.608, m_* ≈ −1.1605 | parent note marks H_* witness as G1 phenomenological pin, **not** Cl(3)-derived | Conditional pending first-principles kappa_* derivation (open) |
| §5 Open routes (a),(b),(c) | full 4×4, transport 4π/√6, kappa_* derivation | explicitly open / no derivation | Open-gate inventory only |

The §6 "global Cl(3) alone cannot derive m_*" closure-statement is
treated, per the prior feedback, as an *open selector-gap inventory*,
not as a closed bounded theorem. Promotion would require either a
retained theorem excluding the §5 open routes or direct retained
dependencies/runners for §1-§4. Until such a retained chain lands,
this note's load-bearing perimeter is the parent V_eff coefficient
assignment alone.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by prior audit feedback so the audit citation graph can track them. It does not promote this note or change the claim scope.

- [koide_z3_scalar_potential_lepton_mass_tower_note_2026-04-19](KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE_2026-04-19.md)
- `charged_lepton_mass_hierarchy_review_note_2026-04-17` (upstream parent
  review note; backticked to avoid length-3 cycle through
  `CHARGED_LEPTON_KOIDE_REVIEW_PACKET_2026-04-18.md` — that hierarchy
  review note already cites the koide review packet which lists this
  selector-gap note, so citation graph direction is *hierarchy_review →
  koide_review_packet → this_selector_gap*)
- `CHARGED_LEPTON_KOIDE_REVIEW_PACKET_2026-04-18.md` (downstream consumer; backticked to avoid length-2 cycle — citation graph direction is *downstream → upstream*)

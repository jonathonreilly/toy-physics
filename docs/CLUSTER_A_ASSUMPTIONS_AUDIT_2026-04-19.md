# Cluster A — Charged-Lepton Assumptions Audit

**Date:** 2026-04-19
**Scope:** All Cluster A (lepton mass tower) work on `frontier/lepton-mass-tower`
**Goal:** Find the assumption(s) we are trapped in; identify which "what ifs" open new directions toward m_*

---

## How to read this

For each assumption: what it is, where it lives in the code, and what concretely changes if it is wrong or dropped. The synthesis section assembles the "what ifs" into candidate new directions.

---

## I. Mathematical Assumptions

---

### M1. Electron mass is not read from x[0,0] — it comes from the Koide formula

**What it is:** When we compute slot values from exp(H_sel(m_*)), we use v = Re(x[2,2]) and w = Re(x[1,1]). The third diagonal entry Re(x[0,0]) ≈ 1.744 is discarded. The electron mass u is instead defined as the small root of the Koide formula applied to (v, w):

```
u_small = 2(v+w) − √(3(v²+4vw+w²))
```

This is how Q=2/3 is guaranteed: u is chosen to satisfy the Koide relation exactly.

**Verification:** At m_*: the three diagonal entries of exp(H_sel) are {1.744, 6.228, 1.519}. Q for this triple = 0.490 ≠ 2/3. Q for (u_koide=0.1056, 1.519, 6.228) = 2/3 exactly by construction.

**Where:** `frontier_koide_selected_line_cyclic_response_bridge.py` lines 55–98; `frontier_koide_gamma_orbit_positive_one_clock_semigroup.py` lines 61–77.

**What if wrong:** If Re(x[0,0]) IS the physical electron slot, then the physical triplet is {1.744, 1.519, 6.228} and Q = 0.490. This would mean the Koide relation is NOT imposed; instead Q ≈ 0.49 is the physical value. The entire selected-slice machinery (which targets Q=2/3 via the Koide formula) would need to be rebuilt around a different constraint. However, this also means the electron mass is NOT anomalously light relative to (v, w) — removing the deep mystery of why u_small ≪ v, w.

**Severity: HIGH.** Dropping this changes the physical triplet and invalidates the V_eff potential derivation entirely.

---

### M2. Slot values are diagonal entries Re(x[i,i]) of exp(H_sel) — not eigenvalues

**What it is:** The physical masses come from the real parts of the diagonal elements of the matrix exponential exp(H_sel), specifically Re(x[2,2]) and Re(x[1,1]). Eigenvalues of exp(H_sel) are NOT used.

**Verification:** Eigenvalues of exp(H_sel(m_*)) are {0.1056, 0.470, 8.915}. Q for this triple = 0.885 ≠ 2/3. However, eigenvalues of exp(β H_sel(m_*)) satisfy Q ≈ 2/3 at β ≈ 0.578 (numerically checked), which differs from β_star ≈ 0.634.

**What if wrong:** If the physical masses come from **eigenvalues** of exp(β H_sel) with Q=2/3 as the selection criterion, then:
- The selection condition is different: find (m, β) such that eigenvalues of exp(β H_sel(m)) satisfy Q=2/3 and match PDG
- This is a **two-dimensional selection condition** — the β and m coordinates are entangled
- At β ≈ 0.578 the eigenvalues of exp(β H_sel(m_*)) already satisfy Q ≈ 2/3
- The kappa formula (v−w)/(v+w) would use the sorted eigenvalues instead of (x[2,2], x[1,1])
- This could in principle provide an algebraic constraint between β and m

**Severity: HIGH.** Dropping this opens a 2D (m, β) condition rather than 1D, and the Q=2/3 eigenvalue condition might pin the physical point without importing kappa_* from the H_* witness.

---

### M3. Index ordering in H3: index 1 = tau, index 2 = muon

**What it is:** The H3 3×3 matrix has a non-obvious species assignment. At the physical selected point:
- x[2,2] = 1.519 → maps to muon (smaller of the two)
- x[1,1] = 6.228 → maps to tau (larger)
- Index 0 is the "missing" electron (computed from Koide formula)

This means kappa = (x[2,2]−x[1,1])/(x[2,2]+x[1,1]) < 0.

**Where:** Implicit in how `slot_values` is defined — this assignment is never explicitly justified in a docstring. From `H_lift_missing_axis`: "Rows/cols 1..3 are ordered by missing-axis 1, 2, 3." So:
- H3 index 0 → missing-axis 1 → state {011} → which lepton?
- H3 index 1 → missing-axis 2 → state {101} → tau (heaviest diagonal)
- H3 index 2 → missing-axis 3 → state {110} → muon

**What if wrong:** If v=x[1,1] and w=x[2,2] (flipped), kappa_* → +0.608. A positive kappa might correspond to a different point on the selected slice. Trivially kappa_flip(m) = −kappa_std(m), so the flip just relabels positive/negative kappa. The physics is the same; the question is which sign convention matches the physical species.

**Severity: LOW** (for sign convention), **MEDIUM** (for species assignment). If the axis-to-species correspondence is wrong, the doublet A analysis used the wrong Kramers pairing.

---

### M4. V_eff is a cubic polynomial (1/2)Tr(K²) + (1/6)Tr(K³), no higher terms

**What it is:** The Z³-invariant scalar action is assumed to have the natural grading that terminates at cubic order:
```
V(m) = V₀ + (c₁ + c₂/2)m + (3/2)m² + (1/6)m³
```
This is justified by the Clifford involution T_m² = I, which means all higher trace powers of K_sel reduce via Cayley-Hamilton to lower-degree polynomials.

**Where:** `frontier_koide_z3_scalar_potential.py` Parts 1–2; `KOIDE_Z3_SCALAR_POTENTIAL_LEPTON_MASS_TOWER_NOTE_2026-04-19.md` §2.

**What if wrong:** If the physical action includes a quartic term (1/12)Tr(K⁴), then Cayley-Hamilton gives Tr(K⁴) = Tr(K²)·Tr(I) − ... which collapses back to lower-degree. So by Cayley-Hamilton for 3×3 matrices, the cubic IS the exact truncation — the fourth-degree is not independent. The cubic V_eff is therefore exact to ALL polynomial orders by Cayley-Hamilton.

**Verdict: NOT an assumption — it is a theorem.** The cubic is the exact Cayley-Hamilton truncation for 3×3 K_sel.

---

### M5. The active coordinate is m = Tr(K_Z3) — a single real number

**What it is:** On the selected slice (δ=q₊=√6/3), the full K_Z3 kernel reduces to K_frozen + m·T_m where m = Tr(K_Z3) = Re(K_Z3[1,2]) + 4√2/9. This is the unique active direction on the 1D selected line.

**Where:** `frontier_koide_selected_slice_frozen_bank_decomposition.py`; `frontier_koide_microscopic_scalar_selector_target.py`.

**What if wrong:** The selected slice IS 1D by construction (multiple proofs, error < 10⁻¹²). The claim is exact. The coordinate m is not an assumption; it is a unique affine coordinate on the selected line.

**Verdict: NOT an assumption — proved structurally.**

---

### M6. The potential V_eff is the full scalar action (not a partial contribution)

**What it is:** V_eff = (1/2)Tr(K²) + (1/6)Tr(K³) is treated as the complete scalar sector action. No kinetic term, no coupling to gauge fields, no loop corrections.

**What if wrong:** If there are additional contributions from:
- Gauge coupling to SU(3)_c or SU(2)_L: the potential picks up a colour factor or isospin correction
- Kinetic term (∂K)²: adds a Laplacian in m-space that could shift the minimum
- Quantum loop correction: adds a Coleman-Weinberg-type logarithm log(K)

The critical-point equation acquires an additional term. If the loop correction is −(λ/4π²)·K·log(K/Λ²), the m-derivative introduces a term with the structure of the doublet A condition. **This has not been explored.**

**Severity: MEDIUM.** A one-loop correction from the gauge coupling (g₂² = 1/4 from Cl(3)) could plausibly shift the minimum from m_V ≈ −0.433 toward m_* ≈ −1.161.

---

### M7. UZ3 is the Z₃ DFT unitary — no other rotation

**What it is:** kz_from_h(h) = UZ3† h UZ3 where UZ3 is the 3×3 discrete Fourier transform matrix. This diagonalizes the Z₃-cyclic action on the three-species sector.

**What if wrong:** A different unitary (e.g., permutation matrix, Hadamard, Clifford rotation) would give different frozen-bank values. The slot pair a_*, b_* would change. The frozen-bank structure is therefore tied to the specific choice of UZ3 = DFT.

**Why DFT:** The Z₃ symmetry group has exactly one irreducible unitary representation structure, realized by the DFT phases ω = e^{2πi/3}. The DFT IS the natural diagonalizer of Z₃.

**Verdict: NOT an assumption — forced by Z₃ group theory.**

---

## II. Physical Assumptions

---

### P1. The Koide relation Q=2/3 is exact and imposed, not derived

**What it is:** The physical charged-lepton masses satisfy Q = (Σmₖ)/(Σ√mₖ)² = 2/3 exactly. The framework uses this as an exact constraint to define the "Koide cone" and the u_small formula. Q=2/3 is NOT derived from the Z³ lattice or Cl(3) structure.

**What if wrong:** If Q = 2/3 is only approximately satisfied (or if the exact value is derivable and equal to something like 2/3 + ε for a small algebraic ε), then:
- The Koide cone shifts slightly
- The slot formula u_koide changes
- The positivity threshold m_pos shifts
- The physical m_* might shift accordingly

**More radical what-if:** If Q is NOT 2/3 but rather is determined by the eigenvalue condition on exp(H_sel) (see M2 above), then Q emerges dynamically. The eigenvalues of exp(β H_sel(m)) satisfy Q=2/3 at specific (m,β) pairs — this could replace the imposed Koide constraint with a derived one.

**Severity: HIGH.** This is possibly the deepest assumption in the framework.

---

### P2. The physical sector is the T_2 (hw=2) missing-axis sector

**What it is:** The exp(H_sel) diagonal entries x[i,i] are interpreted as propagator amplitudes for the T_2 missing-axis states {011, 101, 110}. The charged leptons live in the T_2 sector (hw=2), NOT the T_1 sector (hw=1, axis states {001, 010, 100}).

**Where:** Implicit in `t1_species_basis_L()` in `frontier_higgs_dressed_propagator_v1.py` — but the "L-taste T_1 subspace" is used to RESTRICT the 16×16 operator to 3×3, meaning the matrix is over T_1 species. The propagator then ACTS on T_2 states via Γ₁ hops. So:
- The GENERATOR H3 is defined on the T_1 species basis
- But the PROPAGATED states (exp(H) entries) represent T_2 amplitudes

**What if wrong:** If the charged leptons live in the T_1 (hw=1) sector:
- The slot values would be diagonal entries of exp(H_sel) in a different ordering
- The correspondence between matrix indices and physical species changes
- The x[0,0] entry might BE the electron slot (not discarded)
- The Koide relation might emerge from the T_1 eigenvalue structure without imposition

**Severity: MEDIUM-HIGH.** The T_1 vs T_2 sector assignment is not explicitly derived from the charged-lepton selection mechanism — it comes from the broader DM/neutrino framework's propagator setup.

---

### P3. The one-clock semigroup picture: X_β = exp(βG) with fixed H_sel as G

**What it is:** The gamma_orbit analysis assumes the physical lattice evolution produces identical repeated steps X_β = exp(βH_sel) for some β. This forces an exponential semigroup structure.

**Where:** `frontier_koide_gamma_orbit_positive_one_clock_semigroup.py` Parts 1–2.

**What if wrong:** If the lattice evolution is NOT an exact semigroup (e.g., the steps are slightly different at each lattice site, or there are non-linear corrections), then the semigroup reduction fails. The "β" parameter is then not a free scalar but carries additional physical content. In that case:
- β_* ≈ 0.634 is not arbitrary; it would be fixed by the non-semigroup correction
- The physical condition would be: find (m, β) jointly from a non-semigroup equation
- This could provide the missing constraint on m_*

**Severity: MEDIUM.** The semigroup assumption is physically motivated ("repeated identical clock steps") but is not derived from the microscopic lattice dynamics.

---

### P4. Only real parts of exp(H_sel) diagonal entries are physical

**What it is:** The slot values are Re(x[2,2]) and Re(x[1,1]). The imaginary parts are discarded. At m_*, Im(x[1,1]) ≈ Im(x[2,2]) ≈ 10⁻¹⁶ (machine precision), so the diagonal entries are real to numerical precision.

**Why they are real:** H_sel has imaginary off-diagonal only at (0,2) and (2,0) (from GAMMA=1/2). By block structure, the (1,1) and (2,2) diagonal entries of exp(H_sel) are real because they are in a block that couples through the (1,2) element, which is real. Only elements coupling through GAMMA get imaginary parts — and those are off-diagonal.

**Verdict: NOT an assumption at m_* — provably real.** The imaginary parts vanish exactly by the matrix structure.

---

### P5. The Kramers doublet A pairing is {axis-3(001), axis-1(100)}

**What it is:** Under Cl⁺(3) ≅ ℍ, the SU(2) generator used was one specific quaternion axis, pairing {index 0, index 2} in H3 as Doublet A. This gives m_DA = −√(2/3) ≈ −0.816.

**What if wrong:** There are three SU(2) axes in ℍ = span{1, i, j, k}. Each gives a different doublet pairing:
- **J_z** (used): pairs {index 0, index 2} → m_DA = −√(2/3)
- **J_x**: pairs {index 0, index 1} or {index 1, index 2} → different m_DA
- **J_y**: another pairing

If the physical Kramers doublet uses J_x or J_y instead of J_z:
- The equal-diagonal condition gives a different m_DA value
- One of these might give m_DA closer to m_* ≈ −1.161

**Computation needed:** For Doublet {0,1}: H[0,0]=m, H[1,1]=+√(2/3). Condition H[0,0]=H[1,1]: m = +√(2/3) ≈ +0.816. This is POSITIVE — outside the physical branch [m_pos, 0]. For Doublet {1,2}: H[1,1]=+√(2/3) and H[2,2]=−√(2/3) are BOTH frozen (neither shifts with m). Equal-diagonal condition: always violated (√(2/3) ≠ −√(2/3) for any m). 

So only the {0,2} pairing (Doublet A) gives a finite m_DA. The others are either outside the branch or impossible.

**Verdict: NOT a free assumption — J_z is forced by the structure of T_m.**

---

### P6. The baryon coupling to the hw=1 block is S₃-symmetric (uniform)

**What it is:** The argument that the baryon Schur complement is ∝ −I₃ rests on claiming the baryon {111} couples uniformly to all three axis-direction species by S₃ permutation symmetry.

**What if wrong:** If the baryon-to-hw=1 coupling is NON-uniform (e.g., species 0 couples more strongly than species 1, 2), the Schur complement acquires a diagonal matrix with different entries. This would:
- Add a m-INDEPENDENT non-uniform correction to the diagonal of H_sel
- Shift H_sel[0,0] differently from H_sel[1,1] and H_sel[2,2]
- Change m_DA (since H_sel[2,2] would shift by a different constant)
- Not directly generate an m-dependent correction (still m-independent by the T_m variation argument)

**Can non-uniform coupling arise?** The H3 off-diagonal H[0,1] = E1 ≈ 1.633 and H[1,2] ≈ −0.126 are already NON-uniform. This asymmetry is in the hw=1 block itself. The baryon (hw=3) couples to all three hw=1 species via single-hop transitions; by Z₃ covariance (not full S₃), the coupling amplitudes satisfy a phase rotation ω, ω², 1 rather than being equal. The coupling IS non-uniform — it's phase-rotated by Z₃.

**Why this matters:** If the Z₃ phase rotation in the baryon coupling contributes an m-independent diagonal matrix proportional to diag(1, ω, ω²) (where ω = e^{2πi/3}), and if taking Re(·) is done after the Schur complement is applied, then the real part of the correction might be m-independent (all equal to cos(2πk/3) for some k). Still proportional to the real part of (1, ω, ω²), which is (1, −1/2, −1/2) — not proportional to I₃.

**This correction shifts H[0,0] by +Δ, H[1,1] and H[2,2] by −Δ/2 (if taking Re(·)).** This changes m_DA. But whether this correction is m-dependent is key — it's still m-independent (Schur complement from a fixed baryon energy level), so it shifts m_DA but still doesn't create an m-dependent selector.

**Severity: LOW for m-dependence, MEDIUM for m_DA estimate.**

---

## III. Framework Assumptions

---

### F1. The Koide selected slice is at δ = q₊ = √6/3 exactly

**What it is:** The entire Cluster A analysis is on the 1D slice where both δ and q₊ equal √6/3 = SELECTOR. This is the "charged-lepton selected point" from upstream DM neutrino work.

**Where derived:** From the point-selection boundary theorem (`frontier_dm_neutrino_source_surface_active_affine_point_selection_boundary.py`). At the selected slice, the slot pair, CP pair, and doublet-block diagonal/imaginary entries are all pinned.

**What if wrong:** If the selected slice is at a different (δ, q₊), the frozen bank values change, T_m is different, c₁ and c₂ change, and the V_eff critical point m_V changes. Everything downstream shifts.

**Verdict:** The selected slice is multiply proved from upstream constraints (exact, error < 10⁻¹²). This is NOT a free assumption.

---

### F2. The H_* witness kappa_* ≈ −0.608 imports from G1 PMNS chamber

**What it is:** The physical kappa_* = (v_*−w_*)/(v_*+w_*) ≈ −0.608 is derived from the `hstar_witness_kappa()` function, which optimizes β to maximize cos-similarity of (u, v, w) with PDG sqrt-masses. The H_* generator itself is fixed at (M_STAR, DELTA_STAR, Q_PLUS_STAR) from the G1 PMNS-pinned observational chamber.

**M_STAR = 0.657, DELTA_STAR = 0.934, Q_PLUS_STAR = 0.715**: These are NOT at the Koide selected point (SELECTOR ≈ 0.816). They are separate G1 chamber pins from neutrino PMNS fits.

**What if wrong:** If the G1 chamber pin is incorrect, kappa_* is wrong, and m_* is wrong. More concretely: the PMNS pins import neutrino physics into the charged-lepton selector. If the charged-lepton selector is determined purely by Cl(3) structure (without neutrino input), kappa_* has a different value derivable from framework constants.

**Critical question:** Is kappa_* derivable from {GAMMA=1/2, E1=√(8/3), E2=√8/3, √(2/3), 1/√3, √6/3, 2/3}? No combination of these identified so far reproduces −0.608 exactly.

**Severity: CRITICAL.** This is the central open problem. kappa_* is the missing derived quantity.

---

### F3. The Cl(3) → SM embedding g₂²=1/4, g_Y²=1/5, N_c=3 are the correct coupling inputs

**What it is:** From `frontier/cl3-sm-embedding`, the gauge couplings at tree level are g₂² = 1/4, g_Y² = 1/5. These were tested in the V_eff analysis and do NOT shift the minimum to m_*.

**What if wrong:** If the coupling that enters the scalar sector action is the running coupling at the Koide scale (not the bare coupling), or if there's a threshold correction, the V_eff minimum shifts. But the shift is smooth — there's no obvious mechanism to move from m_V ≈ −0.433 to m_* ≈ −1.161 via a coupling correction.

---

### F4. Working in the 3×3 sector is sufficient — the full 16×16 is not needed

**What it is:** The H3 function provides a 3×3 Hermitian matrix. All selector analysis is done in 3×3. The other sectors (O_0 singlet, T_2 sector, O_3 baryon) are either decoupled (Schur-complemented away) or irrelevant.

**What if wrong:** The full 8×8 (one chirality) or 16×16 matrix couples all sectors. If there's a resonant condition between sectors — e.g., the O_0 sector energy exactly equals the hw=1 doublet splitting at m_* — that would create an eigenvalue crossing that pins m_*. This has NOT been checked.

**Specific check needed:** Does the O_0 (hw=0) sector energy level equal any eigenvalue of H_sel at m_*? In `H_lift_missing_axis`, the O_0 diagonal is a free scalar h_O0. If this equals one of the T_2 eigenvalues at m_*, it creates a level crossing. This would be a 4×4 condition (O_0 + 3 T_2 species) with an eigenvalue crossing that selects m_*.

**Severity: MEDIUM-HIGH.** The 4×4 (O_0 + T_2) eigenvalue crossing condition has not been computed for the selected slice.

---

## IV. Methodological Assumptions

---

### Met1. m_* comes from a polynomial or algebraic condition on H_sel(m)

**What it is:** The selector gap analysis systematically searched for polynomial conditions on H_sel(m) that give m_*: eigenvalue degeneracy, det=0, critical point of V_eff, SU(3) coupling modification. None found. The conclusion was that m_* is "transcendental" — set by the matrix exponential exp(H_sel).

**What if wrong:** The transcendental wall applies to polynomial conditions in m. But m_* might come from a transcendental IDENTITY:
- exp(H_sel(m_*)) satisfies some algebraic condition (not involving m in polynomial form)
- Example: if eigenvalues of exp(H_sel(m_*)) are in ratio e^(−2π/√3) or similar, that's transcendental in m but algebraic in the eigenvalue space

**Specific check:** Do the eigenvalues {0.1056, 0.470, 8.915} of exp(H_sel(m_*)) satisfy any simple ratio condition? Ratios: 8.915/0.1056 ≈ 84.4 ≈ e^{4.44}; 8.915/0.470 ≈ 18.97 ≈ e^{2.94}; 0.470/0.1056 ≈ 4.45 ≈ e^{1.49}. None immediately obvious. But: 4.44 ≈ 4π/√6 ≈ 5.13? No. 2.94 ≈ 3 (one log step)? Possibly.

**Severity: MEDIUM.** The transcendental wall applies within the polynomial framework. Outside that framework (transcendental identities), the wall might not exist.

---

### Met2. Seeking m_* from the V_eff critical point structure

**What it is:** The primary approach was to find conditions that shift the V_eff minimum from m_V ≈ −0.433 to m_* ≈ −1.161. All modifications of the polynomial structure (Clifford coupling, SU(3) corrections, Schur complement) were attempted.

**What if wrong:** m_* is NOT a critical point of any scalar potential at all. Instead, m_* might be selected by:
- A constraint equation (not an extremum condition): e.g., a zero of some function other than dV/dm
- A maximum entropy condition
- A lattice spacing condition (scale derivation)
- A resonance condition in the full propagator (O_0 level crossing — see F4)

**Severity: MEDIUM.** The V_eff critical point is a natural place to look, but the gap between m_V and m_* is large enough (factor ~2.7 in m) to suggest the mechanism is qualitatively different, not just quantitatively shifted.

---

### Met3. The scale factor and kappa_* are independent

**What it is:** In the current analysis, kappa_* pins m_* (via the cyclic-response bridge), and the "one overall scale factor" is stated as a separate remaining task. They are treated as independent.

**What if wrong:** If kappa_* and the scale factor are determined JOINTLY by the same microscopic condition, then:
- The scale condition provides a second equation
- The system {Q=2/3, scale condition} might fix both kappa_* and the scale
- This could remove the need to import kappa_* from the G1 witness

**Why plausible:** The Koide cone (Q=2/3) fixes the direction of (u, v, w). The overall scale and the position on the cone (kappa_*) together determine the triplet completely. If the lattice provides two conditions (scale + orientation), both are determined simultaneously. The one-clock semigroup optimization currently sets kappa_* by maximizing PDG similarity — but the scale follows from the same optimization. They are NOT independent in the gamma_orbit analysis.

**Severity: HIGH.** If the scale derivation requires an additional physical condition, that condition simultaneously pins kappa_* (and hence m_*).

---

### Met4. Restricting the selector search to the "first branch" of the positivity domain

**What it is:** All analysis of kappa(m) is restricted to the first branch m ∈ [m_pos, 0] where the small Koide root u_small > 0. The "second branch" (if it exists) is not considered.

**What if wrong:** If there is a second branch (m outside [m_pos, 0]) where the Koide triplet is positive and the kappa condition is satisfied differently, the physical point could be elsewhere. But from the monotonicity proof (kappa is strictly decreasing on the first branch), the mapping m ↔ kappa is bijective on this branch, so no second branch is needed.

**Verdict: Probably not an issue.** The first branch contains exactly one point per kappa value in [−1/√3, kappa(0)].

---

### Met5. The Clifford involution T_m² = I pins the V_eff structure (not an assumption, proved)

**Verdict: PROVED, not an assumption.** T_m = [[1,0,0],[0,0,1],[0,1,0]] is an involution by direct computation (T_m² = I₃). This is the bedrock of the scalar potential derivation.

---

## V. Synthesis: Which "What Ifs" Open New Directions?

---

### Combination 1 (High priority): Drop M1 + M2 → Eigenvalue-based Koide triplet

**What changes:** Instead of imposing Q=2/3 via the u_small formula, use the eigenvalues of exp(β H_sel(m)) directly as the physical triplet. Require Q=2/3 as an eigenvalue condition on exp(β H_sel(m)).

**Why this matters:**
- At β ≈ 0.578, eigenvalues of exp(β H_sel(m_*)) already satisfy Q ≈ 2/3
- This gives a 2D condition (m, β) rather than 1D
- The β condition might be fixed by a separate physical principle (e.g., lattice step size)
- If β is fixed by scale derivation, the Q=2/3 eigenvalue condition alone selects m_*
- The "transcendental wall" for polynomial conditions does NOT apply to this eigenvalue condition — it IS the natural condition for the semigroup picture

**What to compute:** The surface {(m, β) : Q(eigenvalues of exp(β H_sel(m))) = 2/3} — a curve in (m, β) space. Where does this curve intersect the PDG cos-similarity peak? Does the intersection point have an algebraic characterization?

---

### Combination 2 (High priority): Drop F4 → O_0 level crossing in the 4×4 sector

**What changes:** Extend the analysis from 3×3 (T_2 species only) to 4×4 (O_0 + T_2). Compute eigenvalues of the 4×4 H_lift(m) matrix and check for an eigenvalue crossing at m_*.

**Why this matters:**
- In `H_lift_missing_axis`, the 4×4 matrix has O_0 diagonal = h_O0 (a free parameter)
- If h_O0 is fixed by the framework (e.g., h_O0 = Tr(H_sel)/3 = m/3), the 4×4 eigenvalues become a function of m
- An eigenvalue crossing in the 4×4 matrix at m_* would provide a polynomial condition (det = 0 for the 2×2 sub-block) that selects m_* algebraically
- The O_0 sector energy is structurally linked to m via Tr(H_sel) = m

**What to compute:** Let h_O0 = m/3 (or 0, or some other retained value). Find where the smallest 4×4 eigenvalue of H_lift(m) equals the largest, or where two eigenvalues cross. Check if any crossing is at m ≈ −1.161.

---

### Combination 3 (Medium priority): Drop Met3 → Scale derivation pins kappa_*

**What changes:** Instead of treating scale and kappa_* as independent, derive both from a single lattice scale condition. The lattice spacing a (or some IR/UV ratio) provides an equation that simultaneously fixes the overall scale of the lepton masses and the ratio kappa_*.

**Why this matters:**
- The Koide cone direction (kappa_*) and the overall mass scale are entangled: changing the overall scale changes all three masses proportionally, but the cone direction (kappa_*) is intrinsic
- However, if the scale is derived from an equation of the form Tr(exp(H_sel(m))) = f(lattice), then this transcendental equation in m directly pins m_*
- The "remaining work" in the Koide note says "the remaining work is deriving the one overall scale from the lattice" — this might be exactly the m_* condition in disguise

**What to compute:** The function Tr(exp(H_sel(m))) as a function of m. Is it monotone? Does it equal a natural lattice scale target at m ≈ −1.161?

---

### Combination 4 (Medium priority): Drop F2 → Derive kappa_* from framework without G1 PMNS input

**What changes:** Find a pure Cl(3)/Z³ algebraic expression that gives kappa_* ≈ −0.608 without importing M_STAR, DELTA_STAR, Q_PLUS_STAR from the neutrino PMNS chamber.

**Candidates to try:**
- kappa_* from the geometric mean of the two doublet A eigenvalues at m_DA: (m_DA − GAMMA)^{1/2} · something
- kappa_* = −cos(arctan(GAMMA/√(2/3))): = −cos(arctan(1/2 / 0.816)) = −cos(arctan(0.612)) ≈ −cos(31.5°) ≈ −0.852. No.
- kappa_* from the ratio E2/E1 = √(8)/3 / √(8/3) = 1/√3 ≈ 0.577 — close to |kappa_*| ≈ 0.608 (5% off)
- kappa_* from the ratio GAMMA/(GAMMA + √(2/3)) = 0.5/(0.5+0.816) = 0.5/1.316 ≈ 0.380. No.
- kappa_* from sin(arccos(GAMMA)) = sin(60°) = √3/2 ≈ 0.866. No.
- kappa_* = −(1 − GAMMA²/3)^{1/2}: = −(1 − 0.0833)^{1/2} = −(0.9167)^{1/2} ≈ −0.957. No.

**More systematic search needed** over combinations {GAMMA=1/2, SELECTOR=√6/3, E1=√(8/3), E2=√8/3, √(2/3), 1/√3, 2/3} using PSLQ or continued fraction.

---

### Direction 5 (Speculative): Transport gap 4π/√6 encodes a scale constraint that pins m_*

**What changes:** If the transport gap ratio 4π/√6 ≈ 5.13 (vs observed 5.29) is derivable and exact, and if the 3.2% discrepancy encodes a correction factor that must be applied to the lattice propagator at m_*, this could provide the missing condition.

**The 3.2% discrepancy:** η/η_obs ≈ 0.189 = 1/5.29. If the true ratio is 1/(4π/√6) = √6/(4π) ≈ 0.195, the mismatch is 0.195 vs 0.189 ≈ 3.2%. A multiplicative correction factor of 0.189/0.195 ≈ 0.969 might correspond to a specific cos(angle) or another lattice geometry factor. This is speculative but the 3.2% gap suggests there's a correction whose origin is unknown.

---

## VI. Ranked List of Candidate New Directions

| Rank | Direction | Assumption dropped | Expected yield |
|------|-----------|--------------------|----------------|
| 1 | Eigenvalue-based Koide triplet: find (m,β) s.t. Q=eigenvalues=2/3 | M1, M2 | May provide algebraic (m,β) condition pinning m_* |
| 2 | O_0 level crossing in 4×4 sector: h_O0 = m/3 or other retained value | F4 | May give polynomial m_* condition from 4×4 matrix |
| 3 | Tr(exp(H_sel(m))) = scale target pins m_* | Met3 | Transcendental but derived from lattice |
| 4 | Pure Cl(3) expression for kappa_*: PSLQ over framework constants | F2 | Clean algebraic derivation if it exists |
| 5 | One-loop Coleman-Weinberg correction shifts V_eff minimum | M6 | g₂²/(4π²) ~ 0.006, probably too small |
| 6 | Non-uniform Z₃-phase baryon coupling shifts m_DA (not m_*) | P6 | Unlikely to close full gap |
| 7 | Transport gap 4π/√6 provides scale correction | — | Speculative, 3.2% unexplained mismatch |

---

## Appendix: Quick Numerics on Top Directions

### Direction 1: Eigenvalue Q=2/3 surface (checked)

The curve {(m, β) : Q(eigenvalues of exp(β H_sel(m))) = 2/3} exists and spans the full physical branch. Sampling on it:

| m | β | Q (eigenvalues) |
|---|---|-----------------|
| −1.286 | 0.556 | 2/3 |
| −1.025 | 0.602 | 2/3 |
| −0.765 | 0.642 | 2/3 |
| −0.244 | 0.689 | 2/3 |

Best PDG cos-similarity on this curve: **0.9961** at (m ≈ −1.260, β ≈ 0.560). This is notably worse than the standard approach (cos-sim > 0.9999), but without imposing Q=2/3 via the Koide formula. The β ≈ 0.556–0.689 range overlaps the gamma_orbit β_* ≈ 0.634 only at the upper end of the curve. The best eigenvalue point is at m ≈ −1.260, not m_* ≈ −1.161. **If β is independently fixed at β_* ≈ 0.634, the eigenvalue Q=2/3 condition gives m ≈ −0.790.**

### Direction 2: O_0 level crossing (checked)

For simple h_O0 choices (0, ±E1, m/3): no crossing of an H_sel eigenvalue at m ≈ −1.161. The only crossing found is at m ≈ −0.173 for h_O0 = −E1. This direction requires the coupling of O_0 to T_2 (the off-diagonal 4×4 block) to produce a non-trivial eigenvalue condition; the decoupled case is insufficient.

### Direction 3: Tr(exp(H_sel)) scale condition (checked)

Tr(exp(H_sel(m_*))) ≈ 9.491. This equals x[0,0] + x[1,1] + x[2,2] = 1.744 + 6.228 + 1.519. No natural lattice scale target is obvious. The function is monotone on the physical branch: decreasing from ≈10.033 at m_pos to ≈8.394 at m → 0.

---

## VII. Core Diagnostic

The analysis is trapped in a specific set of nested assumptions:

> **We imposed Q=2/3 via the Koide formula (u_small from v,w), then looked for the m selector in the space of polynomial/algebraic conditions on H_sel(m). This combination guarantees that kappa_* must be imported from outside (the H_* witness) because no polynomial condition on H_sel naturally produces a specific kappa value.**

The transcendental wall is NOT a fundamental obstruction — it is a consequence of seeking algebraic conditions on H_sel while the actual selector lives in exp(H_sel). The right question is:

**What condition on exp(H_sel(m)) (not on H_sel(m) itself) provides a natural physical selection of m_*?**

Candidates: eigenvalue Q=2/3, scale trace condition Tr(exp(H_sel)) = target, or a 4×4 eigenvalue crossing in the extended O_0 + T_2 sector. Direction 1 (eigenvalue Q=2/3) is the most promising because it combines the Koide constraint with the semigroup picture without importing anything from outside the framework.

# Hierarchy Derivation: Honest Top-to-Bottom Review

**Date:** 2026-04-13
**Purpose:** Determine what, if anything, survives after correcting three errors
**Verdict:** v is NOT derived. The framework gets the right ORDER OF MAGNITUDE
through a legitimate mechanism, but the exact match (v = 226 GeV) was an artifact
of mutually compensating errors.

---

## The Three Problems

### Problem 1: Sigma_1 was wrong

**Claimed:** Sigma_1 ~ 6.0, citing "Luscher-Weisz staggered fermion value"

**Actual:** The exact lattice integrals (`frontier_sigma1_exact.py`) give:

| Integral | d=4 value | Source |
|----------|-----------|--------|
| I_Wilson(4) | 0.154933 | Known exact (Watson-type) |
| I_stag(4) = 4 I_Wilson(4) | 0.619734 | Verified numerically + continuum |
| d * I_stag(4) | 2.479 | Naive dimension factor |
| d * I_Wilson(4) | 0.620 | Naive dimension factor |

No standard combination of these integrals gives Sigma_1 ~ 6. The value 6.0
may have been inspired by the staggered Z_2 wavefunction renormalization
coefficient z_2 ~ 5.82 in Feynman gauge (Hein et al, hep-lat/0003013), but
that coefficient applies to a DIFFERENT integral (the full self-energy diagram
including momentum-dependent pieces), not the simple propagator-at-origin
tadpole integral.

**Impact on v:**
- Sigma_1 = 6.0: Z_chi = 0.941, N_eff = 10.64, v = 45 GeV (factor 5.5 too low)
- Sigma_1 = 2.48: Z_chi = 0.976, N_eff = 11.43, v = 652 GeV (factor 2.6 too high)
- Sigma_1 = 3.81: Z_chi = 0.963, N_eff = 11.12, v = 246 GeV (exact match)

The needed Sigma_1 = 3.81 does not correspond to any known lattice integral.
The sigma1_exact.py script itself concludes (Section D-E) that the mapping from
lattice integrals to "Sigma_1" is convention-dependent and the factor ~ 9.56
converting I_stag(4) to the required value has no clear origin.

### Problem 2: Gauge corrections flip B at the Planck scale

**The CW coefficient** B = (1/64 pi^2) sum_i n_i (m_i/phi)^4 determines
whether dimensional transmutation occurs. B < 0 is required.

**At the EW scale** (SM couplings), the top dominates:

    |B_gauge/B_top| = 0.054  ->  B < 0  (EWSB works)

**At M_Pl with SM RG-run couplings** (g_2 ~ 0.51, g' ~ 0.46, y_t ~ 0.44):

    |B_gauge/B_top| = 0.597  ->  B < 0 but marginal

**At M_Pl with framework couplings** (g_2 = 0.65, g' = 0.50, sin^2 theta_W = 3/8):

    |B_gauge/B_top| = 1.37   ->  B > 0  (NO EWSB)

The framework's GUT-normalized gauge couplings at M_Pl are LARGER than the SM
RG-run values because the framework uses sin^2 theta_W = 3/8 (the SU(5)
unification value) with g_2 = 0.65, while the SM running gives g_2 ~ 0.51 at
M_Pl. This larger g_2 makes the W boson loop overwhelm the top quark loop.

With B > 0, the CW potential has NO non-trivial minimum. The dimensional
transmutation formula v = M_Pl * exp(-8pi^2 / (N_eff * y_t^2)) does not apply
because the mechanism that generates v does not trigger.

### Problem 3: The y_t value used was inconsistent

**The derivation chain claims:**
1. alpha_plaq = 0.092 from the Cl(3) lattice
2. g_s = sqrt(4 pi * 0.092) = 1.075
3. y_t = g_s / sqrt(6) = 0.439 (Ward identity + trace identity)
4. Sigma_1 ~ 6 gives Z_chi = 0.941
5. N_eff = 12 * Z_chi^2 = 10.64
6. v = M_Pl * exp(-8pi^2 / (10.64 * 0.9369^2)) = 226 GeV

**The inconsistency:** Step 3 derives y_t = 0.439. Step 6 uses y_t = 0.9369.

The value 0.9369 is the SM top Yukawa at mu = M_t (the pole mass scale), not at
M_Pl. The correct y_t to use in the CW formula evaluated at M_Pl is y_t(M_Pl),
which the framework says is 0.439. The SM value 0.9369 was smuggled in as an
observed input.

With y_t = 0.439 and N_eff = 10.64 (claimed values), v = 45 GeV, not 226 GeV.
With y_t = 0.439 and N_eff = 12 (bare, no Z_chi), v = 3.6 TeV.
The claimed v = 226 only works with y_t = 0.9369, which is NOT derived.

---

## What Actually Survives

### The order of magnitude IS right (and that matters)

With top-only CW and framework's bare y_t = 0.439:
- N_eff = 12 (no corrections): v = 3.6 TeV
- N_eff = 11.4 (correct Sigma_1 = 2.48): v = 652 GeV
- N_eff = 11.1 (needed for 246): v = 246 GeV

The framework genuinely produces v ~ O(100 GeV - 1 TeV) from dimensional
transmutation at M_Pl. This is a 16-order-of-magnitude hierarchy (v/M_Pl ~
10^{-16}) that emerges from an O(1) exponent. The mechanism is legitimate --
it is the standard Coleman-Weinberg mechanism applied at the Planck scale.

The residual factor of 3-15x (depending on corrections) is NOT fine-tuning.
The exponential sensitivity means a 10% shift in N_eff * y_t^2 changes v by a
factor of 10. The framework gets N_eff * y_t^2 ~ 2.1-2.3, and the target is
2.14. This is a legitimate near-miss.

### What the framework DOES determine

1. **y_t(M_Pl) ~ 0.44** from the Ward identity y_t = g_s/sqrt(6). This is
   structural and well-defended.

2. **The CW mechanism IS triggered** (top-only B < 0), provided gauge
   corrections are not so large as to flip the sign. With SM RG-run gauge
   couplings, B remains negative. With GUT-unified couplings, it depends on
   whether unification happens precisely at M_Pl.

3. **The hierarchy scale** v ~ M_Pl * exp(-8pi^2 / (12 * 0.193)) = 3.6 TeV
   is within one order of magnitude of 246 GeV without ANY corrections.

### What the framework does NOT determine

1. **The precise value of v.** The factor between 3.6 TeV and 246 GeV requires
   knowing Sigma_1 to within ~ 1 unit (need 3.81, simplest estimate gives 2.48).
   This is a lattice perturbation theory calculation, not a fundamental constant.

2. **Whether gauge corrections spoil the mechanism.** This depends on whether
   the gauge couplings at M_Pl are the GUT-unified values (g_2 = 0.65, which
   gives B > 0 and kills CW) or the SM RG-run values (g_2 ~ 0.51, which
   preserves B < 0). The framework must decide which applies.

3. **The matching scheme.** Different choices of what enters "Sigma_1" shift v
   by orders of magnitude. The lattice integral is exact; the mapping to the
   hierarchy formula is not.

---

## Why v = 226 GeV Was Wrong

The v = 226 result arose from three errors that partially compensated:

| Error | Effect on v | Direction |
|-------|------------|-----------|
| Used y_t = 0.9369 instead of 0.439 | Huge (exp sensitive) | Increased v massively |
| Used Sigma_1 = 6 instead of ~2.5 | Large (exp sensitive) | Decreased v by ~15x |
| Ignored gauge corrections to B | Moderate | Would decrease v further |

The first error (wrong y_t) increased v from ~ 50 GeV to ~ 5 * 10^5 GeV. The
second error (inflated Sigma_1) decreased it back to ~ 226 GeV. The "agreement"
was a coincidence of two wrongs making a right.

---

## Can Any Version of the Derivation Work?

### Option A: RG-improved CW (evaluate at crossover scale)

The CW potential should be evaluated not at M_Pl but at the scale mu_CW where:
(a) the tree-level Higgs quartic lambda(mu_CW) passes through zero, AND
(b) the top Yukawa dominates over gauge couplings.

In the SM, condition (a) occurs near mu ~ 10^{10} GeV (the famous "metastability
scale"). At that scale, y_t ~ 0.5 and g_2 ~ 0.54, so the top still dominates.
Dimensional transmutation from mu_CW ~ 10^{10} would give v ~ 10^{10} * exp(...)
which requires a different formula entirely.

**Verdict:** This changes the problem structure. It is no longer a "hierarchy from
M_Pl" story but a "hierarchy from the instability scale" story. The framework
would need to derive lambda(mu) = 0 at mu ~ 10^{10} GeV, which requires the full
SM RGE -- importing more physics than the framework contains.

### Option B: Lattice naturalness (no fine-tuning, O(1) bare mass)

The frontier_higgs_mass.py script (PART 5) shows that on the lattice with cutoff
Lambda = pi/a, the Barbieri-Giudice fine-tuning measure Delta ~ 0.5 (no
fine-tuning). The quadratic divergence is absent because the lattice sum is
finite. This means:

- v ~ Lambda / (4pi) ~ M_Pl / (4pi) ~ 6 * 10^{16} GeV (too high by 10^{14})

This does NOT give the right v. It says the natural EW scale on the lattice is
O(M_Pl), not O(100 GeV). The hierarchy problem is not solved by mere UV
finiteness.

### Option C: Accept v as a derived O(TeV) quantity with O(1) uncertainty

The honest statement: the CW mechanism with y_t = 0.439 and N_eff = 12 gives
v ~ 3.6 TeV. The true v is 246 GeV, a factor of 15 lower. The framework
predicts the hierarchy v/M_Pl ~ 10^{-15.5} vs the observed 10^{-16.4}. This is
a prediction of the right order of magnitude from a genuine mechanism (not
fine-tuning), with an O(1) residual that cannot be pinned down without a precise
lattice perturbation theory calculation.

**This is the honest version.** It is still a meaningful result: the CW mechanism
with the framework's structural y_t produces v in the right ballpark. But it is
NOT a derivation of v = 246 GeV.

---

## What the Paper Should Say

### Do say:

"The Coleman-Weinberg mechanism with y_t(M_Pl) = g_s/sqrt(6) = 0.439 produces
dimensional transmutation at v ~ M_Pl * exp(-8pi^2/(12 * y_t^2)) ~ 3.6 TeV,
within one order of magnitude of the observed electroweak scale. The 16-order-
of-magnitude hierarchy v/M_Pl ~ 10^{-16} is a structural consequence of the
exponential sensitivity of CW to y_t^2, which is fixed by the Ward identity to
be ~ 0.19. No fine-tuning or small parameters are introduced."

"Lattice corrections (wavefunction renormalization, gauge boson loops) modify
the effective N_eff by O(1) amounts, shifting v by factors of O(1-10). A
precise determination requires computing the staggered self-energy on the Cl(3)
lattice and properly accounting for gauge boson contributions to the CW
potential at M_Pl, where they are comparable in magnitude to the top loop."

### Do NOT say:

- "v = 226 GeV is derived" (it was not)
- "Sigma_1 = 6.0" (this value has no clear lattice origin)
- "The hierarchy problem is solved" (the O(10) residual is real)
- "v is no longer a boundary condition" (it effectively still is, up to
  the O(10) ambiguity)

### Boundary conditions:

The paper should list THREE boundary conditions (T_CMB, H_0, v), not two.
v = 246 GeV is constrained to the right order of magnitude but not derived.

---

## Summary

| Claim | Status | Corrected |
|-------|--------|-----------|
| Sigma_1 = 6.0 | WRONG | Sigma_1 ~ 2.5 (d*I_stag) or ~5.8 (Hein z_2) |
| y_t = 0.9369 in formula | WRONG (observed input) | y_t = 0.439 (derived) |
| N_eff = 10.64 | Wrong (from wrong Sigma_1 + wrong y_t) | N_eff ~ 11.4 (with Sigma_1=2.5) |
| v = 226 GeV | WRONG | v ~ 650-3600 GeV (top-only) |
| B < 0 at M_Pl | DEPENDS on gauge couplings | B < 0 with SM g_2; B > 0 with GUT g_2 |
| Hierarchy explained | PARTIALLY | O(magnitude) yes, exact value no |
| v is free parameter | YES, within O(10) | Framework constrains v to O(0.1-10 TeV) |

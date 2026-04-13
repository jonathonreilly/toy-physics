# Response to Codex Retain Audit: DM Ratio Lane

**Date:** 2026-04-12
**Branch:** `claude/youthful-neumann`
**Responding to:** Codex review on `codex/review-active`
**Verdict:** 2 of 5 objections fully closed, 1 substantially mitigated, 2 still standing

---

## Objection 1: "the alpha_s runner hard-codes g = 1"

**Codex claim:** alpha_s = 0.092 uses g_bare = 1 as input.

**Our position in the scripts:** All three DM relic scripts set `G_BARE = 1.0` on line 89 (mapping), line 89 (gap-closure), line 88 (synthesis). The coupling chain is:

```
G_BARE = 1.0
ALPHA_BARE = G_BARE^2 / (4*pi) = 1/(4*pi) = 0.0796
ALPHA_PLAQ = -ln(1 - (pi^2/3)*ALPHA_BARE) / (pi^2/3) = 0.0923
ALPHA_V = ALPHA_BARE / U0^4 = 0.092
```

**Honest assessment: Codex is correct. g_bare = 1 is an INPUT, not a derivation.**

The argument that "on a lattice with a = l_Planck, the coupling is O(1)" is true but insufficient. Here is why:

1. **O(1) is not = 1.** Strong coupling on a Planck-scale lattice means g is O(1), i.e., somewhere in the range [0.3, 3]. The specific value g = 1.000 is not forced by any lattice theorem. A lattice field theory at the cutoff has a bare coupling that depends on the regularization details.

2. **There is no uniqueness argument.** In standard lattice gauge theory, beta = 2*N_c/g^2 is a free parameter. Setting g = 1 is equivalent to choosing beta = 6 for SU(3). This is a particular point on the bare coupling axis, not a fixed point or a uniqueness result.

3. **What WOULD close this:** A derivation showing that the Cl(3) framework forces g_bare to a specific value -- e.g., via a fixed-point condition, an anomaly cancellation requirement at the cutoff, or a self-consistency condition. No such derivation exists in our scripts.

4. **The "natural value" defense is weak.** Saying "g = 1 in natural units is the unique dimensionless value" conflates dimensional analysis with dynamics. The coupling is dimensionless in 4D, so ANY value is "natural." The number 1 has no special status without a dynamical argument.

**Mitigation:** The sensitivity is moderate. alpha_s in [0.08, 0.10] gives R in [5.17, 5.68]. So even if g_bare is uncertain by ~10%, R stays within 10% of observation. But this is a CONSISTENCY WINDOW, not a derivation.

**Status: OBJECTION STANDS.** g_bare = 1 is assumed, not derived. The DM ratio result should be stated as "R = 5.48 at the natural coupling g_bare = 1, with R in [5.2, 5.9] for g in [0.9, 1.1]."

---

## Objection 2: "the Sommerfeld runner hard-codes observed abundance values and freeze-out parameters"

**Codex claim:** The Sommerfeld computation imports freeze-out parameters tied to observed abundances.

**Our response (FREEZEOUT_FROM_LATTICE_NOTE.md) claims:**
- g_* = 106.75 derived from taste spectrum counting
- x_F = 25 derived from the lattice Boltzmann equation
- v_rel = 2/sqrt(x_F) from equipartition

**Honest assessment: This objection is SUBSTANTIALLY addressed but not fully closed.**

**What IS closed:**
- g_* = 106.75: This genuinely follows from the taste spectrum decomposition 8 = (2,3) + (2,1) with 3 generations from Z_3 orbits. The counting (28 bosonic + 7/8 * 90 fermionic = 106.75) is structural. The 7/8 factor comes from Fermi-Dirac vs Bose-Einstein statistics, which is encoded in the staggered fermion sign structure. This is solid.

- x_F = 25: This is derived from the freeze-out condition Gamma_ann = H, which itself comes from the lattice master equation in the thermodynamic limit. The logarithmic insensitivity (x_F varies only from 15 to 45 over 16 orders of magnitude in mass) means the exact value barely matters. This is legitimate.

**What is NOT closed:**
- The Sommerfeld factor S_vis is computed using the COULOMB potential V(r) = -alpha_eff/r. This is a perturbative QFT result for the one-gluon-exchange potential. It is NOT derived from the lattice -- it is the continuum QCD potential imported into the Sommerfeld formula. See Objection 3.

- The freeze-out equation itself (dn/dt + 3Hn = -<sigma*v>(n^2 - n_eq^2)) is claimed to be the thermodynamic limit of the lattice master equation. This is plausible and physically motivated, but the limit is demonstrated numerically, not proved as a theorem. The gap-closure note correctly labels this DERIVED (not NATIVE).

**Status: MOSTLY ADDRESSED.** The g_* and x_F parts are genuinely structural. The residual weakness is the Sommerfeld potential shape (Objection 3) and the thermodynamic limit assumption.

---

## Objection 3: "the structural Sommerfeld runner still imports freeze-out machinery through the Boltzmann equation, g_* = 106.75, and sigma_v ~ pi*alpha_s^2/m^2"

**Codex claim:** sigma_v ~ pi*alpha_s^2/m^2 is imported from perturbative QFT.

**Honest assessment: Codex is correct on sigma_v. This is the most serious remaining objection.**

The annihilation cross-section sigma_v = pi * alpha_s^2 / m^2 appears in:
- `frontier_dm_ratio_structural.py` line 468/483
- `frontier_freezeout_from_lattice.py` line 344
- `frontier_dm_relic_mapping.py` (implicitly through x_F computation)

**Where does this formula come from?**

It is the tree-level (Born approximation) s-wave annihilation cross-section for fermion-antifermion annihilation via gauge boson exchange. Specifically:

    sigma_v = (pi * alpha^2 / m^2) * (color factor)

This is a PERTURBATIVE QFT RESULT. It requires:
1. Feynman diagram computation of the 2->2 amplitude
2. The Born approximation (leading order in alpha)
3. The non-relativistic limit (s-wave dominance)

**None of these steps are derived from the lattice.** The lattice defines alpha_s (from the plaquette), but the FORMULA sigma = pi*alpha^2/m^2 is standard perturbative field theory.

**What would close this:** Computing the annihilation cross-section directly on the lattice, e.g., via the lattice two-point function or the optical theorem applied to lattice Green's functions. The `SOMMERFELD_LATTICE_GREENS_NOTE.md` and `DM_RATIO_STRUCTURAL_NOTE.md` argue that the Sommerfeld factor S = G_Coulomb(0)/G_free(0) is a lattice observable (ratio of lattice Green's functions). This is correct for the ENHANCEMENT FACTOR, but the base cross-section sigma_0 = pi*alpha^2/m^2 is still the perturbative result.

**How serious is this?** It is serious for the claim "derived from lattice axioms alone." The functional form sigma ~ alpha^2/m^2 is dictated by dimensional analysis and the gauge coupling structure, so in a sense it is "structural." But the coefficient pi (rather than, say, 4*pi or pi/2) comes from the explicit Feynman diagram. This is textbook QFT, not lattice combinatorics.

**Mitigation:** The coefficient of sigma_v affects R only through x_F, which depends logarithmically on sigma_v. Changing the coefficient by a factor of 2 shifts x_F by ~2 units, which changes R by ~1%. So the sensitivity is low. But Codex's point is about PROVENANCE, not about numerical impact.

**Status: OBJECTION STANDS.** sigma_v = pi*alpha_s^2/m^2 is imported from perturbative QFT. The lattice derivation of alpha_s is real, but the cross-section formula is not derived from the lattice.

---

## Objection 4: "the full ratio is not yet derived from the lattice axioms alone"

**Codex claim:** The complete derivation chain has imports that prevent claiming "from lattice axioms alone."

**Honest assessment: Codex is correct. Here is the complete provenance chain.**

### PROVENANCE CHAIN FOR R = 5.48

```
R = (3/5) * (f_vis/f_dark) * S_vis

Factor 1: MASS_RATIO = 3/5
  Source: Hamming weight spectrum on Cl(3) bit strings
  Provenance: NATIVE (lattice combinatorics, zero imports)

Factor 2: f_vis/f_dark = (C_F*dim_adj_SU3 + C2_SU2*dim_adj_SU2) / (C2_SU2*dim_adj_SU2)
         = (4/3*8 + 3/4*3) / (3/4*3) = (32/3 + 9/4) / (9/4) = 155/27 = 5.741
  Source: SU(3) x SU(2) Casimir operators and adjoint dimensions
  Provenance: NATIVE (group theory of lattice gauge group)

Factor 3: S_vis = thermally averaged Sommerfeld factor = 1.592
  Depends on:
    (a) alpha_s = 0.092
        Source: Plaquette action with G_BARE = 1.0
        Provenance: G_BARE = 1 is ASSUMED (Objection 1)
                    Plaquette -> alpha_plaq transformation is NATIVE
    (b) x_F = 25 (freeze-out ratio)
        Source: Lattice Boltzmann equation, Gamma_ann = H condition
        Provenance: DERIVED (thermodynamic limit of lattice master eq.)
        Sub-dependencies:
          - Boltzmann equation: DERIVED from lattice master equation
          - H(T): DERIVED from Poisson coupling + spectral energy density
          - g_* = 106.75: NATIVE (taste spectrum)
          - sigma_v = pi*alpha_s^2/m^2: IMPORTED (perturbative QFT, Objection 3)
          - n_eq ~ exp(-m/T): NATIVE (heat kernel on lattice)
          - H > 0: DERIVED from spectral gap + 2nd law (AXIOM)
    (c) V(r) = -C_F*alpha_s/r (Coulomb potential shape)
        Source: One-gluon exchange in QCD
        Provenance: IMPORTED (perturbative QFT)
        Note: The 1/r form is also the lattice Green's function of the
              3D Laplacian, so this is "compatible with" the lattice,
              but the identification V_QCD = lattice_Green is an
              additional physical assumption.
    (d) Sommerfeld formula S = pi*zeta/(1 - exp(-pi*zeta))
        Source: Coulomb scattering quantum mechanics
        Provenance: DERIVED (follows from Schrodinger equation with
                    Coulomb potential; equivalent to lattice Green's
                    function ratio per DM_RATIO_STRUCTURAL_NOTE.md)
```

### SUMMARY TABLE

| Input | Value | Status | Notes |
|-------|-------|--------|-------|
| Mass ratio 3/5 | 0.600 | NATIVE | Hamming weights on Cl(3) |
| C_F (SU3) | 4/3 | NATIVE | Group theory |
| dim_adj (SU3) | 8 | NATIVE | Group theory |
| C2 (SU2) | 3/4 | NATIVE | Group theory |
| dim_adj (SU2) | 3 | NATIVE | Group theory |
| g_* | 106.75 | NATIVE | Taste spectrum |
| n_eq ~ exp(-m/T) | -- | NATIVE | Heat kernel |
| H > 0 | -- | DERIVED | Spectral gap + 2nd law |
| Boltzmann equation | -- | DERIVED | Lattice master eq. + thermo limit |
| Friedmann equation | -- | DERIVED | Poisson coupling |
| Sommerfeld formula | -- | DERIVED | Schrodinger eq. / lattice Green's fn |
| x_F = 25 | -- | DERIVED | Boltzmann eq. (log-insensitive) |
| **g_bare = 1** | **1.0** | **ASSUMED** | **Not derived from lattice** |
| **sigma_v = pi*alpha^2/m^2** | -- | **IMPORTED** | **Perturbative QFT** |
| **V(r) = -alpha/r** | -- | **IMPORTED** | **One-gluon exchange** |

**Count: 7 NATIVE, 5 DERIVED, 1 ASSUMED, 2 IMPORTED**

The "zero imports" claim in DM_RELIC_SYNTHESIS_NOTE.md is overstated. The honest count is 1 assumed parameter (g_bare) and 2 imported formulas (sigma_v and V(r)).

**Status: OBJECTION STANDS in its strong form.** The ratio is not "from lattice axioms alone." It is from lattice axioms + one assumed coupling + perturbative QFT for the cross-section and potential shape. The weaker claim -- that R is determined by structural quantities with only one weakly-constrained parameter -- remains valid.

---

## Objection 5: "keep only a bounded consistency-window note unless the coupling is derived without matching to the observed dark-matter ratio"

**Codex recommendation:** Downgrade the DM ratio to a consistency-window result unless g_bare is independently derived.

**Honest assessment: This is the correct framing for a Nature submission.**

The current situation is:
- The STRUCTURE of R (= mass ratio * channel ratio * Sommerfeld enhancement) is genuinely derived from the lattice.
- The NUMERICAL VALUE R = 5.48 requires g_bare = 1 (assumed) and perturbative cross-section formulas (imported).
- The observed R_obs = 5.47 falls within the consistency window R in [5.2, 5.9] for g_bare in [0.9, 1.1].

**What the paper should say:**

> The Cl(3) lattice structure determines the dark-to-visible matter ratio
> up to one parameter: the bare gauge coupling g at the lattice cutoff.
> The structural factors (mass ratio 3/5, Casimir channel ratio 155/27)
> are parameter-free. The Sommerfeld enhancement introduces the coupling
> dependence. At the natural value g_bare = 1, R = 5.48, matching the
> observed R = 5.47 to 0.2%. The consistency window g in [0.9, 1.1]
> spans R in [5.2, 5.9], comfortably containing the observation.
> 
> The base cross-section sigma_v = pi*alpha_s^2/m^2 is the standard
> perturbative s-wave result; deriving it directly from lattice
> observables remains open.

**Status: ACCEPT Codex's recommendation.** Frame as "consistency window with structural backbone" rather than "parameter-free prediction from lattice axioms."

---

## Summary of Verdicts

| # | Objection | Verdict | Action |
|---|-----------|---------|--------|
| 1 | g_bare = 1 is assumed | **STANDS** | Acknowledge; report R(g) window |
| 2 | Freeze-out parameters imported | **MOSTLY CLOSED** | g_* and x_F are structural; cite taste spectrum and lattice Boltzmann |
| 3 | sigma_v imported from pert. QFT | **STANDS** | Acknowledge; note low sensitivity via x_F |
| 4 | Not from lattice axioms alone | **STANDS** | Correct provenance table above; 1 assumed + 2 imported |
| 5 | Downgrade to consistency window | **ACCEPT** | Reframe paper claim accordingly |

## What Would Fully Close the Lane

1. **Derive g_bare from a lattice fixed-point or self-consistency condition.** E.g., show that the Cl(3) algebra + anomaly cancellation + unitarity forces g to a specific value. This would close Objection 1.

2. **Compute sigma_v directly on the lattice.** Use the optical theorem on lattice correlators to extract the annihilation cross-section without importing Feynman diagrams. This would close Objection 3.

3. **Prove the thermodynamic limit.** Show rigorously that the lattice master equation converges to the Boltzmann equation as N -> infinity for the Z^3 graph family. This would upgrade the DERIVED items to PROVED.

None of these are achieved in the current scripts.

## Impact on Nature Framing

The DM ratio remains one of the strongest results in the framework:
- The structural backbone (mass ratio, channel counting, Sommerfeld mechanism) is genuine
- The numerical match R = 5.48 vs 5.47 is striking even as a consistency result
- The sensitivity to g_bare is moderate (10% in g -> 10% in R)

But the claim must be downgraded from "zero-parameter prediction from lattice axioms" to "one-parameter consistency window with structural backbone." Codex is right to hold this lane until the coupling is independently derived.

---

## Scripts Reviewed

- `/Users/jonBridger/Toy Physics/scripts/frontier_dm_relic_mapping.py`
- `/Users/jonBridger/Toy Physics/scripts/frontier_dm_relic_gap_closure.py`
- `/Users/jonBridger/Toy Physics/scripts/frontier_dm_relic_synthesis.py`
- `/Users/jonBridger/Toy Physics/scripts/frontier_dm_ratio_structural.py`
- `/Users/jonBridger/Toy Physics/scripts/frontier_freezeout_from_lattice.py`

## Notes Reviewed

- `docs/FREEZEOUT_FROM_LATTICE_NOTE.md`
- `docs/DM_RELIC_MAPPING_THEOREM_NOTE.md`
- `docs/DM_RELIC_GAP_CLOSURE_NOTE.md`
- `docs/DM_RELIC_SYNTHESIS_NOTE.md`
- `docs/DM_RATIO_STRUCTURAL_NOTE.md`
- `docs/DM_RATIO_SOMMERFELD_NOTE.md`
- `docs/ALPHA_S_DM_RATIO_RESULT_2026-04-12.md`
- `docs/CODEX_REVIEW_PACKET_2026-04-12.md`

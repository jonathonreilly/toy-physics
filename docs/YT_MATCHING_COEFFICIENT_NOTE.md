# y_t Matching Coefficient: Lattice-to-Continuum at M_Pl

## Status

**BOUNDED** -- The lattice-to-continuum matching coefficient delta_match is computed at 1-loop. It is small (~0.6%) and well-controlled, but it does NOT close the 6.5% gap between the m_t prediction (184 GeV) and observation (173 GeV). The y_t lane remains bounded.

**Script:** `scripts/frontier_yt_matching_coefficient.py`

---

## Theorem / Claim

**Claim (Matching Coefficient Computation).**

The lattice-to-continuum matching coefficient for the ratio y_t/g_s = 1/sqrt(6) at the Planck scale cutoff is:

    delta_match = -0.0059 +/- 0.0018

    = (-0.59 +/- 0.18)%

This converts the lattice Yukawa-gauge ratio to the MS-bar continuum scheme:

    (y_t/g_s)^{MS}(M_Pl) = (1/sqrt(6)) * (1 + delta_match)

The coefficient is computed from:

    delta_match = (alpha_V / pi) * [C_F * c_m - c_{V->MS} / 2]

where:
- c_m = -0.4358 is the staggered fermion mass matching coefficient (Hein et al., PRD 62, 074503, 2000)
- c_{V->MS} = -0.76 is the V-scheme to MS-bar gauge coupling matching (Schroder, PLB 447, 321, 1999)
- alpha_V = 0.092 is the V-scheme coupling at M_Pl (derived from g_bare = 1)
- C_F = 4/3 is the SU(3) Casimir

---

## Assumptions

1. **Framework axiom A5:** Cl(3) staggered fermions on Z^3.
2. **Bare UV theorem:** y_t = g_s/sqrt(6) at the lattice scale (proved).
3. **Cl(3) preservation under RG:** Proved in frontier_yt_cl3_preservation.py.
4. **Literature matching coefficients:** c_m and c_{V->MS} are imported from published lattice QCD computations for staggered fermions with the Wilson gauge action.

Assumption 4 is the key bounded input: the matching coefficients are not derived from the framework but computed in lattice perturbation theory for the specific lattice action.

---

## What Is Actually Proved

### 1. Lattice vertex corrections (EXACT on finite lattice)

On the L=8 staggered Cl(3) lattice:
- The Yukawa vertex correction factorizes as Gamma_Y = G5 * Sigma, verified to machine precision (rel err ~5e-17). This follows from G5 being central in Cl(3).
- The gauge vertex correction does NOT factorize (G_mu does not commute with propagators).
- The Z-factor difference delta_Z_Y - delta_Z_g varies with external momentum (momentum-dependent: mean -0.72 +/- 0.20 across 8 momenta).

### 2. Matching coefficient (BOUNDED)

Using literature matching coefficients for staggered fermions:
- Yukawa matching: delta_Y = C_F * c_m * alpha/pi = -0.0170
- Gauge matching: delta_g = (c_{V->MS}/2) * alpha/pi = -0.0111
- Ratio matching: delta_match = delta_Y - delta_g = -0.0059

The Ward identity constrains: |delta_match| < alpha_s/pi = 0.029. The computed value 0.006 is well within this bound.

### 3. Impact on m_t prediction (BOUNDED)

- m_t [bare, no matching] = 184.2 GeV
- m_t [with matching]     = 183.8 GeV (shift: -0.4 GeV)
- m_t [observed]          = 173.0 GeV

The matching narrows the old +/-15% uncertainty band from [172, 194] GeV (width 22 GeV) to [180, 187] GeV (width 7 GeV) using +/-5% residual scheme uncertainty.

### 4. Honest gap assessment

The 6.5% gap between prediction (184 GeV) and observation (173 GeV) is NOT closed by the matching coefficient. The matching shifts m_t by only -0.4 GeV (0.2%), far too small to bridge the 11 GeV gap. The new narrowed band [180, 187] GeV does not contain the observed 173 GeV.

The residual 6.5% gap likely requires:
- Higher-order (2-loop+) RGE matching between V-scheme and MS-bar at M_Pl
- Threshold corrections from integrating out heavy states
- Or it may represent a genuine framework tension that bounds the prediction

---

## What Remains Open

1. **The 6.5% m_t overshoot.** The matching coefficient is too small to close this gap. The dominant uncertainty is not the matching itself but the scheme conversion and the particular choice of alpha_V = 0.092 as the boundary condition.

2. **2-loop matching.** The 2-loop matching coefficient would give O(alpha^2/pi^2) ~ 0.09% corrections, negligible compared to the 6.5% gap.

3. **Non-perturbative matching.** Step-scaling or similar methods could eliminate perturbative matching uncertainty entirely, but would not address the 6.5% gap.

4. **Scheme conversion at M_Pl.** The V-scheme coupling alpha_V = 0.092 is derived from g_bare = 1 via Lepage-Mackenzie tadpole resummation. The MS-bar coupling at the same scale is much smaller (~0.02 from 1-loop extrapolation). This factor-of-4 scheme difference at M_Pl is where the dominant uncertainty lives. Whether the RGE boundary condition should use the V-scheme or MS-bar coupling is a genuine open question for the framework.

What is NOT open:
- The matching coefficient is computed: delta_match = -0.006.
- The Ward identity is satisfied.
- The sign is correct (pushes m_t toward observed).
- Perturbation theory is reliable at alpha_s/pi ~ 0.03.

---

## How This Changes The Paper

### Before this work:

- delta_match was bounded at ~10% by power counting
- The m_t prediction band was [172, 194] GeV (width 22 GeV)
- The matching was described as "computable but not computed"

### After this work:

- delta_match = -0.006 +/- 0.002 (computed)
- The m_t prediction band narrows to [180, 187] GeV (width 7 GeV)
- The matching sub-gap is resolved: it is small and well-controlled
- A new honest finding: the narrowed band does NOT contain 173 GeV
- The dominant remaining uncertainty is scheme conversion, not matching

### Paper-safe wording:

> The lattice-to-continuum matching coefficient for y_t/g_s = 1/sqrt(6) is computed at 1-loop using staggered fermion matching coefficients, giving delta_match = -0.006, well within the Ward identity bound. The matching shifts the m_t prediction by -0.4 GeV, from 184.2 to 183.8 GeV. The 6.5% overshoot relative to the observed 173.0 GeV persists; the narrowed prediction band [180, 187] GeV no longer contains the observed value when matching uncertainty is reduced from +/-15% to +/-5%. The remaining gap is dominated by scheme conversion uncertainties at the Planck scale, not by the matching coefficient.

### Lane status:

- y_t renormalized: BOUNDED (matching sub-gap computed, but 6.5% gap persists)
- This does NOT upgrade the lane to CLOSED
- The matching computation is a tightening, not a closure

---

## Commands Run

```bash
cd "/Users/jonBridger/Toy Physics"
python3 scripts/frontier_yt_matching_coefficient.py
```

**Output:** PASS=22 FAIL=0

**Test classification:**
- 9 exact checks: all PASS (Cl(3) centrality, Yukawa factorization, Ward identity, power counting)
- 13 bounded checks: all PASS (matching coefficients, m_t prediction, band narrowing, residual gap honesty)

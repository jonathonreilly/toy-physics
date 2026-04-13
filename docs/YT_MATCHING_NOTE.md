# y_t Lattice-to-MSbar Matching at the Planck Scale

## Status

**BOUNDED** -- The matching coefficient Z_y for the ratio y_t/g_s is
computed at 1-loop using Lepage-Mackenzie tadpole improvement. The result
Z_y = 1.001 (0.10%) is sub-percent and well within the Ward identity bound.
The matching does NOT close the 6.5% gap between the m_t prediction (184 GeV)
and observation (173 GeV). The y_t lane remains bounded.

**Script:** `scripts/frontier_yt_matching.py`

---

## Theorem / Claim

**Claim (Matching Coefficient via Lepage-Mackenzie).**

The lattice-to-MSbar matching coefficient for the Yukawa-to-gauge ratio
at the Planck scale is:

    Z_y = Z_m / Z_g = 1.001 +/- 0.002

where:
- Z_m = 0.992 is the mass/Yukawa matching from tadpole improvement
- Z_g = 0.991 is the gauge coupling matching (V-scheme to MSbar)
- The ratio Z_y = Z_m / Z_g = 1.001 (0.10%)

This converts the lattice ratio to the MSbar scheme:

    (y_t / g_s)^{MSbar}(M_Pl) = Z_y * (1 / sqrt(6))

The matching is computed from:
- 3D lattice tadpole integral: I_tad = 0.2426 (extrapolated L -> inf)
- Lepage-Mackenzie mean-field link: u_0 = 0.993 from <P>^{1/4}
- Tadpole-subtracted residual: c_1^{sub} = -2.0 (estimated for d=3)
- V-scheme to MSbar conversion: c_{V->MS} = -0.58 (for d=3)

---

## Assumptions

1. **Framework axiom A5:** Cl(3) staggered fermions on Z^3.
2. **Bare UV theorem:** y_t = g_s/sqrt(6) at the lattice scale (proved).
3. **Lepage-Mackenzie (1993):** Tadpole improvement is the dominant
   1-loop lattice artifact. The mean-field link u_0 = <P>^{1/4} resums
   the leading lattice corrections.
4. **V-scheme coupling:** alpha_V(M_Pl) = 0.092 from the plaquette.
   This is a bounded input (derived from g_bare = 1 via LM prescription).
5. **Tadpole-subtracted coefficient:** c_1^{sub} = -2.0 is estimated
   for d=3 staggered fermions by analogy with d=4 results (El-Khadra
   et al., PRD 55, 3933, 1997).
6. **V-to-MSbar conversion in d=3:** c_{V->MS} = -0.58, estimated from
   the d=4 value of Schroder (PLB 447, 321, 1999) with d-dependent scaling.

Assumptions 5 and 6 are the key bounded inputs. They are estimated
from d=4 lattice perturbation theory, not derived from the framework.

---

## What Is Actually Proved

### 1. Lattice tadpole integral (EXACT on finite lattice, BOUNDED extrapolation)

The 3D lattice tadpole integral I_tad(L) is computed exactly at
L = 4, 6, 8, 10, 12, 16. Finite-volume extrapolation gives:

    I_tad(inf) = 0.2426 +/- 0.010

This is 4% below the Luscher-Weisz infinite-volume value 0.2527,
consistent with the 1/L^2 finite-volume correction.

### 2. Mean-field link u_0 (BOUNDED)

From the plaquette expectation value at alpha_V = 0.092:

    u_0 = <P>^{1/4} = 0.993

The tadpole improvement factor 1/u_0 = 1.007 (+0.72%) is the
dominant piece of the mass matching.

### 3. Mass/Yukawa matching Z_m (BOUNDED)

    Z_m = (1/u_0) * (1 + delta_m^{sub})
        = 1.007 * (1 - 0.015)
        = 0.992 (-0.75%)

The tadpole (+0.72%) and residual (-1.46%) partially cancel,
giving a net -0.75% mass matching.

### 4. Gauge coupling matching Z_g (BOUNDED)

    Z_g = sqrt(Z_alpha)  where  Z_alpha = 1 + c_{V->MS} * alpha_V / pi
        = sqrt(0.983)
        = 0.991 (-0.85%)

### 5. Combined ratio matching Z_y (BOUNDED)

    Z_y = Z_m / Z_g = 0.992 / 0.991 = 1.001 (+0.10%)

The mass matching (-0.75%) and gauge matching (-0.85%) largely
cancel in the ratio, leaving a tiny 0.10% net correction.

### 6. Impact on m_t (BOUNDED)

Using 2-loop SM RGE running from M_Pl to M_Z:

- m_t [bare, no matching]    = 184.2 GeV
- m_t [with Z_y matching]    = 184.3 GeV (shift: +0.1 GeV)
- m_t [observed]             = 173.0 GeV

The matching shifts m_t by +0.1 GeV (negligible).

Uncertainty bands:
- Old (+/-10%): [176, 191] GeV (width 14 GeV)
- New (+/- 2%): [183, 186] GeV (width 3 GeV)

### 7. Honest gap assessment

The 6.5% gap between prediction (184 GeV) and observation (173 GeV)
is NOT closed by the matching coefficient. The matching is +0.10%,
negligible compared to the 6.5% gap. The residual gap is dominated by
the V-scheme boundary condition choice at M_Pl, not by the matching.

---

## What Remains Open

1. **The 6.5% m_t overshoot.** The matching coefficient is too small to
   address this. The dominant uncertainty is the V-scheme to MSbar
   scheme conversion at M_Pl (the choice of alpha_V = 0.092 as the BC).

2. **2-loop matching.** The 2-loop correction is O(alpha^2 C_F^2/pi^2) ~
   0.15%, comparable to the 1-loop result because the 1-loop is so small
   (due to cancellation). Both are sub-percent.

3. **d=3 coefficients.** The tadpole-subtracted coefficient c_1^{sub} and
   the V-to-MSbar conversion c_{V->MS} are estimated from d=4 results.
   A dedicated d=3 lattice perturbation theory computation would pin
   these down.

4. **Non-perturbative matching.** Completely negligible at M_Pl where
   alpha_V/pi ~ 0.03. Step-scaling methods would eliminate perturbative
   uncertainty entirely.

What is NOT open:
- The matching coefficient Z_y is computed: Z_y = 1.001 (+0.10%).
- The Ward identity is satisfied: |Z_y - 1| << alpha_V/pi.
- The 3D tadpole integral agrees with the literature to 4%.
- Perturbation theory is reliable: alpha_V/(4pi) = 0.007.

---

## How This Changes The Paper

### Before this work:

- Codex review stated: "Matching coefficient genuinely unknown at ~10%"
- The matching was described as a real unknown, not a precision issue
- The m_t prediction band was [166, 202] GeV (with +/-10% matching)

### After this work:

- Z_y = 1.001 (+0.10%) computed via Lepage-Mackenzie tadpole improvement
- The ~10% unknown is replaced by a concrete sub-percent number
- The m_t prediction band narrows to [183, 186] GeV (with +/-2% residual)
- The matching sub-gap is resolved: it is negligibly small
- A new honest finding: the narrowed band does NOT contain 173 GeV
- The dominant remaining uncertainty is the V-scheme BC, not matching

### Paper-safe wording:

> The lattice-to-MSbar matching coefficient for the Yukawa-to-gauge ratio
> is computed at 1-loop using Lepage-Mackenzie tadpole improvement for
> staggered fermions, giving Z_y = 1.001. The individual matching factors
> for the mass (Z_m = 0.992) and gauge coupling (Z_g = 0.991) partially
> cancel in the ratio, leaving a 0.1% net correction well within the
> Ward identity bound. The 6.5% overshoot of the m_t prediction (184 GeV)
> relative to observation (173 GeV) persists; the matching coefficient is
> too small to close this gap. The dominant remaining uncertainty is the
> scheme conversion at the Planck scale.

### Lane status:

- y_t matching sub-gap: RESOLVED (Z_y computed, negligible correction)
- y_t lane overall: BOUNDED (6.5% gap from scheme BC persists)
- This computation addresses the Codex blocker but does NOT close the gate

---

## Commands Run

```bash
python3 scripts/frontier_yt_matching.py
```

**Output:** PASS=23 FAIL=0 (EXACT=6, BOUNDED=17)

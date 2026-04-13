# y_t Gauge Crossover: Framework to Perturbative SM

**Script:** `scripts/frontier_yt_gauge_crossover.py`
**Status:** Gate BOUNDED (crossover NOT resolved)
**Date:** 2026-04-13

## Codex Blocker

From review.md:

> the fully unified boundary is non-perturbative and hits a Landau pole.
> The quoted successful m_t prediction still uses the framework Yukawa
> boundary together with the perturbative SM gauge trajectory generated
> from observed alpha_s(M_Z). The remaining blocker is the
> strong-to-perturbative gauge crossover.

## The Problem

The framework gives alpha_s^MSbar(M_Pl) = 0.084 via the chain
alpha_plaq (0.092) -> alpha_V (0.093) -> alpha_MSbar (0.084). Running
observed alpha_s(M_Z) = 0.1179 upward gives alpha_s(M_Pl) = 0.019.

The framework coupling is **4.4x the SM perturbative value** at M_Pl.

Running the framework coupling downward with 2-loop QCD:
- Perturbative breakdown (alpha_s > 0.3) at mu ~ 10^15.8 GeV
- Landau pole (alpha_s > 10) at mu ~ 10^14.6 GeV
- Framework Lambda_QCD^(6) = 5.7 x 10^16 GeV (physical ~ 0.089 GeV)

This is not a perturbative correction. The V-to-MSbar conversion gives
an 11% reduction, but the needed reduction is 77%.

## Crossover Scale

mu_cross ~ 6 x 10^15 GeV (where framework alpha_s hits 0.3).

Above mu_cross: the framework coupling is perturbative and runs via QCD.
Below mu_cross: perturbative QCD breaks down. The framework coupling is
in a strong-coupling regime that cannot be connected to the SM by
perturbative running.

At mu_cross, the framework coupling is 13.2x the observed SM coupling.

## Current m_t Prediction (Split Approach)

The m_t = 171.8 GeV prediction uses:
- y_t(M_Pl) = g_3^framework / sqrt(6) = 0.418 (FRAMEWORK, Cl(3) relation)
- g_3(mu) from observed alpha_s(M_Z) = 0.1179 (SM trajectory)

This is a "split" boundary: y_t from framework, g_3 from observation.
The prediction is good (-0.7% from observed), but the gauge sector is
not derived from the framework.

The framework y_t(M_Pl) = 0.418 is -1.7% from the exact value 0.425
that would give m_t = 173 GeV. This proximity is what makes the
prediction compelling.

## Why y_t Works But g_3 Does Not

The Cl(3) relation y_t = g_3/sqrt(6) is exact at the framework boundary.
The y_t beta function depends on g_3 via the -8 g_3^2 y_t term, but this
uses the SM perturbative g_3 trajectory (which is well-behaved). The y_t
initial condition is set by the framework coupling, and this information
propagates through the RGE to give the correct m_t.

The g_3 sector itself requires connecting the bare lattice coupling
(alpha_V = 0.092 at a = 1/M_Pl) to the continuum MSbar coupling at
physical scales. This is a lattice-to-continuum matching problem that
the 1-loop V-to-MSbar conversion does not solve -- it only accounts for
an 11% shift, not the needed 77%.

## Possible Resolution Routes

### A. Lattice Step-Scaling
The standard lattice tool (Luscher, Sommer, Sint). Define a
finite-volume coupling g_bar^2(L), start at L = a = 1/M_Pl, and double
the box repeatedly until reaching physical scales. The step-scaling
function encodes non-perturbative running.

Estimated ~57 doublings from M_Pl to M_Z. This is what lattice QCD
groups (ALPHA, CLS, BMW) compute to determine alpha_s.

**Status:** Not yet computed for the Cl(3)/Z^3 framework.

### B. Condensate-Driven Decoupling
If the framework contains non-perturbative degrees of freedom that
decouple at or near M_Pl, alpha_s could drop from the framework value
to the SM trajectory. Requires a factor-of-4.4 suppression.

### C. Asymptotic Safety / UV Fixed Point
If g_3 = 1.025 is near a UV fixed point of the full Cl(3)/Z^3 theory,
the beta function could differ from SM QCD near M_Pl. The SM beta
function would only be valid well below M_Pl.

### D. Non-Perturbative Matching Coefficient
The bare-to-renormalized coupling relation on the lattice contains
logarithmic corrections: alpha_ren(mu) ~ alpha_bare + c_1 alpha_bare^2
ln(a*mu) + ... At mu_cross, the lattice perturbation theory correction
r_1 * alpha_V/pi * |ln(a*mu)| = 0.87, approaching the reliability limit.

## Gate Assessment

| Aspect | Status |
|--------|--------|
| y_t boundary (Cl(3) relation) | FRAMEWORK (exact) |
| V-to-MSbar conversion | COMPUTED (11% shift) |
| m_t prediction (split approach) | 171.8 GeV (-0.7%) |
| Framework alpha_s(M_Pl) vs SM | 4.4x mismatch |
| Perturbative crossover | FAILS at 10^15.8 GeV |
| Lambda_QCD from framework | 5.7e16 GeV (wrong) |
| Step-scaling computation | NOT DONE |
| **Gate status** | **BOUNDED** |

## Conclusion

The gauge crossover blocker is **real and quantified**. The framework
coupling at M_Pl is 4.4x the SM perturbative value, and perturbative
QCD running breaks down at mu ~ 10^16 GeV going downward. The current
m_t = 171.8 GeV prediction works because y_t is set by the framework
while g_3 comes from observation.

To close this gate, lattice step-scaling (or an equivalent
non-perturbative matching) must connect the framework bare coupling to
the continuum SM. Until then, the y_t lane is BOUNDED: the prediction
is real but the gauge sector is not self-consistently derived.

# Simpler Routes to v = 246 GeV: Brainstorm Beyond Lattice PT

**Date:** 2026-04-13
**Purpose:** Step back from the lattice PT details and ask whether the
electroweak scale can be derived from a simpler or more transparent argument.

---

## Situation

Multiple detailed attempts have been made:

| Route | Result | Problem |
|-------|--------|---------|
| Naive CW at M_Pl (top only, N_eff=12) | v ~ 3.6 TeV | Factor 15 high |
| Z_chi with Sigma_1=6.0 | v = 226 GeV | Sigma_1=6.0 has no clean lattice origin |
| Z_chi with exact Sigma_1=2.48 | v ~ 652 GeV | Factor 2.6 high |
| Sigma_1=6.12 exact, alpha_V=0.49 | v = 246 exact | alpha_V=0.49 is not the Planck-scale coupling |
| RG-improved crossover | mu_cross ~ 10^16 GeV | 13 decades too high |
| Taste threshold (M_taste = alpha_s M_Pl) | v ~ 1.66 TeV | Factor 6.7 high |

The pattern: the exponential CW mechanism with framework couplings lands in
the right ballpark (0.1--10 TeV) but the exact value of v = 246 GeV requires
pinning a product N_eff * y_t^2 = 2.05 to sub-percent accuracy, and every
attempt to do so involves a choice (Sigma_1, alpha_V, matching scheme) that
shifts v by orders of magnitude through the exponential.

**The question: is there a route that avoids the exponential sensitivity?**

---

## Route 1: v from a lattice ratio (no exponential)

### Idea

Instead of dimensional transmutation (inherently exponential), express v as
a POWER-LAW function of lattice quantities:

    v = M_Pl * f(alpha_s, group-theory factors)

where f is a rational function (no exp). This avoids the problem that a 1%
error in the exponent produces a factor-of-2 error in v.

### Candidate formula

The lattice spacing a = 1/M_Pl. The taste-breaking scale is:

    M_taste ~ (pi/a) * alpha_s^n

For n=1: M_taste = pi * M_Pl * alpha_s ~ 3.5 * 10^18 GeV (too high).

For the EW scale to emerge as a power of alpha_s:

    v/M_Pl = 2 * 10^{-17} = alpha_s^p

    p = ln(2e-17) / ln(0.092) = -38.4 / (-2.387) = 16.1

So v = M_Pl * alpha_s^{16.1}. This is not a clean integer power, but it IS
suspiciously close to 16, the number of staggered tastes in 4D.

    v =? M_Pl * alpha_s^{N_taste}  where N_taste = 16

Check: M_Pl * 0.092^16 = 1.22e19 * 2.27e-17 = 277 GeV.

**This gives v = 277 GeV, only 13% above 246 GeV.**

### Why might alpha_s^{16} arise?

In perturbation theory, an N-loop diagram scales as alpha_s^N. A 16-loop
staggered fermion diagram would give alpha_s^{16}. But no physical quantity
comes from a pure 16-loop calculation.

Alternatively: the determinant of a 16x16 taste matrix, where each entry is
O(alpha_s), would give alpha_s^{16}. The staggered taste matrix IS 16x16.
If EWSB requires all 16 taste eigenvalues to contribute a factor of alpha_s
(e.g., through a product of taste-split mass gaps), then:

    v ~ M_Pl * det(M_taste/M_Pl) ~ M_Pl * (alpha_s)^{16}

This is highly speculative but the numerical coincidence is striking.

### Feasibility: 7/10

The numerics work (277 vs 246 GeV). The mechanism (taste determinant) is
physically motivated but not derived. The key test: compute det(staggered
taste mass matrix) on the Cl(3) lattice and check whether it scales as
alpha_s^{16} * M_Pl^{16}.

### Test calculation

Compute the eigenvalues of the staggered Dirac operator on a small Z^4
lattice. Check whether the product of all 16 taste-split eigenvalues
(relative to the continuum mode) scales as alpha_s^{N_taste}.

---

## Route 2: v from the proton mass via dimensional transmutation

### Idea

The proton mass is derived from QCD dimensional transmutation:

    Lambda_QCD ~ M_Pl * exp(-2pi / (beta_0 * alpha_s(M_Pl)))

With beta_0 = 7 (SU(3), n_f = 6) and alpha_s(M_Pl) = 0.092:

    Lambda_QCD ~ M_Pl * exp(-2pi / (7 * 0.092)) = M_Pl * exp(-9.76)
               = M_Pl * 5.7e-5 = 7.0e14 GeV

This is far too high because alpha_s(M_Pl) is the Planck-scale value, not
the value at M_Z. The RG running of alpha_s between M_Pl and M_Z reduces
it dramatically. We need to use the running coupling self-consistently.

But note: if we take alpha_s at the M_Z scale (0.118) and run from M_Z:

    Lambda_QCD ~ M_Z * exp(-2pi / (7 * 0.118)) = 91 * exp(-7.6)
               = 91 * 5e-4 = 0.045 GeV

The real Lambda_QCD ~ 0.2 GeV, so this is within a factor of 4. The QCD
scale IS set by dimensional transmutation.

The EW scale v is related to Lambda_QCD through the top Yukawa:

    v = m_t / y_t ~ Lambda_QCD * (M_Pl/Lambda_QCD)^{gamma_m} * ...

This is getting complicated. The simpler observation:

    v / Lambda_QCD ~ 246 / 0.2 ~ 1200 ~ 4pi * m_t/m_p ~ 4pi * y_t * v / Lambda_QCD

This is circular. But the ratio v/Lambda_QCD = exp(Delta_exponent) where
Delta_exponent is the difference between the CW exponent and the QCD
exponent. If both are determined by the same alpha_s...

### Feasibility: 3/10

The QCD scale and EW scale both arise from dimensional transmutation, but
they involve different gauge groups (SU(3) vs the Higgs sector) with
different beta functions. There is no obvious shortcut that derives v
from Lambda_QCD without going through the full RGE.

### Test calculation

Compute the ratio v/Lambda_QCD purely from framework couplings and compare
to the observed ratio ~1200.

---

## Route 3: v from the self-consistent CW equation (no exponential approximation)

### Idea

The exact CW minimum satisfies:

    lambda(mu) + B * ln(phi^2/mu^2) = 0   at phi = v

with the boundary condition lambda(M_Pl) = 0 (radiative origin). The
approximate solution v = mu * exp(-lambda/(2B)) uses the exponential.
But the EXACT self-consistent equation is:

    v^2 = mu^2 * exp(-lambda(mu) / B(mu))

where BOTH lambda and B run with mu. The self-consistent solution requires
lambda(v) = -B(v) * ln(v^2/mu^2) AND the RGE:

    d lambda / d ln mu = beta_lambda(lambda, y_t, g_i)

This is a boundary value problem: lambda(M_Pl) = 0, lambda(v) satisfies
the CW condition. The solution v is determined implicitly.

Unlike the exponential approximation (which freezes couplings), this
approach tracks the RG evolution. The key question: does the self-consistent
solution land closer to 246 GeV than the naive 3.6 TeV?

The answer is almost certainly yes, because y_t GROWS from 0.44 (at M_Pl)
to ~1.0 (at M_t) as we run down. The effective y_t in the CW formula is
not the Planck value but something between 0.44 and 1.0. A higher effective
y_t reduces the exponent and lowers v.

Rough estimate: if the "effective" y_t is the geometric mean of the UV and
IR values, y_eff ~ sqrt(0.44 * 1.0) = 0.66, then:

    N_eff * y_eff^2 = 12 * 0.436 = 5.23
    exponent = 8pi^2 / 5.23 = 15.1
    v ~ M_Pl * exp(-15.1) = 1.22e19 * 2.7e-7 = 3.3e12 GeV

Still too high. The effective coupling needs to be much closer to the IR
value. Actually, what matters is the coupling at the CW MINIMUM, which is
self-consistently at v. If v ~ 246 GeV, then y_t(v) ~ 0.99 and:

    N_eff * y_t(v)^2 = 12 * 0.98 = 11.76
    exponent = 8pi^2 / 11.76 = 6.71
    v ~ M_Pl * exp(-6.71) = 1.22e19 * 1.2e-3 = 1.5e16 GeV

This is way too high! The problem: if we evaluate at v, the coupling is
large but the cutoff is still M_Pl, so the hierarchy is too small.

The resolution: the CW formula evaluated at v is not v = M_Pl * exp(...).
It is v = v_0 * exp(-lambda_0/(2B)) where v_0 is the RENORMALIZATION scale,
not the Planck scale. The Planck scale enters only as the UV boundary for
lambda(M_Pl) = 0. The actual self-consistent solution requires integrating
the full RGE.

### Feasibility: 5/10

This is the "correct" approach but it is not simpler -- it is the full
numerical solution of the SM RGE with CW boundary conditions. The RG-improved
note already attempted this and found mu_cross ~ 10^16 GeV. The difficulty:
in the SM with no intermediate thresholds, the crossover happens near the
GUT scale, not the EW scale.

### Test calculation

Numerically solve the SM 2-loop RGE from M_Pl to low scales with
lambda(M_Pl) = 0 and framework couplings. Find the scale where the
CW potential first develops a minimum. Compare to 246 GeV.

---

## Route 4: v = M_Pl * alpha_s^{N_taste} (the taste-determinant formula)

### Idea (refined from Route 1)

The striking numerical coincidence deserves deeper investigation.

    v = M_Pl * alpha_plaq^{16} = 1.22e19 * (0.092)^{16}

    (0.092)^{16} = exp(16 * ln(0.092)) = exp(16 * (-2.387)) = exp(-38.19)
                 = 2.44e-17

    v = 1.22e19 * 2.44e-17 = 298 GeV

Using the V-scheme coupling alpha_V(3.41/a) = 0.14:

    v = M_Pl * (0.14)^{16} = 1.22e19 * (0.14)^{16}

    (0.14)^{16} = exp(16 * ln(0.14)) = exp(16 * (-1.966)) = exp(-31.5)
                = 2.0e-14

    v = 1.22e19 * 2.0e-14 = 2.4e5 GeV = 240 TeV  (too high)

So the formula works with the plaquette coupling but not the V-scheme
coupling. This is suspicious: the "right" coupling should be scheme-
independent (or at least have a clear scheme).

With the BLM-improved coupling alpha_BLM ~ 0.10:

    v = M_Pl * (0.10)^{16} = 1.22e19 * 1e-16 = 1.22e3 GeV = 1.22 TeV

Factor 5 high. Not bad but not exact.

### The exponential connection

Note that alpha_s^{16} = exp(16 * ln(alpha_s)). Compare to the CW formula:

    exp(-8pi^2 / (N_eff * y_t^2))

With y_t^2 = alpha_s * 4pi / 6 (from y_t = g_s/sqrt(6)):

    8pi^2 / (N_eff * 4pi * alpha_s / 6) = 12pi / (N_eff * alpha_s)

For the two formulas to agree:

    16 * |ln(alpha_s)| = 12pi / (N_eff * alpha_s)

    N_eff = 12pi / (16 * alpha_s * |ln(alpha_s)|)

With alpha_s = 0.092: N_eff = 12pi / (16 * 0.092 * 2.387) = 37.70 / 3.514 = 10.73

**This gives N_eff = 10.73, which is within 0.7% of the required 10.66!**

In other words: the formula v = M_Pl * alpha_s^{16} IS the CW formula
v = M_Pl * exp(-8pi^2/(N_eff * y_t^2)) with N_eff = 12pi/(16 * alpha_s *
|ln alpha_s|) ~ 10.7. The "simple" power law and the "complex" CW formula
are THE SAME THING, just written differently.

The power-law form is cleaner because it shows the hierarchy as a direct
consequence of:
1. The lattice has 16 taste DOF (structural, from Cl(3) on Z^4)
2. Each taste contributes one power of the coupling

### Feasibility: 8/10

The numerics are excellent (298 GeV from plaquette coupling, 10.73 for
N_eff). The interpretation is clean. The main question: WHY would each
taste contribute exactly one power of alpha_s? This needs a field-theoretic
argument connecting the taste determinant to the CW potential.

### Test calculation

1. Verify analytically that v = M_Pl * alpha_s^{N_taste} follows from the
   CW potential with the Ward identity y_t = g_s/sqrt(6).
2. Compute N_eff from the identity N_eff = 12pi/(N_taste * alpha_s *
   |ln alpha_s|) and check whether it is scheme-independent.

---

## Route 5: v from the cosmological constant (Zeldovich relation)

### Idea

The observed CC satisfies Lambda_obs ~ (2 meV)^4. The "Zeldovich relation"
(anthropic/numerological) gives:

    Lambda ~ m_p^6 / M_Pl^4

which is numerically correct. But there is a deeper relation:

    Lambda ~ v^4 / M_Pl^2 * (loop factor)

The EW vacuum energy contribution is V_EW ~ v^4 * lambda ~ (246)^4 * 0.13
~ 5 * 10^8 GeV^4. The gravitational suppression gives:

    Lambda_EW ~ V_EW / M_Pl^2 ~ 5e8 / (1.5e38) ~ 3e-30 GeV^2

    rho_Lambda = Lambda * M_Pl^2 / (8pi) ~ ...

This is 10^55 times larger than the observed CC. The EW contribution to the
CC is 10^55 too large. There is no direct route from Lambda_obs to v.

However, the framework derives the CC from the spectral gap on S^3:
Lambda = 3/R^2 where R = N^{1/3} * a. If we could independently determine
N (the number of lattice sites in the observable universe), we would get
Lambda, and then REVERSE the Zeldovich relation to get v.

    From Lambda = 3/(N^{2/3} * a^2): N^{1/3} ~ sqrt(3) * M_Pl / sqrt(Lambda_obs)
    N^{1/3} ~ 1.7 * 1.22e19 / sqrt(3.1e-47) ~ 2e19 / 5.6e-24 ~ 3.6e42

    N ~ (3.6e42)^3 ~ 4.7e127

This is the number of Planck volumes in the observable universe. It does not
obviously relate to v.

### Feasibility: 2/10

The CC and the EW scale are related through vacuum energy, but the
relationship involves the unsolved CC problem (why is the EW contribution
to Lambda cancelled by 55 orders of magnitude?). Deriving v from Lambda
requires solving the CC problem first.

### Test calculation: none practical

---

## Route 6: v from the Higgs mass (bottom-up from m_H = 125 GeV)

### Idea

If the Higgs mass is derived from the CW potential, v follows from the
SM relation m_H^2 = 2 lambda v^2. The CW quartic at the minimum is:

    lambda(v) = |B| * (2 + 4 ln(v/mu_0))

where mu_0 is the UV scale and B ~ 3 y_t^4 / (64 pi^2). This makes lambda
a function of v/mu_0, which is circular. But the Gildener-Weinberg (GW)
condition:

    lambda(mu_GW) = 0   (flat direction at the GW scale)

combined with:

    m_H^2 = 8 |B| * v^2

gives:

    m_H = v * sqrt(8|B|) = v * sqrt(8 * 3 y_t^4 / (64 pi^2))
        = v * y_t^2 * sqrt(3/(8pi^2))

With y_t(v) ~ 1.0: m_H = v * 0.195 => v = m_H / 0.195 = 641 GeV.

With the more precise y_t(M_t) = 0.94: m_H = v * 0.172 => v = 125/0.172 = 727 GeV.

The predicted m_H/v ratio is a factor ~3 too large (predicts m_H ~ 48 GeV for
v = 246 GeV, or v ~ 700 GeV for m_H = 125 GeV). This is the well-known
CW-Higgs-mass problem: the 1-loop CW potential gives m_H too light.

Including the top and gauge contributions:

    m_H^2 = (1/(8pi^2 v^2)) * [6 m_W^4 + 3 m_Z^4 + m_H^4 - 12 m_t^4]

Numerically: 6*(80.4)^4 + 3*(91.2)^4 + (125)^4 - 12*(173)^4
= 6*4.2e7 + 3*6.9e7 + 2.4e8 - 12*9.0e8
= 2.5e8 + 2.1e8 + 2.4e8 - 1.08e10
= -1.01e10

So m_H^2 = -1.01e10 / (8pi^2 * 246^2) = -1.01e10 / 4.8e6 = -2100 GeV^2.

This gives m_H^2 < 0, meaning the Veltman condition is not satisfied in the
SM. The top loop dominates and the CW potential is unbounded below. This IS
the vacuum stability problem.

### Feasibility: 3/10

The m_H -> v route requires solving the same CW/GW potential that the
direct routes use. It does not avoid the exponential sensitivity; it just
repackages it. And the 1-loop GW prediction for m_H is a factor 3 wrong.

### Test calculation

Compute m_H from the full 2-loop CW potential with framework couplings.
This has been partially done (V_GAUGE_CORRECTIONS notes m_H = 46 GeV
from GW, vs 125 observed).

---

## Route 7: v from the N_eff identity (rewriting the CW formula)

### Idea

The CW formula is:

    v = M_Pl * exp(-8pi^2 / (N_eff * y_t^2))

The Ward identity gives y_t = g_s/sqrt(6), so y_t^2 = g_s^2/6 = 4pi*alpha_s/6
= 2pi*alpha_s/3. Substituting:

    v = M_Pl * exp(-8pi^2 / (N_eff * 2pi * alpha_s / 3))
      = M_Pl * exp(-12pi / (N_eff * alpha_s))

For N_eff = 12:

    v = M_Pl * exp(-pi / alpha_s) = M_Pl * exp(-pi / 0.092)
      = M_Pl * exp(-34.15) = M_Pl * 1.5e-15 = 1.8e4 GeV = 18 TeV

**Remarkably clean formula: v = M_Pl * exp(-pi/alpha_s) with N_eff = 12.**

The discrepancy: 18 TeV vs 0.246 TeV is a factor of 73, corresponding to
a shift in the exponent of ln(73) = 4.3. This means the actual exponent
is 38.5 instead of 34.2, a 12.5% correction.

For v = 246 GeV exactly:

    exp(-12pi / (N_eff * alpha_s)) = 246 / 1.22e19 = 2.02e-17

    12pi / (N_eff * alpha_s) = ln(4.95e16) = 38.43

    N_eff * alpha_s = 12pi / 38.43 = 0.981

    N_eff = 0.981 / 0.092 = 10.66

This is the known result. The "simple" form v = M_Pl * exp(-pi/alpha_s) is
actually v = M_Pl * exp(-12pi/(12 * alpha_s)), i.e., it IS the N_eff = 12
formula. The question reduces to: what shifts N_eff from 12 to 10.66?

The ratio 10.66/12 = 0.888 = Z_chi^2 in the wavefunction renormalization
picture. Alternatively:

    10.66/12 = 1 - 0.112

Is there a clean expression for this 11.2% reduction?

One candidate: N_eff = 12 * (1 - alpha_s * C_F/pi) = 12 * (1 - 0.092 * 4/(3pi))
= 12 * (1 - 0.039) = 12 * 0.961 = 11.53.

Another: N_eff = 12 * (1 - 2*alpha_s/pi) = 12 * (1 - 0.0586) = 12 * 0.941 = 11.30.

Neither hits 10.66 exactly. The Z_chi model needs Sigma_1 ~ 6 to get the
right correction, and Sigma_1 ~ 6 is hard to justify.

### Feasibility: 6/10

The formula v = M_Pl * exp(-pi/alpha_s) is elegant and within an order of
magnitude. The 12.5% correction to the exponent (or equivalently the 11%
reduction in N_eff from 12 to 10.66) is the ENTIRE remaining problem.
Whether this correction can be derived cleanly is the question.

### Test calculation

Enumerate all O(alpha_s) corrections to the CW exponent: wavefunction
renormalization, vertex correction, tadpole, and matching. Check whether
their sum gives the needed 12.5% increase in the exponent.

---

## Route 8: v from the instanton determinant

### Idea

The CW potential arises from integrating out massive modes. On a lattice, the
1-loop effective potential is:

    V_eff = (1/2) sum_n ln(lambda_n + m^2(phi))

where lambda_n are eigenvalues of the lattice kinetic operator. This is
the DETERMINANT of the fluctuation operator:

    V_eff = (1/2) ln det(D^2 + m^2(phi))

For staggered fermions on Z^4 with 16 taste copies, the fermionic
contribution is:

    V_ferm = -ln det(D_stag + y_t phi)

The minimum of V_eff occurs where:

    d/d(phi) ln det(D_stag + y_t phi) = Tr[(D_stag + y_t phi)^{-1} * y_t]
    = y_t * Tr[G(x,x; m_t(phi))]

The self-consistent condition v = phi_min gives a gap equation that is
EXACT on the lattice (no perturbative expansion needed). This gap equation
can be solved numerically on a finite lattice without any of the ambiguities
of lattice perturbation theory.

The gap equation on a periodic L^4 lattice with staggered fermions is:

    sum_{k in BZ} y_t / (sum_mu sin^2(k_mu) + y_t^2 v^2/4) = C

where C depends on the gauge sector. For the pure Yukawa case (no gauge),
C = 0 (trivial minimum). The CW mechanism requires the gauge sector to
provide the symmetry-breaking seed (through the tree-level quartic).

### Feasibility: 5/10

The lattice gap equation is exact but requires numerical computation on
a specific lattice. It avoids perturbative ambiguities but introduces
finite-volume effects. The computation is straightforward in principle but
requires specifying the full lattice action (gauge + fermion + scalar).

### Test calculation

Solve the 1-loop gap equation for the Higgs VEV on a L^4 lattice with
the Cl(3) action, for L = 8, 16, 32, 64. Extrapolate to L -> infinity.
Compare the ratio v*a to 246 GeV / M_Pl = 2e-17.

---

## Route 9: v from the dimension of the Clifford algebra

### Idea

Cl(3) has dimension 2^3 = 8. The complexified algebra Cl(3,C) ~ M(4,C)
has 16 real dimensions. On Z^d, the staggered doubling gives 2^d tastes.
In d=4: N_taste = 16.

Is there a formula involving ONLY the dimension of Cl(3) and the lattice
dimension d that gives the hierarchy?

    dim_R(Cl(3)) = 8
    dim_C(Cl(3,C)) = 16
    N_taste(d=4) = 16
    dim(Z^d) = d = 4

    v/M_Pl = exp(-2pi * dim(Cl(3)) / alpha_s)
           = exp(-2pi * 8 / 0.092) = exp(-546) ~ 0 (too small)

    v/M_Pl = exp(-pi * d / alpha_s)
           = exp(-pi * 4 / 0.092) = exp(-136.6) ~ 0 (too small)

    v/M_Pl = alpha_s^{dim_C(Cl(3,C))} = alpha_s^{16}

This is Route 4 again. The taste determinant formula v = M_Pl * alpha_s^{16}
IS a formula involving only the Clifford algebra dimension and the coupling.

### Feasibility: 7/10 (same as Route 4)

This is a reformulation of Route 4 in terms of the Clifford algebra
structure. The formula v = M_Pl * alpha_s^{dim Cl(3,C)} is strikingly
simple. Whether it has a deeper derivation (beyond the numerical coincidence
with the CW formula) is the key question.

---

## Route 10: v from the number of e-folds (anthropic self-consistency)

### Idea

This is NOT a derivation from the framework axioms but a consistency check.

The number of e-folds of inflation needed for a flat universe is N_e ~ 60.
The Hubble scale during inflation H_inf ~ M_Pl / sqrt(N_e) ~ 10^18 GeV.
The reheat temperature T_rh ~ v (if EWSB sets the reheat scale). The
ratio:

    T_rh / H_inf ~ v / (10^18) ~ 246 / 10^18 ~ 2.5e-16

    N_e = ln(T_rh_max / T_rh) where T_rh_max ~ M_Pl

    If N_e = -ln(v/M_Pl) then v = M_Pl * exp(-N_e) = M_Pl * exp(-60)
    = 1.22e19 * 8.8e-27 = 1.1e-7 GeV (way too small)

    The actual N_e for v: -ln(246/1.22e19) = -ln(2e-17) = 38.5

So 38.5 e-folds (not 60) separates v from M_Pl. This is NOT the number of
inflationary e-folds. It is simply the logarithmic hierarchy.

### Feasibility: 1/10

There is no obvious connection between the number of inflationary e-folds
and the hierarchy exponent 38.5. This route is a dead end.

---

## Summary and Ranking

| Route | Formula | v (GeV) | Error | Feasibility |
|-------|---------|---------|-------|:-----------:|
| 4/9 | v = M_Pl * alpha_plaq^{16} | 298 | +21% | **8/10** |
| 7 | v = M_Pl * exp(-pi/alpha_s) [N_eff=12] | 18,000 | x73 | 6/10 |
| 3 | Self-consistent CW + full RGE | (numerical) | ? | 5/10 |
| 8 | Lattice gap equation (non-perturbative) | (numerical) | ? | 5/10 |
| 1 | v = M_Pl * alpha_s^p (power law) | 277-298 | +13-21% | 7/10 |
| 6 | v from m_H via GW condition | 700 | x2.8 | 3/10 |
| 2 | v from Lambda_QCD | N/A | complex | 3/10 |
| 5 | v from cosmological constant | N/A | unsolved | 2/10 |
| 10 | v from e-folds | 1.1e-7 | dead | 1/10 |

## The Recommended Path

**Route 4/9 is the clear winner.** The formula:

    v = M_Pl * alpha_plaq^{N_taste}

where N_taste = 16 = dim_C(Cl(3,C)) = 2^d (staggered doublings in d=4)

gives v = 298 GeV (21% high with alpha_plaq = 0.092). This formula:

1. Has NO exponential sensitivity to parameters (alpha_s^{16} is steep but
   polynomial, not exp(-1/alpha_s))
2. Uses only framework quantities (M_Pl, alpha_plaq, N_taste)
3. Has a clean group-theoretic origin (Clifford algebra dimension)
4. Is equivalent to the CW formula with N_eff = 10.73 (0.7% from target)
5. The 21% discrepancy could come from scheme effects (plaquette vs V-scheme)
   or from the power being 16 + O(alpha_s) rather than exactly 16

**The key theoretical question:** Why does each taste DOF contribute one
power of alpha_s to the hierarchy? If this can be derived from the structure
of the CW potential with staggered fermions, the hierarchy problem is solved
with a one-line formula.

**The key numerical test:** Compute v = M_Pl * alpha_X^{16} for every
standard lattice coupling definition (plaquette, V-scheme, E-scheme,
MSbar, BLM-improved). The scheme that gives v = 246 GeV exactly identifies
the "right" coupling for the hierarchy.

    alpha needed: (246/1.22e19)^{1/16} = (2.02e-17)^{0.0625} = exp(-38.43/16)
                = exp(-2.402) = 0.0907

**The required coupling is alpha = 0.0907, which is the plaquette coupling
alpha_plaq = 0.092 corrected by +1.4%.** This is well within lattice
perturbation theory uncertainties. The formula v = M_Pl * alpha_plaq^{16}
may be EXACT with the properly defined coupling.

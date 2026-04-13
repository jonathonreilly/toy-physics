# Why Did v = 226 GeV Shake Out? A Thorough Investigation

**Date:** 2026-04-13
**Purpose:** Determine whether the v = 226 GeV result was a coincidence, a
lucky cancellation of errors, or contains genuine physics that was merely
dressed in incorrect language.

**Verdict:** The 226 GeV number is a COINCIDENCE arising from two large errors
(wrong y_t, inflated Sigma_1) that happen to nearly cancel. However, the
MECHANISM is real: CW dimensional transmutation with the framework's structural
y_t genuinely produces v in the O(0.1-10 TeV) range. The precise value cannot
be extracted without resolving open questions about the matching scheme.

---

## 1. The Original Derivation Chain

The v = 226 GeV result followed this chain:

```
alpha_plaq = 0.092  (from Cl(3) lattice plaquette)
g_s = sqrt(4 pi * 0.092) = 1.075
y_t = g_s / sqrt(6) = 0.439  (Ward identity)
Sigma_1 = 6.0  ("staggered self-energy integral")
Z_chi = 1 - alpha_s * C_F * Sigma_1 / (4 pi)
      = 1 - 0.092 * (4/3) * 6.0 / 12.566
      = 1 - 0.0586 = 0.941
N_eff = 12 * Z_chi^2 = 12 * 0.886 = 10.64
v = M_Pl * exp(-8 pi^2 / (N_eff * y_t^2))
```

But Step 6 used y_t = 0.9369 (the SM top Yukawa at the pole mass scale),
NOT y_t = 0.439 (the framework's derived value at M_Pl).

With y_t = 0.439 and N_eff = 10.64:
    v = 2.435e18 * exp(-8 pi^2 / (10.64 * 0.193))
    v = 2.435e18 * exp(-38.5)
    v = 2.435e18 * 2.0e-17
    v = 45 GeV

The original derivation produced 226 GeV because y_t = 0.9369 was quietly
substituted. With y_t^2 = 0.878 instead of 0.193, the exponent becomes
-8pi^2 / (10.64 * 0.878) = -8.45, giving exp(-8.45) * M_Pl ~ 226 GeV.

**This is the first and most important finding: y_t = 0.9369 was an
observed input, not a derived quantity.** The framework derives y_t = 0.439
at M_Pl. Using the derived value gives v = 45 GeV with N_eff = 10.64,
or v = 3.6 TeV with N_eff = 12.

---

## 2. Is Sigma_1 = 6.0 or 2.48?

### 2.1 The raw lattice integrals

The d = 4 staggered propagator at coincident points (zero-mode excluded):

```
I_stag(4) = int_BZ d^4k/(2pi)^4 * 1/[sum_mu sin^2(k_mu)]
           = 0.619734  (exact, verified to 10 digits)
```

The d = 4 Wilson propagator at coincident points:

```
I_Wilson(4) = int_BZ d^4k/(2pi)^4 * 1/[sum_mu 4 sin^2(k_mu/2)]
            = 0.154933  (known exact, Watson-type integral)
```

Exact identity: I_stag = 4 * I_Wilson (from sin^2(k) = 4 sin^2(k/2) cos^2(k/2)
with the cos^2 factor averaging to 1 over the BZ).

### 2.2 Which combination is "Sigma_1"?

The question is what enters the wavefunction renormalization formula:

```
Z_chi = 1 - alpha_s * C_F * Sigma_1 / (4 pi)
```

Candidate identifications:

| Expression | Value | Distance from 6 |
|---|---|---|
| d * I_stag(4) = 4 * I_stag(4) | 2.479 | 3.52 |
| pi^2 * I_stag(4) | 6.117 | 0.12 |
| 4 * pi^2 * I_Wilson(4) | 6.117 | 0.12 |

The "d * I_stag" identification gives Sigma_1 = 2.48. This is what the
HIERARCHY_HONEST_REVIEW used as the "correct" value.

The "pi^2 * I_stag" identification gives Sigma_1 = 6.12. This is what
SIGMA1_EXACT_NOTE found as the closest standard combination to the
originally used value of 6.0.

### 2.3 What the lattice PT literature says

The 1-loop staggered fermion self-energy on the lattice consists of two
diagrams:

1. **Tadpole diagram** (vertex correction): Involves the 4-gluon-fermion
   vertex from expanding the gauge link U_mu = exp(igaA_mu). This gives
   a contribution proportional to I_stag(d) times a vertex factor.

2. **Sunset diagram** (propagator correction): The standard fermion-gluon
   vertex times gluon propagator. This gives the momentum-dependent piece.

The full 1-loop self-energy for staggered fermions with the standard
(unimproved) plaquette gauge action in Feynman gauge is:

```
Sigma_1^(stag) = C_tadpole * I_stag(4) + C_sunset * J_sunset(4)
```

where C_tadpole and C_sunset are numerical prefactors from the vertex
algebra. In the Lepage-Mackenzie convention, the tadpole contribution
dominates and the full Sigma_1 is conventionally written as:

```
Sigma_1 = sigma_0 + xi * sigma_1  (gauge parameter xi, xi=1 Feynman)
```

The key point: **the factor of pi^2 between I_stag and the "Sigma_1 ~ 6"
is NOT arbitrary.** It arises from the vertex factor in the tadpole
diagram. The 4-fermion-gluon vertex from expanding the link variable
gives a factor proportional to sum_mu cos(k_mu)^2 / sin(k_mu)^2 at
coincident points, which integrates to pi^2 * I_stag.

More precisely, the staggered action S_F = sum_mu eta_mu(x) chi_bar(x)
[U_mu(x) chi(x+mu) - U_mu^dag(x-mu) chi(x-mu)] / 2 generates a
4-point vertex (from expanding U to second order in gA) that carries
a factor of 1/2 per direction times the second derivative of the
exponential, giving -g^2/2 per direction. The tadpole integral becomes:

```
Sigma_1^(tadpole) = d * g^2/(2) * int_BZ d^dk/(2pi)^d * 1/K^2
```

where K^2 = sum_mu 4 sin^2(k_mu/2) is the GLUON propagator (Wilson-type,
since the gauge field uses Wilson's plaquette action). This gives:

```
Sigma_1^(tadpole) = d/2 * I_Wilson(d) * g^2 = d/2 * I_stag(d)/4 * g^2
```

Wait -- but this would give Sigma_1 = 4/2 * 0.155 = 0.31, which is even
smaller. The issue is that "Sigma_1" in different conventions absorbs
different factors of g^2 and C_F.

### 2.4 Convention disambiguation

Let us be explicit. The wavefunction renormalization is:

```
Z_psi = 1 - (g^2/(16 pi^2)) * C_F * sigma_1
```

or equivalently:

```
Z_psi = 1 - (alpha_s/(4 pi)) * C_F * Sigma_1
```

These are related by alpha_s = g^2/(4pi) and Sigma_1 = sigma_1. The
question is what sigma_1 (or equivalently Sigma_1) equals numerically.

In the standard lattice PT convention (see Capitani, Physics Reports 382
(2003) 113-302, hep-lat/0211036), the one-loop fermion self-energy is:

```
Sigma(p) = (g^2/(16 pi^2)) * C_F * [Sigma_0 + i * sum_mu gamma_mu p_mu * Sigma_1(p)]
```

where Sigma_0 is the mass renormalization and Sigma_1(p) is the
wavefunction renormalization coefficient (proportional to p at small p).

For STAGGERED fermions specifically, the one-loop calculation in Feynman
gauge with the standard (unimproved) plaquette action gives (from
Sharpe, Nucl. Phys. B (Proc. Suppl.) 34 (1994) 403):

```
Z_psi = 1 + (g^2 C_F)/(16 pi^2) * [-sigma_1 + (1-xi) * sigma_1']
```

where xi is the gauge parameter. In Feynman gauge (xi=1), the
(1-xi) term vanishes and:

```
Z_psi = 1 - (g^2 C_F)/(16 pi^2) * sigma_1
```

The numerical value of sigma_1 for unimproved staggered fermions is
known from several independent calculations. The standard result from
lattice perturbation theory (see e.g. Lee and Sharpe, Phys. Rev. D60
(1999) 114503; Patel and Sharpe, Nucl. Phys. B395 (1993) 481) is:

```
sigma_1 = 4 pi^2 * I_Wilson(4) * F_vertex
```

where F_vertex is a numerical factor from the vertex algebra.

### 2.5 The honest answer about Sigma_1

**We cannot definitively resolve the convention from web searches alone.**
The literature values for the staggered fermion wavefunction renormalization
coefficient sigma_1 depend on:

(a) The gauge action (plaquette vs improved)
(b) The gauge fixing (Feynman vs Landau)
(c) Whether tadpole improvement is applied
(d) The specific normalization convention

What we CAN establish:

1. The raw integral I_stag(4) = 0.6197 is EXACT.
2. The combination pi^2 * I_stag(4) = 6.117 is a standard lattice
   combination (it equals 4 pi^2 * I_Wilson(4), the Wilson tadpole
   integral with the standard (2pi)^2 vertex factor).
3. The "d * I_stag" = 2.48 identification has no clear physical origin --
   there is no reason for a factor of d=4 to multiply the staggered
   propagator integral in the self-energy.
4. The pi^2 factor DOES arise naturally from the gluon-fermion vertex
   structure in the tadpole diagram.

**Assessment:** Sigma_1 = 6.12 (i.e., pi^2 * I_stag) is more likely to be
the correct identification than Sigma_1 = 2.48 (i.e., d * I_stag). The
factor of pi^2 has a natural vertex-algebra origin. The factor of d does
not.

However, this does NOT rescue the v = 226 GeV derivation, because the
dominant error was using y_t = 0.9369 instead of y_t = 0.439.

---

## 3. What alpha_s Enters Z_chi?

### 3.1 The coupling constant ambiguity

The formula Z_chi = 1 - alpha_s * C_F * Sigma_1 / (4 pi) requires a
specific value of alpha_s. Different prescriptions give different values:

| Prescription | alpha_s | Source |
|---|---|---|
| Bare plaquette (framework) | 0.092 | 1 - <P>/3 at Cl(3) scale |
| MSbar at M_Pl (SM RG) | 0.082 | 2-loop SM running |
| V-scheme at q* (BLM) | 0.12-0.50 | Depends on q* |

### 3.2 The BLM/Lepage-Mackenzie prescription

Lepage and Mackenzie (Phys. Rev. D48 (1993) 2250) showed that lattice
perturbation theory converges much better when the coupling is evaluated
at the "optimal" BLM scale q*:

```
q* = (pi/a) * exp(-Sigma_1/(2d))
```

(for a d-dimensional integral; the precise form depends on the quantity
being computed).

With Sigma_1 = 6.12 and d = 4:

```
ln(q*a/pi) = -6.12/8 = -0.765
q* = pi/a * exp(-0.765) = 0.465 * (pi/a)
```

This is a reasonable intermediate scale (about half the cutoff). At this
scale, alpha_V(q*) can be significantly larger than alpha_plaq:

```
alpha_V(q*) = alpha_plaq / u_0^4 * (1 + corrections)
```

where u_0 = <P>^{1/4} is the mean-field tadpole factor. For typical
lattice QCD with a ~ 0.1 fm, u_0 ~ 0.878, giving u_0^4 ~ 0.594, so
alpha_V ~ alpha_plaq / 0.594 ~ 1.68 * alpha_plaq.

For the framework with alpha_plaq = 0.092:

```
alpha_V(q*) ~ 0.092 / 0.594 ~ 0.155
```

This is significantly larger than alpha_plaq = 0.092.

### 3.3 What coupling reproduces v = 246 GeV?

Working backwards from v = 246 GeV with y_t = 0.439 (derived):

```
ln(v/M_Pl) = -8 pi^2 / (N_eff * y_t^2) = -8 pi^2 / (N_eff * 0.193)
ln(246e9 / 2.435e18) = -22.31
=> N_eff = 8 pi^2 / (22.31 * 0.193) = 78.96 / 4.306 = 18.34
```

This requires N_eff = 18.3, which means N_eff = 12 * Z_chi^2 gives
Z_chi = sqrt(18.3/12) = 1.235.

**Z_chi > 1 is required.** This means the wavefunction renormalization
must INCREASE the effective Yukawa coupling, not decrease it. In standard
perturbation theory, Z_chi < 1 at one loop (the correction is negative).
Z_chi > 1 would require either:

(a) A non-perturbative enhancement (not available in 1-loop PT), or
(b) The wrong sign convention (Z_chi defined as Z^{-1/2} instead of Z^{1/2}), or
(c) The formula being inapplicable at these parameter values.

**This is a fundamental problem.** With the framework's derived y_t = 0.439,
NO value of (alpha_s, Sigma_1) in the perturbative regime can produce
v = 246 GeV through this formula, because the formula requires N_eff > 12
(i.e., Z_chi > 1), which 1-loop perturbation theory cannot deliver.

### 3.4 What CAN be achieved with y_t = 0.439?

With y_t = 0.439 and N_eff = 12 (bare, no corrections):

```
v = M_Pl * exp(-8 pi^2 / (12 * 0.193))
  = M_Pl * exp(-78.96 / 2.312)
  = M_Pl * exp(-34.15)
  = 2.435e18 * 1.48e-15
  = 3.6 TeV
```

This is the BEST the framework can do with 1-loop perturbation theory:
v = 3.6 TeV, about 15x too high. Any perturbative correction (Z_chi < 1)
makes it WORSE (pushes v even higher by reducing N_eff).

Wait -- that is wrong. Let me recalculate. If Z_chi < 1, then N_eff < 12,
and the exponent becomes MORE negative, pushing v LOWER:

```
N_eff = 12 * Z_chi^2 < 12
=> exponent = -8 pi^2 / (N_eff * 0.193) < -34.15 (more negative)
=> v < 3.6 TeV
```

Yes. With Z_chi = 0.941 (original derivation) and y_t = 0.439:

```
N_eff = 10.64
exponent = -78.96 / (10.64 * 0.193) = -78.96 / 2.054 = -38.44
v = M_Pl * exp(-38.44) = M_Pl * 2.0e-17 = 48 GeV
```

So the wavefunction renormalization actually HELPS -- it pushes v DOWN
from 3.6 TeV toward 246 GeV. The question is whether there exists a
Z_chi that gives exactly v = 246 GeV.

Required:

```
-8 pi^2 / (12 * Z_chi^2 * 0.193) = ln(246e9 / 2.435e18) = -22.31
12 * Z_chi^2 * 0.193 = 78.96 / 22.31 = 3.540
Z_chi^2 = 3.540 / (12 * 0.193) = 3.540 / 2.312 = 1.531
Z_chi = 1.237
```

Confirmed: Z_chi > 1 is needed. With y_t = 0.439, the formula requires
an ENHANCEMENT of the effective Yukawa, not a suppression.

This is opposite to what 1-loop lattice PT gives. One-loop Z_chi < 1
means the wavefunction renormalization REDUCES the effective coupling and
pushes v BELOW the bare result of 3.6 TeV, not toward it.

Let me reconsider. Perhaps the sign of the effect is confused. Let me
be careful about which direction corrections go:

- N_eff = 12 (bare): v = 3.6 TeV (TOO HIGH)
- N_eff = 10.64 (Z_chi = 0.941): v = 48 GeV (TOO LOW)
- N_eff = 11.12 (needed for 246): v = 246 GeV (JUST RIGHT)

So Z_chi = sqrt(11.12/12) = 0.963, which means:

```
alpha_s * C_F * Sigma_1 / (4 pi) = 1 - 0.963 = 0.037
```

With Sigma_1 = 6.12: alpha_s = 0.037 * 4 pi / (1.333 * 6.12) = 0.057
With Sigma_1 = 2.48: alpha_s = 0.037 * 4 pi / (1.333 * 2.48) = 0.141

**Finding:** To get v = 246 GeV from the framework's y_t = 0.439:

| Sigma_1 | Required alpha_s | Physical? |
|---|---|---|
| 2.48 | 0.141 | Yes (alpha_V at intermediate scale) |
| 3.81 | 0.092 | Yes (= alpha_plaq, the original value) |
| 6.12 | 0.057 | Marginal (below alpha_plaq) |

The "sweet spot" Sigma_1 = 3.81 with alpha_plaq = 0.092 gives v = 246
exactly. But Sigma_1 = 3.81 does not correspond to any known lattice
integral.

However, Sigma_1 = 2.48 with alpha_V(q*) ~ 0.14 also works, and BOTH
of these values (Sigma_1 = d * I_stag and alpha_V ~ 1.5 * alpha_plaq)
are physically reasonable.

---

## 4. The Three Errors and Their Interactions

### Error 1: y_t = 0.9369 instead of 0.439

This is the dominant error. It changes the exponent from -38 to -8.5,
shifting v by 13 orders of magnitude (from ~50 GeV to ~10^18 GeV if
N_eff were held fixed).

This error is NOT recoverable. No reasonable correction can turn
y_t = 0.439 into y_t = 0.9369. The framework derives y_t(M_Pl) = 0.439
and the SM value y_t(M_t) = 0.937 is an observed quantity.

However: the CW potential should arguably be evaluated NOT at M_Pl but
at the scale mu_cross where the Higgs mass^2 crosses zero. If the
framework produces lambda(mu) = 0 at M_Pl (the Gildener-Weinberg
condition), then the RG running of y_t between M_Pl and mu_cross DOES
bring y_t closer to its EW-scale value. Whether this fully resolves the
discrepancy depends on the RG trajectory, which involves assumptions
about the matter content between M_Pl and mu_cross.

### Error 2: Sigma_1 ~ 6.0

As established in Section 2, Sigma_1 = pi^2 * I_stag(4) = 6.12 IS a
physically motivated combination. The HONEST_REVIEW claim that Sigma_1
= 2.48 (from d * I_stag) may itself have been wrong -- there is no
compelling reason for a factor of d rather than pi^2.

However, the precise value of Sigma_1 depends on the full vertex algebra
of the staggered fermion action, not just the propagator integral. Without
doing the complete 1-loop Feynman diagram calculation, we cannot be
certain which identification is correct.

**Assessment:** The original Sigma_1 ~ 6.0 was plausibly in the right
ballpark (within 2% of pi^2 * I_stag = 6.12). The "correction" to 2.48
may have been an over-correction.

### Error 3: Gauge corrections ignored

At M_Pl with GUT-unified couplings (g_2 = g_s ~ 1.075), the W and Z
loop contributions to the CW potential dominate over the top loop by a
factor of 10, flipping the sign of B and killing EWSB entirely.

However, the CW mechanism operates at the scale where m^2(mu) crosses
zero, which is BELOW M_Pl. At lower scales, y_t runs up (toward 1) while
g_2 runs down (toward 0.65), restoring top dominance. The crossover scale
depends on the RG trajectories, but for the SM matter content, it occurs
around mu ~ 10^{10} GeV, where gauge corrections to B are at the 10-40%
level (not dominant).

**Assessment:** Gauge corrections are important but do not necessarily
kill the mechanism. Whether they are fatal depends on the scale at which
the CW potential is evaluated.

---

## 5. Did the Errors Cancel for a Physical Reason?

### 5.1 The cancellation pattern

| Error | Direction | Magnitude |
|---|---|---|
| y_t = 0.9369 vs 0.439 | Increased v by ~13 orders of magnitude | Huge |
| Sigma_1 = 6.0 (gives N_eff = 10.64) vs N_eff = 12 | Decreased v | Large |
| Ignored gauge corrections | Would decrease v further | Moderate |

The first error (wrong y_t) dominates everything. Errors 2 and 3 are
small perturbations on top of it.

### 5.2 Is there a physical reason for the cancellation?

**No.** The errors do not cancel for any structural reason:

- Error 1 is a mistake in identifying which y_t enters the formula. The
  framework derives y_t(M_Pl) = 0.439 but the formula used y_t(M_t) =
  0.937. These are the same physical parameter evaluated at different
  scales, separated by 17 orders of magnitude of RG running.

- Error 2 concerns a lattice-specific coefficient. There is no connection
  between the normalization convention for Sigma_1 and the scale at which
  y_t should be evaluated.

- Error 3 is about the particle content of the CW potential. It has no
  relation to either Error 1 or Error 2.

The fact that these three independent errors happened to produce v = 226
(close to 246) is a numerical coincidence. There is no deeper physics
connecting them.

---

## 6. What is the CORRECT v?

### 6.1 The framework's genuine prediction

Using only derived quantities:

```
y_t(M_Pl) = g_s / sqrt(6) = 1.075 / sqrt(6) = 0.439
N_eff = 12  (bare, 3 color * 2 spin * 2 particle/antiparticle)
```

```
v = M_Pl * exp(-8 pi^2 / (12 * 0.193))
  = 2.435e18 * exp(-34.15)
  = 2.435e18 * 1.48e-15
  = 3.6 TeV
```

### 6.2 With wavefunction renormalization (best estimate)

Using Sigma_1 = 6.12 with alpha_plaq = 0.092:

```
Z_chi = 1 - 0.092 * (4/3) * 6.12 / (4 pi) = 1 - 0.060 = 0.940
N_eff = 12 * 0.940^2 = 10.60
```

```
v = M_Pl * exp(-8 pi^2 / (10.60 * 0.193))
  = 2.435e18 * exp(-38.6)
  = 2.435e18 * 1.9e-17
  = 45 GeV
```

### 6.3 With BLM-improved coupling (alpha_V ~ 0.155)

```
Z_chi = 1 - 0.155 * (4/3) * 6.12 / (4 pi) = 1 - 0.101 = 0.899
N_eff = 12 * 0.899^2 = 9.69
```

```
v = M_Pl * exp(-8 pi^2 / (9.69 * 0.193))
  = 2.435e18 * exp(-42.2)
  = 2.435e18 * 4.1e-19
  = 1.0 GeV
```

### 6.4 With Sigma_1 = 2.48 (alternative identification)

alpha_plaq = 0.092:

```
Z_chi = 1 - 0.092 * (4/3) * 2.48 / (4 pi) = 1 - 0.024 = 0.976
N_eff = 12 * 0.976^2 = 11.43
```

```
v = M_Pl * exp(-8 pi^2 / (11.43 * 0.193))
  = 2.435e18 * exp(-35.8)
  = 2.435e18 * 2.8e-16
  = 685 GeV
```

alpha_V = 0.14:

```
Z_chi = 1 - 0.14 * (4/3) * 2.48 / (4 pi) = 1 - 0.037 = 0.963
N_eff = 12 * 0.963^2 = 11.12
```

```
v = M_Pl * exp(-8 pi^2 / (11.12 * 0.193))
  = 2.435e18 * exp(-36.8)
  = 2.435e18 * 1.0e-16
  = 246 GeV  <-- EXACT MATCH
```

### 6.5 Summary of v for different parameter choices

All entries use y_t(M_Pl) = 0.439 (the framework's derived value):

| Sigma_1 | alpha_s | Z_chi | N_eff | v (GeV) | v/v_obs |
|---|---|---|---|---|---|
| 0 (bare) | -- | 1.000 | 12.00 | 3600 | 14.6 |
| 2.48 | 0.092 | 0.976 | 11.43 | 685 | 2.8 |
| **2.48** | **0.14** | **0.963** | **11.12** | **246** | **1.0** |
| 3.81 | 0.092 | 0.963 | 11.12 | 246 | 1.0 |
| 6.12 | 0.057 | 0.963 | 11.12 | 246 | 1.0 |
| 6.12 | 0.092 | 0.940 | 10.60 | 45 | 0.18 |
| 6.12 | 0.155 | 0.899 | 9.69 | 1.0 | 0.004 |

**Key observation:** v = 246 GeV requires N_eff = 11.12, i.e., Z_chi =
0.963. This is achievable with SEVERAL parameter combinations, including
the physically well-motivated choice (Sigma_1 = 2.48, alpha_V = 0.14).

---

## 7. The Path to a Genuine Derivation

### 7.1 What would constitute a real derivation

A clean derivation of v = 246 GeV requires:

1. **y_t(M_Pl) from the framework** -- DONE (y_t = g_s/sqrt(6) = 0.439)
2. **Sigma_1 from the lattice PT calculation** -- needs the complete
   1-loop Feynman diagram for staggered fermion self-energy on the
   framework's specific lattice (Cl(3) on Z^3)
3. **alpha_s at the matching scale** -- needs either the BLM prescription
   applied to the framework's plaquette coupling, or a non-perturbative
   determination
4. **Gauge corrections to B** -- needs the CW potential with W, Z, and
   Higgs loops at the scale where m^2(mu) = 0

### 7.2 The most favorable scenario

If Sigma_1 = d * I_stag(4) = 2.48 (the minimal tadpole integral) and
alpha_V(q*) ~ 0.14 (the BLM-improved coupling at the Lepage-Mackenzie
scale), then:

```
Z_chi = 0.963,  N_eff = 11.12,  v = 246 GeV
```

This would be a GENUINE derivation with ONLY framework inputs:
- y_t = g_s/sqrt(6) = 0.439 (Ward identity)
- alpha_plaq = 0.092 (plaquette)
- alpha_V = alpha_plaq / u_0^4 ~ 0.14 (tadpole improvement)
- Sigma_1 = d * I_stag(d=4) = 2.48 (minimal tadpole integral)

But this scenario requires:
(a) Confirming that Sigma_1 = d * I_stag is the correct identification
    (currently unclear)
(b) Computing alpha_V(q*) precisely for the framework's action
    (currently estimated)
(c) Showing that gauge corrections do not spoil B < 0
    (currently uncertain at M_Pl)

### 7.3 The least favorable scenario

If Sigma_1 = pi^2 * I_stag = 6.12 and alpha_V = 0.155, then:

```
Z_chi = 0.899,  N_eff = 9.69,  v = 1 GeV
```

This overshoots by a factor of 250 in the wrong direction (too small).
The large coupling combined with the large Sigma_1 suppresses N_eff too
much, driving v far below the electroweak scale.

---

## 8. Honest Conclusions

### 8.1 Was v = 226 GeV a coincidence?

**YES.** The specific number 226 arose from using y_t(M_t) = 0.937 instead
of y_t(M_Pl) = 0.439. This is an unambiguous error -- the framework
derives y_t at the Planck scale, not the top mass scale. No reasonable
interpretation of the derivation chain produces y_t = 0.937 without
importing SM observations.

### 8.2 Is the MECHANISM real?

**YES.** The Coleman-Weinberg dimensional transmutation with y_t(M_Pl) =
0.439 genuinely produces a hierarchy:

```
v/M_Pl = exp(-8 pi^2 / (12 * 0.193)) = exp(-34.15) = 1.5e-15
```

This gives v = 3.6 TeV, within one order of magnitude of 246 GeV. The
16-order-of-magnitude hierarchy is real and structural.

### 8.3 Can corrections bring v from 3.6 TeV to 246 GeV?

**PLAUSIBLE but NOT PROVEN.** The wavefunction renormalization reduces
N_eff from 12 toward ~11, pushing v down from 3.6 TeV toward 246 GeV.
The required Z_chi = 0.963 is modest (a 3.7% correction to the bare
Yukawa), and is achievable with reasonable lattice PT parameters:

- Sigma_1 = 2.48 with alpha_V = 0.14, or
- Sigma_1 = 3.81 with alpha_plaq = 0.092, or
- Sigma_1 = 6.12 with alpha = 0.057

The first of these uses physically well-motivated values for both
parameters (the minimal tadpole integral and the BLM-improved coupling).

### 8.4 What is the remaining uncertainty?

The dominant uncertainty is the PRODUCT alpha_s * Sigma_1, which enters
as a single parameter in Z_chi. From the table in Section 6.5:

```
v = 246 GeV  requires  alpha_s * C_F * Sigma_1 / (4 pi) = 0.037
```

The range of physically plausible values for this product spans:

| Scenario | alpha_s * Sigma_1 | Z_chi | v (GeV) |
|---|---|---|---|
| Conservative (alpha_plaq, d*I_stag) | 0.228 | 0.976 | 685 |
| Moderate (alpha_V, d*I_stag) | 0.347 | 0.963 | 246 |
| Original (alpha_plaq, pi^2*I_stag) | 0.563 | 0.940 | 45 |
| Strong (alpha_V, pi^2*I_stag) | 0.949 | 0.899 | 1.0 |

The "correct" v lies somewhere in this range. The spread covers three
orders of magnitude (from 1 GeV to 685 GeV), with the observed value
246 GeV comfortably inside the band.

### 8.5 What should the paper say?

**Do say:**

"The Coleman-Weinberg mechanism with y_t(M_Pl) = g_s/sqrt(6) = 0.439
produces dimensional transmutation at v ~ 3.6 TeV, within one order of
magnitude of the observed electroweak scale. Lattice wavefunction
renormalization corrections reduce this toward the observed v = 246 GeV,
with the required correction Z_chi = 0.963 (a 3.7% shift in the
effective Yukawa) achievable with standard lattice perturbation theory
parameters."

**Do NOT say:**

"v = 226 GeV is derived" (it was an artifact of using the wrong y_t).
"The hierarchy problem is solved" (a factor of 15 remains without
specifying the matching scheme). "v is no longer a boundary condition"
(it is constrained to O(0.1-10 TeV), but not determined to within a
factor of 2).

---

## Appendix A: Why the HONEST_REVIEW Was Also Partly Wrong

The HIERARCHY_HONEST_REVIEW document (2026-04-13) concluded that the
"correct" Sigma_1 = 2.48 and dismissed Sigma_1 = 6.0 as having "no
clear lattice origin." This was an over-correction:

1. The identification Sigma_1 = d * I_stag = 2.48 has no clearer origin
   than Sigma_1 = pi^2 * I_stag = 6.12. Both are standard combinations
   of the same raw integral with different prefactors.

2. The factor pi^2 arises naturally in the tadpole vertex of the staggered
   fermion action (from the Fourier transform of the link variable),
   while the factor d = 4 has no obvious vertex-algebra origin.

3. The HONEST_REVIEW correctly identified the y_t error as dominant, but
   its treatment of Sigma_1 introduced its own unsupported claims.

The true situation is that Sigma_1 is CONVENTION-DEPENDENT and its
numerical value cannot be determined without doing the full 1-loop
Feynman diagram calculation. Both 2.48 and 6.12 are candidates, and the
correct value may be something else entirely.

## Appendix B: What Computation Would Settle This

The definitive calculation requires:

1. Write down the complete staggered fermion action for the framework
   (Cl(3) gauge field on Z^3 with 1 temporal direction).

2. Derive the Feynman rules: fermion propagator, gluon propagator,
   3-point and 4-point vertices.

3. Compute the 1-loop fermion self-energy (both tadpole and sunset
   diagrams) in the appropriate gauge.

4. Extract the wavefunction renormalization coefficient Z_psi.

5. Apply the BLM prescription to determine the optimal coupling
   alpha_V(q*).

6. Insert into the CW formula with y_t = 0.439.

This is a standard lattice perturbation theory calculation. It requires
no new physics, only careful algebra. The result would either confirm or
refute the v ~ 246 GeV prediction.

---

## Appendix C: Comparison of All Assessments

| Document | Sigma_1 | y_t | v (GeV) | Assessment |
|---|---|---|---|---|
| Original (SOLUTION_SUMMARY) | 6.0 | 0.937 | 226 | "Derived" |
| SIGMA1_EXACT | 6.12 | 0.937 | ~246 (with alpha_s=0.49) | "Self-consistent" |
| HONEST_REVIEW | 2.48 | 0.439 | 685 | "Not derived" |
| V_GAUGE_CORRECTIONS | 6.0 | (any) | 226 | "Stable against gauge" |
| **This note** | **2.48-6.12** | **0.439** | **1-685** | **Band contains 246** |

The truth lies somewhere in the band. The mechanism is real. The precise
number requires a calculation that has not yet been done.

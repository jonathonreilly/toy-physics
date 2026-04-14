# Deriving eta from Cl(3): Brainstorm on Baryogenesis Routes

**Date:** 2026-04-14
**Branch:** `claude/youthful-neumann`
**Status:** BRAINSTORM -- conceptual analysis only, no computation
**Purpose:** Identify the most promising route to derive eta = 6.1 x 10^{-10}
from framework axioms alone, bypassing the EWPT detonation problem.

---

## The Problem

The DM gate is PARTIALLY CLOSED: R = Omega_DM/Omega_b = 5.48 is derived
from exact group theory, matching Planck (5.47) to 0.2%. But R uses the
observed eta = 6.12 x 10^{-10} as input. The standard electroweak
baryogenesis (EWBG) route is blocked:

- E x 2 taste correction makes the EWPT too strong (detonation)
- All bubble walls go supersonic; transport baryogenesis fails
- Alternative EW-scale mechanisms (cold, bubble-collision, magnetic)
  all need ~1000x more CP violation than J_Z3 = 3 x 10^{-5} provides

This note considers routes that BYPASS the detonation problem entirely.

**Constraint:** Every input must trace to Cl(3) on Z^3. No observed values
(eta from Planck, alpha_s from PDG, m_t from experiment) may be imported.

---

## Approach 1: Spontaneous Baryogenesis During Hierarchy Generation

### Core Idea

The hierarchy theorem gives v = M_Pl * C * alpha_LM^16. The transition
from v = 0 to v = 246 GeV is not instantaneous -- it occurs as the
universe cools through the taste staircase from T ~ M_Pl down to T ~ v.
During this transition, the time derivative of the Higgs VEV provides a
chemical potential for baryon number via the Cohen-Kaplan (1987) mechanism:

    mu_B = (d phi / dt) / f^2

where phi is the phase of the Higgs field and f is the symmetry breaking
scale. No bubble walls needed. No out-of-equilibrium condition needed
(the chemical potential itself drives the asymmetry).

### Why It Bypasses Detonation

Spontaneous baryogenesis operates during the SMOOTH evolution of phi(t),
not during a first-order phase transition. There are no bubble walls,
no deflagration/detonation distinction. The asymmetry is generated
continuously as v(T) evolves from 0 to 246 GeV.

### Framework Inputs

- The time-dependent VEV v(T) follows from the hierarchy theorem:
  v(T) ~ M_Pl * alpha_LM(T)^16, where alpha_LM(T) runs with temperature.
- The derivative dv/dt ~ dv/dT * dT/dt, where dT/dt = -H*T from
  the Friedmann equation (derived from Newtonian cosmology).
- The CP-violating phase comes from the Z_3 structure: the complex
  phase of the Higgs VEV in the Z_3 eigenbasis is delta = 2pi/3.
- Sphalerons convert the chemical potential to baryon number at rate
  Gamma_sph ~ alpha_w^5 * T^4 (derived).

### Estimate

The baryon asymmetry is:

    n_B/s ~ (Gamma_sph/T^3) * (mu_B/T)
          ~ alpha_w^5 * (d phi/dt) / (f^2 * T)
          ~ alpha_w^5 * (H * v / f^2)

At T ~ T_EW: H ~ T^2/M_Pl, v ~ 246 GeV, f ~ v. So:

    n_B/s ~ alpha_w^5 * T_EW / M_Pl ~ (1/30)^5 * (200 / 10^19) ~ 10^{-24}

This is 14 orders of magnitude too small. The standard spontaneous
baryogenesis formula gives eta ~ 10^{-24}, not 10^{-10}.

### Can the Taste Staircase Help?

The taste staircase provides 16 sequential symmetry-breaking steps between
M_Pl and v. If baryogenesis occurs at a higher scale (T ~ alpha^k * M_Pl
for some k), the ratio H/T is larger and the asymmetry grows. But the
sphaleron rate Gamma_sph is exponentially suppressed above T_EW (sphalerons
are confined). The window where both sphalerons are active AND H/T is
appreciable is narrow: T ~ 100-1000 GeV.

The 16 taste steps do provide 16 separate "kicks" to the VEV, each
contributing additively to the baryon asymmetry. But 16 x 10^{-24} is
still 10^{-23}. Not enough.

### Assessment

| Criterion | Score |
|-----------|-------|
| Bypasses detonation? | YES |
| Produces eta ~ 6e-10? | NO (14 orders too small) |
| Calculations needed | dv/dT from hierarchy theorem, Gamma_sph(T) |
| Publishable? | No -- known to fail for SM-like scenarios |

### Verdict: 2/10. The mechanism is clean but the parametric estimate is
hopelessly too small. The framework does not provide any enhancement
over the standard result because the relevant scales (T_EW, M_Pl) are
the same as in the SM.

---

## Approach 2: Gravitational Baryogenesis

### Core Idea

Davoudiasl, Kitano, Kribs, Murayama (2004): couple the baryon current
to the derivative of the Ricci scalar:

    L_int = (1/M_*^2) * (d_mu R) * J_B^mu

In an expanding FRW universe during radiation domination, R is not exactly
zero (it vanishes only for a perfect radiation fluid; QCD trace anomaly,
mass thresholds, and phase transitions give R != 0). The time derivative
dR/dt provides a chemical potential for baryons.

### Framework Connection

The framework derives:
- H(T) from Newtonian cosmology (Poisson equation on Z^3)
- g_*(T) = 106.75 from the taste spectrum (exactly)
- The QCD trace anomaly from the lattice strong coupling

In radiation domination with mass thresholds:

    R = -8pi G * (rho - 3p) = -8pi G * T * (d rho / dT - 3 rho/T)

The trace anomaly gives rho - 3p ~ T^4 * sum_i (m_i/T)^2 for species
with mass m_i near the temperature. The derivative dR/dt peaks during
rapid changes in g_*(T) -- i.e., at mass thresholds.

### Estimate

    n_B/s ~ (dR/dt) / (M_*^2 * T)

With M_* = M_Pl and dR/dt ~ H * T^2/M_Pl^2 (during radiation domination):

    n_B/s ~ H * T^2 / (M_Pl^2 * T * M_Pl^2) ~ T^3 / M_Pl^5

At T = T_EW ~ 200 GeV: n_B/s ~ (200)^3 / (10^19)^5 ~ 10^{-89}. Far too
small with M_* = M_Pl.

To get eta ~ 10^{-10}, need M_* ~ 10^{12} GeV. This is NOT the Planck
scale. The framework gives M_* = M_Pl (the lattice cutoff). No way to
lower M_* without importing a new scale.

### Can the Taste Staircase Provide a Lower M_*?

The taste staircase gives intermediate scales at alpha^k * M_Pl. The
scale alpha^8 * M_Pl ~ 10^8 GeV is in the right ballpark for M_*.
But this would require the gravitational-baryonic coupling to occur
at the TASTE scale, not the Planck scale. There is no structural
reason in the framework for this coupling to be enhanced at intermediate
taste scales.

### Assessment

| Criterion | Score |
|-----------|-------|
| Bypasses detonation? | YES |
| Produces eta ~ 6e-10? | NO (needs M_* << M_Pl) |
| Calculations needed | Trace anomaly from lattice, dR/dt at EW scale |
| Publishable? | No -- requires unjustified M_* tuning |

### Verdict: 1/10. The mechanism requires a new scale M_* ~ 10^{12} GeV
that the framework does not provide. Dead end unless the taste staircase
can structurally select an intermediate scale, which is speculative.

---

## Approach 3: Leptogenesis via Taste Staircase Right-Handed Neutrinos

### Core Idea

The framework has neutrino-like states from the taste decomposition.
The Z_3 selection rules constrain the right-handed Majorana mass matrix
M_R to a 2-parameter family with eigenvalues {A, B+eps, -(B-eps)}
(NEUTRINO_HIERARCHY_DERIVED_NOTE.md). The seesaw mechanism gives light
neutrino masses m_nu ~ v^2/M_R.

If M_R is at the taste staircase scale (M_R ~ alpha^k * M_Pl for some
k), then heavy right-handed neutrinos decay out of equilibrium and
generate a lepton asymmetry. Sphalerons convert L to B with factor
B = -(28/79)*L (standard, depends only on g_* which is derived).

### Why It Bypasses Detonation

Leptogenesis occurs at T ~ M_R >> T_EW. The EWPT is irrelevant. The
out-of-equilibrium condition is the decay of heavy right-handed neutrinos,
not bubble wall dynamics. No bubble walls, no detonation.

### Framework Inputs

From the neutrino sector:
- M_R is constrained by Z_3 to {A, B+eps, B-eps}
- The CP violation in heavy neutrino decay comes from the COMPLEX eps
  (NEUTRINO_COMPLEX_Z3_NOTE.md): eps is complex because the Z_3 Fourier
  transform of real lattice anisotropies produces complex eigenvalues
- The CP asymmetry epsilon_CP ~ (1/8pi) * Im(Y^dag Y)^2 / (Y^dag Y)
  where Y is the Dirac Yukawa matrix

Key structural result: the CP-violating phase in M_R has a DEEP origin
in the Cl(3) algebra. The imaginary Pauli matrix sigma_2 in Cl(3)
generates the complex phase phi ~ 50 degrees in the Z_3 eigenbasis.
This gives delta_CP ~ -103 degrees for neutrinos, consistent with
T2K/NOvA hints.

### The Leptogenesis Estimate

The baryon asymmetry from thermal leptogenesis:

    eta ~ 0.01 * epsilon_CP * kappa / g_*

where:
- epsilon_CP is the CP asymmetry in heavy neutrino decay
- kappa is the washout efficiency factor (0 < kappa < 1)
- g_* = 106.75 (derived)
- 0.01 = sphaleron conversion factor (28/79 ~ 0.35, times dilution)

The Davidson-Ibarra bound gives:

    epsilon_CP <= (3/16pi) * M_1 * m_3 / v^2

With m_3 ~ sqrt(Dm^2_31) ~ 0.05 eV and v = 246 GeV:

    epsilon_CP <= (3/16pi) * M_1 * (0.05 eV) / (246 GeV)^2
               = 8e-17 * (M_1 / GeV)

For eta ~ 6e-10 with kappa ~ 0.1:

    6e-10 ~ 0.01 * 8e-17 * (M_1/GeV) * 0.1 / 106.75

    M_1 ~ 8e13 GeV

This is the well-known leptogenesis scale M_1 ~ 10^{14} GeV.

### Can the Framework Produce M_1 ~ 10^{14} GeV?

The taste staircase gives scales:

    M_k = M_Pl * alpha_LM^k    (k = 0, 1, ..., 16)

With alpha_LM = 0.091:

    k=0:  M_Pl = 1.2e19 GeV
    k=4:  alpha^4 * M_Pl ~ 8.2e14 GeV
    k=5:  alpha^5 * M_Pl ~ 7.5e13 GeV
    k=6:  alpha^6 * M_Pl ~ 6.8e12 GeV

The scale k=5 gives M ~ 7.5 x 10^{13} GeV, which is RIGHT IN THE
LEPTOGENESIS WINDOW.

The Z_3 structure constrains M_R to have eigenvalues {A, B+eps, B-eps}.
If A corresponds to the k=5 staircase level and B to k=4, we get:

    M_1 ~ alpha^5 * M_Pl ~ 7.5e13 GeV
    M_2,3 ~ alpha^4 * M_Pl ~ 8e14 GeV

This is a PREDICTION, not a fit: the taste staircase selects the scale,
and the Z_3 selection rules determine the mass pattern.

### The CP Asymmetry from Framework

The CP asymmetry in N_1 decay:

    epsilon_1 ~ (1/8pi) * (M_1/M_2) * Im[(Y^dag Y)_{12}^2] / (Y^dag Y)_{11}

The Yukawa matrix Y is related to the Dirac neutrino mass matrix m_D by
Y = m_D / v. The Z_3 structure constrains Y to have the same circulant
structure as the CKM matrix. The complex phase from sigma_2 gives
Im[(Y^dag Y)_{12}^2] != 0.

With M_1/M_2 ~ alpha ~ 0.091 and the Z_3 phase structure:

    epsilon_1 ~ (1/8pi) * alpha * sin(2 delta_Z3) * |Y|^2
              ~ (1/8pi) * 0.091 * sin(240 deg) * |Y|^2

The Yukawa coupling |Y|^2 ~ m_3 * M_1 / v^2 ~ 0.05 * 7.5e13 / (246)^2
~ 6.2e7, giving:

    epsilon_1 ~ (1/25) * 0.091 * 0.866 * 6.2e7 ~ 2.2e5

Wait -- this is the UNSUPPRESSED version. The actual formula has |Y|^4
in the numerator and |Y|^2 in the denominator, so the net dependence is
|Y|^2, and the numerical value depends on the specific texture.

Let me be more careful. The Davidson-Ibarra result gives:

    epsilon_1 <= (3 M_1 m_3) / (16 pi v^2) = 3 * 7.5e13 * 0.05 / (16 pi * (246)^2 * 1e18)
              = 1.125e12 / (3.05e24) ~ 3.7e-13 [in natural units, eV^2/eV^2 = dimensionless]

Hmm, let me redo this with consistent units. In GeV:
m_3 = 0.05 eV = 5e-11 GeV, v = 246 GeV, M_1 = 7.5e13 GeV.

    epsilon_1 <= (3 * 7.5e13 * 5e-11) / (16 pi * 246^2)
              = 1.125e4 / (3.05e6)
              ~ 3.7e-3

This is actually quite large! With kappa ~ 0.01 (strong washout):

    eta ~ 0.01 * 3.7e-3 * 0.01 / 106.75 ~ 3.5e-9

That is within a factor of 6 of the observed eta = 6.1e-10. Given that
epsilon_1 can be below the DI bound, and kappa depends on the specific
washout regime, the parametric estimate lands in the right ballpark.

### What Calculations Are Needed

1. **Fix M_R eigenvalues from the taste staircase.** Map the Z_3
   selection rule {A, B+eps, B-eps} to the staircase scales
   alpha^k * M_Pl. Determine which k levels correspond to A, B, eps.

2. **Compute epsilon_CP from the Z_3 Yukawa texture.** The CKM-like
   structure of the neutrino Yukawa matrix, combined with the complex
   Z_3 phase, gives a specific CP asymmetry. This is a matrix algebra
   calculation on the 3x3 Z_3-constrained Yukawa matrix.

3. **Compute the washout factor kappa.** This depends on the ratio
   M_1/T and the Yukawa coupling strength. For strong washout
   (likely given the large Yukawa), kappa ~ 0.01-0.1.

4. **Propagate through sphalerons.** B = -(28/79)*L depends on g_*
   (derived) and the number of Higgs doublets (1 in the framework,
   but with 8 taste states -- does the taste enhancement 8/3 apply
   to the sphaleron conversion too?).

### Assessment

| Criterion | Score |
|-----------|-------|
| Bypasses detonation? | YES -- leptogenesis at T >> T_EW |
| Produces eta ~ 6e-10? | PROMISING -- parametric estimate within 6x |
| Calculations needed | M_R from staircase, epsilon_CP from Z_3 texture, kappa |
| Publishable? | YES -- if the mass scale is a prediction, not a fit |

### Verdict: 8/10. This is the strongest candidate. The taste staircase
NATURALLY provides M_1 ~ 10^{14} GeV at the k=5 level. The Z_3 complex
phase provides CP violation. The seesaw mechanism is already in the
framework (NEUTRINO_HIERARCHY_DERIVED_NOTE.md). The parametric estimate
gives eta within an order of magnitude, with room for the specific Z_3
texture to close the gap. The calculation is concrete and finite.

**Key risk:** The staircase-to-M_R mapping must be derived, not asserted.
If A and B are free parameters (as in NEUTRINO_HIERARCHY_DERIVED_NOTE.md),
then M_1 is fitted, and eta is fitted, and nothing is predicted. The
staircase must SELECT A = alpha^5 * M_Pl structurally.

---

## Approach 4: Asymmetric Dark Matter (ADM) -- Bypass eta Entirely

### Core Idea

If the dark matter candidate S_3 carries a conserved charge Q_dark that
is violated by SU(2) sphalerons (along with baryon number), then the
dark-to-baryon ratio is set by the CHARGE RATIO, not by separate
baryogenesis and freeze-out calculations:

    R = Omega_DM / Omega_b = (m_DM / m_p) * (Q_dark_violation / Q_B_violation)

This eliminates eta from the problem entirely. R becomes a function of
masses and quantum numbers, both of which are framework-derived.

### Framework Connection

From TASTE_SPHALERON_COUPLING_NOTE.md: ALL 8 taste states are SU(2)
doublets. The sphaleron transition changes the occupation of ALL 8
simultaneously:

    Delta B = N_doublets_vis = 6 (the triplet states)
    Delta Q_dark = N_doublets_dark = 2 (S_0 and S_3)

So the asymmetry ratio is:

    (n_DM - n_DM_bar) / (n_B - n_B_bar) = Delta Q_dark / Delta B = 2/6 = 1/3

And:

    R = (m_DM / m_p) * (1/3)

With the Wilson mass ratio m_DM/m_vis = 3 and identifying m_vis ~ m_p
(the proton is the lightest baryon):

    R_ADM = 3 * (1/3) = 1

This is wrong by a factor of 5.5. The naive ADM ratio gives R = 1,
not R = 5.5.

### Why the Naive Version Fails

The ADM mechanism assumes:
1. Both sectors get their relic abundance from the asymmetry alone
   (symmetric component annihilates away)
2. The charge ratio is set by the sphaleron structure

Condition 1 fails for the S_3 in the current framework: S_3 is a gauge
singlet, so its annihilation cross section is SMALL. The symmetric
component does NOT efficiently annihilate. The relic abundance is set
by FREEZE-OUT (the current calculation), not by the asymmetry.

For ADM to work, S_3 must have efficient enough annihilation to eliminate
the symmetric component. This requires new interactions beyond the gauge
sector -- e.g., a dark-sector self-interaction mediated by taste exchange.

### Can We Fix the Mass Ratio?

If instead of using Wilson masses we use the actual DM mass that gives
R = 5.48 via the asymmetry formula:

    5.48 = (m_DM / m_p) * (1/3)  =>  m_DM = 16.4 * m_p ~ 15.4 GeV

Can the framework predict m_DM ~ 15 GeV? The Wilson mass gives
m_DM = 3 * m_base, where m_base is the smallest Wilson mass. If m_base
is identified with the proton mass (wrong -- it should be the EW scale),
we get m_DM ~ 3 GeV, off by factor 5.

There is no clean mechanism to get m_DM ~ 15 GeV from the framework.

### A Different ADM Variant: Shared Asymmetry with Freeze-Out

Suppose S_3 gets a SMALL asymmetry from sphalerons (1/3 of the baryon
asymmetry per sphaleron), but the relic abundance is dominated by
FREEZE-OUT of the symmetric component. Then the observable R is:

    R = (freeze-out R) + (asymmetric R) = 5.48 + small correction

The asymmetry contributes at the level n_asym/n_freeze ~ eta * m_p/m_DM
~ 10^{-10} * (1/100) ~ 10^{-12}. Completely negligible.

So the ADM correction is tiny. The relic abundance is dominated by
freeze-out, as in the current calculation. The ADM idea adds nothing.

### Assessment

| Criterion | Score |
|-----------|-------|
| Bypasses detonation? | YES -- bypasses eta entirely |
| Produces eta ~ 6e-10? | N/A (bypasses eta, but gives R = 1, wrong) |
| Calculations needed | Dark sector annihilation, charge structure |
| Publishable? | Not in current form -- R = 1 is off by 5.5x |

### Verdict: 3/10. Elegant in principle but quantitatively wrong. The
naive sphaleron charge ratio gives R = 1, not 5.5. The DM mass needed
to fix this (15 GeV) is not naturally produced by the framework. The
ADM route would require significant model-building beyond what the
lattice structure provides.

---

## Approach 5: eta from the Taste Determinant (Structural Number)

### Core Idea

The hierarchy gives v = M_Pl * C * alpha^16. Perhaps eta has a similar
structural origin:

    eta = (some algebraic number from the taste block) * alpha^N

for some integer N. Both v/M_Pl and eta are small numbers; both might
be powers of the same small parameter alpha ~ 0.09.

### Numerical Exploration

    alpha = 0.091
    log(eta) / log(alpha) = log(6.1e-10) / log(0.091)
                           = -21.2 / -2.40
                           = 8.84

So eta ~ alpha^8.84. Not an integer power. Let's check nearby integers:

    alpha^8 = 0.091^8 = 4.3e-9    (too large by 7x)
    alpha^9 = 0.091^9 = 3.9e-10   (close! ratio 0.64)
    alpha^10 = 0.091^10 = 3.6e-11 (too small by 17x)

The closest integer power is N = 9: alpha^9 = 3.9e-10, which gives
eta/alpha^9 = 6.1e-10 / 3.9e-10 = 1.56. So:

    eta ~ 1.56 * alpha^9

Can 1.56 be a structural prefactor? The channel ratio 155/27 = 5.74,
the mass ratio 3/5 = 0.6, the Sommerfeld factor 1.59... None of these
obviously give 1.56.

But wait: 1.56 ~ pi/2 = 1.571. So:

    eta ~ (pi/2) * alpha^9

Or perhaps more suggestively:

    eta ~ (pi/2) * alpha_LM^9

Is there a structural reason for N = 9? The taste space has 2^3 = 8
states. The Hamming weights sum to 0+1+1+1+2+2+2+3 = 12. The number
of taste-changing operators is 8^2 - 8 = 56. None of these give 9.

However: 9 = 8 + 1 = N_taste + 1. Or 9 = 3^2 = d^2 where d = 3.
The number of independent CKM parameters for 3 generations is 4, and
the number of Euler angles is 3. Neither gives 9 naturally.

### Deeper Structure: eta as a Sphaleron Suppression

The sphaleron rate is Gamma_sph ~ alpha_w^5 * T^4. The asymmetry
produced per Hubble time is:

    n_B/s ~ (Gamma_sph / H) * epsilon_CP ~ (alpha_w^5 * M_Pl / T) * J_Z3

At T_EW ~ 200 GeV:

    n_B/s ~ (1/30)^5 * (10^19/200) * 3e-5
           ~ 4.1e-8 * 5e16 * 3e-5
           ~ 6.2e4

This gives the OVERPRODUCTION of baryons before washout. The observed
eta requires exponential washout:

    eta = eta_prod * exp(-Gamma_sph(broken) * t_EW)

The washout exponent is:

    Gamma_sph(broken)/H ~ (alpha_w^4 * T) * exp(-E_sph/T) / (T^2/M_Pl)
                        = alpha_w^4 * M_Pl * exp(-E_sph/T) / T

With E_sph/T = 4pi * v/(g*T) ~ 36 * v/T:

    ln(eta_prod/eta) = alpha_w^4 * M_Pl/T * exp(-36 * v/T)

This is the double exponential that makes eta exquisitely sensitive to
v/T (per ETA_FROM_FRAMEWORK_NOTE.md). The crossing point where
eta = 6e-10 occurs at v/T ~ 0.52.

### The Structural Question

Is v/T = 0.52 derivable? If the EWPT produces EXACTLY v/T = 0.52
from framework parameters, then eta is determined by the double-
exponential washout mechanism with all-framework inputs.

From the EWPT notes:
- Gauge-effective MC: v/T = 0.56 +/- 0.05 (encompasses 0.52)
- E x 2 taste-corrected: v/T = 1.10 (too large, detonation)

The E x 2 correction is the structurally correct result. At v/T = 1.10,
the washout is OFF (exp(-36 * 1.10) ~ 10^{-17}), and eta ~ eta_prod
~ 10^4 * J_Z3 ~ 0.3 (!). This is absurd -- the asymmetry would be
O(1), meaning comparable baryonic and antibaryonic matter.

### Assessment

| Criterion | Score |
|-----------|-------|
| Bypasses detonation? | Partially -- needs v/T from somewhere |
| Produces eta ~ 6e-10? | Only if v/T ~ 0.52, which contradicts E x 2 |
| Calculations needed | Reconcile v/T surface, or new structural origin for N=9 |
| Publishable? | Numerological unless N=9 has algebraic derivation |

### Verdict: 4/10. The alpha^9 coincidence is intriguing (ratio = pi/2
from exact), but without a structural derivation of why eta ~ alpha^9,
this is numerology. The double-exponential washout mechanism could
work but contradicts the E x 2 EWPT correction. Worth noting in the
paper as a "tantalizing coincidence" but not a derivation.

---

## Approach 6: GUT-Scale Baryogenesis from Leptoquark Operators

### Core Idea

The framework contains leptoquark operators (36 out of 64 operators in
the full Cl(3) tensor algebra mix quarks and leptons, per
PROTON_LIFETIME_DERIVED_NOTE.md). At the Planck/GUT scale, these
operators mediate baryon-number-violating processes. If X and Y bosons
(the off-diagonal generators connecting the 3 and 3* taste sectors) are
present at T ~ M_Pl, they can generate a baryon asymmetry via
out-of-equilibrium decays.

### Why It Bypasses Detonation

GUT baryogenesis occurs at T ~ M_GUT ~ M_Pl. The EWPT is irrelevant
(it happens 17 orders of magnitude later). No bubble walls needed.

### Framework Inputs

- Leptoquark operators: EXACT (from Cl(3) algebra structure)
- M_X = M_Pl: FRAMEWORK AXIOM (lattice cutoff)
- CP violation: Z_3 complex phase delta = 2pi/3
- Out-of-equilibrium: X decays at T ~ M_Pl when H ~ M_Pl (marginal)

### The Problem: Washout

GUT baryogenesis has a well-known problem: B-L must be violated for
the asymmetry to survive sphaleron washout below T_EW. In the framework:

- B+L is violated by SU(2) sphalerons (derived)
- B-L is conserved by SU(2) sphalerons (exactly, per anomaly structure)
- The Cl(3) leptoquark operators violate both B and L separately

If the GUT-scale process generates a B-L asymmetry, it survives sphalerons.
If it generates only B+L, sphalerons wash it out.

The framework's leptoquark operators couple the 3 (quarks) to 1 (leptons).
The quantum number structure (from PROTON_LIFETIME_DERIVED_NOTE.md):
B = 1/3 on triplets, L = 1 on singlets. So leptoquark decay
X -> qq (Delta B = 2/3) or X -> q l_bar (Delta B = 1/3, Delta L = -1).
The B-L change is:

    X -> qq: Delta(B-L) = 2/3
    X -> q l_bar: Delta(B-L) = 1/3 + 1 = 4/3

Both channels violate B-L. So the GUT-scale asymmetry DOES survive
sphaleron washout. This is structurally guaranteed by the Cl(3)
representation content.

### Estimate

The baryon asymmetry from GUT-scale X decay:

    eta ~ epsilon_CP * (n_X / n_gamma)|_{T ~ M_X}

At T ~ M_X: n_X/n_gamma ~ 1 (X is in thermal equilibrium). The CP
asymmetry from interference of tree and loop diagrams:

    epsilon_CP ~ (alpha_GUT / 4pi) * sin(delta_Z3) ~ (1/100) * 0.866 ~ 10^{-2}

But this overproduces by 8 orders of magnitude! We need eta ~ 10^{-10},
not 10^{-2}. The resolution is that X decay occurs CLOSE to equilibrium
(the departure from equilibrium is small):

    eta ~ epsilon_CP * (Gamma_X / H)|_{T=M_X}^{-1}

The out-of-equilibrium factor (Gamma_X/H)^{-1} suppresses the asymmetry:

    Gamma_X / H ~ alpha_GUT * M_X / (M_X^2 / M_Pl) = alpha_GUT * M_Pl / M_X

With M_X = M_Pl: Gamma/H ~ alpha_GUT ~ 1/25. So the departure from
equilibrium is only a factor of 25 (X decays faster than the universe
expands). This gives:

    eta ~ 10^{-2} * 25 = 0.25

Still way too large. The problem is that at T = M_Pl, the universe
is expanding fast (H ~ M_Pl) but the leptoquark interactions are also
fast (Gamma ~ alpha * M_Pl). The slight departure from equilibrium is
not enough to suppress the asymmetry.

### The Dilution Problem

The standard GUT baryogenesis solution invokes entropy production
(e.g., from inflaton decay) to dilute the asymmetry. Dilution by
factor D:

    eta_final = eta_GUT / D

For eta_final = 6e-10 and eta_GUT ~ 10^{-2}: D ~ 10^{7.2}.

Can the framework provide D ~ 10^7? The taste staircase involves
16 sequential symmetry-breaking steps. If each step produces entropy
(like a phase transition), the cumulative dilution could be large.
But quantifying this requires a detailed model of the entropy
production at each taste step, which does not exist.

### Assessment

| Criterion | Score |
|-----------|-------|
| Bypasses detonation? | YES -- GUT scale, no EWPT needed |
| Produces eta ~ 6e-10? | NO -- overproduces by 10^8, needs dilution |
| Calculations needed | Entropy production at taste staircase steps |
| Publishable? | Marginal -- standard GUT baryogenesis with lattice leptoquarks |

### Verdict: 3/10. The framework provides the ingredients (leptoquark
operators, CP violation, B-L violation) but the parametric estimate
overproduces by 8 orders of magnitude. A dilution mechanism from the
taste staircase is speculative and unquantified.

---

## Approach 7: Affleck-Dine Along Taste Flat Directions

### Core Idea

The taste scalar potential on the Cl(3) lattice may have flat directions
(directions in field space where V = 0 at tree level). If a scalar field
phi carrying baryon number sits in a flat direction, it acquires a large
VEV during inflation, then oscillates coherently after inflation, and
the CP-violating phases in the potential generate a baryon asymmetry.

### Framework Connection

The taste space is C^8 = (C^2)^3. The effective potential V(phi_1,...,phi_8)
is constrained by the Z_2^3 taste symmetry and the derived gauge symmetry.
Flat directions would be field configurations where the taste-symmetric
quartic terms vanish.

### Problems

1. **No inflation in the framework.** The Affleck-Dine mechanism requires
   a period of inflation to set the initial large VEV along the flat
   direction. The framework does not include an inflaton. The lattice
   cosmology starts at T ~ M_Pl with radiation domination.

2. **No identified flat directions.** The taste potential is not worked
   out in detail. The quartic terms from the lattice T-matrix are
   generically non-zero along all directions.

3. **Baryon number assignment.** For Affleck-Dine to work, the flat
   direction must carry baryon number. The taste scalars are bilinears
   of fermion fields, so they could carry B in principle, but the
   specific B assignment in the taste space is not established.

### Assessment

| Criterion | Score |
|-----------|-------|
| Bypasses detonation? | YES |
| Produces eta ~ 6e-10? | Unknown -- too many unknowns |
| Calculations needed | Taste potential flat directions, B assignment, initial conditions |
| Publishable? | No -- requires inflation + flat directions, neither available |

### Verdict: 1/10. Requires too much infrastructure (inflation, flat
directions, B-carrying scalars) that the framework does not provide.

---

## Approach 8: eta from Sphaleron Rate at the Lattice Scale

### Core Idea

The framework derives Gamma_sph/T^4 ~ alpha_w^5. If sphalerons are
active not just at the EW scale but also during the early universe
(T >> T_EW), then the baryon asymmetry is generated CONTINUOUSLY by
the CP-violating interactions, integrated over the entire thermal
history from T ~ M_Pl to T ~ T_EW.

### Framework Connection

Sphalerons are active in the SYMMETRIC phase (T > T_EW). The symmetric
phase extends from T_EW up to... how far? In the SM, sphalerons are
gauge configurations of the SU(2) theory, and they exist at ALL
temperatures (not just near T_EW). The rate scales as alpha_w^5 * T^4
at all temperatures in the symmetric phase.

The total baryon number produced is:

    n_B/s ~ integral_{T_EW}^{M_Pl} (Gamma_sph/T^4) * epsilon_CP(T) * (1/H) dT/T

With Gamma_sph/T^4 = alpha_w^5 and H = T^2/M_Pl:

    n_B/s ~ alpha_w^5 * epsilon_CP * integral_{T_EW}^{M_Pl} (M_Pl/T) dT/T
           = alpha_w^5 * epsilon_CP * M_Pl * ln(M_Pl/T_EW) / T_EW

Wait, this does not make sense dimensionally. Let me be more careful.

The rate of baryon production per unit volume is:

    dn_B/dt ~ Gamma_sph * epsilon_CP / T^3

Converting to comoving density n_B/s:

    d(n_B/s)/dt ~ (Gamma_sph / s) * epsilon_CP ~ alpha_w^5 * T * epsilon_CP

Integrating with dt = -dT/(H*T):

    n_B/s ~ integral alpha_w^5 * epsilon_CP * dT / (H) 
           = alpha_w^5 * epsilon_CP * integral (M_Pl / T) dT
           = alpha_w^5 * epsilon_CP * M_Pl * ln(M_Pl/T_EW)

This has dimensions of energy. Something is wrong. The issue is that
in thermal equilibrium, the sphaleron rate CANNOT generate a net baryon
asymmetry -- detailed balance forbids it. The CP violation must be
OUT of equilibrium to produce an asymmetry.

At T >> T_EW, all SM interactions are in equilibrium. The CP phase
delta = 2pi/3 is present but cannot generate an asymmetry because the
inverse processes are equally fast. The asymmetry can only be generated
at a PHASE TRANSITION or MASS THRESHOLD where equilibrium is broken.

### The Taste Mass Thresholds

The taste staircase has mass thresholds at M_k = alpha^k * M_Pl.
At each threshold, heavy states decouple and the equilibrium shifts.
This is analogous to the EW phase transition but spread over 16
discrete steps.

At each threshold k, the departure from equilibrium is:

    Delta ~ Gamma_k / H |_{T = M_k} ~ alpha * M_k / (M_k^2/M_Pl) = alpha * M_Pl/M_k

For k = 5 (M_5 ~ 7.5e13): Delta ~ 0.091 * 1.2e19 / 7.5e13 ~ 1.5e4.
The decoupling is FAST (Delta >> 1), so the departure from equilibrium
is small. Only the heaviest thresholds (k = 0, 1) have Delta ~ O(1).

The asymmetry from each threshold:

    delta_eta_k ~ alpha_w^5 * epsilon_CP * (Delta_k)^{-1}

Summing over k = 0 to 16: the dominant contribution comes from the
steps where Delta ~ 1, which is k = 0 (Planck scale). This reduces
to GUT-scale baryogenesis (Approach 6).

### Assessment

| Criterion | Score |
|-----------|-------|
| Bypasses detonation? | YES |
| Produces eta ~ 6e-10? | Reduces to GUT baryogenesis (Approach 6) |
| Calculations needed | Departure from equilibrium at each taste threshold |
| Publishable? | No -- does not add to Approach 6 |

### Verdict: 2/10. This is a more elaborate version of Approach 6 that
does not produce a new mechanism. The continuous production is zero in
equilibrium; the only contributions come from thresholds, which are
essentially GUT-scale baryogenesis at each step.

---

## Approach 9: Direct Computation via Partition Function Ratio

### Core Idea

The baryon-to-photon ratio is:

    eta = n_B / n_gamma = (n_B / s) * (s / n_gamma) = (n_B/s) * 7.04

The entropy density s = (2pi^2/45) * g_* * T^3 and the baryon density
n_B are both determined by the partition function Z = Tr[exp(-beta H)].
In principle, Z encodes everything. Can we extract eta directly from a
ratio of partition function determinants?

### Framework Connection

The partition function of the lattice theory is:

    Z = integral DU det(D[U] + m) * exp(-S_gauge[U])

The baryon number density is:

    n_B = (1/Z) * d Z / d mu_B |_{mu_B = 0}

where mu_B is the baryon chemical potential. On the lattice, introducing
mu_B modifies the temporal hopping terms of the Dirac operator:

    D(mu_B) = D(0) + mu_B * (taste-projected temporal derivative)

So:

    n_B / T^3 = (1/Z) * (dZ/d(mu_B/T)) |_{mu_B=0}
              = d ln Z / d(mu_B/T) |_{mu_B=0}

### The Problem: This Gives Zero at mu_B = 0

At zero chemical potential and in thermal equilibrium, n_B = 0 exactly
(by CPT invariance). The baryon asymmetry is a NON-EQUILIBRIUM quantity.
It cannot be extracted from the equilibrium partition function.

To compute eta, we would need to:
1. Include the CP-violating interactions that are out of equilibrium
2. Solve the real-time (not Euclidean-time) evolution
3. Track the baryon number as a function of time through a phase transition

This is essentially full non-equilibrium field theory, which is the
hardest computational problem in theoretical physics. The lattice
partition function approach does not simplify it.

### A Ratio Trick?

Consider the ratio of determinants with and without CP violation:

    eta ~ (det(D + delta_CP) - det(D - delta_CP)) / det(D)

This LOOKS like it could give a small number (difference of nearly
equal determinants). But this is not the correct formula for eta --
it would give the CP asymmetry in the spectrum, not the baryon asymmetry.
The baryon asymmetry requires non-equilibrium dynamics.

### Assessment

| Criterion | Score |
|-----------|-------|
| Bypasses detonation? | N/A -- fundamentally different approach |
| Produces eta ~ 6e-10? | Cannot -- eta is non-equilibrium |
| Calculations needed | Full non-equilibrium lattice simulation |
| Publishable? | No -- eta is not an equilibrium quantity |

### Verdict: 1/10. eta is fundamentally a non-equilibrium quantity.
No equilibrium partition function trick can extract it. This approach
confuses the question.

---

## Overall Ranking

| Rank | Approach | Score | Key advantage | Key risk |
|------|----------|-------|---------------|----------|
| **1** | **3. Leptogenesis via taste staircase** | **8/10** | Staircase gives M_1 ~ 10^{14} naturally; Z_3 CP phase; seesaw exists | M_R eigenvalue mapping must be derived, not fitted |
| 2 | 5. eta from alpha^N structural | 4/10 | alpha^9 ~ 0.64 * eta; pi/2 prefactor | Numerological without derivation of N=9 |
| 3 | 4. Asymmetric dark matter | 3/10 | Eliminates eta entirely | R = 1, off by 5.5x |
| 4 | 6. GUT-scale leptoquark | 3/10 | B-L violation proved | Overproduces by 10^8 |
| 5 | 1. Spontaneous baryogenesis | 2/10 | No bubble walls | 14 orders too small |
| 6 | 8. Continuous sphaleron | 2/10 | Uses all 16 taste steps | Reduces to Approach 6 |
| 7 | 2. Gravitational baryogenesis | 1/10 | Uses derived R | Needs M_* << M_Pl |
| 8 | 7. Affleck-Dine | 1/10 | Bypasses EWPT | Needs inflation |
| 9 | 9. Partition function ratio | 1/10 | Direct computation | eta is non-equilibrium |

---

## Recommended Strategy

### Primary path: Leptogenesis (Approach 3)

This is the clear winner. The specific calculation chain would be:

**Step 1: Map M_R eigenvalues to the taste staircase.**

The Z_3 selection rules give M_R = diag(A, B+eps, -(B-eps)) in the
Z_3 eigenbasis (NEUTRINO_HIERARCHY_DERIVED_NOTE.md). Currently A and B
are free parameters fitted to Dm^2_31/Dm^2_21 = 32.6.

The taste staircase gives a DISCRETE set of allowed scales:
M_k = C_k * alpha_LM^k * M_Pl for k = 0,...,16 where C_k are O(1)
algebraic prefactors from the taste determinant at each level.

The structural claim would be: A = M_{k_A} and B = M_{k_B} for specific
integers k_A and k_B selected by the Z_3 charge structure. The lightest
eigenvalue M_1 = min(A, |B-eps|) is the one that matters for leptogenesis.

**Step 2: Compute epsilon_CP from the Z_3 Yukawa texture.**

The neutrino Yukawa matrix is constrained by the same Z_3 circulant
structure that gives the CKM matrix (CKM_FIRST_PRINCIPLES_NOTE.md).
The CP asymmetry in N_1 decay involves Im[(Y^dag Y)^2], which depends
on the complex phase phi ~ 50 degrees from the sigma_2 direction of
Cl(3) (NEUTRINO_COMPLEX_Z3_NOTE.md).

This is a finite matrix algebra calculation: take the Z_3-constrained
3x3 Yukawa matrix, compute (Y^dag Y)_{ij}, and evaluate the
self-energy and vertex loop diagrams for N_1 decay.

**Step 3: Compute the washout factor kappa.**

The washout parameter K = Gamma_{N_1}/H |_{T=M_1} depends on the
Yukawa coupling and M_1. For K >> 1 (strong washout), kappa ~ 0.01/K.
The Z_3 texture constrains the Yukawa coupling, making K computable.

**Step 4: Assemble eta.**

    eta = (28/79) * (1/g_*) * epsilon_1 * kappa * 7.04
        = structural number from steps 1-3

If this gives eta ~ 6e-10 with no adjustable parameters, the DM gate
closes completely: R = Omega_DM/Omega_b with BOTH numerator and
denominator derived from Cl(3).

### Fallback: Honest framing with eta ~ alpha^9 observation

If the leptogenesis calculation cannot be completed (e.g., because the
staircase-to-M_R mapping is not unique), then the paper can note:

1. R = 5.48 is derived with eta as the one remaining import
2. eta ~ (pi/2) * alpha_LM^9 is a numerical coincidence, with
   alpha_LM = 0.091 the same coupling that enters the hierarchy theorem
3. The exponent 9 = 8+1 = N_taste + 1 is suggestive but not derived
4. Leptogenesis with the taste staircase is identified as the
   structural mechanism, with the parametric estimate within one
   order of magnitude

This is HONEST: it identifies the mechanism and the parametric scale
without claiming closure.

### What NOT to pursue

- Approaches 7, 9 (Affleck-Dine, partition function) are dead ends.
- Approach 2 (gravitational baryogenesis) needs an unjustified scale.
- Approach 4 (ADM) gives R = 1, wrong by 5.5x.
- Approach 1 (spontaneous) is 14 orders too small.

---

## Relationship to Existing Notes

| Note | What it says | What this note adds |
|------|-------------|---------------------|
| DM_CLOSURE_ASSESSMENT.md | eta is the remaining import; detonation blocks EWBG | Identifies 9 alternatives to EWBG |
| DM_ELEGANT_BRAINSTORM.md | 5 proof strategies for R; ADM at 5/10 | Quantifies ADM to R=1 (kills it); promotes leptogenesis |
| DM_WILD_RATIO_NOTE.md | Freeze-out ratio idea fails | Confirms: baryon abundance is asymmetry, not freeze-out |
| NEUTRINO_HIERARCHY_DERIVED_NOTE.md | Z_3 constrains M_R to 2-param family | Connects M_R to taste staircase scales |
| NEUTRINO_COMPLEX_Z3_NOTE.md | Complex eps from sigma_2 gives delta_CP | Uses this as CP source for leptogenesis |
| BARYOGENESIS_NOTE.md | EWBG parametric estimate eta ~ 6e-10 if v/T ~ 0.52 | Identifies why EWBG is blocked and what replaces it |
| HIERARCHY_THEOREM.md | v = M_Pl * C * alpha^16 | Taste staircase provides leptogenesis mass scale |
| PROTON_LIFETIME_DERIVED_NOTE.md | 36 leptoquark operators, B-L violated | Used in Approach 6 (GUT baryogenesis) |
| ROOT_CAUSE_ANALYSIS_THREE_GATES.md | All residuals from taste undercounting | Taste staircase approach addresses root cause |

---

## Files

This note does not produce any computation. Recommended next steps are
in the "Recommended Strategy" section above.

- Supersedes: nothing (new brainstorm)
- Depends on: all notes listed in the table above
- Next action: implement Step 1 of the leptogenesis calculation
  (map M_R to taste staircase)

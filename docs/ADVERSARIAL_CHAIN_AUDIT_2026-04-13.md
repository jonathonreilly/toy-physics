# Adversarial Chain Audit: y_t and DM Closure Claims

**Date:** 2026-04-13
**Role:** Hostile referee -- find every hidden observed input
**Target:** GATE_CLOSURE_CASE_YT_DM_2026-04-13.md

---

## METHOD

For every number in both chains, trace provenance to EITHER:
- (A) The axiom: Cl(3) on Z^3
- (T) T_CMB = 2.7255 K (the one declared boundary condition)

Anything that traces to neither is FLAGGED.

---

## y_t CHAIN AUDIT

### 1. g_bare = 1 -- where does it come from?

**VERDICT: AMBER -- defensible but needs explicit axiom-level justification**

The code (`frontier_alpha_s_determination.py` line 151) sets `g_bare_unit = 1.0` with
the comment "unit hopping: g = 1." The justification given is that the gauge coupling
enters the link variable as U = exp(i g A a), and at the lattice scale a = 1 in lattice
units, "the natural normalization is g A a = O(1), giving g ~ 1 when A ~ 1/a."

This is NOT the same as deriving g = 1 from Cl(3). It is a *convention* that the
kinetic term coefficient is unity -- i.e., the gauge field is canonically normalized at
the lattice scale. This is analogous to setting hbar = 1 in natural units: it is a
unit choice, not a dynamical prediction. The beta = 2 N_c / g^2 = 6 that follows is
the strong-coupling regime of lattice QCD.

**Severity:** LOW. Canonical normalization of the kinetic term IS determined by the
lattice action structure. The Wilson action fixes the relationship between beta and g.
Setting g = 1 at the cutoff is equivalent to specifying the lattice spacing in units
of the Planck length. This traces to the axiom (lattice spacing = Planck length).
But the document should state this explicitly as: "g_bare = 1 follows from canonical
normalization of the staggered Hamiltonian at a = l_Pl."

### 2. Lepage-Mackenzie tadpole coefficient

**VERDICT: CLEAN**

The tadpole integral I_tad = 0.2527 is computed directly on the 3D lattice
(`frontier_yt_matching.py` lines 134-167) by summing 1/D_lat(k) over the Brillouin
zone. This is a pure lattice calculation -- the Luscher-Weisz value is cited only as
a cross-check. The Lepage-Mackenzie prescription (mean-field improvement via
u_0 = <P>^{1/4}) is standard lattice perturbation theory applied to the framework's
own lattice action. No observed input enters.

### 3. V-to-MSbar conversion: r_1 = 3.83, n_f = 6

**VERDICT: FLAGGED -- n_f = 6 is imported SM particle content**

The conversion coefficient r_1 (`frontier_yt_boundary_resolution.py` line 275):
```
r_1 = a_1/4 + (5/12) * beta_0
a_1 = (31/9) * C_A - (20/9) * T_F * n_f
```

The value n_f = 6 is set on line 257: `n_f_Pl = 6  # all SM quarks active at M_Planck`.

The claim is that n_f = 6 follows from the taste spectrum: 8 taste states decompose as
(2,3) + (2,1) under SU(2) x SU(3), giving 2 quark flavors per generation x 3
generations = 6 quarks. The 3 generations come from Z_3 orbits.

**Assessment:** This IS derivable within the framework IF the generation counting
(N_gen = 3 from Z_3 triplet structure) is accepted. The key chain is:
Cl(3) -> 8 taste states -> SU(2) x SU(3) decomposition -> 2 quarks/gen -> 3 gen -> n_f = 6.
The chain is long but each step is structural.

**Residual concern:** The identification of taste states with physical quark flavors is
an interpretation of the lattice content, not a derivation from first principles. A
hostile referee could argue: "You have 8 taste states per generation, so why not
n_f = 8 x 3 = 24?" The answer (taste states are not independent propagating degrees
of freedom for RGE purposes) relies on understanding continuum-limit taste reduction,
which is standard in staggered QCD but is additional physics knowledge, not pure axiom.

**Severity:** MEDIUM. The derivation of n_f = 6 requires the standard staggered fermion
interpretation (taste reduction in continuum limit). This is structural lattice QCD
knowledge, not an observed input per se, but it is also not pure Cl(3) axiom content.

### 4. 2-loop SM RGE thresholds: m_b = 4.18, m_c = 1.27, m_tau = 1.78, m_t = 173

**VERDICT: FLAGGED -- observed quark masses used as RGE thresholds**

The RGE (`frontier_yt_boundary_resolution.py` lines 82-85) hardcodes:
```python
M_B = 4.18             # GeV (b quark MSbar mass)
M_C = 1.27             # GeV (c quark MSbar mass)
M_TAU = 1.7768         # GeV
```

These enter the step-function threshold (line 429-438):
```python
def n_eff_sm(mu):
    if mu > M_T_OBS:   return 6
    elif mu > M_B:      return 5
    elif mu > M_C:      return 4
    else:               return 3
```

These threshold masses are OBSERVED INPUTS. They are NOT derived from the axiom.
The framework would need to derive the entire quark mass spectrum (m_b, m_c, etc.)
from Cl(3) structure to make this claim clean. Currently, the RGE running from
M_Pl to M_Z uses observed b and c quark masses to decide where to change n_f.

**Severity:** LOW-MEDIUM. The RGE thresholds affect the running at the ~0.5% level
(the running is logarithmic and dominated by the large desert between M_Pl and M_Z
where n_f = 6 throughout). Moving m_b by 50% changes m_t by roughly 0.1-0.3%.
The effect is within the stated 1% error budget, but the document claims "every step
framework-derived" and this step is not.

### 5. Higgs VEV v = 246 GeV

**VERDICT: FLAGGED -- observed input used in final step**

The conversion from y_t(M_Z) to m_t uses (`frontier_yt_boundary_resolution.py` line 531):
```python
mt = yt_mz * V_SM / np.sqrt(2)
```
with V_SM = 246.22 GeV (line 86).

This is an OBSERVED quantity. To derive m_t from y_t, you need v_EW. The framework
would need to derive EWSB and the Higgs VEV from Cl(3) structure.

**Severity:** HIGH. This is not a small correction -- it is the ENTIRE conversion from
coupling to mass. Without v, the chain predicts y_t(M_Z), not m_t. The document
states m_t = 171 GeV as the output, but this requires v = 246 GeV as input.

The honest claim should be: "We predict y_t(M_Z) from the axiom. Combined with the
observed v = 246 GeV, this gives m_t = 171 GeV." This makes the prediction a
ONE-parameter prediction (using v), not a zero-parameter prediction.

Alternatively, if v is derived elsewhere in the framework (e.g., from EWSB cascade),
this should be explicitly cited in the chain. Currently it is not.

### 6. EW gauge couplings at M_Z used for RGE initialization

**VERDICT: FLAGGED -- used in "consistent g3" approach**

Line 89-92 of `frontier_yt_boundary_resolution.py`:
```python
ALPHA_S_MZ = 0.1179    # PDG 2024
ALPHA_EM_MZ = 1.0 / 127.951
SIN2_TW_MZ = 0.23122
```

The "Scenario C" (the one that gives m_t = 171 GeV) uses g1_pl and g2_pl from running
these observed M_Z couplings UP to M_Pl (lines 418-422). The y_t boundary comes from
the lattice, but g1 and g2 at M_Pl come from running OBSERVED alpha_EM and sin^2(theta_W).

**Severity:** LOW. The y_t running is dominated by g3 (QCD), not g1/g2 (EW). The
sensitivity to g1, g2 is at the ~0.1% level. But the document says "every step
framework-derived" and these EW couplings at M_Z are observed.

### y_t CHAIN SUMMARY

| Input | Source | Observed? | Severity |
|-------|--------|-----------|----------|
| g_bare = 1 | Canonical normalization at a = l_Pl | Convention/axiom | LOW |
| I_tad = 0.2527 | Lattice Brillouin zone sum | No | CLEAN |
| n_f = 6 | Taste decomposition + generation counting | Structural | MEDIUM |
| m_b = 4.18, m_c = 1.27 | PDG quark masses | YES | LOW-MEDIUM |
| v = 246 GeV | Observed Higgs VEV | YES | HIGH |
| alpha_EM, sin^2(theta_W) at M_Z | PDG electroweak | YES | LOW |
| M_Z = 91.19 GeV | Observed Z mass | YES | LOW |

**Bottom line:** The chain uses at least 4 observed inputs (v, m_b, m_c, EW couplings).
The dominant one is v = 246 GeV. The correct framing is: "We predict y_t(M_Z) from
the axiom; combined with the observed v and standard RGE with observed thresholds,
this gives m_t = 171 GeV, 1.1% from observation."

---

## DM CHAIN AUDIT

### 1. MC computation of v/T

**VERDICT: AMBER -- the MC itself is framework, but uses SM-observed parameters**

The MC in `frontier_ewpt_gauge_closure.py` uses:
- G_WEAK = 0.653 (line 79) -- SU(2) coupling
- G_PRIME = 0.350 (line 80) -- U(1) coupling
- Y_TOP = 0.995 (line 81) -- top Yukawa
- M_H = 125.1 (line 88) -- Higgs mass
- M_W = 80.4, M_Z = 91.2 (lines 87-88)
- V_EW = 246.0 (line 90) -- Higgs VEV
- T_EW = 160.0 (line 93) -- EW phase transition temperature

**Key question:** Are these framework-derived or observed?

The document claims the MC is a "framework computation." But the CW potential that
the MC samples is constructed from M_H, M_W, M_Z, V_EW, and gauge couplings. If these
are the OBSERVED values, then the MC is effectively parameterized by observation.

If these are derived elsewhere in the framework (e.g., M_W from g2 * v/2, etc.), the
derivation chain must be shown. Currently, `frontier_dm_native_eta.py` (line 88) sets
`M_T = 173.0` and `V_EW = 246.0` as hardcoded constants labeled "SM masses (GeV)."

**Severity:** HIGH for the eta chain. The EWPT strength v(T_n)/T_n is a critical
multiplier in the baryogenesis calculation. Using observed SM masses to construct
the CW potential means the eta prediction implicitly contains observed inputs.

### 2. Taste enhancement 8/3 -- do all 8 tastes couple to sphalerons?

**VERDICT: FLAGGED -- assumption not proved**

The code (`frontier_dm_native_eta.py` lines 468-476) states: "all 8 taste states of a
given generation share the SAME gauge quantum numbers, so their chemical potentials are
locked by gauge interactions."

This means the claim is: taste states have the same SU(2) charge, so sphalerons
(which are SU(2) processes) act on all of them equally.

**Problem:** Sphalerons couple to LEFT-HANDED SU(2) doublets. Of the 8 taste states,
how many are left-handed doublets vs. right-handed singlets? If tastes are merely
copies of the same gauge representation, then yes, all 8 couple. But if tastes have
different chiralities (as staggered fermions normally produce -- 4 tastes with each
chirality in 4D), then only 4 of 8 couple to sphalerons, and the enhancement would
be 4/3, not 8/3.

The document does not address this. The code simply asserts TASTE_RATIO = 8/3.

**Severity:** HIGH. This is a factor-of-2 question. If the correct ratio is 4/3
instead of 8/3, eta drops by half, destroying the 0.5% match.

### 3. BBN step: eta -> Omega_b uses m_p

**VERDICT: AMBER -- claimed derived but chain not shown**

The BBN script (`frontier_bbn_from_framework.py` line 141) claims m_p is derived:
"m_p = Lambda_QCD * f(alpha_s), where alpha_s from plaquette action."

This is in principle correct: m_p ~ Lambda_QCD up to a dimensionless factor from
lattice QCD. Lambda_QCD is set by alpha_s at the lattice scale and the RG running.
But the actual VALUE m_p = 1.67262192e-27 kg (line 126) is the OBSERVED proton mass,
not a computed lattice QCD result.

The framework has never actually computed m_p from its lattice. It claims m_p is
derivable in principle, then uses the observed number.

**Severity:** LOW-MEDIUM. Since Omega_b = eta * n_gamma * m_p / rho_crit, using the
observed m_p means the BBN conversion is partly observational. However, the proton
mass IS in principle computable from QCD, and the 0.7% He correction is noted as
negligible. The honest framing: "The conversion uses m_p, which is computable from
lattice QCD but we use the observed value for convenience."

### 4. g_* = 106.75 -- does it count tastes?

**VERDICT: FLAGGED -- internal inconsistency**

The freeze-out script (`frontier_freezeout_from_lattice.py` lines 248-284) derives
g_* = 106.75 by counting the STANDARD MODEL particle content: 28 boson d.o.f. +
(7/8) * 90 fermion d.o.f. = 106.75.

But the DM chain ALSO uses 8 taste states per generation for the baryogenesis
enhancement. If tastes are physical d.o.f. above the EWPT temperature (~160 GeV),
they should contribute to g_*. With 8 taste scalars contributing 8 additional bosonic
d.o.f., g_* would be 106.75 + 8 = 114.75 (or more, depending on taste spectrum).

Actually, `frontier_dm_native_eta.py` line 98 uses G_STAR = 110.75 with the comment
"Relativistic d.o.f. (SM + 4 taste scalars)." This DIFFERS from the 106.75 used in
the freeze-out chain.

**Internal inconsistency:** The DM ratio chain uses g_* = 106.75 for freeze-out, but
the baryogenesis chain uses g_* = 110.75 for sphaleron rates. These should be the same
number if both apply at the same epoch (T ~ 100-160 GeV).

**Severity:** MEDIUM. The 4% difference in g_* propagates as ~2% in x_F and ~1% in R.
The inconsistency suggests the taste scalar contribution to g_* has not been
self-consistently treated.

### 5. Hubble parameter H(T) and H_0

**VERDICT: FLAGGED -- H_0 = 67.4 km/s/Mpc is observed**

The BBN script (`frontier_bbn_from_framework.py` line 135) uses:
```python
H_0_SI = 67.4e3 / 3.0857e22   # s^-1
```

This is the OBSERVED Hubble constant from Planck 2018. The document claims H_0 is
"derived" via H_0 = c/R_Hubble where R_Hubble = N^{1/3} * a, but N (total lattice
sites) is never actually computed.

For the freeze-out computation, H(T) = sqrt(8 pi G rho / 3) with
rho = (pi^2/30) g_* T^4, which uses G = 1/M_Pl^2 (derived from a = l_Pl) and g_*
(from taste counting). So H(T) at the EWPT epoch does NOT use H_0.

But the conversion of rho_crit = 3 H_0^2 / (8 pi G) in the BBN step DOES use H_0.
Since rho_crit determines Omega_b = rho_b / rho_crit, the final Omega_b value
depends on the observed H_0.

**Severity:** MEDIUM-HIGH. Omega_b and Omega_DM are defined relative to rho_crit,
which requires H_0. The ratio R = Omega_DM / Omega_b is H_0-independent (it cancels),
but the individual Omega values require H_0. The document quotes Omega_Lambda = 0.682
matching observation -- this comparison requires H_0 as input.

### 6. R = 5.48 and x_F = 27 -- does x_F use observed Omega_DM?

**VERDICT: CLEAN for x_F -- but x_F is not 27 in the code**

The freeze-out computation (`frontier_freezeout_from_lattice.py` lines 367-393)
solves x_F iteratively from the freeze-out equation using only lattice inputs
(alpha_s, g_*, M_Pl, m_chi). The code does NOT use Omega_DM as input for x_F.

However, the x_F values computed range from ~15 to ~45 depending on m_chi (line 427),
with a mean around 25-30. The value x_F = 27 cited in the closure document is
consistent but is not a unique prediction -- it depends on the DM mass, which is
not precisely specified.

The DM ratio R = C_2(8)/C_2(3) * Sommerfeld_correction. The Sommerfeld factor
uses v_rel = 2/sqrt(x_F), so R does depend weakly on x_F. But the code in
`frontier_alpha_s_determination.py` line 71 uses `X_F = 25.0` (not 27).

**Severity:** LOW. The x_F dependence is logarithmic and R varies by ~20% over
x_F = [15, 45]. The specific value matters at the ~5% level.

### 7. Sphaleron rate: kappa_sph = 20.0

**VERDICT: FLAGGED -- imported from d'Onofrio et al. 2014**

`frontier_dm_native_eta.py` line 119: `KAPPA_SPH = 20.0  # d'Onofrio et al. 2014`

This is a lattice QCD result for the sphaleron rate prefactor, published by d'Onofrio
et al. It is not derived from the Cl(3) axiom. It is a result of SU(2) gauge theory
lattice simulations that were performed independently of this framework.

**Counterargument:** The sphaleron rate is a pure SU(2) gauge theory quantity,
computable in principle from the lattice. If the framework claims to contain SU(2)
gauge theory, then kappa_sph is in principle derivable. But it has not actually been
derived within the framework -- the published value is imported.

**Severity:** LOW-MEDIUM. Similar to using Luscher-Weisz's I_tad value -- it's
structural lattice gauge theory, not an observed SM parameter. But it IS external
computation, not framework-derived.

### 8. c_mag = 0.37 from Kajantie et al. 1996

**VERDICT: FLAGGED -- imported external lattice result**

`frontier_dm_native_eta.py` line 198: `c_mag = 0.37  # Kajantie et al. NPB 458:90 (1996)`

The magnetic mass coefficient is a non-perturbative 3D SU(2) lattice result. The code
explicitly acknowledges this (line 428): "The only non-framework input is c_mag = 0.37
from 3D SU(2) lattice."

**Severity:** MEDIUM. This enters the non-perturbative enhancement of v/T, which
directly affects eta. The analytic route (v/T = 0.73 without c_mag) gives eta that
is 15% off. The MC route (v/T = 0.80) still relies on SM masses.

### 9. SM masses in the baryogenesis chain

**VERDICT: FLAGGED -- pervasive use of observed masses**

`frontier_dm_native_eta.py` uses:
- M_W = 80.4, M_Z = 91.2, M_H = 125.1, M_T = 173.0, V_EW = 246.0
- alpha_s(M_Z) = 0.1185

These are ALL observed values. They enter the CW potential, the cubic coefficient
E, the running of alpha_s to T_n, the diffusion coefficients, and the wall velocity.

**Severity:** HIGH. The eta = 6.15e-10 prediction is built on top of observed SM
parameters throughout. The honest claim is: "Given the SM spectrum (which we aim to
derive separately), the Z_3 CP phase + taste enhancement gives eta."

---

## DM CHAIN SUMMARY

| Input | Source | Observed? | Severity |
|-------|--------|-----------|----------|
| alpha_s = 0.092 | Lattice plaquette | No | CLEAN |
| C_2(8)/C_2(3) = 31/9 | SU(3) group theory | No | CLEAN |
| Sommerfeld factor | Lattice Green's function | No | CLEAN |
| x_F ~ 25 | Freeze-out equation with lattice inputs | No | CLEAN |
| g_* = 106.75 | Taste spectrum counting | Structural | CLEAN (but inconsistent with 110.75) |
| N_taste/N_gen = 8/3 | All 8 tastes couple to sphalerons | ASSUMED | HIGH |
| M_W, M_Z, M_H, M_T, V_EW | Observed SM spectrum | YES | HIGH |
| kappa_sph = 20 | d'Onofrio et al. lattice | External computation | LOW-MEDIUM |
| c_mag = 0.37 | Kajantie et al. lattice | External computation | MEDIUM |
| H_0 = 67.4 | Planck 2018 | YES | MEDIUM-HIGH |
| m_p = 1.673e-27 kg | Observed proton mass | YES (in principle derivable) | LOW-MEDIUM |
| alpha_s(M_Z) = 0.1185 | PDG | YES | MEDIUM |
| T_CMB = 2.7255 K | Observed | YES (declared boundary) | ACCEPTED |

---

## OVERALL VERDICT

### y_t chain: NOT zero-parameter

The chain predicts y_t(M_Z) from the axiom with ~2 structural inputs (g_bare
normalization, n_f from taste counting). But converting to m_t requires the observed
Higgs VEV v = 246 GeV, and the RGE uses observed quark thresholds (m_b, m_c) and
EW couplings. The correct framing is a ONE-parameter prediction:

> "Given v = 246 GeV, the framework predicts m_t = 171 GeV from Cl(3) structure alone."

The RGE threshold sensitivity is within the error budget (~0.3%), so those observed
inputs are defensible as sub-leading corrections.

### DM chain: NOT zero-parameter, substantial hidden imports

The R = 5.48 prediction (DM-to-baryon ratio) has a CLEAN core: Casimir ratio + 
Sommerfeld + freeze-out from lattice inputs. This part genuinely traces to the axiom.

The eta = 6.15e-10 prediction has MULTIPLE observed inputs: SM masses (M_W, M_Z, M_H,
M_T, V_EW), sphaleron and magnetic mass coefficients from external lattice
computations, and alpha_s(M_Z). The 8/3 taste enhancement is assumed but not proved
(chirality of taste states under sphalerons is unaddressed).

The Omega_Lambda = 0.682 comparison additionally requires H_0.

### g_* inconsistency

The DM ratio chain uses g_* = 106.75. The baryogenesis chain uses g_* = 110.75.
These should be reconciled.

### Recommended corrections to the closure document

1. State that v = 246 GeV is a REQUIRED input for the m_t prediction
2. Acknowledge RGE thresholds use observed m_b, m_c (sub-leading)
3. Prove or acknowledge the chirality question for the 8/3 enhancement
4. List ALL SM masses used in the baryogenesis chain as inputs
5. Reconcile g_* = 106.75 vs 110.75 inconsistency
6. Acknowledge H_0 is needed for Omega comparisons (but not for R)
7. Distinguish "structural lattice QCD results" (kappa_sph, c_mag) from
   "framework-derived" -- these are external computations, not axiom outputs

### What IS genuinely framework-derived (clean)

- alpha_plaq = 0.092 from g_bare = 1 lattice plaquette
- y_t/g_s = 1/sqrt(6) from Ward identity + trace identity
- Z_gauge = 1 from Feshbach projection
- Z_y/Z_g = 1 from vertex factorization
- R_base = C_2(8)/C_2(3) = 31/9 from group theory
- Sommerfeld factor from lattice Green's function
- x_F ~ 25 from freeze-out equation with lattice inputs
- g_* = 106.75 from taste spectrum counting (if tastes = SM)
- Boltzmann equation as lattice master equation limit

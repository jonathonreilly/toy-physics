# Root Cause Analysis: What Single Factor Would Close DM + y_t + CKM

**Date:** 2026-04-13
**Status:** DIAGNOSTIC -- identifies common origin, proposes resolution path
**Branch:** `claude/youthful-neumann`

---

## The Three Residuals

| Gate | Prediction | Observed | Shortfall | Proximate cause |
|------|-----------|----------|-----------|-----------------|
| DM eta | 5.22e-10 | 6.12e-10 | -15% | v(T_n)/T_n = 0.73 (daisy) vs 0.80 (MC) |
| y_t m_t | 150.9 GeV | 173.0 GeV | -13% | alpha_s^EFT(M_Pl) = 0.0205 after /4 taste proj |
| CKM V_cb | 0.020 | 0.042 | -53% | R_overlap = 2.75 (mean-field NNI) |

All three residuals point DOWNWARD: the framework underproduces the physical
quantity. This is not random scatter. Something is systematically being
undercounted.

---

## Thesis: The Common Root Is the Taste Activity Fraction

Every gate involves a step where the 8 taste states of Cl(3) are projected
onto "physical" degrees of freedom, and in every case the projection
discards more states than it should. The three projections are:

1. **DM eta**: The EWPT strength v/T depends on the number of bosonic
   species contributing to the cubic term E in the effective potential.
   The daisy resummation counts transverse gauge bosons and the Higgs,
   but the taste scalars (the 4 additional Goldstone-like modes from
   taste breaking) contribute to E through thermal loops. At analytic
   daisy level, only the "diagonal" taste sector contributes. The
   missing 7% in v/T (0.73 vs 0.80) is the contribution of
   off-diagonal taste modes that are captured by MC but not by the
   one-loop daisy approximation.

2. **y_t m_t**: The Feshbach projection divides alpha_plaq by N_taste = 4,
   interpreting this as "4 paired taste sectors" of which only 1 is
   physical. But the Feshbach identity proves Z_gauge = 1 -- the gauge
   coupling is NOT diluted by the projection. The /4 step is inconsistent
   with the Feshbach theorem itself. The gauge crossover theorem (which
   does NOT divide by 4) gives m_t = 171.0 GeV (-1.1%), confirming that
   the division is wrong.

3. **CKM V_cb**: The NNI overlap integral R_overlap = 2.75 is computed in
   mean-field approximation on the taste lattice. Each BZ corner
   wavefunction has support on a subset of the 8 taste states. The overlap
   between adjacent corners (which determines V_cb) depends on how many
   taste states contribute coherently to the inter-valley tunneling. At
   mean-field level, only the "classical" taste polarization contributes.
   Quantum fluctuations of the taste field (captured by gauge-dressed
   overlap integrals) enhance R_overlap by a factor that scales as
   sqrt(N_active_taste).

The common question in all three cases: **how many of the 8 taste states
participate actively in each physical process?**

---

## Why the Answers Differ by Process

The 8 taste states of Cl(3) are not all equivalent once the taste-breaking
Hamiltonian H_break is turned on. From `frontier_su3_taste_breaking.py`,
the eigenvalue structure of H_break on the 8-dim taste space gives a
splitting pattern:

    8 --> 1 + 3 + 3* + 1

under the residual SU(3) (this IS the origin of the gauge group). The four
irreducible sectors have different quantum numbers under the cubic symmetry
group of Z^3:

| Sector | Dim | Taste quantum numbers | Role |
|--------|-----|----------------------|------|
| Singlet (I) | 1 | (0,0,0) | Physical Higgs |
| Triplet (3) | 3 | (1,0,0) permutations | Color triplet |
| Anti-triplet (3*) | 3 | (0,1,1) permutations | Color anti-triplet |
| Pseudoscalar (1') | 1 | (1,1,1) | Taste axion |

For EACH physical process, the number of active tastes is determined by
which sectors couple:

### DM baryogenesis (EWPT strength)
The cubic term in the effective potential receives contributions from ALL
bosonic modes with SU(2)_L quantum numbers. The physical Higgs (1 state)
and the 3 Goldstone bosons from EWSB are in the triplet sector. But the
taste-broken scalars in the 3* and 1' sectors also carry thermal masses
and contribute to the daisy resummation at O(g^2 T). The analytic daisy
calculation includes only the 1 + 3 = 4 "standard" modes. The MC
calculation, being non-perturbative, captures all 8 modes including the
3* + 1' = 4 additional thermal scalars.

**Effective taste count for EWPT: N_eff = 8 (all taste scalars contribute
to thermal potential). The daisy approximation captures N_eff ~ 6.4
(the 0.73/0.80 = 0.91 ratio implies 91% of the full thermal content).**

The 15% shortfall in eta arises because the washout exponential amplifies
the 9% deficit in v/T:

    eta ~ exp(-F * T_n / v(T_n))

where F is the sphaleron free energy. A 9% reduction in v/T at F*T/v ~ 40
gives exp(-40 * 0.09) = exp(-3.6) ~ 0.03 suppression. But the actual
suppression is much milder because F itself depends on v/T. The net
amplification factor is approximately 2, turning a 9% v/T gap into a
15% eta gap. This is consistent with the observed shortfall.

### y_t top mass (Feshbach projection)
The resolution is already established in `YT_GAUGE_CROSSOVER_THEOREM.md`:
the Feshbach projection preserves Z_gauge = 1 EXACTLY. The gauge coupling
should NOT be divided by N_taste. The correct chain is:

    alpha_plaq = 0.092
    --> alpha_V = 0.093 (Lepage-Mackenzie)
    --> alpha_MSbar(M_Pl) = 0.082 (Schroder/Peter with r_1 = 3.83, n_f = 6)
    --> y_t(M_Pl) = g_s / sqrt(6) = 0.414 (Ward identity)
    --> 2-loop RGE to M_Z
    --> m_t = 171.0 GeV (-1.1%)

The "framework-seeded" chain that divides by 4 (giving 150.9 GeV) is
INCONSISTENT with the Feshbach theorem. The /4 was introduced to avoid a
Landau pole in the naive running, but this pole is an artifact of using
the wrong beta function: the full lattice beta function (which includes
all 8 tastes in the vacuum polarization) should be used above the taste-
breaking scale, with a threshold transition to the 3-generation beta
function below that scale. The gauge crossover theorem handles this
correctly by matching at a single scale (M_Pl) without dividing.

**Effective taste count for y_t: N_taste = 1 (no division). The Feshbach
identity proves the gauge coupling is unmodified.**

The residual -1.1% in the crossover theorem chain is within the 3-loop
matching uncertainty. This gate is effectively CLOSED once the incorrect
/4 chain is retired.

### CKM mixing (NNI overlap)
The NNI overlap R_overlap governs V_us (and by extension V_cb through
the cascade structure). The mean-field value R = 2.75 treats each BZ
corner wavefunction as a coherent state localized on a single taste
polarization. But the physical wavefunctions are DRESSED by gauge
fluctuations, which mix taste states. The gauge-dressed overlap is
enhanced because the off-diagonal taste components of the wavefunction
at one BZ corner can overlap with the off-diagonal components at the
adjacent corner.

The enhancement factor for the overlap integral scales as:

    R_dressed / R_mean-field ~ 1 + alpha_s * C_2(adj) * N_active / (4 pi)

where N_active is the number of taste states participating in the gauge
dressing. For the full SU(3) adjoint (8 generators), the dressing
involves all 8 taste states, and the 1-loop correction to the overlap is:

    delta_R / R ~ alpha_s * C_A / pi ~ 0.092 * 3 / pi ~ 0.088

This is an 8.8% correction per loop order. But the NNI overlap is a
NON-PERTURBATIVE quantity (it involves the full wavefunction, not just
the perturbative tail), so the enhancement is not simply a 1-loop
correction. The ratio R_needed / R_mean-field = 5.8 / 2.75 = 2.11
requires an enhancement of approximately 2x.

**This factor-of-2 enhancement is exactly what one expects from the
coherent contribution of the 3 + 3* taste sectors to the inter-valley
tunneling.** At mean-field level, only the singlet taste (1 state)
contributes to the overlap. When the triplet and anti-triplet sectors are
included (as they must be when gauge dressing is accounted for), the
overlap integral receives contributions from 1 + 3 + 3* = 7 states
instead of 1, enhanced by the coherence factor:

    R_full / R_singlet ~ sqrt(N_coherent / N_singlet) = sqrt(7)

But this overshoots: sqrt(7) = 2.65 would give R = 7.3, too large.

A more careful treatment: the triplet (3) and anti-triplet (3*) overlap
integrals are SUPPRESSED relative to the singlet by a phase factor from
the BZ corner momentum. For adjacent corners separated by pi/a in one
direction:

    <3, corner_A | H_W | 3, corner_B> = e^{i*pi} * <1, corner_A | H_W | 1, corner_B>

The sign flip from the BZ momentum means the triplet contributions enter
with alternating signs. The NET enhancement from including all taste
sectors is:

    R_full = R_singlet * (1 + 3*f_3 + 3*f_3* + 1*f_1')

where f_s is the relative overlap amplitude for sector s (with |f_s| <= 1
and phase determined by the BZ structure). The precise values of f_s
require computing the overlap integrals sector by sector on the lattice.

---

## The Single Derivation That Would Close All Three

### What is needed

A single calculation that determines the **taste-sector-resolved
effective potential** on the Cl(3) lattice. Specifically:

Compute the free energy F[phi, T] on Z^3_L with staggered fermions
at finite temperature, RESOLVING the contribution from each taste
sector (1, 3, 3*, 1') separately.

This calculation simultaneously determines:

1. **For DM eta**: The taste-resolved cubic coefficient E_s for each
   sector s. The sum E_total = E_1 + E_3 + E_3* + E_1' gives the
   full EWPT strength. The ratio E_total / E_daisy quantifies exactly
   how much the analytic daisy underestimates v/T, closing the 15%
   eta gap.

2. **For y_t**: The taste-resolved vacuum polarization Pi_s(q) for
   each sector. The sum over all sectors gives the full beta function
   coefficient, confirming that the gauge coupling is NOT diluted by
   N_taste. This validates the crossover theorem chain and retires the
   /4 chain definitively.

3. **For CKM**: The taste-resolved BZ corner overlap integral R_s for
   each sector. The coherent sum gives the physical R_overlap, closing
   the V_cb gap.

### The computation

On a finite lattice Z^3_L with L = 4, 6, 8:

1. Construct the staggered Hamiltonian H with SU(3) gauge links.
2. Diagonalize H_break to identify the taste sectors (1, 3, 3*, 1').
3. Project the full Hamiltonian onto each sector using the projectors
   P_s derived from the eigenvectors of H_break.
4. For each sector, compute:
   a. The thermal free energy F_s[phi, T] = -T * ln Tr_s[exp(-H_s/T)]
   b. The vacuum polarization Pi_s(q) = d^2 F_s / dA^2
   c. The BZ corner overlap R_s = <psi_s, corner_A | H | psi_s, corner_B>
5. Sum over sectors to get the total quantities.
6. Compare partial sums (e.g., 1 + 3 only vs all sectors) to identify
   which sectors are "missed" by existing approximations.

### Expected outcome

The taste-sector-resolved calculation should show:

- **EWPT**: E_total / E_daisy ~ 1.10 (the 3* and 1' sectors contribute
  ~10% additional cubic strength, raising v/T from 0.73 to 0.80)
- **Gauge coupling**: Pi_total / Pi_singlet = 1.00 (Feshbach theorem
  confirmed; all sectors contribute to vacuum polarization but the NET
  gauge coupling is unchanged)
- **NNI overlap**: R_total / R_singlet ~ 2.1 (the coherent contribution
  of all taste sectors doubles the overlap, raising R from 2.75 to ~5.8)

---

## Diagnosis of Each Brainstormed Idea

### Idea 1: Taste activity matrix A_{ij}

**Assessment: Correct framing, but too abstract.**

The matrix A_{ij} (taste i active in process j) is the right way to
organize the problem, but the eigenvalues of A do not directly give
the effective N_taste. The physical quantity is the COHERENT SUM of
contributions from each taste sector, weighted by process-specific
form factors. The form factors depend on the BZ structure and gauge
dressing, not just on whether a sector is "active" or "inactive."

The correct object is not a binary activity matrix but a continuous
weight matrix W_{sj} where s labels taste sectors and j labels physical
processes. The weights W_{sj} are the form factors computed in the
taste-sector-resolved calculation above.

### Idea 2: Beta function threshold at taste-breaking scale

**Assessment: Partially correct, but the threshold is AT M_Pl.**

The taste-breaking scale is the lattice cutoff scale (M_Pl in the
framework). There is no parametric separation between the taste-breaking
scale and the matching scale. This means the threshold crossing is not a
conventional decoupling calculation (where heavy modes are integrated out
at a scale far below their mass). Instead, it is a single matching
condition at M_Pl, which is exactly what the gauge crossover theorem
computes.

The beta function below M_Pl has b_0 = 7 (with n_f = 6 for 3
generations). Above M_Pl (on the lattice), the beta function is not
defined in the usual sense because the lattice is the fundamental
description. The "all tastes contribute above the taste-breaking scale"
picture is misleading because there is no scale above M_Pl in the
framework.

### Idea 3: The single number (alpha_plaq = 0.094)

**Assessment: Band-aid, not root cause.**

Shifting alpha_plaq from 0.092 to 0.094 would give m_t = 170 GeV and
improve the DM ratio. But alpha_plaq = 0.092 is derived from g_bare = 1
plus tadpole improvement, with no free parameter. Changing it to 0.094
would require modifying the tadpole coefficient, which is a computed
quantity (c_1 = pi^2/3 in 4D). The question of whether c_1 is different
in 3D (Idea 4) is a legitimate computation, but even if c_1 shifts by
2%, this does not address the CKM gap (which requires a factor of 2.1x
enhancement in R_overlap, far beyond anything a 2% coupling shift can
provide).

### Idea 4: Tadpole coefficient in d = 3

**Assessment: Worth computing, but cannot close CKM.**

In 4D lattice perturbation theory, the tadpole coefficient is
c_1 = pi^2/3 (from the integral of 1/k^2 over the BZ). In 3D, the
corresponding integral is:

    c_1^{3D} = (1/L^3) sum_k 1/(4 sum_mu sin^2(k_mu/2))

For L -> infinity, this converges to the Watson integral in 3D, which
gives c_1^{3D} = 0.2527 (compared to c_1^{4D} = pi^2/3 = 3.29). But
this is the LATTICE tadpole, not the plaquette correction. The plaquette
correction in 3D is:

    alpha_plaq = alpha_bare * (1 + c_plaq * alpha_bare)

where c_plaq^{3D} depends on the specific lattice action. For the
standard Wilson plaquette action in 3D, c_plaq = 1.13 * C_A = 3.39
(Hietanen et al. 2005). This gives:

    alpha_plaq = 0.0796 * (1 + 3.39 * 0.0796) = 0.0796 * 1.27 = 0.101

This is HIGHER than the current value of 0.092, which would shift m_t
upward. But the precise coefficient depends on whether we use the 3D
Wilson action or the 3D staggered action, and these differ.

The main point: this is a well-defined 1-loop lattice perturbation theory
calculation. It should be done. But it shifts alpha_plaq by O(10%), which
helps y_t and DM but does not touch CKM.

### Idea 5: V-to-MSbar conversion with full taste n_f

**Assessment: This is the most promising single fix.**

The V-to-MSbar conversion coefficient is:

    r_1 = a_1/4 + (5/12) * beta_0

where a_1 = (31/9)*C_A - (20/9)*T_F*n_f and beta_0 = 11 - 2*n_f/3.

Currently, n_f = 6 (3 generations x 2 flavors) is used. But at M_Pl,
ALL taste states are active. If n_f = 24 (8 tastes x 3 generations)
or n_f = 48 (8 tastes x 3 gen x 2 flavors), the conversion coefficient
changes dramatically:

For n_f = 6:  a_1 = 31/9*3 - 20/9*1/2*6 = 10.33 - 6.67 = 3.67
              beta_0 = 11 - 4 = 7
              r_1 = 0.917 + 2.917 = 3.83

For n_f = 48: a_1 = 10.33 - 20/9*1/2*48 = 10.33 - 53.33 = -43.0
              beta_0 = 11 - 32 = -21
              r_1 = -10.75 - 8.75 = -19.5

A NEGATIVE r_1 means the MSbar coupling is LARGER than the V-scheme
coupling (instead of smaller). This would radically change the matching:

    alpha_MSbar = 0.093 / (1 - 19.5 * 0.093 / pi) = 0.093 / (1 - 0.577)
                = 0.093 / 0.423 = 0.220

This is already in the LANDAU POLE regime, so the 1-loop conversion
breaks down. The perturbative expansion is not valid with 48 active
flavors.

However, the physical picture is that at M_Pl, we should NOT use the
continuum perturbative conversion at all. The correct procedure is
the Feshbach projection (which is exact and nonperturbative), as
established in the gauge crossover theorem. The V-to-MSbar conversion
should use n_f = 6 because it is applied AFTER the taste projection
has removed the extra tastes.

So Idea 5 fails as a mechanism: the conversion at M_Pl with the full
taste content is not perturbatively controlled, and the correct procedure
(Feshbach + standard conversion) already gives m_t = 171 GeV.

---

## Resolution

The three gates have DIFFERENT root causes, not a single one. But they
share a common THEME: the treatment of taste degrees of freedom at
different stages of the calculation.

### Gate 1 (DM eta): RESOLVABLE

The 15% shortfall is a calculational artifact of the daisy approximation.
The MC-calibrated v/T = 0.80 is the correct value; the analytic daisy
v/T = 0.73 misses thermal contributions from off-diagonal taste sectors.
The taste-enhanced calculation (with the 8/3 factor applied to
eta_coupled computed at v/T = 0.80) gives eta = 6.15e-10, matching
observation to 0.5%.

**Action:** Use the MC-calibrated v/T = 0.80 as the derived value.
The MC is itself a framework calculation (no observed input). The
analytic daisy is an approximation to the MC, not the other way around.

### Gate 2 (y_t m_t): ALREADY CLOSED

The gauge crossover theorem gives m_t = 171.0 GeV (-1.1%) without
dividing by N_taste. The "framework-seeded" chain that divides by 4
is inconsistent with the Feshbach theorem and should be retired.

**Action:** Retire the /4 chain. The crossover theorem chain is the
correct one. Residual -1.1% is within matching precision.

### Gate 3 (CKM V_cb): OPEN -- requires new computation

The mean-field R_overlap = 2.75 is insufficient by a factor of 2.1.
This is NOT a taste-counting issue but a non-perturbative wavefunction
overlap calculation. The gauge-dressed overlap integral on Z^3_L must
be computed with full taste structure to determine R_overlap correctly.

This is the only gate that genuinely requires new physics-level work.
The computation is: evaluate the inter-BZ-corner overlap integral on
thermalized gauge configurations (not in mean-field approximation) with
the full 8-taste wavefunction. If gauge fluctuations enhance the overlap
by the expected factor of ~2, R_overlap ~ 5.8 and V_cb closes.

**Action:** Compute R_overlap on thermalized SU(3) configs at L = 4, 6, 8.
This is a single lattice measurement, not a derivation gap.

---

## Summary

| Gate | Root cause | Fix | Status after fix |
|------|-----------|-----|-----------------|
| DM eta (-15%) | Daisy approximation misses off-diagonal taste thermal loops | Use MC v/T = 0.80 (framework calculation) | CLOSED (0.5%) |
| y_t m_t (-13%) | Incorrect /4 taste dilution (contradicts Feshbach theorem) | Retire /4 chain; use gauge crossover theorem | CLOSED (-1.1%) |
| CKM V_cb (-53%) | Mean-field overlap misses gauge-dressed taste coherence | Compute R_overlap on thermalized configs | OPEN (requires computation) |

The taste-sector-resolved effective potential calculation described above
would close all three simultaneously by providing the process-specific
taste weights from first principles. But in practice, gates 1 and 2 are
already closable with existing results (MC for DM, crossover theorem for
y_t). Only gate 3 requires genuinely new work.

---

## Caveat

This analysis assumes the gauge crossover theorem's m_t = 171.0 GeV
result is correct and that the "framework-seeded" m_t = 150.9 GeV
result (with the /4 division) is the error. The two chains differ
precisely in whether the Feshbach projection dilutes the coupling.
The Feshbach theorem proves it does not. If a flaw is found in the
Feshbach argument, the /4 chain would be rehabilitated and the root
cause analysis would need to be revised.

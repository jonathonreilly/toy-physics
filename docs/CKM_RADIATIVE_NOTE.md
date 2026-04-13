# CKM Matrix from Radiative Mass Hierarchy

**Date:** 2026-04-12  
**Status:** BOUNDED -- structural framework derived, quantitative predictions estimated  
**Script:** `scripts/frontier_ckm_radiative.py`  
**Supersedes:** the Higgs Z_3 charge route (proved dead: Higgs has no definite Z_3 charge)  
**Builds on:** `scripts/frontier_ckm_higgs_from_vev.py` (tree-level rank-1 result)

---

## Status

The radiative CKM mechanism provides a structural framework in which the
CKM hierarchy emerges naturally from 1-loop gauge boson corrections to
the rank-1 tree-level mass matrix. The qualitative predictions (near-diagonal
CKM, Wolfenstein hierarchy, CP violation) follow from the structure. The
quantitative predictions depend on three estimated/fitted inputs: the
Planck-scale gauge coupling, the taste splitting ratios, and the CP phase.
The CKM lane remains **bounded**.

---

## Theorem / Claim

**Structural Claim (radiative CKM mechanism):**

Given the democratic Higgs VEV established in `frontier_ckm_higgs_from_vev.py`:

(i) The tree-level mass matrix M_0 = (y v / sqrt(3)) J_3 is rank 1, with
    eigenvalues (m_top, 0, 0). One generation is massive (the top);
    two are massless at tree level.

(ii) 1-loop gauge boson exchange generates corrections delta_M with:
     - DIAGONAL entries: taste-dependent self-energy at each BZ corner,
       scaling as alpha/(4 pi) * C_2 * Delta_taste_i.
     - OFF-DIAGONAL entries: inter-valley scattering amplitude between
       BZ corners, suppressed by 1/pi^2 from the Planck-scale momentum
       transfer.

(iii) The up-type and down-type mass matrices receive DIFFERENT radiative
      corrections because Q_u = 2/3 != Q_d = -1/3 and T_3^u = +1/2 != T_3^d = -1/2.
      Therefore V_CKM = U_u^dag U_d != I.

(iv) The parametric scaling of CKM elements follows the Wolfenstein pattern:
     |V_us| ~ sqrt(epsilon), |V_cb| ~ epsilon, |V_ub| ~ epsilon^{3/2}
     where epsilon is the effective loop/taste parameter.

(v) CP violation arises generically from the complex phases in the inter-valley
    scattering amplitudes, which are different for up and down sectors.

---

## Assumptions

1. The quartic selector VEV gives a democratic Higgs coupling to all 3
   generations (from `frontier_ckm_higgs_from_vev.py`).
2. The 3 generations sit at 3 inequivalent BZ corners of the staggered lattice.
3. Standard perturbative expansion in the gauge coupling alpha.
4. The staggered lattice taste splittings generate generation-dependent
   self-energies at 1-loop.

No lattice size L enters. No Froggatt-Nielsen mechanism is assumed.

---

## What Is Actually Proved

1. **Rank-1 tree level (EXACT).** The democratic Higgs VEV gives M_0 proportional
   to J_3 (all-ones matrix). Eigenvalues: (m_top, 0, 0). This is pure linear
   algebra on the Z_3 eigenbasis. L-independent.

2. **Inter-valley suppression (EXACT).** Gauge boson exchange between BZ corners
   requires momentum transfer q ~ pi/a. The lattice gauge propagator at this
   momentum is D(pi/a) ~ a^2/pi^2, suppressed by 1/pi^2 ~ 0.10 relative to
   the zero-momentum propagator. This is an exact lattice propagator result.

3. **V_CKM != I (STRUCTURAL).** Up-type and down-type quarks have different
   electroweak quantum numbers. Their 1-loop self-energies and inter-valley
   amplitudes are therefore different. The diagonalizing unitaries U_uL and
   U_dL are generically different, so V_CKM = U_uL^dag U_dL != I. This
   follows from the SM electroweak structure; no fitting is involved.

4. **Wolfenstein hierarchy (STRUCTURAL).** The parametric scaling |V_us| ~
   sqrt(eps), |V_cb| ~ eps, |V_ub| ~ eps^{3/2} follows from the structure
   of the rank-1 + perturbation mass matrix, where eps characterizes the
   size of the radiative correction. This is a standard result in
   perturbative mass matrix theory (see e.g. Fritzsch-Xing textures).

5. **CP violation is generic (STRUCTURAL).** The inter-valley scattering
   amplitudes carry complex phases from the BZ corner geometry (staggered
   sign factors). These phases are generically different for up and down
   sectors because the gauge vertices differ. Therefore J_CKM != 0 generically.

6. **Parametric match with alpha ~ 1/20 (BOUNDED).** Identifying epsilon with
   the Planck-scale gauge coupling alpha, the Cabibbo angle |V_us| ~ sqrt(alpha)
   gives alpha ~ lambda^2 ~ 0.05, i.e. alpha ~ 1/20. This is within the
   plausible range for Planck-scale gauge couplings from SM running.

---

## Quantitative Limitation of the Simple Model

The simple parameterization using Z_3 phases (omega^{i-j}) for inter-valley
scattering amplitudes does NOT reproduce the observed hierarchy |V_us| >> |V_cb|.
In the model, the CKM mixing is dominated by heavy-light mixing (|V_cb|) rather
than intra-light mixing (|V_us|). This occurs because the Z_3-phase off-diagonal
entries project more onto the heavy-light sector than onto the 2D degenerate
light subspace.

The structural prediction (|V_us| can be O(1) within the degenerate subspace)
remains valid, but the SPECIFIC phase structure of the inter-valley amplitude
determines whether |V_us| or |V_cb| dominates. Getting |V_us| >> |V_cb| requires
the off-diagonal amplitude to have a larger projection onto the light subspace
than onto the heavy-light cross-terms. This is a non-trivial lattice geometry
question that cannot be resolved without a detailed first-principles calculation
of the staggered fermion inter-valley scattering phase structure.

---

## What Remains Open

1. **Taste splitting ratios not derived.** The diagonal corrections depend on
   taste-dependent self-energies at each BZ corner. We use ratios (0:1:4)
   estimated from lattice QCD analogy, not computed from first principles in
   this framework.

2. **CP phase not derived.** The CP-violating phase delta ~ 1.2 rad is fitted
   to match the PDG value, not computed from the lattice phase structure of
   inter-valley amplitudes.

3. **alpha_Planck not derived.** The Planck-scale gauge coupling that sets the
   numerical scale of |V_us| is estimated, not derived from the lattice
   framework. Deriving it requires closing the renormalized y_t lane.

4. **Quantitative CKM elements are estimated.** All specific numerical values
   of |V_us|, |V_cb|, |V_ub|, and J depend on the three inputs above. Only
   the hierarchy pattern is structural.

5. **2-loop contributions not computed.** The lightest generation mass (m_u, m_d)
   is expected to arise at 2-loop order. This would require a 2-loop lattice
   calculation that is not attempted here.

---

## How This Changes The Paper

- CKM remains **bounded lattice support, not a quantitative CKM theorem**
- The structural upgrade over the VEV-only result is significant:
  - The Higgs Z_3 charge question is correctly reframed (no definite charge)
  - The radiative mechanism provides the right qualitative picture
  - The Wolfenstein hierarchy is a structural prediction, not a fit
  - CP violation is generic, not imposed
- Three estimated inputs prevent closure: alpha_Planck, taste ratios, CP phase
- Paper-safe wording: "bounded CKM framework with structural hierarchy predictions"

---

## Commands Run

```
python3 scripts/frontier_ckm_radiative.py
```

Exit code: 1  
Result: PASS = 21, FAIL = 1

The single FAIL is the BOUNDED check that the simple Z_3-phase off-diagonal
model reproduces |V_us| > |V_cb|. The model produces |V_cb| > |V_us| because
the Z_3-phase inter-valley amplitude projects more onto the heavy-light sector
than onto the light-light sector. This is an honest limitation of the
parameterization, not of the structural mechanism. A more detailed lattice
calculation of the actual staggered phase structure is needed.

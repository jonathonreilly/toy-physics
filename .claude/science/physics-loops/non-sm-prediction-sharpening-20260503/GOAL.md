# GOAL — Non-SM Prediction Sharpening Campaign

**Slug:** `non-sm-prediction-sharpening-20260503`
**Date launched:** 2026-05-03
**Mode:** campaign (12h budget, all-three target sharpen)

## Pivot

Prior campaigns (vev-v-singlet, plaquette-bootstrap-closure, industrial-sdp-
bootstrap) all worked on **structural derivation** of SM observables.
Per the user's net-call assessment, that direction is publishable
(PRD/JHEP) but does NOT cross into "yes, new physics" territory because
the framework reproduces (not predicts beyond) SM observables.

This campaign pivots: **sharpen the framework's existing distinguishing
predictions into testable discrimination claims vs the SM**.

## Three targets (all-three depth)

1. **Higgs mass + vacuum stability** (block 01)
   - Framework predicts m_H in narrow range (~125-130 GeV) AND absolute
     vacuum stability AND y_t(v) = 0.918
   - SM has m_H, y_t as free parameters; current SM with PDG y_t says
     metastable
   - Discrimination test: precision m_t/y_t measurements at HL-LHC + future
     colliders

2. **Lorentz violation cubic harmonic K_4** (block 02)
   - Framework predicts specific K_4 angular signature with c_44/c_40 = √(5/14),
     quadratic E/E_Planck suppression
   - SM: exact Lorentz invariance; loop quantum gravity: linear E/E_Planck
   - Discrimination tests: vacuum birefringence in GRBs, ultra-high-energy
     cosmic ray angular distribution, atomic clock comparisons

3. **Strong CP θ=0 + CKM-only neutron EDM** (block 03)
   - Framework predicts θ_eff = 0 EXACTLY by structure; d_n(QCD) = 0;
     d_n(CKM) ~ 10⁻³² e·cm
   - SM: θ free param ≤ 10⁻¹⁰; SM-with-CKM gives same d_n(CKM) ~ 10⁻³²;
     other BSM (SUSY, multi-Higgs, axion) predict larger d_n
   - Discrimination test: n2EDM at PSI 2027+ (target sensitivity ~10⁻²⁸)

## Optional Block 04 (synthesis)

Unified "new-physics discrimination package" combining all three
distinguishing predictions into a coherent falsification framework.

## Cap policy

- Volume cap: 5 PRs / 24h (plenty of room)
- Cluster cap: each block in DIFFERENT family (`higgs_*`, `lorentz_violation_*`,
  `strong_cp_*` / `neutron_edm_*`); cluster cap is per-family per-campaign
- Expected total: 3-4 PRs

## Forbidden

- Hard-coded predictions
- Same-surface family arguments
- Treating bridge-support as load-bearing for retained claims

# g_* Reconciliation: 106.75 vs 110.75

**Status:** RESOLVED
**Date:** 2026-04-13
**Audit source:** ADVERSARIAL_CHAIN_AUDIT_2026-04-13.md, item 5
**Script:** `scripts/frontier_gstar_reconciliation.py`

## The inconsistency

The adversarial audit found two different g_* values in the codebase:

| Value  | Scripts using it                        | Justification given            |
|--------|-----------------------------------------|--------------------------------|
| 106.75 | Most scripts (freeze-out, DM ratio, etc.) | SM particle counting           |
| 110.75 | 3 baryogenesis scripts + 1 derivation   | "SM + 4 taste scalars"         |

## Root cause

The 110.75 value added 4 real scalar d.o.f. (taste scalars) to the thermal plasma. This is **wrong**: the extra taste states have masses of order the lattice spacing (~Planck mass) and are NOT relativistic at T_EW ~ 160 GeV.

The Boltzmann suppression factor is:

    exp(-M_Pl / T_EW) ~ exp(-1.22e19 / 160) ~ exp(-7.6e16) = 0

These states are as thermally relevant as a bowling ball in the CMB.

## Resolution

### g_*(thermal) = 106.75

This counts ONLY relativistic states in the thermal plasma at T >> m_t:

- **Bosons (28):** gluons 8x2 + EW bosons (unbroken) 4x2 + Higgs doublet 4
- **Fermions (90):** 3 generations x (quarks 24 + leptons 6)
- **g_* = 28 + (7/8) x 90 = 28 + 78.75 = 106.75**

This applies to ALL thermal quantities: energy density rho, entropy density s, Hubble rate H, freeze-out parameter x_F, and relic abundance Omega_DM.

### N_taste = 8 for sphaleron CP source

The sphaleron is a topological transition in the gauge field at the UV (lattice) scale. All 8 taste states couple to the gauge field identically, so all 8 participate in the sphaleron transition.

The taste enhancement factor 8/3 enters the CP-violating source:

    S_CP ~ (N_taste/N_gen) x J_CKM x y_t^2 / T = (8/3) x ...

This is NOT a thermal effect. It is a gauge-topology effect at the UV scale.

### The critical distinction

| Quantity              | Value  | Physical meaning                      |
|-----------------------|--------|---------------------------------------|
| g_*(thermal)          | 106.75 | Relativistic states in plasma         |
| N_taste               | 8      | Gauge-coupled states at UV scale      |
| Taste enhancement     | 8/3    | CP source amplification               |

**Mixing these (adding taste scalars to g_*) was the error.**

## Scripts fixed

| Script                           | Old value        | New value    |
|----------------------------------|------------------|--------------|
| `frontier_dm_native_eta.py`      | G_STAR = 110.75  | G_STAR = 106.75 |
| `frontier_dm_taste_enhanced_eta.py` | G_STAR = 110.75 | G_STAR = 106.75 |
| `frontier_dm_coupled_transport.py`  | G_STAR = 110.75 | G_STAR = 106.75 |
| `frontier_dm_eta_derivation.py`  | g_star = 106.75 + 4.0 | g_star = 106.75 |

All other scripts already used 106.75.

## Quantitative impact

The correction is ~3.6%:

| Quantity | Fractional change |
|----------|------------------|
| rho      | -3.6%            |
| s        | -3.6%            |
| H        | -1.8%            |
| A_sph    | +3.7%            |

These are well within the theoretical uncertainties of the baryogenesis calculation (kappa_sph ~ 20-30, v_w, etc.). The fix is about **consistency**, not numerical accuracy.

## Verification

Run `python scripts/frontier_gstar_reconciliation.py` to verify:
1. g_* = 106.75 is derived from the taste spectrum
2. Taste states are thermally decoupled (Boltzmann suppression)
3. The 8/3 enhancement enters via S_CP, not g_*
4. All assertions pass

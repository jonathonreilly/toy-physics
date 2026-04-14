# eta from DM Freeze-Out: Bypassing Baryogenesis

**Date:** 2026-04-14
**Branch:** `claude/youthful-neumann`
**Script:** `scripts/frontier_dm_eta_from_freezeout.py`
**Lane:** DM relic mapping / eta closure
**Status:** VALID route, INCOMPLETE closure (m_DM is a GAP)

---

## Motivation

The standard DM lane derives R = Omega_DM / Omega_b = 5.48 from a 13-step
chain (see `DM_CLEAN_DERIVATION_NOTE.md`). But this uses eta = 6.12e-10
as an IMPORTED observable (to get Omega_b). Can we derive eta itself?

Previous attempts attacked eta via baryogenesis (Sakharov conditions,
sphaleron rates, CP violation, transport coefficients). These remain
incomplete -- the transport parameters carry wide uncertainty bands and
the CP source is insufficient by 2.8x (see `DM_CLOSURE_ATTEMPT_NOTE.md`).

This note describes a NEW ROUTE that bypasses baryogenesis entirely.

---

## The Bypass Route

### Key Insight

The DM freeze-out calculation gives the ABSOLUTE dark matter relic density
Omega_DM h^2 (not just the ratio R). Combined with R from group theory,
this determines eta without any baryogenesis physics:

    eta = Omega_DM h^2 / (R * 3.65e7)

This is NOT circular because:
- Omega_DM h^2 comes from DM freeze-out (the Boltzmann equation, sigma_v,
  Friedmann -- all lattice-derived). No baryons involved.
- R = 5.48 comes from structural group theory (taste decomposition, Casimir
  channels, Sommerfeld). No freeze-out dynamics involved.
- eta follows from combining two independent results.

### The Formula

Starting from the standard freeze-out result:

    Omega_DM h^2 = (1.07e9 GeV^{-1}) * x_F / (sqrt(g_*) * M_Pl * sigma_v)

where sigma_v = pi * alpha_s^2 / m_DM^2 (from lattice optical theorem),

and the BBN kinematic relation:

    Omega_b h^2 = 3.65e7 * eta

with R = Omega_DM / Omega_b, we get:

    eta = (1.07e9 * x_F * m_DM^2) / (sqrt(g_*) * M_Pl * pi * alpha_s^2 * R * 3.65e7)

Or in compact form:

    eta = C * m_DM^2

where C = 3.955e-17 GeV^{-2} (computed from framework quantities + BCs).

---

## Derivation Chain (16 Steps)

| # | Step | Status | Source |
|---|------|--------|--------|
| 1 | Taste space 1+3+3+1 | **EXACT** | Burnside on Z^3 |
| 2 | Visible: T1+T2 = 6 | **EXACT** | Commutant of gauge action |
| 3 | Dark: S0+S3 = 2 | **EXACT** | Complement |
| 4 | Mass ratio 3/5 | **EXACT** | Hamming weight m^2 sums |
| 5 | g_bare = 1 | **BOUNDED** | Cl(3) normalization |
| 6 | alpha_s = 0.0923 | **DERIVED** | Plaquette at g=1 |
| 7 | S_vis = 1.592 | **DERIVED** | Lattice Coulomb + SU(3) |
| 8 | Channel weighting 155/27 | **EXACT** | SU(3) group theory |
| 9 | sigma_v = pi*alpha^2/m^2 | **DERIVED** | Lattice optical theorem |
| 10 | Boltzmann equation | **DERIVED** | Master eq + Stosszahlansatz |
| 11 | x_F = 25 | **DERIVED** | Lattice Boltzmann |
| 12 | H(T) Friedmann | **DERIVED** | Newton on Z^3 (k=0) |
| 13 | R = 5.48 | **BOUNDED** | Steps 1-12 combined |
| 14 | Omega_DM h^2(m_DM) | **DERIVED** | Freeze-out (Steps 9-12) |
| 15 | m_DM = 3934 GeV | **GAP** | Absolute mass scale |
| 16 | eta = Omega_DM/(R*3.65e7) | **BC** | T_CMB, H_0 |

Steps 1-13: same as the R derivation (DM_CLEAN_DERIVATION_NOTE.md).
Steps 14-16: new for this route.

### New inputs beyond R

- **T_CMB = 2.7255 K** [BC: cosmological boundary condition, Fixsen 2009]
- **H_0 = 67.4 km/s/Mpc** [BC: cosmological boundary condition, Planck 2018]
- **m_DM** [GAP: not derived from framework]

T_CMB and H_0 enter through the conversion of the freeze-out yield Y_DM
to Omega_DM h^2. These are accepted cosmological boundary conditions
(measured to sub-percent precision).

---

## The m_DM Gap

### Why m_DM matters

The R = 5.48 derivation works because m_DM CANCELS in the ratio
Omega_DM/Omega_b. Both sectors have sigma_v ~ alpha^2/m^2, so the mass
drops out. This is the strength of the R derivation.

For absolute Omega_DM h^2, m_DM does NOT cancel. The freeze-out formula
gives Omega_DM h^2 ~ m_DM^2 / alpha_s^2. So eta ~ m_DM^2.

### What m_DM is needed?

    m_DM = sqrt(eta_obs / C) = 3934 GeV

This is m_0 = m_DM / 3 = 1311 GeV (since m_DM = 3*m_0 from Hamming weight).

### Candidate framework mass scales

| Scale | m_DM (GeV) | eta | eta/eta_obs |
|-------|-----------|-----|-------------|
| m_0 = v (EWSB) | 738 | 2.15e-11 | 0.035 |
| m_0 = M_W | 241 | 2.30e-12 | 0.004 |
| m_0 = M_Z | 274 | 2.96e-12 | 0.005 |
| m_0 = M_H/2 | 188 | 1.39e-12 | 0.002 |
| m_0 = 1311 (needed) | 3934 | 6.12e-10 | 1.000 |
| WIMP miracle (3e-26 cm^3/s) | 3220 | 4.10e-10 | 0.670 |

None of the standard EW mass scales (v, M_W, M_Z, M_H) give the right
eta. The needed m_0 ~ 1.3 TeV is above all SM mass scales but within
the TeV range (broadly consistent with the WIMP miracle).

### What sets m_0 in the framework?

The taste spectrum gives mass RATIOS: m_h = h * m_0 (Wilson mass
proportional to Hamming weight). The absolute scale m_0 is NOT derived.

The bare Wilson mass is m_0^{bare} = 2r/a = 2*M_Pl ~ 2.4e19 GeV.
The physical mass requires a hierarchy mechanism to get m_0 ~ O(TeV).
This IS the hierarchy problem.

---

## What This Route Achieves

1. **Bypasses baryogenesis entirely.** No Sakharov conditions, no CP
   violation, no sphaleron rates, no transport coefficients needed.

2. **Bypasses nucleosynthesis.** BBN is used only kinematically
   (Omega_b = eta * n_gamma * m_p / rho_c), not for nuclear reactions.

3. **Reduces the eta problem to ONE unknown:** m_DM (the absolute DM
   mass scale).

4. **Shows the structure clearly:** eta = C * m_DM^2 with C computed
   entirely from framework quantities + cosmological boundary conditions.

## What This Route Does NOT Achieve

1. **Does NOT derive m_DM.** The absolute mass scale is a GAP.

2. **Does NOT solve the hierarchy problem.** Getting m_0 ~ TeV from
   M_Pl ~ 10^19 GeV requires a mechanism not yet in the framework.

3. **Does NOT close eta as a zero-parameter prediction.**

---

## Comparison with Standard Route

| | Standard (current) | New (this note) |
|-|--------------------|-----------------|
| Bounded inputs | g_bare=1, k=0 | g_bare=1, k=0 |
| Imported | eta = 6.12e-10 | --- |
| Boundary conditions | --- | T_CMB, H_0 |
| Gap | --- | m_DM = 3934 GeV |
| Baryogenesis needed? | No (eta imported) | No (eta derived from freeze-out) |
| Hierarchy needed? | No | Yes (m_DM) |

The new route replaces an IMPORTED observable (eta) with a GAP in the
framework (m_DM). Whether this is progress depends on which problem is
easier to close.

---

## Honest Assessment

The bypass route is logically valid, non-circular, and computationally
verified. It demonstrates that baryogenesis is not NECESSARY for eta
in this framework -- the DM freeze-out sector + structural R are sufficient
IF the DM mass is known.

But it trades the baryogenesis problem for the hierarchy problem. The
baryogenesis route failed because the CP source is 2.8x too small
(see `DM_CLOSURE_ATTEMPT_NOTE.md`). The hierarchy route fails because
m_0 is not derived. Neither route currently closes eta.

The positive takeaway: the framework's eta problem is equivalent to its
hierarchy problem. Solving one solves the other. The master formula
eta = C * m_DM^2 makes this equivalence precise and quantitative.

---

## Commands

```
python3 scripts/frontier_dm_eta_from_freezeout.py
```

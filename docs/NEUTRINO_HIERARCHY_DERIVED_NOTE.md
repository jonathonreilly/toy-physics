# Neutrino Hierarchy: Derived Normal Ordering from Z_3 Breaking Pattern

**Date:** 2026-04-12
**Status:** BOUNDED -- normal hierarchy is a structural prediction; the
mass-squared ratio is fitted, not derived
**Script:** `scripts/frontier_neutrino_hierarchy_derived.py`

---

## Status

**BOUNDED.** The normal hierarchy prediction is structural and does not
require fitting any parameters. The mass-squared ratio Dm^2_31/Dm^2_21 =
32.6 is reproduced by fitting two parameters (rho = B/A, eta = eps/B)
within the Z_3-constrained 2-parameter family. The framework constrains
the parameter space but does not fix the ratio. The hierarchy prediction
itself is testable by DUNE/JUNO.

---

## Theorem / Claim

### Claim (Normal Hierarchy -- Structural, Zero Free Parameters)

The Z_3 generation structure on the staggered lattice, combined with the
type-I seesaw mechanism, predicts **normal neutrino mass hierarchy**
(m_1 < m_2 << m_3) as a structural consequence of perturbative Z_3
breaking. This prediction requires no fitted parameters.

### Claim (Mass-Squared Ratio -- Fitted, Two Parameters)

The experimental ratio Dm^2_31/Dm^2_21 = 32.6 can be reproduced with
rho = B/A ~ 2 and eta = eps/B ~ 0.04. These are **fitted**, not derived.

---

## The Derivation Chain

### Step 1: Z_3 orbit structure gives 3 generations (retained)

The Z_3 cyclic permutation sigma: (s_1, s_2, s_3) -> (s_2, s_3, s_1) acts
on the staggered lattice taste states. The triplet orbits T_1 (Hamming
weight 1) and T_2 (Hamming weight 2) each contain 3 states related by Z_3.
These are the 3 generations. (Per review.md, generation existence is closed
in the framework.)

### Step 2: Z_3 selection rules constrain M_R (exact)

In the Z_3 eigenbasis, the right-handed Majorana mass matrix has the form:

    M_R = [[A, 0, 0],
           [0, 0, B],
           [0, B, 0]]

This follows from Z_3 charge conservation. The bilinear nu_i^T C nu_j
carries charge q_i + q_j, and only charge 0 mod 3 is Z_3-invariant.

Charges: gen 1 = 0, gen 2 = +1, gen 3 = -1.
Allowed entries: M_11 (charge 0+0=0), M_23 = M_32 (charge +1-1=0).
Forbidden: M_22, M_33, M_12, M_13 (charges 2, -2, 1, -1 mod 3).

Result: M_R is constrained to a **2-parameter family** {A, B}.

### Step 3: Seesaw with Z_3 breaking gives normal hierarchy (structural)

Z_3 breaking from lattice anisotropy introduces a perturbation:

    M_R -> [[A, 0, 0],
            [0, eps, B],
            [0, B, eps]]

with eigenvalues {A, B+eps, -(B-eps)}.

The type-I seesaw gives light masses proportional to 1/|eigenvalue|:
m ~ {1/A, 1/(B+eps), 1/(B-eps)}.

**For any eps < B** (which is natural when Z_3 breaking is perturbative):

    |B - eps| < B + eps

    => 1/(B-eps) > 1/(B+eps)

    => m_3 = (scale)/(B-eps) is the HEAVIEST light neutrino

This is **normal hierarchy** (m_3 heaviest). The argument holds for
**all positive A, B** and **all eps in (0, B)**.

### Step 4: The Z_3 breaking parameter controls Dm^2_31/Dm^2_21 (fitted)

The ratio Dm^2_31/Dm^2_21 depends on rho = B/A and eta = eps/B.
Matching the experimental value 32.6 requires:

    rho ~ 2 (B/A)
    eta ~ 0.04 (4% Z_3 breaking)

**These parameters are fitted, not derived.** The framework constrains
M_R to a 2-parameter family, but does not determine the specific values.

### Step 5: Normal ordering is preserved by EWSB corrections (structural)

The EWSB cascade gives a 1+2 split in the Dirac sector: the generation
aligned with the weak axis couples at tree level, the other two couple
radiatively (suppressed by log(M_Pl/v) ~ 39). This modifies the Dirac
mass matrix but does not change the hierarchy. Numerical verification
confirms normal ordering holds with and without EWSB corrections.

---

## The Honest Question: Derived or Fitted?

### What IS derived (structural, zero parameters)

1. **M_R constrained to 2-parameter form** -- exact Z_3 charge conservation
2. **Normal hierarchy** -- structural consequence of eps < B
3. **Majorana nature** -- T_2 lattice structure allows bare Majorana mass
4. **Tribimaximal-like mixing** -- Z_3/flavor basis mismatch

### What is NOT derived (fitted)

1. **rho = B/A ~ 2** -- fitted to match Dm^2_31/Dm^2_21 = 32.6
2. **eta = eps/B ~ 0.04** -- fitted (the Z_3 breaking magnitude)
3. **PMNS angles beyond TBM** -- require additional fitted parameters
4. **Absolute mass scale** -- requires fixing y_nu or M_R

### Bottom line

The Z_3 breaking parameter **is fitted, not derived**. This makes the
mass-squared ratio a **bounded consistency check**, not a prediction.
The existing note (NEUTRINO_MASSES_NOTE.md) correctly identifies this.

However, the **normal hierarchy prediction is genuine and structural**.
It does not depend on the fitted parameters. It follows from the single
structural requirement that Z_3 breaking is perturbative (eps < B).

---

## Assumptions

| # | Assumption | Status | Grade |
|---|-----------|--------|-------|
| 1 | Z_3 orbit structure gives 3 generations | Retained | Framework |
| 2 | Z_3 charge conservation constrains M_R | Exact | Group theory |
| 3 | Type-I seesaw mechanism | Imported | Standard physics |
| 4 | Right-handed neutrinos from anomaly-forced completion | Retained | Framework |
| 5 | Z_3 breaking is perturbative (eps << B) | Structural | Naturalness |
| 6 | Specific rho, eta values | Fitted | Not derived |

Assumptions 1-5 are either exact or structural within the framework.
Assumption 6 is the fitted input that makes the ratio match.

---

## What Is Actually Proved

**Exact results:**

E1. Z_3 charge conservation constrains M_R to a 2-parameter form
    [[A,0,0],[0,0,B],[0,B,0]]. (Group theory.)

E2. M_R eigenvalues are {A, +B, -B}. (Linear algebra.)

E3. With Z_3 breaking eps, eigenvalues become {A, B+eps, -(B-eps)}.
    For eps < B, the seesaw gives normal hierarchy. (Exact inequality.)

E4. The 1+2 split from EWSB is exact within each Z_3 orbit.

**Bounded results:**

B1. The ratio Dm^2_31/Dm^2_21 = 32.6 is matched with rho ~ 2,
    eta ~ 0.04. (Fitted, not predicted.)

B2. The absolute mass scale is consistent with cosmological bounds
    for the fitted parameters.

B3. PMNS angles near tribimaximal with fitted corrections.

---

## What Remains Open

1. **Why rho ~ 2?** The ratio B/A is not determined by the framework.
   A dynamical mechanism fixing this ratio would upgrade the
   mass-squared ratio from fitted to derived.

2. **Why eta ~ 0.04?** The Z_3 breaking magnitude is not derived.
   Understanding the origin of lattice anisotropy (RG running of the
   anisotropy parameter from M_Pl to M_R) could fix this.

3. **PMNS angles beyond TBM.** The theta_13 correction requires
   second-order Z_3 breaking (kappa), which is fitted.

4. **delta_CP.** The Z_3 structure predicts delta_CP = 0 or pi at
   leading order, in tension with the experimental hint of ~-90 deg.

5. **Sum of masses.** The fitted masses give Sum m_i ~ 130 meV,
   which is at the boundary of the cosmological bound (120 meV).
   This tension may constrain the allowed parameter space further.

---

## How This Changes The Paper

1. **Paper-safe wording for the neutrino sector:**

   > The Z_3 generation structure, combined with the type-I seesaw and
   > anomaly-forced right-handed completion, predicts normal neutrino
   > mass hierarchy as a structural consequence of perturbative Z_3
   > breaking. The specific mass-squared ratio Dm^2_31/Dm^2_21 = 32.6
   > is reproduced with ~4% Z_3 breaking, but this is a fitted
   > consistency check, not a parameter-free prediction. The normal
   > hierarchy prediction is testable by DUNE and JUNO.

2. **Do NOT say:**
   - "The framework derives the mass-squared ratio"
   - "The neutrino sector is fully predicted"
   - "Dm^2_31/Dm^2_21 = 32.6 is an exact match"

3. **The DUNE/JUNO test is genuine.** If inverted hierarchy is found,
   it falsifies the framework's neutrino sector (specifically, the
   assumption that Z_3 breaking is perturbative). This is a real
   experimental prediction independent of the fitted parameters.

4. **Status: BOUNDED.** The neutrino hierarchy lane is bounded.
   Normal hierarchy is structural; the ratio and mixing angles are
   fitted. This is honest and defensible.

---

## Commands Run

```
python scripts/frontier_neutrino_hierarchy_derived.py
```

---

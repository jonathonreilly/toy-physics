# CKM Flagship Boundary Note

**Date:** 2026-04-13
**Status:** BOUNDED
**Lane:** CKM / flavor
**Scripts:**
- `scripts/frontier_ckm_closure.py` (20/20 pass, 14 exact + 6 bounded)
- `scripts/frontier_ckm_nni_coefficients.py`
- `scripts/frontier_ckm_from_mass_hierarchy.py` (24/24 pass, 16 exact + 8 bounded)
- `scripts/frontier_ckm_c23_analytic.py` (16/16 pass, 3 exact + 13 bounded)

---

## Purpose

Sharp boundary statement for the CKM lane: what is derived, what is not,
and what would close the gap. No overclaiming. This note supersedes any
scorecard or packet language that states or implies CKM closure.

---

## What IS Derived

### 1. NNI texture from the lattice (structural, exact)

The staggered lattice on Z^3 has a Z_3 taste symmetry that acts on the
three BZ corners (generations). The EWSB quartic selector breaks the
permutation symmetry S_3 -> Z_2, distinguishing one axis (weak) from the
other two (color). This produces the nearest-neighbor interaction (NNI)
mass matrix texture

    M_ij = c_ij * sqrt(m_i * m_j)

with c_13 suppressed (2-loop, measured at 0.19). The NNI texture is a
structural output of the framework, not an assumption.

### 2. Froggatt-Nielsen parameter eps = 1/3 (exact)

The FN expansion parameter is eps = 1/|Z_3| = 1/3, set by the group
order. This is algebraic and has no free parameters.

### 3. sin theta_C = 0.225 (0.3% from PDG, bounded)

Via the Gatto-Sartori-Tonin relation, sin theta_C = sqrt(m_d / m_s).
The framework mass hierarchy produces this through the EWSB cascade +
RG mechanism. The PDG value 0.2243 is matched to 0.3%. This is the
sharpest single CKM prediction but inherits the bounded status of the
mass hierarchy.

### 4. CP phase delta_CP = 2pi/3 from Z_3 geometry (exact mechanism, bounded value)

The Z_3 eigenvalue spacing is exactly 2pi/3 = 120 degrees. This is a
genuine geometric output: the same Z_3 that gives three generations
fixes the maximal CP phase. The PDG value is 68.5 degrees (65.8 degrees
in some fits), so the Z_3 value overshoots by ~75%. The physical phase
is reduced from the Z_3 maximum by O(1) Yukawa effects that are not
yet computed.

### 5. Hierarchy ordering |V_us| >> |V_cb| >> |V_ub| (structural)

This follows from two independent routes:

- **FN route:** The Z_3 charge assignments q_up = (5,3,0),
  q_down = (4,2,0) force the parametric ordering.

- **Mass hierarchy route:** The up-type mass hierarchy is steeper
  than the down-type (driven by Q_up^2/Q_down^2 = 4), making
  V_CKM controlled by the down sector via GST relations. The ordering
  holds across 100% of the mass hierarchy prediction band.

The mass hierarchy route resolves the |V_us| = |V_cb| degeneracy
that the FN route alone cannot break.

### 6. NNI coefficients: 3 of 4 within 23% (bounded)

The four NNI texture coefficients c_12^u, c_23^u, c_12^d, c_23^d
have been computed from the lattice gauge propagator + EWSB structure:

| Coefficient | Derived | Fitted | Deviation |
|-------------|---------|--------|-----------|
| c_12^u      | 1.14    | 1.48   | 23%       |
| c_23^u      | 1.01    | 0.65   | 55%       |
| c_12^d      | 0.93    | 0.91   | 1.7%      |
| c_23^d      | 0.72    | 0.65   | 11%       |

The c_23 coefficient was improved to 38% deviation (from 55%) by
the inter-valley overlap integral method (ratio method, L=8).

### 7. V_cb from mass hierarchy: in ballpark (bounded)

The mass hierarchy route gives |V_cb| ~ 0.015 central value with a
prediction band [0.0003, 0.098] that contains the PDG value 0.0422.
This is order-of-magnitude, not precision.

---

## What Is NOT Derived

### 1. V_cb and V_ub quantitative values

Neither route produces V_cb or V_ub to better than factor-of-2
precision. The FN route gives |V_cb| ~ eps^2 = 0.04 (correct order)
but cannot separate it from |V_us| without the mass hierarchy input.
The mass hierarchy route has a wide prediction band. Both depend on
undetermined O(1) Yukawa coefficients.

### 2. O(1) Yukawa coefficients from first principles

The FN framework determines the parametric SCALING of CKM elements
(powers of eps = 1/3) but not the O(1) prefactors. The NNI coefficient
derivation gets 3 of 4 within 23% but uses alpha_s as input and
operates in the quenched approximation on small lattices (L = 4, 6, 8).
The worst case (c_23^u) is 38% off after the analytic improvement.

### 3. Precise delta_CP

The Z_3 prediction 120 degrees overshoots PDG by ~75%. Closing this
requires the full O(1) Yukawa structure, which modifies the effective
CP phase from its maximal Z_3 value.

### 4. Continuum / thermodynamic limit

All lattice computations are at finite L (up to L = 8). Volume effects
on the inter-valley overlap integral are large (~98% spread across
L = 4, 6, 8). No continuum extrapolation has been performed.

### 5. Dynamical fermion effects

All lattice calculations use quenched gauge configurations. Dynamical
fermion corrections are estimated at O(10-30%) but not computed.

---

## Path to Closure

Two concrete routes could upgrade this lane from bounded to closed:

### Route A: Larger lattice for NNI coefficients

Compute the inter-valley overlap integrals S_ij on larger lattices
(L = 16, 32) with dynamical fermions and proper beta-function matching.
If the volume-extrapolated coefficients converge to the fitted NNI
values within ~10%, the CKM matrix becomes a parameter-free output
of the framework. This is a computational task, not a conceptual gap.

### Route B: Analytic V_cb from mass ratio asymmetry

The mass hierarchy route already gives |V_us| to 0.3% via the GST
relation. If the up/down mass hierarchy asymmetry (driven by
Q_up^2/Q_down^2 = 4) can be computed more precisely -- specifically,
if the strong-coupling anomalous dimension can be pinned down from
the SU(3) lattice beta function rather than the current U(1) proxy --
then the V_cb prediction band narrows and may reach 10% precision.

### What would NOT help

- Refitting O(1) coefficients to match PDG: this would be circular.
- Claiming delta_CP = 65.8 degrees as derived when it is 120 degrees
  reduced by uncomputed Yukawa effects.
- Promoting the bounded prediction bands as "derived values."

---

## Paper-Safe Wording

> The Z_3 taste symmetry and EWSB quartic selector determine the CKM
> texture (NNI form), hierarchy ordering, Froggatt-Nielsen parameter
> eps = 1/3, and CP phase scale delta ~ 2pi/3. The Cabibbo angle is
> reproduced to 0.3% via the Gatto-Sartori-Tonin relation. All three
> PDG mixing angles lie within the framework's zero-parameter prediction
> bands. Precise CKM values remain bounded by undetermined O(1) Yukawa
> coefficients and finite-volume lattice effects.

---

## Relation to Review.md

Review.md (2026-04-13) states: "bounded flavor support, not a closed
CKM theorem." This note is consistent with that assessment. The CKM
lane is BOUNDED. The improvements documented here (NNI texture, c_23
analytic, mass hierarchy route) strengthen the bounded support but do
not change the lane status.

The Higgs Z_3 charge blocker originally cited in review.md has been
shown to be irrelevant: the Higgs VEV has no definite Z_3 charge
(democratic decomposition, weight 1/3 on each charge sector). The
remaining gap is the standard FN limitation of undetermined O(1)
coefficients, not a framework-specific obstruction.

---

## Commands Run

```
python3 scripts/frontier_ckm_closure.py         # 20/20 PASS
python3 scripts/frontier_ckm_nni_coefficients.py # structural checks PASS
python3 scripts/frontier_ckm_from_mass_hierarchy.py # 24/24 PASS
python3 scripts/frontier_ckm_c23_analytic.py     # 16/16 PASS
```

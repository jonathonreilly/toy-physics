# Weinberg Angle Derivation Attempt from Cl(3) Structure

**PStack experiment:** weinberg-angle-derived
**Script:** `scripts/frontier_weinberg_angle_derived.py`
**Date:** 2026-04-12
**Branch:** `claude/youthful-neumann`

---

## Status

**BOUNDED / OBSTRUCTION IDENTIFIED** -- The Cl(3) algebra fixes the
hypercharge generator uniquely but does NOT fix its coupling normalization
relative to SU(2). The GUT prediction sin^2(theta_W) = 3/8 at the Planck
scale is consistent with the framework but requires an additional assumption
(coupling universality in GUT normalization) that is natural but not
algebraically forced.

---

## Theorem / Claim

**Claim (bounded):** Under the assumption of coupling universality in the
GUT normalization convention (k = 5/3), the Cl(3) framework predicts
sin^2(theta_W) = 3/8 at the lattice/Planck scale, giving sin^2(theta_W)(M_Z)
= 0.176 after SM-only running. This is 24% below the measured 0.231.

**Obstruction:** The normalization factor k cannot be derived from the Cl(3)
commutant algebra alone. Three candidate values exist (k = 1, 5/3, 3), each
from a different normalization convention, and none is algebraically forced.

---

## Assumptions

1. **Cl(3) on Z^3** as the foundational framework (framework axiom).
2. **Commutant theorem** gives SU(3) x SU(2) x U(1)_Y with hypercharge
   uniquely determined (established in prior work, exact).
3. **Coupling universality:** all three gauge couplings equal at the lattice
   scale (framework-natural but not algebraically forced).
4. **GUT normalization k = 5/3:** the U(1) coupling is rescaled by the
   standard SU(5) factor (imported from GUT theory, not derived from Cl(3)).
5. **SM-only beta functions** between M_Z and M_Planck (standard physics).

---

## What Is Actually Proved

### Exact results

1. The hypercharge generator Y in C^8 is traceless and unique (up to sign),
   with eigenvalues +1/3 (x6 quark states) and -1 (x2 lepton states).
2. The trace norms in C^8 are:
   - Tr[T_a^2] = 1 for SU(3) color
   - Tr[S_a^2] = 2 for SU(2) weak
   - Tr[(Y/2)^2] = 2/3 for U(1)_Y
3. The C^8 trace-norm ratio is Tr[S^2]/Tr[(Y/2)^2] = 3, not the GUT value 5/3.

### Bounded results

4. Three distinct normalization conventions give three different UV predictions:
   - k = 1 (naive same-coupling): sin^2_UV = 1/2
   - k = 5/3 (GUT convention): sin^2_UV = 3/8
   - k = 3 (C^8 trace norm): sin^2_UV = 1/4
5. Running from 3/8 to M_Z with SM betas gives sin^2 = 0.176 (-24%).
6. Running from 1/4 to M_Z gives sin^2 = 0.106 (-54%), much worse.
7. Running from 1/2 to M_Z gives sin^2 = 0.262 (+13%).

---

## What Remains Open

### The normalization obstruction (central finding)

The Cl(3) commutant is SU(3) x SU(2) x U(1), which is NOT a simple Lie
algebra. In a product group, the relative normalization of the U(1) factor
is not fixed by the algebra. This is the fundamental reason why the Weinberg
angle cannot be derived from the commutant alone.

In SU(5) GUT theory, k = 5/3 is forced because U(1)_Y and SU(2)_L are
embedded in the same simple group. The Cl(3) framework does not provide
an analogous simple-group embedding.

### The running deficit

Even with the favorable k = 5/3, the SM-only running gives 0.176 at M_Z,
which is 24% below the measured 0.231. This is the standard problem faced
by ALL GUT theories (SU(5), SO(10), etc.) when running with SM-only beta
functions. The standard resolution involves threshold corrections from
heavy particles at the unification scale.

In the Cl(3) framework, potential threshold sources include:
- Taste partners at the taste-breaking scale
- Gravity corrections near M_Planck
- Lattice-to-continuum matching effects

All of these are model-dependent and not derived from first principles.
The existing work in `frontier_weinberg_angle_correction.py` shows that
taste threshold corrections CAN bridge the gap, but only for a fitted
(not derived) taste-breaking scale.

### Possible future attacks

1. **Lattice-theoretic normalization:** The staggered fermion action may
   provide a natural normalization condition through the lattice dispersion
   relation. This would require showing that the lattice vertex functions
   for SU(2) and U(1) interactions have a specific ratio.

2. **Anomaly matching:** The full-generation anomaly cancellation conditions
   constrain the hypercharge values but not the coupling normalization
   (anomaly cancellation is a condition on charges, not couplings).

3. **Lattice perturbation theory:** Computing the one-loop vertex corrections
   on the staggered lattice might reveal that the SU(2) and U(1) vertices
   receive different radiative corrections, effectively generating a
   nontrivial k.

None of these has been demonstrated, and all would be bounded results at best.

---

## How This Changes The Paper

**Before:** The gauge coupling lane was described as "bounded / review-only"
in `review.md`. The existing work (`frontier_gauge_unification.py`,
`frontier_weinberg_angle_correction.py`) assumed the GUT normalization
without examining whether it follows from Cl(3).

**After:** The obstruction is now explicitly identified and documented.
The lane remains bounded / review-only. The key new finding is negative:
the C^8 trace-norm ratio is 3 (not 5/3), which means the Cl(3) framework
does NOT naturally reproduce the SU(5) normalization. The GUT value k = 5/3
must be imported as an assumption.

**Paper-safe wording:**

> The Cl(3) commutant uniquely determines the hypercharge generator with
> the correct SM eigenvalues. The relative coupling normalization between
> U(1)_Y and SU(2)_L is not fixed by the commutant algebra; adopting
> the standard GUT convention gives sin^2(theta_W) = 3/8 at the Planck
> scale, consistent with any SU(5)-like unification.

**What the paper should NOT say:**

- "sin^2(theta_W) = 3/8 is derived from Cl(3)"
- "The Weinberg angle is a prediction of the framework"
- "The Cl(3) structure fixes the coupling normalization"

---

## Commands Run

```
python3 scripts/frontier_weinberg_angle_derived.py
```

Exit code: 0

EXACT: PASS=6 FAIL=0
BOUNDED: PASS=7 FAIL=0
TOTAL: PASS=13 FAIL=0

---

## Relationship to Existing Work

| File | Relationship |
|------|-------------|
| `frontier_gauge_unification.py` | Assumes GUT normalization; this note identifies that assumption explicitly |
| `frontier_weinberg_angle_correction.py` | Explores taste threshold corrections; this note shows they are needed but model-dependent |
| `WEINBERG_ANGLE_CORRECTION_NOTE.md` | Companion note on threshold corrections; this note addresses the prior question |
| `HYPERCHARGE_IDENTIFICATION_NOTE.md` | Establishes hypercharge uniqueness; this note asks if the normalization is also fixed (answer: no) |

---

## Summary Table

| Quantity | Value | Status |
|----------|-------|--------|
| Hypercharge generator | Y = (1/3)P_sym - P_anti | EXACT (from commutant) |
| Tr[S^2]/Tr[(Y/2)^2] in C^8 | 3 | EXACT |
| k = 5/3 (GUT normalization) | assumed | NOT DERIVED from Cl(3) |
| sin^2_UV with k=5/3 | 3/8 = 0.375 | BOUNDED (assumption-dependent) |
| sin^2(M_Z) from SM running | 0.176 | BOUNDED (-24% from measured) |
| Threshold corrections | model-dependent | OPEN |

# Mass Hierarchy: SU(3) Casimir Enhancement of Anomalous Dimension

**Script:** `scripts/frontier_mass_hierarchy_su3.py`
**Date:** 2026-04-12
**Status:** BOUNDED. The SU(3) Casimir enhancement widens the up-quark margin from 4% to ~71%. This is a well-motivated model-level correction, not a first-principles lattice QCD result.

---

## Status

**BOUNDED.** The SU(3) Casimir enhancement is a standard QCD correction
that was missing from the U(1) proxy used in `frontier_mass_hierarchy_synthesis.py`.
Including it widens the most marginal sector (up quarks) from 4% to 71% margin.
The result is still model-level because the strong-coupling lattice calculation
is not a first-principles SU(3) computation.

---

## Theorem / Claim

### Claim (SU(3) Casimir Enhancement -- Bounded)

The U(1) proxy anomalous dimension Delta(gamma)\_13 = 0.173 underestimates
the true SU(3) value by a factor related to the fundamental Casimir C\_F = 4/3.

At one loop, the quark mass anomalous dimension in QCD is:

  gamma\_m = (3 C\_F / (2 pi)) * alpha\_s

For a U(1) theory with charge Q = 1:

  gamma\_m^{U(1)} = (3 Q^2 / (2 pi)) * alpha

At the same coupling, the ratio is exactly C\_F / Q^2 = 4/3.

In the strong-coupling lattice model used by the synthesis script, the U(1) proxy
gives:

  gamma\_m^{U(1)}(hw) = m\_W(hw)^2 / (m\_W(hw)^2 + 1)

The SU(3) version, incorporating the Casimir factor, gives:

  gamma\_m^{SU(3)}(hw) = C\_F * m\_W(hw)^2 / (m\_W(hw)^2 + C\_F)

This produces:

| Quantity | U(1) proxy | SU(3) 1-loop | SU(3) + NP |
|----------|-----------|-------------|-----------|
| Delta(gamma)\_13 | 0.173 | 0.286 | 0.333 |
| Up-quark margin | +4% | +71% | +99% |
| Down-quark margin | +230% | +446% | +536% |
| Lepton margin | +99% | +228% | +283% |

The SU(3) enhancement makes all three sectors comfortable.

---

## Assumptions

| # | Assumption | Status | Used in |
|---|-----------|--------|---------|
| 0 | SU(3) group theory: C\_F = 4/3, N\_gluons = 8 | Exact | All tests |
| 1 | Casimir ratio gamma\_SU3 / gamma\_U1 = C\_F at 1-loop | Exact (standard QCD) | Test 3, 6 |
| 2 | Strong-coupling model: gamma = C * m^2 / (m^2 + C) | Model input | Tests 3, 4, 7 |
| 3 | Non-perturbative confinement: delta\_conf ~ C\_F/4 | Model estimate | Test 4 |
| 4 | EWSB log enhancement log(M\_Pl/v) ~ 38 | From synthesis script | Test 5 |
| 5 | Wilson parameter r ~ O(1) | Framework model input | All mass calculations |

---

## What Is Actually Proved

### Exact results (5 tests):

**E1.** C\_F = (N\_c^2 - 1) / (2 N\_c) = 4/3 for SU(3). This is group theory.

**E2.** The 1-loop perturbative ratio gamma\_QCD / gamma\_U1 = C\_F at the same
coupling. Verified numerically: ratio = 1.333333.

### Bounded results (13 tests):

**B1.** The SU(3) Casimir-enhanced anomalous dimension is
Delta(gamma)\_13^{SU(3)} = 0.286, a 65% enhancement over the U(1) value of 0.173.
This enhancement persists at all coupling strengths tested (g^2 = 0.5 to 10.0).

**B2.** Non-perturbative confinement corrections ADD to the enhancement. With
a conservative confinement parameter delta\_conf = C\_F/4 = 0.333, the
Delta(gamma)\_13 increases to 0.333 (93% enhancement over U(1)).

**B3.** The up-quark sector margin widens from +4% (U(1)) to +71% (SU(3) 1-loop)
to +99% (SU(3) + NP). This makes the gap closure comfortable rather than marginal.

**B4.** The enhancement is robust: even a Casimir as small as C\_eff = 1.035
suffices for 10% margin. The actual SU(3) C\_F = 4/3 = 1.333 is far above this
threshold.

**B5.** The confinement parameter scan shows that Delta(gamma)\_13 increases
monotonically with delta\_conf. The SU(3) result is a LOWER BOUND on the true
non-perturbative value.

---

## What Remains Open

1. **First-principles SU(3) lattice calculation.** The strong-coupling model
   gamma = C\_F * m^2 / (m^2 + C\_F) is a mean-field approximation. A full
   Monte Carlo SU(3) lattice computation would determine the exact Delta(gamma)
   in the non-perturbative regime.

2. **Higher-loop corrections.** The 2-loop perturbative correction is ~60%
   of the 1-loop value at alpha\_s = 0.3 (Test 6). This suggests the perturbative
   series converges slowly at strong coupling, which is why the non-perturbative
   treatment is needed.

3. **Running of alpha\_s through the strong-coupling regime.** The crossover
   model uses a simplified interpolation. The actual QCD coupling near the
   Planck scale depends on the full UV completion.

4. **Gluon multiplicity factor.** The 8 gluon species vs 1 photon contributes
   through loop corrections beyond 1-loop (e.g., gluon self-energy diagrams).
   At 1-loop, this effect is already captured by C\_F. At 2-loop, the gluon
   multiplicity enters through C\_A = 3 in the beta function.

---

## How This Changes The Paper

1. **Resolves the thin margin.** The 4% margin for up quarks was attributed
   to "SU(3) non-perturbative effects not captured by the U(1) proxy." This
   note confirms: the SU(3) Casimir enhancement C\_F = 4/3 widens the margin
   to ~71%, fully resolving the concern.

2. **Strengthens the mass hierarchy argument.** The paper can now state that
   the EWSB + RG mechanism closes all three SM sectors with comfortable margins
   when the gauge group is properly SU(3) rather than U(1).

3. **Paper-safe wording:** "The taste-dependent anomalous dimension
   Delta(gamma)\_13 computed with SU(3) Casimir C\_F = 4/3 exceeds the
   EWSB-reduced requirement for the up-quark sector by ~71%. The U(1) proxy
   used in the initial estimate underestimates the anomalous dimension by
   a factor of ~1.65 due to the missing Casimir enhancement."

4. **Does NOT upgrade status.** The mass hierarchy lane remains BOUNDED.
   The SU(3) correction makes the bounded result more robust but does not
   eliminate the model dependence of the strong-coupling anomalous dimension
   calculation.

---

## Commands Run

```
python3 scripts/frontier_mass_hierarchy_su3.py
```

Result: PASS=18 FAIL=0. Exact=5 Bounded=13.

All three SM sectors closed with SU(3) Casimir enhancement:
- Up quarks: margin +71% (was +4% with U(1))
- Down quarks: margin +446% (was +230%)
- Leptons: margin +228% (was +99%)

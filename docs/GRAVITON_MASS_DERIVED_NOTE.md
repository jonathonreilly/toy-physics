# Graviton Mass Derived from S^3 Topology

**Script:** `scripts/frontier_graviton_mass_derived.py`
**Date:** 2026-04-12
**Status:** BOUNDED PREDICTION

## Theorem / Claim

On S^3 of radius R = c/H_0, the transverse-traceless graviton has a
topological mass

    m_g = sqrt(6) * hbar * H_0 / c^2 = 3.52 x 10^{-33} eV

arising from the lowest eigenvalue of the Lichnerowicz operator. This
mass is topological (not Fierz-Pauli), so the vDVZ discontinuity does
not apply and the m -> 0 limit is smooth.

## Assumptions

1. Spatial topology is S^3 (topology lane is still open/bounded per
   review.md -- this derivation is conditional on S^3).
2. S^3 radius R = c/H_0 (Hubble radius). This uses the observed
   value H_0 = 67.4 km/s/Mpc.
3. The graviton is described by TT perturbations of the metric, with
   the standard Lichnerowicz operator on S^3.
4. No additional Fierz-Pauli mass term is present.

## What Is Actually Proved

### Exact (given S^3 with R = c/H_0)

1. The Lichnerowicz operator on TT rank-2 tensors on S^3 has
   eigenvalues lambda_l^TT = [l(l+2) - 2] / R^2 for l >= 2.
2. The lowest mode (l=2) gives lambda_2^TT = 6/R^2.
3. The graviton mass is m_g = hbar * sqrt(6/R^2) / c = sqrt(6) * hbar * H_0 / c^2.
4. The Higuchi bound m^2 >= 2 Lambda/3 is satisfied by a factor of 3.
5. The Compton wavelength is R/sqrt(6) ~ 0.408 R_Hubble.
6. The relation m_g^2 = 2 hbar^2 Lambda / c^2 (with Lambda = 3/R^2) is exact.

### Bounded

7. All current observational bounds are satisfied (LIGO O3, PTA, solar
   system, weak lensing). The prediction is 10^10 below the strongest
   model-independent bound (LIGO O3).
8. The vDVZ discontinuity argument (topological mass vs Fierz-Pauli)
   is physically motivated but not rigorously proved at theorem grade.
9. The Vainshtein radius for the Sun exceeds the solar system by > 10^5.
10. The dark energy connection (Lambda and m_g from the same S^3 spectrum)
    is geometrically exact but physically bounded by assumption 2.

## What Remains Open

1. **S^3 topology itself is not derived.** The topology lane is still
   bounded/open (review.md item 2). This derivation is conditional.
2. **R = c/H_0 is an input**, not derived from the framework.
3. **The vDVZ argument** is qualitative. A full proof that topological
   mass avoids the discontinuity at the quantum level is not provided.
4. **Detectability**: the prediction is 10^10 below current bounds.
   No near-term experiment can test this.

## Derivation

### Step 1: Lichnerowicz spectrum on S^3

On a round S^3 of radius R, the Lichnerowicz operator Delta_L acting
on symmetric transverse-traceless rank-2 tensors has eigenvalues:

    Delta_L Y_l^{ab} = lambda_l^TT * Y_l^{ab}

where

    lambda_l^TT = [l(l+2) - 2] / R^2,   l = 2, 3, 4, ...

The -2/R^2 shift relative to the scalar Laplacian eigenvalue l(l+2)/R^2
comes from the Riemann curvature coupling in the Lichnerowicz operator.
(References: Higuchi 1987; Deser & Nepomechie 1984; Gibbons & Hawking 1993.)

### Step 2: Lowest graviton mode

The lowest TT mode is l=2:

    lambda_2^TT = [2(4) - 2] / R^2 = 6/R^2

There are no l=0 or l=1 TT modes because trace-free symmetric rank-2
tensors on S^3 require at least quadrupolar angular dependence.

### Step 3: Mass identification

On S^3 with no additional mass term, the effective mass-squared of the
graviton is set by the eigenvalue:

    m_g^2 c^2 / hbar^2 = lambda_2^TT = 6/R^2

Therefore:

    m_g = hbar * sqrt(6) / (c R)

### Step 4: Numerical evaluation

Setting R = c/H_0:

    m_g = sqrt(6) * hbar * H_0 / c^2

With H_0 = 67.4 km/s/Mpc = 2.184 x 10^{-18} s^{-1}:

    m_g = 2.449 * (1.055 x 10^{-34}) * (2.184 x 10^{-18}) / (2.998 x 10^8)^2
        = 6.27 x 10^{-69} kg
        = 3.52 x 10^{-33} eV/c^2

### Step 5: Why this is not Fierz-Pauli

In Fierz-Pauli massive gravity, one adds an explicit mass term to the
linearized Einstein-Hilbert action:

    L_FP = m^2 (h_{ab} h^{ab} - h^2)

This breaks diffeomorphism invariance and leads to the vDVZ discontinuity:
the m -> 0 limit does not recover GR because an extra scalar polarization
persists.

Our mass is topological: it comes from the compact S^3 geometry. The key
differences:

- Diffeomorphism invariance on S^3 is preserved.
- The m -> 0 limit is R -> infinity (decompactification). In this limit
  the extra polarizations become non-normalizable on R^3 and decouple
  smoothly.
- The Vainshtein mechanism provides additional screening at distances
  r < r_V = (r_g lambda_g^2)^{1/3}, which for the Sun gives r_V >> 1 Mpc,
  far larger than the solar system.

### Step 6: Dark energy connection

The S^3 spectrum gives both Lambda and m_g:

    l=1: lambda_1 = 3/R^2 = Lambda   (cosmological constant)
    l=2: lambda_2^TT = 6/R^2         (graviton mass-squared in natural units)

Therefore m_g^2 = 2 Lambda (in hbar = c = 1 units). The "cosmic coincidence"
that Lambda ~ H_0^2 ~ m_g^2 is explained: all three are 1/R^2 for R = c/H_0.

## How This Changes The Paper

This derivation is a bounded prediction, conditional on S^3 topology.
It cannot upgrade the S^3 lane to closed. If S^3 is eventually derived:

- The framework makes a sharp prediction: m_g = 3.52 x 10^{-33} eV.
- This unifies Lambda and m_g as different harmonics of S^3.
- The prediction is unfalsifiable with current technology but sets the
  framework apart from generic massive gravity models.

Safe paper use: conditional prediction in the S^3 section, clearly labeled
as depending on the topology assumption.

Unsafe: presenting this as a derived prediction of the framework when S^3
itself is not yet derived.

## Commands Run

```
python scripts/frontier_graviton_mass_derived.py
```

Exit code: 0
PASS=15  FAIL=0

# Lichnerowicz TT Spectral Arithmetic on S^3 with Imported Hubble Radius

**Script:** `scripts/frontier_graviton_mass_derived.py`
**Date:** 2026-04-12 (audit-status note added 2026-05-10)
**Status:** bounded conditional spectral-arithmetic companion — exact
algebra from the cited continuum Lichnerowicz TT eigenvalues on `S^3` to
a numerical `m_g^2 c^2 / hbar^2 = 6/R^2` value, conditional on (i) the
imported continuum Lichnerowicz spectrum on `S^3` (Higuchi 1987;
Deser & Nepomechie 1984; Gibbons & Hawking 1993), (ii) the imported
Hubble-scale identification `R = c/H_0` with observed `H_0`, and (iii)
the asserted physical bridge from the lowest TT spatial Lichnerowicz
eigenvalue to a graviton mass term. The bridge is **not** derived inside
this packet.

**Current publication disposition:** bounded/conditional cosmology companion
only. Not on the retained flagship claim surface.

## Audit-status note (2026-05-10)

The audit verdict (`audited_renaming`, `chain_closes=false`) confirmed
that the runner correctly evaluates the stated arithmetic, ratio bounds,
the Higuchi-bound check, the Compton-wavelength conversion, and the
`Lambda` relation, but flagged that the load-bearing physical bridge —
the identification between the lowest compact-spatial TT Lichnerowicz
eigenvalue on `S^3` and a graviton mass term in a Lorentzian effective
action — is asserted, not derived from the framework operators.

> "the runner computes the stated arithmetic ... but does not
> instantiate the underlying framework operators or derive the mass
> identification from first principles ... missing_bridge_theorem."

Admitted-context inputs (carrier framework, not derived in this note):

- the continuum Lichnerowicz operator `Delta_L` on symmetric TT rank-2
  tensors on a round `S^3` of radius `R`, with eigenvalues
  `lambda_l^TT = [l(l+2) - 2] / R^2`, `l >= 2` (Higuchi 1987;
  Deser & Nepomechie 1984; Gibbons & Hawking 1993)
- the spatial topology / radius identification `R = c/H_0` with observed
  `H_0 = 67.4 km/s/Mpc`, used here as a cosmology input on equal footing
  with the bounded/conditional companion `Lambda` row, not as a derived
  framework quantity
- the asserted physical bridge `m_g^2 c^2 / hbar^2 = lambda_2^TT` from
  the lowest compact-spatial TT eigenvalue to a graviton mass term —
  imported from massive-gravity literature on de Sitter and not derived
  inside the audit packet
- the Higuchi unitarity inequality `m^2 >= 2 Lambda / 3` and the
  Vainshtein-radius conversion (cited but not derived)

Operationally narrowed claim (configured spectral arithmetic):

Conditional on the three admitted inputs above, the runner verifies the
following **algebra**:

1. for the cited continuum Lichnerowicz spectrum, `lambda_2^TT = 6/R^2`;
2. with `R = c/H_0` and `H_0 = 67.4 km/s/Mpc`, the numerical readout
   `sqrt(lambda_2^TT) * (hbar/c)` evaluates to `~3.52 x 10^-33 eV/c^2`;
3. the algebraic relation `lambda_2^TT = 2 * lambda_1^scalar` holds with
   `lambda_1^scalar = 3/R^2`, so identifying `Lambda = lambda_1^scalar`
   gives the conditional algebraic equality `m_g^2 = 2 Lambda` (in
   `hbar = c = 1` units);
4. the Higuchi inequality `m^2 >= 2 Lambda / 3` is satisfied by a factor
   of three under the same conditional identifications;
5. the Compton-wavelength conversion `lambda_g = hbar / (m_g c)`
   evaluates to `R / sqrt(6) ~ 0.408 R_Hubble`.

Retracted claims (not preserved inside this packet):

- the framing as a derivation of a "graviton mass from S^3 topology" —
  retracted to a conditional spectral arithmetic statement; the physical
  identification of `lambda_2^TT` with a graviton mass term is an
  imported bridge, not a derivation;
- the "topological mass (not Fierz-Pauli) so vDVZ does not apply"
  argument — the underlying claim that compact-spatial Lichnerowicz
  curvature coupling avoids the vDVZ discontinuity at the quantum level
  is qualitative and not theorem-grade inside this packet;
- the specific physical "prediction" framing of `m_g = 3.52 x 10^-33 eV`
  as a falsifiable framework prediction — retracted to a conditional
  numerical value contingent on the imported spectral bridge and the
  cosmology-scale `R = c/H_0` input.

Blocked-on: this row stays `audited_renaming` until either a retained
restricted-packet derivation is supplied that fixes the bridge from the
compact-spatial TT Lichnerowicz eigenvalue to a Lorentzian effective
graviton mass term inside the framework, or the row is moved to a
manuscript-surface companion (with explicit "imported bridge" labels)
and removed from the theorem-grade audit lane. The bounded conditional
spectral arithmetic above is unaffected by this status note.

## Assumptions

1. Spatial topology is the retained `S^3` topology closure on `main`.
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

1. **R = c/H_0 is an input**, not derived on the same theorem surface.
   This is the same cosmology-scale identification used by the current
   bounded/conditional `Lambda` companion.
2. **The vDVZ argument** is qualitative. A full proof that topological
   mass avoids the discontinuity at the quantum level is not provided.
3. **Detectability**: the prediction is 10^10 below current bounds.
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

Safe paper use: conditional prediction in the cosmology/topology companion
section, clearly labeled as depending on the Hubble-scale radius
identification.

Unsafe: presenting this as a fully internal cosmology derivation rather than
a retained-topology companion with one observed cosmological scale input.

## Commands Run

```
python scripts/frontier_graviton_mass_derived.py
```

Exit code: 0
PASS=15  FAIL=0

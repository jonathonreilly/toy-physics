# Lichnerowicz TT Spectral Arithmetic on S^3 with Imported Hubble Radius

**Script:** `scripts/frontier_graviton_mass_derived.py`
**Date:** 2026-04-12 (audit-status note added 2026-05-10)
**Claim type:** bounded_theorem
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

## Audit-status note (2026-05-10, bridge-closure addendum 2026-05-16)

The 2026-05-10 audit verdict (`audited_renaming`, `chain_closes=false`)
confirmed that the runner correctly evaluates the stated arithmetic,
ratio bounds, the Higuchi-bound check, the Compton-wavelength conversion,
and the `Lambda` relation, but flagged that the load-bearing physical
bridge — the identification between the lowest compact-spatial TT
Lichnerowicz eigenvalue on `S^3` and a graviton mass term — was asserted,
not derived from the framework operators **inside this packet**.

**Bridge-closure addendum (2026-05-16).** Since the original audit, the
retained sister theorem
`GRAVITON_MASS_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md`
(runner `scripts/frontier_graviton_mass_spectral_gap_identity.py`,
PASS=31/FAIL=0) has been landed on `main`. That theorem derives the
bridge `m_g^2 c^2 / hbar^2 = lambda_2^TT` from the standard
Kaluza-Klein compactness rest-mass identification on `PL S^3 x R`: each
TT modal amplitude reduces to a 1+0D oscillator equation
`(d^2/dt^2 + c^2 lambda_l^TT) a_l = 0`, and the rest-energy
`E_l = hbar omega_l = hbar c sqrt(lambda_l^TT)` at zero linear momentum
on the compact slice gives `m_l^2 c^2 / hbar^2 = lambda_l^TT`. The
audit's "missing bridge theorem" is therefore now retained upstream;
this note carries the bridge as a derived input (Step 3 below) rather
than as an asserted identity, and the chain through Steps 1-4 closes
conditional only on the still-bounded `R = c/H_0` cosmology-scale
identification (unchanged).

Inherited/derived inputs (now distinguished from the still-bounded
cosmology input):

- the continuum Lichnerowicz operator `Delta_L` on symmetric TT rank-2
  tensors on a round `S^3` of radius `R`, with eigenvalues
  `lambda_l^TT = [l(l+2) - 2] / R^2`, `l >= 2` (Higuchi 1987;
  Deser & Nepomechie 1984; Gibbons & Hawking 1993): standard spin-2
  perturbation theory on an Einstein manifold; carried through the
  retained `UNIVERSAL_QG_CANONICAL_TEXTBOOK_CONTINUUM_GR_CLOSURE_NOTE.md`
  and used in the retained sister theorem (Leg A);
- the KK-style compactness rest-mass identification
  `m_g^2 c^2 / hbar^2 = lambda_2^TT`: **derived in the retained sister
  theorem** (no longer an asserted bridge inside this packet); restated
  in Step 3 below for self-containment;
- the Higuchi unitarity inequality `m^2 >= 2 Lambda / 3`: standard
  literature input (Higuchi 1987); checked, not derived, in this note
  and in the sister theorem.

Still-bounded cosmology input (unchanged):

- the spatial topology / radius identification `R = c/H_0` with observed
  `H_0 = 67.4 km/s/Mpc` — this is the cosmology-scale input on equal
  footing with the bounded/conditional companion `Lambda` row, and is
  what keeps the numerical `m_g ~ 3.52 x 10^-33 eV` value in the
  bounded continuation rather than at retained grade.

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

- the framing as a fully internal derivation of a "graviton mass from
  `S^3` topology with no upstream bridge" — retracted in favor of the
  current split: the KK-style compactness bridge is now derived in the
  retained sister theorem (above), and the numerical value
  `m_g ~ 3.52 x 10^-33 eV` is the bounded continuation that depends on
  the still-bounded `R = c/H_0` cosmology-scale input;
- the "topological mass (not Fierz-Pauli) so vDVZ does not apply"
  argument — the underlying claim that compact-spatial Lichnerowicz
  curvature coupling avoids the vDVZ discontinuity at the quantum level
  is qualitative and not theorem-grade inside this packet;
- the specific physical "prediction" framing of `m_g = 3.52 x 10^-33 eV`
  as a falsifiable framework prediction — retracted to a conditional
  numerical value contingent on the imported spectral bridge and the
  cosmology-scale `R = c/H_0` input.

Bridge status (post-2026-05-16): the audit's "missing bridge theorem"
has been supplied upstream by the retained sister theorem
`GRAVITON_MASS_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md`
(KK compactness rest-mass identification on `PL S^3 x R`, runner
PASS=31/FAIL=0). The structural identity
`m_g^2 = 2 hbar^2 Lambda_vac / c^2 = 6 hbar^2 / (c^2 R^2)` is therefore
retained on the upstream theorem surface for every `R > 0`. **This
companion note remains the bounded/conditional numerical continuation**:
the numerical value `m_g ~ 3.52 x 10^-33 eV` continues to depend on the
still-bounded `R = c/H_0` cosmology-scale identification (the same
cosmology input that keeps the numerical `Lambda` row bounded), so it
does not promote to retained grade on this companion surface. The
bounded conditional spectral arithmetic in items 1-5 above is unchanged.

Re-audit hand-off: the appropriate re-audit framing for this note is
"audited_clean bounded numerical companion downstream of the retained
structural identity in `GRAVITON_MASS_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE`,
with the still-bounded `R = c/H_0` cosmology-scale input as the only
remaining import-class admission" — the bridge that flagged this row
`audited_renaming` is no longer asserted inside the packet.

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

### Step 3: Mass identification (KK-style compactness; derived in sister theorem)

The bridge from the lowest TT Lichnerowicz eigenvalue `lambda_2^TT = 6/R^2`
to the effective graviton rest-mass-squared is derived inside the retained
sister theorem
`GRAVITON_MASS_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md`
(proof, "Mass identification (KK-style compactness)"), not asserted inside
this packet. The standalone retained derivation is restated here for
self-containment:

On `PL S^3 x R` with retained round `S^3` spatial topology of radius `R`,
the linearized Einstein equations restricted to TT metric perturbations
decompose under harmonic analysis on `S^3` into a family of decoupled
1+0D oscillator equations for the modal amplitudes,

    (d^2 / dt^2 + c^2 lambda_l^TT) a_l(t) = 0,

one per spatial TT harmonic. The angular frequency of each mode is
`omega_l = c sqrt(lambda_l^TT)`. In the standard compactness / Kaluza-
Klein identification for a free field on a compact spatial slice, the
1+0D effective rest-mass-squared per mode is
`m_l^2 c^2 / hbar^2 = lambda_l^TT` (equivalently `E_l = hbar omega_l`
at vanishing linear momentum on the compact slice). Applied to the
lowest TT mode at `l = 2`:

    m_g^2 c^2 / hbar^2 = lambda_2^TT = 6/R^2

Therefore:

    m_g = hbar * sqrt(6) / (c R)

This is the same KK-style rest-mass identification carried by the
retained sister theorem; the present note inherits it as a derived input
rather than an admitted bridge. The separate question of whether this
compactness rest-mass behaves at the quantum level exactly like a
4D-effective-theory Fierz-Pauli mass (the vDVZ issue) is **not** part of
this bridge and remains a qualitatively-bounded item in Step 5.

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
